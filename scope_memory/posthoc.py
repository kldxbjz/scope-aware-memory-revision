"""Post-hoc analyses of the final results (docs/analysis.md, "Post-hoc analyses").

The test split was evaluated once, on 2026-11-24, with the pre-specified analyses in scope_memory.analysis. The
analyses here were written afterwards to describe those results and to compare them with dev. None was planned before
the test run, none changes a setting, and the pre-specified numbers stay the reported result.

  python3 -m scope_memory.posthoc decompose --sft RUN [RUN ...] --gold RUN
  python3 -m scope_memory.posthoc mechanism RUN [RUN ...]
  python3 -m scope_memory.posthoc cost --sft RUN [RUN ...] [--zero-shot RUN] [--six-shot RUN] [--gold RUN] [--noop RUN]
  python3 -m scope_memory.posthoc composition DATA [DATA ...]
  python3 -m scope_memory.posthoc dev-vs-test --dev-sft RUN [RUN ...] --dev-gold RUN --test-sft RUN [RUN ...]
                                              --test-gold RUN

Every command prints a JSON report and also writes it to --out when given.

decompose splits the SFT scope-minus-CRUD difference on each probe into two parts that add up to it:
  format = gold scope - gold CRUD: how much better the Answer Agent reads the scope format when the memory is right;
  write  = (SFT scope - gold scope) - (SFT CRUD - gold CRUD): how much less the scope arm loses against its own gold
           memory than the CRUD arm does, that is, the difference in how well the two arms write.
Intervals are 95% bootstrap intervals with two resampling units: the episode (one fictional user; the unit of the
pre-specified analyses) and the family (one preference attribute; train, dev and test have 28 each and share none),
which shows how far a result carries over to other attributes.
mechanism: teacher-forced write metrics of each arm pooled over seeds (every event's output applied to the gold memory
before it, as in scope_memory.evaluate), whether the operation structure matches gold, and the paired scope-minus-CRUD
difference. These read memory with the rule readers: diagnostics, not results.
Standard library only.
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

from .analysis import CONDITIONS, GROUPS, STRUCTURE, _in_group, _picks, _write, correctness, load_run, probe_info
from .evaluate import (PARSE_FAILURE_METRICS, RULE_READER_METRICS, TEACHER_FORCED_METRICS, _ci, _read_keyed, _tally,
                       parse_output, teacher_forced)
from .protocol import ARMS, CATEGORIES, PROBE_TYPES, QA_GROUPS, read_episodes, sft_rows

UNITS = ("episode", "family")
PARTS = ("total", "format", "write")
POSTHOC_NOTE = ("Post-hoc: written after the single test run to describe it; not part of the pre-specified analysis. "
                "The pre-specified numbers are in results/test_p12/report.json.")


# ---------------------------------------------------------------- probes, families and cluster bootstrap

def family_of(episode):
    """The episode's family (one preference attribute in data v1.1); the episode id when it has none."""
    return episode.get("family") or episode["episode_id"]


def probe_table(episodes):
    """scope_memory.analysis.probe_info plus each probe's family."""
    family = {e["episode_id"]: family_of(e) for e in episodes}
    info = probe_info(episodes)
    for i in info.values():
        i["family"] = family[i["episode_id"]]
    return info


def _posix(path):
    """A run path as given, with forward slashes, so that reports made on any system are equal."""
    return Path(path).as_posix()


def _unit(info_row, unit):
    return info_row["episode_id"] if unit == "episode" else info_row["family"]


def cluster_means(series, info, unit="episode", groups=GROUPS, bootstrap=2000, seed=0, keep=False):
    """Mean of each series (name -> {probe: value}) in each group, with a 95% bootstrap interval that draws units
    (episodes or families) with replacement, each with all its probes. With the episode unit the draws are those of
    scope_memory.analysis. keep=True also returns the mean of every draw (None where a draw holds no probe of the
    group), in the same order for every group and series."""
    names = list(series)
    picks = _picks({_unit(i, unit) for i in info.values()}, bootstrap, seed)
    out = {}
    for group in groups:
        cells = defaultdict(lambda: [0.0] * (len(names) + 1))
        for key, i in info.items():
            if _in_group(i, group):
                cell = cells[_unit(i, unit)]
                for n, name in enumerate(names):
                    cell[n] += series[name][key]
                cell[-1] += 1
        probes = int(sum(c[-1] for c in cells.values()))
        if not probes:
            continue
        cells = dict(cells)
        drawn = [[cells[u] for u in pick if u in cells] for pick in picks]
        sizes = [sum(c[-1] for c in d) for d in drawn]
        entry = {"probes": probes, "units": len(cells)}
        for n, name in enumerate(names):
            draws = [sum(c[n] for c in d) / m if m else None for d, m in zip(drawn, sizes)]
            entry[name] = {"mean": round(sum(c[n] for c in cells.values()) / probes, 4),
                           "ci95": _ci([x for x in draws if x is not None])}
            if keep:
                entry[name]["draws"] = draws
        out[group] = entry
    return out


