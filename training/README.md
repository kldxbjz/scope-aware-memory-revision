# Training material

Three packages received as ZIP archives on 2026-11-15. Their files are kept byte-identical to the archives; provenance, SHA-256 hashes and check results are in [docs/training-intake.md](../docs/training-intake.md).

| Directory | Contents |
|---|---|
| `scope_revision_training/` | 160 synthetic examples (128 train / 32 dev, 40 per action): visible inputs, gold labels, paired CRUD and scope SFT rows, deterministic generator `build.py`, validator `validate.py`, `manifest.json` with SHA-256 |
| `scope_revision_training_audit/` | CPU leakage/cue audit (`audit.py`), transition replay check (`check_transitions.py`), unit tests and the reports shipped with the package |
| `scope_revision_sft_preflight/` | offline prompt/completion collator preflight (`preflight.py`); the real-tokenizer run needs TRL and an approved local tokenizer and has not been run |

The package READMEs give commands relative to this directory:

```sh
cd training
python3 scope_revision_training/validate.py
python3 scope_revision_training_audit/check_transitions.py scope_revision_training
python3 -m unittest discover -s scope_revision_training_audit -v
python3 -m unittest discover -s scope_revision_sft_preflight -v
python3 scope_revision_sft_preflight/preflight.py --corpus scope_revision_training --source-only
```

Notes:
- `build.py` rewrites the four JSONL files and `manifest.json` in place; its output is deterministic (a re-run was byte-identical).
- `labels.jsonl` holds gold states and actions: never concatenate it into model inputs.
- The `--reference` inputs named in the audit README (the earlier 40-example smoke pilot and 24-example candidate eval) are not stored in this repository; both sets must stay out of training.
