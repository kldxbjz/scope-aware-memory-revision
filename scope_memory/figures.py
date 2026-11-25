"""Figures and tables for the report and poster, drawn from the stored analysis reports.

  python3 -m scope_memory.figures --results results --out results/figures

Reads results/test_p12/report.json (pre-specified) and results/posthoc/*.json (post-hoc, scope_memory.posthoc) and
writes every figure as PDF (vector, fonts embedded, for the report) and PNG (300 dpi, for the poster), plus tables.md
with the numbers behind every figure. Needs matplotlib; the rest of the package uses the standard library only.
Colours: CRUD and scope-aware are categorical slots 1 and 2 of the reference palette (blue, orange; checked for
colour-vision deficiency on white); differences between the arms are drawn in ink, the comparison series hollow.
"""
import argparse
import json
from pathlib import Path

ARMS = ("crud", "scope")
ARM_COLOR = {"crud": "#2a78d6", "scope": "#eb6834"}
ARM_NAME = {"crud": "CRUD", "scope": "Scope-aware"}
INK, INK2, MUTED = "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, SURFACE = "#e1e0d9", "#c3c2b7", "#ffffff"
MINUS, UP, DOWN = "\u2212", "\u2191", "\u2193"
WIDTH = 6.5  # inches, the text width of a one-column page

CONDITIONS = (("noop", "Never written (floor)"), ("zero_shot", "Zero-shot prompt"), ("six_shot", "Six-shot prompt"),
              ("sft", "SFT (3 seeds)"), ("gold", "Gold memory (ceiling)"))
QA_ROWS = (("all", "All questions"), ("all_but_boundary", "Without boundary questions"),
           ("general_update", "General update"), ("scoped_exception", "Scoped exception"),
           ("exception_revision", "Exception revision"), ("stable_preference", "Stable preference"))
TYPE_ROWS = (("type_target", "Target"), ("type_default", "Default (ordinary occasion)"),
             ("type_neighbor", "Neighbor situation"), ("type_boundary", "Boundary (window ended)"))
PART_ROWS = (("total", "After SFT: scope \u2212 CRUD"), ("format", "Format: same gap on gold memory"),
             ("write", "Writing: loss against own gold"))
COST_ROWS = (("policy_input_tokens", "Policy input, per event"), ("policy_output_tokens", "Policy output, per event"),
             ("answer_input_tokens", "Answer Agent input, per question"),
             ("memory_tokens_at_probes", "Memory at question time"))
MECHANISM_ROWS = (  # name, label, higher is better
    ("row_correct", "Event handled exactly right", True),
    ("state_correct", "Memory state right", True),
    ("decision_correct", "Decision right (store or clarify)", True),
    ("structure_matches_gold", "Operations match gold", True),
    ("false_overwrite", "General value overwritten by mistake", False),
    ("missed_update", "General update missed", False),
    ("exception_disturbed", "Untouched situation record changed", False),
    ("spurious_write", "Write on a no-change event", False),
    ("clarify_recall", "Asks when it should clarify", True),
    ("false_clarify", "Asks when it should not", False),
    ("rejected_by_executor", "Output rejected by the executor", False),
    ("rule_reader_parse_failure", "Memory the rule reader cannot parse", False))
CATEGORY_NAMES = {"general_update": "General update", "scoped_exception": "Scoped exception",
                  "exception_revision": "Exception revision", "exception_retirement": "Exception retirement",
                  "stable_preference": "Stable preference", "clarify": "Clarify"}


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def num(x, digits=1, sign=False):
    """A number with a typographic minus sign."""
    text = f"{x:+.{digits}f}" if sign else f"{x:.{digits}f}"
    return text.replace("-", MINUS)


def diff_text(mean, ci, scale=100):
    """'+2.7 [+0.9, +4.5]' from a mean and interval given as shares."""
    return f"{num(scale * mean, sign=True)} [{num(scale * ci[0], sign=True)}, {num(scale * ci[1], sign=True)}]"


# ---------------------------------------------------------------- drawing helpers

def _pyplot():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.5, "axes.titlesize": 9.5, "axes.labelsize": 8.5,
        "xtick.labelsize": 8, "ytick.labelsize": 8.5, "legend.fontsize": 8, "text.color": INK,
        "axes.edgecolor": AXIS, "axes.linewidth": 0.8, "axes.labelcolor": INK2,
        "xtick.color": AXIS, "ytick.color": AXIS, "xtick.labelcolor": INK2, "ytick.labelcolor": INK,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
        "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none", "axes.unicode_minus": True})
    return plt


