#!/usr/bin/env bash
# loudnorm2.sh CUT.mp4 : second loudnorm pass on a finished cut (route-a.md, e903 live): measure, then linear
# loudnorm to -14 LUFS with TP -2.2; picture and subtitle tracks are copied. The original goes to <dir>/pre/.
set -euo pipefail
f=$1; d=$(dirname "$f"); b=$(basename "$f"); mkdir -p "$d/pre"
pre="$d/pre/${b%.mp4}.pre-loudnorm.mp4"; mv "$f" "$pre"
j=$(ffmpeg -hide_banner -i "$pre" -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
g() { echo "$j" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
ffmpeg -v error -y -i "$pre" -map 0 -c copy -c:a aac -b:a 192k -af "loudnorm=I=-14:TP=-2.2:LRA=11:measured_I=$(g input_i):measured_TP=$(g input_tp):measured_LRA=$(g input_lra):measured_thresh=$(g input_thresh):offset=$(g target_offset):linear=true,aresample=48000" "$f"
ffmpeg -hide_banner -i "$f" -map 0:a -af ebur128 -f null - 2>&1 | grep -E '^\s+I:' | tail -1
