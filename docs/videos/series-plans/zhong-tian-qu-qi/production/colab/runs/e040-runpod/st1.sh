#!/usr/bin/env bash
# Route A stage 1 for e040 on one RunPod pod: every part, then one retry pass; always stops.
set -u
REPO="$1"
M=C:/Users/x8120/mokaair-work/videos/zhong-tian-qu-qi-e040-dh/runpod/a/st1
export USERPROFILE=C:/Users/x8120/mokaair-work/videos/_audition/runpod-first-test-20261031/home
export HOME="$USERPROFILE" PYTHON=python PYTHONUNBUFFERED=1
H3R="$REPO/.agents/skills/minimax-h3-runpod/scripts/h3r.sh"
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$H3R" stop; }
trap stop_pod EXIT
for try in 1 2; do
  for p in "$M"/ref-e040-part*.json; do
    echo "=== $(basename "$p") try $try $(date -u +%T)"
    bash "$H3R" batch --manifest "$p" --output-dir "$M/out" --progress "$M/out/progress-$(basename "$p" .json).json" --profile hero --keep --label e040-st1 --slug zhong-tian-qu-qi-e040 || echo "exit=$?"
  done
done
echo "have $(ls "$M"/out/*.mp4 | wc -l) drafts"
echo "=== end $(date -u +%T)"
