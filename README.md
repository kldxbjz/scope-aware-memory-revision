# Learning Scope-Aware Memory Revision for Evolving User Preferences

How should an AI agent revise stored preferences when a new statement is a contextual exception rather than a global preference change? This three-person final project compares an SFT-trained generic CRUD memory manager (add / update / delete / no-op over free-text memories) with an SFT-trained manager that also represents preference scope and relationships between memories. RL is a stretch goal and has not started. The experiment design is in [docs/sft-plan.md](docs/sft-plan.md).

> **Status (2026-11-24):** the test split has been evaluated once, with the settings frozen on 2026-11-17 (git tag `freeze-p12`) and after a label audit of the synthetic data found no label error (2026-11-23, one annotator, 58 of 60 gold categories confirmed; a second annotator, after the test run, agreed with her on 58 of 60, kappa 0.96, and both disagreements were decided for gold). On test, SFT beats the zero-shot and six-shot prompts in both arms by 21–30 points of Answer Agent QA (H2). After SFT the scope arm leads CRUD: 86.1 vs 83.3, +2.7 [+0.9, +4.5]; without boundary probes +1.7 [−0.2, +3.4] (H1). The lead is as large as the two formats' gap on gold memory (+2.7) and sits in default and boundary probes, so it reflects how well the Answer Agent reads the scope format; both SFT policies lose about the same against their own gold memory. On dev the scope arm had trailed (−2.5 [−5.2, +0.3]) and on the hand-written challenge set ([training/challenge_v1/](training/challenge_v1/README.md#results-2026-11-17)) the arms tied (+0.4 [−2.9, +4.0]), so the sign of H1 depends on the episode set. Details: [docs/evaluation.md](docs/evaluation.md#test-results-2026-11-24). Post-hoc (2026-11-24): on test the lead is all format (writing +0.0 [−1.5, +1.3]) and holds when the 28 preference attributes are resampled; dev and test share no attribute, and the difference varies strongly between attributes ([docs/analysis.md](docs/analysis.md#post-hoc-analyses-2026-11-24)). Figures for the report are in `results/figures/`. Next: the manual error analysis on the packets in `annotations/error_analysis/`.

**Follow-up recommendations (2026-11-24):** the 60-item two-annotator audit and user-reported C adjudication are complete; the original agreement remains 96.67% (kappa 0.96). The current priorities are A (raw history), B (fixed-memory rendering), then external reading diagnostics. The A/B implementation and run plan are already in the repository; check smoke/freeze/job status before running or collecting the formal results. The reserve 60 category labels and manual dialogue rewriting are not prerequisites. See [后续实验建议](docs/后续实验建议.md), [中期 update](docs/中期update.md), and [adjudication provenance](annotations/label_audit/adjudication_C_record.json).

## Repository layout

```text
scope_memory/   stdlib-only Python code; run modules with python3 -m scope_memory.<name> (figures also needs matplotlib)
tests/          unit tests for scope_memory
fixtures/       handwritten toy timeline and a worked protocol v1 episode
annotations/    blind annotation pilot; label audit of the synthetic data; error-analysis packets of the test run
results/        small saved outputs of the scope_memory scripts; test results, post-hoc analyses, report figures
docs/           experiment plan and one write-up per milestone
training/       synthetic corpora (v0.1, v1.1), challenge set v1; SFT and baseline scripts for Babel in training/sft/
```

## Milestones

