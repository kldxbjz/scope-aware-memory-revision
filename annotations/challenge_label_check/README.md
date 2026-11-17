# Blind label check of the challenge set

A check of the hand-written labels in [training/challenge_v1](../../training/challenge_v1/README.md) before any model ran
on the set. Two annotators labelled every event (166) from a packet without labels, each alone; neither had written
any of the episodes. Both annotators are LLM instances (Claude), not team members, so this is a consistency check of
the labels, not the team's own audit; the team can still label `packet.md` the same way.

```sh
python3 -m scope_memory.analysis label-sample training/challenge_v1/data/challenge.jsonl --per-category 1000 \
  --seed 0 --out annotations/challenge_label_check
python3 -m scope_memory.analysis agreement --labels annotations/challenge_label_check/labels_A.json \
  annotations/challenge_label_check/labels_B.json --key annotations/challenge_label_check/key.json
```

`packet.md` shows, for every event in shuffled order, the stored preferences before it (as CRUD sentences) and the
conversation; `key.json` names the event behind each id. Each annotator chose one category from protocol §3 and wrote
in `note` what should be stored.

Result (`agreement.json`): both annotators agree with the gold category on all 166 events and with each other
(agreement 1.0, kappa 1.0). Both marked the same two `clarify` events as unsure, with `stable_preference` as the
alternative; neither changes memory, so only the decision differs. The notes name the gold value (in the catalog's or
the user's words) and, for windows, the gold dates of every write. No label was changed after the check.
