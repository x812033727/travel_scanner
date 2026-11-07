#!/usr/bin/env bash
# after the e904 refine chain: e905 stage-1 drafts (stock retries), then stop the pod
while pgrep -f chain904r.sh >/dev/null; do sleep 30; done
cd /home/user/travel_scanner
A=$HOME/mokaair-work/videos/zhong-tian-qu-qi-e905-dh/runpod/a
for round in 1 2 3 4 5 6 7 8; do
  [ "$(ls "$A"/v1/out/*.mp4 2>/dev/null | wc -l)" -ge 80 ] && break
  KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 905 v1
done
echo "=== stop $(date -u +%T)"; bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh stop
echo "=== chain done $(date -u +%T)"
