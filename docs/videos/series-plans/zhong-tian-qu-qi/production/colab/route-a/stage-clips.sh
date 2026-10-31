#!/usr/bin/env bash
# stage-clips.sh NN [sNN ...] : place episode NN's 1080p finals as <workdir>/zhong-tian-qu-qi-e0NN-dh/clips/sNN-t1.mp4,
# the shape assemble-v4.mjs reads. The shots named after NN are inserts that opened on the set picture:
# headtrim.sh cuts them at their first hard cut (and copies them unchanged when it finds none).
set -u
N=$1; shift
HERE=$(cd "$(dirname "$0")" && pwd)
V=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}
W=$V/zhong-tian-qu-qi-e0$N-dh
mkdir -p "$W/clips"
trim=" $* "
for f in "$W"/colab/a/final/s*_1080.mp4; do
  s=$(basename "$f" _1080.mp4)
  out="$W/clips/$s-t1.mp4"
  [ -f "$out" ] && [ "$out" -nt "$f" ] && continue
  case "$trim" in
    *" $s "*) printf '%s ' "$s"; bash "$HERE/headtrim.sh" "$f" "$out" ;;
    *) cp "$f" "$out" ;;
  esac
done
echo "clips: $(ls "$W"/clips/s*-t1.mp4 2>/dev/null | wc -l)"
