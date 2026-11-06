#!/usr/bin/env bash
# chain.sh STEP... : run route-A steps one after another on one long-lived pod (KEEP=1), each step
# retried by its own *-retry.sh, with speed-guard watching. A step is "st23:NN" (stages 2-3 of NN,
# seeds from <runpod/a>/st2-seeds.txt) or "st1:NN" (stage-1 drafts of NN). The pod is left up at
# the end (idle stop 60 min on the site) so the next review's retakes reuse it.
set -u
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(git -C "$HERE" rev-parse --show-toplevel)"
V=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}
export KEEP=1
for step in "$@"; do
  kind=${step%%:*}; N=${step##*:}; EP=$(printf '%03d' "$N"); A=$V/zhong-tian-qu-qi-e$EP-dh/runpod/a; mkdir -p "$A"
  echo "##### chain step $step $(date -u +%T)"
  case $kind in
    st23) L=$A/st23.log; [ -f "$L" ] && mv "$L" "$A/st23-$(date +%s).log"
          bash "$HERE/st23-retry.sh" "$N" "${N}0000" $(cat "$A/st2-seeds.txt" 2>/dev/null) > "$L" 2>&1 &
          pid=$!; bash "$HERE/speed-guard.sh" "$L" 500 "route_a_st23.sh $N|runpod_runner.py (refine|upscale)" & g=$!
          wait $pid; kill $g 2>/dev/null ;;
    st1)  L=$A/st1.log; [ -f "$L" ] && mv "$L" "$A/st1-$(date +%s).log"
          bash "$HERE/st1-retry.sh" "$N" > "$L" 2>&1 &
          pid=$!; bash "$HERE/speed-guard.sh" "$L" 400 "st1-ep.sh $N|runpod_runner.py batch" & g=$!
          wait $pid; kill $g 2>/dev/null ;;
  esac
  echo "##### chain step $step finished $(date -u +%T): $(tail -1 "$L")"
done
echo "##### chain done $(date -u +%T)"
