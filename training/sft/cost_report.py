"""Token and call counts of finished runs with the policy tokenizer (docs/evaluation.md, Cost).

Per run and arm: policy calls (one per rollout event) with chat-templated input tokens and generated tokens; Answer
Agent calls (one per probe) with input and generated tokens; memory tokens at the probes; rejected outputs. Teacher-
forced passes are diagnostics and are not counted. Reference runs (--policy gold / noop) have no policy calls. With
--sft-rows, the tokens of exported SFT rows: the chat-templated prompt and the completion (the loss tokens).

  python cost_report.py --tokenizer MODEL_DIR --repo MIRROR --runs RUN [RUN ...] [--sft-rows FILE ...] --out FILE
"""
import argparse
import json
import statistics
import sys
from pathlib import Path


def stats(values):
    return {"calls": len(values), "mean": round(statistics.fmean(values), 1) if values else None, "total": sum(values)}


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tokenizer", required=True)
    p.add_argument("--repo", required=True, help="repository mirror the runs used (scope_memory)")
    p.add_argument("--runs", nargs="*", default=[])
    p.add_argument("--sft-rows", nargs="*", default=[])
    p.add_argument("--out", required=True)
    args = p.parse_args()
    sys.path.insert(0, args.repo)
    from transformers import AutoTokenizer
    from scope_memory.evaluate import answer_prompt
    from scope_memory.protocol import (ARMS, POLICY_INSTRUCTIONS, CrudMemory, ScopeMemory, canon, catalogs_of,
                                       policy_input, read_episodes, sft_rows)
    tok = AutoTokenizer.from_pretrained(args.tokenizer)

    def count(text):
        return len(tok(text or "", add_special_tokens=False)["input_ids"])

    def chat(messages):
        return len(tok.apply_chat_template(messages, add_generation_prompt=True, tokenize=True))

    report = {"tokenizer": args.tokenizer, "runs": {}, "sft_rows": {}}
    for run in map(Path, args.runs):
        config = json.loads((run / "run_config.json").read_text(encoding="utf-8"))
        episodes = {e["episode_id"]: e for e in read_episodes(run / "episodes.jsonl")}
        reader = config.get("reader_version", 1)
        demos = {arm: [] for arm in ARMS}
        if config.get("shots"):
            pool = {r["id"]: r for e in read_episodes(config["demo_episodes"]) for r in sft_rows(e)}
            for arm in ARMS:
                ids = json.loads((run / f"demos_{arm}.json").read_text(encoding="utf-8"))
                demos[arm] = [m for i in ids for m in ({"role": "user", "content": pool[i]["prompt"]},
                                                        {"role": "assistant", "content": pool[i]["completion"]})]
        answers = {row["id"]: row.get("raw") for row in jsonl(run / "answers.jsonl")}
        arms = {}
        for arm in ARMS:
            policy_in, policy_out, answer_in, answer_out, memory, rejected = [], [], [], [], [], 0
            for t in jsonl(run / f"trajectories_{arm}.jsonl"):
                e = episodes[t["episode_id"]]
                if config.get("policy", "model") == "model":
                    seeded = ScopeMemory() if arm == "scope" else CrudMemory()
                    seeded.seed(e["initial_state"], catalogs_of(e))
                    before = seeded.view()
                    for ev, step in zip(e["events"], t["steps"]):
                        if step["event_id"] != ev["event_id"]:
                            sys.exit(f"{run}: trajectory steps out of order in {e['episode_id']}")
                        policy_in.append(chat([{"role": "system", "content": POLICY_INSTRUCTIONS[arm]}] + demos[arm] +
                                              [{"role": "user", "content": canon(policy_input(before, ev))}]))
                        policy_out.append(count(step["completion"]))
                        rejected += not step["accepted"]
                        before = t["snapshots"][ev["event_id"]]
                for probe in e["probes"]:
                    view = t["snapshots"][probe["after_event"]]
                    answer_in.append(chat([{"role": "user", "content": answer_prompt(view, probe, reader)}]))
                    answer_out.append(count(answers.get(f"{e['episode_id']}/{probe['probe_id']}/{arm}")))
                    memory.append(count(json.dumps(view)))
            arms[arm] = {"policy_input_tokens": stats(policy_in), "policy_output_tokens": stats(policy_out),
                         "rejected_outputs": rejected, "answer_input_tokens": stats(answer_in),
                         "answer_output_tokens": stats(answer_out), "memory_tokens_at_probes": stats(memory)}
        report["runs"][str(run)] = {"config": {k: config.get(k) for k in ("policy", "shots", "adapters", "reader_version",
                                                                           "episodes")}, "arms": arms}
    for path in args.sft_rows:
        rows = jsonl(path)
        prompts = [chat([{"role": "system", "content": r["system"]}, {"role": "user", "content": r["prompt"]}])
                   for r in rows]
        report["sft_rows"][str(path)] = {"rows": len(rows), "prompt_tokens": stats(prompts),
                                         "completion_tokens": stats([count(r["completion"]) for r in rows])}
    text = json.dumps(report, indent=2)
    Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
