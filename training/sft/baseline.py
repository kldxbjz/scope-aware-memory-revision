"""Policy evaluation runs for both arms: batched teacher-forced outputs, lockstep rollouts with each arm's own
memory, and replies from a fixed Answer Agent to every probe.

Without adapters this is the prompt baseline M0 (CRUD) / M1 (scope); `--shots k` adds fixed train
demonstrations, the same events for both arms. With SFT, each arm loads only its own adapter (`--adapter-scope`,
`--adapter-crud`). `--policy gold` and `--policy noop` replace the policy model with reference memories (the gold
path, and memory never written), so the Answer Agent's ceiling and the do-nothing floor are measured the same way.
The Answer Agent is always a freshly loaded base model without any adapter.
Writes predictions_<arm>.jsonl (policy model only), trajectories.jsonl, answers.jsonl and answer_agent.json for
scope_memory.evaluate.
"""
import argparse
import gc
import hashlib
import json
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


class Generator:
    def __init__(self, model_dir, adapter, batch_size):
        self.tok = AutoTokenizer.from_pretrained(model_dir)
        self.tok.padding_side = "left"
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, torch_dtype=torch.bfloat16, device_map="cuda")
        if adapter:
            from peft import PeftModel
            self.model = PeftModel.from_pretrained(self.model, adapter)
        self.model.eval()
        self.adapter = adapter
        self.batch_size = batch_size

    def __call__(self, conversations, max_new_tokens):
        outputs = []
        for start in range(0, len(conversations), self.batch_size):
            chunk = conversations[start:start + self.batch_size]
            texts = [self.tok.apply_chat_template(c, add_generation_prompt=True, tokenize=False) for c in chunk]
            enc = self.tok(texts, return_tensors="pt", padding=True, add_special_tokens=False).to("cuda")
            with torch.no_grad():
                gen = self.model.generate(**enc, max_new_tokens=max_new_tokens, do_sample=False,
                                          pad_token_id=self.tok.pad_token_id)
            outputs += self.tok.batch_decode(gen[:, enc["input_ids"].shape[1]:], skip_special_tokens=True)
        return outputs

    def close(self):
        del self.model
        gc.collect()
        torch.cuda.empty_cache()


def lora_modules(model):
    """Names of injected LoRA submodules; PEFT injects them into the base model itself."""
    return [name for name, _ in model.named_modules() if name.rsplit(".", 1)[-1].startswith("lora_")]


def pick_option(reply, options):
    text = " ".join(reply.lower().split())
    hits = [o for o in options if " ".join(o.lower().split()) in text]
    return max(hits, key=len) if hits else reply.strip()


