# Analyses for the report

`scope_memory/analysis.py` turns finished run directories (as `training/sft/baseline.sbatch` writes them) into the report's tables. Standard library only. Answer Agent correctness is the primary measure; the rule-reader classes below are diagnostics. Intervals are 95% bootstraps that resample episodes (one fictional user each) together with all their probes and seeds, drawn the same way as in `scope_memory/evaluate.py`.

## Main table: `report`

```sh
python3 -m scope_memory.analysis report --noop RUN --zero-shot RUN --six-shot RUN \
  --sft RUN_S0 RUN_S1 RUN_S2 --gold RUN --out report.json
```

It gives accuracy per condition and arm, scope minus CRUD per condition, H1 (SFT scope minus SFT CRUD) and H2 (SFT minus zero-shot and SFT minus six-shot, per arm). Groups: `all`, `all_but_boundary`, the four QA groups and the four probe types (`type_target`, `type_default`, `type_neighbor`, `type_boundary`); on the challenge set (`training/challenge_v1/`) also one `stressor_<name>` group per stressor. Runs of one condition (seeds) are pooled per probe: a probe counts as the share of seeds that answered it correctly. Boundary probes ask about the day after a temporary preference ended; even gold memory gets most of them wrong ([evaluation.md](evaluation.md)), so they are reported apart and the headline is also given without them. `paired --a RUN... --arm-a ARM --b RUN... --arm-b ARM` compares any two pooled conditions the same way.

On the protocol 1.1 dev runs it reproduces the numbers reported so far: H1 −3.1 [−5.5, −0.8]; H2 CRUD +28.3 (zero-shot) and +31.7 (six-shot), scope +32.3 and +25.5. By probe type, the scope arm's deficit there sat in target probes (−8.5 [−11.9, −4.7]) and neighbor probes (−4.3 [−7.8, −1.0]); default probes +3.4 [−1.6, +8.3].

## Where a difference sits: `memory-classes` (diagnostic)

```sh
python3 -m scope_memory.analysis memory-classes RUN_S0 RUN_S1 RUN_S2
```

Each probe's memory for its attribute is compared with the gold state after the probe's event, read with that arm's rule reader:

| Class | Meaning |
|---|---|
| `matches_gold` | the records map to exactly the gold state (aliases count as the catalog value) |
| `same_structure` | the same general record and the same situations with the same validity, but some value differs (another option, or words that are not a listed form) |
| `different_structure` | records or validity differ: a missing, extra or duplicate record, another situation, other dates |
| `unreadable` | a record that may belong to the attribute does not map to the catalog (an unlisted situation, a CRUD text outside the CRUD sentences) |

The report gives the class shares and QA accuracy per arm, and the paired scope-minus-CRUD difference split by either arm's class, with the number of probes of the gap in each class (`gap_probes`, summed over seeds). The split is made after the fact on the memory a policy wrote, so it locates a difference; it is not by itself causal evidence.

## Teacher-forced structure: `structure` (diagnostic)

```sh
python3 -m scope_memory.analysis structure RUN_S0 RUN_S1 RUN_S2
```

On the teacher-forced predictions, how often each arm's operations match gold when written strings are ignored (operation, target, validity kind, `EXCEPTION_TO` target for the scope arm; operation and target id for CRUD), by event category; the most common mismatches as gold → predicted; and how many written values and situations are listed forms (catalog name or alias) versus other words.

## Manual error analysis (pre-specified)

Outline v2.7 §6 asks to separate action choice, executor rejection, reader matching and Answer Agent reasoning on a sample fixed in advance. Fixed before the test split is read:

- Run: `runs/test_p12_sft_s0` (SFT seed 0), both arms.
- Sample: `python3 -m scope_memory.analysis error-sample RUN --arm scope --n 40 --seed 0 --out DIR`, and the same with `--arm crud`: 40 probes the Answer Agent got wrong per arm, drawn with seed 0 from the sorted wrong probe ids (all of them when fewer). `packet_<arm>.md` shows the question, options, gold, the Answer Agent's reply, the arm's memory and the gold memory at the probe, and every event up to the probe with its gold output and the policy's output.
- Two annotators label every item alone in a copy of `labels_<arm>.json`, then run `agreement --labels A.json B.json`, settle disagreements by discussion, and the report gives the settled counts per source and arm with the raw agreement and kappa.
- Made on 2026-11-24 after the test run, with the commands above: [annotations/error_analysis/](../annotations/error_analysis/) holds `packet_<arm>.md`, `sample_<arm>.json` and the empty `labels_<arm>.json` (40 of 275 wrong scope probes, 40 of 332 wrong CRUD probes). Not labelled yet.