def _drop_draws(obj):
    if isinstance(obj, dict):
        return {k: _drop_draws(v) for k, v in obj.items() if k != "draws"}
    if isinstance(obj, list):
        return [_drop_draws(v) for v in obj]
    return obj


# ---------------------------------------------------------------- format versus write

def _tables(sft_runs, gold_run):
    info = probe_table(sft_runs[0]["episodes"])
    if probe_table(gold_run["episodes"]) != info:
        raise ValueError("the SFT and gold runs cover different probes")
    return info, {arm: correctness(sft_runs, arm) for arm in ARMS}, {arm: correctness([gold_run], arm) for arm in ARMS}


def decomposition_series(sft, gold):
    """Per probe: total (SFT scope - SFT CRUD) = format (gold scope - gold CRUD) + write (what scope loses against its
    gold minus what CRUD loses against its gold)."""
    keys = list(sft["scope"])
    return {"total": {k: sft["scope"][k] - sft["crud"][k] for k in keys},
            "format": {k: gold["scope"][k] - gold["crud"][k] for k in keys},
            "write": {k: (sft["scope"][k] - gold["scope"][k]) - (sft["crud"][k] - gold["crud"][k]) for k in keys}}


def per_family(series, info):
    """Mean of each series per family, families sorted by name."""
    sums, counts = defaultdict(lambda: defaultdict(float)), Counter()
    for key, i in info.items():
        counts[i["family"]] += 1
        for name, values in series.items():
            sums[i["family"]][name] += values[key]
    return [{"family": f, "probes": counts[f], **{name: round(sums[f][name] / counts[f], 4) for name in series}}
            for f in sorted(counts)]


def decompose(sft_runs, gold_run, bootstrap=2000, seed=0):
    """The decomposition and both arms' accuracies (SFT pooled over seeds, gold) per group, with episode and family
    intervals, and per family."""
    info, sft, gold = _tables(sft_runs, gold_run)
    parts = decomposition_series(sft, gold)
    series = {**parts, "sft_crud": sft["crud"], "sft_scope": sft["scope"], "gold_crud": gold["crud"],
              "gold_scope": gold["scope"]}
    return {"note": POSTHOC_NOTE, "sft_runs": [_posix(r["path"]) for r in sft_runs],
            "gold_run": _posix(gold_run["path"]),
            "episodes": len({i["episode_id"] for i in info.values()}),
            "families": len({i["family"] for i in info.values()}), "probes": len(info),
            "by_unit": {unit: cluster_means(series, info, unit, bootstrap=bootstrap, seed=seed) for unit in UNITS},
            "per_family": per_family(series, info)}


# ---------------------------------------------------------------- teacher-forced mechanism metrics (diagnostic)

STRUCTURE_METRIC = ("structure_matches_gold", None, lambda s: s["structure_matches_gold"])
MECHANISM_METRICS = TEACHER_FORCED_METRICS + (STRUCTURE_METRIC,) + PARSE_FAILURE_METRICS
CATEGORY_METRICS = tuple((f"{name}:{c}", (c,), fn) for c in CATEGORIES
                         for name, _, fn in (TEACHER_FORCED_METRICS[0], STRUCTURE_METRIC))


def teacher_forced_rows(run, arm):
    """scope_memory.evaluate.teacher_forced rows of one run and arm, each with structure_matches_gold: the output's
    operation structure equals gold's (scope_memory.analysis.structure; an event without output counts as no match)."""
    completions = _read_keyed(Path(run["path"]) / f"predictions_{arm}.jsonl", "completion")
    rows = teacher_forced(run["episodes"], arm, completions)
    gold = {r["id"]: r["completion"] for e in run["episodes"] for r in sft_rows(e) if r["arm"] == arm}
    shape = STRUCTURE[arm]
    for row in rows:
        out, _ = parse_output(completions.get(row["id"]))
        row["structure_matches_gold"] = out is not None and shape(out) == shape(parse_output(gold[row["id"]])[0])
    return rows


