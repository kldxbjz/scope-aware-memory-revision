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

None yet.
