"""Greedy teacher-forced generation for one arm on the first K episodes of a split.

Writes the selected episodes and {id, completion} predictions for `scope_memory.evaluate teacher-forced`.
Usage: python generate.py --model DIR [--adapter DIR] --arm scope --episodes DATA.jsonl --limit 5 --out-dir DIR
"""
import argparse
import json
import sys
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--adapter")
    p.add_argument("--arm", choices=("scope", "crud"), required=True)
    p.add_argument("--episodes", required=True)
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--repo", required=True, help="repository root, for scope_memory")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--max-new-tokens", type=int, default=768)
    args = p.parse_args()
    sys.path.insert(0, args.repo)
    from scope_memory.protocol import read_episodes, sft_rows

    episodes = read_episodes(args.episodes)[:args.limit]
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "episodes.jsonl").write_text("".join(json.dumps(e) + "\n" for e in episodes), encoding="utf-8")
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, torch_dtype=torch.bfloat16, device_map="cuda")
    if args.adapter:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, args.adapter)
    model.eval()
    lines = []
    for episode in episodes:
        for row in (r for r in sft_rows(episode) if r["arm"] == args.arm):
            messages = [{"role": "system", "content": row["system"]}, {"role": "user", "content": row["prompt"]}]
            ids = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to("cuda")
            with torch.no_grad():
                generated = model.generate(ids, max_new_tokens=args.max_new_tokens, do_sample=False)
            completion = tokenizer.decode(generated[0, ids.shape[1]:], skip_special_tokens=True)
            lines.append(json.dumps({"id": row["id"], "completion": completion}))
    (out / f"predictions_{args.arm}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(lines)} predictions for {args.arm}")


if __name__ == "__main__":
    main()