def _dot(ax, y, mean, ci, color, filled=True):
    """A 95% interval (thin line) with its estimate (a dot with a surface ring, or a hollow ring)."""
    ax.plot([ci[0], ci[1]], [y, y], color=color, lw=1.4, solid_capstyle="round", zorder=2)
    ax.plot([mean], [y], linestyle="none", marker="o", ms=6.5, zorder=3, mfc=color if filled else SURFACE,
            mec=SURFACE if filled else color, mew=1.5 if filled else 1.6)


def _key(color, filled=True):
    from matplotlib.lines import Line2D
    return Line2D([0], [0], color=color, lw=1.4, marker="o", ms=6.5, mfc=color if filled else SURFACE,
                  mec=SURFACE if filled else color, mew=1.5 if filled else 1.6)


def _rows(ax, labels):
    ys = list(range(len(labels) - 1, -1, -1))
    ax.set_yticks(ys)
    ax.set_yticklabels(labels)
    ax.tick_params(axis="y", length=0, pad=6)
    ax.set_ylim(-0.6, len(labels) - 0.4)
    ax.grid(axis="x", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    return ys


def _right(ax, y, text, header=False):
    """Text in a column right of the plot (x in axes coordinates, y in data coordinates)."""
    ax.text(1.02, y, text, transform=ax.get_yaxis_transform(), va="center", ha="left", fontsize=8,
            color=INK2 if header else INK, fontweight="bold" if header else "normal")


def _zero(ax):
    ax.axvline(0, color=INK2, lw=0.8, zorder=1)


def _title(ax, title, legend=True):
    """A left-aligned title; with a legend row under it (placed at the top edge of the axes), raised above it."""
    ax.set_title(title, loc="left", fontsize=9.5, color=INK, fontweight="bold", pad=26 if legend else 10)


def _save(fig, out, name):
    for ext, kw in (("pdf", {}), ("png", {"dpi": 300})):
        fig.savefig(out / f"{name}.{ext}", bbox_inches="tight", pad_inches=0.05,
                    metadata={"CreationDate": None} if ext == "pdf" else None, **kw)
    return [f"{name}.pdf", f"{name}.png"]


# ---------------------------------------------------------------- figures

def fig_main(plt, report, out):
    fig, ax = plt.subplots(figsize=(WIDTH, 2.7))
    ys = _rows(ax, [label for _, label in CONDITIONS])
    for (cond, _), y in zip(CONDITIONS, ys):
        for arm, dy in (("crud", 0.14), ("scope", -0.14)):
            a = report["accuracy"][cond][arm]["all"]
            _dot(ax, y + dy, 100 * a["accuracy"], [100 * c for c in a["ci95"]], ARM_COLOR[arm])
        e = report["scope_minus_crud"][cond]["all"]
        _right(ax, y, diff_text(e["difference"], e["ci95"]))
    _right(ax, len(CONDITIONS) - 0.35, "Scope \u2212 CRUD", header=True)
    ax.set_xlim(40, 100)
    ax.set_xlabel("Answer Agent QA accuracy (%), 95% episode-bootstrap intervals")
    ax.legend([_key(ARM_COLOR[a]) for a in ARMS], [ARM_NAME[a] for a in ARMS], loc="lower left",
              bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, handletextpad=0.4, columnspacing=1.2, borderaxespad=0.2)
    _title(ax, "Test split: QA accuracy by condition (2,027 questions per arm)")
    return _save(fig, out, "fig1_main_results")


def fig_breakdown(plt, report, out):
    fig, axes = plt.subplots(2, 1, figsize=(WIDTH, 4.1), sharex=True,
                             gridspec_kw={"height_ratios": [len(QA_ROWS), len(TYPE_ROWS)], "hspace": 0.12})
    h1, gold = report["scope_minus_crud"]["sft"], report["scope_minus_crud"]["gold"]
    for ax, rows in zip(axes, (QA_ROWS, TYPE_ROWS)):
        ys = _rows(ax, [f"{label} ({h1[g]['probes']})" for g, label in rows])
        _zero(ax)
        for (g, _), y in zip(rows, ys):
            _dot(ax, y + 0.14, 100 * h1[g]["difference"], [100 * c for c in h1[g]["ci95"]], INK)
            _dot(ax, y - 0.14, 100 * gold[g]["difference"], [100 * c for c in gold[g]["ci95"]], INK2, filled=False)
            _right(ax, y, diff_text(h1[g]["difference"], h1[g]["ci95"]))
    _right(axes[0], len(QA_ROWS) - 0.35, "After SFT", header=True)
    axes[1].set_xlim(-10, 40)
    axes[1].set_xlabel("Scope-aware minus CRUD (points), 95% episode-bootstrap intervals")
    axes[0].legend([_key(INK), _key(INK2, filled=False)], ["After SFT (3 seeds)", "On gold memory (format only)"],
                   loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, handletextpad=0.4,
                   columnspacing=1.2, borderaxespad=0.2)
    _title(axes[0], "Test split: scope-aware minus CRUD, by question group and question type")
    return _save(fig, out, "fig2_difference_by_group_and_type")


def fig_decomposition(plt, dvt, out):
    fig, ax = plt.subplots(figsize=(WIDTH, 2.2))
    ys = _rows(ax, [label for _, label in PART_ROWS])
    _zero(ax)
    for (part, _), y in zip(PART_ROWS, ys):
        texts = []
        for split, dy, color, filled in (("test", 0.14, INK, True), ("dev", -0.14, INK2, False)):
            e = dvt["splits"][split]["by_unit"]["episode"]["all"][part]
            _dot(ax, y + dy, 100 * e["mean"], [100 * c for c in e["ci95"]], color, filled)
            texts.append(f"{split} {diff_text(e['mean'], e['ci95'])}")
        _right(ax, y + 0.14, texts[0])
        _right(ax, y - 0.14, texts[1])
    ax.set_xlim(-7, 7)
    ax.set_xlabel("Points; total = format + writing; 95% episode-bootstrap intervals")
    ax.legend([_key(INK), _key(INK2, filled=False)], ["Test (28 attributes)", "Dev (28 other attributes)"],
              loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, handletextpad=0.4,
              columnspacing=1.2, borderaxespad=0.2)
    _title(ax, "Where the scope \u2212 CRUD difference comes from: reading the format vs. writing it")
    return _save(fig, out, "fig3_format_vs_writing")


def fig_cost(plt, cost, out):
    arms = cost["conditions"]["sft"]["arms"]
    fig, ax = plt.subplots(figsize=(WIDTH, 2.3))
    ys = _rows(ax, [label for _, label in COST_ROWS])
    ax.grid(False)
    ax.grid(axis="x", color=GRID, lw=0.6)
    height, gap = 0.3, 0.04
    for (m, _), y in zip(COST_ROWS, ys):
        for arm, dy in (("crud", (height + gap) / 2), ("scope", -(height + gap) / 2)):
            value = arms[arm][m]["mean"]
            ax.barh(y + dy, value, height=height, color=ARM_COLOR[arm], linewidth=0, zorder=2)
            ax.text(value + 12, y + dy, f"{value:,.0f}", va="center", ha="left", fontsize=7.5, color=INK2)
        _right(ax, y, f"\u00d7{arms['scope'][m]['mean'] / arms['crud'][m]['mean']:.2f}")
    _right(ax, len(COST_ROWS) - 0.35, "Scope / CRUD", header=True)
    ax.set_xlim(0, 1000)
    ax.spines["left"].set_visible(True)
    ax.spines["left"].set_color(AXIS)
    ax.set_xlabel("Tokens per call (Qwen3 tokenizer), mean over the three SFT seeds")
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=ARM_COLOR[a]) for a in ARMS], [ARM_NAME[a] for a in ARMS],
              loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2, frameon=False, handletextpad=0.4,
              columnspacing=1.2, borderaxespad=0.2)
    _title(ax, "Test split: cost per call after SFT")
    return _save(fig, out, "fig4_cost")


