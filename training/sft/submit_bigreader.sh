#!/bin/bash
# Larger-reader check of the read-time experiments (post-hoc; docs/analysis.md "Larger reader"): the Answer Agent's
# base model is the one in bigreader_model.json, everything else as before (prompt version 3, greedy, 160 reply
# tokens). Every job takes two 48 GB GPUs (bigreader.sbatch; spread.py splits the model by decoder layers). Run on the
# Babel login node:
#   bash ~/scope-sft-work/sft/submit_bigreader.sh smoke       # one job: the check unit (spread_check.py), then three
#                                                             # units on 5 dev episodes (pipeline checks, speed)
#   bash ~/scope-sft-work/sft/submit_bigreader.sh full        # the nine dev units in four jobs; needs SMOKE_PASSED
#   bash ~/scope-sft-work/sft/submit_bigreader.sh test        # the same nine units on test, in five jobs (2026-11-26)
#   bash ~/scope-sft-work/sft/submit_bigreader.sh challenge   # both arms' challenge-set memories, in one job
# Run directories, runs/bigreader_<model>/ (smoke units in runs/bigreader_<model>_smoke/), named as the source runs:
#   sft_p12_eval_s{0,1,2}, reference_gold_p12      both arms' memories of the dev runs answered by the reader
#                                                  (baseline.py --from-run with the source run's own options)
#   readtime/dev_history                           A: the raw history
#   readtime/dev_sft_s{0,1,2}, readtime/dev_gold   B: replay, compact and CRUD sentences of the scope memory
#   test_p12_sft_s{0,1,2}, test_p12_gold, readtime/test_{history,sft_s0,sft_s1,sft_s2,gold}: the same on test
#   challenge_p12_<hash>_sft_s{0,1,2}, challenge_p12_<hash>_gold: both arms' challenge-set memories (the challenge set
#                                                  has no read-time runs)
# The names match the source runs, so scope_memory.readtime a / b take them as --sft / --gold / --display. Each job's
# units file goes to <run root>/units/; every unit directory gets a SUBMITTED marker, so nothing is submitted twice.
# Dev jobs: br-s0, br-s1, br-s2 (one SFT seed's memories, then its displays) and br-gold (gold memory, its displays,
# then the raw history); about one hour each at the smoke's speed. Test jobs, with SPLIT=test as the source runs:
# br-t-s0, br-t-s1, br-t-s2 and br-t-gold as on dev, and the raw history in br-t-hist of its own (test has 1.7 times
# the dev questions). The challenge job br-c, with SPLIT=challenge: seeds 0, 1 and 2, then gold memory.
# BIGREADER_SBATCH adds sbatch options (e.g. --time=06:00:00); BIGREADER_BATCH sets the batch size (default 64; 128 ran
# out of memory on 48 GB GPUs with the raw history).
set -euo pipefail
MODE=${1:?usage: submit_bigreader.sh smoke|full|test|challenge}
W=/home/zichuwu/scope-sft-work/runs
M=/home/zichuwu/scope-aware-memory-revision
SFT=/home/zichuwu/scope-sft-work/sft
D=$M/training/scope_revision_v1/data
BATCH=${BIGREADER_BATCH:-64}
read -r -a EXTRA <<< "${BIGREADER_SBATCH:-}"
SPLITOPT=()  # --export=ALL,SPLIT=... for the test and challenge jobs (baseline.sbatch picks the data by SPLIT)
for f in bigreader.sbatch download_model.py bigreader_model.json baseline.py baseline.sbatch reread.py reread.sbatch \
         spread.py spread_check.py; do
  [ -f "$SFT/$f" ] || { echo "missing $SFT/$f"; exit 3; }
