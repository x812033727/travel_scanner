#!/usr/bin/env bash
# st1-ep.sh NN : route A stage 1 for any episode, the e043 way: ref2manifest -> extras_patch.py
# (colab/runs/eNNN/extras.json, if any) -> free check -> drafts with one retry pass -> always stop.
# DRY=1 stops after the check. Seed NN0000.
set -u
N=$1; EP=$(printf '%03d' "$N")
REPO="$(git -C "$(dirname "${BASH_SOURCE[0]}")" rev-parse --show-toplevel)"
P=$REPO/docs/videos/series-plans/zhong-tian-qu-qi/production
S=$REPO/.agents/skills/minimax-h3-runpod/scripts
A=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/zhong-tian-qu-qi-e$EP-dh/runpod/a
M=$A/st1
mkdir -p "$M/out"
VIDEO_WORKDIR="$A" node "$P/colab/ref2manifest.mjs" "$P/hailuo/clips-dh-e$EP.json" "$P/hailuo/ff-dh-e$EP.json" "$N" "$M" \
  --refs "$P/assets/refs-dh" --seed "${N}0000" --width 960 --height 544 || exit 2
X=$P/colab/runs/e$EP/extras.json; [ -f "$X" ] || { mkdir -p "$(dirname "$X")"; echo '{}' > "$X"; }
python3 -I "$P/colab/runs/_scripts/extras_patch.py" "$M" "$P/assets/refs-dh" "$REPO/docs/videos/zhong-tian-qu-qi-e$EP/video.json" "$X" || exit 2
for p in "$M"/ref-e"$EP"-part*.json; do bash "$S/h3r.sh" check --manifest "$p" || exit 1; done
# Read every prompt before paying (preflight-prompts.py): an ERROR stops the batch; PREFLIGHT=0 skips it.
[ "${PREFLIGHT:-1}" = 0 ] || python3 -I "$P/colab/runs/_scripts/preflight-prompts.py" "$M"/ref-e"$EP"-part*.json || exit 2
[ "${DRY:-0}" = 1 ] && exit 0
stop_pod() { echo "=== stop $(date -u +%T)"; bash "$S/h3r.sh" stop; }
[ "${KEEP:-0}" = 1 ] || trap stop_pod EXIT
for try in 1 2; do
  for p in "$M"/ref-e"$EP"-part*.json; do
    echo "=== $(basename "$p") try $try $(date -u +%T)"
    bash "$S/h3r.sh" batch --manifest "$p" --output-dir "$M/out" --progress "$M/out/progress-$(basename "$p" .json).json" \
      --profile hero --keep --label "e$EP-st1" --slug "zhong-tian-qu-qi-e$EP" || echo "exit=$?"
  done
done
echo "have $(ls "$M"/out/s*.mp4 | wc -l) drafts; review them before stage 2"
