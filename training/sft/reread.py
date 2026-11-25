"""Answer Agent runs of the read-time experiments (scope_memory.readtime; post-hoc): A, the raw history, and B, a
finished run's scope memory shown in other ways. The Answer Agent is the frozen one: a freshly loaded base model
without any adapter, greedy decoding, the reply format and token budget of prompt version 3.

  python reread.py --model DIR --repo MIRROR --out-dir RUN --history --episodes DATA [--limit N]
  python reread.py --model DIR --repo MIRROR --out-dir RUN --from-run SOURCE [--limit N]

--history answers every probe of DATA from the raw history (answers_history.jsonl, history_check.json). --from-run
reads SOURCE's scope memory at every probe and answers it as replay, compact and sentences (answers_<condition>.jsonl,
display_check.json); SOURCE is a finished baseline.sbatch run. Each answer row holds the parsed option, the raw reply,
the chat-templated input tokens, the reply tokens and the prompt's SHA-256 (display rows also the tokens of the memory
block); prompts_<condition>.jsonl keeps the first 20 prompts whole. Resumable: a finished condition is not run again,
and a run directory written with other settings or another scope_memory/readtime.py is refused.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
from collections import Counter
from pathlib import Path


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def write_atomic(path, text):
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--model", required=True)
    p.add_argument("--repo", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--history", action="store_true", help="A: answer from the raw history of --episodes")
    p.add_argument("--episodes", help="data split for --history")
    p.add_argument("--from-run", help="B: finished baseline.sbatch run whose scope memory is shown")
    p.add_argument("--limit", type=int, help="first N episodes only (smoke runs)")
    p.add_argument("--batch-size", type=int, default=16)
    args = p.parse_args()
    if args.history == bool(args.from_run) or args.history != bool(args.episodes):
        sys.exit("give --history with --episodes, or --from-run")
    sys.path.insert(0, args.repo)
    sys.path.insert(1, str(Path(__file__).resolve().parent))
    from scope_memory import readtime
    from scope_memory.evaluate import ANSWER_LINE, pick_option
    from scope_memory.protocol import read_episodes
    from baseline import Generator, lora_modules

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    kind = readtime.HISTORY if args.history else "display"
    conditions = [readtime.HISTORY] if args.history else list(readtime.DISPLAYS)
    config = {"model": args.model, "kind": kind, "episodes": args.episodes, "from_run": args.from_run,
              "limit": args.limit, "batch_size": args.batch_size, "conditions": conditions,
              "answer_agent": "base model, no adapter", "reader_version": readtime.READER,
              "max_new_tokens": readtime.REPLY_TOKENS,
              "readtime_sha256": hashlib.sha256(Path(readtime.__file__).read_bytes()).hexdigest()}
    config_path = out / "run_config.json"  # a resumed run must use the same settings and prompts
    if config_path.exists() and json.loads(config_path.read_text(encoding="utf-8")) != config:
        sys.exit(f"{config_path} was written with other settings or prompts; use a new --out-dir")
    config_path.write_text(json.dumps(config) + "\n", encoding="utf-8")

    if args.history:
        episodes = read_episodes(args.episodes)
    else:
        source = Path(args.from_run)
        if not (source / "ALL_DONE").exists():
            sys.exit(f"{source} has no ALL_DONE marker")
        episodes = read_episodes(source / "episodes.jsonl")
        shutil.copyfile(source / "run_config.json", out / "source_run_config.json")
    episodes = episodes[:args.limit] if args.limit else episodes
    (out / "episodes.jsonl").write_text("".join(json.dumps(e) + "\n" for e in episodes), encoding="utf-8")
    if not args.history:
        mine = {e["episode_id"] for e in episodes}
        trajectories = [t for t in jsonl(source / "trajectories_scope.jsonl") if t["episode_id"] in mine]
        if [t["episode_id"] for t in trajectories] != [e["episode_id"] for e in episodes]:
            sys.exit(f"{source}: scope trajectories do not follow the episodes")
        (out / "trajectories.jsonl").write_text("".join(json.dumps(t) + "\n" for t in trajectories),
                                                encoding="utf-8")
        stored = {r["id"]: r["answer"] for r in jsonl(source / "answers.jsonl")}

    gen = None
    for condition in conditions:
        target = out / f"answers_{condition}.jsonl"
        if target.exists():
            continue
        items = []  # (id, prompt, extra fields)
        if args.history:
            for e in episodes:
                for probe in e["probes"]:
                    n = len(readtime.events_until(e, probe["after_event"]))
                    items.append((f"{e['episode_id']}/{probe['probe_id']}/{condition}",
                                  readtime.history_prompt(e, probe), {"events": n}))
        else:
            by_id = {e["episode_id"]: e for e in episodes}
            for t in trajectories:
                for probe in by_id[t["episode_id"]]["probes"]:
                    view = t["snapshots"][probe["after_event"]]
                    items.append((f"{t['episode_id']}/{probe['probe_id']}/{condition}",
                                  readtime.display_prompt(view, probe, condition),
                                  {"memory_text": readtime.memory_block(view, condition)}))
        if gen is None:  # the Answer Agent: the base model, never an adapter
            gen = Generator(args.model, None, args.batch_size)
            injected = lora_modules(gen.model)
            if injected:
                sys.exit(f"Answer Agent still has LoRA modules, e.g. {injected[0]}")
        messages = [[{"role": "user", "content": prompt}] for _, prompt, _ in items]
        replies = gen(messages, readtime.REPLY_TOKENS)
        options = {}
        for e in episodes:
            for probe in e["probes"]:
                options[f"{e['episode_id']}/{probe['probe_id']}"] = probe["options"]
        rows = []
        for (item_id, prompt, extra), message, reply in zip(items, messages, replies):
            row = {"id": item_id, "answer": pick_option(reply, options[item_id.rsplit("/", 1)[0]], readtime.READER),
                   "raw": reply,
                   "input_tokens": len(gen.tok.apply_chat_template(message, add_generation_prompt=True,
                                                                   tokenize=True)),
                   "output_tokens": len(gen.tok(reply, add_special_tokens=False)["input_ids"]),
                   "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest()}
            if "memory_text" in extra:
                row["memory_tokens"] = len(gen.tok(extra["memory_text"], add_special_tokens=False)["input_ids"])
            else:
                row.update(extra)
            rows.append(row)
        (out / f"prompts_{condition}.jsonl").write_text(
            "".join(json.dumps({"id": i, "prompt": prompt}) + "\n" for i, prompt, _ in items[:20]), encoding="utf-8")
        write_atomic(target, "".join(json.dumps(r) + "\n" for r in rows))
        missing = sum(not ANSWER_LINE.search(r["raw"]) for r in rows)
        print(f"{condition}: {len(rows)} answers, answer line missing in {missing}", flush=True)

    agent = {"model": args.model, "adapter": None, "lora_modules": 0, "reader_version": readtime.READER,
             "answer_line_missing": {}}
    for condition in conditions:
        rows = jsonl(out / f"answers_{condition}.jsonl")
        agent["answer_line_missing"][condition] = sum(not ANSWER_LINE.search(r["raw"]) for r in rows)
    (out / "answer_agent.json").write_text(json.dumps(agent) + "\n", encoding="utf-8")
    if args.history:
        rows = jsonl(out / "answers_history.jsonl")
        tokens = [r["input_tokens"] for r in rows]
        check = {"prompts": len(rows), "episodes": len(episodes),
                 "events_per_prompt": dict(sorted(Counter(r["events"] for r in rows).items())),
                 "input_tokens": {"mean": round(sum(tokens) / len(tokens), 1), "max": max(tokens)},
                 "prompts_over_32k_tokens": sum(t + readtime.REPLY_TOKENS > 32768 for t in tokens),
                 "truncation": "none: every prompt is given whole"}
        (out / "history_check.json").write_text(json.dumps(check, indent=1) + "\n", encoding="utf-8")
    else:
        counts = Counter()
        by_id = {e["episode_id"]: e for e in episodes}
        for t in trajectories:
            for probe in by_id[t["episode_id"]]["probes"]:
                counts.update(readtime.display_check(t["snapshots"][probe["after_event"]]))
        replay = {r["id"].rsplit("/", 1)[0]: r["answer"] for r in jsonl(out / "answers_replay.jsonl")}
        counts["replay_same_raw_answer"] = sum(replay[k] == stored.get(f"{k}/scope") for k in replay)
        counts["probes"] = len(replay)
        (out / "display_check.json").write_text(json.dumps(dict(sorted(counts.items())), indent=1) + "\n",
                                                encoding="utf-8")
    print("done", flush=True)


if __name__ == "__main__":
    main()
