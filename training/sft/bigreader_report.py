"""Larger reader against the 4B reader on dev (docs/analysis.md, "Larger reader"): experiments A and B for both
readers side by side, the same numbers by probe type and question group, and the readings fixed before any run.

    cd ~/scope-sft-work    # the folder that holds runs/
    python3 -I $REPO/training/sft/bigreader_report.py $REPO runs runs/bigreader_qwen3-30b-a3b-instruct-2507 \
        $REPO/results/posthoc/bigreader_dev.json

The second and third arguments each hold sft_p12_eval_s{0,1,2}, reference_gold_p12 and readtime/dev_{history,sft_s0,
sft_s1,sft_s2,gold} (the 4B dev runs, and those of the larger reader). Numbers are percentages on the 1,170 dev probes,
with 95% intervals from the episode bootstrap (2,000 resamples, seed 0, as in Tables 8 and 9); the family bootstrap is
printed for the readings, which are judged on the point estimates, as they were written. Standard library only.
"""
import json
import sys
from pathlib import Path

repo, small, big = (Path(a) for a in sys.argv[1:4])
out_path = Path(sys.argv[4]) if len(sys.argv) > 4 else None
sys.path.insert(0, str(repo))
from scope_memory import analysis, readtime  # noqa: E402

SEEDS = (0, 1, 2)
GROUPS = [("type_target", "target"), ("type_default", "default (ordinary occasion)"),
          ("type_neighbor", "neighbouring situation"), ("type_boundary", "boundary"),
          ("general_update", "group: general update"), ("scoped_exception", "group: scoped exception"),
          ("exception_revision", "group: exception revision"), ("stable_preference", "group: stable preference")]


def reports(root):
    sft = [analysis.load_run(root / f"sft_p12_eval_s{k}") for k in SEEDS]
    gold = analysis.load_run(root / "reference_gold_p12")
    a = readtime.experiment_a(readtime.load_readtime(root / "readtime" / "dev_history"), sft, gold)
    displays = [readtime.load_readtime(root / "readtime" / f"dev_sft_s{k}") for k in SEEDS]
    displays.append(readtime.load_readtime(root / "readtime" / "dev_gold"))
    b = readtime.experiment_b(displays, sft, gold)
    return a, b


def fmt(entry, signed):
    m, (lo, hi) = (100 * entry["mean"], [100 * x for x in entry["ci95"]])
    f = "{:+.1f}" if signed else "{:.1f}"
    return f"{f.format(m)} [{f.format(lo)}, {f.format(hi)}]"  # ASCII minus: the Windows console is not UTF-8


readers = {"4B": reports(small), "larger": reports(big)}
for name, (a, b) in readers.items():
    print(f"{name}: A {a['probes']} probes / {a['episodes']} episodes, answer line missing {a['answer_line_missing']},"
          f" history_check {json.dumps(a['history_check'])}")
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
print("\nA (dev, episode bootstrap)")
print(f"  {'':26s} {'4B reader':24s} {'larger reader':24s}")
for key, label, signed in A_ROWS:
    cells = [fmt(r[0]["by_unit"]["episode"]["all"][key], signed) for r in readers.values()]
    print(f"  {label:26s} {cells[0]:24s} {cells[1]:24s}")

B_ROWS = [("original", False), ("replay", False), ("compact", False), ("sentences", False), ("crud", False),
          ("compact_minus_replay", True), ("sentences_minus_replay", True), ("display_part", True),
          ("content_part", True), ("original_minus_crud", True)]
for label in ("sft", "gold"):
    print(f"\nB, {'after SFT (3 seeds)' if label == 'sft' else 'gold memory'} (dev, episode bootstrap)")
    print(f"  {'':26s} {'4B reader':24s} {'larger reader':24s}")
    for key, signed in B_ROWS:
        cells = [fmt(r[1]["sets"][label]["by_unit"]["episode"]["all"][key], signed) for r in readers.values()]
        print(f"  {key:26s} {cells[0]:24s} {cells[1]:24s}")
    shares = [sum(e["replay_same_answer"]["share"] for e in r[1]["sets"][label]["per_run"]) /
              len(r[1]["sets"][label]["per_run"]) for r in readers.values()]
    print(f"  {'replay same answer':26s} {100 * shares[0]:.1f}%{'':19s} {100 * shares[1]:.1f}%")

print("\nBy probe type and question group (dev, episode bootstrap; 4B reader -> larger reader)")
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


def value(series_set, key, unit="episode"):
    return series_set["by_unit"][unit]["all"][key]


def both_units(series_set, key):
    return (f"{fmt(value(series_set, key), True)} by episode, {fmt(value(series_set, key, 'family'), True)} "
            f"by family")


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
print(f"  B display reading: {'HOLDS' if ok else 'DOES NOT HOLD'} (display part > 0 for SFT and gold, content part"
      f" of SFT not positive)")
for s in ("sft", "gold"):
    print(f"     display part, {s}: {both_units(b['sets'][s], 'display_part')}")
print(f"     content part, sft: {both_units(sft, 'content_part')}")
cost = {s: 100 * value(b["sets"][s], "compact_minus_replay")["mean"] for s in ("sft", "gold")}
print(f"  B compact cost: {'HOLDS' if all(v < 0 for v in cost.values()) else 'DOES NOT HOLD'} (compact - replay < 0"
      f" for SFT and gold)")
for s in ("sft", "gold"):
    print(f"     compact - replay, {s}: {both_units(b['sets'][s], 'compact_minus_replay')}")

if out_path:
    out_path.write_text(json.dumps({name: {"a": r[0], "b": r[1]} for name, r in readers.items()}, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    print(f"\nwrote {out_path}")
