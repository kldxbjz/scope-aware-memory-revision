#!/bin/bash
#SBATCH --job-name=scope-sft-smoke
#SBATCH --account=atalwalk
#SBATCH --partition=preempt
#SBATCH --qos=preempt_qos
#SBATCH --gres=gpu:1
#SBATCH --requeue
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --exclude=babel-z5-20,babel-l5-[16,20,28,32],babel-l9-[16,20,28,32],babel-m9-[16,20,28,32],babel-n9-20,babel-z5-[16,28,32],babel-z9-[16,20,24]
#SBATCH --output=/home/zichuwu/scope-sft-work/runs/smoke/slurm-%j.out
# Staged, resumable smoke run for protocol-v1 SFT with Qwen3-4B-Instruct-2507 (both arms).
set -euo pipefail
MIRROR=/home/zichuwu/scope-aware-memory-revision
CODE=/home/zichuwu/scope-sft-work/sft
RUN=/home/zichuwu/scope-sft-work/runs/smoke
BIG=/data/user_data/zichuwu/scope-sft
VENV=$BIG/venv-trl024
MODEL=$BIG/models/Qwen3-4B-Instruct-2507
export HF_HOME=$BIG/hf_home PIP_CACHE_DIR=/scratch/job_tmp/${SLURM_JOB_ID:-local}/pip PYTHONDONTWRITEBYTECODE=1 TOKENIZERS_PARALLELISM=false
mkdir -p "$RUN/markers" "$BIG/models" "$BIG/ckpt" "$HF_HOME"
[ -f "$RUN/markers/ALL_DONE" ] && { echo "already done"; exit 0; }
echo "host=$(hostname) job=${SLURM_JOB_ID:-} $(date -Is)"; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

stage() {  # stage NAME command...
  local name=$1; shift
  if [ -f "$RUN/markers/$name" ]; then echo "== skip $name"; return; fi
  echo "== start $name $(date -Is)"
  "$@"
  touch "$RUN/markers/$name"; echo "== done $name $(date -Is)"
}

setup_env() {
  [ -x "$VENV/bin/python" ] || "$HOME/miniconda3/envs/mlsys-fw/bin/python" -m venv --system-site-packages "$VENV"
  "$VENV/bin/pip" install --quiet "trl==0.24.0" "peft==0.17.1" > "$RUN/pip.log" 2>&1
  "$VENV/bin/python" -c "import torch, transformers, trl, peft, datasets, accelerate; print('versions', torch.__version__, transformers.__version__, trl.__version__, peft.__version__, datasets.__version__, accelerate.__version__, 'cuda', torch.cuda.is_available())" | tee "$RUN/versions.txt"
}
download_model() {
  "$VENV/bin/python" -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3-4B-Instruct-2507', local_dir='$MODEL')"
  du -sh "$MODEL" | tee "$RUN/model_size.txt"
}
export_rows() {
  (cd "$MIRROR" && "$VENV/bin/python" -m scope_memory.protocol export-sft training/scope_revision_v1/data/train.jsonl training/scope_revision_v1/data/dev.jsonl --out "$BIG/sft") | tee "$RUN/export.txt"
}
smoke_train() {
  for arm in scope crud; do
    "$VENV/bin/python" "$CODE/train_sft.py" --model "$MODEL" --sft-dir "$BIG/sft" --arm $arm --output-dir "$BIG/ckpt/smoke-$arm" --max-steps 20 | tail -n 1 | tee -a "$RUN/train_smoke.txt"
  done
}
generate_all() {
  for arm in scope crud; do
    "$VENV/bin/python" "$CODE/generate.py" --model "$MODEL" --adapter "$BIG/ckpt/smoke-$arm/adapter" --arm $arm --episodes "$MIRROR/training/scope_revision_v1/data/dev.jsonl" --limit 5 --repo "$MIRROR" --out-dir "$RUN/gen_sft"
    "$VENV/bin/python" "$CODE/generate.py" --model "$MODEL" --arm $arm --episodes "$MIRROR/training/scope_revision_v1/data/dev.jsonl" --limit 5 --repo "$MIRROR" --out-dir "$RUN/gen_base"
  done
}
evaluate_all() {
  for kind in gen_sft gen_base; do
    for arm in scope crud; do
      (cd "$MIRROR" && "$VENV/bin/python" -m scope_memory.evaluate teacher-forced --data "$RUN/$kind/episodes.jsonl" --arm $arm --predictions "$RUN/$kind/predictions_$arm.jsonl" --bootstrap 200 --out "$RUN/eval_${kind}_$arm.json" > /dev/null)
    done
  done
}

stage env setup_env
stage model download_model
stage export export_rows
stage preflight "$VENV/bin/python" "$CODE/preflight_sft.py" --model "$MODEL" --sft-dir "$BIG/sft" --out "$RUN/preflight.json"
stage train smoke_train
stage generate generate_all
stage evaluate evaluate_all
touch "$RUN/markers/ALL_DONE"; echo "ALL_DONE $(date -Is)"
