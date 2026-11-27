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

Version 1 misread correct memory: on gold memory it failed every boundary probe (a date just after a temporary preference ended: 0/28 for CRUD, 2/28 for scope, against 14/28 and 12/28 when memory was never written) and answered default probes ("an ordinary occasion") with an exception's value (77.8% CRUD, 85.9% scope). The version for formal results is chosen on gold memory alone, before any SFT result exists: the highest QA averaged over the two arms, and the simpler version when two are within one point. `run_config.json`, `answer_agent.json` and the primary report record the version.

Calibration on the dev split (1,170 probes per arm):

| Version | Gold memory CRUD | Gold memory scope | Mean | Scope − CRUD on gold [95% CI] | Never written CRUD / scope | Boundary probes on gold, CRUD / scope |
|---|---|---|---|---|---|---|
| 1 | 88.5 | 91.2 | 89.9 | +2.6 [+0.3, +5.0] | 35.3 / 36.0 | 0/28, 2/28 |
| 2 | 90.8 | 91.9 | 91.4 | +1.0 [−0.9, +3.0] | 35.9 / 36.4 | 0/28, 2/28 |
| 3 | 92.5 | 93.3 | 92.9 | +0.9 [−1.2, +2.9] | 36.1 / 36.9 | 8/28, 11/28 |

Version 3 is the default (`ANSWER_READER = 3`); 2 of its 2,340 replies on gold memory lacked the `Answer:` line. Even version 3 misses most boundary probes on gold memory, fewer than it gets right when memory was never written (14/28 and 12/28), so boundary probes reward not storing an ended preference; report them apart from the other probe types. `baseline.py --from-run OLD_RUN` re-reads a finished run with another version without running the policy again; the settings must match apart from the version.

This calibration used protocol 1.1 gold memory, written with catalog names. Protocol 1.2 gold memory uses the user's words, so its gold reference is run again, but the version stays 3: it is not re-chosen on later results. On dev, protocol 1.2 gold memory scores CRUD 91.4, scope 91.5 (scope − CRUD +0.1 [−2.4, +2.5]).

## Cost

Each run directory gets `cost.json` from `training/sft/cost_report.py` (older runs: run it by hand with `--runs`). Per arm it counts policy calls (one per rollout event) with chat-templated input tokens and generated tokens, Answer Agent calls (one per probe) with input and generated tokens, memory tokens at the probes, and rejected outputs. `--sft-rows` adds the prompt and completion (loss) tokens of exported SFT rows, which differ between the arms because the scope arm's outputs are longer. GPU time comes from Slurm accounting (`sacct --duplicates`, summing preempted attempts); the cluster charges no money, so cost is reported in tokens, calls and GPU-hours.

## Final test evaluation

The test split is read once, after everything below is frozen; nothing is re-chosen after its results.

