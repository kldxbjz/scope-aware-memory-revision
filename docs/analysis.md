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

One team member (Raina) labelled all 60 items alone, from the packet and a Chinese instruction sheet with the same six
categories and a recommended order of checks. Her file is `annotations/label_audit/labels_raina.json`, as received
(SHA-256 `3d162e9f…`, no notes). `agreement --labels annotations/label_audit/labels_raina.json --key
annotations/label_audit/key.json` wrote `annotations/label_audit/agreement_raina.json`: she chose the gold category
for 58 of the 60 items (96.7%; Cohen's kappa against gold 0.96). The two disagreements were checked against the
category definitions and the stored preferences shown in the packet. This check was not blind: the checker saw the
gold labels.

| Item | Source | Annotator | Gold | Reading |
|---|---|---|---|---|
| L008 | train `tr-0138` | `exception_revision` | `stable_preference` | There is no stored rule for the situation (typing without gloves), so there is nothing to revise, and the user limits the change to today ("Once this occasion is over, keep my earlier preferences"), which makes it a one-off request. Gold holds. |
| L024 | test `te-0053` | `general_update` | `exception_revision` | The stored preferences already hold a rule for lodgings used for a single night; the user changes its value and says the rest of the preferences stay. Gold holds. |

The audit therefore found no label error in 60 events (one-sided 95% upper bound 4.9%). Even if both disagreements
counted as errors, the rate would be 2 of 60 (3.3%, 95% CI 0.4–11.5%). No data were changed. A second annotator was
not available, so there is no agreement between annotators to report; the team decided on 2026-11-23 to go ahead
with one annotator.

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
