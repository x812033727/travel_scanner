#!/usr/bin/env bash
# one queue on the pod: after the e906 drafts, the retake batches in order (e905 fix1, e904 fix1, e903 fix3, then e902 fix2
# when its retake.json exists); each batch writes a "=== <name> done" line. The pod stays up (KEEP) for the refines I start.
cd /home/user/travel_scanner
R=docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh
V=$HOME/mokaair-work/videos
while pgrep -f chain906.sh >/dev/null; do sleep 30; done
for job in "905 fix1" "904 fix1" "903 fix3" "902 fix2"; do
  set -- $job
  f=$V/zhong-tian-qu-qi-e$1-dh/runpod/a/$2/retake.json
  for i in $(seq 1 60); do [ -f "$f" ] && break; sleep 60; done
  [ -f "$f" ] || { echo "=== e$1 $2 skipped (no retake.json)"; continue; }
  KEEP=1 PREFLIGHT=0 bash $R $1 $2
  echo "=== e$1 $2 done $(date -u +%T)"
done
echo "=== queue done $(date -u +%T)"
