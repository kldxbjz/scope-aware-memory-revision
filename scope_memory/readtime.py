"""Read-time experiments A and B (docs/analysis.md, "Read-time experiments"); post-hoc.

The team proposed both in its mid-project update of 2026-11-24, after the single test run, so they are post-hoc and
exploratory: every pre-specified number stays as reported. The Answer Agent is the frozen one (the base model without an
adapter, greedy decoding, the reply format and token budget of prompt version 3); only what it reads changes.

A, raw history: no memory manager. The Answer Agent reads the user's preferences at the start of the episode (the fixed
CRUD sentences that also seed the CRUD arm's memory) and every conversation up to and including the probe's event,
oldest first, and answers the same question with the same options. The prompt takes only the dates and the messages of
those events: nothing from the gold path, the event categories or later events.

B, the display of the same memory: a finished run's scope memory at each probe, shown three ways.
  replay     the original prompt (scope_memory.evaluate.answer_prompt) answered again: how much the answers change when
             the Answer Agent simply runs again;
  compact    one block per attribute: the general preference, then one line per situation with its dates; memory ids,
             relations and evidence ids are left out;
  sentences  the CRUD arm's display: every record as its fixed CRUD sentence, in {"id", "text"} records.
Every record of the snapshot is shown, errors included; nothing is repaired, selected or dropped. Leaving out the
relations loses nothing the reader could use as long as every situation record points at its own attribute's general
record and REPLACES points only at retired records; display_check counts both.

  python3 -m scope_memory.readtime a --history RUN --sft RUN [RUN ...] --gold RUN [--noop RUN] [--cost FILE ...]
  python3 -m scope_memory.readtime b --display RUN [RUN ...] --sft RUN [RUN ...] --gold RUN
  python3 -m scope_memory.readtime show --data DATA --probe EPISODE/PROBE [--run RUN --condition NAME]

History and display RUNs are written by training/sft/reread.py; --sft, --gold and --noop name baseline.sbatch runs and
--cost names cost reports of training/sft/cost_report.py that cover the --sft runs. a and b print a JSON report and
also write it to --out when given; show prints one prompt. Standard library only.
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from .analysis import _write, correctness, load_run
from .evaluate import ANSWER_LINE, ANSWER_READERS, answer_prompt
from .posthoc import UNITS, _posix, cluster_means, probe_table
from .protocol import (ARMS, GENERAL, PERSISTENT, PROBE_TYPES, QA_GROUPS, CrudMemory, canonical_value, catalogs_of,
                       crud_sentence, read_episodes)

READER = 3  # the frozen Answer Agent prompt version; every condition keeps its reply format and token budget
REPLY_TOKENS = ANSWER_READERS[READER][2]
HISTORY = "history"
DISPLAYS = ("replay", "compact", "sentences")
READTIME_NOTE = ("Post-hoc and exploratory: proposed after the single test run (mid-project update, 2026-11-24). The "
                 "pre-specified results are in results/test_p12/report.json.")
HISTORY_RULES = (
    "The conversations are in time order; a later conversation can change or end a preference from an earlier one. "
    "Only the user's own lasting preferences count: one-off requests, other people's preferences and changes the user "
    "has not settled leave them as they were.",
    "A preference limited to a situation or to dates applies only in that situation and on those dates; when no "
    "limited preference applies, use the general preference.")
HISTORY_REPLY = ("Before answering, say in one sentence which preference applies on this date and in this situation; "
                 "then give your choice on a final line that starts with \"Answer:\".")


# ---------------------------------------------------------------- A: the raw history

def initial_sentences(episode):
    """The preferences at the start of the episode as the fixed CRUD sentences, in the CRUD arm's seed order."""
    memory = CrudMemory()
    memory.seed(episode["initial_state"], catalogs_of(episode))
    return [r["text"] for r in memory.view()]


def events_until(episode, event_id):
    """The episode's events up to and including event_id."""
    ids = [ev["event_id"] for ev in episode["events"]]
    if event_id not in ids:
        raise ValueError(f"{episode['episode_id']} has no event {event_id}")
    return episode["events"][:ids.index(event_id) + 1]


def _question(probe):
    return [f"Date: {probe['date']}", f"Question: {probe['question']}", f"Options: {' | '.join(probe['options'])}"]


