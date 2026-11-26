"""Larger reader against the 4B reader (docs/analysis.md, "Larger reader"): on dev or test, experiments A and B for
both readers side by side, the same numbers by probe type and question group, and the readings fixed before the
runs; on the challenge set, which has no read-time runs, both arms' memories, also by stressor.

    cd ~/scope-sft-work    # the folder that holds runs/
    python3 -I $REPO/training/sft/bigreader_report.py $REPO runs runs/bigreader_qwen3-30b-a3b-instruct-2507 \
        $REPO/results/posthoc/bigreader_dev.json
    python3 -I $REPO/training/sft/bigreader_report.py --split test $REPO runs \
        runs/bigreader_qwen3-30b-a3b-instruct-2507 $REPO/results/posthoc/bigreader_test.json

The second and third arguments each hold the split's runs (the 4B runs, and those of the larger reader):
  dev (default)  sft_p12_eval_s{0,1,2}, reference_gold_p12, readtime/dev_{history,sft_s0,sft_s1,sft_s2,gold}
  test           test_p12_sft_s{0,1,2}, test_p12_gold, readtime/test_{history,sft_s0,sft_s1,sft_s2,gold}
  challenge      challenge_p12_ffeb6a87_sft_s{0,1,2}, challenge_p12_ffeb6a87_gold
Numbers are percentages, with 95% intervals from the episode bootstrap (2,000 resamples, seed 0, as in Tables 8 and
9); the family bootstrap is printed for the readings, which are judged on the point estimates as they were written
(the test lead also on its interval). Standard library only.
"""
import argparse
import json
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description="Larger reader against the 4B reader (post-hoc; docs/analysis.md).")
parser.add_argument("repo", type=Path, help="the repository")
parser.add_argument("small", type=Path, help="the folder with the 4B runs")
parser.add_argument("big", type=Path, help="the folder with the larger reader's runs")
parser.add_argument("out", type=Path, nargs="?", help="the JSON report to write")
parser.add_argument("--split", choices=("dev", "test", "challenge"), default="dev")
args = parser.parse_args()
SPLIT = args.split
sys.path.insert(0, str(args.repo))
from scope_memory import analysis, posthoc, readtime  # noqa: E402

SEEDS = (0, 1, 2)
CHALLENGE = "challenge_p12_ffeb6a87"  # the challenge set's run names carry its data hash (training/challenge_v1)
RUNS = {"dev": ([f"sft_p12_eval_s{k}" for k in SEEDS], "reference_gold_p12"),
        "test": ([f"test_p12_sft_s{k}" for k in SEEDS], "test_p12_gold"),
        "challenge": ([f"{CHALLENGE}_sft_s{k}" for k in SEEDS], f"{CHALLENGE}_gold")}
GROUPS = [("type_target", "target"), ("type_default", "default (ordinary occasion)"),
          ("type_neighbor", "neighbouring situation"), ("type_boundary", "boundary"),
          ("general_update", "group: general update"), ("scoped_exception", "group: scoped exception"),
          ("exception_revision", "group: exception revision"), ("stable_preference", "group: stable preference")]


def memory_report(sft, gold):
    """Both arms' memories after SFT (pooled over seeds) and gold memory, and scope-aware - CRUD for each, by probe
    type, question group and stressor."""
    info = posthoc.probe_table(gold["episodes"])
    series = {}
    for label, runs in (("sft", sft), ("gold", [gold])):
        for arm in ("crud", "scope"):
            table = analysis.correctness(runs, arm)
            if set(table) != set(info):
                raise ValueError(f"{label} {arm}: other probes than the gold run's")
            series[f"{label}_{arm}"] = table
        series[f"{label}_scope_minus_crud"] = {k: series[f"{label}_scope"][k] - series[f"{label}_crud"][k]
                                               for k in info}
    groups = analysis.groups_for(info)
    return {"sft_runs": [posthoc._posix(r["path"]) for r in sft], "gold_run": posthoc._posix(gold["path"]),
            "probes": len(info), "episodes": len({i["episode_id"] for i in info.values()}),
            "by_unit": {unit: posthoc.cluster_means(series, info, unit, groups=groups) for unit in posthoc.UNITS}}


def reports(root):
    sft_names, gold_name = RUNS[SPLIT]
    sft = [analysis.load_run(root / name) for name in sft_names]
    gold = analysis.load_run(root / gold_name)
    if SPLIT == "challenge":
        return memory_report(sft, gold), None
    a = readtime.experiment_a(readtime.load_readtime(root / "readtime" / f"{SPLIT}_history"), sft, gold)
    displays = [readtime.load_readtime(root / "readtime" / f"{SPLIT}_sft_s{k}") for k in SEEDS]
    displays.append(readtime.load_readtime(root / "readtime" / f"{SPLIT}_gold"))
    b = readtime.experiment_b(displays, sft, gold)
    return a, b


