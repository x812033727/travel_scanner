#!/usr/bin/env bash
# e903 stage-1 drafts (resume; up to 8 rounds of retake-run's hour of stock retries), then the live-action pilot portraits on the same pod
cd /home/user/travel_scanner
A=$HOME/mokaair-work/videos/zhong-tian-qu-qi-e903-dh/runpod/a
for round in 1 2 3 4 5 6 7 8; do
  KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 903 v1
  [ "$(ls "$A"/v1/out/*.mp4 2>/dev/null | wc -l)" -ge 80 ] && break
  echo "=== round $round gave up $(date -u +%T)"
done
W=$HOME/mokaair-work/videos/_series/zhong-tian-qu-qi/live-pilot
echo "=== portraits $(date -u +%T)"
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh images --manifest docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/live-pilot/portraits.json \
  --output-dir "$W" --progress "$W/progress-portraits.json" --keep --label live-pilot-refs
echo "=== chain done $(date -u +%T)"
