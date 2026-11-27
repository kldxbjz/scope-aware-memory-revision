# Final report draft (11-768, ACL format)

Draft of 2026-11-27. Every number in it comes from the result files in [results/](../results/) at commit `8c89308`.

## Files

- `main.tex`, `custom.bib`: the report. Red `[TODO: ...]` marks what the team still has to write.
- `main.pdf`: built from these sources when they were committed; rebuild it after editing.
- `acl.sty`, `acl_natbib.bst`: the standard ACL style files, unchanged.
- `figures/report_fig_types.*`, `figures/report_fig_attributes.*`: report-sized versions of
  `results/figures/fig2_difference_by_group_and_type` and `fig5_attributes`, drawn with the repository's style
  helpers from `results/test_p12/report.json` and `results/posthoc/dev_vs_test.json`. To redraw them (needs
  matplotlib), from the repository root: `python report/figures_src/make_report_figures.py . report/figures`.
- The challenge-set row of Table 4 (format and writing) is `results/posthoc/decomposition_challenge.json`, computed
  for the report ([docs/analysis.md](../docs/analysis.md#format-against-writing)).

## Build

```sh
cd report && pdflatex main && bibtex main && pdflatex main && pdflatex main
```

On Overleaf: upload the files of this folder as a project; the compiler is pdfLaTeX.

## Still open

- Authors: check names and order; add the third member.
- Team Member Contributions and the AI-tools statement.
- Section 5.6 and Appendix D: the manual error analysis (packets in
  [annotations/error_analysis/](../annotations/error_analysis/)).
- The main text (through the AI-tools paragraph) ends on page 9, the course maximum; keep it there when filling in.
- Course staff need access to this private repository before submission.
