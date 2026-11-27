# Challenge set v1 (protocol 1.2)

Hand-written episodes that concentrate the cases where an explicit scope-aware memory should matter most and that
the v1.1 corpus leaves out or keeps rare. It answers one question left open by the dev results: the scope arm trails
CRUD by 2.5 points on dev, where both formats score the same with gold memory; does it still trail when the episodes
need more structure? The set is evaluation data only: it never enters training, prompt selection or the choice of a
checkpoint, and it does not replace the test split.

## Why a new set

The v0.2 hard pilot that protocol.md calls a challenge set cannot be used as it is: it has the old CRUD-only
free-text format, one write per history, no QA probes and 12 test instances. Its two remaining case types,
overlapping situations with precedence and several changes in one event, need protocol changes (protocol.md §10), so
they stay out of this set as well.

## Design: six stressors, four episodes each

| Stressor | What is hard | Never or rarely in v1.1 |
|---|---|---|
| `dense` | 3–4 situation-specific records for one attribute; every write must pick the right one | v1.1 has at most 2 per attribute |
| `shared` | two attributes share a situation phrase; a change to one must leave the other's record alone | no v1.1 episode shares a phrase |
| `confusable` | situations that differ in one detail (weekday / weekend mornings) | rare |
| `chain` | answers that depend on the order of changes: retire after a general update, re-add after a retirement, change the validity, then the value | short chains |
| `temporal` | windows announced before they start, windows that end, open periods that later get an end date | windows mostly start at once |
| `distractor` | no-write events about situations and values that are in memory: someone else's preference, one-off requests, hypotheticals, rejected suggestions, restatements, clarifications resolved later | weaker cues |

All episodes follow protocol 1.2 unchanged: one or two attributes, 4–8 events, one state change per event, at most one
exception per probe, and every new value or situation named by the user in a listed form. Probes use the v1.1
question wording; the four options are the gold value and the three most confusable other values (earlier values of
the probed situation, the general value, the other active records), so a mixed-up memory leads to a plausible wrong
option. Probe types keep their meaning, with two extensions: `neighbor` also covers the same situation under the other
attribute (`shared`), and `boundary` covers every date outside a window, before it starts as well as after it ends.

## Authoring rules

Same quality rules as v1.1 (docs/data-generation-prompt.md): natural dialogue with small talk, no one states a
labelling rule or names a data field, the assistant never repeats the answer or decides for the user, each event has
exactly one correct change, fictional content only (no real names, brands or places). In addition:

- Attributes, values, situation phrases and aliases share no string with the v1.1 corpus (any split) or the
  instruction example; `build.py` checks this exactly.
- Dialogues have 3, 5 or 7 messages, the user first and last, as in v1.1.
- A general update names no situation; a retirement names no new value for its situation; a new or revised exception
  never takes the current general value (that is a retirement); a new general value differs from every active
  exception of the attribute.
- The cases are written so that a careful reader labels them the same way; none is written to make either memory
  format succeed or fail.

Provenance: the dialogues and labels in `episodes/` were drafted with Claude (an LLM), independently of the
GPT-generated v1.1 corpus; `build.py` computes everything else. Two further annotators that had not written the data
labelled all 166 events blind and agree with every gold category
([annotations/challenge_label_check](../../annotations/challenge_label_check/README.md)); `samples.md` is the readable
copy for the team's own review.

## Size

24 episodes (5 with two attributes), 166 events (general update 26, new exception 32, revision 31, retirement 21,
stable preference 44, clarify 12) and 567 probes (target 170, default 124, neighbor 253, boundary 20), 87–100 per
stressor. Written exceptions: 49 persistent, 8 windows, 6 open. Every episode reaches at least 2 active exceptions
for one attribute, 19 of them 3–5. `data/manifest.json` has the counts and the SHA-256 of `data/challenge.jsonl`.

## Build and check

```sh
python3 training/challenge_v1/build.py            # writes data/challenge.jsonl, data/manifest.json, samples.md
python3 training/challenge_v1/build.py --check    # the files match a rebuild
python3 -m scope_memory.protocol check training/challenge_v1/data/challenge.jsonl
```