def pick_demos(rows, shots, arms):
    """One train event per event category, the same events for every arm: in each category the event whose rows
    (prompt + completion, summed over the arms) are shortest. Returns {arm: rows in category order}."""
    events = {}
    for r in rows:
        events.setdefault((r["episode_id"], r["event_id"]), {})[r["arm"]] = r
    size = {key: sum(len(r["prompt"]) + len(r["completion"]) for r in by_arm.values()) for key, by_arm in events.items()}
    by_category = {}
    for key in sorted(events, key=lambda k: (size[k], k)):
        if set(events[key]) == set(arms):
            by_category.setdefault(events[key][arms[0]]["category"], key)
    chosen = [by_category[c] for c in sorted(by_category)][:shots]
    return {arm: [events[key][arm] for key in chosen] for arm in arms}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--adapter-scope", help="LoRA adapter trained on the scope arm (SFT runs only)")
    p.add_argument("--adapter-crud", help="LoRA adapter trained on the CRUD arm (SFT runs only)")
    p.add_argument("--repo", required=True)
    p.add_argument("--episodes", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--batch-size", type=int, default=16)
    p.add_argument("--max-new-tokens", type=int, default=512)
    p.add_argument("--shots", type=int, default=0, help="fixed in-context demonstrations per arm (0 = zero-shot)")
    p.add_argument("--demo-episodes", help="split the demonstrations come from (train)")
    p.add_argument("--policy", choices=("model", "gold", "noop"), default="model",
                   help="model: the policy LLM (default); gold / noop: reference memories along the gold path or "
                        "never written, answered by the same Answer Agent")
    args = p.parse_args()
    if bool(args.adapter_scope) != bool(args.adapter_crud):
        sys.exit("give both --adapter-scope and --adapter-crud, or neither")
    if args.policy != "model" and (args.adapter_scope or args.shots):
        sys.exit("--policy gold/noop takes no adapters or demonstrations")
    adapters = {"scope": args.adapter_scope, "crud": args.adapter_crud}
    sys.path.insert(0, args.repo)
    from scope_memory.evaluate import answer_prompt, gold_policy, noop_policy, parse_output, rollout
    from scope_memory.protocol import (ARMS, POLICY_INSTRUCTIONS, CrudMemory, ScopeMemory, canon, catalogs_of,
                                       policy_input, read_episodes, sft_rows)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    config = {"model": args.model, "policy": args.policy, "episodes": args.episodes, "limit": args.limit,
              "adapters": adapters, "shots": args.shots, "demo_episodes": args.demo_episodes,
              "answer_agent": "base model, no adapter",
              "policy_instructions_sha256": {arm: hashlib.sha256(POLICY_INSTRUCTIONS[arm].encode("utf-8")).hexdigest()
                                             for arm in ARMS}}
    config_path = out / "run_config.json"  # a resumed run must use the same settings and instructions
    if config_path.exists() and json.loads(config_path.read_text(encoding="utf-8")) != config:
        sys.exit(f"{config_path} was written with other settings or instructions; use a new --out-dir")
    config_path.write_text(json.dumps(config) + "\n", encoding="utf-8")
    episodes = read_episodes(args.episodes)[:args.limit] if args.limit else read_episodes(args.episodes)
    (out / "episodes.jsonl").write_text("".join(json.dumps(e) + "\n" for e in episodes), encoding="utf-8")
    demos = {arm: [] for arm in ARMS}
    if args.shots:  # one train event per category, the same events for both arms, fixed for every prompt
        pool = [r for e in read_episodes(args.demo_episodes) for r in sft_rows(e)]
        for arm, chosen in pick_demos(pool, args.shots, ARMS).items():
            demos[arm] = [m for r in chosen for m in ({"role": "user", "content": r["prompt"]},
                                                       {"role": "assistant", "content": r["completion"]})]
            (out / f"demos_{arm}.json").write_text(json.dumps([r["id"] for r in chosen]) + "\n", encoding="utf-8")
    reference = None  # policy model
    if args.policy == "gold":
        reference = gold_policy(episodes)
    elif args.policy == "noop":
        reference = noop_policy

    loaded = {"gen": None}

    def generator(adapter):
        """Loaded lazily: an arm's model carries only that arm's adapter; adapter None is a fresh base model."""
        gen = loaded["gen"]
        if gen is None or gen.adapter != adapter:
            if gen is not None:
                gen.close()
            gen = loaded["gen"] = Generator(args.model, adapter, args.batch_size)
        return gen

    for arm in ARMS:
        if reference is not None:  # reference memories: no policy model, no teacher-forced outputs
            traj_path = out / f"trajectories_{arm}.jsonl"
            if not traj_path.exists():
                traj_path.write_text("".join(json.dumps(rollout(e, arm, reference)) + "\n" for e in episodes),
                                     encoding="utf-8")
                print(f"reference {args.policy} {arm}: {len(episodes)} trajectories", flush=True)
            continue
        target = out / f"predictions_{arm}.jsonl"
        if not target.exists():  # teacher-forced
            rows = [r for e in episodes for r in sft_rows(e) if r["arm"] == arm]
            replies = generator(adapters[arm])([[{"role": "system", "content": r["system"]}] + demos[arm] +
                                                [{"role": "user", "content": r["prompt"]}] for r in rows],
                                               args.max_new_tokens)
            target.write_text("".join(json.dumps({"id": r["id"], "completion": c}) + "\n" for r, c in zip(rows, replies)),
                              encoding="utf-8")
            print(f"teacher-forced {arm}: {len(rows)} outputs", flush=True)
        traj_path = out / f"trajectories_{arm}.jsonl"
        if not traj_path.exists():  # rollout, lockstep over episodes, own memory only
            state = {}
            for e in episodes:
                memory = ScopeMemory() if arm == "scope" else CrudMemory()
                memory.seed(e["initial_state"], catalogs_of(e))
                state[e["episode_id"]] = {"memory": memory, "seen": ["seed"], "steps": [], "snapshots": {}}
            for k in range(max(len(e["events"]) for e in episodes)):
                active = [(e, e["events"][k]) for e in episodes if len(e["events"]) > k]
                prompts = []
                for e, ev in active:
                    st = state[e["episode_id"]]
                    st["seen"].append(ev["event_id"])
                    prompts.append([{"role": "system", "content": POLICY_INSTRUCTIONS[arm]}] + demos[arm] +
                                   [{"role": "user", "content": canon(policy_input(st["memory"].view(), ev))}])
                for (e, ev), reply in zip(active, generator(adapters[arm])(prompts, args.max_new_tokens)):
                    st = state[e["episode_id"]]
                    obj, how = parse_output(reply)
                    reason = how if obj is None else st["memory"].apply(obj, ev["event_id"], st["seen"])[0]
                    st["steps"].append({"event_id": ev["event_id"], "completion": reply, "accepted": reason is None,
                                        "reason": reason})
                    st["snapshots"][ev["event_id"]] = st["memory"].view()
                print(f"rollout {arm}: event index {k} done for {len(active)} episodes", flush=True)
            traj_path.write_text("".join(json.dumps({"episode_id": e["episode_id"], "arm": arm,
                                                     "steps": state[e["episode_id"]]["steps"],
                                                     "snapshots": state[e["episode_id"]]["snapshots"]}) + "\n"
                                         for e in episodes), encoding="utf-8")
    trajectories_path = out / "trajectories.jsonl"
    trajectories_path.write_text("".join((out / f"trajectories_{arm}.jsonl").read_text(encoding="utf-8") for arm in ARMS),
                                 encoding="utf-8")

    answers_path = out / "answers.jsonl"
    if not answers_path.exists():  # fixed Answer Agent: the base model, never an adapter
        gen = generator(None)
        injected = lora_modules(gen.model)
        if injected:
            sys.exit(f"Answer Agent still has LoRA modules, e.g. {injected[0]}")
        (out / "answer_agent.json").write_text(json.dumps({"model": args.model, "adapter": None, "lora_modules": 0})
                                               + "\n", encoding="utf-8")
        by_id = {e["episode_id"]: e for e in episodes}
        items, prompts = [], []
        for line in trajectories_path.read_text(encoding="utf-8").splitlines():
            t = json.loads(line)
            for probe in by_id[t["episode_id"]]["probes"]:
                items.append((f"{t['episode_id']}/{probe['probe_id']}/{t['arm']}", probe))
                prompts.append([{"role": "user", "content": answer_prompt(t["snapshots"][probe["after_event"]], probe)}])
        replies = gen(prompts, 48)
        answers_path.write_text("".join(json.dumps({"id": i, "answer": pick_option(r, p["options"]), "raw": r}) + "\n"
                                        for (i, p), r in zip(items, replies)), encoding="utf-8")
        print(f"answers: {len(items)}", flush=True)


if __name__ == "__main__":
    main()