def fmt(entry, signed):
    m, (lo, hi) = (100 * entry["mean"], [100 * x for x in entry["ci95"]])
    f = "{:+.1f}" if signed else "{:.1f}"
    return f"{f.format(m)} [{f.format(lo)}, {f.format(hi)}]"  # ASCII minus: the Windows console is not UTF-8


def value(series_set, key, unit="episode"):
    return series_set["by_unit"][unit]["all"][key]


def both_units(series_set, key):
    return (f"{fmt(value(series_set, key), True)} by episode, {fmt(value(series_set, key, 'family'), True)} "
            f"by family")


def replication(small_set, big_set):
    """The dev finding (fixed as a reading for test and the challenge set): SFT CRUD on ordinary-occasion questions
    falls by more than 5 points with the larger reader."""
    before, after = (100 * s["by_unit"]["episode"]["type_default"]["sft_crud"]["mean"] for s in (small_set, big_set))
    word = "REPLICATES" if before - after > 5 else "DOES NOT REPLICATE"
    print(f"  Dev finding on ordinary-occasion questions: {word} (SFT CRUD falls by more than 5 points): "
          f"{before:.1f} -> {after:.1f} ({after - before:+.1f})")


readers = {"4B": reports(args.small), "larger": reports(args.big)}

if SPLIT == "challenge":
    for name, (m, _) in readers.items():
        print(f"{name}: {m['probes']} probes / {m['episodes']} episodes")
    M_ROWS = [("sft_crud", "SFT CRUD memory", False), ("sft_scope", "SFT scope-aware memory", False),
              ("sft_scope_minus_crud", "SFT scope-aware - CRUD", True), ("gold_crud", "Gold CRUD memory", False),
              ("gold_scope", "Gold scope-aware memory", False),
              ("gold_scope_minus_crud", "Gold scope-aware - CRUD", True)]
    print("\nChallenge set, both arms' memories (episode bootstrap)")
    print(f"  {'':26s} {'4B reader':24s} {'larger reader':24s}")
    for key, label, signed in M_ROWS:
        cells = [fmt(r[0]["by_unit"]["episode"]["all"][key], signed) for r in readers.values()]
        print(f"  {label:26s} {cells[0]:24s} {cells[1]:24s}")
    stressors = [(g, "stressor: " + g[len("stressor_"):]) for g in readers["larger"][0]["by_unit"]["episode"]
                 if g.startswith("stressor_")]
    print("\nBy group (challenge set, episode bootstrap; 4B reader -> larger reader)")
    for key, label, signed in M_ROWS:
        print(f"  {label}")
        for group, glabel in [("all_but_boundary", "all but boundary")] + GROUPS + stressors:
            entries = [r[0]["by_unit"]["episode"].get(group) for r in readers.values()]
            if not all(entries):
                continue
            print(f"    {glabel:28s} {entries[1]['probes']:5d} probes  {fmt(entries[0][key], signed):24s} -> "
                  f"{fmt(entries[1][key], signed)}")
    print("\nReadings fixed before the runs (larger reader):")
    big = readers["larger"][0]
    print(f"  Challenge set: described, not judged. SFT scope-aware - CRUD: {both_units(big, 'sft_scope_minus_crud')}"
          f" (4B: {fmt(value(readers['4B'][0], 'sft_scope_minus_crud'), True)})")
    replication(readers["4B"][0], big)
