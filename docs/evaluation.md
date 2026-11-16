# Evaluation under protocol v1

`scope_memory/evaluate.py` scores both arms on episodes that follow [protocol.md](protocol.md). Standard library only.

## Primary result and diagnostics

| Role | What | Where |
|---|---|---|
| Primary | Answer Agent QA on each arm's own rollout memory: overall, per QA group and probe type, and the paired scope-minus-CRUD difference | `rollout-score --answers`; the report says `"role": "primary"` |
| Diagnostic | Everything read with the rule readers `read_scope_state` / `read_crud_state`: teacher-forced metrics, rollout write metrics, QA read by the oracle reader | teacher-forced reports, `<arm>.diagnostic` in rollout reports, `rollout-score` without answers; `"role": "diagnostic"` |
| Reported apart | Rule-reader parse failures: accepted output whose memory the reader cannot parse | `parse_failures` (teacher-forced), `crud_rule_reader_parse_failure` (rollout) |

The Answer Agent is the same base model for both arms, loaded without any adapter, and reads the memory records as written. `read_crud_state` accepts only the canonical sentences, so a CRUD record with the right meaning in other words is a parse failure for the rule reader, not a wrong answer. Rule-reader error metrics (`false_overwrite`, `missed_update`, `exception_disturbed` and the `_if_readable` accuracies) leave such rows out; the strict `row_correct` and `state_correct` count them as wrong. Conclusions about H1 and H2 rest on the primary result.

## Teacher-forced (outline v2.7, G2; diagnostic)

Each event is scored on its own: the completion is applied to the gold memory before that event. Predictions are JSONL rows `{"id": "<episode>/<event>/<arm>", "completion": "<raw model output>"}`; the matching prompts come from `python3 -m scope_memory.protocol export-sft`.

Parse failures (`parse_failures`; the per-event `status` in brackets):

| Metric | Events | Meaning |
|---|---|---|
| `invalid_output` | all | missing, not JSON, or not a JSON object (`invalid`) |
| `rejected_by_executor` | all | breaks the protocol, so the memory is kept (`rejected`) |
| `rule_reader_parse_failure` | all | accepted, but the rule reader cannot parse the resulting memory (`uninterpretable`) |
| `rule_reader_parse_failure_if_accepted` | accepted outputs | the same, among accepted outputs only |

Metrics (`metrics`; the report names the rule-reader ones in `rule_reader_metrics`):

| Metric | Events | Meaning |
|---|---|---|
| `row_correct` | all | accepted, readable output with the gold state and the gold decision; parse failures count as wrong |
| `row_correct_if_readable` | all but parse failures | the same, leaving parse failures out |
| `state_correct`, `state_correct_if_readable` | as the two above | the state part alone |
| `decision_correct` | all | the `resolved` / `clarify` decision (no reader) |
| `false_overwrite` | readable, all except `general_update` | a general value changed |
| `missed_update` | readable `general_update` | the general value is not the new one |
| `exception_disturbed` | readable events with exceptions outside the gold change | such an exception changed or vanished |
| `spurious_write` | `stable_preference`, `clarify` | memory changed (no reader) |
| `clarify_recall`, `false_clarify` | `clarify` / all others | the decision is `clarify` (no reader) |

## Rollout (outline v2.7 main metric)

`rollout(episode, arm, policy)` runs one arm with its own memory, where `policy(arm, system, prompt, context)` returns the raw completion. Each probe reads the snapshot after its event. QA accuracy is reported overall, per QA group (`general_update`, `scoped_exception`, `exception_revision`, `stable_preference`) and per probe type, together with the paired scope-minus-CRUD difference, rejected outputs, missing answers and memory size at the probes.

Answer Agent replies are passed as JSONL rows `{"id": "<episode>/<probe>/<arm>", "answer": "..."}`; `answer_prompt(view, probe)` builds the same input for both arms. Without answers the deterministic oracle reader is used, which only checks the pipeline.

Each arm's `diagnostic` block holds the rule-reader numbers along its own memory: `rule_reader_parse_failure_at_probes`, `rule_reader_parse_failure_after_events`, and `write_metrics` (`rollout_false_overwrite`, `rollout_missed_update`, `rollout_spurious_write`, `rollout_state_matches_gold`, `rollout_state_matches_gold_if_readable`). The CRUD parse-failure rates are repeated at the top of the report as `crud_rule_reader_parse_failure`.

Intervals are 95% percentile bootstraps over episodes (one fictional user each).

## Safeguards

- `rollout-score` without `--answers` uses the oracle reader, labels the report as a pipeline check and warns unless `--oracle-reader` is passed.
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

## Model runs

`training/sft/baseline.py` produces the inputs on Babel: teacher-forced predictions, rollout trajectories and Answer Agent replies. Prompt baselines run without adapters; with `--shots k` both arms see demonstrations of the same train events, one per event category. SFT runs pass `--adapter-scope` and `--adapter-crud`, so each arm generates only with its own adapter; the Answer Agent is then a freshly loaded base model, and the script stops if any LoRA module is present.

Two reference rows put the QA numbers in range, both read by the same Answer Agent: `--policy gold` gives it each arm's gold memory (its ceiling with correct memory) and `--policy noop` the memory as seeded, never written (the do-nothing floor). Chance is 25% (four options per probe).

### Answer Agent prompt versions

`ANSWER_READERS` in `scope_memory/evaluate.py` holds the Answer Agent prompts, the same for both arms. Version 1 is the original prompt. Version 2 adds one reading rule: "A record limited to a situation or to dates applies only in that situation and on those dates; when no limited record applies, use the general preference." Version 3 adds the rule and asks for a one-sentence check before a final `Answer:` line, which is where the option is read.

Version 1 misread correct memory: on gold memory it failed every boundary probe (a date just after a temporary preference ended: 0/28 for CRUD, 2/28 for scope, against 14/28 and 12/28 when memory was never written) and answered default probes ("an ordinary occasion") with an exception's value (77.8% CRUD, 85.9% scope). The version for formal results is chosen on gold memory alone, before any SFT result exists: the highest QA averaged over the two arms, and the simpler version when two are within one point. `run_config.json`, `answer_agent.json` and the primary report record the version. `baseline.py --from-run OLD_RUN` re-reads a finished run with another version without running the policy again; the settings must match apart from the version.

## Not covered yet

- Cost metrics beyond memory size and token counts at the probes.
- The v0.1 corpus in `training/scope_revision_training/`, which predates this protocol.
