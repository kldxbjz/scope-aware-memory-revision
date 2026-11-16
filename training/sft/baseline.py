"""Prompt baselines M0 (CRUD) and M1 (scope) on a split: batched teacher-forced outputs, lockstep rollouts
with the policy's own memory, and fixed Answer Agent replies to every probe.

Writes predictions_<arm>.jsonl, trajectories.jsonl and answers.jsonl for scope_memory.evaluate.
Usage: python baseline.py --model DIR [--adapter DIR] --repo DIR --episodes DATA.jsonl --out-dir DIR
"""
import argparse
import json
import re
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


def pick_option(reply, options):
    text = " ".join(reply.lower().split())
    hits = [o for o in options if " ".join(o.lower().split()) in text]
    return max(hits, key=len) if hits else reply.strip()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--adapter")
    p.add_argument("--repo", required=True)
    p.add_argument("--episodes", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--batch-size", type=int, default=16)
    p.add_argument("--max-new-tokens", type=int, default=512)
    p.add_argument("--shots", type=int, default=0, help="fixed in-context demonstrations per arm (0 = zero-shot)")
    p.add_argument("--demo-episodes", help="split the demonstrations come from (train)")
    args = p.parse_args()
    sys.path.insert(0, args.repo)
    from scope_memory.evaluate import answer_prompt, parse_output
    from scope_memory.protocol import (ARMS, POLICY_INSTRUCTIONS, CrudMemory, ScopeMemory, canon, catalogs_of,
                                       policy_input, read_episodes, sft_rows)

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    episodes = read_episodes(args.episodes)[:args.limit] if args.limit else read_episodes(args.episodes)
    (out / "episodes.jsonl").write_text("".join(json.dumps(e) + "\n" for e in episodes), encoding="utf-8")
    gen = Generator(args.model, args.adapter, args.batch_size)
    demos = {arm: [] for arm in ARMS}
    if args.shots:  # shortest train example per event category, fixed for every prompt
        pool = [r for e in read_episodes(args.demo_episodes) for r in sft_rows(e)]
        for arm in ARMS:
            by_category = {}
            for r in sorted((r for r in pool if r["arm"] == arm), key=lambda r: len(r["prompt"]) + len(r["completion"])):
                by_category.setdefault(r["category"], r)
            chosen = [by_category[c] for c in sorted(by_category)][:args.shots]
            demos[arm] = [m for r in chosen for m in ({"role": "user", "content": r["prompt"]},
                                                       {"role": "assistant", "content": r["completion"]})]
            (out / f"demos_{arm}.json").write_text(json.dumps([r["id"] for r in chosen]) + "\n", encoding="utf-8")

    for arm in ARMS:  # teacher-forced
        target = out / f"predictions_{arm}.jsonl"
        if target.exists():
            continue
        rows = [r for e in episodes for r in sft_rows(e) if r["arm"] == arm]
        replies = gen([[{"role": "system", "content": r["system"]}] + demos[arm] + [{"role": "user", "content": r["prompt"]}]
                       for r in rows], args.max_new_tokens)
        target.write_text("".join(json.dumps({"id": r["id"], "completion": c}) + "\n" for r, c in zip(rows, replies)),
                          encoding="utf-8")
        print(f"teacher-forced {arm}: {len(rows)} outputs", flush=True)

    trajectories_path = out / "trajectories.jsonl"
    if not trajectories_path.exists():  # rollouts, lockstep over episodes
        trajectories = []
        for arm in ARMS:
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
                for (e, ev), reply in zip(active, gen(prompts, args.max_new_tokens)):
                    st = state[e["episode_id"]]
                    obj, how = parse_output(reply)
                    reason = how if obj is None else st["memory"].apply(obj, ev["event_id"], st["seen"])[0]
                    st["steps"].append({"event_id": ev["event_id"], "completion": reply, "accepted": reason is None,
                                        "reason": reason})
                    st["snapshots"][ev["event_id"]] = st["memory"].view()
                print(f"rollout {arm}: event index {k} done for {len(active)} episodes", flush=True)
            for e in episodes:
                st = state[e["episode_id"]]
                trajectories.append({"episode_id": e["episode_id"], "arm": arm, "steps": st["steps"],
                                     "snapshots": st["snapshots"]})
        trajectories_path.write_text("".join(json.dumps(t) + "\n" for t in trajectories), encoding="utf-8")

    answers_path = out / "answers.jsonl"
    if not answers_path.exists():  # fixed Answer Agent: same base model, no adapter
        if args.adapter:
            gen.model = gen.model.get_base_model()
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
