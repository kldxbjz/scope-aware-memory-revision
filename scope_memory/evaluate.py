"""Evaluate memory-revision policies under protocol v1 (docs/protocol.md).

teacher-forced: one output per event, applied to the gold memory before that event
  (outline v2.7 G2: valid outputs, state, decision, overwrite and update errors).
rollout: each arm carries its own memory forward and QA probes read the snapshot
  after their event (outline v2.7 main metric; Answer Agent answers when given,
  otherwise the deterministic oracle reader, which is a pipeline check only).
Intervals: percentile bootstrap over episodes (one fictional user each).
Roles: Answer Agent QA on rollout memory, with the paired scope-minus-CRUD difference, is the
  primary result. Everything read with the rule readers (teacher-forced metrics, rollout write
  metrics, the oracle reader) is diagnostic, and rule-reader parse failures are reported apart.

  python3 -m scope_memory.evaluate self-check --data DATA.jsonl
  python3 -m scope_memory.evaluate teacher-forced --data DATA.jsonl --arm scope --predictions preds.jsonl
  python3 -m scope_memory.evaluate rollout-score --data DATA.jsonl --trajectories traj.jsonl [--answers answers.jsonl]
"""
import argparse
import sys
import copy
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path

from .protocol import (ARMS, CATEGORIES, POLICY_INSTRUCTIONS, QA_GROUPS, READERS, CrudMemory, ScopeMemory, canon,
                       canonical_state, canonical_value, catalogs_of, gold_trajectory, oracle_answer, policy_input,
                       read_episodes, replay_gold)

FENCE = re.compile(r"```(?:json)?\s*(.*?)\s*```", re.S)
NO_CHANGE = ("stable_preference", "clarify")
NOOP_OUTPUT = {"scope": {"decision": "resolved", "actions": [{"operation": "NOOP"}]},
               "crud": {"decision": "resolved", "operations": [{"op": "NOOP"}]}}


def parse_output(text):
    """Return (object, how); how is strict/fenced/extracted, or the failure reason when object is None."""
    if not isinstance(text, str):
        return None, "missing"
    stripped = text.strip()
    candidates = [(stripped, "strict")]
    fenced = FENCE.search(stripped)
    if fenced:
        candidates.append((fenced.group(1), "fenced"))
    start, end = stripped.find("{"), stripped.rfind("}")
    if 0 <= start < end:
        candidates.append((stripped[start:end + 1], "extracted"))
    for candidate, how in candidates:
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        return (obj, how) if isinstance(obj, dict) else (None, "not_an_object")
    return None, "not_json"


def teacher_forced(episodes, arm, completions):
    """Score one completion per event (keyed '<episode>/<event>/<arm>') against the gold memory before it."""
    scored = []
    for episode in episodes:
        replay_gold(episode)
        catalogs = catalogs_of(episode)
        for step in gold_trajectory(episode):
            event, gold = step["event"], step["event"]["gold"]
            memory = copy.deepcopy(step["before"][arm])
            obj, how = parse_output(completions.get(f"{episode['episode_id']}/{event['event_id']}/{arm}"))
            if obj is None:
                status, reason = "invalid", how
            else:
                reason = memory.apply(obj, event["event_id"], step["seen"])[0]
                status = "rejected" if reason else "ok"
            pre = canonical_state(step["state_before"], catalogs)
            expected = canonical_state(gold["state_after"], catalogs)
            read, unmatched = READERS[arm](memory.view(), catalogs)
            if status == "ok" and unmatched:
                status = "uninterpretable"
            decision = obj.get("decision") if status in ("ok", "uninterpretable") else None
            targeted = {(attribute, key) for _, attribute, key in step["changes"]}
            untouched = [(a, k) for a, entry in pre.items() for k in entry["exceptions"] if (a, k) not in targeted]
            category = gold["category"]
            readable = status != "uninterpretable"  # rule-reader metrics skip memory the reader cannot parse
            scored.append({
                "id": f"{episode['episode_id']}/{event['event_id']}/{arm}", "episode_id": episode["episode_id"],
                "event_id": event["event_id"], "arm": arm, "category": category, "status": status, "reason": reason,
                "decision": decision, "decision_correct": decision == gold["decision"],
                "state_correct": status == "ok" and read == expected,
                "general_changed": (any(read.get(a, {}).get("general") != pre[a]["general"] for a in pre)
                                    if readable else None),
                "missed_update": (any(read.get(a, {}).get("general") != expected[a]["general"]
                                      for kind, a, _ in step["changes"] if kind == "general") if readable else None),
                "exception_disturbed": (any(read.get(a, {}).get("exceptions", {}).get(k) != pre[a]["exceptions"][k]
                                            for a, k in untouched) if untouched and readable else None),
                "wrote": memory.view() != step["before"][arm].view()})
            scored[-1]["row_correct"] = scored[-1]["state_correct"] and scored[-1]["decision_correct"]
    return scored


