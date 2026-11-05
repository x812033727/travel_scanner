#!/usr/bin/env bash
# route_a_st1.sh NN [SEED] : route A stage 1 (960x544 hero drafts) of a zhong-tian episode on one pod.
# Builds the Ref2VA manifests, runs the free check, drafts every shot with one retry pass, always
# stops the pod. A draft that already exists is skipped. Spends money: the owner approves first.
# ref2manifest.mjs's main guard only fires on Linux, so run this from a Linux session.
set -u
N=$1
SEED=${2:-${N}0000}
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(git -C "$HERE" rev-parse --show-toplevel)"
P=$REPO/docs/videos/series-plans/zhong-tian-qu-qi/production
EP=$(printf '%03d' "$N")
A=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e$EP-dh/runpod/a
M=$A/st1
PYTHON=${PYTHON:-python3}; export PYTHON
H3R="$HERE/h3r.sh"
mkdir -p "$M/out"
VIDEO_WORKDIR="$A" node "$P/colab/ref2manifest.mjs" "$P/hailuo/clips-dh-e$EP.json" "$P/hailuo/ff-dh-e$EP.json" "$N" "$M" \
  --refs "$P/assets/refs-dh" --seed "$SEED" --width 960 --height 544 || exit 2
for p in "$M"/ref-e"$EP"-part*.json; do bash "$H3R" check --manifest "$p" || exit 1; done
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$H3R" stop; }
trap stop_pod EXIT
for try in 1 2; do
  for p in "$M"/ref-e"$EP"-part*.json; do
    echo "=== $(basename "$p") try $try $(date -u +%T)"
    bash "$H3R" batch --manifest "$p" --output-dir "$M/out" --progress "$M/out/progress-$(basename "$p" .json).json" \
      --profile hero --keep --label "e$EP-st1" --slug "zhong-tian-qu-qi-e$EP" || echo "exit=$?"
  done
done
echo "have $(ls "$M"/out/*.mp4 | wc -l) drafts; review them before stage 2"
