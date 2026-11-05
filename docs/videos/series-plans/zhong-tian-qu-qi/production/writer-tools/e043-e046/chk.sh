#!/bin/bash
# usage: chk.sh EP
S=$(cd "$(dirname "$0")" && pwd)
cd /home/user/travel_scanner
python3 $S/e0$1.py || exit 1
node tools/video/cli.mjs lint --slug zhong-tian-qu-qi-e0$1 2>&1 | grep "WARN\|ERROR\|errors"
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs docs/videos/zhong-tian-qu-qi-e0$1/video.json | grep -v "^ok\|^info"
node .agents/skills/animation-camera/scripts/shot_reading.mjs docs/videos/zhong-tian-qu-qi-e0$1/video.json | grep "陷阱  \|讀了"
H=$S/h$1.md; F=$S/f$1.md; [ -f $H ] || H=$S/h.md; [ -f $F ] || F=$S/f.md
node $S/sb.mjs $1 $H $F | tail -2