def _swarm(xs, width=1.0, step=0.1, lanes=3):
    """Vertical offsets for a one-row beeswarm: each dot, in order of x, takes the lane nearest the center (0, +step,
    -step, +2 step, ...) where no dot placed before lies within `width` on the x axis (the last lane if none is
    free)."""
    candidates = [0.0] + [sign * k * step for k in range(1, lanes + 1) for sign in (1, -1)]
    placed, offsets = [], [0.0] * len(xs)
    for i in sorted(range(len(xs)), key=lambda i: xs[i]):
        for offset in candidates:
            if all(abs(xs[i] - x) >= width or abs(offset - o) > 1e-9 for x, o in placed):
                break
        offsets[i] = offset
        placed.append((xs[i], offset))
    return offsets


def fig_attributes(plt, dvt, out):
    fig, ax = plt.subplots(figsize=(WIDTH, 1.9))
    splits = (("test", INK, True), ("dev", INK2, False))
    ys = _rows(ax, ["Test", "Dev"])
    _zero(ax)
    for (split, color, filled), y in zip(splits, ys):
        families = dvt["splits"][split]["per_family"]
        xs = [100 * f["total"] for f in families]
        for x, dy in zip(xs, _swarm(xs)):
            ax.plot([x], [y + dy], linestyle="none", marker="o", ms=5.5, mfc=color if filled else SURFACE,
                    mec=SURFACE if filled else color, mew=1.2 if filled else 1.3, zorder=3)
        overall = 100 * dvt["splits"][split]["by_unit"]["episode"]["all"]["total"]["mean"]
        ax.plot([overall, overall], [y - 0.42, y + 0.42], color=color, lw=2.2, solid_capstyle="butt", zorder=2)
        spread = dvt["splits"][split]["family_spread"]
        _right(ax, y, f"overall {num(overall, sign=True)}; scope ahead in {spread['scope_ahead']} of "
                      f"{len(families)}")
    ax.set_xlim(-36, 16)
    ax.set_xlabel("Scope-aware minus CRUD after SFT (points); one dot per preference attribute, bar = overall")
    _title(ax, "The difference varies a lot between attributes, and dev and test share none", legend=False)
    return _save(fig, out, "fig5_attributes")