`build.py` replays every episode with `replay_gold` (categories, both gold projections, read-back, probe answers) and
checks the rules above, the option set of every probe, probe dates (between their event and the next one) and that
boundary probes are exactly the dates outside a window.

## Evaluation plan (fixed before any model runs on this set)

- Runs: the seven of the test split (never-written and gold references, zero-shot, six-shot, the three `sft-p12`
  seeds), Answer Agent reader 3, `SPLIT=challenge` in `training/sft/baseline.sbatch`, run directories
  `runs/challenge_p12_*`, submitted by `training/sft/submit_challenge.sh`.
- Order: the two reference runs first. Every probe that the Answer Agent gets wrong on gold memory in both arms is
  inspected; only data errors (a wrong label, a dialogue that does not say what its label says, an ambiguous
  question) are fixed, by editing `episodes/` and rebuilding, and each fix is listed below. Nothing is removed for
  being hard. Then the five policy runs, once.
- Primary: SFT scope minus SFT CRUD, Answer Agent QA pooled over the three seeds, on all probes and without boundary
  probes, with 95% episode-bootstrap intervals (`python3 -m scope_memory.analysis report`).
- Secondary: per stressor (descriptive; four episodes each), per QA group and probe type; gold scope minus gold CRUD
  (the reading side); the prompt baselines; memory classes and teacher-forced structure (diagnostic).
- Reading: on dev the gap was −2.5 [−5.2, +0.3]. If explicit structure helps where cases need it, the scope arm's
  relative accuracy is higher here than on dev; a gap at or below the dev gap means it does not help within this
  design. With 24 episodes the interval is wide, and conclusions stay limited to this controlled synthetic set.

## Data fixes after the reference runs

None. The two reference runs finished on 2026-11-17 (`runs/challenge_p12_ffeb6a87_{noop,gold}`, Answer Agent
reader 3):

| Memory | CRUD | scope |
|---|---|---|
| gold, without boundary probes | 501/547 = 91.6% | 511/547 = 93.4% |
| gold, all probes | 510/567 = 89.9% | 517/567 = 91.2% |
| gold, boundary probes only | 9/20 | 6/20 |
| never written (seed records only), all probes | 278/567 = 49.0% | 268/567 = 47.3% |

Both arms pass the 85% check on gold memory. The Answer Agent gets 25 probes wrong on gold memory in both arms
(target 9, neighbor 7, boundary 8, default 1). Each was read against its dialogues, and all 25 are Answer Agent
errors, not data errors ([reference_check.md](reference_check.md) lists them): 8 dates outside a window read
as inside it, 12 probes where the reply applied another situation's record although the general value holds,
and 5 records stored in the user's own words that the reply did not match to the question's situation or to an
option. The data stays `ffeb6a87`; `runs/challenge_p12_ffeb6a87_REFERENCES_CHECKED` records the check, and the five
policy runs were submitted once after it.

## Results (2026-11-17)

Run directories `runs/challenge_p12_ffeb6a87_*` on Babel, Answer Agent reader 3. The tables come from
`python3 -m scope_memory.analysis report`, where SFT pools the three `sft-p12` seeds per probe; intervals are 95%
episode bootstraps. Answer Agent QA in %, all 567 probes / the 547 without boundary probes:

| Condition | CRUD | scope | scope − CRUD, all probes | scope − CRUD, no boundary |
|---|---|---|---|---|
| never written (seed records) | 49.0 / 48.8 | 47.3 / 47.2 | −1.8 [−4.4, +0.7] | −1.7 [−4.3, +0.8] |
| zero-shot | 64.2 / 65.6 | 58.6 / 60.2 | −5.6 [−15.1, +2.9] | −5.5 [−15.2, +3.2] |
| six-shot | 68.6 / 70.4 | 56.3 / 57.2 | −12.3 [−22.6, −2.3] | −13.2 [−23.6, −2.9] |
| SFT, 3 seeds | 80.6 / 82.4 | 81.0 / 83.1 | **+0.4 [−2.9, +4.0]** | **+0.6 [−2.9, +4.4]** |
| gold memory | 89.9 / 91.6 | 91.2 / 93.4 | +1.2 [−2.6, +4.9] | +1.8 [−1.5, +5.2] |