- Protocol 1.2 (gold copies the user's words), the policy instructions and the Answer Agent prompt version 3.
- Base model Qwen3-4B-Instruct-2507, greedy decoding, 512 new tokens for the policy.
- Prompt baselines M0 / M1: zero-shot, and six-shot with the six train events `pick_demos` chooses (the same as in the protocol 1.2 dev run).
- SFT M2 / M3: LoRA r16 / alpha 32, 2 epochs, lr 1e-4, effective batch 16, seeds 0, 1 and 2, the final checkpoint of each seed (`sft-p12`); results pool the three seeds per probe.
- Reference rows: gold memory and never-written memory.
- The analyses and their settings in [analysis.md](analysis.md): the main table (`report`), boundary probes reported apart, the rule-reader diagnostics, and the pre-specified samples for the manual error analysis.

Frozen on 2026-11-17 (git tag `freeze-p12`), after the challenge-set results. The three pre-registered SFT seeds are
kept; no seed or setting was added or changed after the challenge set. Identifiers:

| Item | Value |
|---|---|
| Data v1.1, `training/scope_revision_v1/data/` | SHA-256 train `494b76c7…`, dev `c8bd3dea…`, test `f5e680a1…` (full values in `manifest.json`) |
| Policy instructions | SHA-256 scope `a41fed14…`, CRUD `6d54c95c…` |
| SFT rows (protocol 1.2 export) | SHA-256 scope `beaca8bd…`, CRUD `e5745306…` |
| SFT adapters | `/data/user_data/zichuwu/scope-sft/ckpt/sft-p12-{scope,crud}-s{0,1,2}/adapter`; each run's `train_summary.json` records its arm and instruction SHA-256, which `baseline.py` checks |
| Answer Agent | prompt version 3 |

Before the run, the label audit in [analysis.md](analysis.md#label-audit-of-the-synthetic-data) is done and the team
decides whether its error rate needs a data fix. Then `submit_test.sh` runs once.

The initial label audit recorded on 2026-11-23 contained Raina's file, agreeing with 58 of the 60 gold categories.
A non-blind check retained both disputed gold labels and no data were changed
([initial result](analysis.md#result-2026-11-23)).

A second annotation file covering the same 60 items was added after the test run (2026-11-24): the original two
files agree on 58 of 60 (96.67%, kappa 0.96). Raina reported that C decided both disagreements for A, and the final
aggregate agrees with the generated categories on all 60
([record](analysis.md#second-annotator-and-adjudication-after-the-test-run-2026-11-24)). This does not
change the record above.

`bash ~/scope-sft-work/sft/submit_test.sh` (Babel login node) submits the seven runs with `SPLIT=test` into `runs/test_p12_*`; every run directory gets a `SUBMITTED` marker, so a second call submits nothing again.

## Test results (2026-11-24)

The seven runs from `submit_test.sh` (jobs 11262743–11262749, submitted once on 2026-11-23 at 21:41 ET) finished on
2026-11-24 at 00:03 ET. Every run covers the 200 test episodes and the same 2,027 probes per arm with Answer Agent
prompt version 3, and each SFT run used the `sft-p12` adapters of its own seed. The tables come from the analyses
fixed in [analysis.md](analysis.md); their JSON output is in [results/test_p12/](../results/test_p12/).

Answer Agent QA in % of probes (SFT pools the three seeds per probe; 95% intervals from the episode bootstrap):

| Condition | CRUD | Scope | Scope − CRUD | Without the 88 boundary probes: CRUD / scope, scope − CRUD |
|---|---|---|---|---|
| Never written | 48.1 | 50.1 | +2.0 [+1.0, +3.0] | 47.5 / 49.7, +2.1 [+1.2, +3.0] |
| Zero-shot | 56.6 | 57.0 | +0.4 [−2.9, +3.7] | 58.2 / 57.2, −1.0 [−4.2, +2.4] |
| Six-shot | 53.8 | 65.3 | +11.5 [+8.1, +14.9] | 54.8 / 66.5, +11.7 [+8.1, +15.1] |
| SFT, three seeds | 83.3 | 86.1 | **+2.7 [+0.9, +4.5]** | 86.3 / 88.0, **+1.7 [−0.2, +3.4]** |
| Gold memory | 86.9 | 89.6 | +2.7 [+1.2, +4.2] | 90.0 / 91.7, +1.7 [+0.1, +3.1] |

**H1** (SFT scope minus SFT CRUD): +2.7 [+0.9, +4.5] on all probes and +1.7 [−0.2, +3.4] without boundary probes. The
three seeds point the same way (description only): +2.8 [+0.4, +5.0], +0.8 [−1.4, +3.0] and +4.5 [+2.6, +6.4]
(CRUD 83.6 / 83.8 / 82.6, scope 86.4 / 84.6 / 87.2). The development sets did not show this: on dev the scope arm
trailed (−2.5 [−5.2, +0.3]; without boundary probes −3.3 [−6.0, −0.5]), and on the challenge set the arms tied
(+0.4 [−2.9, +4.0]) with seeds that disagreed.

**H2** (SFT minus the prompt baselines): CRUD +26.7 [+23.6, +29.8] over zero-shot and +29.6 [+26.6, +32.4] over
six-shot; scope +29.0 [+26.1, +32.1] and +20.8 [+18.0, +23.4]. Without boundary probes: +28.1, +31.5, +30.8 and
+21.5, every interval far from zero. SFT closes about 91% of the gap between never-written and gold memory in both
arms.

By probe type and QA group (SFT pooled over the seeds, and gold memory for comparison):

| Group | Probes | SFT CRUD / scope | SFT scope − CRUD | Gold CRUD / scope | Gold scope − CRUD |
|---|---|---|---|---|---|
| Target probes | 691 | 86.8 / 84.4 | −2.4 [−5.1, +0.3] | 92.0 / 90.5 | −1.6 [−4.1, +1.0] |
| Default probes | 531 | 79.7 / 91.0 | +11.2 [+7.9, +14.8] | 81.7 / 92.8 | +11.1 [+7.5, +14.9] |
| Neighbor probes | 717 | 90.8 / 89.3 | −1.4 [−4.2, +1.0] | 94.3 / 92.0 | −2.2 [−4.1, −0.3] |
| Boundary probes | 88 | 17.4 / 43.2 | +25.8 [+15.7, +36.0] | 17.1 / 43.2 | +26.1 [+14.1, +38.0] |
| `general_update` | 279 | 89.6 / 90.3 | +0.7 [−4.3, +5.1] | 92.1 / 94.3 | +2.1 [−1.2, +5.6] |
| `scoped_exception` | 558 | 73.6 / 77.9 | +4.3 [+1.5, +7.0] | 76.5 / 81.0 | +4.5 [+1.6, +7.4] |
| `exception_revision` | 596 | 84.4 / 87.2 | +2.8 [−0.1, +5.5] | 88.1 / 90.8 | +2.7 [−0.2, +5.4] |
| `stable_preference` | 594 | 88.5 / 90.6 | +2.1 [−0.5, +4.8] | 92.9 / 94.3 | +1.4 [−1.0, +3.9] |

Reading, after the fact (not a pre-registered test). The SFT difference is as large as the difference on gold memory
(+2.7 both), where the two arms hold the same content in their own formats, and it sits in the same probes: default
probes ("an ordinary occasion"), which the Answer Agent gets wrong more often from CRUD text, and boundary probes (the
day after a temporary preference ended). On target and neighbor probes CRUD is slightly ahead in both conditions. Each
SFT policy loses about as much against its own gold memory (CRUD −3.6, scope −3.5 points). On dev the scope policy
lost twice as much (−5.2 against −2.6), which accounts for the dev deficit. So on the test split the scope arm's lead
reflects how well the Answer Agent reads the scope format, while the two policies' own write errors cost about the
same.

Diagnostics (rule readers; descriptive):

- Memory at the probe, three seeds pooled (6,081 probe-seed pairs per arm): it matches gold for CRUD 84.2% and scope
  83.5%, and its structure differs from gold for CRUD 6.0% and scope 7.2% (dev 7.6% and 12.4%). Split by the scope
  arm's class, scope leads by +5.2 [+3.7, +6.8] where its memory matches gold (263 probe-seeds net) and trails where it
  does not: −16.6 [−33.2, −4.9] with the same structure but another value (−56) and −11.2 [−18.9, −3.9] with another
  structure (−49).
- Teacher-forced structure match (3,573 events per arm over the seeds): CRUD 96.1%, scope 95.0% (dev 96–97% and
  92–95%). Among the most common errors, both arms skip a new scoped exception (NOOP: CRUD 26, scope 27) or overwrite
  another record with it (CRUD UPDATE 20, scope REVISE 11), turn an exception revision into a NOOP or a new record
  (CRUD 38, scope 40), and write on stable-preference events (CRUD 24, scope 18).
- Written words: 4.2% of the values the scope policy writes are not a listed form (77 of 1,851), 5.8% for CRUD
  (108 of 1,871).
- Executor rejections in the rollouts, of 1,191 events per arm: SFT scope 1 / 9 / 1 by seed, CRUD 0; zero-shot scope
  312, CRUD 5; six-shot scope 371, CRUD 13.

Cost: per call (SFT seed 0), the policy reads 886 tokens for scope and 604 for CRUD and writes 66 and 36; the Answer
Agent reads 468 and 263; the memory at a probe is 253 and 107 tokens (`cost.json` in each run directory). Slurm
accounting, summing preempted attempts: 8.2 GPU-hours for the seven runs, one GPU each (mixed GPU types): SFT
1.06 / 1.37 / 1.37 h, six-shot 2.18 h, zero-shot 1.62 h, never-written 0.25 h and gold 0.34 h.

Run notes. Zero-shot (11262745) was preempted once and SFT seed 2 (11262749) twice; `baseline.py` resumed them,
keeping the stages already written. After `ALL_DONE` the preemption quirk requeued both: the zero-shot copy was
cancelled while pending, and the seed-2 copy started, printed "already done" and overwrote that run's Slurm log, so
seed 2 has no full log; its result files are complete. After download all seven runs were checked: the same 2,027
probes per arm, no duplicate answers, the test file, reader 3, and adapters that match the seed.

Post-hoc analyses added afterwards (format against writing with intervals over episodes and over attributes, the
comparison with dev, teacher-forced write metrics, cost, and the figures for the report) are in
[analysis.md](analysis.md#post-hoc-analyses-2026-11-24); they re-read these runs and change none of the numbers above.
The read-time experiments of the team's mid-project update (A: answering from the raw conversations; B: the same
memory shown in other ways) ran later with the same frozen Answer Agent and are post-hoc too
([analysis.md](analysis.md#read-time-experiments-post-hoc-2026-11-24)). A larger reader (Qwen3-30B-A3B-Instruct-2507)
later re-read the same test memories, also post-hoc: the scope arm's lead stays, +3.2 [+1.1, +5.0]
([analysis.md](analysis.md#results-on-test-and-the-challenge-set-2026-11-27)).

Next is the manual error analysis fixed in [analysis.md](analysis.md#manual-error-analysis-pre-specified). Its packets
are in [annotations/error_analysis/](../annotations/error_analysis/): 40 of the 275 wrong scope probes and 40 of the
332 wrong CRUD probes of seed 0, each to be labelled by two annotators.

## Challenge set

`training/challenge_v1/` holds 24 hand-written episodes of structure-heavy cases (dense memory, a situation shared by two attributes, confusable situations, order-dependent chains, windows, distractors). Its README gives the design and the evaluation plan, fixed before any model ran on it. `baseline.sbatch` reads it with `SPLIT=challenge`. `bash ~/scope-sft-work/sft/submit_challenge.sh references` runs the never-written and gold references first; after the data check on gold memory, `submit_challenge.sh policies` runs zero-shot, six-shot and the three `sft-p12` seeds once, with the settings frozen for the test split. `analysis.py report` adds a `stressor_<name>` group per stressor. The set is evaluation data only and does not replace the test split.

## Not covered yet

- The v0.1 corpus in `training/scope_revision_training/`, which predates this protocol.

