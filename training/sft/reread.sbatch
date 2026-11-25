#!/bin/bash
#SBATCH --job-name=scope-reread
#SBATCH --account=atalwalk
#SBATCH --partition=preempt
#SBATCH --qos=preempt_qos
#SBATCH --gres=gpu:1
#SBATCH --requeue
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=04:00:00
#SBATCH --exclude=babel-aa9-[16,20,24],babel-l5-[16,20,28,32],babel-l9-[16,20,28,32],babel-m9-[16,20,28,32],babel-n9-20,babel-z5-[16,20,28,32],babel-z9-[16,20,24,28]
# --exclude: every RTX PRO 6000 Blackwell node (sinfo of 2026-11-24); torch 2.6+cu124 has no kernels for them.
#SBATCH --output=/home/zichuwu/scope-sft-work/runs/slurm-%j.out
# Read-time experiments (scope_memory.readtime; post-hoc): reread.py with Qwen3-4B-Instruct-2507 as the Answer Agent;
# resumable. submit_readtime.sh submits the runs.
# Usage: mkdir -p RUN && sbatch --job-name=NAME --output=RUN/slurm-%j.out reread.sbatch RUN [reread.py options]
#   A, raw history:     --history --episodes <mirror>/training/scope_revision_v1/data/{dev,test}.jsonl
#   B, memory display:  --from-run <finished baseline.sbatch run>
# When RUN/cost_runs.txt lists baseline.sbatch runs, cost_report.py writes their token counts to RUN/cost_runs.json.
# READTIME_MIRROR and READTIME_CODE (sbatch --export=ALL,...) replace the mirror and the script folder, for a run from a
# staged copy before the code is pushed.
# READTIME_MODEL replaces the Answer Agent's base model (post-hoc runs with a larger reader; default
# Qwen3-4B-Instruct-2507).
set -euo pipefail
RUN=${1:?usage: reread.sbatch RUN_DIR [reread.py options]}
shift
MIRROR=${READTIME_MIRROR:-/home/zichuwu/scope-aware-memory-revision}
CODE=${READTIME_CODE:-/home/zichuwu/scope-sft-work/sft}
BIG=/data/user_data/zichuwu/scope-sft
MODEL=${READTIME_MODEL:-$BIG/models/Qwen3-4B-Instruct-2507}
PY=$BIG/venv-trl024/bin/python
export HF_HOME=$BIG/hf_home HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 TOKENIZERS_PARALLELISM=false
mkdir -p "$RUN"
[ -f "$RUN/ALL_DONE" ] && { echo "already done"; exit 0; }
echo "host=$(hostname) job=${SLURM_JOB_ID:-} mirror=$MIRROR code=$CODE model=$MODEL options=$* $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
"$PY" "$CODE/reread.py" --model "$MODEL" --repo "$MIRROR" --out-dir "$RUN" "$@"
if [ -f "$RUN/cost_runs.txt" ] && [ ! -f "$RUN/cost_runs.json" ]; then
  # shellcheck disable=SC2046
  "$PY" "$CODE/cost_report.py" --tokenizer "$BIG/models/Qwen3-4B-Instruct-2507" --repo "$MIRROR" \
    --runs $(cat "$RUN/cost_runs.txt") --out "$RUN/cost_runs.json" > /dev/null || echo "cost report failed"
fi
touch "$RUN/ALL_DONE"; echo "ALL_DONE $(date -Is)"
