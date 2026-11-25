#!/bin/bash
# Read-time experiments A and B (scope_memory.readtime; post-hoc, docs/analysis.md). Run on the Babel login node:
#   bash ~/scope-sft-work/sft/submit_readtime.sh smoke   # dev, first 5 episodes: pipeline checks before the freeze
#   bash ~/scope-sft-work/sft/submit_readtime.sh full    # dev and test, every probe; once, after the freeze
# full needs runs/readtime/FROZEN (the commit the settings were frozen at). Every run directory gets a SUBMITTED
# marker, so a second call submits nothing twice.
set -euo pipefail
MODE=${1:?usage: submit_readtime.sh smoke|full}
W=/home/zichuwu/scope-sft-work/runs
M=/home/zichuwu/scope-aware-memory-revision
SB=/home/zichuwu/scope-sft-work/sft/reread.sbatch
D=$M/training/scope_revision_v1/data
grep -q "^def history_prompt" "$M/scope_memory/readtime.py" ||
  { echo "the mirror has no scope_memory/readtime.py"; exit 3; }
sub() {  # sub JOB_NAME RUN_DIR [reread.py options]
  local name=$1 run=$2 id
  shift 2
  mkdir -p "$run"
  if [ -f "$run/SUBMITTED" ]; then echo "$name exists: $(cat "$run/SUBMITTED")"; return; fi
  id=$(sbatch --parsable --job-name="$name" --output="$run/slurm-%j.out" "$SB" "$run" "$@") &&
    echo "$id" > "$run/SUBMITTED" && echo "$name $id"
}
case "$MODE" in
  smoke)
    R=$W/readtime_smoke
    sub rt-smoke-history "$R/dev_history" --history --episodes "$D/dev.jsonl" --limit 5
    sub rt-smoke-display "$R/dev_sft_s0" --from-run "$W/sft_p12_eval_s0" --limit 5
    ;;
  full)
    R=$W/readtime
    [ -f "$R/FROZEN" ] || { echo "no $R/FROZEN: freeze the settings first"; exit 3; }
    mkdir -p "$R/dev_history"
    [ -f "$R/dev_history/cost_runs.txt" ] || echo "$W/sft_p12_eval_s0 $W/sft_p12_eval_s1 $W/sft_p12_eval_s2" \
      > "$R/dev_history/cost_runs.txt"  # the dev SFT runs predate cost_report.py
    sub rt-dev-history "$R/dev_history" --history --episodes "$D/dev.jsonl"
    sub rt-test-history "$R/test_history" --history --episodes "$D/test.jsonl"
    for k in 0 1 2; do
      sub "rt-dev-sft-s$k" "$R/dev_sft_s$k" --from-run "$W/sft_p12_eval_s$k"
      sub "rt-test-sft-s$k" "$R/test_sft_s$k" --from-run "$W/test_p12_sft_s$k"
    done
    sub rt-dev-gold "$R/dev_gold" --from-run "$W/reference_gold_p12"
    sub rt-test-gold "$R/test_gold" --from-run "$W/test_p12_gold"
    ;;
  *) echo "usage: submit_readtime.sh smoke|full"; exit 2 ;;
esac
sleep 2
squeue -u zichuwu -h -o "%i %j %T %R" | grep " rt-" | sort || true