Primary result: after SFT the two arms tie on this set (+0.4 [−2.9, +4.0]; without boundary probes +0.6
[−2.9, +4.4]). On dev the scope arm trailed by 2.5 [−5.2, +0.3]. The shift goes in the direction the plan names for
explicit structure helping where the cases need it, but it does not establish that:

- The interval is wide and contains the dev gap.
- The seeds disagree, which they did not on dev. Scope − CRUD is +6.7 [+1.6, +12.2] for seed 0 (CRUD 78.8, scope
  85.5), −2.8 [−8.1, +2.3] for seed 1 (81.8 vs 79.0) and −2.6 [−8.3, +3.5] for seed 2 (81.1 vs 78.5). Two of the
  three seeds reproduce the dev deficit.
- On gold memory the scope arm reads 1.2 points better here (dev: +0.1), so part of the shift is on the reading side.

Within this design, then, the scope arm's dev deficit does not grow on structure-heavy cases, and there is no evidence
that it turns into an advantage.

Secondary results (descriptive; four episodes per stressor). SFT scope − CRUD per stressor, with CRUD / scope
accuracy:

| Stressor | scope − CRUD | CRUD / scope | Note |
|---|---|---|---|
| chain | +7.3 | 82.0 / 89.4 | mostly ch-0014, where CRUD gets 49% |
| confusable | 0.0 | 72.9 / 72.9 | on gold memory scope reads 10.4 points better |
| dense | +1.0 | 88.0 / 89.0 | |
| distractor | −4.5 | 93.1 / 88.5 | gold memory −3.1 |
| shared | −0.3 | 78.7 / 78.3 | |
| temporal | −0.8 | 67.4 / 66.7 | |

By QA group the differences stay within ±2.3 points. By probe type they stay within ±3.0, except boundary at −5.0
(20 probes). SFT gains over the prompt baselines are CRUD +16.4 (zero-shot) and +12.0 (six-shot), and scope +22.5 and
+24.8; all four intervals exclude 0.

Diagnostics (rule readers and teacher forcing; not primary):

- Teacher-forced operations match gold on 85.9% of events for scope and 84.9% for CRUD (dev: 92–95% and 96–97%), so
  the harder cases cost CRUD more. CRUD's most common mismatches:
  - an UPDATE on a no-write event (18);
  - a retirement written as an UPDATE (15);
  - a new exception written as an UPDATE of another record (14).
  Scope's most common mismatch is a general update written as ADD (14) or NOOP (7).
- At the probe, memory maps exactly to the gold state on 49.8% of probes for scope and 38.7% for CRUD (dev: 80% and
  87%).
- Written values that are not a listed form (the catalog name or the user's words) rose from 3–4% on dev to 18%
  (scope) and 22% (CRUD). Words new to both models are often not copied exactly.
- Prompt baselines: the executor rejected 43 (zero-shot) and 85 (six-shot) of 166 scope outputs, against 5 and 5 for
  CRUD. Most rejections are records with a missing or invalid field: a REVISE without its target, an ADD without a
  valid attribute, or an exception without its single EXCEPTION_TO edge.
- Memory at the probes takes about 370 tokens for scope and 130 for CRUD (seed records alone: 266 and 111).

Post-hoc (2026-11-27): the same stored memories read by a larger reader (Qwen3-30B-A3B-Instruct-2507) still tie: SFT
scope − CRUD −1.1 [−4.2, +1.8] (4B reader: +0.4 [−2.9, +4.0]), gold memory +0.2 [−1.6, +2.0]
([docs/analysis.md](../../docs/analysis.md#results-on-test-and-the-challenge-set-2026-11-27)).