def _if_readable(field):
    """Per-row value that leaves out outputs whose memory the rule reader cannot parse."""
    return lambda s: None if s["status"] == "uninterpretable" else s[field]


TEACHER_FORCED_METRICS = (  # name, rows it applies to (None = all), per-row value (None = not applicable)
    ("row_correct", None, lambda s: s["row_correct"]),
    ("row_correct_if_readable", None, _if_readable("row_correct")),
    ("state_correct", None, lambda s: s["state_correct"]),
    ("state_correct_if_readable", None, _if_readable("state_correct")),
    ("decision_correct", None, lambda s: s["decision_correct"]),
    ("false_overwrite", tuple(c for c in CATEGORIES if c != "general_update"), lambda s: s["general_changed"]),
    ("missed_update", ("general_update",), lambda s: s["missed_update"]),
    ("exception_disturbed", None, lambda s: s["exception_disturbed"]),
    ("spurious_write", NO_CHANGE, lambda s: s["wrote"]),
    ("clarify_recall", ("clarify",), lambda s: s["decision"] == "clarify"),
    ("false_clarify", tuple(c for c in CATEGORIES if c != "clarify"), lambda s: s["decision"] == "clarify"),
)
RULE_READER_METRICS = ("row_correct", "row_correct_if_readable", "state_correct", "state_correct_if_readable",
                       "false_overwrite", "missed_update", "exception_disturbed")
PARSE_FAILURE_METRICS = (  # outputs that could not be scored as written
    ("invalid_output", None, lambda s: s["status"] == "invalid"),
    ("rejected_by_executor", None, lambda s: s["status"] == "rejected"),
    ("rule_reader_parse_failure", None, lambda s: s["status"] == "uninterpretable"),
    ("rule_reader_parse_failure_if_accepted", None,
     lambda s: s["status"] == "uninterpretable" if s["status"] in ("ok", "uninterpretable") else None),
)
TEACHER_FORCED_NOTE = ("Diagnostic only. The metrics named in rule_reader_metrics read memory with the rule reader, "
                       "which accepts only the canonical CRUD sentences; outputs it cannot parse are counted in "
                       "parse_failures. The primary result is Answer Agent QA from rollout-score --answers.")


def rollout(episode, arm, policy):
    """Run one arm with its own memory. policy(arm, system, prompt, context) returns the raw completion."""
    catalogs = catalogs_of(episode)
    memory = ScopeMemory() if arm == "scope" else CrudMemory()
    memory.seed(episode["initial_state"], catalogs)
    seen, steps, snapshots = ["seed"], [], {}
    for event in episode["events"]:
        seen.append(event["event_id"])
        prompt = canon(policy_input(memory.view(), event))
        completion = policy(arm, POLICY_INSTRUCTIONS[arm], prompt,
                            {"episode_id": episode["episode_id"], "event_id": event["event_id"]})
        obj, how = parse_output(completion)
        reason = how if obj is None else memory.apply(obj, event["event_id"], seen)[0]
        steps.append({"event_id": event["event_id"], "completion": completion, "accepted": reason is None,
                      "reason": reason})
        snapshots[event["event_id"]] = memory.view()
    return {"episode_id": episode["episode_id"], "arm": arm, "steps": steps, "snapshots": snapshots}