HISTORY_ROWS = (("history", "Raw history, no memory", INK), ("sft_crud", "SFT CRUD memory", ARM_COLOR["crud"]),
                ("sft_scope", "SFT scope-aware memory", ARM_COLOR["scope"]),
                ("gold_crud", "Gold CRUD memory", ARM_COLOR["crud"]),
                ("gold_scope", "Gold scope-aware memory", ARM_COLOR["scope"]))
COST_OF = {"history": "history", "sft_crud": "crud", "sft_scope": "scope"}
DISPLAY_ROWS = (("original", "Scope memory, original display", ARM_COLOR["scope"]),
                ("replay", "same, answered again", ARM_COLOR["scope"]),
                ("compact", "same, compact display", ARM_COLOR["scope"]),
                ("sentences", "same, as CRUD sentences", ARM_COLOR["scope"]),
                ("crud", "CRUD memory (its own display)", ARM_COLOR["crud"]))


def _low(entries):
    """Left edge of an accuracy axis: 5 points below the lowest interval, rounded down to a multiple of 5."""
    return 5 * int((100 * min(e["ci95"][0] for e in entries) - 5) // 5)


def _split_keys(ax):
    ax.legend([_key(INK), _key(INK, filled=False)], ["Test", "Dev"], loc="lower left", bbox_to_anchor=(0, 1.0),
              ncol=2, frameon=False, handletextpad=0.4, columnspacing=1.2, borderaxespad=0.2)


def fig_history(plt, a_test, a_dev, out):
    fig, ax = plt.subplots(figsize=(WIDTH, 2.5))
    ys = _rows(ax, [label for _, label, _ in HISTORY_ROWS])
    for (name, _, color), y in zip(HISTORY_ROWS, ys):
        for a, dy, filled in ((a_test, 0.14, True), (a_dev, -0.14, False)):
            e = a["by_unit"]["episode"]["all"][name]
            _dot(ax, y + dy, 100 * e["mean"], [100 * c for c in e["ci95"]], color, filled)
        text = f"{num(100 * a_test['by_unit']['episode']['all'][name]['mean'])}"
        cost = a_test["cost_per_run"].get(COST_OF.get(name, ""), {})
        if cost:
            text += f"; {cost['total_tokens'] / 1e6:.2f} M tokens"
        _right(ax, y, text)
    _right(ax, len(HISTORY_ROWS) - 0.35, "Test; tokens per run", header=True)
    ax.set_xlim(_low([a["by_unit"]["episode"]["all"][name] for a in (a_test, a_dev)
                      for name, _, _ in HISTORY_ROWS]), 100)
    ax.set_xlabel("Answer Agent QA accuracy (%), 95% episode-bootstrap intervals")
    _split_keys(ax)
    _title(ax, "Answering from the raw conversations instead of memory (post-hoc)")
    return _save(fig, out, "fig6_raw_history")


def fig_display(plt, b_test, b_dev, out):
    fig, axes = plt.subplots(2, 1, figsize=(WIDTH, 4.0), sharex=True, gridspec_kw={"hspace": 0.3})
    for ax, label in zip(axes, ("sft", "gold")):
        ys = _rows(ax, [name for _, name, _ in DISPLAY_ROWS])
        test, dev = b_test["sets"][label], b_dev["sets"][label]
        for (name, _, color), y in zip(DISPLAY_ROWS, ys):
            for s, dy, filled in ((test, 0.14, True), (dev, -0.14, False)):
                e = s["by_unit"]["episode"]["all"][name]
                _dot(ax, y + dy, 100 * e["mean"], [100 * c for c in e["ci95"]], color, filled)
            text = num(100 * test["by_unit"]["episode"]["all"][name]["mean"])
            shown = "replay" if name == "original" else name
            if shown in test["tokens"]:
                text += f"; {test['tokens'][shown]['memory_tokens']['mean']:,.0f} tokens"
            _right(ax, y, text)
        _right(ax, len(DISPLAY_ROWS) - 0.35, "Test; memory block", header=True)
        ax.set_title("After SFT (3 seeds)" if label == "sft" else "Gold memory", loc="left", fontsize=8.5,
                     color=INK2, pad=4)
    axes[1].set_xlim(_low([b["sets"][s]["by_unit"]["episode"]["all"][name] for b in (b_test, b_dev)
                           for s in ("sft", "gold") for name, _, _ in DISPLAY_ROWS]), 100)
    axes[1].set_xlabel("Answer Agent QA accuracy (%), 95% episode-bootstrap intervals")
    axes[0].legend([_key(INK), _key(INK, filled=False)], ["Test", "Dev"], loc="lower left",
                   bbox_to_anchor=(0, 1.12), ncol=2, frameon=False, handletextpad=0.4, columnspacing=1.2,
                   borderaxespad=0.2)
    axes[0].text(0, 1.42, "The same memory shown in other ways (post-hoc)", transform=axes[0].transAxes,
                 fontsize=9.5, fontweight="bold", color=INK, ha="left", va="bottom")
    return _save(fig, out, "fig7_memory_display")


# ---------------------------------------------------------------- tables

def _table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    return lines + ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]


