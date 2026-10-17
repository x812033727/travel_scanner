#!/usr/bin/env bash
# asm.sh NNN : cut episode NNN (assemble-v4 + edit-dh-eNNN.json) into <workdir>/cut/eNNN-dh.mp4,
# then a 1280-wide phone copy and a 4x4 contact sheet (sheet.png, one frame every 6 s) to look at.
# Read cut/final.log afterwards: "held X s" over ~0.5 s means a clip was too short for its lines.
set -u
H=$(cd "$(dirname "$0")/.." && pwd)
R=$(cd "$H/../../../../../.." && pwd)
V=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}
D="$R/docs/videos/zhong-tian-qu-qi-e$1"
W="$V/zhong-tian-qu-qi-e$1-dh"
mkdir -p "$W/cut"
node "$H/assemble-v4.mjs" "$D/video.json" "$D/overlays.json" "$H/edit-dh-e$1.json" "$W" "$W/cut/e$1-dh.mp4" > "$W/cut/final.log" 2>&1; echo "exit $?" >> "$W/cut/final.log"
cd "$W/cut" || exit 1
ffmpeg -v error -y -i "e$1-dh.mp4" -map 0 -c:v libx264 -preset fast -crf 27 -vf scale=1280:-2 -c:a aac -b:a 128k -c:s mov_text -movflags +faststart "e$1-dh-phone.mp4" && echo phone-ok >> final.log
ffmpeg -v error -y -i "e$1-dh.mp4" -vf "fps=1/6,scale=480:-2,tile=4x4" -frames:v 1 sheet.png
echo "e$1 $(grep '^total' final.log) $(tail -1 final.log)"
grep -E "held [0-9.]+s" final.log || true