def answer_prompt(view, probe):
    """Input for the fixed Answer Agent; identical wording for both arms."""
    return (f"Memory records:\n{json.dumps(view, ensure_ascii=False, indent=1)}\n\nDate: {probe['date']}\n"
            f"Question: {probe['question']}\nOptions: {' | '.join(probe['options'])}\n"
            "Reply with exactly one option.")


def score_rollouts(episodes, trajectories, answers=None, count_tokens=None):
    """Score QA probes on rollout snapshots. answers maps '<episode>/<probe>/<arm>' to the Answer Agent's reply."""
    by_id = {e["episode_id"]: e for e in episodes}
    scored = []
    for trajectory in trajectories:
        episode = by_id[trajectory["episode_id"]]
        catalogs = catalogs_of(episode)
        arm = trajectory["arm"]
        rejected = sum(not step["accepted"] for step in trajectory["steps"])
        for probe in episode.get("probes", []):
            view = trajectory["snapshots"][probe["after_event"]]
            key = f"{episode['episode_id']}/{probe['probe_id']}/{arm}"
            read, unmatched = READERS[arm](view, catalogs)
            if answers is None:
                raw = oracle_answer(read, probe)
            else:
                raw = answers.get(key)
            answer = None if raw is None else canonical_value(catalogs[probe["attribute"]], raw)
            scored.append({"id": key, "episode_id": episode["episode_id"], "arm": arm,
                           "qa_group": probe["category"], "probe_type": probe["probe_type"],
                           "answer": answer, "correct": answer == probe["gold"],
                           "reader": "oracle" if answers is None else "answer_agent", "memory_readable": not unmatched,
                           "memory_records": len(view), "memory_words": len(json.dumps(view).split()),
                           "memory_tokens": count_tokens(json.dumps(view)) if count_tokens else None,
                           "episode_rejected_outputs": rejected, "episode_steps": len(trajectory["steps"])})
    return scored


ROLLOUT_WRITE_METRICS = (
    ("rollout_false_overwrite", tuple(c for c in CATEGORIES if c != "general_update"), lambda s: s["general_changed"]),
    ("rollout_missed_update", ("general_update",), lambda s: s["missed_update"]),
    ("rollout_spurious_write", NO_CHANGE, lambda s: s["wrote"]),
    ("rollout_state_matches_gold", None, lambda s: s["state_matches_gold"]),
    ("rollout_state_matches_gold_if_readable", None,
     lambda s: s["state_matches_gold"] if s["readable_after"] else None),
)
ROLLOUT_NOTES = {
    "primary": ("Primary result: Answer Agent QA on each arm's own memory (<arm>.metrics, <arm>.by_probe_type, "
                "scope_minus_crud). <arm>.diagnostic holds rule-reader numbers, which are diagnostics only."),
    "diagnostic": ("Diagnostic only: QA read by the oracle rule reader, a pipeline check and not a formal result. "
                   "CRUD memory outside the canonical sentences counts as a parse failure here."),
}


def rollout_write_rows(episodes, trajectories):
    """Per-event write behaviour along each arm's own memory (no gold roll-in); unreadable memory is not scored."""
    by_id = {e["episode_id"]: e for e in episodes}
    rows = []
    for t in trajectories:
        episode = by_id[t["episode_id"]]
        catalogs = catalogs_of(episode)
        memory = ScopeMemory() if t["arm"] == "scope" else CrudMemory()
        memory.seed(episode["initial_state"], catalogs)
        before_view = memory.view()
        for event in episode["events"]:
            after_view = t["snapshots"][event["event_id"]]
            before, unread_before = READERS[t["arm"]](before_view, catalogs)
            after, unread_after = READERS[t["arm"]](after_view, catalogs)
            gold = canonical_state(event["gold"]["state_after"], catalogs)
            category = event["gold"]["category"]
            readable = not unread_before and not unread_after
            general = lambda state, a: state.get(a, {}).get("general")
            rows.append({"episode_id": episode["episode_id"], "event_id": event["event_id"], "arm": t["arm"],
                         "category": category, "readable": readable, "readable_after": not unread_after,
                         "wrote": after_view != before_view,
                         "general_changed": any(general(after, a) != general(before, a) for a in gold) if readable else None,
                         "missed_update": (any(general(after, a) != gold[a]["general"] for a in gold) if readable else None)
                         if category == "general_update" else None,
                         "state_matches_gold": not unread_after and after == gold,
                         "memory_after": after_view})
            before_view = after_view
    return rows


