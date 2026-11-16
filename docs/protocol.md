# Memory revision protocol v1

Contract between the data generator (`training/scope_revision_v1/`), the executors and projections (`scope_memory/protocol.py`) and the evaluator (`scope_memory/evaluate.py`, see [evaluation.md](evaluation.md)). It implements sections 4–6 of the course outline v2.7, with the trims listed in section 10. The instructions given to the data generator are in [data-generation-prompt.md](data-generation-prompt.md); `fixtures/protocol_episode.json` is a complete worked episode. Version 1, 2026-11-15.

## 1. Episodes

An episode is one fictional user, one or two preference attributes and 4–8 events in date order. After every event the policy writes once (one output, possibly several operations). Two to four events per episode are followed by QA probes.

```json
{"episode_id": "tr-0001", "split": "train", "family": "commute-seat-03", "contrast_group": null,
 "attributes": [{"attribute": "train seat",
                 "options": ["aisle seat", "window seat", "quiet-car seat"],
                 "value_aliases": {"window seat": ["window"]},
                 "scopes": {"scenic": {"scope": "scenic journeys", "aliases": ["scenic routes"]}}}],
 "initial_state": {"train seat": {"general": "aisle seat", "exceptions": {}}},
 "events": [{"event_id": "e1", "date": "2027-03-02",
             "dialogue": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}],
             "gold": {"category": "scoped_exception", "decision": "resolved",
                      "state_after": {"train seat": {"general": "aisle seat",
                                      "exceptions": {"scenic": {"value": "window seat", "validity": {"kind": "persistent"}}}}},
                      "evidence_message": 3, "rationale": "..."}}],
 "probes": [{"probe_id": "p1", "after_event": "e1", "attribute": "train seat",
             "question": "Which seat should I book for the user's scenic trip on 12 March 2027?",
             "date": "2027-03-12", "situation_scope_keys": ["scenic"],
             "options": ["aisle seat", "window seat", "quiet-car seat"], "gold": "window seat",
             "category": "scoped_exception", "probe_type": "target"}]}
```

- `dialogue`: 2–8 messages, roles alternate, the user speaks first. Event dates are ISO dates and strictly increase.
- Only the event (`event_id`, `date`, `dialogue`) and the memory reach the policy. `family`, `contrast_group`, the catalogs, `gold` and `probes` are bookkeeping and evaluation data.
- `contrast_group` links two episodes that differ in one earlier user message of one event and have different gold transitions.
- `evidence_message` is the 1-based index, inside the event, of the user message that settles the decision.

## 2. Arm-neutral gold state

`{attribute: {"general": value, "exceptions": {scope_key: {"value": value, "validity": V}}}}`, where V is one of

- `{"kind": "persistent"}`
- `{"kind": "window", "from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}` (inclusive),
- `{"kind": "open"}`: stated as temporary but with no end; it stays active until revised or retired and is never turned into a lasting preference without new evidence.

Values come from the attribute's `options`; scope phrases come from its `scopes` catalog through `scope_key`.

## 3. Event categories

Exactly one per event.

| Category | Gold state change | Decision |
|---|---|---|
| `general_update` | the general value changes; exceptions untouched | resolved |
| `scoped_exception` | one new exception | resolved |
| `exception_revision` | one existing exception changes value or validity | resolved |
| `exception_retirement` | one exception is removed, so its situations inherit the general value again | resolved |
| `stable_preference` | none: one-off request, someone else's or a quoted preference, hypothetical, rejected suggestion, reaffirmation | resolved |
| `clarify` | none: the user leaves the target or the persistence genuinely open | clarify |

QA groups from outline v2.7: General Update = `general_update`; Scoped Exception = `scoped_exception`; Exception Revision = `exception_revision` and `exception_retirement`; Stable Preference = `stable_preference` and `clarify`.

## 4. Scope-aware arm