def tables(report, dvt, cost, mech_test, mech_dev, comp):
    pct = lambda x: num(100 * x)  # noqa: E731
    lines = ["# Tables behind the figures", "",
             "Generated by `python3 -m scope_memory.figures`. Test numbers in Tables 1 and 2 are the pre-specified "
             "results (results/test_p12/report.json); Tables 3 and later are post-hoc (results/posthoc/, "
             "docs/analysis.md). Intervals are 95% episode-bootstrap intervals unless a column says otherwise.", "",
             "## Table 1. Answer Agent QA accuracy on test (Figure 1)", ""]
    rows = []
    for cond, label in CONDITIONS:
        a = report["accuracy"][cond]
        e, nb = report["scope_minus_crud"][cond]["all"], report["scope_minus_crud"][cond]["all_but_boundary"]
        rows.append([label] + [f"{pct(a[arm]['all']['accuracy'])} [{pct(a[arm]['all']['ci95'][0])}, "
                               f"{pct(a[arm]['all']['ci95'][1])}]" for arm in ARMS]
                    + [diff_text(e["difference"], e["ci95"]), diff_text(nb["difference"], nb["ci95"])])
    lines += _table(["Condition", "CRUD", "Scope-aware", "Scope \u2212 CRUD", "Without boundary questions"], rows)
    lines += ["", "## Table 2. Scope-aware minus CRUD by group and question type, test (Figure 2)", ""]
    rows = []
    for g, label in QA_ROWS + TYPE_ROWS:
        h, gold = report["scope_minus_crud"]["sft"][g], report["scope_minus_crud"]["gold"][g]
        rows.append([label, h["probes"], pct(h["b"]), pct(h["a"]), diff_text(h["difference"], h["ci95"]),
                     diff_text(gold["difference"], gold["ci95"])])
    lines += _table(["Questions", "n", "SFT CRUD", "SFT scope", "SFT scope \u2212 CRUD", "Gold scope \u2212 CRUD"],
                    rows)
    lines += ["", "## Table 3. Format against writing, dev and test (Figure 3; post-hoc)", "",
              "total = format + writing. Family intervals resample the 28 preference attributes of the split "
              "instead of episodes.", ""]
    rows = []
    for part, label in PART_ROWS:
        for split in ("test", "dev"):
            e = dvt["splits"][split]["by_unit"]["episode"]["all"][part]
            f = dvt["splits"][split]["by_unit"]["family"]["all"][part]
            rows.append([label, split, diff_text(e["mean"], e["ci95"]), f"[{num(100 * f['ci95'][0], sign=True)}, "
                                                                         f"{num(100 * f['ci95'][1], sign=True)}]"])
        d = dvt["test_minus_dev"]["episode"]["all"][part]
        rows.append([label, "test \u2212 dev", diff_text(d["mean"], d["ci95"]), ""])
    lines += _table(["Part", "Split", "Points [episode interval]", "Family interval"], rows)
    lines += ["", "Each split with the other split's mix of question types or groups (episode intervals):", ""]
    rows = []
    for key, label in (("dev_with_test_mix", "Dev with test's mix"), ("test_with_dev_mix", "Test with dev's mix")):
        for mix in ("probe_type", "qa_group"):
            m = dvt["standardised"][key][mix]
            rows.append([label, mix.replace("_", " ")] + [diff_text(m[p]["mean"], m[p]["ci95"]) for p in
                                                          ("total", "format", "write")])
    lines += _table(["Split", "Mix of", "Total", "Format", "Writing"], rows)
    lines += ["", "## Table 4. Teacher-forced write metrics, 3 seeds pooled (post-hoc; rule-reader diagnostics)", "",
              "Each event's output is applied to the gold memory before it. Rates in %; the arrow says which "
              "direction is better. Scope \u2212 CRUD with a 95% episode-bootstrap interval.", ""]
    rows = []
    for name, label, up in MECHANISM_ROWS:
        row = [f"{label} {UP if up else DOWN}"]
        for m in (mech_test, mech_dev):
            v = m["metrics"][name]
            row += [pct(v["crud"]["rate"]), pct(v["scope"]["rate"]),
                    diff_text(v["scope_minus_crud"]["difference"], v["scope_minus_crud"]["ci95"])]
        rows.append(row)
    lines += _table(["Metric", "Test CRUD", "Test scope", "Test scope \u2212 CRUD", "Dev CRUD", "Dev scope",
                     "Dev scope \u2212 CRUD"], rows)
    lines += ["", "Events handled exactly right, by event category:", ""]
    rows = []
    for category, label in CATEGORY_NAMES.items():
        row = [label]
        for m in (mech_test, mech_dev):
            v = m["by_category"]["row_correct"][category]
            row += [f"{pct(v['crud']['rate'])} / {pct(v['scope']['rate'])}",
                    diff_text(v["scope_minus_crud"]["difference"], v["scope_minus_crud"]["ci95"])]
        rows.append(row)
    lines += _table(["Category", "Test CRUD / scope", "Test scope \u2212 CRUD", "Dev CRUD / scope",
                     "Dev scope \u2212 CRUD"], rows)
    lines += ["", "## Table 5. Cost per call on test (Figure 4; post-hoc summary of cost.json)", ""]
    rows = []
    for cond, label in CONDITIONS:
        if cond not in cost["conditions"]:
            continue
        arms = cost["conditions"][cond]["arms"]
        for m, mlabel in COST_ROWS:
            if m in arms["crud"] and m in arms["scope"]:
                rows.append([label, mlabel, f"{arms['crud'][m]['mean']:,.1f}", f"{arms['scope'][m]['mean']:,.1f}"])
    lines += _table(["Condition", "Tokens per call", "CRUD", "Scope-aware"], rows)
    lines += ["", "## Table 6. What the splits contain (post-hoc)", ""]
    files = comp["files"]
    names = list(files)
    rows = [["Episodes"] + [files[n]["episodes"] for n in names],
            ["Preference attributes (families)"] + [files[n]["families"] for n in names],
            ["Events per episode"] + [files[n]["events_per_episode"] for n in names],
            ["Questions"] + [files[n]["probes"] for n in names]]
    for key, label in (("event_categories", "Events"), ("probe_types", "Questions"), ("qa_groups", "Questions")):
        for k in files[names[0]][key]:
            rows.append([f"{label}: {k.replace('_', ' ')} (%)"] + [pct(files[n][key][k]["share"]) for n in names])
    for k in files[names[0]]["situation_records_at_probe"]:
        rows.append([f"Situation records of the attribute at the question: {k} (%)"]
                    + [pct(files[n]["situation_records_at_probe"][k]["share"]) for n in names])
    lines += _table(["", *names], rows)
    lines += ["", "Families shared between files: " + ", ".join(f"{k} {v}" for k, v in comp["shared_families"].items())]
    lines += ["", "## Table 7. Per attribute, after SFT (Figure 5; post-hoc)", ""]
    rows = []
    for split in ("test", "dev"):
        s = dvt["splits"][split]["family_spread"]
        rows.append([split, s["scope_ahead"], s["crud_ahead"], s["tied"], num(100 * s["min"], sign=True),
                     num(100 * s["max"], sign=True), num(100 * s["sd"])])
    lines += _table(["Split", "Scope ahead", "CRUD ahead", "Tied", "Lowest", "Highest", "SD across attributes"], rows)
    return "\n".join(lines) + "\n"


