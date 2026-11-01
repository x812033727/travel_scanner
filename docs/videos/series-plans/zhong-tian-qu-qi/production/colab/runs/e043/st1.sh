#!/usr/bin/env bash
# e043 stage 1: route_a_st1.sh plus patch_st1.py (registrar, proctor, Wei servant portraits; shoes line).
# ref2manifest -> patch -> free check -> drafts with one retry pass -> always stop the pod.
set -u
REPO="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
P=$REPO/docs/videos/series-plans/zhong-tian-qu-qi/production
S=$REPO/.agents/skills/minimax-h3-runpod/scripts
A=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e043-dh/runpod/a
M=$A/st1
mkdir -p "$M/out"
VIDEO_WORKDIR="$A" node "$P/colab/ref2manifest.mjs" "$P/hailuo/clips-dh-e043.json" "$P/hailuo/ff-dh-e043.json" 43 "$M" \
  --refs "$P/assets/refs-dh" --seed 430000 --width 960 --height 544 || exit 2
python3 -I "$P/colab/runs/e043/patch_st1.py" "$M" "${E043_REFS:-$P/assets/refs-dh}" || exit 2
for p in "$M"/ref-e043-part*.json; do bash "$S/h3r.sh" check --manifest "$p" || exit 1; done
[ "${DRY:-0}" = 1 ] && exit 0
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$S/h3r.sh" stop; }
trap stop_pod EXIT
for try in 1 2; do
  for p in "$M"/ref-e043-part*.json; do
    echo "=== $(basename "$p") try $try $(date -u +%T)"
    bash "$S/h3r.sh" batch --manifest "$p" --output-dir "$M/out" --progress "$M/out/progress-$(basename "$p" .json).json" \
      --profile hero --keep --label e043-st1 --slug zhong-tian-qu-qi-e043 || echo "exit=$?"
  done
done
echo "have $(ls "$M"/out/*.mp4 | wc -l) drafts; review them before stage 2"