def _ci(samples):
    if not samples:
        return None
    ordered = sorted(samples)
    return [round(ordered[int(round(q * (len(ordered) - 1)))], 4) for q in (0.025, 0.975)]


def _tally(rows, field, allowed, value_of):
    num = den = 0
    for row in rows:
        if allowed is not None and row[field] not in allowed:
            continue
        value = value_of(row)
        if value is None:
            continue
        den += 1
        num += bool(value)
    return num, den


def summarize(scored, metrics, field, bootstrap=2000, seed=0):
    """Counts, rates and episode-cluster bootstrap intervals for (name, allowed values of field, value) metrics."""
    episodes = defaultdict(list)
    for row in scored:
        episodes[row["episode_id"]].append(row)
    names = sorted(episodes)
    tables = {e: {name: _tally(episodes[e], field, allowed, fn) for name, allowed, fn in metrics} for e in names}
    rng = random.Random(seed)
    picks = [[names[rng.randrange(len(names))] for _ in names] for _ in range(bootstrap)] if names else []
    out = {}
    for name, _, _ in metrics:
        num = sum(tables[e][name][0] for e in names)
        den = sum(tables[e][name][1] for e in names)
        if not den:
            continue
        samples = []
        for pick in picks:
            d = sum(tables[e][name][1] for e in pick)
            if d:
                samples.append(sum(tables[e][name][0] for e in pick) / d)
        out[name] = {"count": num, "denominator": den, "rate": round(num / den, 4), "ci95": _ci(samples)}
    return out


def summarize_teacher_forced(scored, bootstrap=2000, seed=0):
    by_category = {c: summarize(scored, (("row_correct", (c,), lambda s: s["row_correct"]),), "category",
                                bootstrap, seed).get("row_correct") for c in CATEGORIES}
    return {"role": "diagnostic", "role_note": TEACHER_FORCED_NOTE,
            "events": len(scored), "episodes": len({s["episode_id"] for s in scored}),
            "parse_failures": summarize(scored, PARSE_FAILURE_METRICS, "category", bootstrap, seed),
            "metrics": summarize(scored, TEACHER_FORCED_METRICS, "category", bootstrap, seed),
            "rule_reader_metrics": list(RULE_READER_METRICS),
            "row_correct_by_category": {c: v for c, v in by_category.items() if v},
            "status": dict(Counter(s["status"] for s in scored)),
            "rejection_reasons": dict(Counter(s["reason"] for s in scored if s["reason"]))}


