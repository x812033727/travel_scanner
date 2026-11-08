#!/usr/bin/env bash
# st1-retry.sh NN : st1-ep.sh NN, retried every 3 min while RunPod has no stock (HTTP 409) or a pod
# was reclaimed before every draft exists; 30 tries at most. Drafts that exist are skipped.
set -u
N=$1; EP=$(printf '%03d' "$N")
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(git -C "$HERE" rev-parse --show-toplevel)"
A=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e$EP-dh/runpod/a
want=$(python3 -c "import json;print(len(json.load(open('$REPO/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e$EP.json'))))")
for i in $(seq 1 30); do
  echo "##### try $i $(date -u +%T)"
  bash "$HERE/st1-ep.sh" "$N"
  have=$(ls "$A"/st1/out/s[0-9][0-9].mp4 2>/dev/null | wc -l)
  [ "$have" -ge "$want" ] && { echo "##### done: $have drafts"; exit 0; }
  sleep 180
done
echo "##### gave up: $(ls "$A"/st1/out/s[0-9][0-9].mp4 | wc -l) of $want"
