#!/bin/bash
# Final test-split runs of protocol 1.2, submitted once after the freeze (docs/evaluation.md, Final test evaluation).
# Run on the Babel login node: bash ~/scope-sft-work/sft/submit_test.sh
# Every run directory gets a SUBMITTED marker, so a second call submits nothing twice.
set -euo pipefail
W=/home/zichuwu/scope-sft-work/runs
M=/home/zichuwu/scope-aware-memory-revision
B=/data/user_data/zichuwu/scope-sft
SB=/home/zichuwu/scope-sft-work/sft/baseline.sbatch
NAME=sft-p12  # the frozen SFT runs whose final adapters are evaluated
grep -q "^def user_words" "$M/scope_memory/protocol.py" || { echo "the mirror is not at protocol 1.2"; exit 3; }
grep -q 'SPLIT=${SPLIT:-dev}' "$SB" || { echo "$SB cannot select the test split"; exit 3; }
for arm in scope crud; do
  for k in 0 1 2; do
    [ -f "$W/$NAME/$arm-s$k/DONE" ] || { echo "$NAME $arm-s$k has not finished"; exit 3; }
  done
done
sub() {  # sub JOB_NAME RUN_DIR [baseline.py options]
  local name=$1 run=$2 id
  shift 2
  mkdir -p "$run"
  if [ -f "$run/SUBMITTED" ]; then echo "$name exists: $(cat "$run/SUBMITTED")"; return; fi
  id=$(sbatch --parsable --export=ALL,SPLIT=test --job-name="$name" --output="$run/slurm-%j.out" "$SB" "$run" "$@") &&
    echo "$id" > "$run/SUBMITTED" && echo "$name $id"
}
sub test-noop "$W/test_p12_noop" --policy noop --reader-version 3
sub test-gold "$W/test_p12_gold" --policy gold --reader-version 3
sub test-zero-shot "$W/test_p12_zero_shot" --reader-version 3
sub test-six-shot "$W/test_p12_six_shot" --shots 6 --demo-episodes "$M/training/scope_revision_v1/data/train.jsonl" \
  --batch-size 8 --reader-version 3
for k in 0 1 2; do
  sub "test-sft-s$k" "$W/test_p12_sft_s$k" --adapter-scope "$B/ckpt/$NAME-scope-s$k/adapter" \
    --adapter-crud "$B/ckpt/$NAME-crud-s$k/adapter" --reader-version 3
done
sleep 2
squeue -u zichuwu -h -o "%i %j %T %R" | grep " test-" | sort || true
