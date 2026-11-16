#!/bin/bash
#SBATCH --job-name=scope-sft
#SBATCH --account=atalwalk
#SBATCH --partition=preempt
#SBATCH --qos=preempt_qos
#SBATCH --gres=gpu:1
#SBATCH --requeue
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=08:00:00
#SBATCH --exclude=babel-z5-20,babel-l5-[16,20,28,32],babel-l9-[16,20,28,32],babel-m9-[16,20,28,32],babel-n9-20,babel-z5-[16,28,32],babel-z9-[16,20,24]
#SBATCH --output=/home/zichuwu/scope-sft-work/runs/slurm-%j.out
# LoRA SFT of one arm and one seed on the v1.1 train split with Qwen3-4B-Instruct-2507; resumes after preemption.
# Usage: LOG=/home/zichuwu/scope-sft-work/runs/NAME/ARM-sSEED; mkdir -p $LOG
#        sbatch --job-name=NAME-ARM-sSEED --output=$LOG/slurm-%j.out train.sbatch NAME ARM SEED [train_sft.py options]
# The rows are exported from the mirror into the run's own directory, so parallel jobs never share an export. The
# adapter goes to /data/user_data/zichuwu/scope-sft/ckpt/NAME-ARM-sSEED/adapter (compute nodes only); train.log,
# train_summary.json and a DONE marker go to the log directory, which the login node can read.
set -euo pipefail
NAME=${1:?usage: train.sbatch NAME ARM SEED [train_sft.py options]}
ARM=${2:?arm: scope or crud}
SEED=${3:?seed}
shift 3
MIRROR=/home/zichuwu/scope-aware-memory-revision
CODE=/home/zichuwu/scope-sft-work/sft
BIG=/data/user_data/zichuwu/scope-sft
PY=$BIG/venv-trl024/bin/python
OUT=$BIG/ckpt/$NAME-$ARM-s$SEED
LOG=/home/zichuwu/scope-sft-work/runs/$NAME/$ARM-s$SEED
export HF_HOME=$BIG/hf_home HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 TOKENIZERS_PARALLELISM=false
mkdir -p "$LOG"
[ -f "$LOG/DONE" ] && { echo "already done"; exit 0; }
{ echo "host=$(hostname) job=${SLURM_JOB_ID:-} restart=${SLURM_RESTART_COUNT:-0} options=$* $(date -Is)"
  nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
  df -h /data/user_data/zichuwu | tail -n 1; } | tee -a "$LOG/train.log"
mkdir -p "$OUT"
if [ ! -f "$OUT/sft/EXPORTED" ]; then
  rm -rf "$OUT/sft"
  (cd "$MIRROR" && "$PY" -m scope_memory.protocol export-sft training/scope_revision_v1/data/train.jsonl --out "$OUT/sft")
  touch "$OUT/sft/EXPORTED"
fi
sha256sum "$OUT/sft/train_${ARM}_sft.jsonl" | tee -a "$LOG/train.log"
"$PY" "$CODE/train_sft.py" --model "$BIG/models/Qwen3-4B-Instruct-2507" --sft-dir "$OUT/sft" --arm "$ARM" \
  --seed "$SEED" --output-dir "$OUT" "$@" 2>&1 | tee -a "$LOG/train.log"
cp "$OUT/train_summary.json" "$LOG/"
touch "$LOG/DONE"; echo "DONE $(date -Is)" | tee -a "$LOG/train.log"
