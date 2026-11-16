# Learning Scope-Aware Memory Revision for Evolving User Preferences

How should an AI agent revise stored preferences when a new statement is a contextual exception rather than a global preference change? This three-person final project compares an SFT-trained generic CRUD memory manager (add / update / delete / no-op over free-text memories) with an SFT-trained manager that also represents preference scope and relationships between memories. RL is a stretch goal and has not started. The experiment design is in [docs/sft-plan.md](docs/sft-plan.md).

> **Status (2026-11-15):** no model has been trained and no SFT or GPU job has been launched. Everything here is evaluation plumbing, a data audit or data preparation, not evidence of learned performance.

## Repository layout

```text
scope_memory/   stdlib-only Python code; run modules with python3 -m scope_memory.<name>
tests/          unit tests for scope_memory
fixtures/       handwritten toy timeline for the replay smoke test
annotations/    blind annotation pilot: packet, author key, locked labels
results/        small saved outputs of the scope_memory scripts
docs/           experiment plan and one write-up per milestone
training/       synthetic SFT corpus v0.1, its audit and the CPU preflight
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

## Quickstart

Python 3 standard library only, no install step. From the repository root:

```sh
python3 -m unittest -v                          # 21 tests
python3 -m scope_memory.replay                  # replay smoke test
python3 -m scope_memory.read_write_diagnostic   # stdout = results/read_write_results.json
python3 -m scope_memory.score_blind_pilot       # stdout = results/blind_score.json
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

- Tracked: code, small handwritten fixtures and annotations, small saved results, and the synthetic training corpus v0.1 (about 0.4 MB of JSONL).
- Not tracked: raw correspondence, raw dataset rows, credentials, checkpoints and run outputs (`local-notes/`, `private/`, `data/`, `outputs/`, `runs/`, `logs/`, `checkpoints/` are ignored).
- The three audited HorizonBench users are audit-only and stay out of training, validation and final test.
- The earlier 40-example smoke pilot and 24-example candidate eval set must never enter training.
- `training/scope_revision_training/labels.jsonl` holds gold states and actions; never feed it to a model as input.
