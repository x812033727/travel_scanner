#!/usr/bin/env bash
# retake-run.sh NN DIR : run <runpod/a>/DIR/retake.json for episode NN, retrying every 3 min while
# RunPod has no stock (HTTP 409), 20 tries at most. KEEP=1 leaves the pod up for stage 2.
set -u
EP=$(printf '%03d' "$1"); R=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e$EP-dh/runpod/a/$2
REPO="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
keep=(); [ "${KEEP:-0}" = 1 ] && keep=(--keep)
mkdir -p "$R/out"
for i in $(seq 1 20); do
  echo "=== try $i $(date -u +%T)"
  bash "$REPO/.agents/skills/minimax-h3-runpod/scripts/h3r.sh" batch --manifest "$R/retake.json" --output-dir "$R/out" \
    --progress "$R/out/progress.json" --profile hero "${keep[@]}" --label "e$EP-$2" --slug "zhong-tian-qu-qi-e$EP" 2>&1 | tee "$R/try.log"
  grep -q "started pod\|reusing pod" "$R/try.log" && { echo "=== batch done"; exit 0; }
  sleep 180
done
echo "=== gave up: no stock"