def _stored_counts(run, arm):
    path = Path(run["path"]) / f"eval_tf_{arm}.json"
    if not path.exists():
        return None
    stored = json.loads(path.read_text(encoding="utf-8"))
    return {name: (v["count"], v["denominator"]) for part in ("metrics", "parse_failures")
            for name, v in stored.get(part, {}).items()}


def mechanism(runs, bootstrap=2000, seed=0):
    """Teacher-forced metrics per arm pooled over runs (seeds), with episode-bootstrap intervals (an episode is drawn
    with all its events and seeds) and the paired scope-minus-CRUD difference; row_correct and structure per category.
    checks: whether the recomputed counts equal each run's stored eval_tf_<arm>.json."""
    rows, checks = {arm: [] for arm in ARMS}, []
    for run in runs:
        for arm in ARMS:
            mine = teacher_forced_rows(run, arm)
            rows[arm] += mine
            stored = _stored_counts(run, arm)
            if stored is not None:
                recomputed = {name: _tally(mine, "category", allowed, fn)
                              for name, allowed, fn in TEACHER_FORCED_METRICS + PARSE_FAILURE_METRICS}
                checks.append({"run": _posix(run["path"]), "arm": arm, "matches_eval_tf": all(
                    tuple(recomputed[name]) == tuple(count) for name, count in stored.items() if name in recomputed)})
    metrics = MECHANISM_METRICS + CATEGORY_METRICS
    tables = {}
    for arm in ARMS:
        by_episode = defaultdict(list)
        for r in rows[arm]:
            by_episode[r["episode_id"]].append(r)
        tables[arm] = {e: {name: _tally(rs, "category", allowed, fn) for name, allowed, fn in metrics}
                       for e, rs in by_episode.items()}
    episodes = sorted(set(tables["scope"]) | set(tables["crud"]))
    picks = _picks(set(episodes), bootstrap, seed)
    zero = (0, 0)

    def counts(arm, name, chosen):
        table = tables[arm]
        return (sum(table[e][name][0] if e in table else 0 for e in chosen),
                sum(table[e][name][1] if e in table else 0 for e in chosen))

    summary = {}
    for name, _, _ in metrics:
        whole = {arm: counts(arm, name, episodes) for arm in ARMS}
        if not any(den for _, den in whole.values()):
            continue
        drawn = [{arm: counts(arm, name, pick) for arm in ARMS} for pick in picks]
        entry = {}
        for arm in ARMS:
            num, den = whole.get(arm, zero)
            if den:
                entry[arm] = {"count": num, "denominator": den, "rate": round(num / den, 4),
                              "ci95": _ci([d[arm][0] / d[arm][1] for d in drawn if d[arm][1]])}
        if len(entry) == len(ARMS):
            entry["scope_minus_crud"] = {
                "difference": round(whole["scope"][0] / whole["scope"][1] - whole["crud"][0] / whole["crud"][1], 4),
                "ci95": _ci([d["scope"][0] / d["scope"][1] - d["crud"][0] / d["crud"][1]
                             for d in drawn if d["scope"][1] and d["crud"][1]])}
        summary[name] = entry
    plain = {k: v for k, v in summary.items() if ":" not in k}
    by_category = defaultdict(dict)
    for key, v in summary.items():
        if ":" in key:
            name, category = key.split(":", 1)
            by_category[name][category] = v
    return {"role": "diagnostic", "note": POSTHOC_NOTE + " Teacher-forced metrics read memory with the rule readers.",
            "runs": [_posix(r["path"]) for r in runs], "episodes": len(episodes),
            "events": {arm: len(rows[arm]) for arm in ARMS}, "checks": checks,
            "rule_reader_metrics": list(RULE_READER_METRICS), "metrics": plain, "by_category": dict(by_category),
            "status": {arm: dict(Counter(r["status"] for r in rows[arm])) for arm in ARMS},
            "rejection_reasons": {arm: dict(Counter(r["reason"] for r in rows[arm] if r["reason"])) for arm in ARMS}}


# ---------------------------------------------------------------- cost

COST_MEASURES = ("policy_input_tokens", "policy_output_tokens", "answer_input_tokens", "answer_output_tokens",
                 "memory_tokens_at_probes")


