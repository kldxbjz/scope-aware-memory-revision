# Offline CPU SFT preflight (prepared, actual dependencies unavailable here)

Run with an explicitly provided local fast tokenizer, no downloads:

```sh
python scope_revision_sft_preflight/preflight.py --corpus scope_revision_training --tokenizer /existing/local/tokenizer --max-length 2048
```

Current protocol is deliberately scoped: raw JSON prompt, newline, raw target JSON, explicit tokenizer EOS. No chat template, packing, model loading, GPU, training, or installs. The selected tokenizer must be approved separately and available locally. It uses the installed **actual TRL DataCollatorForLanguageModeling**, rejects token-boundary straddling and overlength rather than silently truncating, inspects every single sample plus longest examples from both arms in a padded batch, validates EOS/prompt/padding labels and exact prompt parity. For versions exposing completion_only_loss it supplies completion_mask; newer versions receive prebuilt labels. Installed version strings are emitted, and mismatches fail rather than pass silently.

This is a COLLATOR-ONLY preflight, not SFTTrainer integration. The actual trainer preprocessing, chosen model chat template, model loss/shift execution, model context limit, and training adapter still need separate validation before training. A successful output explicitly says PASS_COLLATOR_ONLY. `--max-length` is a requested limit, not a verified model capacity.

Official API checked when preparing:
- https://huggingface.co/docs/trl/sft_trainer
- https://raw.githubusercontent.com/huggingface/trl/main/trl/trainer/sft_trainer.py

Current upstream main accepts prebuilt labels and masks padding. APIs evolve, so installed behavior is checked directly. No source code from upstream is installed by this script.

Locally executed: source-only parity for 160 paired records; Python compile; three dependency-free unit tests. These use a toy character tokenizer only to test guard/mask algebra, NOT to claim tokenizer or TRL success. Torch, transformers, TRL, and tokenizers are unavailable in this workspace; the real-tokenizer/collator path has NOT been executed.
