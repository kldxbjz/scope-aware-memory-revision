# Training pilot v0.1 intake and CPU preflight status (2026-11-15)

Synthetic warm-start tranche only: no SFT, GPU job, model load, download, install, Slurm job or paid API call was run.

## Sources and placement
| ZIP (user-supplied) | SHA-256 | Location |
|---|---|---|
| Scope_Aware_Memory_Training_Pilot_v0.1.zip (49,326 B) | f6221ba662665f57617a27eac1f962d1ea1d4a4c3350862f0121bdb59f4031fc | `training/scope_revision_training/` (8 files), `training/scope_revision_training_audit/` (6 files) |
| Scope_Aware_Memory_CPU_Preflight.zip (4,044 B) | ab4de231f49c81c517f8b64fdad7dbd1f681f401876ff73eec00a17ebd1106fa | `training/scope_revision_sft_preflight/` (3 files) |

Files were written with exclusive create from the verified ZIPs and are byte-identical to the archives. They were first placed at the repository root and moved under `training/` in the same day's layout cleanup. No existing eval, label or fixture was changed.

Corpus: 160 records, 128 train / 32 dev, 40 per action (`set_default`, `set_exception`, `no_op`, `defer`), 40 intact contrast groups, discourse families t00-t07 train and t08-t09 dev. CRUD and scope rows share byte-identical prompts; only the completion representation differs.

The earlier 40-example smoke pilot and 24-example candidate eval are not stored in this repo. The zero-overlap cross-reference against them in `training/scope_revision_training_audit/final_report.json` was produced by the package author and could not be re-run here. A local re-run against this repo's own fictional eval texts (`annotations/blind_pilot/blind_packet.json`, 12 items; `scope_memory.paired_pilot.build()`, 6 dialogues) found no ID, metadata or exact normalized-text overlap.

## Checks run (WSL Python 3.12.3, stdlib only; commands relative to `training/`)
| Check | Result |
|---|---|
| manifest SHA-256 of the 4 JSONL files | 4/4 match |
| `python3 scope_revision_training/validate.py` | PASS |
| `python3 scope_revision_training_audit/check_transitions.py scope_revision_training` | PASS; identical to shipped `transition_report.json` |
| `audit.py` re-run (in-repo references) | every section identical to shipped `final_report.json` except `cross_reference` (40/24 references unavailable) |
| `python3 -m unittest discover -s scope_revision_training_audit -v` | 4/4 OK |
| `python3 -m unittest discover -s scope_revision_sft_preflight -v` | 3/3 OK (toy character tokenizer: mask/guard algebra only) |
| `preflight.py --corpus scope_revision_training --source-only` | `source_pair_parity: PASS`, n_each 160 |
| repository `python3 -m unittest -v` (from the root) | 21/21 OK |
| `build.py` re-run in a scratch copy | 4 JSONL + manifest byte-identical |
| independent extra checks | prompts contain only `memory` + `conversation`, no label vocabulary; CRUD targets are free-text `{id,text}` records with add/update/no_op; 100/160 target states hold two records (default plus a separate exception record); set_default never touches the exception record; at most one exception per state; zero delete examples |

Tokenizer-free size: prompt + newline + completion is at most 794 characters (CRUD) and 737 (scope); longest record `sr-fe71e6b70684` in both arms. Token counts are not measured.

Babel mirror `/home/zichuwu/scope-aware-memory-revision`: at intake the 17 package files were copied over SSH with `tar -k` (no overwrite) and their SHA-256 matched on both ends; the 24 files tracked at `fc26303` matched; `validate.py` passed on login4.

## Preflight status, recorded separately
| Stage | Status |
|---|---|
| Source pair parity (no tokenizer) | PASS |
| Collator-only: real tokenizer + installed TRL `DataCollatorForLanguageModeling` (would print `PASS_COLLATOR_ONLY`) | NOT RUN |
| Actual SFTTrainer preprocessing (dataset tokenization, completion mask, truncation, chat template) | NOT RUN; needs its own check even after a collator pass |
| Model loss/shift on the chosen model | NOT RUN |

## Blockers before the real-tokenizer preflight
1. TRL is not installed in any environment checked: WSL system Python, miniconda base and 14 conda envs; Windows `C:\Python311`, Miniconda base and `cmu-llms-hw3`, `D:\Tools\Anaconda` base and `gat`, Store Python 3.10; Babel `mlsys-fw` and `copilot-judge-pairrm`. Closest env: WSL `10605` (torch 2.9.0, transformers 4.57.1, tokenizers 0.22.1, datasets 4.3.0, accelerate 1.11.0, peft 0.17.1), missing only trl.
2. No project-designated base model, tokenizer or chat template ([sft-plan.md](sft-plan.md): model choice UNSET). Locally cached candidates needing approval: WSL `Qwen/Qwen3-4B-Instruct-2507` (weights + tokenizer), `Qwen/Qwen3.5-4B` (tokenizer + `chat_template.jinja`, no weights); Babel home cache `Qwen2.5-0.5B/1.5B/14B-Instruct` (tokenizer + config only).
3. No training entry point and no fixed per-arm task/schema instruction yet. The CRUD instruction must allow add/update/delete/no_op over multiple free-text records.
