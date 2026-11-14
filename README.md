# Learning Scope-Aware Memory Revision for Evolving User Preferences

Three-person final-project scaffold. Main research plan: compare an SFT-trained generic CRUD memory manager (Add/Update/Delete/No-op) with an SFT-trained manager that also represents scope and relationships. RL is a stretch goal, not started.

## Current engineering status
A stdlib-only chronological replay smoke test uses one handwritten, structured toy timeline. It covers a persistent preference, a contextual exception that should not overwrite it, and a genuine global update that retains an explicit local exception. No model has been trained and no research dataset has been downloaded.

```sh
python3 -m unittest -v
python3 replay.py
```

The scope-blind rule and scope-aware oracle receive supplied action/scope annotations. Their toy outcomes demonstrate evaluator plumbing only, **not learned performance, SFT baselines, or evidence for the proposed method**. QA is exact match on six toy probes. False-overwrite rate counts scoped events that changed a previously stored global value, divided by scoped events with an existing global value; this narrow engineering definition must be finalized for the real study. Gold QA fields stay outside the manager input.

## TA feedback and next steps
The latest supplied reply supports the direction and recommends data curation, SFT, and benchmarking first. Audit:
- [HorizonBench](https://github.com/stellalisy/HorizonBench): mental_state_graphs, dated preferences/events/conversations and exception coverage.
- [LongMemEval](https://github.com/xiaowu0162/LongMemEval): temporal reasoning and knowledge updates.
- [MemSyco-Bench](https://github.com/XMUDeepLIT/MemSyco-Bench/blob/main/data/README.md): contextual scope and current versus outdated preference selection.

These are candidates, not verified ready-made per-event action-label datasets. Prefer adapting existing examples if needed rather than immediately generating long synthetic dialogues. Split by user/timeline before deriving training examples. Keep hidden graph dates distinct from when preference changes become observable in replay. Never use future conversations or gold memory/evaluation fields as model inputs. Audit licenses, provenance and annotation agreement before data use. Evaluate chronological QA and false overwriting under matched models, seeds and decode settings.

## Hygiene
The Windows original scaffold is preserved. This WSL working copy is the active development copy. No GitHub remote has been created. Raw correspondence, generated data, outputs, credentials and checkpoints are excluded from Git. Only tiny handwritten fixtures are tracked.