def cost(run_paths):
    """Token counts per call from each run's cost.json (training/sft/cost_report.py), pooled over the runs."""
    sums = {arm: {m: [0, 0] for m in COST_MEASURES} for arm in ARMS}
    rejected = Counter()
    for path in run_paths:
        data = json.loads((Path(path) / "cost.json").read_text(encoding="utf-8"))
        for run in data["runs"].values():
            for arm, measures in run["arms"].items():
                for m in COST_MEASURES:
                    if m in measures:
                        sums[arm][m][0] += measures[m]["total"]
                        sums[arm][m][1] += measures[m]["calls"]
                rejected[arm] += measures.get("rejected_outputs", 0)
    return {"runs": [_posix(p) for p in run_paths],
            "arms": {arm: {**{m: {"calls": c, "total": t, "mean": round(t / c, 1)}
                              for m, (t, c) in sums[arm].items() if c},
                           "rejected_outputs": rejected[arm]} for arm in ARMS}}


# ---------------------------------------------------------------- what the data files contain

def _share(counter, keys=None):
    total = sum(counter.values())
    keys = keys or sorted(counter)
    return {k: {"count": counter[k], "share": round(counter[k] / total, 4) if total else 0.0} for k in keys}


def composition(paths):
    """Per data file: episodes, families, events by category, probes by type and QA group, and the gold memory of the
    probed attribute at each probe (number of situation records, their validity); families shared between files."""
    out, families = {}, {}
    for path in paths:
        episodes = read_episodes(path)
        name = Path(path).stem
        families[name] = {family_of(e) for e in episodes}
        events = [ev for e in episodes for ev in e["events"]]
        probes = [(e, p) for e in episodes for p in e.get("probes", [])]
        exceptions, validity, situated = Counter(), Counter(), 0
        for e, p in probes:
            state = next(ev["gold"]["state_after"] for ev in e["events"] if ev["event_id"] == p["after_event"])
            records = state.get(p["attribute"], {}).get("exceptions", {})
            exceptions["3+" if len(records) >= 3 else str(len(records))] += 1
            validity.update(r["validity"]["kind"] for r in records.values())
            situated += bool(p.get("situation_scope_keys"))
        out[name] = {
            "episodes": len(episodes), "families": len(families[name]),
            "two_attribute_episodes": sum(len(e["attributes"]) > 1 for e in episodes),
            "events": len(events), "events_per_episode": round(len(events) / len(episodes), 2),
            "event_categories": _share(Counter(ev["gold"]["category"] for ev in events), CATEGORIES),
            "probes": len(probes), "probes_per_episode": round(len(probes) / len(episodes), 2),
            "probe_types": _share(Counter(p["probe_type"] for _, p in probes), PROBE_TYPES),
            "qa_groups": _share(Counter(p["category"] for _, p in probes), QA_GROUPS),
            "probes_naming_a_situation": situated,
            "situation_records_at_probe": _share(exceptions, ("0", "1", "2", "3+")),
            "validity_of_situation_records_at_probes": _share(validity)}
    names = list(out)
    shared = {f"{a} & {b}": len(families[a] & families[b]) for n, a in enumerate(names) for b in names[n + 1:]}
    return {"files": out, "shared_families": shared}


# ---------------------------------------------------------------- dev against test

def _standardised(draws_by_cell, means_by_cell, weights):
    """sum_c weights[c] * mean[c], with the interval of the same sum over aligned bootstrap draws."""
    point = sum(weights[c] * means_by_cell[c] for c in weights)
    columns = [draws_by_cell[c] for c in weights]
    samples = [sum(weights[c] * x for c, x in zip(weights, row)) for row in zip(*columns) if None not in row]
    return {"mean": round(point, 4), "ci95": _ci(samples)}