def summarize_rollouts(scored, bootstrap=2000, seed=0, write_rows=None):
    """QA per arm (primary when every probe was answered by the Answer Agent); rule-reader numbers kept apart."""
    role = "primary" if scored and all(s["reader"] == "answer_agent" for s in scored) else "diagnostic"
    report, arms = {"role": role, "role_note": ROLLOUT_NOTES[role]}, {}
    probe_sets = {arm: {s["id"].rsplit("/", 1)[0] for s in scored if s["arm"] == arm} for arm in ARMS}
    for arm in ARMS:
        rows = [s for s in scored if s["arm"] == arm]
        if not rows:
            continue
        metrics = [("qa_accuracy", None, lambda s: s["correct"])]
        metrics += [(f"qa_{g}", (g,), lambda s: s["correct"]) for g in QA_GROUPS]
        by_type = summarize(rows, [(f"qa_{t}", (t,), lambda s: s["correct"])
                                   for t in sorted({s["probe_type"] for s in rows})], "probe_type", bootstrap, seed)
        episodes = {s["episode_id"]: s for s in rows}
        arms[arm] = {"probes": len(rows), "reader": rows[0]["reader"],
                     "metrics": summarize(rows, metrics, "qa_group", bootstrap, seed), "by_probe_type": by_type,
                     "missing_answers": sum(s["reader"] == "answer_agent" and s["answer"] is None for s in rows),
                     "rejected_outputs": sum(s["episode_rejected_outputs"] for s in episodes.values()),
                     "steps": sum(s["episode_steps"] for s in episodes.values()),
                     "mean_memory_records_at_probes": round(sum(s["memory_records"] for s in rows) / len(rows), 2),
                     "mean_memory_words_at_probes": round(sum(s["memory_words"] for s in rows) / len(rows), 1)}
        tokens = [s["memory_tokens"] for s in rows if s.get("memory_tokens") is not None]
        if tokens:
            arms[arm]["mean_memory_tokens_at_probes"] = round(sum(tokens) / len(tokens), 1)
        diagnostic = summarize(rows, (("rule_reader_parse_failure_at_probes", None,
                                       lambda s: not s["memory_readable"]),), "qa_group", bootstrap, seed)
        if write_rows is not None:
            own = [r for r in write_rows if r["arm"] == arm]
            diagnostic.update(summarize(own, (("rule_reader_parse_failure_after_events", None,
                                               lambda s: not s["readable_after"]),), "category", bootstrap, seed))
            diagnostic["write_metrics"] = summarize(own, ROLLOUT_WRITE_METRICS, "category", bootstrap, seed)
        arms[arm]["diagnostic"] = diagnostic
    if all(arm in arms for arm in ARMS):
        report["pairing_complete"] = probe_sets["scope"] == probe_sets["crud"]
        if report["pairing_complete"]:
            report["scope_minus_crud"] = _paired_qa(scored, bootstrap, seed)
    if "crud" in arms:  # reported on its own: how often the rule reader could not parse the CRUD memory
        report["crud_rule_reader_parse_failure"] = {k: v for k, v in arms["crud"]["diagnostic"].items()
                                                    if k.startswith("rule_reader_parse_failure")}
    report.update(arms)
    return report


def _paired_qa(scored, bootstrap, seed):
    """Paired difference in QA accuracy (scope minus CRUD), resampling the same episodes for both arms."""
    table = defaultdict(lambda: {arm: defaultdict(lambda: [0, 0]) for arm in ARMS})
    for s in scored:
        for group in ("all", s["qa_group"]):
            cell = table[s["episode_id"]][s["arm"]][group]
            cell[0] += s["correct"]
            cell[1] += 1
    names = sorted(table)
    rng = random.Random(seed)
    picks = [[names[rng.randrange(len(names))] for _ in names] for _ in range(bootstrap)]

    def rate(pick, arm, group):
        den = sum(table[e][arm][group][1] for e in pick)
        return sum(table[e][arm][group][0] for e in pick) / den if den else None

    out = {}
    for group in ("all",) + QA_GROUPS:
        a, b = rate(names, "crud", group), rate(names, "scope", group)
        if a is None or b is None:
            continue
        diffs = [rb - ra for ra, rb in ((rate(p, "crud", group), rate(p, "scope", group)) for p in picks)
                 if ra is not None and rb is not None]
        out[group] = {"crud": round(a, 4), "scope": round(b, 4), "difference": round(b - a, 4), "ci95": _ci(diffs)}
    return out


def gold_policy(episodes):
    """Reference policy that returns the projected gold output; valid only while memory follows the gold path."""
    table = {(e["episode_id"], step["event_id"], arm): canon(step["outputs"][arm])
             for e in episodes for step in replay_gold(e) for arm in ARMS}
    return lambda arm, system, prompt, context: table[(context["episode_id"], context["event_id"], arm)]


