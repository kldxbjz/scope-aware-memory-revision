# Evaluation under protocol v1

`scope_memory/evaluate.py` scores both arms on episodes that follow [protocol.md](protocol.md). Standard library only.

## Teacher-forced (outline v2.7, G2)

Each event is scored on its own: the completion is applied to the gold memory before that event. Predictions are JSONL rows `{"id": "<episode>/<event>/<arm>", "completion": "<raw model output>"}`; the matching prompts come from `python3 -m scope_memory.protocol export-sft`.

| Metric | Events | Meaning |
|---|---|---|
| `row_correct` | all | accepted output with the gold state and the gold decision |
| `state_correct`, `decision_correct` | all | each part on its own |
| `invalid_or_rejected` | all | unparseable, or rejected by the executor (the state is kept) |
| `uninterpretable` | all | accepted CRUD text that does not read back as the canonical sentences |
| `false_overwrite` | all except `general_update` | a general value changed |
| `missed_update` | `general_update` | the general value is not the new one |
| `exception_disturbed` | events with exceptions outside the gold change | such an exception changed or vanished |
| `spurious_write` | `stable_preference`, `clarify` | memory changed |
| `clarify_recall`, `false_clarify` | `clarify` / all others | the decision is `clarify` |

## Rollout (outline v2.7 main metric)

`rollout(episode, arm, policy)` runs one arm with its own memory, where `policy(arm, system, prompt, context)` returns the raw completion. Each probe reads the snapshot after its event. QA accuracy is reported overall, per QA group (`general_update`, `scoped_exception`, `exception_revision`, `stable_preference`) and per probe type, together with the paired scope-minus-CRUD difference, rejected outputs and memory size at the probes.

Answer Agent replies are passed as JSONL rows `{"id": "<episode>/<probe>/<arm>", "answer": "..."}`; `answer_prompt(view, probe)` builds the same input for both arms. Without answers the deterministic oracle reader is used, which only checks the pipeline.

Intervals are 95% percentile bootstraps over episodes (one fictional user each).

## Safeguards and extra metrics

- `rollout-score` without `--answers` uses the oracle reader, labels the report as a pipeline check and warns unless `--oracle-reader` is passed. Formal H1/H2 numbers need Answer Agent replies.
- Rollout write metrics follow each arm's own memory: `rollout_false_overwrite`, `rollout_missed_update`, `rollout_spurious_write`, `rollout_state_matches_gold`, plus `rollout_unreadable_memory` for memory the canonical reader cannot parse.
- CRUD format problems are kept apart from semantic errors: `state_correct_if_readable` scores only readable outputs, and `uninterpretable` counts the rest; Answer Agent QA does not depend on sentence format.
- The paired scope-minus-CRUD difference is reported only when both arms cover the same episode and probe IDs (`pairing_complete`).
- `--tokenizer DIR` adds memory token counts at the probes; otherwise memory size is in records and words.

## Commands

```sh
python3 -m scope_memory.evaluate self-check --data fixtures/protocol_episode.json
python3 -m scope_memory.protocol check training/scope_revision_v1/data/dev.jsonl
python3 -m scope_memory.protocol export-sft training/scope_revision_v1/data/train.jsonl --out outputs/sft
python3 -m scope_memory.evaluate teacher-forced --data DEV.jsonl --arm scope --predictions preds.jsonl
python3 -m scope_memory.evaluate rollout-score --data DEV.jsonl --trajectories traj.jsonl --answers answers.jsonl
```

`self-check` must show gold at 100% in both modes; the NOOP reference shows what never writing costs.

## Not covered yet

- The Answer Agent and the policy model calls themselves (to run on Babel).
- Cost metrics beyond memory size at the probes; token counts need the chosen tokenizer.
- The v0.1 corpus in `training/scope_revision_training/`, which predates this protocol.
