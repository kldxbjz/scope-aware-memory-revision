"""Where the Answer Agent's base model runs (baseline.Generator), and how the larger reader of docs/analysis.md
("Larger reader") runs correctly and in reasonable time on two 48 GB GPUs.

load_reader(model_dir) returns the model in bfloat16, ready for generate():
  * one GPU: the whole model on it, as for every 4B run;
  * two or more GPUs: the decoder layers in two halves, the first half with the embeddings, the final norm and the
    output layer on cuda:0, the second half on cuda:1. Tensors that cross between the GPUs are copied through host
    memory, never from GPU to GPU: the first smoke run (2026-11-25, two L40S GPUs, accelerate's direct copies)
    answered every probe with garbage, and on 2026-11-26 spread_check.py found all 40 direct copies between the two
    L40S GPUs of another node different from the source, although the driver reports peer access (0 of 20 copies
    through host memory differed).
Qwen3-MoE blocks (the larger reader) run expert_loop: transformers' own Qwen3MoeSparseMoeBlock.forward with the
routing sorted once per layer. It runs the same experts in the same order, each on the same tokens in the same order,
so every operation and its result stay the same (spread_check.py compares them bit for bit); only the host no longer
waits for the GPU twice at every expert (24 greedy tokens for four prompts: 6.0 s instead of 8.6 s on two L40S GPUs).
"""
import inspect
import sys

import torch
import torch.nn.functional as F
from transformers import AutoConfig, AutoModelForCausalLM

ORIGINAL = {}  # transformers' own forward of a patched class, for spread_check.py
# statements of transformers' Qwen3MoeSparseMoeBlock.forward that expert_loop reproduces; another implementation
# (a later transformers) stops the run instead of being replaced silently
MOE_STATEMENTS = ("routing_weights = F.softmax(router_logits, dim=1, dtype=torch.float)",
                  "torch.topk(routing_weights, self.top_k, dim=-1)",
                  "routing_weights /= routing_weights.sum(dim=-1, keepdim=True)",
                  "expert_hit = torch.greater(expert_mask.sum(dim=(-1, -2)), 0).nonzero()",
                  "idx, top_x = torch.where(expert_mask[expert_idx].squeeze(0))",
                  "current_state = hidden_states[None, top_x].reshape(-1, hidden_dim)",
                  "current_hidden_states = expert_layer(current_state) * routing_weights[top_x, idx, None]",
                  "final_hidden_states.index_add_(0, top_x, current_hidden_states.to(hidden_states.dtype))")


def expert_loop(self, hidden_states):
    """Qwen3MoeSparseMoeBlock.forward of transformers with the routing sorted once per layer. transformers loops over
    the experts that received tokens in ascending order, and torch.where gives each expert's (slot, token) pairs in
    row-major order of the [top_k, tokens] mask; a stable sort of the slot-major expert list gives the same pairs in
    the same order, with one wait for the host per layer instead of two per expert."""
    batch_size, sequence_length, hidden_dim = hidden_states.shape
    hidden_states = hidden_states.view(-1, hidden_dim)
    router_logits = self.gate(hidden_states)
    routing_weights = F.softmax(router_logits, dim=1, dtype=torch.float)
    routing_weights, selected_experts = torch.topk(routing_weights, self.top_k, dim=-1)
    if self.norm_topk_prob:
        routing_weights /= routing_weights.sum(dim=-1, keepdim=True)
    routing_weights = routing_weights.to(hidden_states.dtype)
    final_hidden_states = torch.zeros((batch_size * sequence_length, hidden_dim), dtype=hidden_states.dtype,
                                      device=hidden_states.device)
    tokens = hidden_states.shape[0]
    chosen = selected_experts.t().reshape(-1)  # entry slot * tokens + token: that token's expert in that slot
    order = torch.sort(chosen, stable=True).indices
    counts = torch.bincount(chosen, minlength=self.num_experts).tolist()
    slots, token_ids = order // tokens, order % tokens
    start = 0
    for expert_idx, count in enumerate(counts):
        if count == 0:
            continue
        idx, top_x = slots[start:start + count], token_ids[start:start + count]
        start += count
        current_state = hidden_states[None, top_x].reshape(-1, hidden_dim)
        current_hidden_states = self.experts[expert_idx](current_state) * routing_weights[top_x, idx, None]
        final_hidden_states.index_add_(0, top_x, current_hidden_states.to(hidden_states.dtype))
    final_hidden_states = final_hidden_states.reshape(batch_size, sequence_length, hidden_dim)
    return final_hidden_states, router_logits