def readtime_tables(a_test, a_dev, b_test, b_dev):
    """Tables 8 and 9: the read-time experiments (scope_memory.readtime; post-hoc)."""
    pct = lambda x: num(100 * x)  # noqa: E731

    def acc(e):
        return f"{pct(e['mean'])} [{pct(e['ci95'][0])}, {pct(e['ci95'][1])}]"

    lines = ["", "## Table 8. A: answering from the raw history (Figure 6; post-hoc)", "",
             "The history condition reads the preferences at the start and every conversation up to the question, "
             "with no memory. Differences are history minus the memory, paired per question; SFT pooled over the "
             "three seeds.", ""]
    rows = []
    for name, label, _ in HISTORY_ROWS:
        rows.append([label] + [acc(a["by_unit"]["episode"]["all"][name]) for a in (a_test, a_dev)])
    for name, label, _ in HISTORY_ROWS[1:]:
        rows.append([f"History \u2212 {label}"]
                    + [diff_text(a["by_unit"]["episode"]["all"][f"history_minus_{name}"]["mean"],
                                 a["by_unit"]["episode"]["all"][f"history_minus_{name}"]["ci95"])
                       for a in (a_test, a_dev)])
    if "noop_scope" in a_test["by_unit"]["episode"]["all"]:
        rows.append(["Never-written memory, scope / CRUD (test)",
                     f"{pct(a_test['by_unit']['episode']['all']['noop_scope']['mean'])} / "
                     f"{pct(a_test['by_unit']['episode']['all']['noop_crud']['mean'])}", ""])
    lines += _table(["", "Test", "Dev"], rows)
    lines += ["", "By question type, test (accuracy; history minus SFT memory):", ""]
    rows = []
    for g, label in TYPE_ROWS + (("all_but_boundary", "Without boundary questions"),):
        e = a_test["by_unit"]["episode"].get(g)
        if not e:
            continue
        rows.append([label, e["probes"], pct(e["history"]["mean"]), pct(e["sft_crud"]["mean"]),
                     pct(e["sft_scope"]["mean"]),
                     diff_text(e["history_minus_sft_crud"]["mean"], e["history_minus_sft_crud"]["ci95"]),
                     diff_text(e["history_minus_sft_scope"]["mean"], e["history_minus_sft_scope"]["ci95"])])
    lines += _table(["Questions", "n", "History", "SFT CRUD", "SFT scope", "History \u2212 CRUD",
                     "History \u2212 scope"], rows)
    lines += ["", "Questions only one side gets right, per SFT seed (mean over the three seeds), and tokens of one "
              "run:", ""]
    rows = []
    for a, split in ((a_test, "test"), (a_dev, "dev")):
        for arm in ("crud", "scope"):
            seeds = [f for f in a["flips_per_seed"] if f["arm"] == arm]
            mean = lambda key: sum(f[key] for f in seeds) / len(seeds)  # noqa: E731
            cost = a["cost_per_run"].get(arm)
            rows.append([split, ARM_NAME[arm], f"{mean('history_only'):.1f}", f"{mean('memory_only'):.1f}",
                         f"{cost['total_tokens'] / 1e6:.2f} M" if cost else "",
                         f"{a['cost_per_run']['history']['total_tokens'] / 1e6:.2f} M"])
    lines += _table(["Split", "Memory", "Only the history right", "Only the memory right", "Tokens, memory run",
                     "Tokens, history run"], rows)
    lines += ["", "## Table 9. B: the same scope memory shown in other ways (Figure 7; post-hoc)", "",
              "original = the stored answers of the main runs; replay = the same prompt answered again in the new "
              "job; compact and CRUD sentences show the same records. display + content = scope \u2212 CRUD, with "
              "display = original \u2212 sentences and content = sentences \u2212 CRUD.", ""]
    rows = []
    for label, set_name in (("sft", "After SFT (3 seeds)"), ("gold", "Gold memory")):
        for b, split in ((b_test, "test"), (b_dev, "dev")):
            s = b["sets"][label]
            e = s["by_unit"]["episode"]["all"]
            row = [set_name, split] + [pct(e[name]["mean"]) for name, _, _ in DISPLAY_ROWS]
            row += [diff_text(e[k]["mean"], e[k]["ci95"]) for k in ("compact_minus_replay", "sentences_minus_replay",
                                                                     "display_part", "content_part")]
            replay = sum(r["replay_same_answer"]["same"] for r in s["per_run"])
            row.append(f"{100 * replay / sum(r['replay_same_answer']['probes'] for r in s['per_run']):.1f}%")
            rows.append(row)
    lines += _table(["Memory", "Split", "Original", "Replay", "Compact", "Sentences", "CRUD", "Compact \u2212 replay",
                     "Sentences \u2212 replay", "Display part", "Content part", "Replay same answer"], rows)
    lines += ["", "Answers lost and gained against the original, summed over runs, and tokens per question (test):", ""]
    rows = []
    for label, set_name in (("sft", "After SFT (3 seeds)"), ("gold", "Gold memory")):
        s = b_test["sets"][label]
        for c in ("replay", "compact", "sentences"):
            lost = sum(r[c]["lost"] for r in s["per_run"])
            gained = sum(r[c]["gained"] for r in s["per_run"])
            t = s["tokens"][c]
            rows.append([set_name, c, lost, gained, f"{t['memory_tokens']['mean']:,.1f}",
                         f"{t['input_tokens']['mean']:,.1f}"])
    lines += _table(["Memory", "Display", "Lost", "Gained", "Memory block tokens", "Prompt tokens"], rows)
    return lines


