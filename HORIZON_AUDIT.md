# HorizonBench bounded schema audit (2026-11-14)
This is a schema/observability audit, NOT a completed semantic annotation study and NOT SFT evidence.

## Provenance
Dataset: stellalisy/HorizonBench, mental_state_graphs/test, deterministic row indices 0,1,2.
Source revision (API sha and response x-revision agreed): 50941f00f90c03a5a60219d76393869b757b835a.
Endpoint is recorded in audit_horizon.py; response hash and hashed user IDs in audit_horizon_result.json.
CC BY 4.0 per publisher dataset card. Attribute HorizonBench authors on redistribution.
Only three rows fetched (~13 MB); no parquet shards/full dataset or model calls.
Raw public synthetic profiles/dialogue remain in ignored local storage; NOT committed or sent to Babel.
All three audited users are audit/development-only. Exclude their hashes from subsequent train/validation/final-test manifests; do not call this a three-way experimental split.

## Counts and interpretation
3 users, 374 conversations, 100 unique latent change records, 307 changed-attribute instances.
Unit = user + preference structure + complete evolution-history record, deduplicated across dated snapshots.
43/100 have a later user-turn preference_expressed metadata anchor; 57/100 do not.
These metadata anchors are NOT evidence that the specific new attribute is stated or inferable.
100/100 remain ambiguous/unverified for usable observable revision labels.
0 confirmed global revision and 0 confirmed scoped exception in this *uncompleted verification*, NOT evidence that the dataset has none.
No prevalence, suitability, or performance claim is warranted from first three rows of one ordering.

## Actual schema and leakage hazard
Rows contain JSON strings user_profile, timeline_metadata, preference_record, event_record, conversations.
preference_record maps date to structures with attributes, expression_context, last_expressed_date,
original_expressed_attributes, evolution_history (date, trigger, attribute_changes).
Conversations have date, event_id and conversation.turns; turns carry role/content plus optional hidden annotations.
A changed latent snapshot may retain an earlier last_expressed_date. Neither latent date nor later annotation proves first observable evidence.
The inference adapter strips everything except date/role/content. No graph, scenarios, event IDs, annotations, gold attributes or future turns.
Replay must use a turn-index cutoff inside a conversation when labelling an action; current date-prefix helper is only for complete-session boundaries.

## Next annotation pass (required before SFT)
Select a fixed bounded subset of change records and inspect preceding evidence + subsequent prefix only.
Record the earliest exact conversation/turn evidence, scope, prior belief, changed belief, confidence, and rationale.
Double annotate global revisions, scoped exceptions, ambiguous/no observable evidence; adjudicate disagreement.
Do not infer absence of exceptions from evolution_history alone: also sample ordinary user statements.
Only observable confirmed examples enter training. Unknown evidence is an abstain/no-label, not NOOP.
Snapshot metadata supplies candidate supervision, never automatically ground truth for inference.

## Reproduce
python3 -m unittest -v
python3 audit_horizon.py PATH_TO_ROWS_RESPONSE --output audit_horizon_result.json
The script reads a saved bounded response, rejects truncated rows, and does not fetch data or call a model.
