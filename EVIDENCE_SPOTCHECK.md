# Six-case evidence spot-check (2026-11-14)
Single-assistant screening, NOT independent human annotation/adjudication. No population inference.

## Selection / boundary
Same three users and pinned response as HORIZON_AUDIT.md.
Within each user, sort unique candidate JSON keys (structure ID, complete change record);
choose the first with a later user annotation and first without: 3 anchored + 3 unanchored = 6.
Anchored cutoff: first later annotated user turn; unanchored cutoff: end of latent-change date.
Checked previous same-structure annotated user turns and user turns in cutoff conversation (unanchored: entire change-date sessions).
This is targeted evidence retrieval, NOT exhaustive reading of every preceding turn.
Earlier metadata/latent-event-day excerpts were also inspected as diagnostics; they do not establish labels.
No future turns after cutoff used for labels. Same-date original conversation index is a deterministic
engineering tie-break, NOT authenticated chronology. Any order-sensitive judgment remains ambiguous.
The updated visible_prefix accepts exact conversation/turn indices and has a same-date leakage regression test.

## Rubric
Lasting change: visible evidence establishes old value and explicitly/inferably replaces it persistently.
Exception: visible bounded condition changes a value while preserving an established general preference.
No change: enough evidence affirms the same preference; absence of evidence is NOT this class.
Insufficient/ambiguous: no verified old/new link, scope/duration unclear, or chronology uncertain.
Latent metadata and preference_expressed tags nominate candidates but cannot satisfy these criteria.

## Case decisions (zero-based source conversation/turn)
All 6 insufficient/ambiguous; 0 confirmed lasting changes, 0 confirmed exceptions, 0 proven no-change.
These counts concern selected graph changes, NOT all preferences in the inspected dialogue.
| Row/type | Structure | Cutoff | Why insufficient |
|---|---|---|---|
|0 anchored|advice_delivery_preferences_101|conversation130 turn22|Old checklist requests are visible. Later travel-planning action summary request does not establish checklist=False or urgent/important matrix preference.|
|0 unanchored|apology_style_preferences_376|end 2026-02-16|Earlier concern about excuses and later sponsorship-disclosure task do not establish the graph's new admission/explanation settings.|
|1 anchored|apology_style_preferences_376|conversation64 turn8|Missed-date discussion and proposed reminders do not establish qualified rather than full admission.|
|1 unanchored|advice_delivery_preferences_148|end 2025-11-07|Burnout/return-to-work context and requests for a checklist do not establish all four new ethical/format/empathy attributes.|
|2 anchored|philosophical_engagement_13|conversation32 turn8|A philosophy reading-group exchange and resonance with experience do not establish persistent shifts in three philosophical tendencies.|
|2 unanchored|empirical_evidence_integration_preferences_392|end 2025-10-29|Executive-summary acceptance is task-specific; persistent format change and preference for visual charts are not both supported.|

## Decision
Do not auto-convert these latent transitions to SFT update labels.
There may be useful task-scoped preferences in the same text, but a contextual request alone is not a
verified exception to an old general preference. Next step is a separately sampled ordinary-turn audit,
independent second annotation and adjudication. Existing three users remain audit-only.
No raw text/profiles copied into this report. Dataset coordinates allow authorized local reproduction.
A tiny fictional paired pilot is included solely to validate schema/splits/label isolation, not demonstrate learning.
Training gate: preregister annotation rubric and user/family splits, obtain independently checked examples
in BOTH update and exception strata, bound model/resources, and freeze the paired evaluation protocol.