def noop_policy(arm, system, prompt, context):
    """Reference policy that never writes."""
    return canon(NOOP_OUTPUT[arm])


def self_check(episodes, bootstrap=200, seed=0):
    """Gold must score perfectly; the NOOP reference shows what never writing costs."""
    report = {}
    for arm in ARMS:
        gold = {f"{e['episode_id']}/{s['event_id']}/{arm}": canon(s["outputs"][arm]) for e in episodes for s in replay_gold(e)}
        report[f"teacher_forced_gold_{arm}"] = summarize_teacher_forced(teacher_forced(episodes, arm, gold), bootstrap, seed)
    for name, policy in (("gold", gold_policy(episodes)), ("noop", noop_policy)):
        trajectories = [rollout(e, arm, policy) for e in episodes for arm in ARMS]
        report[f"rollout_{name}"] = summarize_rollouts(score_rollouts(episodes, trajectories), bootstrap, seed)
    return report


def _read_keyed(path, value_field):
    table = {}
    for n, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict) or "id" not in row or value_field not in row:
            raise ValueError(f"{path}:{n}: each row needs 'id' and '{value_field}'")
        if row["id"] in table:
            raise ValueError(f"{path}:{n}: duplicate id {row['id']!r}")
        table[row["id"]] = row[value_field]
    return table


def main(argv=None):
    parser = argparse.ArgumentParser(description="Evaluate memory-revision policies under protocol v1.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("self-check", "teacher-forced", "rollout-score"):
        p = sub.add_parser(name)
        p.add_argument("--data", required=True, help="episodes JSONL")
        p.add_argument("--bootstrap", type=int, default=2000)
        p.add_argument("--seed", type=int, default=0)
        p.add_argument("--out", help="also write the report JSON here")
        if name == "teacher-forced":
            p.add_argument("--arm", choices=ARMS, required=True)
            p.add_argument("--predictions", required=True, help="JSONL rows {id: '<episode>/<event>/<arm>', completion}")
            p.add_argument("--details", help="write per-event results as JSONL")
        if name == "rollout-score":
            p.add_argument("--trajectories", required=True, help="JSONL rows written by rollout()")
            p.add_argument("--answers", help="JSONL rows {id: '<episode>/<probe>/<arm>', answer}")
            p.add_argument("--oracle-reader", action="store_true", help="score without answers (pipeline check only)")
            p.add_argument("--tokenizer", help="tokenizer directory for memory token counts")
    args = parser.parse_args(argv)
    episodes = read_episodes(args.data)
    if args.command == "self-check":
        report = self_check(episodes, args.bootstrap, args.seed)
    elif args.command == "teacher-forced":
        scored = teacher_forced(episodes, args.arm, _read_keyed(args.predictions, "completion"))
        report = {"arm": args.arm, **summarize_teacher_forced(scored, args.bootstrap, args.seed)}
        if args.details:
            Path(args.details).write_text("".join(json.dumps(s) + "\n" for s in scored), encoding="utf-8")
    else:
        trajectories = [json.loads(line) for line in Path(args.trajectories).read_text(encoding="utf-8").splitlines()
                        if line.strip()]
        answers = _read_keyed(args.answers, "answer") if args.answers else None
        count_tokens = None
        if args.tokenizer:
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
            count_tokens = lambda text: len(tokenizer(text, add_special_tokens=False)["input_ids"])
        report = summarize_rollouts(score_rollouts(episodes, trajectories, answers, count_tokens), args.bootstrap,
                                    args.seed, rollout_write_rows(episodes, trajectories))
        if answers is None:
            report["reader"] = "oracle: pipeline check only, not a formal result"
            if not args.oracle_reader:
                report["reader_warning"] = "no --answers given and --oracle-reader not set"
                print("WARNING: scoring with the oracle reader; pass --answers for formal results", file=sys.stderr)
    report = {"data": args.data, "command": args.command, **report}
    text = json.dumps(report, indent=2)
    print(text)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
