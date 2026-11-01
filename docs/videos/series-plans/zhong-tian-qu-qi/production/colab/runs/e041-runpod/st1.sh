#!/usr/bin/env bash
# e041 route A stage 1 plus the third e040 retake on one pod: one retry pass, always stops.
# Owner 2026-11-01: finish e040, then carry on with the next episode.
set -u
REPO="$1"
V=C:/Users/x8120/mokaair-work/videos
M=$V/zhong-tian-qu-qi-e041-dh/runpod/a/st1
R=$V/zhong-tian-qu-qi-e040-dh/runpod/a/retake3
export USERPROFILE=$V/_audition/runpod-first-test-20261031/home
export HOME="$USERPROFILE" PYTHON=python PYTHONUNBUFFERED=1
H3R="$REPO/.agents/skills/minimax-h3-runpod/scripts/h3r.sh"
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$H3R" stop; }
trap stop_pod EXIT
for try in 1 2; do
  echo "=== e040 retake try $try $(date -u +%T)"
  bash "$H3R" batch --manifest "$R/retake.json" --output-dir "$R/out" --progress "$R/out/progress.json" --profile hero --keep --label e041-st1 --slug zhong-tian-qu-qi-e040 || echo "exit=$?"
  for p in "$M"/ref-e041-part*.json; do
    echo "=== $(basename "$p") try $try $(date -u +%T)"
    bash "$H3R" batch --manifest "$p" --output-dir "$M/out" --progress "$M/out/progress-$(basename "$p" .json).json" --profile hero --keep --label e041-st1 --slug zhong-tian-qu-qi-e041 || echo "exit=$?"
  done
done
echo "have $(ls "$M"/out/*.mp4 | wc -l) e041 drafts, $(ls "$R"/out/*.mp4 | wc -l) e040 retakes"
echo "=== end $(date -u +%T)"