def history_prompt(episode, probe):
    """Input of the Answer Agent in A: the preferences at the start, the date and messages of every event up to the
    probe's, then the probe as in scope_memory.evaluate.answer_prompt. Nothing else of the events or the probe."""
    start = "\n".join(f"- {s}" for s in initial_sentences(episode))
    talks = "\n\n".join(f"Conversation on {ev['date']}:\n" + "\n".join(f"{m['role']}: {m['content']}"
                                                                        for m in ev["dialogue"])
                        for ev in events_until(episode, probe["after_event"]))
    return "\n".join([f"Preferences at the start:\n{start}\n", f"Conversations since then, oldest first:\n\n{talks}\n",
                      *_question(probe), *HISTORY_RULES, HISTORY_REPLY])


# ---------------------------------------------------------------- B: the display of the same memory

def _validity(validity):
    if validity["kind"] == "window":
        return f"; from {validity['from']} through {validity['to']}"
    return "; for now, with no end date given" if validity["kind"] == "open" else ""


def render_compact(view):
    """One block per attribute, in order of first appearance: the general record, then one line per situation record
    with its dates, in the order of the view."""
    blocks = []
    for attribute in dict.fromkeys(r["attribute"] for r in view):
        records = [r for r in view if r["attribute"] == attribute]
        lines = [f"{attribute}:"]
        lines += [f"- general: {r['value']}{_validity(r['validity'])}" for r in records if r["scope"] == GENERAL]
        lines += [f"- when {r['scope']}: {r['value']}{_validity(r['validity'])}" for r in records
                  if r["scope"] != GENERAL]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks) if blocks else "(none)"


def as_crud_view(view):
    """The scope records shown as the CRUD arm shows its memory: {"id", "text"} with each record's CRUD sentence."""
    return [{"id": r["memory_id"],
             "text": crud_sentence(r["attribute"], None if r["scope"] == GENERAL else r["scope"], r["value"],
                                   r["validity"])} for r in view]


def memory_block(view, condition):
    """The text between "Memory records:" and the probe in a display condition."""
    if condition not in DISPLAYS:
        raise ValueError(f"unknown display {condition}")
    if condition == "compact":
        return render_compact(view)
    return json.dumps(as_crud_view(view) if condition == "sentences" else view, ensure_ascii=False, indent=1)


def display_prompt(view, probe, condition):
    """Input of the Answer Agent in B: answer_prompt of prompt version 3 with only the memory block changed."""
    before, reply, _ = ANSWER_READERS[READER]
    return "\n".join([f"Memory records:\n{memory_block(view, condition)}\n", *_question(probe), *before, reply])


def display_check(view):
    """Counts that show whether leaving out ids and relations loses anything: bad_edges (a situation record whose
    EXCEPTION_TO does not point at its own attribute's general record, or a general record with one) and
    replaces_active (REPLACES pointing at a record still shown) should both be 0."""
    by_id = {r["memory_id"]: r for r in view}
    counts = Counter(records=len(view))
    for r in view:
        edges = [x for x in r["relations"] if x["type"] == "EXCEPTION_TO"]
        if r["scope"] == GENERAL:
            counts["general"] += 1
            counts["general_not_persistent"] += r["validity"] != PERSISTENT
            counts["bad_edges"] += bool(edges)
        else:
            counts["situation"] += 1
            counts[f"situation_{r['validity']['kind']}"] += 1
            target = by_id.get(edges[0]["target"]) if len(edges) == 1 else None
            ok = target is not None and target["scope"] == GENERAL and target["attribute"] == r["attribute"]
            counts["edges_ok" if ok else "bad_edges"] += 1
        counts["replaces_active"] += sum(x["type"] == "REPLACES" and x["target"] in by_id for x in r["relations"])
    return counts


# ---------------------------------------------------------------- loading and scoring

