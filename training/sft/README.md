# SFT and baseline scripts (Babel)

Policy base model: Qwen3-4B-Instruct-2507. Environment: a venv on top of the `mlsys-fw` conda env with `trl==0.24.0` and `peft==0.17.1` (no other packages upgraded). Large files live under `/data/user_data/zichuwu/scope-sft/` (compute nodes only); the jobs read these scripts from `~/scope-sft-work/sft/` and write logs and reports to `~/scope-sft-work/runs/`.

| File | Purpose |
|---|---|
| `sft_common.py` | load rows from `python3 -m scope_memory.protocol export-sft`, build chat prompt-completion examples, length report |
| `preflight_sft.py` | real-tokenizer preflight per arm; records the collator check and the SFTTrainer preprocessing check separately and refuses overlength rows |
| `train_sft.py` | LoRA SFT of one arm with completion-only loss, no truncation, resumable checkpoints |
| `generate.py` | greedy teacher-forced generation for a few episodes |
| `baseline.py` | prompt baselines M0 (CRUD) and M1 (scope): teacher-forced outputs, lockstep rollouts with each arm's own memory, Answer Agent replies; `--shots k` adds fixed train demonstrations (one per event category) |
| `smoke.sbatch` | staged smoke run: venv, model download, export, preflight, 20-step LoRA per arm, generation, evaluation |
| `baseline.sbatch`, `baseline_icl.sbatch` | zero-shot and six-shot baselines on the full dev split, scored with `scope_memory.evaluate` |

The Answer Agent is the same untrained base model for every condition, so differences come from the memory each policy writes.
