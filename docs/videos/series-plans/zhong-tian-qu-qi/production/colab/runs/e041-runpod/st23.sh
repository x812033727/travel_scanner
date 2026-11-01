#!/usr/bin/env bash
# e041 plus four e040 shots, stages 2 and 3: one pod per stage (a pod lives four hours at most),
# one retry pass, always stops the pod. Owner 2026-11-01: finish e040, carry on with the next episode.
set -u
REPO="$1"
V=C:/Users/x8120/mokaair-work/videos
ROOTS="$V/zhong-tian-qu-qi-e041-dh/runpod/a/picked $V/zhong-tian-qu-qi-e040-dh/runpod/a/picked3"
export USERPROFILE=$V/_audition/runpod-first-test-20261031/home
export HOME="$USERPROFILE" PYTHON=python PYTHONUNBUFFERED=1
H3R="$REPO/.agents/skills/minimax-h3-runpod/scripts/h3r.sh"
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$H3R" stop; }
trap stop_pod EXIT
for try in 1 2; do
  for P in $ROOTS; do
    mkdir -p "$P/st2/refined" "$P/final"
    for m in "$P"/st2/st2-*.json; do
      echo "=== refine $m try $try $(date -u +%T)"
      bash "$H3R" refine --manifest "$m" --output-dir "$P/st2/refined" --progress "$P/st2/refined/progress-$(basename "$m")" --keep --label e041-st2 || echo "exit=$?"
    done
  done
done
stop_pod
for try in 1 2; do
  for P in $ROOTS; do
    todo=()
    for f in "$P"/st2/refined/*.mp4; do [ -f "$P/final/$(basename "${f%.mp4}")_1080.mp4" ] || todo+=("$f"); done
    batch=0
    while [ "${#todo[@]}" -gt 0 ]; do
      batch=$((batch + 1))
      echo "=== upscale $P try $try batch $batch $(date -u +%T)"
      bash "$H3R" upscale "${todo[@]:0:20}" --output-dir "$P/final" --progress "$P/final/progress-$try-$batch.json" --keep --label e041-st3 || echo "exit=$?"
      todo=("${todo[@]:20}")
    done
  done
done
for P in $ROOTS; do echo "$P: $(ls "$P"/final/*_1080.mp4 | wc -l) finals"; done
echo "=== end $(date -u +%T)"