def _jsonl(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def load_readtime(path):
    """A run directory of training/sft/reread.py: its config, episodes, answer rows per condition and checks."""
    path = Path(path)
    config = json.loads((path / "run_config.json").read_text(encoding="utf-8"))
    conditions = [HISTORY] if config["kind"] == HISTORY else list(DISPLAYS)
    checks = path / ("history_check.json" if config["kind"] == HISTORY else "display_check.json")
    return {"path": str(path), "config": config, "episodes": read_episodes(path / "episodes.jsonl"),
            "answers": {c: {r["id"]: r for r in _jsonl(path / f"answers_{c}.jsonl")} for c in conditions},
            "checks": json.loads(checks.read_text(encoding="utf-8")) if checks.exists() else None}


def correct_table(episodes, rows, condition):
    """'<episode>/<probe>' -> 1.0 when the answer, mapped to the catalog as in scope_memory.evaluate.score_rollouts, is
    the gold option, else 0.0. Every probe needs exactly one answer."""
    out = {}
    for e in episodes:
        catalogs = catalogs_of(e)
        for p in e.get("probes", []):
            key = f"{e['episode_id']}/{p['probe_id']}"
            row = rows.get(f"{key}/{condition}")
            if row is None:
                raise ValueError(f"no {condition} answer for {key}")
            out[key] = float(canonical_value(catalogs[p["attribute"]], row["answer"]) == p["gold"])
    if len(out) != len(rows):
        raise ValueError(f"{len(rows)} {condition} answers for {len(out)} probes")
    return out


def _restrict(table, info, what):
    """table limited to the probes of info (a smoke run covers the first episodes only)."""
    if not set(info) <= set(table):
        raise ValueError(f"{what} lacks probes of the read-time run")
    return {k: table[k] for k in info}


def flips(first, second):
    """Probes right in first only, in second only, in both and in neither (first, second: probe -> 0 or 1)."""
    names = {(1, 0): "first_only", (0, 1): "second_only", (1, 1): "both", (0, 0): "neither"}
    counts = Counter({name: 0 for name in names.values()})
    for key, value in first.items():
        counts[names[(int(value), int(second[key]))]] += 1
    return dict(counts)


def flips_by(first, second, info, field):
    """first_only and second_only per value of an info field (probe_type or qa_group)."""
    out = defaultdict(lambda: {"first_only": 0, "second_only": 0, "probes": 0})
    for key, i in info.items():
        cell = out[i[field]]
        cell["probes"] += 1
        cell["first_only"] += first[key] > second[key]
        cell["second_only"] += second[key] > first[key]
    order = PROBE_TYPES if field == "probe_type" else QA_GROUPS
    return {k: out[k] for k in order if k in out}


def _stats(values):
    values = list(values)
    return {"calls": len(values), "total": sum(values), "mean": round(sum(values) / len(values), 1) if values else None}


# ---------------------------------------------------------------- A: report

def _memory_cost(cost_files, sft_runs):
    """Per arm, the tokens of one run (mean over the --sft runs) from cost reports that cover each of them."""
    names = {Path(r["path"]).name for r in sft_runs}
    found = {}
    for path in cost_files:
        for run, entry in json.loads(Path(path).read_text(encoding="utf-8"))["runs"].items():
            if Path(run).name in names:
                found[Path(run).name] = entry["arms"]
    if set(found) != names:
        return None
    out = {}
    for arm in ARMS:
        per = {m: [found[n][arm][m]["total"] for n in sorted(names)] for m in
               ("policy_input_tokens", "policy_output_tokens", "answer_input_tokens", "answer_output_tokens")}
        calls = {m: [found[n][arm][m]["calls"] for n in sorted(names)] for m in ("policy_input_tokens",
                                                                                "answer_input_tokens")}
        mean = {m: sum(v) / len(v) for m, v in per.items()}
        out[arm] = {"policy_calls": round(sum(calls["policy_input_tokens"]) / len(names), 1),
                    "answer_calls": round(sum(calls["answer_input_tokens"]) / len(names), 1),
                    **{m: round(v, 1) for m, v in mean.items()},
                    "total_tokens": round(sum(mean.values()), 1)}
    return out


def experiment_a(history_run, sft_runs, gold_run, noop_run=None, cost_files=(), bootstrap=2000, seed=0):
    """Accuracy of the raw history against the SFT memories (pooled over seeds), gold memory and, given, the
    never-written memory, with paired differences per group (episode and family bootstrap); probes that only the
    history or only a memory gets right, per seed; and the tokens of each."""
    info = probe_table(history_run["episodes"])
    history = correct_table(history_run["episodes"], history_run["answers"][HISTORY], HISTORY)
    series = {HISTORY: history}
    references = [("sft", sft_runs), ("gold", [gold_run])] + ([("noop", [noop_run])] if noop_run else [])
    for name, runs in references:
        for arm in ARMS:
            series[f"{name}_{arm}"] = _restrict(correctness(runs, arm), info, f"{name} {arm}")
    for name in ("sft_scope", "sft_crud", "gold_scope", "gold_crud"):
        series[f"history_minus_{name}"] = {k: history[k] - series[name][k] for k in info}
    per_seed = []
    for run in sft_runs:
        for arm in ARMS:
            memory = _restrict(correctness([run], arm), info, run["path"])
            counts = flips(history, memory)
            per_seed.append({"run": _posix(run["path"]), "arm": arm, "history_only": counts["first_only"],
                             "memory_only": counts["second_only"], "both": counts["both"],
                             "neither": counts["neither"],
                             "by_probe_type": {t: {"history_only": c["first_only"], "memory_only": c["second_only"],
                                                   "probes": c["probes"]}
                                               for t, c in flips_by(history, memory, info, "probe_type").items()}})
    rows = list(history_run["answers"][HISTORY].values())
    history_cost = {"policy_calls": 0, "answer_calls": len(rows),
                    "answer_input_tokens": sum(r["input_tokens"] for r in rows),
                    "answer_output_tokens": sum(r["output_tokens"] for r in rows)}
    history_cost["total_tokens"] = history_cost["answer_input_tokens"] + history_cost["answer_output_tokens"]
    return {"note": READTIME_NOTE, "history_run": _posix(history_run["path"]),
            "sft_runs": [_posix(r["path"]) for r in sft_runs], "gold_run": _posix(gold_run["path"]),
            "noop_run": _posix(noop_run["path"]) if noop_run else None,
            "probes": len(info), "episodes": len({i["episode_id"] for i in info.values()}),
            "history_check": history_run["checks"],
            "by_unit": {unit: cluster_means(series, info, unit, bootstrap=bootstrap, seed=seed) for unit in UNITS},
            "flips_per_seed": per_seed,
            "cost_per_run": {HISTORY: history_cost, **(_memory_cost(cost_files, sft_runs) or {})},
            "answer_line_missing": sum(not ANSWER_LINE.search(r["raw"]) for r in rows)}


# ---------------------------------------------------------------- B: report

def _source_name(display_run):
    return Path(display_run["config"]["from_run"]).name


def experiment_b(display_runs, sft_runs, gold_run, bootstrap=2000, seed=0):
    """For the SFT runs (pooled over seeds) and for gold memory: accuracy of the scope memory as originally shown
    (the stored answers), replayed, compact and as CRUD sentences, and of the CRUD arm; the paired differences, among
    them the split of scope minus CRUD into display (original - sentences) and content (sentences - CRUD); answers
    gained and lost against the original per run; replay agreement; tokens; and the display checks."""
    displays = {}
    for d in display_runs:
        if d["config"]["kind"] != "display":
            raise ValueError(f"{d['path']} is not a display run")
        if _source_name(d) in displays:
            raise ValueError(f"two display runs read {_source_name(d)}")
        displays[_source_name(d)] = d
    out = {"note": READTIME_NOTE, "sets": {}}
    for label, runs in (("sft", sft_runs), ("gold", [gold_run])):
        mine = []
        for run in runs:
            name = Path(run["path"]).name
            if name not in displays:
                raise ValueError(f"no display run reads {name}")
            mine.append(displays.pop(name))
        info = probe_table(mine[0]["episodes"])
        tables = {"original": _restrict(correctness(runs, "scope"), info, "the scope arm"),
                  "crud": _restrict(correctness(runs, "crud"), info, "the CRUD arm")}
        per_run = []
        for c in DISPLAYS:
            per = []
            for d in mine:
                per.append(correct_table(d["episodes"], d["answers"][c], c))
                if set(per[-1]) != set(info):
                    raise ValueError(f"{d['path']} covers other probes")
            tables[c] = {k: sum(t[k] for t in per) / len(per) for k in info}
        series = dict(tables)
        for c in DISPLAYS:
            series[f"{c}_minus_original"] = {k: tables[c][k] - tables["original"][k] for k in info}
            series[f"{c}_minus_crud"] = {k: tables[c][k] - tables["crud"][k] for k in info}
        for c in ("compact", "sentences"):  # against the replay: same job, GPU and batch size
            series[f"{c}_minus_replay"] = {k: tables[c][k] - tables["replay"][k] for k in info}
        series["original_minus_crud"] = {k: tables["original"][k] - tables["crud"][k] for k in info}
        series["display_part"] = {k: tables["original"][k] - tables["sentences"][k] for k in info}
        series["content_part"] = {k: tables["sentences"][k] - tables["crud"][k] for k in info}
        for run, d in zip(runs, mine):
            stored = {k.rsplit("/", 1)[0]: s["answer"] for k, s in run["scored"].items() if s["arm"] == "scope"}
            original = _restrict(correctness([run], "scope"), info, run["path"])
            entry = {"run": _posix(run["path"]), "display_run": _posix(d["path"])}
            for c in DISPLAYS:
                counts = flips(original, correct_table(d["episodes"], d["answers"][c], c))
                entry[c] = {"lost": counts["first_only"], "gained": counts["second_only"]}
            catalogs = {e["episode_id"]: catalogs_of(e) for e in d["episodes"]}
            attribute = {f"{e['episode_id']}/{p['probe_id']}": p["attribute"]
                         for e in d["episodes"] for p in e["probes"]}
            same = sum(canonical_value(catalogs[k.split("/")[0]][attribute[k]], d["answers"]["replay"][f"{k}/replay"]
                                       ["answer"]) == stored[k] for k in info)
            entry["replay_same_answer"] = {"probes": len(info), "same": same, "share": round(same / len(info), 4)}
            per_run.append(entry)
        tokens = {c: {field: _stats(r[field] for d in mine for r in d["answers"][c].values())
                      for field in ("input_tokens", "memory_tokens", "output_tokens")} for c in DISPLAYS}
        checks = Counter()
        for d in mine:
            checks.update(d["checks"] or {})
        out["sets"][label] = {
            "runs": [_posix(r["path"]) for r in runs], "probes": len(info),
            "by_unit": {unit: cluster_means(series, info, unit, bootstrap=bootstrap, seed=seed) for unit in UNITS},
            "per_run": per_run, "tokens": tokens, "display_check": dict(sorted(checks.items())),
            "answer_line_missing": {c: sum(not ANSWER_LINE.search(r["raw"]) for d in mine
                                           for r in d["answers"][c].values()) for c in DISPLAYS}}
    if displays:
        raise ValueError(f"display runs of other sources: {sorted(displays)}")
    return out


# ---------------------------------------------------------------- command line

def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-time experiments A and B (post-hoc; docs/analysis.md).")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("a", help="A: raw history against the memories")
    p.add_argument("--history", required=True, metavar="RUN")
    p.add_argument("--sft", nargs="+", required=True, metavar="RUN")
    p.add_argument("--gold", required=True, metavar="RUN")
    p.add_argument("--noop", metavar="RUN")
    p.add_argument("--cost", nargs="*", default=[], metavar="FILE")
    p = sub.add_parser("b", help="B: the same scope memory shown in other ways")
    p.add_argument("--display", nargs="+", required=True, metavar="RUN")
    p.add_argument("--sft", nargs="+", required=True, metavar="RUN")
    p.add_argument("--gold", required=True, metavar="RUN")
    for p in sub.choices.values():
        p.add_argument("--bootstrap", type=int, default=2000)
        p.add_argument("--seed", type=int, default=0)
        p.add_argument("--out")
    p = sub.add_parser("show", help="print one prompt: the history prompt, or with --run a display prompt")
    p.add_argument("--data", required=True, help="episodes (JSONL), or with --run that run's episodes.jsonl")
    p.add_argument("--probe", required=True, metavar="EPISODE/PROBE")
    p.add_argument("--run", help="baseline.sbatch run whose scope memory is shown")
    p.add_argument("--condition", choices=DISPLAYS, default="compact")
    args = parser.parse_args(argv)
    if args.command == "a":
        out = experiment_a(load_readtime(args.history), [load_run(r) for r in args.sft], load_run(args.gold),
                           load_run(args.noop) if args.noop else None, args.cost, args.bootstrap, args.seed)
        _write(out, args.out)
    elif args.command == "b":
        out = experiment_b([load_readtime(r) for r in args.display], [load_run(r) for r in args.sft],
                           load_run(args.gold), args.bootstrap, args.seed)
        _write(out, args.out)
    else:
        episode_id, probe_id = args.probe.split("/")
        episode = next(e for e in read_episodes(args.data) if e["episode_id"] == episode_id)
        probe = next(p for p in episode["probes"] if p["probe_id"] == probe_id)
        if not args.run:
            print(history_prompt(episode, probe))
            return
        lines = (Path(args.run) / "trajectories.jsonl").read_text(encoding="utf-8").splitlines()
        trajectory = next(t for t in map(json.loads, lines) if t["episode_id"] == episode_id and t["arm"] == "scope")
        print(display_prompt(trajectory["snapshots"][probe["after_event"]], probe, args.condition))


if __name__ == "__main__":
    main()
