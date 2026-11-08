#!/usr/bin/env bash
# st23-retry.sh NN SEED [sNN:SEED ...] : route_a_st23.sh, retried every 3 min while RunPod has no stock
# (HTTP 409) or a pod was reclaimed before every final exists; 30 tries at most. Skips what exists.
set -u
N=$1; EP=$(printf '%03d' "$N")
REPO="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
A=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e$EP-dh/runpod/a
want=$(python3 -c "import json;print(len(json.load(open('$REPO/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e$EP.json'))))")
for i in $(seq 1 30); do
  echo "##### try $i $(date -u +%T)"
  bash "$REPO/.agents/skills/minimax-h3-runpod/scripts/route_a_st23.sh" "$@"
  have=$(ls "$A"/final/*_1080.mp4 2>/dev/null | wc -l)
  [ "$have" -ge "$want" ] && { echo "##### done: $have finals"; exit 0; }
  sleep 180
done
echo "##### gave up: $(ls "$A"/final/*_1080.mp4 | wc -l) of $want"
