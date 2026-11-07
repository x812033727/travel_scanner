#!/usr/bin/env bash
# e903 stage-1 drafts (resume), then the live-action pilot portraits on the same pod; the pod stays up (idle stop 60 min) for the pilot review
cd /home/user/travel_scanner
KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 903 v1
W=$HOME/mokaair-work/videos/_series/zhong-tian-qu-qi/live-pilot
echo "=== portraits $(date -u +%T)"
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh images --manifest docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/live-pilot/portraits.json \
  --output-dir "$W" --progress "$W/progress-portraits.json" --keep --label live-pilot-refs
echo "=== chain done $(date -u +%T)"
