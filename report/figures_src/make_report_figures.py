"""Report-sized versions of two repository figures, drawn with the repository's own style helpers.

  python report/figures_src/make_report_figures.py . report/figures     (from the repository root; needs matplotlib)

The first argument is the repository root; the numbers come from its results/test_p12/report.json (pre-specified)
and results/posthoc/dev_vs_test.json (post-hoc).
"""
import json
import sys
from pathlib import Path

repo, out = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(repo))
from scope_memory import figures as F  # noqa: E402

plt = F._pyplot()
plt.rcParams.update({"font.size": 7.5, "xtick.labelsize": 7, "ytick.labelsize": 7.5, "legend.fontsize": 7,
                     "axes.labelsize": 7.5})
out.mkdir(parents=True, exist_ok=True)
report = json.loads((repo / "results/test_p12/report.json").read_text(encoding="utf-8"))
dvt = json.loads((repo / "results/posthoc/dev_vs_test.json").read_text(encoding="utf-8"))

# Column-width version of fig2: scope - CRUD by question type and QA group, after SFT and on gold memory.
rows_type = (("type_default", "Default"), ("type_boundary", "Boundary"), ("type_target", "Target"),
             ("type_neighbor", "Neighbor"))
rows_group = (("scoped_exception", "Scoped exception"), ("exception_revision", "Exception revision"),
              ("stable_preference", "Stable preference"), ("general_update", "General update"),
              ("all", "All questions"))
h1, gold = report["scope_minus_crud"]["sft"], report["scope_minus_crud"]["gold"]
fig, axes = plt.subplots(2, 1, figsize=(3.05, 2.55), sharex=True,
                         gridspec_kw={"height_ratios": [len(rows_type), len(rows_group)], "hspace": 0.16})
fig.subplots_adjust(left=0.375, right=0.975, top=0.9, bottom=0.16)
for ax, rows in zip(axes, (rows_type, rows_group)):
    ys = F._rows(ax, [f"{label} ({h1[g]['probes']})" for g, label in rows])
    F._zero(ax)
    for (g, _), y in zip(rows, ys):
        for dy, src, color, filled in ((0.15, h1, F.INK, True), (-0.15, gold, F.INK2, False)):
            mean, ci = 100 * src[g]["difference"], [100 * c for c in src[g]["ci95"]]
            ax.plot(ci, [y + dy] * 2, color=color, lw=1.0, solid_capstyle="butt", zorder=2)
            ax.plot([mean], [y + dy], linestyle="none", marker="o", ms=4.0, zorder=3,
                    mfc=color if filled else F.SURFACE, mec=color, mew=0.9)
    ax.tick_params(axis="y", pad=3)
axes[1].set_xlim(-10, 40)
axes[1].set_xlabel("Scope-aware minus CRUD (points)")
from matplotlib.lines import Line2D  # noqa: E402
keys = [Line2D([0], [0], color=F.INK, lw=1.0, marker="o", ms=4.0, mfc=F.INK, mec=F.INK, mew=0.9),
        Line2D([0], [0], color=F.INK2, lw=1.0, marker="o", ms=4.0, mfc=F.SURFACE, mec=F.INK2, mew=0.9)]
fig.legend(keys, ["After SFT (3 seeds)", "Gold memory (format only)"], loc="upper center",
           bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, handletextpad=0.3, columnspacing=0.9,
           borderaxespad=0.1)
F._save(fig, out, "report_fig_types")

# Full-width version of fig5: scope - CRUD per attribute on test and dev.
fig, ax = plt.subplots(figsize=(6.3, 1.35))
ys = F._rows(ax, ["Test", "Dev"])
F._zero(ax)
for (split, color, filled), y in zip((("test", F.INK, True), ("dev", F.INK2, False)), ys):
    families = dvt["splits"][split]["per_family"]
    xs = [100 * f["total"] for f in families]
    for x, dy in zip(xs, F._swarm(xs, width=0.9, step=0.13)):
        ax.plot([x], [y + dy], linestyle="none", marker="o", ms=4.0, mfc=color if filled else F.SURFACE,
                mec=color, mew=0.9, zorder=3)
    overall = 100 * dvt["splits"][split]["by_unit"]["episode"]["all"]["total"]["mean"]
    ax.plot([overall, overall], [y - 0.42, y + 0.42], color=color, lw=1.8, solid_capstyle="butt", zorder=2)
    spread = dvt["splits"][split]["family_spread"]
    ax.text(1.01, y, f"overall {F.num(overall, sign=True)}; scope-aware ahead\non {spread['scope_ahead']} of "
            f"{len(families)} attributes", transform=ax.get_yaxis_transform(), va="center", ha="left",
            fontsize=7, color=F.INK)
ax.set_xlim(-36, 16)
ax.set_xlabel("Scope-aware minus CRUD after SFT (points); one dot per attribute, bar = overall")
F._save(fig, out, "report_fig_attributes")
print("done")
