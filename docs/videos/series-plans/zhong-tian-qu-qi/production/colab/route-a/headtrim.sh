#!/usr/bin/env bash
# headtrim.sh in.mp4 out.mp4 : an insert given only the set picture opens on that picture for a moment
# and then cuts to the insert. Find the first hard cut in the first 1.5 s and start the clip there;
# with no cut, copy unchanged. Prints the cut time.
set -u
t=$(ffmpeg -v error -t 1.5 -i "$1" -vf "select='gt(scene,0.30)',metadata=print:file=-" -an -f null - 2>/dev/null | grep -o "pts_time:[0-9.]*" | head -1 | cut -d: -f2)
if [ -z "$t" ]; then cp "$1" "$2"; echo "no cut"; exit 0; fi
ffmpeg -v error -y -ss "$t" -i "$1" -c:v libx264 -crf 14 -preset slow -c:a aac "$2" && echo "cut at $t"