done
grep -q -- "--answer-model" "$SFT/baseline.py" || { echo "$SFT/baseline.py has no --answer-model"; exit 3; }
grep -q "from spread import load_reader" "$SFT/baseline.py" \
  || { echo "$SFT/baseline.py does not place the model with spread.py"; exit 3; }
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
finished() {  # finished RUN...: stop unless every source run has ALL_DONE
  local run
  for run in "$@"; do [ -f "$run/ALL_DONE" ] || { echo "$run has not finished"; exit 3; }; done
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
  id=$(sbatch --parsable ${EXTRA[@]+"${EXTRA[@]}"} ${SPLITOPT[@]+"${SPLITOPT[@]}"} --job-name="$name" \
         --output="$root/units/slurm-$name-%j.out" "$SFT/bigreader.sbatch" "$units")
  for line in "$@"; do run=$(awk '{print $2}' <<< "$line"); mkdir -p "$run"; echo "$id" > "$run/SUBMITTED"; done
  echo "$name $id ($# units)"
}
case "$MODE" in
  smoke)
    submit br-smoke "$RS" \
      "check $RS/check" \
      "baseline $RS/reference_gold_p12 --policy gold --limit 5 --batch-size $BATCH" \
      "reread $RS/readtime/dev_history --history --episodes $D/dev.jsonl --limit 5 --batch-size $BATCH" \
      "reread $RS/readtime/dev_sft_s0 --from-run $W/sft_p12_eval_s0 --limit 5 --batch-size $BATCH"
    ;;
  full)
    [ -f "$R/SMOKE_PASSED" ] || { echo "no $R/SMOKE_PASSED: check the smoke first"; exit 3; }
    for k in 0 1 2; do
      src=$W/sft_p12_eval_s$k
      submit "br-s$k" "$R" \
        "baseline $R/sft_p12_eval_s$k --from-run $src $(adapters "$src") --batch-size $BATCH" \
        "reread $R/readtime/dev_sft_s$k --from-run $src --batch-size $BATCH"
    done
    submit br-gold "$R" \
      "baseline $R/reference_gold_p12 --from-run $W/reference_gold_p12 --policy gold --batch-size $BATCH" \
      "reread $R/readtime/dev_gold --from-run $W/reference_gold_p12 --batch-size $BATCH" \
      "reread $R/readtime/dev_history --history --episodes $D/dev.jsonl --batch-size $BATCH"
    ;;
  test)
    [ -f "$R/SMOKE_PASSED" ] || { echo "no $R/SMOKE_PASSED: check the smoke first"; exit 3; }
    grep -q 'SPLIT=${SPLIT:-dev}' "$SFT/baseline.sbatch" || { echo "$SFT/baseline.sbatch cannot select test"; exit 3; }
    finished "$W"/test_p12_sft_s{0,1,2} "$W/test_p12_gold"
    SPLITOPT=(--export=ALL,SPLIT=test)
    for k in 0 1 2; do
      src=$W/test_p12_sft_s$k
      submit "br-t-s$k" "$R" \
        "baseline $R/test_p12_sft_s$k --from-run $src $(adapters "$src") --batch-size $BATCH" \
        "reread $R/readtime/test_sft_s$k --from-run $src --batch-size $BATCH"
    done
    submit br-t-gold "$R" \
      "baseline $R/test_p12_gold --from-run $W/test_p12_gold --policy gold --batch-size $BATCH" \
      "reread $R/readtime/test_gold --from-run $W/test_p12_gold --batch-size $BATCH"
    submit br-t-hist "$R" "reread $R/readtime/test_history --history --episodes $D/test.jsonl --batch-size $BATCH"
    ;;
  challenge)
    [ -f "$R/SMOKE_PASSED" ] || { echo "no $R/SMOKE_PASSED: check the smoke first"; exit 3; }
    grep -q 'challenge) DATA=' "$SFT/baseline.sbatch" || { echo "$SFT/baseline.sbatch cannot select it"; exit 3; }
    H=$(sha256sum "$M/training/challenge_v1/data/challenge.jsonl" | cut -c1-8)
    P=challenge_p12_$H
    finished "$W/${P}"_sft_s{0,1,2} "$W/${P}_gold"
    SPLITOPT=(--export=ALL,SPLIT=challenge)
    a0=$(adapters "$W/${P}_sft_s0"); a1=$(adapters "$W/${P}_sft_s1"); a2=$(adapters "$W/${P}_sft_s2")
    submit br-c "$R" \
      "baseline $R/${P}_sft_s0 --from-run $W/${P}_sft_s0 $a0 --batch-size $BATCH" \
      "baseline $R/${P}_sft_s1 --from-run $W/${P}_sft_s1 $a1 --batch-size $BATCH" \
      "baseline $R/${P}_sft_s2 --from-run $W/${P}_sft_s2 $a2 --batch-size $BATCH" \
      "baseline $R/${P}_gold --from-run $W/${P}_gold --policy gold --batch-size $BATCH"
    ;;
  *) echo "usage: submit_bigreader.sh smoke|full|test|challenge"; exit 2 ;;
esac
sleep 2
squeue -u zichuwu -h -o "%i %j %T %R" | grep " br-" | sort || true
