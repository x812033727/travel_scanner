#!/usr/bin/env bash
# make-s36-still.sh : the still that stands in for s36 (not shot) in the e905 live cut.
# Run after `stage.py 5` has written clips/s37-t1.mp4 (the refined s37, already trimmed at start 1.0), before
# assemble-v4.mjs. Frame 0 of the staged s37 = draft s37-9051401 at 1.0 s. It is scaled to 1920x1080, cropped to
# the eyes (960:540:640:120 in 1920x1080 coordinates, from fix3/review-picks.tsv) and scaled back to 1920x1080.
# edit-dh-e905-live.json then moves it (still_move s36: slow push 1.0 -> 1.06) and reddens it (vf s36).
# Fallback when s37 is refined but not staged yet: the refined picture at 1.0 s.
set -euo pipefail
E="${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}"
case "$E" in */_live-e905) ;; *) E="$E/_live-e905" ;; esac
E="$E/zhong-tian-qu-qi-e905-dh"
OUT="$E/first-frames/s36-t1.png"
VF="scale=1920:1080:flags=lanczos,crop=960:540:640:120,scale=1920:1080:flags=lanczos,format=rgb24"
mkdir -p "$E/first-frames"
if [ -f "$E/clips/s37-t1.mp4" ]; then
  ffmpeg -v error -y -i "$E/clips/s37-t1.mp4" -frames:v 1 -vf "$VF" "$OUT"
elif [ -f "$E/runpod/a/st2/refined/s37.mp4" ]; then
  ffmpeg -v error -y -ss 1.0 -i "$E/runpod/a/st2/refined/s37.mp4" -frames:v 1 -vf "$VF" "$OUT"
else
  echo "no refined s37 yet ($E/clips/s37-t1.mp4 or runpod/a/st2/refined/s37.mp4)" >&2; exit 1
fi
# assemble-v4 takes a still only when the shot has no clip: there must be no clips/s36-t*.mp4
if ls "$E"/clips/s36-t*.mp4 >/dev/null 2>&1; then echo "warning: clips/s36-t*.mp4 exists and would win over the still" >&2; fi
echo "$OUT $(ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 "$OUT")"
