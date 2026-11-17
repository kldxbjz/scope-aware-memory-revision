# SFT and baseline scripts (Babel)

Policy base model: Qwen3-4B-Instruct-2507. Environment: a venv on top of the `mlsys-fw` conda env with `trl==0.24.0` and `peft==0.17.1` (no other packages upgraded). Large files live under `/data/user_data/zichuwu/scope-sft/` (compute nodes only); the jobs read these scripts from `~/scope-sft-work/sft/` and write logs and reports to `~/scope-sft-work/runs/`.

| File | Purpose |
|---|---|
| `sft_common.py` | load rows from `python3 -m scope_memory.protocol export-sft`, build chat prompt-completion examples, length report |
| `preflight_sft.py` | real-tokenizer preflight per arm; records the collator check and the SFTTrainer preprocessing check separately and refuses overlength rows |
| `train_sft.py` | LoRA SFT of one arm with completion-only loss, no truncation, resumable checkpoints; defaults 2 epochs, lr 1e-4, LoRA r16 / alpha 32, batch 4 × 4 accumulation; `train_summary.json` records the arm and the SHA-256 of the policy instruction in the rows |
| `train.sbatch` | one arm and one seed of `train_sft.py` on the v1.1 train split: exports the rows from the mirror into the run's own checkpoint directory, resumes after preemption, and copies `train.log`, `train_summary.json` and a `DONE` marker to `runs/NAME/ARM-sSEED/` |
| `generate.py` | greedy teacher-forced generation for a few episodes |
| `baseline.py` | policy runs for both arms: teacher-forced outputs, lockstep rollouts with each arm's own memory, Answer Agent replies. Without adapters these are the prompt baselines M0 (CRUD) and M1 (scope), and `--shots k` adds fixed train demonstrations (one event per category, the same events for both arms); SFT runs pass `--adapter-scope` and `--adapter-crud`, and each arm generates only with its own adapter, after checking that the adapter's `train_summary.json` names that arm and the current policy instruction; `--policy gold` / `--policy noop` skip the policy model and give the Answer Agent the gold memory or the never-written memory; `--reader-version N` picks the Answer Agent prompt (default 3, chosen on gold memory; see `docs/evaluation.md`), and `--from-run OLD_RUN` reuses a finished run's policy outputs so that only the Answer Agent runs again |
| `smoke.sbatch` | staged smoke run: venv, model download, export, preflight, 20-step LoRA per arm, generation, evaluation |
| `baseline.sbatch` | `baseline.py` on the full dev split (or the test split with `sbatch --export=ALL,SPLIT=test`), then scoring with `scope_memory.evaluate` and token counts with `cost_report.py`; the run directory is the first argument and further arguments go to `baseline.py` (none for zero-shot, `--shots 6 ...` for ICL, the two adapters for SFT, `--policy gold` or `--policy noop` for the reference rows) |
| `cost_report.py` | tokens and calls per arm with the policy tokenizer: policy input and output tokens per rollout event, Answer Agent input and output tokens per probe, memory tokens at the probes, rejected outputs; `--sft-rows` adds the prompt and completion tokens of exported SFT rows (`cost.json` in every run directory) |
| `submit_test.sh` | the final test-split runs (references, zero-shot, six-shot, the three `sft-p12` seeds), submitted once after the freeze in `docs/evaluation.md`; refuses to run before all six SFT runs are done |

The Answer Agent is the base model without any adapter in every condition, so differences come from the memory each policy writes. After adapter runs `baseline.py` loads a fresh copy of the base model instead of calling `get_base_model()`: PEFT injects the LoRA layers into the base model, where they stay active. The script stops if any LoRA module is present and records the check in `answer_agent.json`.

`run_config.json` records the settings and the SHA-256 of both policy instructions; a requeued job resumes only when they match, so a protocol change needs a new run directory. Exported SFT rows carry the instruction too: export again after any protocol change. `train.sbatch` exports afresh for every run.

SFT runs (protocol 1.1): `train.sbatch sft-p11 ARM SEED` for both arms and seeds 0, 1, 2, then `baseline.sbatch runs/sft_p11_eval_sSEED --adapter-scope .../ckpt/sft-p11-scope-sSEED/adapter --adapter-crud .../ckpt/sft-p11-crud-sSEED/adapter` per seed. No hyperparameter is tuned on dev.

Protocol 1.2 changes only the gold text (new values and situations in the user's words), not the policy instructions, so the instruction SHA-256 and the adapter check cannot tell 1.1 adapters from 1.2 ones: the run name carries the version (`sft-p12`). Under 1.2 the six-shot demonstrations and the gold reference change and are run again; the zero-shot baselines and the never-written reference do not depend on gold text and stay valid.

Reports in each run directory: `eval_rollout_answer_agent.json` is the primary result (Answer Agent QA, `"role": "primary"`, with memory token counts). `eval_tf_<arm>.json` and `eval_rollout_oracle_reader.json` are rule-reader diagnostics (`"role": "diagnostic"`); CRUD parse failures are listed on their own in `parse_failures` and `crud_rule_reader_parse_failure`.