Sources, taking the first that applies:

| Source | When |
|---|---|
| `data` | the question, the options or the gold answer is wrong or ambiguous given the conversations |
| `executor_rejection` | the memory is wrong because the executor rejected a policy output that held the needed write |
| `action` | the memory is wrong because of an accepted policy output or a missing one: wrong operation or target, situation, dates or value, a missed write, a spurious write |
| `reader_matching` | the memory is right, but its words do not plainly match the question or options and the reply shows the Answer Agent did not connect them |
| `answer_reasoning` | the memory is right and plainly matches, and the Answer Agent still chose wrong, for example by ignoring the dates or applying a situation's preference to an ordinary occasion |
| `other` | none of these; the note says why |

The memory is right when the record that should answer the probe holds the gold value for that situation and date; differences elsewhere in memory do not count.

## Label audit of the synthetic data

Outline v2.7 §5 asks that demonstrations be checked by rules and by sampling. `replay_gold` passes for all 920 episodes; the sample check is done before the test split is evaluated:

```sh
python3 -m scope_memory.analysis label-sample training/scope_revision_v1/data/train.jsonl \
  training/scope_revision_v1/data/test.jsonl --per-category 5 --seed 0 --out annotations/label_audit
python3 -m scope_memory.analysis agreement --labels A.json B.json --key annotations/label_audit/key.json
```

The first command draws 5 events of every category from train and from test (60 events, shuffled, opaque ids) and writes `packet.md` (the stored preferences before the event, written as CRUD sentences, and the conversation, no labels), `labels_template.json` and `key.json`, which names the event behind each id. Two team members copy the template, label every item alone with one category from protocol §3 without opening the data files, and run the second command. It reports each annotator's agreement with the gold category and the disagreements, and the agreement and kappa between the annotators. A gold label both annotators reject is counted as a label error; the team decides on the error rate before the test evaluation whether the data need fixing.

### Result (2026-11-23)

