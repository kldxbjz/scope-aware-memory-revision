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
