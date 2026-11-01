#!/usr/bin/env bash
# e040 stages 2 and 3 from the picked drafts: one pod per stage (a pod lives four hours at most),
# one retry pass, always stops the pod. Spend approved by the owner 2026-10-31.
set -u
REPO="$1"
P=C:/Users/x8120/mokaair-work/videos/zhong-tian-qu-qi-e040-dh/runpod/a/picked
export USERPROFILE=C:/Users/x8120/mokaair-work/videos/_audition/runpod-first-test-20261031/home
export HOME="$USERPROFILE" PYTHON=python PYTHONUNBUFFERED=1
H3R="$REPO/.agents/skills/minimax-h3-runpod/scripts/h3r.sh"
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$H3R" stop; }
trap stop_pod EXIT
mkdir -p "$P/st2/refined" "$P/final"
for try in 1 2; do
  for m in "$P"/st2/st2-*.json; do
    echo "=== refine $(basename "$m") try $try $(date -u +%T)"
    bash "$H3R" refine --manifest "$m" --output-dir "$P/st2/refined" --progress "$P/st2/refined/progress-$(basename "$m")" --keep --label e040-st2 || echo "exit=$?"
  done
done
echo "have $(ls "$P"/st2/refined/*.mp4 | wc -l) refined"
stop_pod
for try in 1 2; do
  todo=()
  for f in "$P"/st2/refined/*.mp4; do [ -f "$P/final/$(basename "${f%.mp4}")_1080.mp4" ] || todo+=("$f"); done
  batch=0
  while [ "${#todo[@]}" -gt 0 ]; do
    batch=$((batch + 1))
    echo "=== upscale try $try batch $batch $(date -u +%T)"
    bash "$H3R" upscale "${todo[@]:0:20}" --output-dir "$P/final" --progress "$P/final/progress-$try-$batch.json" --keep --label e040-st3 || echo "exit=$?"
    todo=("${todo[@]:20}")
  done
done
echo "have $(ls "$P"/final/*_1080.mp4 | wc -l) finals"
echo "=== end $(date -u +%T)"
