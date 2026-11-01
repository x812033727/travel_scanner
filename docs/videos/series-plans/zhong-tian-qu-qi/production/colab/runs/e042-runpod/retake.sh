#!/usr/bin/env bash
# e042 retake on one pod: one retry pass, always stops.
set -u
REPO="$1"
V=C:/Users/x8120/mokaair-work/videos
R=$V/zhong-tian-qu-qi-e042-dh/runpod/a/retake
export USERPROFILE=$V/_audition/runpod-first-test-20261031/home
export HOME="$USERPROFILE" PYTHON=python PYTHONUNBUFFERED=1
H3R="$REPO/.agents/skills/minimax-h3-runpod/scripts/h3r.sh"
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$H3R" stop; }
trap stop_pod EXIT
for try in 1 2; do
  echo "=== retake try $try $(date -u +%T)"
  bash "$H3R" batch --manifest "$R/retake.json" --output-dir "$R/out" --progress "$R/out/progress.json" --profile hero --keep --label e042-retake --slug zhong-tian-qu-qi-e042 || echo "exit=$?"
done
echo "have $(ls "$R"/out/*.mp4 | wc -l) retakes"
echo "=== end $(date -u +%T)"
