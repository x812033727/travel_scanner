#!/usr/bin/env bash
# finish the e904 stage-1 drafts (stock retries), then the e903 s06/s08 retakes on the same pod; the pod stays up for review and the refine (site idle stop 60 min)
cd /home/user/travel_scanner
A=$HOME/mokaair-work/videos/zhong-tian-qu-qi-e904-dh/runpod/a
while pgrep -f "retake-run.sh 904 v1" >/dev/null; do sleep 30; done
for round in 1 2 3 4 5 6 7 8; do
  [ "$(ls "$A"/v1/out/*.mp4 2>/dev/null | wc -l)" -ge 80 ] && break
  KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 904 v1
done
echo "=== e903 fix2 $(date -u +%T)"
KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 903 fix2
echo "=== chain done $(date -u +%T)"
