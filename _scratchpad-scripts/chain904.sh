#!/usr/bin/env bash
# after the e903 refine: e904 stage-1 drafts (up to 8 rounds of stock retries), then stop the pod
while pgrep -f "route_a_st23.sh 903" >/dev/null; do sleep 30; done
cd /home/user/travel_scanner
A=$HOME/mokaair-work/videos/zhong-tian-qu-qi-e904-dh/runpod/a
for round in 1 2 3 4 5 6 7 8; do
  KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 904 v1
  [ "$(ls "$A"/v1/out/*.mp4 2>/dev/null | wc -l)" -ge 80 ] && break
  echo "=== round $round gave up $(date -u +%T)"
done
echo "=== stop $(date -u +%T)"; bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh stop