Memory view, active records only (retired records stay in the executor's audit log):

```json
{"memory_id": "m3", "attribute": "afternoon drink", "value": "decaf coffee", "scope": "exam weeks",
 "validity": {"kind": "persistent"},
 "relations": [{"type": "EXCEPTION_TO", "target": "m1"}, {"type": "REPLACES", "target": "m2"}],
 "evidence_ids": ["e3"]}
```

A general record has `"scope": "general"` and no `EXCEPTION_TO`. Output:

```json
{"decision": "resolved",
 "actions": [{"operation": "REVISE", "target_id": "m2", "value": "decaf coffee", "scope": "exam weeks",
              "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}],
              "evidence_ids": ["e3"]}]}
```

- `ADD`: `attribute`, `value`, `scope`, `validity`, `relations`, `evidence_ids`.
- `REVISE`: `target_id` plus the full new version (`value`, `scope`, `validity`, `relations`, `evidence_ids`). The executor adds `REPLACES` to the target and retires the target. Revising a general record re-points the active exceptions' `EXCEPTION_TO` to the new general record.
- `RETIRE`: `target_id`, `evidence_ids`. Only exceptions can be retired.
- `NOOP`: alone. A `clarify` decision requires exactly `[{"operation": "NOOP"}]`.

Executor rules. Any violation rejects the whole output, keeps the state and logs the reason:
a JSON object with `decision` and a non-empty `actions` list; known operations; `NOOP` only alone; targets exist, are active and appear once; non-empty `value`; `scope` is `"general"` or a non-empty phrase; well-formed validity; at most one active general record per attribute (change it with `REVISE`); every exception has `EXCEPTION_TO` to the active general record of its attribute; non-empty `evidence_ids` that name only events already seen. New ids are `m1`, `m2`, … in creation order.

## 5. CRUD arm

Memory view: `[{"id": "m1", "text": "..."}]`. Ids are opaque and texts are free text; there are no scope or relation fields. Output:

```json
{"decision": "resolved",
 "operations": [{"op": "ADD", "text": "..."}, {"op": "UPDATE", "id": "m2", "text": "..."}, {"op": "DELETE", "id": "m4"}]}
```

or `[{"op": "NOOP"}]`. Any number of records is allowed, so an exception can be its own record. Same rejection rule; ids `m1`, `m2`, … in creation order, never reused.

## 6. Gold projection

Both arms' gold outputs are computed from consecutive gold states by `scope_memory.protocol`, never written by hand:

| Change | Scope-aware | CRUD |
|---|---|---|
| general value | `REVISE` the general record | `UPDATE` its record |
| new exception | `ADD` with `EXCEPTION_TO` the general record | `ADD` |
| changed exception | `REVISE` it | `UPDATE` it |
| removed exception | `RETIRE` it | `DELETE` it |
| none | `NOOP` | `NOOP` |

CRUD sentences: `For {attribute}, the user prefers {value}.` and `For {attribute} when {scope}, the user prefers {value}.`, with ` from {from} through {to}` or ` for now, with no end date given` before the final period for window and open validity. Seed records have evidence `seed`.

## 7. Policy input and SFT rows

`{"memory": <arm view>, "event": {"event_id": ..., "date": ..., "dialogue": [...]}}`. The `event` object is byte-identical across arms; only the memory view differs. A fixed instruction per arm (`POLICY_INSTRUCTIONS` in `scope_memory/protocol.py`) precedes it. SFT rows use the gold memory (teacher forcing); rollout evaluation uses the policy's own memory. The policy never sees later events, probes or gold.

## 8. Probes and readers

A probe asks for the value in one situation on one date, as multiple choice over `options`. Gold is the value of the single active exception whose `scope_key` is in `situation_scope_keys` and whose validity covers `date`; otherwise the general value. At most one exception may apply to a probe. Probe types: `target` (the changed situation), `default` (an ordinary situation), `neighbor` (another scope of the same attribute), `boundary` (a date just outside a window).

Main metric (outline v2.7 §6): a fixed Answer Agent reads each arm's active memory and picks an option; both arms use the same agent, decoding, questions and memory token cap. The deterministic oracle reader in `scope_memory/protocol.py` maps scope phrases to the catalog (phrase or alias) and is used for data validation and pipeline tests, not as the main result.

## 9. Splits and isolation

Train, dev and test are disjoint in attributes, scope phrases, families and phrase-bank templates. Test is frozen before any prompt, checkpoint or threshold is chosen. The 40-example smoke pilot, the 24-example candidate eval, the v0.1 corpus and the v0.2 hard pilot are not used for generation; the v0.2 test split stays a separate challenge set.

## 10. Trims relative to outline v2.7

- No `SUPPORTS` relation, and no overlapping scopes or precedence rules in the generated set (the v0.2 challenge set keeps such cases).
- One state change per event; multi-record events are left to the v0.2 challenge set.
- Validity has three kinds; `status` is implicit (active records are shown, retired ones stay in the audit log).
- General preferences change immediately; there are no future-dated general updates.
- `clarify` is an explicit decision for genuinely unresolved targets, kept from the earlier pilots.
