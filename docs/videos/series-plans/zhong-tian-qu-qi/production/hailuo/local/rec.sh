#!/usr/bin/env bash
# rec.sh NNN : record every line of episode NNN that has no wav yet into the -dh workdir (Gemini
# voices from video.json; needs the video tool login, `node tools/video/cli.mjs login`). Copies the
# three music cues from the previous episode's workdir the first time.
set -u
H=$(cd "$(dirname "$0")" && pwd)
R=$(cd "$H/../../../../../../.." && pwd)
V=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}
F="$R/docs/videos/zhong-tian-qu-qi-e$1/video.json"
W="$V/zhong-tian-qu-qi-e$1-dh"
IDS=$(node -e "const v=require(process.argv[1]);console.log(v.scenes.flatMap(s=>(s.lines||[]).map(l=>l.id)).join(','))" "$F")
mkdir -p "$W/audio" "$W/music"
if [ -z "$(ls -A "$W/music" 2>/dev/null)" ]; then
  P=$(printf %03d $((10#$1 - 1)))
  cp "$V/zhong-tian-qu-qi-e$P-dh/music/"* "$W/music/"
fi
node "$H/lines.mjs" "$R" "$F" "$W/audio" "$IDS" 2>&1 | tail -2
echo "e$1 $(ls "$W/audio" | wc -l) / $(echo "$IDS" | tr ',' '\n' | wc -l)"
