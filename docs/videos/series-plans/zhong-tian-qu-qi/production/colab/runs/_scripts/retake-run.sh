#!/usr/bin/env bash
# retake-run.sh NN DIR : run <runpod/a>/DIR/retake.json for episode NN, retrying every 3 min while
# RunPod has no stock (HTTP 409) or a pod died or was switched (speed-guard), until every output
# exists; 20 tries at most (then exit 1). KEEP=1 leaves the pod up for stage 2. A pod this run
# reused (started by an earlier, killed run) is never stopped by `h3r.sh batch`: stop it yourself.
set -u
EP=$(printf '%03d' "$1"); R=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e$EP-dh/runpod/a/$2
REPO="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
keep=(); [ "${KEEP:-0}" = 1 ] && keep=(--keep)
mkdir -p "$R/out"
# Read every prompt before paying (preflight-prompts.py): an ERROR stops; PREFLIGHT=0 skips it.
[ "${PREFLIGHT:-1}" = 0 ] || python3 -I "$(dirname "${BASH_SOURCE[0]}")/preflight-prompts.py" "$R/retake.json" || exit 2
for i in $(seq 1 20); do
  echo "=== try $i $(date -u +%T)"
  bash "$REPO/.agents/skills/minimax-h3-runpod/scripts/h3r.sh" batch --manifest "$R/retake.json" --output-dir "$R/out" \
    --progress "$R/out/progress.json" --profile hero "${keep[@]}" --label "e$EP-$2" --slug "zhong-tian-qu-qi-e$EP" 2>&1 | tee "$R/try.log"
  want=$(python3 -c "import json;print(len(json.load(open('$R/retake.json'))['jobs']))")
  have=$(ls "$R"/out/*.mp4 2>/dev/null | wc -l)
  [ "$have" -ge "$want" ] && { echo "=== batch done: $have of $want"; exit 0; }
  sleep 180
done
echo "=== gave up: no stock"
exit 1   # a caller looping on this must see the give-up (it used to exit 0)
