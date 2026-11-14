# Learning Scope-Aware Memory Revision for Evolving User Preferences

Research project scaffold for a three-person final-project team. No implementation, training, or experiments have been launched.

## Research question
How should an AI agent revise stored preferences when a new statement is a contextual exception rather than a global preference change?

## Planned comparison
- **Baseline:** an SFT-trained generic CRUD memory manager with Add, Update, Delete, and No-op actions.
- **Proposed:** an SFT-trained scope-aware memory manager that also represents preference scope and relationships between memories.
- **Optional extension:** reinforcement learning, only after the SFT study is feasible and separately planned.

## Candidate data approach (not yet decided)
The team initially considered HorizonBench but has not established that it supplies sufficient contextual exceptions or structured revision labels. One proposed alternative is to generate structured preference timelines and ground-truth revision labels first, then verbalize them as natural conversations. Short event-based episodes may be sufficient; this remains a feasibility question, not an accepted dataset protocol.

## Evaluation plan
Chronologically replay each timeline and evaluate preference question answering and false overwriting. Distinguish global changes, contextual exceptions, and unchanged preferences. Before implementation, define scope representation, action-label semantics, train/dev/test splits, and the false-overwrite denominator. Keep evaluation timelines held out from training and retain provenance for synthetic examples.

## Open decisions
1. Existing dataset versus synthetic timelines, and how to validate label quality.
2. Whether short episodes sufficiently test scope and long-term revision.
3. Matching model, training data, and evaluation conditions across both managers.
4. A manageable alternative learning task if reliable action supervision is unavailable.

## Feedback status
The TA has acknowledged receipt and plans to review the proposal. No substantive dataset or method recommendation has been received in the supplied reply. Private correspondence is kept locally outside version control.

## Repository hygiene
Do not commit raw correspondence, credentials, generated datasets, model weights, checkpoints, or experiment outputs. This repository presently contains planning documentation only.