| Milestone | Write-up | Code | Saved output |
|---|---|---|---|
| Chronological replay smoke test | [below](#replay-smoke-test) | `scope_memory/replay.py` | stdout only |
| HorizonBench schema audit (3 rows) | [docs/horizon-audit.md](docs/horizon-audit.md) | `scope_memory/audit_horizon.py` | `results/audit_horizon_result.json` |
| Six-case evidence spot-check, fictional paired pilot | [docs/evidence-spotcheck.md](docs/evidence-spotcheck.md) | `scope_memory/paired_pilot.py` | in the write-up |
| Read vs write diagnostic | [docs/read-write-diagnostic.md](docs/read-write-diagnostic.md) | `scope_memory/read_write_diagnostic.py` | `results/read_write_results.json` |
| Internal blind annotation pilot | [docs/blind-pilot.md](docs/blind-pilot.md) | `scope_memory/score_blind_pilot.py` | `results/blind_score.json` |
| Synthetic SFT corpus v0.1 and CPU preflight | [docs/training-intake.md](docs/training-intake.md) | [training/](training/README.md) | in the write-up |
| Memory revision protocol v1 (outline v2.7): executors, gold projection, data-generation prompt; 1.2 writes the user's own words | [docs/protocol.md](docs/protocol.md) | `scope_memory/protocol.py` | none |
| Evaluator: teacher-forced and rollout; Answer Agent prompt versions; cost; final test procedure | [docs/evaluation.md](docs/evaluation.md) | `scope_memory/evaluate.py` | run directories on Babel |
| Synthetic chronological corpus v1.1 (920 episodes, protocol v1) | [training/scope_revision_v1/README.md](training/scope_revision_v1/README.md), [docs/data-generation-prompt.md](docs/data-generation-prompt.md) | `training/scope_revision_v1/build.py` | `training/scope_revision_v1/data/` |
| Prompt baselines and SFT on Babel | [training/sft/README.md](training/sft/README.md) | `training/sft/` | run directories on Babel |
| Analyses for the report: main table, memory classes, structure errors, error-analysis and label-audit packets | [docs/analysis.md](docs/analysis.md) | `scope_memory/analysis.py` | `annotations/label_audit/` |
| Challenge set v1: 24 hand-written episodes in six structure-heavy stressors, evaluation plan fixed in advance | [training/challenge_v1/README.md](training/challenge_v1/README.md) | `training/challenge_v1/build.py` | `training/challenge_v1/data/`, `samples.md` |
| Final test evaluation (run once, 2026-11-23/24) and error-analysis packets | [docs/evaluation.md](docs/evaluation.md#test-results-2026-11-24) | `scope_memory/analysis.py` | `results/test_p12/`, `annotations/error_analysis/` |
| Post-hoc analyses (format against writing, dev against test, write metrics, cost) and figures for the report | [docs/analysis.md](docs/analysis.md#post-hoc-analyses-2026-11-24) | `scope_memory/posthoc.py`, `scope_memory/figures.py` | `results/posthoc/`, `results/figures/` |

## Quickstart

Python 3 standard library only, no install step. From the repository root:

```sh
python3 -m unittest -v                          # 55 tests
python3 -m scope_memory.replay                  # replay smoke test
python3 -m scope_memory.read_write_diagnostic   # stdout = results/read_write_results.json
python3 -m scope_memory.score_blind_pilot       # stdout = results/blind_score.json
python3 -m scope_memory.evaluate self-check --data fixtures/protocol_episode.json   # protocol pipeline check
python3 -m scope_memory.audit_horizon PATH_TO_ROWS_RESPONSE --output results/audit_horizon_result.json
```

The HorizonBench rows response is kept out of Git ([docs/horizon-audit.md](docs/horizon-audit.md)). Training-corpus checks are listed in [training/README.md](training/README.md).

## Replay smoke test

`scope_memory/replay.py` replays one handwritten, structured toy timeline (`fixtures/toy_episode.json`) in chronological order. It covers a persistent preference, a contextual exception that should not overwrite it, and a genuine global update that retains an explicit local exception.

The scope-blind rule and scope-aware oracle receive supplied action/scope annotations. Their toy outcomes demonstrate evaluator plumbing only, **not learned performance, SFT baselines, or evidence for the proposed method**. QA is exact match on six toy probes. False-overwrite rate counts scoped events that changed a previously stored global value, divided by scoped events with an existing global value; this narrow engineering definition must be finalized for the real study. Gold QA fields stay outside the manager input.

## TA feedback and candidate datasets

The latest supplied reply supports the direction and recommends data curation, SFT, and benchmarking first. Audit:
- [HorizonBench](https://github.com/stellalisy/HorizonBench): mental_state_graphs, dated preferences/events/conversations and exception coverage.
- [LongMemEval](https://github.com/xiaowu0162/LongMemEval): temporal reasoning and knowledge updates.
- [MemSyco-Bench](https://github.com/XMUDeepLIT/MemSyco-Bench/blob/main/data/README.md): contextual scope and current versus outdated preference selection.

These are candidates, not verified ready-made per-event action-label datasets. Prefer adapting existing examples if needed rather than immediately generating long synthetic dialogues. Split by user/timeline before deriving training examples. Keep hidden graph dates distinct from when preference changes become observable in replay. Never use future conversations or gold memory/evaluation fields as model inputs. Audit licenses, provenance and annotation agreement before data use. Evaluate chronological QA and false overwriting under matched models, seeds and decode settings.

## Data hygiene

- Tracked: code, small handwritten fixtures and annotations, small saved results, and the synthetic corpora v0.1 and v1.1 (about 13 MB of JSONL).
- Not tracked: raw correspondence, raw dataset rows, credentials, checkpoints and run outputs (`local-notes/`, `private/`, `data/`, `outputs/`, `runs/`, `logs/`, `checkpoints/` are ignored).
- The three audited HorizonBench users are audit-only and stay out of training, validation and final test.
- The earlier 40-example smoke pilot and 24-example candidate eval set must never enter training.
- `training/scope_revision_training/labels.jsonl` holds gold states and actions; never feed it to a model as input.

