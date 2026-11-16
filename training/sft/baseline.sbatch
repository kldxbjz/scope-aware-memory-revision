#!/bin/bash
#SBATCH --job-name=scope-baseline-dev
#SBATCH --account=atalwalk
#SBATCH --partition=preempt
#SBATCH --qos=preempt_qos
#SBATCH --gres=gpu:1
#SBATCH --requeue
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=06:00:00
#SBATCH --exclude=babel-z5-20,babel-l5-[16,20,28,32],babel-l9-[16,20,28,32],babel-m9-[16,20,28,32],babel-n9-20,babel-z5-[16,28,32],babel-z9-[16,20,24]
#SBATCH --output=/home/zichuwu/scope-sft-work/runs/baseline_dev/slurm-%j.out
# M0/M1 prompt baselines on the full v1.1 dev split with Qwen3-4B-Instruct-2507 (no adapter); resumable.
set -euo pipefail
MIRROR=/home/zichuwu/scope-aware-memory-revision
CODE=/home/zichuwu/scope-sft-work/sft
RUN=/home/zichuwu/scope-sft-work/runs/baseline_dev
BIG=/data/user_data/zichuwu/scope-sft
PY=$BIG/venv-trl024/bin/python
export HF_HOME=$BIG/hf_home HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 TOKENIZERS_PARALLELISM=false
[ -f "$RUN/ALL_DONE" ] && { echo "already done"; exit 0; }
echo "host=$(hostname) job=${SLURM_JOB_ID:-} $(date -Is)"; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
"$PY" "$CODE/baseline.py" --model "$BIG/models/Qwen3-4B-Instruct-2507" --repo "$MIRROR" \
  --episodes "$MIRROR/training/scope_revision_v1/data/dev.jsonl" --out-dir "$RUN"
cd "$MIRROR"
for arm in scope crud; do
  "$PY" -m scope_memory.evaluate teacher-forced --data "$RUN/episodes.jsonl" --arm $arm \
    --predictions "$RUN/predictions_$arm.jsonl" --details "$RUN/details_$arm.jsonl" --out "$RUN/eval_tf_$arm.json" > /dev/null
done
"$PY" -m scope_memory.evaluate rollout-score --data "$RUN/episodes.jsonl" --trajectories "$RUN/trajectories.jsonl" \
  --answers "$RUN/answers.jsonl" --out "$RUN/eval_rollout_answer_agent.json" > /dev/null
"$PY" -m scope_memory.evaluate rollout-score --data "$RUN/episodes.jsonl" --trajectories "$RUN/trajectories.jsonl" \
  --out "$RUN/eval_rollout_oracle_reader.json" > /dev/null
touch "$RUN/ALL_DONE"; echo "ALL_DONE $(date -Is)"