else:
    for name, (a, b) in readers.items():
        print(f"{name}: A {a['probes']} probes / {a['episodes']} episodes, answer line missing "
              f"{a['answer_line_missing']}, history_check {json.dumps(a['history_check'])}")
        for label in ("sft", "gold"):
            s = b["sets"][label]
            print(f"  B {label}: {s['probes']} probes, answer line missing {s['answer_line_missing']}, "
                  f"display_check {json.dumps(s['display_check'])}")

    A_ROWS = [("history", "Raw history, no memory", False), ("sft_crud", "SFT CRUD memory", False),
              ("sft_scope", "SFT scope-aware memory", False), ("gold_crud", "Gold CRUD memory", False),
              ("gold_scope", "Gold scope-aware memory", False),
              ("history_minus_sft_crud", "History - SFT CRUD", True),
              ("history_minus_sft_scope", "History - SFT scope", True),
              ("history_minus_gold_crud", "History - gold CRUD", True),
              ("history_minus_gold_scope", "History - gold scope", True)]
    print(f"\nA ({SPLIT}, episode bootstrap)")
    print(f"  {'':26s} {'4B reader':24s} {'larger reader':24s}")
    for key, label, signed in A_ROWS:
        cells = [fmt(r[0]["by_unit"]["episode"]["all"][key], signed) for r in readers.values()]
        print(f"  {label:26s} {cells[0]:24s} {cells[1]:24s}")

    B_ROWS = [("original", False), ("replay", False), ("compact", False), ("sentences", False), ("crud", False),
              ("compact_minus_replay", True), ("sentences_minus_replay", True), ("display_part", True),
              ("content_part", True), ("original_minus_crud", True)]
    for label in ("sft", "gold"):
        print(f"\nB, {'after SFT (3 seeds)' if label == 'sft' else 'gold memory'} ({SPLIT}, episode bootstrap)")
        print(f"  {'':26s} {'4B reader':24s} {'larger reader':24s}")
        for key, signed in B_ROWS:
            cells = [fmt(r[1]["sets"][label]["by_unit"]["episode"]["all"][key], signed) for r in readers.values()]
            print(f"  {key:26s} {cells[0]:24s} {cells[1]:24s}")
        shares = [sum(e["replay_same_answer"]["share"] for e in r[1]["sets"][label]["per_run"]) /
                  len(r[1]["sets"][label]["per_run"]) for r in readers.values()]
        print(f"  {'replay same answer':26s} {100 * shares[0]:.1f}%{'':19s} {100 * shares[1]:.1f}%")

    print(f"\nBy probe type and question group ({SPLIT}, episode bootstrap; 4B reader -> larger reader)")
    by_group = [("A", "history", None, False), ("A", "sft_crud", None, False), ("A", "sft_scope", None, False),
                ("A", "gold_crud", None, False), ("A", "gold_scope", None, False)]
    by_group += [("B", key, s, True) for s in ("sft", "gold")
                 for key in ("compact_minus_replay", "display_part", "content_part", "original_minus_crud")]
    for part, key, s, signed in by_group:
        print(f"  {part} {key}{'' if s is None else ', ' + s}")
        for group, label in GROUPS:
            cells = []
            for a, b in readers.values():
                series = a if part == "A" else b["sets"][s]
                cells.append(fmt(series["by_unit"]["episode"][group][key], signed))
            n = (readers["larger"][0] if part == "A" else readers["larger"][1]["sets"][s])["by_unit"]["episode"][group]
            print(f"    {label:28s} {n['probes']:5d} probes  {cells[0]:24s} -> {cells[1]}")

    print("\nReadings fixed before the runs (larger reader; judged on the point estimates):")
    a, b = readers["larger"]
    gaps = {m: 100 * value(a, f"history_minus_sft_{m}")["mean"] for m in ("crud", "scope")}
    if all(g <= -10 for g in gaps.values()):
        verdict = "HOLDS: the raw history stays at least 10 points below each SFT memory"
    elif any(g > -5 for g in gaps.values()):
        verdict = "DOES NOT HOLD: a gap under 5 points, so A's result was mostly a property of the small reader"
    else:
        verdict = "IN BETWEEN: gaps of 5 to 10 points, weaker than the rule for 'holds' but not under 5"
    print(f"  A: {verdict}")
    for m in ("crud", "scope"):
        print(f"     history - SFT {m}: {both_units(a, f'history_minus_sft_{m}')}")
    sft, gold = b["sets"]["sft"], b["sets"]["gold"]
    disp = {s: 100 * value(b["sets"][s], "display_part")["mean"] for s in ("sft", "gold")}
    content = 100 * value(sft, "content_part")["mean"]
    ok = all(v > 0 for v in disp.values()) and content <= 0
    print(f"  B display reading: {'HOLDS' if ok else 'DOES NOT HOLD'} (display part > 0 for SFT and gold, content "
          f"part of SFT not positive)")
    for s in ("sft", "gold"):
        print(f"     display part, {s}: {both_units(b['sets'][s], 'display_part')}")
    print(f"     content part, sft: {both_units(sft, 'content_part')}")
    cost = {s: 100 * value(b["sets"][s], "compact_minus_replay")["mean"] for s in ("sft", "gold")}
    print(f"  B compact cost: {'HOLDS' if all(v < 0 for v in cost.values()) else 'DOES NOT HOLD'} (compact - replay "
          f"< 0 for SFT and gold)")
    for s in ("sft", "gold"):
        print(f"     compact - replay, {s}: {both_units(b['sets'][s], 'compact_minus_replay')}")
    if SPLIT == "test":
        lead = value(sft, "original_minus_crud")
        if lead["mean"] > 0 and lead["ci95"][0] > 0:
            verdict = "STAYS: scope-aware - CRUD after SFT is positive and its interval excludes zero"
        elif lead["mean"] <= 0:
            verdict = "DOES NOT STAY: scope-aware - CRUD after SFT is zero or below"
        else:
            verdict = "POSITIVE, INTERVAL REACHES ZERO"
        print(f"  Test lead: {verdict}")
        print(f"     scope-aware - CRUD, sft: {both_units(sft, 'original_minus_crud')} (4B: "
              f"{fmt(value(readers['4B'][1]['sets']['sft'], 'original_minus_crud'), True)})")
        replication(readers["4B"][0], a)

if args.out:
    body = {name: ({"memory": r[0]} if SPLIT == "challenge" else {"a": r[0], "b": r[1]}) for name, r in readers.items()}
    args.out.write_text(json.dumps(body, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"\nwrote {args.out}")