The initial repository record contained one submitted annotation file (Raina), covering all 60 items from the packet
and a Chinese instruction sheet with the same six categories and a recommended order of checks. Subsequent provenance
review established that Raina discussed some items with AI; the record should not be described as unaided human annotation. Her file is `annotations/label_audit/labels_raina.json`, as received
(SHA-256 `3d162e9f…`, no notes). `agreement --labels annotations/label_audit/labels_raina.json --key
annotations/label_audit/key.json` wrote `annotations/label_audit/agreement_raina.json`: she chose the gold category
for 58 of the 60 items (96.7%; Cohen's kappa against gold 0.96). The two disagreements were checked against the
category definitions and the stored preferences shown in the packet. This check was not blind: the checker saw the
gold labels.

| Item | Source | Annotator | Gold | Reading |
|---|---|---|---|---|
| L008 | train `tr-0138` | `exception_revision` | `stable_preference` | There is no stored rule for the situation (typing without gloves), so there is nothing to revise, and the user limits the change to today ("Once this occasion is over, keep my earlier preferences"), which makes it a one-off request. Gold holds. |
| L024 | test `te-0053` | `general_update` | `exception_revision` | The stored preferences already hold a rule for lodgings used for a single night; the user changes its value and says the rest of the preferences stay. Gold holds. |

That non-blind check retained both gold categories and no data were changed. At the time of the test submission,
only Raina's annotation file was recorded in the repository, so the initial report had no inter-annotator agreement.
The later completion below is a separate update; it does not change that submission history. These category-balanced
sample checks do not establish an error-rate bound for the full corpus.

### Second annotator and adjudication (after the test run, 2026-11-24)

After the single test run, the completed second annotation file (A) for the same 60 items was added, together with
Raina's report that a third member (C) settled both disagreements in A's favour. The files were recorded on 2026-11-24; they are in `annotations/label_audit/` as received:
`labels_A.json` (SHA-256 `3ad4f159…`, no notes), `labels_final.json` (SHA-256 `24f5a260…`, the labels after
adjudication; its `annotator` field says `final_adjudicated`: a summary, not a third annotation) and
`adjudication_summary.md` (in Chinese: the comparison, the adjudication and the SHA-256 of both raw files, which it
names by their paths in the team's folders).

```sh
python3 -m scope_memory.analysis agreement --labels annotations/label_audit/labels_raina.json \
  annotations/label_audit/labels_A.json --key annotations/label_audit/key.json \
  --out annotations/label_audit/agreement_raina_A.json
python3 -m scope_memory.analysis agreement --labels annotations/label_audit/labels_final.json \
  --key annotations/label_audit/key.json --out annotations/label_audit/agreement_final.json
```

The two annotators agree on 58 of the 60 items (96.7%; Cohen's kappa 0.96), computed from the two raw files. A chose
the gold category for all 60. The two disagreements are L008 and L024 above; C decided both for A, as Raina reported
(C's own record was not sent). The final labels therefore equal A's labels and the gold category on all 60 items. No
data, setting or result changed.

The audit recorded before the test run is the one-annotator result of 2026-11-23 above; this second file and
adjudication were recorded later and do not change that history. Raina discussed some items with an AI assistant,
which the report should say. The blinding process was not independently verified.

The machine-readable [`adjudication_C_record.json`](../annotations/label_audit/adjudication_C_record.json) records
Raina's confirmation, the two decisions and source hashes; it is not C's original annotation file. The final
aggregate's 60/60 agreement with generated categories does not establish that all fields, probes or episodes are
correct, and must not replace the original 58/60 inter-annotator agreement. The additional 60-item packet remains
a reserve, not a prerequisite for A/B. The separate 40-per-arm error-analysis packets remain a different task.

Current recommendations: [后续实验建议](后续实验建议.md) and [中期 update](中期update.md). The A/B implementation
and run plan below are already committed; check smoke/freeze/job status before submitting duplicate work.

## Post-hoc analyses (2026-11-24)

The team asked for these after the single test run, to describe it and to compare it with dev. None was planned
before the test run, none changes a setting or a pre-specified number, and the test split was not evaluated again:
everything below re-reads the stored run directories (the seven test runs, and the protocol-1.2 dev runs
`sft_p12_eval_s0`–`s2` and `reference_gold_p12`). Code: `scope_memory/posthoc.py`; reports:
[results/posthoc/](../results/posthoc/); figures and the tables behind them: [results/figures/](../results/figures/)
(`tables.md`).

```sh
# from a folder that holds the run directories under runs/ (on Babel: ~/scope-sft-work/runs), with REPO the
# repository and PYTHONPATH=$REPO
P="python3 -m scope_memory.posthoc"; T=runs/test_p12; D=runs/sft_p12_eval; O=$REPO/results/posthoc
$P decompose --sft ${T}_sft_s0 ${T}_sft_s1 ${T}_sft_s2 --gold ${T}_gold --out $O/decomposition_test.json
$P decompose --sft ${D}_s0 ${D}_s1 ${D}_s2 --gold runs/reference_gold_p12 --out $O/decomposition_dev.json
$P mechanism ${T}_sft_s0 ${T}_sft_s1 ${T}_sft_s2 --out $O/mechanism_test.json
$P mechanism ${D}_s0 ${D}_s1 ${D}_s2 --out $O/mechanism_dev.json
$P cost --noop ${T}_noop --zero-shot ${T}_zero_shot --six-shot ${T}_six_shot \
  --sft ${T}_sft_s0 ${T}_sft_s1 ${T}_sft_s2 --gold ${T}_gold --out $O/cost_test.json
$P composition $REPO/training/scope_revision_v1/data/{train,dev,test}.jsonl --out $O/composition.json
$P dev-vs-test --dev-sft ${D}_s0 ${D}_s1 ${D}_s2 --dev-gold runs/reference_gold_p12 \
  --test-sft ${T}_sft_s0 ${T}_sft_s1 ${T}_sft_s2 --test-gold ${T}_gold --out $O/dev_vs_test.json
python3 -m scope_memory.figures --results $REPO/results --out $REPO/results/figures   # needs matplotlib
```

### Format against writing

The SFT difference on every probe splits into two parts that add up to it:

- format = gold scope − gold CRUD: what the Answer Agent gains from the scope format when the memory is right;
- writing = (SFT scope − gold scope) − (SFT CRUD − gold CRUD): how much less the scope policy loses against its own
  gold memory than the CRUD policy does (negative: it loses more).

The intervals use two resampling units: the episode, as in the pre-specified analyses, and the family. A family is one
preference attribute. Train, dev and test have 28 attributes each and share none, so the family interval shows how
far a result carries over to other attributes.

| Points (scope − CRUD) | Test | Dev | Test − dev |
|---|---|---|---|
| Total, after SFT | +2.7 [+0.9, +4.5]; family [+0.9, +4.6] | −2.5 [−5.2, +0.3]; family [−6.3, +0.9] | +5.2 [+1.9, +8.3] |
| Format | +2.7 [+1.2, +4.2]; family [+0.9, +4.5] | +0.1 [−2.4, +2.5]; family [−3.1, +3.2] | +2.6 [−0.2, +5.4] |
| Writing | +0.0 [−1.5, +1.3]; family [−1.9, +1.6] | −2.5 [−4.3, −1.0]; family [−4.9, −0.5] | +2.6 [+0.4, +4.8] |

The total reproduces the pre-specified H1 interval exactly (the same draws). On test the whole lead is format: the
two policies write equally well against their own gold memory. Per question type on test, total = format + writing
is +11.2 = +11.1 + 0.1 for default probes, +25.8 = +26.1 − 0.4 for boundary probes, −2.4 = −1.6 − 0.8 for target
and −1.4 = −2.2 + 0.8 for neighbor probes; for scoped-exception questions it is +4.3 = +4.5 − 0.2. The family
intervals on test are about as wide as the episode intervals, so the test result does not rest on a few attributes.

### Dev against test

- The splits share no attribute, but their mixes are close (Table 6 of `tables.md`): target, default and neighbor
  probes make up the same shares; boundary probes are 2.4% of dev and 4.3% of test, scoped-exception questions 23.8%
  and 27.5%, exception-revision events 24.4% and 19.1%.
- The mix explains little. Dev reweighted to test's mix of question types gives −1.8 [−4.7, +1.0], to test's mix of
  QA groups −2.2 [−5.1, +0.5]; test with dev's mixes gives +2.4 and +2.7.
- Both parts moved by the same amount (+2.6 each). The format pattern by question type has the same sign on both
  splits (default +5.3 on dev and +11.1 on test, boundary +14.3 and +26.1, target −2.5 and −1.6, neighbor −2.4 and
  −2.2); on dev the gains and losses cancel. The writing loss is a dev effect: −2.5 there, +0.0 on test.
- The difference varies strongly between attributes (`fig5_attributes`): per attribute it ranges from −33.3 to
  +12.8 points on dev (SD 10.3; scope ahead in 9 of 28) and from −9.9 to +13.2 on test (SD 4.9; scope ahead in 20).
  On dev the four lowest attributes (calendar alert title visibility −33.3, saved-search alert grouping −27.5, desk
  cable arrangement −19.4, short work break activity −15.4) lose 34.7 probes net, more than the whole dev deficit
  (28.7). In the first two it is writing (−23.3 and −24.5), in the other two format (−19.4 and −14.8).
- Teacher-forced (below), the dev writing loss sits in new scoped exceptions: events handled exactly right 94.4% for
  CRUD against 84.7% for scope (−9.7 [−13.6, −5.4]) on dev, 78.5% against 79.8% (+1.3 [−2.8, +5.1]) on test.

Reading: dev and test are two samples of 28 attributes each, and the arms' difference depends strongly on the
attribute, so a sign flip between two such samples is not surprising. What both splits agree on is the pattern by
question type: the scope format reads better on default and boundary probes and slightly worse on target and neighbor
probes. Whether that nets out positive depends on the attributes and the mix. The test numbers are the reported
result; the dev comparison qualifies how far they generalise.

### Teacher-forced write metrics (diagnostic)

`mechanism` re-scores every SFT output with the evaluator's teacher-forced rules (each event's output applied to the
gold memory before it); its counts equal each run's stored `eval_tf_<arm>.json`. It adds whether the operation
structure matches gold. These metrics read memory with the rule readers, so they describe the write policies and are
not results. Test, three seeds pooled (3,573 events per arm), in %:

| Metric | CRUD | Scope | Scope − CRUD |
|---|---|---|---|
| Event handled exactly right (state and decision) | 91.7 | 91.2 | −0.4 [−1.7, +0.7] |
| Operation structure matches gold | 96.1 | 95.0 | −1.1 [−2.0, −0.3] |
| General value overwritten by mistake | 0.6 | 0.3 | −0.3 [−0.6, +0.0] |
| General update missed | 6.3 | 6.5 | +0.2 [−2.4, +2.9] |
| Untouched situation record changed | 1.8 | 1.8 | +0.0 [−0.6, +0.6] |
| Write on a no-change event | 2.1 | 2.6 | +0.5 [−0.5, +1.5] |
| Clarifies when it should | 99.3 | 96.2 | −3.0 [−5.2, −1.4] |
| Output rejected by the executor | 0.0 | 0.3 | +0.3 [+0.1, +0.5] |

On test the two policies make about the same write errors. The scope policy misses more clarifications (16 of 426
against 3), and the executor rejected 10 of its outputs (for example a RETIRE of the general record or a REVISE that
changes the kind of validity). On dev the scope policy was behind on events handled exactly right (−2.4 [−3.9, −1.1]),
mostly in new scoped exceptions (above). Table 4 of `tables.md` has dev beside test and the rows per event category.

### Cost

From each run's `cost.json`, pooled over the three SFT seeds: per event the scope policy reads 884 tokens and writes
65 (CRUD 603 and 36: ×1.46 and ×1.80); per question the Answer Agent reads 461 tokens (CRUD 263, ×1.76); the memory
at a question is 248 tokens (CRUD 107, ×2.32). In the rollouts the executor rejected 11 of 3,573 scope outputs and no
CRUD output. Latency per call was not recorded; GPU-hours per run are in
[evaluation.md](evaluation.md#test-results-2026-11-24). Table 5 of `tables.md` has every condition.

### Figures

`python3 -m scope_memory.figures` (needs matplotlib) draws five figures from these reports and
`results/test_p12/report.json`, each as PDF for the report and PNG (300 dpi) for the poster, and writes `tables.md`
with the numbers behind them. CRUD is blue and scope-aware orange in every figure; differences between the arms are
drawn in black, the comparison (gold memory, dev) as hollow grey circles.

1. `fig1_main_results`: QA accuracy per condition and arm (pre-specified numbers).
2. `fig2_difference_by_group_and_type`: scope − CRUD per QA group and question type, after SFT and on gold memory
   (pre-specified numbers).
3. `fig3_format_vs_writing`: the decomposition on test and dev (post-hoc).
4. `fig4_cost`: tokens per call after SFT (post-hoc summary).
5. `fig5_attributes`: scope − CRUD per attribute on test and dev (post-hoc).

## Read-time experiments (post-hoc, 2026-11-24)

The team's mid-project update of 2026-11-24 asked for two experiments that change only what the frozen Answer Agent
reads. Both were proposed after the single test run, so they are post-hoc and exploratory: they are reported apart
from the main table, which stays as it is. Code: `scope_memory/readtime.py` (prompts and reports; standard library)
and `training/sft/reread.py` (Answer Agent runs on Babel); `training/sft/submit_readtime.sh` submits them.

The Answer Agent is the frozen one in every condition: Qwen3-4B-Instruct-2507 without an adapter, greedy decoding,
batch size 16, the reply format and the 160-token budget of prompt version 3. Replies are parsed with `pick_option`
and scored as in `rollout-score`. Every probe of dev (1,170) and test (2,027) is answered.

**A, raw history.** No memory manager. The prompt holds the user's preferences at the start of the episode, as the
fixed CRUD sentences that also seed the CRUD arm's memory; then the date and the messages of every event up to and
including the probe's, oldest first; then the probe exactly as in prompt version 3. Nothing else of the events (no
gold state, category or output) and no later event enters it. In place of the memory reading rule it gets three
sentences: the conversations are in time order and a later one can change or end an earlier preference; only the
user's own lasting preferences count (one-off requests, other people's preferences and unsettled changes do not),
which is what the policy instructions tell both memory managers; and the reading rule with "preference" for "record".
The reply instruction is prompt version 3's, also with "preference" for "record". Prompts are given whole: the
longest history has about 4,500 characters, and `history_check.json` records the token counts.

Compared with SFT scope and SFT CRUD (pooled over the three seeds), the gold memory of both arms and, on test, the
never-written memory: paired differences per group with episode and family intervals; per seed, the probes that only
the history gets right and those that only the memory gets right; and the tokens of one run (a memory arm: every
policy call on every event plus every Answer Agent call; the history: its Answer Agent calls).

**B, the display of the same memory.** For each finished scope rollout (SFT seeds 0-2 and gold memory, dev and test),
the memory at every probe is shown three ways:

- `replay`: the original prompt, answered again; this measures how much the answers change on a second run (another
  GPU type, other neighbours in a batch);
- `compact`: one block per attribute with the general preference and one line per situation with its dates
  (`; for now, with no end date given` or `; from YYYY-MM-DD through YYYY-MM-DD`); memory ids, relations and
  evidence ids are left out;
- `sentences`: the CRUD arm's own display, every record as its fixed CRUD sentence in `{"id", "text"}` records.

Nothing is repaired, selected or dropped, errors included. Leaving out the relations loses nothing the reader could
use, because every situation record points at its own attribute's general record and REPLACES points only at retired
records: `display_check.json` counts both, and both counts are 0 in all stored dev and test SFT snapshots. On gold
memory, `sentences` shows exactly the CRUD arm's gold texts (checked on all 702 dev and 1,191 test snapshots), so it
differs from the CRUD prompt only in record ids and order. Reported: the accuracy of each display, paired against the
stored original answers and against the CRUD arm per group; scope minus CRUD split into a display part (original -
sentences) and a content part (sentences - CRUD); answers lost and gained per run; replay agreement; and the tokens
of the memory block and of the prompt.

Procedure, fixed before any run:

1. Smoke: `bash ~/scope-sft-work/sft/submit_readtime.sh smoke` answers the first 5 dev episodes (A, and B on seed 0's
   memory). It checks the pipeline only: every probe answered, the "Answer:" line present, no prompt cut, prompts as
   intended, replay agreeing with the stored answers. A smoke result may change code only to fix such an error; its
   accuracies decide nothing.
2. Freeze: `runs/readtime/FROZEN` names the commit of the settings.
3. `bash ~/scope-sft-work/sft/submit_readtime.sh full` runs dev and test once (ten jobs). Every result is reported,
   whichever way it falls.

```sh
P="python3 -m scope_memory.readtime"; R=runs/readtime; T=runs/test_p12; D=runs/sft_p12_eval; O=$REPO/results/posthoc
$P a --history $R/test_history --sft ${T}_sft_s0 ${T}_sft_s1 ${T}_sft_s2 --gold ${T}_gold --noop ${T}_noop \
  --cost ${T}_sft_s0/cost.json ${T}_sft_s1/cost.json ${T}_sft_s2/cost.json --out $O/readtime_a_test.json
$P a --history $R/dev_history --sft ${D}_s0 ${D}_s1 ${D}_s2 --gold runs/reference_gold_p12 \
  --cost $R/dev_history/cost_runs.json --out $O/readtime_a_dev.json
$P b --display $R/test_sft_s0 $R/test_sft_s1 $R/test_sft_s2 $R/test_gold \
  --sft ${T}_sft_s0 ${T}_sft_s1 ${T}_sft_s2 --gold ${T}_gold --out $O/readtime_b_test.json
$P b --display $R/dev_sft_s0 $R/dev_sft_s1 $R/dev_sft_s2 $R/dev_gold \
  --sft ${D}_s0 ${D}_s1 ${D}_s2 --gold runs/reference_gold_p12 --out $O/readtime_b_dev.json
$P show --data DATA --probe EPISODE/PROBE [--run RUN --condition compact]   # print one prompt
```

### Results (2026-11-24, read-time)

Runs. The smoke ran from a staged copy of the files of `587525c` (byte-identical; WSL, where commits are made, was
busy) as jobs 11271161 and 11271162 and passed every check: all 54 probes answered in each condition, no "Answer:"
line missing, history prompts at most 1,216 tokens, replay equal to the stored answers on 54 of 54. No code changed,
and `runs/readtime/FROZEN` names `587525c`. The ten runs (11271278-11271287) finished on 2026-11-24 between 21:16
and 21:53 ET on A100, A6000, L40, L40S and RTX 6000 Ada GPUs. Two of them (test seed 1, dev seed 2) first landed on
a Blackwell node that was missing from the exclude list (babel-aa9-24; torch 2.6 has no kernels for it) and failed
before answering anything; they were resubmitted (11271408, 11271409) with all 24 such nodes excluded, which the job
scripts now list. Dev gold was preempted once and resumed; the requeue quirk later overwrote its log ("already
done"), and its result files are complete. Every probe got exactly one answer per condition; the "Answer:" line is
missing in at most 0.6% of the replies (CRUD sentences on dev: 21 of 3,510). Reports:
`results/posthoc/readtime_{a,b}_{test,dev}.json`; Figures 6 and 7 and Tables 8 and 9 in `results/figures/`.

**A, raw history.** Accuracy in %, 95% episode-bootstrap intervals, SFT pooled over the three seeds:

| | Test (2,027 questions) | Dev (1,170) |
|---|---|---|
| Raw history, no memory | 58.2 [55.7, 60.6] | 50.8 [47.5, 54.1] |
| SFT CRUD memory | 83.3 | 88.8 |
| SFT scope-aware memory | 86.1 | 86.3 |
| Gold memory, CRUD / scope-aware | 86.9 / 89.6 | 91.4 / 91.5 |
| Never-written memory, CRUD / scope-aware | 48.1 / 50.1 | |
| History − SFT CRUD | −25.2 [−28.0, −22.4] | −37.9 [−41.8, −34.2] |
| History − SFT scope-aware | −27.9 [−30.4, −25.4] | −35.5 [−39.7, −31.4] |

- Without memory, the same Answer Agent answers 58.2% of the test questions: 25-28 points below either SFT memory
  and only 8-10 points above memory that was never written. Resampling the attributes instead of the episodes gives
  about the same intervals.
- It does worst on ordinary-occasion questions (test 48.0%; the SFT memories 79.7-91.0%) and in the question groups
  of stable preferences and revised exceptions (56.1%, 53.5%). Its replies apply a situation's or a stopgap
  preference to an ordinary occasion, or take a hypothetical or one-off request for a change. On boundary questions
  it is close to CRUD (20.4% against 17.4%) and far below scope-aware (43.2%).
- Per seed on test, the memory answers 620-677 questions right that the history misses, and misses 89-124 that the
  history gets right.
- Tokens of one test run: history 1.55 M (766 per question; its prompts average 714 tokens), CRUD 1.40 M,
  scope-aware 2.17 M, counting every policy call on every event. On these short timelines (at most 8 events) the raw
  history is 11% dearer than the CRUD memory and 29% cheaper than the scope-aware memory, at a far lower accuracy.
- Limits: one small reader with one prompt written for this experiment and not tuned; a larger reader may read raw
  histories much better, and longer histories cost more per question.

**B, the display of the same memory.** Test accuracy in %:

| Scope-aware memory shown as | SFT, 3 seeds | Gold memory | Memory block, tokens (SFT) |
|---|---|---|---|
| original (the stored answers) | 86.1 | 89.6 | 315 |
| replay (the same prompt, answered again) | 86.1 | 89.6 | 315 |
| compact | 83.1 | 87.4 | 58 |
| CRUD sentences | 82.8 | 86.9 | 116 |
| (the CRUD arm's memory, its own display) | 83.3 | 86.9 | |

- Replay: answering the original prompts again gives the stored answer on 99.7% of the SFT probes (gold 98.7%; dev
  99.7% and 99.9%), and the accuracy moves by at most 0.1 point, so the differences below are effects of the display.
- Compact cuts the memory block by 82% and the prompt from 461 to 205 tokens, but costs accuracy against the replay:
  test SFT −3.0 [−4.3, −1.6], gold −2.3 [−3.6, −1.0]; dev −2.2 [−4.4, +0.3] and −2.6 [−5.0, −0.1]. The loss sits in
  boundary questions (test SFT 42.8 with the replay, 15.2 compact) and neighbouring situations (−3.9 [−5.8, −2.1]);
  ordinary-occasion and target questions are unchanged. Some replies name the right rule and then give another
  line's value. This compact display is therefore not a free saving.
- As CRUD sentences, the scope-aware memory is read no better than the CRUD memory: test SFT −0.5 [−2.2, +1.1], gold
  +0.1 [−1.2, +1.1]. Scope minus CRUD on test (+2.7) thus splits into display (original − sentences) +3.2 [+1.9,
  +4.5] and content (sentences − CRUD) −0.5 [−2.2, +1.1]: measured on the SFT memories themselves, the lead is the
  display, as the decomposition with gold memory suggested. It sits in ordinary-occasion questions (+10.0 [+6.9,
  +13.2]) and boundary questions (+18.9 [+10.6, +27.9]), where the explicit general record and validity fields help
  the reader.
- On dev the display helps about as much (SFT +2.0 [−0.4, +4.2]; gold +2.5 [+0.3, +4.7]), but under the same display
  the scope-aware memory is behind CRUD's (−4.4 [−6.6, −2.3]). Part of this is record order: on dev gold memory, the
  very same sentences in the scope-aware arm's order (a revised record moves to the end) are read 2.4 points worse
  than in the CRUD arm's order ([−4.1, −0.9]; test +0.1 [−1.2, +1.1]), so the content part also holds an order
  effect.

In short: with this reader both memories beat the raw history by 25-38 points; the structured scope-aware display is
worth about 2-3 points on both splits, while what the scope-aware policy writes is no better than CRUD's on test and
worse on dev; and the compact display trades 2-3 points for 82% fewer memory tokens.

## Larger reader (post-hoc, dev only, 2026-11-25)

Experiments A and B used one small reader. To see whether their readings depend on it, the dev runs are answered
again by a larger reader with nothing else changed: Qwen3-30B-A3B-Instruct-2507 (the same 2507 instruct line,
non-thinking only, 30.5 B parameters of which 3.3 B are active; the revision and every file's size and hash are pinned
in `training/sft/bigreader_model.json`), prompt version 3, greedy decoding, the 160-token reply budget, batch size 64.
The test split stays read once: dev only. The model is read from a Hugging Face cache on the cluster's shared storage
when one holds the pinned revision, and is otherwise downloaded into node scratch for each job, checked file by file
and deleted afterwards (`training/sft/bigreader.sbatch`). On 2026-11-25 every 80 GB GPU of the cluster was held by
long jobs, so each job uses two 48 GB GPUs: `training/sft/spread.py` puts the first 24 decoder layers (with the
embeddings, the final norm and the output layer) on one and the other 24 on the other.

Placement on two GPUs (2026-11-25/26). The first smoke job let accelerate spread the layers (`device_map="auto"`),
which copies hidden states directly from one GPU to the other. Every reply came back as garbage ("!!!!" runs and
repeated tokens; none of the 216 replies had the "Answer:" line), and at about 18 minutes per batch of 32 the job hit
its 3-hour limit; the downloaded model files had passed the hash check. `training/sft/spread_check.py`, run as the
first unit of the second smoke job (two L40S GPUs of another node), shows why: the driver reports peer access between
the two GPUs, yet all 40 direct GPU-to-GPU copies of random tensors differed from the source, while all 20 copies
through host memory were exact. `spread.py` therefore removes accelerate's hooks and copies every tensor that crosses
between the GPUs through host memory. It also replaces transformers' loop over the experts of each Qwen3-MoE block,
which waits for the GPU twice per expert, by the same loop with the routing sorted once per layer, so the same
experts run on the same tokens in the same order. The check compared the two on the block inputs of layers 0, 23, 24
and 47 (the prefill of four history prompts and one decode step: 8 of 8 outputs equal bit for bit) and generated 24
greedy tokens for those prompts with each (identical tokens; 6.0 s against 8.6 s). The model copy on shared storage
(a Hugging Face cache at the pinned revision) matched the manifest in all 24 files. The check then
answered 128 dev history prompts at batch size 64 in 113 s (0.88 s per reply, against about 39 s in the first smoke,
whose replies also ran to the full 160 tokens), every reply with the "Answer:" line, using at most 36.7 of 44.4 GiB
per GPU; batch size 128 ran out of GPU memory. The garbled first smoke is kept as
`runs/bigreader_qwen3-30b-a3b-instruct-2507_smoke_garbled/` and enters no result.

Runs (`training/sft/submit_bigreader.sh`; run root `runs/bigreader_qwen3-30b-a3b-instruct-2507/`):

- `sft_p12_eval_s{0,1,2}` and `reference_gold_p12`: both arms' stored dev memories (the same files as before)
  answered by the larger reader (`baseline.py --from-run ... --answer-model`);
- `readtime/dev_history`: A with the larger reader;
- `readtime/dev_sft_s{0,1,2}` and `readtime/dev_gold`: B with the larger reader.

The directory names match the source runs, so the reports are made exactly as for A and B (`readtime a` and
`readtime b` on these directories) and shown next to the 4B numbers. `display_check.json` of these runs compares the
replay with the 4B reader's stored answers; the report's replay agreement compares it with the larger reader's own.

Readings, fixed before any run (dev; 4B values in brackets; intervals are reported with every number):

- A holds if the raw history stays at least 10 points below each SFT memory (4B: −37.9 against CRUD, −35.5 against
  scope); a gap under 5 points to either would make A's result mostly a property of the small reader.
- The display reading of B holds if the display part (original − sentences) is positive for both SFT and gold memory
  (4B: +2.0, +2.5) and the content part (sentences − CRUD) is not positive for SFT memory (4B: −4.4).
- The cost of the compact display holds if compact − replay is negative for both SFT and gold memory (4B: −2.2, −2.6).

Procedure: `submit_bigreader.sh smoke` runs one job: the check above, then the first 5 dev episodes answered three
ways (gold memory, A, and B on seed 0's memory) to check the pipeline only (every probe answered, the "Answer:" line
present, no prompt cut, the prompts equal to the ones the repository builds) and to measure the speed. The second
smoke (2026-11-26) passed all of these: 324 answers, none without the "Answer:" line, no reply at the token budget.
After the smoke, `SMOKE_PASSED` in the run root names the commit, and `submit_bigreader.sh full` submits the nine dev
units once, in four jobs (one per SFT seed with its memories and its displays; one with gold memory, its displays and
the raw history). Every result is reported, whichever way it falls.
