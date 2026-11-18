#!/bin/bash
# arc 4 (2026-11-18, e032 r2 review 必改 1; coordinator's decision): dawn versions of set-jingkeng-l1 and two of its crops, so the
# third MORNING (e032 s11-s15) does not get the same golden low sun as the evening (s16-s26b): jingkeng_chen.py paints out the
# lone far trunk that reads as a person, then one grade (desaturate, flatten, lift, cool; the golden willow to a grey yellow), then
# the same crop boxes as jingkeng_crops.sh. Each a new id with its own l1, lanczos to 1312x736.
# Usage: bash jingkeng_chen.sh refs-live/set-jingkeng-l1.png OUTDIR
set -e
Q=$1; O=$2; HERE=$(cd "$(dirname "$0")" && pwd)
T="$O/.jingkeng-notrunk.png"
python3 -I "$HERE/jingkeng_chen.py" "$Q" "$T"
F="$O/set-jingkeng-chen-l1.png"
G="eq=saturation=0.40:contrast=0.80:gamma=1.18,colorbalance=rs=-0.12:gs=-0.02:bs=0.12:rm=-0.08:gm=-0.01:bm=0.08:rh=-0.05:bh=0.05"
ffmpeg -v error -y -i "$T" -vf "$G" -flags +bitexact -fflags +bitexact "$F"
rm -f "$T"
c() { ffmpeg -v error -y -i "$F" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-jingkeng-kou-chen-l1 640:360:0:376     # as set-jingkeng-kou-l1, at dawn: s12, s14, s15
c set-jingkeng-dui-chen-l1 640:360:440:280   # as set-jingkeng-dui-l1, at dawn: s13
