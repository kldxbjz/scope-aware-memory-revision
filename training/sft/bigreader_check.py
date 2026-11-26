"""Pipeline checks of the larger reader's dev runs (docs/analysis.md, "Larger reader"):

    cd ~/scope-sft-work    # the folder that holds runs/
    python3 -I $REPO/training/sft/bigreader_check.py $REPO runs/bigreader_qwen3-30b-a3b-instruct-2507 runs

Only the reader may differ from the 4B runs: the same episodes, the same memories (predictions and trajectories copied
from the 4B runs; JSON summaries equal apart from the path of the run's own episodes.jsonl), the same prompts (read-time
prompts recomputed from the repository code and compared with the 4B runs' prompt hashes), every probe answered. Also
reports the "Answer:" line, replies at the token budget, the job logs (hosts, GPUs, errors) and the unit times.
Prints PIPELINE CHECKS PASSED or FAILED. Standard library only.
"""
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

repo, big, small = (Path(a) for a in sys.argv[1:4])
sys.path.insert(0, str(repo))
from scope_memory import readtime  # noqa: E402
from scope_memory.evaluate import ANSWER_LINE  # noqa: E402

problems = []


def sha(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def same_bytes(a, b):
    """Equal files; for a JSON summary, equal apart from "data", the path of the run's own episodes.jsonl."""
    if not (a.exists() and b.exists()):
        return False
    if a.suffix == ".json":
        x, y = (json.loads(p.read_text(encoding="utf-8")) for p in (a, b))
        if isinstance(x, dict) and isinstance(y, dict) \
                and Path(str(x.get("data"))).name == Path(str(y.get("data"))).name:
            x.pop("data", None)
            y.pop("data", None)
        return x == y
    return a.read_bytes() == b.read_bytes()


print("== job logs")
stamps = []
for log in sorted((big / "units").glob("slurm-*.out")):
    text = log.read_text(encoding="utf-8", errors="replace").splitlines()
    hosts = sorted({m.group(1) for line in text for m in [re.match(r"host=(\S+) job=", line)] if m})
    gpus = sorted({line.strip() for line in text if line.startswith("NVIDIA")})
    bad = [line for line in text if re.search(r"Traceback|Error|error|Killed|out of memory", line)
           and "DUE TO PREEMPTION" not in line]
    pre = [line[:120] for line in text if "DUE TO PREEMPTION" in line]
    print(f"  {log.name}: hosts {hosts}, GPUs {gpus}, preempted: {pre or 'no'}, error lines: {bad or 'none'}")
    if bad:
        problems.append(f"{log.name}: error lines")
    for line in text:
        m = re.match(r"== unit (done )?(?:(\w+) )?(\S+) (\d{4}-\d\d-\d\dT[\d:]+)", line)
        if m:
            stamps.append((m.group(1) is not None, m.group(3), datetime.fromisoformat(m.group(4))))
starts = {}
print("  unit times:")
for done, run_dir, t in stamps:
    if not done:
        starts[run_dir] = t
    elif run_dir in starts:
        name = Path(run_dir).name if "readtime" not in run_dir else "readtime/" + Path(run_dir).name
        print(f"    {name}: {(t - starts[run_dir]).total_seconds() / 60:.1f} min")

print("\n== memory-reading runs (baseline.py --from-run, both arms)")
SAME_FILES = ("episodes.jsonl", "predictions_crud.jsonl", "predictions_scope.jsonl", "trajectories.jsonl",
              "trajectories_crud.jsonl", "trajectories_scope.jsonl", "eval_tf_crud.json", "eval_tf_scope.json",
              "eval_rollout_oracle_reader.json")
EXPECTED_NEW = {"policy_outputs_from", "answer_model"}
for name in ("sft_p12_eval_s0", "sft_p12_eval_s1", "sft_p12_eval_s2", "reference_gold_p12"):
    b, s = big / name, small / name
    cb = json.loads((b / "run_config.json").read_text(encoding="utf-8"))
    cs = json.loads((s / "run_config.json").read_text(encoding="utf-8"))
    differ = sorted(k for k in set(cb) | set(cs) if cb.get(k) != cs.get(k))
    files = {f: same_bytes(b / f, s / f) for f in SAME_FILES if (s / f).exists()}
    ab, as_ = jsonl(b / "answers.jsonl"), jsonl(s / "answers.jsonl")
    ids_equal = [r["id"] for r in ab] == [r["id"] for r in as_]
    missing = sum(not ANSWER_LINE.search(r["raw"]) for r in ab)
    missing4 = sum(not ANSWER_LINE.search(r["raw"]) for r in as_)
    agent = json.loads((b / "answer_agent.json").read_text(encoding="utf-8"))
    same_answer = sum(x["answer"] == y["answer"] for x, y in zip(ab, as_)) / len(ab)
    print(f"  {name}: config keys differing from the 4B run: {differ}; files equal to the 4B run: "
          f"{sum(files.values())}/{len(files)}{'' if all(files.values()) else ' ' + str(files)}; answers {len(ab)}, "
          f"ids as in the 4B run: {ids_equal}; answer line missing {missing} (4B: {missing4}); answer_agent.json "
          f"{agent['model']} missing={agent['answer_line_missing']}; same answer text as the 4B reader: "
          f"{100 * same_answer:.1f}%")
    if set(differ) != EXPECTED_NEW or not all(files.values()) or not ids_equal or len(ab) != 2340:
        problems.append(f"{name}: run differs from the 4B run beyond the reader")

print("\n== read-time runs")
local_sha = hashlib.sha256((repo / "scope_memory" / "readtime.py").read_bytes()).hexdigest()
for name in ("dev_history", "dev_sft_s0", "dev_sft_s1", "dev_sft_s2", "dev_gold"):
    rb = readtime.load_readtime(big / "readtime" / name)
    rs = readtime.load_readtime(small / "readtime" / name)
    cfg = rb["config"]
    differ = sorted(k for k in set(cfg) | set(rs["config"]) if cfg.get(k) != rs["config"].get(k))
    print(f"  {name}: model {cfg['model']}, batch {cfg['batch_size']}, max_new_tokens {cfg['max_new_tokens']}, "
          f"reader_version {cfg['reader_version']}, readtime.py equal to the local copy: "
          f"{cfg['readtime_sha256'] == local_sha}; config keys differing from the 4B run: {differ}")
    if cfg["readtime_sha256"] != local_sha or set(differ) - {"model", "batch_size"}:
        problems.append(f"{name}: config")
    for f in ("episodes.jsonl", "trajectories.jsonl"):
        if (big / "readtime" / name / f).exists() or (small / "readtime" / name / f).exists():
            eq = same_bytes(big / "readtime" / name / f, small / "readtime" / name / f)
            print(f"    {f} equal to the 4B run: {eq}")
            if not eq:
                problems.append(f"{name}: {f}")
    eps = rb["episodes"]
    probes = [(e, p) for e in eps for p in e["probes"]]
    keys = [f"{e['episode_id']}/{p['probe_id']}" for e, p in probes]
    trajectories = None
    if name != "dev_history":
        trajectories = {t["episode_id"]: t for t in jsonl(big / "readtime" / name / "trajectories.jsonl")}
    for c in rb["answers"]:
        mine, theirs = rb["answers"][c], rs["answers"][c]
        if trajectories is None:
            want = {k: sha(readtime.history_prompt(e, p)) for k, (e, p) in zip(keys, probes)}
        else:
            want = {k: sha(readtime.display_prompt(trajectories[e["episode_id"]]["snapshots"][p["after_event"]], p, c))
                    for k, (e, p) in zip(keys, probes)}
        wrong_local = [k for k in keys if mine[f"{k}/{c}"]["prompt_sha256"] != want[k]]
        wrong_4b = [k for k in keys if mine[f"{k}/{c}"]["prompt_sha256"] != theirs[f"{k}/{c}"]["prompt_sha256"]]
        out = [r["output_tokens"] for r in mine.values()]
        inp = [r["input_tokens"] for r in mine.values()]
        miss = sum(not ANSWER_LINE.search(r["raw"]) for r in mine.values())
        miss4 = sum(not ANSWER_LINE.search(r["raw"]) for r in theirs.values())
        at_budget = sum(t >= readtime.REPLY_TOKENS for t in out)
        at_budget4 = sum(r["output_tokens"] >= readtime.REPLY_TOKENS for r in theirs.values())
        print(f"    {c}: {len(mine)} answers for {len(keys)} probes; prompts as recomputed: {not wrong_local}, as in "
              f"the 4B run: {not wrong_4b}; input tokens max {max(inp)}; reply tokens mean {sum(out) / len(out):.0f}"
              f" max {max(out)}, at the {readtime.REPLY_TOKENS} budget {at_budget} (4B: {at_budget4}); answer line "
              f"missing {miss} (4B: {miss4})")
        if wrong_local or wrong_4b or len(mine) != len(keys):
            problems.append(f"{name}/{c}: prompts or count")
    print(f"    checks: {json.dumps(rb['checks'])}")

print("\nPIPELINE CHECKS PASSED" if not problems else f"\nPIPELINE CHECKS FAILED: {problems}")
