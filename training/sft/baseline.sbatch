#!/bin/bash
#SBATCH --job-name=scope-eval
#SBATCH --account=atalwalk
#SBATCH --partition=preempt
#SBATCH --qos=preempt_qos
#SBATCH --gres=gpu:1
#SBATCH --requeue
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=06:00:00
#SBATCH --exclude=babel-aa9-[16,20,24],babel-l5-[16,20,28,32],babel-l9-[16,20,28,32],babel-m9-[16,20,28,32],babel-n9-20,babel-z5-[16,20,28,32],babel-z9-[16,20,24,28]
# --exclude: every RTX PRO 6000 Blackwell node (sinfo of 2026-11-24); torch 2.6+cu124 has no kernels for them.
#SBATCH --output=/home/zichuwu/scope-sft-work/runs/slurm-%j.out
# Policy runs and scoring on the full v1.1 dev split (default), with SPLIT=test the test split, or with
# SPLIT=challenge the challenge set (training/challenge_v1), with Qwen3-4B-Instruct-2507; resumable. The test split is
# run once, after the freeze (docs/evaluation.md; submit_test.sh); the challenge set by submit_challenge.sh.
# Usage: mkdir -p RUN && sbatch [--export=ALL,SPLIT=test] --job-name=NAME --output=RUN/slurm-%j.out baseline.sbatch RUN [baseline.py options]
#   zero-shot M0/M1: no options
#   six-shot ICL:    --shots 6 --demo-episodes <mirror>/training/scope_revision_v1/data/train.jsonl --batch-size 8
#   SFT:             --adapter-scope DIR --adapter-crud DIR
#   references:      --policy gold (Answer Agent on gold memory) or --policy noop (memory never written)
#   reader:          --reader-version N picks the Answer Agent prompt; --from-run OLD_RUN plus OLD_RUN's own options
#                    reuses its policy outputs, so only the Answer Agent runs again
set -euo pipefail
RUN=${1:?usage: baseline.sbatch RUN_DIR [baseline.py options]}
shift
SPLIT=${SPLIT:-dev}
MIRROR=/home/zichuwu/scope-aware-memory-revision
case "$SPLIT" in
  dev|test) DATA=$MIRROR/training/scope_revision_v1/data/$SPLIT.jsonl ;;
  challenge) DATA=$MIRROR/training/challenge_v1/data/challenge.jsonl ;;
  *) echo "SPLIT must be dev, test or challenge, not $SPLIT"; exit 2 ;;
esac
CODE=/home/zichuwu/scope-sft-work/sft
BIG=/data/user_data/zichuwu/scope-sft
PY=$BIG/venv-trl024/bin/python
export HF_HOME=$BIG/hf_home HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 TOKENIZERS_PARALLELISM=false
mkdir -p "$RUN"
[ -f "$RUN/ALL_DONE" ] && { echo "already done"; exit 0; }
echo "host=$(hostname) job=${SLURM_JOB_ID:-} split=$SPLIT options=$* $(date -Is)"; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
"$PY" "$CODE/baseline.py" --model "$BIG/models/Qwen3-4B-Instruct-2507" --repo "$MIRROR" \
  --episodes "$DATA" --out-dir "$RUN" "$@"
cd "$MIRROR"
# Primary: eval_rollout_answer_agent.json (Answer Agent QA). Diagnostic: eval_tf_*.json, eval_rollout_oracle_reader.json.
for arm in scope crud; do
  [ -f "$RUN/predictions_$arm.jsonl" ] || continue  # reference runs have no policy outputs to score
  "$PY" -m scope_memory.evaluate teacher-forced --data "$RUN/episodes.jsonl" --arm $arm \
    --predictions "$RUN/predictions_$arm.jsonl" --details "$RUN/details_$arm.jsonl" --out "$RUN/eval_tf_$arm.json" > /dev/null
done
"$PY" -m scope_memory.evaluate rollout-score --data "$RUN/episodes.jsonl" --trajectories "$RUN/trajectories.jsonl" \
  --answers "$RUN/answers.jsonl" --answer-agent "$RUN/answer_agent.json" --tokenizer "$BIG/models/Qwen3-4B-Instruct-2507" \
  --out "$RUN/eval_rollout_answer_agent.json" > /dev/null
"$PY" -m scope_memory.evaluate rollout-score --data "$RUN/episodes.jsonl" --trajectories "$RUN/trajectories.jsonl" \
  --oracle-reader --out "$RUN/eval_rollout_oracle_reader.json" > /dev/null
# Cost: policy and Answer Agent tokens per call (docs/evaluation.md); a failure here does not fail the run.
"$PY" "$CODE/cost_report.py" --tokenizer "$BIG/models/Qwen3-4B-Instruct-2507" --repo "$MIRROR" --runs "$RUN" \
  --out "$RUN/cost.json" > /dev/null || echo "cost report failed"
touch "$RUN/ALL_DONE"; echo "ALL_DONE $(date -Is)"