def dev_vs_test(dev_sft, dev_gold, test_sft, test_gold, bootstrap=2000, seed=0):
    """The decomposition on both splits; test minus dev with independent draws (dev seed, test seed + 1); each split
    standardised to the other's mix of probe types and of QA groups; the spread over families."""
    splits, draws = {}, {}
    for name, (sft_runs, gold_run) in (("dev", (dev_sft, dev_gold)), ("test", (test_sft, test_gold))):
        info, sft, gold = _tables(sft_runs, gold_run)
        parts = decomposition_series(sft, gold)
        by_unit = {unit: cluster_means(parts, info, unit, bootstrap=bootstrap, seed=seed, keep=True) for unit in UNITS}
        families = per_family(parts, info)
        totals = [f["total"] for f in families]
        mean = sum(totals) / len(totals)
        sd = (sum((t - mean) ** 2 for t in totals) / (len(totals) - 1)) ** 0.5 if len(totals) > 1 else 0.0
        splits[name] = {"episodes": len({i["episode_id"] for i in info.values()}), "families": len(families),
                        "probes": len(info), "by_unit": by_unit, "per_family": families,
                        "family_spread": {"scope_ahead": sum(t > 0 for t in totals),
                                          "crud_ahead": sum(t < 0 for t in totals), "tied": sum(t == 0 for t in totals),
                                          "min": min(totals), "max": max(totals), "sd": round(sd, 4)}}
        draws[name] = (info, parts)
    # test minus dev, each split drawn on its own
    groups = ("all", "all_but_boundary") + tuple(f"type_{t}" for t in PROBE_TYPES)
    difference = {}
    for unit in UNITS:
        other = cluster_means(draws["test"][1], draws["test"][0], unit, groups, bootstrap, seed + 1, keep=True)
        difference[unit] = {}
        for group in groups:
            entry = {}
            for part in PARTS:
                dev_draws = splits["dev"]["by_unit"][unit][group][part]["draws"]
                test_draws = other[group][part]["draws"]
                entry[part] = {"mean": round(splits["test"]["by_unit"][unit][group][part]["mean"]
                                             - splits["dev"]["by_unit"][unit][group][part]["mean"], 4),
                               "ci95": _ci([t - d for t, d in zip(test_draws, dev_draws)
                                            if t is not None and d is not None])}
            difference[unit][group] = entry
    # each split with the other's mix of probe types and of QA groups (episode draws)
    mixes = {"probe_type": tuple(f"type_{t}" for t in PROBE_TYPES), "qa_group": QA_GROUPS}
    standardised = {}
    for source, target in (("dev", "test"), ("test", "dev")):
        standardised[f"{source}_with_{target}_mix"] = {}
        for mix, cells in mixes.items():
            src = splits[source]["by_unit"]["episode"]
            probes = {c: splits[target]["by_unit"]["episode"][c]["probes"] for c in cells}
            weights = {c: probes[c] / sum(probes.values()) for c in cells}
            standardised[f"{source}_with_{target}_mix"][mix] = {
                "weights": {c: round(w, 4) for c, w in weights.items()},
                **{part: _standardised({c: src[c][part]["draws"] for c in cells},
                                       {c: src[c][part]["mean"] for c in cells}, weights) for part in PARTS}}
    return {"note": POSTHOC_NOTE + " Dev was used during development; its runs are the protocol-1.2 dev runs.",
            "splits": _drop_draws(splits), "test_minus_dev": difference, "standardised": standardised}


# ---------------------------------------------------------------- command line

def main(argv=None):
    parser = argparse.ArgumentParser(description="Post-hoc analyses of the final results (docs/analysis.md).")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("decompose", help="SFT scope minus CRUD = format gap on gold memory + write difference")
    p.add_argument("--sft", nargs="+", required=True, metavar="RUN")
    p.add_argument("--gold", required=True, metavar="RUN")
    p = sub.add_parser("mechanism", help="teacher-forced write metrics per arm, pooled over seeds (diagnostic)")
    p.add_argument("runs", nargs="+", metavar="RUN")
    p = sub.add_parser("cost", help="tokens per call per condition and arm, from the runs' cost.json")
    for name in CONDITIONS:
        p.add_argument(f"--{name.replace('_', '-')}", dest=name, nargs="+", default=[], metavar="RUN")
    p = sub.add_parser("composition", help="what the data files contain")
    p.add_argument("data", nargs="+")
    p = sub.add_parser("dev-vs-test", help="the decomposition on dev and test, standardised and per family")
    for split in ("dev", "test"):
        p.add_argument(f"--{split}-sft", nargs="+", required=True, metavar="RUN")
        p.add_argument(f"--{split}-gold", required=True, metavar="RUN")
    for p in sub.choices.values():
        p.add_argument("--out", help="also write the JSON report here")
        p.add_argument("--bootstrap", type=int, default=2000)
        p.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv)
    if args.command == "decompose":
        out = decompose([load_run(r) for r in args.sft], load_run(args.gold), args.bootstrap, args.seed)
    elif args.command == "mechanism":
        out = mechanism([load_run(r) for r in args.runs], args.bootstrap, args.seed)
    elif args.command == "cost":
        out = {"note": POSTHOC_NOTE,
               "conditions": {name: cost(getattr(args, name)) for name in CONDITIONS if getattr(args, name)}}
    elif args.command == "composition":
        out = composition(args.data)
    else:
        out = dev_vs_test([load_run(r) for r in args.dev_sft], load_run(args.dev_gold),
                          [load_run(r) for r in args.test_sft], load_run(args.test_gold), args.bootstrap, args.seed)
    _write(out, args.out)


if __name__ == "__main__":
    main()
