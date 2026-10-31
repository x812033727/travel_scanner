#!/usr/bin/env bash
# route_a_st23.sh NN [SEED] [sNN:SEED ...] : route A stages 2 and 3 after the drafts are reviewed.
# Refines and upscales on one pod (twenty clips a batch), skips what exists, always stops the pod.
# Spends money: the owner approves first. A pod lives four hours at most, so a long episode may
# need a second run, which continues where this one stopped.
set -u
N=$1
SEED=${2:-${N}0000}
[ $# -ge 2 ] && shift 2 || shift 1
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(git -C "$HERE" rev-parse --show-toplevel)"
EP=$(printf '%03d' "$N")
A=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e$EP-dh/runpod/a
PYTHON=${PYTHON:-python3}; export PYTHON
H3R="$HERE/h3r.sh"
"$PYTHON" -I "$HERE/route_a_st2.py" "$REPO/docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/clips-dh-e$EP.json" "$A" "$SEED" "$@" || exit 1
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$H3R" stop; }
trap stop_pod EXIT
mkdir -p "$A/st2/refined" "$A/final"
for m in "$A"/st2/st2-*.json; do
  echo "=== refine $(basename "$m") $(date -u +%T)"
  bash "$H3R" refine --manifest "$m" --output-dir "$A/st2/refined" --progress "$A/st2/refined/progress-$(basename "$m")" \
    --keep --label "e$EP-st23" || echo "exit=$?"
done
todo=()
for f in "$A"/st2/refined/*.mp4; do
  [ -f "$A/final/$(basename "${f%.mp4}")_1080.mp4" ] || todo+=("$f")
done
batch=0
while [ "${#todo[@]}" -gt 0 ]; do
  batch=$((batch + 1))
  echo "=== upscale batch $batch $(date -u +%T)"
  bash "$H3R" upscale "${todo[@]:0:20}" --output-dir "$A/final" --progress "$A/final/progress-$batch.json" \
    --keep --label "e$EP-st23" || echo "exit=$?"
  todo=("${todo[@]:20}")
done
echo "have $(ls "$A"/final/*_1080.mp4 | wc -l) finals"