def patch_moe(model):
    """Number of Qwen3-MoE blocks in model, after their class runs expert_loop (0: nothing changed)."""
    try:
        from transformers.models.qwen3_moe import modeling_qwen3_moe as qm
    except ImportError:
        return 0
    cls = qm.Qwen3MoeSparseMoeBlock
    blocks = sum(isinstance(m, cls) for m in model.modules())
    if blocks and "moe" not in ORIGINAL:
        source = inspect.getsource(cls.forward)
        missing = [s for s in MOE_STATEMENTS if s not in source]
        if missing:
            sys.exit(f"transformers' Qwen3MoeSparseMoeBlock.forward is not the one expert_loop reproduces: {missing}")
        ORIGINAL["moe"] = cls.forward
        cls.forward = expert_loop
    return blocks


def via_host(obj, device, memo):
    """obj with each tensor that lives on another device copied to `device` through host memory; tuples, lists and
    dicts are followed, anything else (the KV cache) is passed on as it is. memo keeps one copy per tensor for the
    current forward pass, since the rotary tables and the attention mask reach every layer."""
    if isinstance(obj, torch.Tensor):
        if obj.device == device:
            return obj
        key = (id(obj), str(device))
        if key not in memo:
            memo[key] = (obj, obj.to("cpu").to(device))  # the source stays referenced, so its id is not reused
        return memo[key][1]
    if type(obj) in (tuple, list):
        return type(obj)(via_host(o, device, memo) for o in obj)
    if type(obj) is dict:
        return {k: via_host(v, device, memo) for k, v in obj.items()}
    return obj


def split_over_two(model_dir, config):
    from accelerate.hooks import remove_hook_from_submodules
    layers = config.num_hidden_layers
    device_map = {"model.embed_tokens": 0, "model.rotary_emb": 0, "model.norm": 0, "lm_head": 0}
    device_map.update({f"model.layers.{i}": 0 if i < layers // 2 else 1 for i in range(layers)})
    model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=torch.bfloat16, device_map=device_map)
    remove_hook_from_submodules(model)  # accelerate's hooks copy from GPU to GPU (and wrap every linear layer)
    for module in model.modules():  # removal leaves each old forward as an instance attribute; the class's applies
        module.__dict__.pop("forward", None)
    memo = {}
    model.register_forward_pre_hook(lambda module, args: memo.clear())
    model.register_forward_hook(lambda module, args, output: memo.clear())

    def to_own_device(module, args, kwargs):
        device = next(module.parameters()).device
        return via_host(args, device, memo), via_host(kwargs, device, memo)

    for block in list(model.model.layers) + [model.model.norm]:
        block.register_forward_pre_hook(to_own_device, with_kwargs=True)
    return model


def load_reader(model_dir):
    """The base model in bfloat16 on this job's GPUs, with a one-line note of the placement on stdout."""
    config = AutoConfig.from_pretrained(model_dir)
    if torch.cuda.device_count() > 1:
        model = split_over_two(model_dir, config)
        where = {}
        for p in model.parameters():
            where[str(p.device)] = where.get(str(p.device), 0) + p.numel()
        if set(where) != {"cuda:0", "cuda:1"}:
            sys.exit(f"{model_dir}: parameters on {sorted(where)}, not on cuda:0 and cuda:1")
        share = ", ".join(f"{d}: {n / 1e9:.2f} B parameters" for d, n in sorted(where.items()))
        note = f"split over 2 GPUs by decoder layers ({share}), copies between them through host memory"
    else:
        model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=torch.bfloat16, device_map="cuda")
        note = "on one GPU"
    blocks = patch_moe(model)
    if blocks:
        note += f"; {blocks} Qwen3-MoE blocks run spread.expert_loop"
    print(f"{model_dir} {note}", flush=True)
    return model
