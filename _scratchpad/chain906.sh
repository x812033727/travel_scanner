#!/usr/bin/env bash
# finish the e905 drafts (stock retries), then the e906 drafts on the same pod; the pod stays up for the e905 refine (site idle stop 60 min)
cd /home/user/travel_scanner
for ep in 905 906; do
  A=$HOME/mokaair-work/videos/zhong-tian-qu-qi-e$ep-dh/runpod/a
  while pgrep -f "retake-run.sh $ep v1" >/dev/null; do sleep 30; done
  for round in 1 2 3 4 5 6 7 8; do
    [ "$(ls "$A"/v1/out/*.mp4 2>/dev/null | wc -l)" -ge 80 ] && break
    KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh $ep v1
  done
  echo "=== e$ep drafts done $(date -u +%T)"
done
echo "=== chain done $(date -u +%T)"
