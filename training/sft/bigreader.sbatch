#!/bin/bash
#SBATCH --job-name=scope-bigreader
#SBATCH --account=atalwalk
#SBATCH --partition=preempt
#SBATCH --qos=preempt_qos
#SBATCH --gres=gpu:1
#SBATCH --constraint=VRAM_80GB|VRAM_141GB|A100_80G
#SBATCH --requeue
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --output=/home/zichuwu/scope-sft-work/runs/slurm-%j.out
# Larger-reader check (post-hoc, dev only; docs/analysis.md): puts the reader model of bigreader_model.json on this
# node, then runs the units of UNITS_FILE one after another with it as the Answer Agent. One unit per line:
#   baseline RUN [baseline.py options]   both arms' memories answered by the reader (baseline.sbatch, --answer-model)
#   reread RUN [reread.py options]       read-time conditions answered by the reader (reread.sbatch, READTIME_MODEL)
# Units whose RUN has ALL_DONE are skipped, so a requeued job goes on where it stopped (and a finished job that the
# preempt quirk requeues does nothing).
# The model comes from a shared Hugging Face cache snapshot at the pinned revision whose blobs carry the manifest's
# hashes, or else it is downloaded into node scratch (/scratch/job_tmp/zichuwu-br, or /tmp/zichuwu-br when that is not
# writable) and checked file by file. Every job reads it as /tmp/zichuwu-br-model/NAME (a link), so a resumed run sees
# the same settings. My jobs on one node share one download (flock on ROOT/.lock; ROOT/users lists them); the last to
# leave deletes it. A job killed outright can leave a copy behind: remove those after the batch.
# Usage: sbatch --job-name=NAME --output=LOG bigreader.sbatch UNITS_FILE
set -euo pipefail
UNITS=${1:?usage: bigreader.sbatch UNITS_FILE}
CODE=${READTIME_CODE:-/home/zichuwu/scope-sft-work/sft}
BIG=/data/user_data/zichuwu/scope-sft
PY=$BIG/venv-trl024/bin/python
MAN=$CODE/bigreader_model.json
field() { "$PY" -I -c 'import json, sys; print(json.load(open(sys.argv[1]))[sys.argv[2]])' "$MAN" "$1"; }
REPO=$(field repo); REV=$(field revision); NAME=$(field name)
LINKDIR=/tmp/zichuwu-br-model
MODEL=$LINKDIR/$NAME
HOST=$(hostname -s)
echo "host=$HOST job=${SLURM_JOB_ID:-} units=$UNITS model=$REPO@${REV:0:8} $(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

mapfile -t LINES < <(grep -v -e '^[[:space:]]*#' -e '^[[:space:]]*$' "$UNITS")
todo=0
for line in "${LINES[@]}"; do
  read -r _kind run _rest <<< "$line"
  [ -f "$run/ALL_DONE" ] || todo=$((todo + 1))
done
[ "$todo" -gt 0 ] || { echo "all ${#LINES[@]} units already done"; exit 0; }

ROOT=""
prune_users() {  # drop listed jobs that no longer run on this node (keep all when squeue cannot answer)
  local running u
  running=$(squeue -h -u "$USER" -t RUNNING -o "%i %N" 2>/dev/null) || return 0
  for u in "$ROOT"/users/*; do
    [ -e "$u" ] || continue
    grep -qx "$(basename "$u") $HOST" <<< "$running" || rm -f "$u"
  done
}
cleanup() {
  [ -n "$ROOT" ] || return 0
  exec 9> "$ROOT/.lock"
  flock 9
  rm -f "$ROOT/users/${SLURM_JOB_ID:-x}"
  prune_users
  if [ -z "$(ls -A "$ROOT/users" 2>/dev/null)" ]; then
    rm -rf "${ROOT:?}/$NAME" "${ROOT:?}/hf_home"
    [ "$(readlink "$MODEL" 2>/dev/null)" = "$ROOT/$NAME" ] && rm -f "$MODEL"
    echo "removed the model copy from $ROOT on $HOST"
  else
    echo "model copy kept on $HOST for: $(ls "$ROOT/users" | tr '\n' ' ')"
  fi
  flock -u 9
}
trap cleanup EXIT
trap 'exit 143' TERM INT

shared=""
for base in /data/hf_cache/hub /data/hf_cache /data/models/hub /data/models /data/models/huggingface/hub; do
  d=$base/models--${REPO//\//--}/snapshots/$REV
  if [ -d "$d" ] && "$PY" -I "$CODE/download_model.py" --manifest "$MAN" --check-links "$d"; then shared=$d; break; fi
done
mkdir -p "$LINKDIR"
if [ -n "$shared" ]; then
  echo "using the shared copy $shared"
  [ "$(readlink "$MODEL" 2>/dev/null)" = "$shared" ] || ln -sfn "$shared" "$MODEL"
else
  mkdir -p -m 1777 /scratch/job_tmp 2>/dev/null || true
  for r in /scratch/job_tmp/zichuwu-br /tmp/zichuwu-br; do
    if mkdir -p "$r/users" 2>/dev/null && [ -w "$r" ]; then ROOT=$r; break; fi
  done
  [ -n "$ROOT" ] || { echo "no writable scratch on $HOST"; exit 1; }
  exec 9> "$ROOT/.lock"
  flock 9
  : > "$ROOT/users/${SLURM_JOB_ID:-x}"
  prune_users
  if [ ! -f "$ROOT/$NAME/DOWNLOAD_OK" ]; then
    have=$(du -s -BG "$ROOT/$NAME" 2>/dev/null | cut -f1 | tr -dc 0-9 || true); have=${have:-0}
    free=$(df --output=avail -BG "$ROOT" | tail -1 | tr -dc 0-9 || true); free=${free:-0}
    [ $((free + have)) -ge 66 ] || { echo "only ${free}G free in $ROOT on $HOST (+${have}G already there)"; exit 1; }
    echo "downloading into $ROOT/$NAME (${free}G free) $(date -Is)"
    env -u HF_HUB_OFFLINE HF_HOME="$ROOT/hf_home" HF_HUB_DISABLE_TELEMETRY=1 \
      "$PY" -I "$CODE/download_model.py" --manifest "$MAN" --dir "$ROOT/$NAME"
    echo "$REPO $REV $(date -Is)" > "$ROOT/$NAME/DOWNLOAD_OK"
  else
    echo "the model is already on $HOST: $(cat "$ROOT/$NAME/DOWNLOAD_OK")"
  fi
  [ "$(readlink "$MODEL" 2>/dev/null)" = "$ROOT/$NAME" ] || ln -sfn "$ROOT/$NAME" "$MODEL"
  flock -u 9
fi

for line in "${LINES[@]}"; do
  read -r kind run rest <<< "$line"
  if [ -f "$run/ALL_DONE" ]; then echo "== skip $run (done)"; continue; fi
  mkdir -p "$run"
  echo "== unit $kind $run $(date -Is)"
  # shellcheck disable=SC2086
  case "$kind" in
    baseline) bash "$CODE/baseline.sbatch" "$run" $rest --answer-model "$MODEL" ;;
    reread) READTIME_MODEL="$MODEL" bash "$CODE/reread.sbatch" "$run" $rest ;;
    *) echo "unknown unit kind $kind"; exit 2 ;;
  esac < /dev/null 2>&1 | tee -a "$run/bigreader_unit.log"
  echo "== unit done $run $(date -Is)"
done
echo "ALL_UNITS_DONE $(date -Is)"
