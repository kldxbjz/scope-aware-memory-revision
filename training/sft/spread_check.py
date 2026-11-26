"""Checks of spread.py for the larger reader on the job's node (docs/analysis.md "Larger reader"); prints only.

    python spread_check.py --model DIR --repo MIRROR --episodes DEV.jsonl [--manifest bigreader_model.json]
                           [--prompts 128] [--batches 64,128]

1. direct GPU-to-GPU copies, and copies through host memory, bit for bit against the source;
2. with --manifest: size and hash of every model file against the manifest (download_model.check_dir);
3. spread.expert_loop against transformers' own Qwen3MoeSparseMoeBlock.forward on the inputs that the blocks of four
   layers (on both GPUs) receive in the prefill of four history prompts and in the next decode step, bit for bit;
4. greedy generation of 24 tokens for those four prompts with each of the two forwards, token for token;
5. replies (prompt version 3, the 160-token budget) to the history prompts of the first dev episodes, once per batch
   size: replies with the answer line, seconds per reply, the first replies.
Exit 1 when 2, 3 or 4 differ, or when fewer than 90% of the replies of a batch size carry the answer line."""
import argparse
import importlib.util
import json
import sys
import time
from pathlib import Path

import torch


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--episodes", required=True)
    p.add_argument("--manifest")
    p.add_argument("--prompts", type=int, default=128)
    p.add_argument("--batches", default="64,128")
    args = p.parse_args()
    sys.stdout.reconfigure(errors="replace")
    sys.path.insert(0, args.repo)
    sys.path.insert(1, str(Path(__file__).resolve().parent))
    import accelerate
    import transformers
    from scope_memory import readtime
    from scope_memory.evaluate import ANSWER_LINE
    from scope_memory.protocol import read_episodes
    import spread
    from baseline import Generator

    count = torch.cuda.device_count()
    print("torch", torch.__version__, "| transformers", transformers.__version__, "| accelerate",
          accelerate.__version__, "| vllm installed:", importlib.util.find_spec("vllm") is not None)
    print("GPUs:", [torch.cuda.get_device_name(i) for i in range(count)], flush=True)
    failures = []

    if count > 1:
        print("peer access reported: 0->1", torch.cuda.can_device_access_peer(0, 1), "| 1->0",
              torch.cuda.can_device_access_peer(1, 0))
        rng = torch.Generator(device="cuda:0").manual_seed(0)
        direct = host = total = 0
        for n in (1 << 10, 1 << 16, 1 << 20, 1 << 24, 1 << 26):
            for _ in range(4):
                a = torch.randn(n, device="cuda:0", generator=rng)
                source = a.cpu()
                there = a.to("cuda:1")
                back = there.to("cuda:0")
                hosted = a.to("cpu").to("cuda:1")
                torch.cuda.synchronize(0)
                torch.cuda.synchronize(1)
                direct += (not torch.equal(there.cpu(), source)) + (not torch.equal(back.cpu(), source))
                host += not torch.equal(hosted.cpu(), source)
                total += 1
        print(f"direct GPU-to-GPU copies that differ from the source: {direct} of {2 * total}; "
              f"copies through host memory: {host} of {total}", flush=True)
        if host:
            failures.append("copies through host memory")

    if args.manifest:
        import download_model
        manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        t0 = time.time()
        bad = download_model.check_dir(manifest, args.model)
        print(f"model files against the manifest: {len(manifest['files'])} checked in {time.time() - t0:.0f} s, "
              f"differing: {bad or 'none'}", flush=True)
        if bad:
            failures.append("model files")

    try:
        import inspect
        from transformers.models.qwen3_moe import modeling_qwen3_moe as qm
        source = inspect.getsource(qm.Qwen3MoeSparseMoeBlock.forward)
        missing = [s for s in spread.MOE_STATEMENTS if s not in source]
        print("transformers' Qwen3MoeSparseMoeBlock.forward holds every statement expert_loop reproduces:", not missing)
        if missing:
            print(source, flush=True)
    except ImportError:
        print("no Qwen3-MoE in this transformers")

    batches = [int(b) for b in args.batches.split(",")]
    gen = Generator(args.model, None, batches[0])
    model, tok = gen.model, gen.tok
    own = sum("forward" in m.__dict__ for m in model.modules())
    print("modules with a forward of their own (they would bypass a patched class):", own, flush=True)
    if own:
        failures.append("modules with their own forward")
    prompts = []
    for e in read_episodes(args.episodes):
        prompts += [readtime.history_prompt(e, probe) for probe in e["probes"]]
        if len(prompts) >= args.prompts:
            break
    conversations = [[{"role": "user", "content": q}] for q in prompts[:args.prompts]]
    texts = [tok.apply_chat_template(c, add_generation_prompt=True, tokenize=False) for c in conversations[:4]]
    enc = tok(texts, return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")

    if "moe" in spread.ORIGINAL:
        from transformers.models.qwen3_moe import modeling_qwen3_moe as qm
        layers = model.model.layers
        picked = sorted({0, len(layers) // 2 - 1, len(layers) // 2, len(layers) - 1})
        seen = {i: [] for i in picked}
        hooks = [layers[i].mlp.register_forward_pre_hook(lambda m, a, i=i: seen[i].append(a[0].detach().clone()))
                 for i in picked]
        with torch.no_grad():
            model.generate(**enc, max_new_tokens=2, do_sample=False, pad_token_id=tok.pad_token_id)
        for h in hooks:
            h.remove()
        same = []
        with torch.no_grad():
            for i in picked:
                for x in seen[i]:
                    a = spread.ORIGINAL["moe"](layers[i].mlp, x)
                    b = spread.expert_loop(layers[i].mlp, x)
                    same.append(torch.equal(a[0], b[0]) and torch.equal(a[1], b[1]))
        print(f"expert_loop against transformers' forward: {sum(same)} of {len(same)} block inputs equal bit for bit "
              f"(layers {picked}; prefill of 4 prompts, {enc['input_ids'].shape[1]} tokens, and one decode step)",
              flush=True)
        if not all(same):
            failures.append("expert_loop outputs")
        tokens = {}
        for name, forward in (("transformers' forward", spread.ORIGINAL["moe"]), ("expert_loop", spread.expert_loop)):
            qm.Qwen3MoeSparseMoeBlock.forward = forward
            t0 = time.time()
            with torch.no_grad():
                tokens[name] = model.generate(**enc, max_new_tokens=24, do_sample=False, pad_token_id=tok.pad_token_id)
            print(f"{name}: 24 tokens for 4 prompts in {time.time() - t0:.1f} s", flush=True)
        qm.Qwen3MoeSparseMoeBlock.forward = spread.expert_loop
        equal = torch.equal(*tokens.values())
        print("greedy tokens equal:", equal, flush=True)
        if not equal:
            failures.append("generated tokens")

    for batch in batches:
        gen.batch_size = batch
        for i in range(count):
            torch.cuda.reset_peak_memory_stats(i)
        t0 = time.time()
        try:
            replies = gen(conversations, readtime.REPLY_TOKENS)
        except torch.cuda.OutOfMemoryError as exc:
            print(f"batch {batch}: out of GPU memory ({str(exc)[:160]})", flush=True)
            torch.cuda.empty_cache()
            continue
        seconds = time.time() - t0
        peaks = [torch.cuda.max_memory_allocated(i) / 2 ** 30 for i in range(count)]
        lines = sum(bool(ANSWER_LINE.search(r)) for r in replies)
        print(f"batch {batch}: {len(replies)} history replies in {seconds:.0f} s ({seconds / len(replies):.2f} s per "
              f"reply), answer line in {lines}; peak GPU memory {', '.join(f'{g:.1f}' for g in peaks)} GiB", flush=True)
        for r in replies[:3]:
            print("   ", r.replace("\n", " / ")[:300])
        if lines < 0.9 * len(replies):
            failures.append(f"answer lines at batch {batch}")
    print("SPREAD_CHECK", ("FAILED: " + ", ".join(failures)) if failures else "PASSED", flush=True)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