def main(argv=None):
    parser = argparse.ArgumentParser(description="Figures and tables for the report and poster.")
    parser.add_argument("--results", default="results", help="the repository's results folder")
    parser.add_argument("--out", default="results/figures")
    args = parser.parse_args(argv)
    results, out = Path(args.results), Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    report = _load(results / "test_p12" / "report.json")
    post = results / "posthoc"
    dvt, cost = _load(post / "dev_vs_test.json"), _load(post / "cost_test.json")
    plt = _pyplot()
    written = []
    written += fig_main(plt, report, out)
    written += fig_breakdown(plt, report, out)
    written += fig_decomposition(plt, dvt, out)
    written += fig_cost(plt, cost, out)
    written += fig_attributes(plt, dvt, out)
    names = [f"readtime_{x}_{split}.json" for x in ("a", "b") for split in ("test", "dev")]
    readtime = [_load(post / n) for n in names] if all((post / n).exists() for n in names) else None
    if readtime:  # the read-time experiments, once their reports exist
        written += fig_history(plt, readtime[0], readtime[1], out)
        written += fig_display(plt, readtime[2], readtime[3], out)
    plt.close("all")
    text = tables(report, dvt, cost, _load(post / "mechanism_test.json"), _load(post / "mechanism_dev.json"),
                  _load(post / "composition.json"))
    if readtime:
        text += "\n".join(readtime_tables(*readtime)) + "\n"
    (out / "tables.md").write_text(text, encoding="utf-8", newline="\n")
    written.append("tables.md")
    print("\n".join(str(out / name) for name in written))


if __name__ == "__main__":
    main()
