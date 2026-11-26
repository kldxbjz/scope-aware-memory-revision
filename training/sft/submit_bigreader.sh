#!/bin/bash
# Larger-reader check of the read-time experiments (post-hoc, dev only; docs/analysis.md "Larger reader"): the Answer
# Agent's base model is the one in bigreader_model.json, everything else as before (prompt version 3, greedy, 160 reply
# tokens). Run on the Babel login node:
#   bash ~/scope-sft-work/sft/submit_bigreader.sh smoke   # one job: three units on 5 dev episodes (pipeline checks,
#                                                         # speed), then the full re-read of the dev gold memory
#   bash ~/scope-sft-work/sft/submit_bigreader.sh full    # the other eight units, one job each; needs SMOKE_PASSED
# Run directories, runs/bigreader_<model>/ (smoke units in runs/bigreader_<model>_smoke/):
#   sft_p12_eval_s{0,1,2}, reference_gold_p12      both arms' memories of the dev runs answered by the reader
#                                                  (baseline.py --from-run with the source run's own options)
#   readtime/dev_history                           A: the raw history
#   readtime/dev_sft_s{0,1,2}, readtime/dev_gold   B: replay, compact and CRUD sentences of the scope memory
# The names match the source runs, so scope_memory.readtime a / b take them as --sft / --gold / --display. Each job's
# units file goes to <run root>/units/; every unit directory gets a SUBMITTED marker, so nothing is submitted twice.
# BIGREADER_SBATCH adds sbatch options, e.g. two 48 GB GPUs instead of one 80 GB GPU (baseline.py then spreads the
# decoder layers over both):
#   BIGREADER_SBATCH='--gres=gpu:2 --constraint=L40S|A6000|L40|6000Ada --cpus-per-task=2 --mem=32G --time=03:00:00'
# BIGREADER_BATCH sets the batch size (default 32).
set -euo pipefail
MODE=${1:?usage: submit_bigreader.sh smoke|full}
W=/home/zichuwu/scope-sft-work/runs
M=/home/zichuwu/scope-aware-memory-revision
SFT=/home/zichuwu/scope-sft-work/sft
D=$M/training/scope_revision_v1/data
BATCH=${BIGREADER_BATCH:-32}
read -r -a EXTRA <<< "${BIGREADER_SBATCH:-}"
for f in bigreader.sbatch download_model.py bigreader_model.json baseline.py baseline.sbatch reread.py reread.sbatch; do
  [ -f "$SFT/$f" ] || { echo "missing $SFT/$f"; exit 3; }
done
grep -q -- "--answer-model" "$SFT/baseline.py" || { echo "$SFT/baseline.py has no --answer-model"; exit 3; }
grep -q READTIME_MODEL "$SFT/reread.sbatch" || { echo "$SFT/reread.sbatch has no READTIME_MODEL"; exit 3; }
NAME=$(python3 -I -c 'import json, sys; print(json.load(open(sys.argv[1]))["name"])' "$SFT/bigreader_model.json")
TAG=$(tr 'A-Z.' 'a-z_' <<< "$NAME")
R=$W/bigreader_$TAG
RS=${R}_smoke
adapters() {  # the adapter options of a finished baseline.sbatch run (--from-run wants the same settings)
  python3 -I -c 'import json, sys
a = json.load(open(sys.argv[1]))["adapters"]
print("--adapter-scope " + a["scope"] + " --adapter-crud " + a["crud"] if a["scope"] else "")' "$1/run_config.json"
}
submit() {  # submit JOB_NAME ROOT UNIT_LINE...: one job that runs these units in order
  local name=$1 root=$2 id line run units
  shift 2
  for line in "$@"; do
    run=$(awk '{print $2}' <<< "$line")
    if [ -f "$run/SUBMITTED" ]; then echo "$name: $run already submitted ($(cat "$run/SUBMITTED"))"; return; fi
  done
  mkdir -p "$root/units"
  units=$root/units/$name.txt
  printf '%s\n' "$@" > "$units"
  id=$(sbatch --parsable ${EXTRA[@]+"${EXTRA[@]}"} --job-name="$name" --output="$root/units/slurm-$name-%j.out" \
         "$SFT/bigreader.sbatch" "$units")
  for line in "$@"; do run=$(awk '{print $2}' <<< "$line"); mkdir -p "$run"; echo "$id" > "$run/SUBMITTED"; done
  echo "$name $id ($# units)"
}
case "$MODE" in
  smoke)
    submit br-smoke "$RS" \
      "baseline $RS/reference_gold_p12 --policy gold --limit 5 --batch-size $BATCH" \
      "reread $RS/readtime/dev_history --history --episodes $D/dev.jsonl --limit 5 --batch-size $BATCH" \
      "reread $RS/readtime/dev_sft_s0 --from-run $W/sft_p12_eval_s0 --limit 5 --batch-size $BATCH" \
      "baseline $R/reference_gold_p12 --from-run $W/reference_gold_p12 --policy gold --batch-size $BATCH"
    ;;
  full)
    [ -f "$R/SMOKE_PASSED" ] || { echo "no $R/SMOKE_PASSED: check the smoke first"; exit 3; }
    for k in 0 1 2; do
      submit "br-sft-s$k" "$R" \
        "baseline $R/sft_p12_eval_s$k --from-run $W/sft_p12_eval_s$k $(adapters "$W/sft_p12_eval_s$k") --batch-size $BATCH"
      submit "br-display-s$k" "$R" \
        "reread $R/readtime/dev_sft_s$k --from-run $W/sft_p12_eval_s$k --batch-size $BATCH"
    done
    submit br-history "$R" "reread $R/readtime/dev_history --history --episodes $D/dev.jsonl --batch-size $BATCH"
    submit br-display-gold "$R" "reread $R/readtime/dev_gold --from-run $W/reference_gold_p12 --batch-size $BATCH"
    ;;
  *) echo "usage: submit_bigreader.sh smoke|full"; exit 2 ;;
esac
sleep 2
squeue -u zichuwu -h -o "%i %j %T %R" | grep " br-" | sort || true
