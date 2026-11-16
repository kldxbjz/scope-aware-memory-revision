# Scope-Aware Memory Revision: chronological data v1.1

Protocol source: snapshot eee84cb, `../../docs/protocol.md`. This is the v1.1
replacement for the dataset directory in a fresh checkout; it is not a patch
to the policy, reader, evaluator, fixture, or test code. The previous v1 ZIP
is a separate release. No SFT rows, predicted writes, or model checkpoints
are shipped here.

## Build and check

Use Python 3.10+ standard library only. From the snapshot root:

```sh
python3 training/scope_revision_v1/build.py --seed 0
python3 -m unittest
python3 -m scope_memory.protocol check training/scope_revision_v1/data/train.jsonl training/scope_revision_v1/data/dev.jsonl training/scope_revision_v1/data/test.jsonl
python3 training/scope_revision_v1/validate.py
```

The generator emits UTF-8 LF `data/{train,dev,test}.jsonl`, the full audit,
a manifest with exact byte hashes and counts, and 30 seeded, human-readable
samples. The manifest does not hash itself. Keep examples in this directory,
probes, and audit artifacts out of model inputs. The protocol projects SFT
rows from successive gold states when the caller explicitly requests it.

## What changed from v1

- Event planning samples legal next writes or no-writes from the current
  state, with varied initial exception counts and 4–8 chronological events.
  Not every timeline visits every category. Some undecided choices are
  resolved later; others remain genuinely open. Existing exception revision,
  general updates that retain exceptions, retirement with inheritance, and
  validity boundaries remain covered. Every episode has 2–4 probed events.
- Exactly 30% of each split uses two distinct attributes. The two
  attributes both occur in the dialogue and state transitions, not just
  as added catalogs. Attribute-count stratification does not determine
  the number or order of labels.
- The authored split banks add colloquial references and scenario details.
  Catalog option and scope aliases map to their existing canonical values
  in both readers. Attribute shorthand is dialogue text only; protocol v1
  has no attribute alias field. The canonical attribute is still the state
  key. Both arms see the same event text.
- Comparisons retain one earlier differing user message and otherwise
  matched dialogue; scopes can be added or revised depending on the
  shared earlier memory. The pair is kept in one split.

## Audits and limitations

`data/audit.json` includes the train-fit six-way majority lookup by 1-based
event position and number of exceptions before the write. It reports both
the date-active (window endpoints included) and stored-record definitions,
with a train-global majority fallback for unseen buckets. The six-way
last-user bag-of-words diagnostic is the original train-only multinomial
naive Bayes implementation; it receives neither IDs nor memory. Both
diagnostics include a focal-contrast slice.

Class-exclusive phrases are exact normalized contiguous token sequences
in one message, counted once per event. The audit reports detailed 1–8
word statistics and checks all longer lengths exhaustively for >15%
violations using class-frequency prefix pruning. The coverage denominator
is the number of events of the only category in which the phrase occurs,
in that split. This is not a guarantee against paraphrases, shorter cues,
cross-turn shortcuts, or shortcuts combining several weak features.
Assistant-utterance diversity counts distinct normalized token sequences;
punctuation and capitalization alone do not count. Canonical attribute
mentions are matches of the complete normalized name in a dialogue event.

These checks do not establish naturalness, broad generalization, or training
readiness. 84 authored scenario families are recombined into synthetic
timelines, not independent conversations collected from people. Some
construction patterns remain, and the held-out split was audited for the
specified generation gates; use independently authored held-out families
for later external validation. The old 40-case smoke, 24-case candidate,
v0.1 and v0.2 sets are checked by exact normalized fingerprints. This
cannot prove semantic disjointness. No network, model APIs, GPU or training
were used.

## Seed-0 release results

| Split | Episodes | Events | QA probes | Two attributes | Contrast pairs |
|---|---:|---:|---:|---:|---:|
| train | 600 | 3573 | 6011 | 180 | 90 |
| dev | 120 | 702 | 1170 | 36 | 60 |
| test | 200 | 1191 | 2027 | 60 | 80 |

| Event category | train | dev | test |
|---|---:|---:|---:|
| `clarify` | 535 | 104 | 142 |
| `exception_retirement` | 449 | 70 | 155 |
| `exception_revision` | 605 | 171 | 227 |
| `general_update` | 630 | 118 | 195 |
| `scoped_exception` | 683 | 107 | 211 |
| `stable_preference` | 671 | 132 | 261 |

- Test structural diagnostic: **28.88%** (limit 35%; archived v1: 61.19%).
  Same result under both exception-count definitions; zero unseen test buckets.
- Test last-user diagnostic: **29.64%** (limit 40%; archived v1: 55.75%).
- Distinct normalized train assistant turns: **1,772**.
  17.30% of train
  events have no question mark in any assistant message.
- Full canonical attribute mention rates: train
  **17.86%**,
  dev **16.81%**,
  test **16.62%**.
- No class-exclusive contiguous phrase at any length exceeds 15% event coverage.
  Every contrast pair has the same last six dialogue messages; the deterministic
  suffix-only accuracy ceiling is 50% for the shared 1–6 message suffix.
- Longest common normalized train/test sequence spans
  8 words:
  “i want to be able to tell what”.
