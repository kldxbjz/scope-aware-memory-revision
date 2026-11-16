# Independent CPU-only training corpus audit

Run from the workspace root:

```sh
python scope_revision_training_audit/audit.py --records scope_revision_training/inputs.jsonl --key scope_revision_training/labels.jsonl --reference scope_revision_pilot/blind.jsonl::scope_revision_pilot/intended_key.jsonl --reference scope_revision_heldout/blind.jsonl::scope_revision_heldout/authored_key.jsonl --crud scope_revision_training/crud_sft.jsonl --scope scope_revision_training/scope_sft.jsonl --out scope_revision_training_audit/final_report.json
python scope_revision_training_audit/check_transitions.py scope_revision_training
python -m unittest discover -s scope_revision_training_audit -v
```

`audit.py` checks metadata and normalized-content intersections, grouped lexical shortcut probes, exact final-turn contrasts, and paired visible-input identity. It does not treat distinct IDs as evidence of independent content. Metadata independence does not exclude semantic aliases, neighboring topics, or paraphrased templates. Shared assistant boilerplate alone is not a failure: whether it predicts the label matters.

Probes exclude neighbors sharing any available domain/family, template family, or contrast group. Each lexical trigram Jaccard nearest neighbor receives a uniform tie over the best labels, rather than arbitrary first-record wins. These are deterministic cue probes, not trained classifier results. On the old 40-record pilot the assistant-only probe correctly detects 100% label prediction, serving as a positive control. On the 160-record draft both single-view probes return 25%; this does not prove all shortcuts are absent. Inspect same-final-turn contrasts and use full-prefix versus ablated learned-model comparisons later.

`check_transitions.py` independently applies scope changes to pre-state and CRUD operations to visible free-text records. It asserts exact canonical post-state, target decision consistency, unchanged non-target state, and byte-identical prompts across arms. This validates authored target algebra, not the natural-language truth of labels. All corpus examples are synthetic; no empirical research claim follows from these checks.

Four unit tests cover normalized-content collision despite different IDs, nested conversation extraction, template exclusions, and deterministic balanced cue ties. No inputs or heldout evidence are modified.
