#!/bin/bash
# Challenge set v1 runs (training/challenge_v1/README.md, evaluation plan), in two stages, on the Babel login node:
#   bash ~/scope-sft-work/sft/submit_challenge.sh references   # never-written and gold memory
#   bash ~/scope-sft-work/sft/submit_challenge.sh policies     # zero-shot, six-shot, sft-p12 seeds 0-2, once
# Run directories carry the first 8 hex digits of the data's SHA-256 (runs/challenge_p12_<hash>_*), so a data fix
# after the reference check gets new directories. The policy stage refuses until both references of the current data
# are done and the data check is recorded in runs/challenge_p12_<hash>_REFERENCES_CHECKED. Every run directory gets a
# SUBMITTED marker, so a second call submits nothing twice.
set -euo pipefail
STAGE=${1:?usage: submit_challenge.sh references|policies}
W=/home/zichuwu/scope-sft-work/runs
M=/home/zichuwu/scope-aware-memory-revision
B=/data/user_data/zichuwu/scope-sft
SB=/home/zichuwu/scope-sft-work/sft/baseline.sbatch
NAME=sft-p12  # the frozen SFT runs whose final adapters are evaluated
DATA=$M/training/challenge_v1/data/challenge.jsonl
[ -f "$DATA" ] || { echo "no challenge set on the mirror"; exit 3; }
grep -q 'challenge) DATA=' "$SB" || { echo "$SB cannot select the challenge set"; exit 3; }
H=$(sha256sum "$DATA" | cut -c1-8)
P=$W/challenge_p12_$H
echo "challenge data $H"
sub() {  # sub JOB_NAME RUN_DIR [baseline.py options]
  local name=$1 run=$2 id
  shift 2
  mkdir -p "$run"
  if [ -f "$run/SUBMITTED" ]; then echo "$name exists: $(cat "$run/SUBMITTED")"; return; fi
  id=$(sbatch --parsable --export=ALL,SPLIT=challenge --job-name="$name" --output="$run/slurm-%j.out" "$SB" "$run" "$@") &&
    echo "$id" > "$run/SUBMITTED" && echo "$name $id"
}
case "$STAGE" in
  references)
    sub ch-noop "${P}_noop" --policy noop --reader-version 3
    sub ch-gold "${P}_gold" --policy gold --reader-version 3
    ;;
  policies)
    for r in noop gold; do
      [ -f "${P}_$r/ALL_DONE" ] || { echo "challenge_p12_${H}_$r has not finished"; exit 3; }
    done
    [ -f "${P}_REFERENCES_CHECKED" ] || { echo "record the reference data check in ${P}_REFERENCES_CHECKED first"; exit 3; }
    for arm in scope crud; do
      for k in 0 1 2; do
        [ -f "$W/$NAME/$arm-s$k/DONE" ] || { echo "$NAME $arm-s$k has not finished"; exit 3; }
      done
    done
    sub ch-zero-shot "${P}_zero_shot" --reader-version 3
    sub ch-six-shot "${P}_six_shot" --shots 6 --demo-episodes "$M/training/scope_revision_v1/data/train.jsonl" \
      --batch-size 8 --reader-version 3
    for k in 0 1 2; do
      sub "ch-sft-s$k" "${P}_sft_s$k" --adapter-scope "$B/ckpt/$NAME-scope-s$k/adapter" \
        --adapter-crud "$B/ckpt/$NAME-crud-s$k/adapter" --reader-version 3
    done
    ;;
  *) echo "the stage is references or policies, not $STAGE"; exit 2 ;;
esac
sleep 2
squeue -u zichuwu -h -o "%i %j %T %R" | grep " ch-" | sort || true
