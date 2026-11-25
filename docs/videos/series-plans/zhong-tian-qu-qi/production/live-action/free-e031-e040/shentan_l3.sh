#!/bin/bash
# arc 4 (2026-11-19, e033 r2 independent review 必改 1, 2, 5, 建議 10): the deep-pond pictures the episode sends, rebuilt on the
# wheel WITH paddles. set-shentan-l2 is the paid one-change edit of set-shentan-l1 (Qwen-Image-Edit-2509 on Colab, twelve flat
# wooden paddles on the rim; colab/runs/e933-live/shentan-l2/, picked in refs-live/README.md). Everything here is free:
#   shentan_clean.py paints out the low left frame's rope (it would join the sluice rope Carpenter Shi pulls, e032 fix2), the
#   pylon on the far left horizon and the thin poles on the right horizon (rule 13):
#     set-shentan-l2 -> set-shentan-l3 (the finished wheel), set-shentan-gongdi-l1 -> set-shentan-gongdi-l2 (the half-built site)
#   then the crops, each lanczos to 1312x736, with shentan_crops.sh's boxes plus one new box:
#     -bian (review 必改 2): the stone edge at the left and the wheel's near rim and paddles at the RIGHT, so a man standing at
#     the left can rest his hand on a paddle at the right edge (s30 at dawn, s35 at noon); -lun keeps its box for s38.
#   and the dawn grade of set-shentan-l3 with its two crops (shentan_crops.sh's grade, byte for byte the same filter).
# The l1 crops of shentan_crops.sh stay in refs-live as they were (no longer sent by e033).
# Usage: bash shentan_l3.sh refs-live/set-shentan-l2.png refs-live/set-shentan-gongdi-l1.png OUTDIR
set -e
A2=$1; G1=$2; O=$3; HERE=$(cd "$(dirname "$0")" && pwd)
A="$O/set-shentan-l3.png"; G="$O/set-shentan-gongdi-l2.png"
python3 -I "$HERE/shentan_clean.py" "$A2" "$A" wheel > /dev/null
python3 -I "$HERE/shentan_clean.py" "$G1" "$G" gongdi > /dev/null
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
# the finished wheel at noon
c "$A" set-shentan-lun-l3  640:360:380:200   # the lower half of the wheel in the water, its trestle and paddles (s38)
c "$A" set-shentan-an-l3   640:360:0:250     # the left: the stone steps, the small wooden landing, the left frame, no rope
c "$A" set-shentan-bian-l3 560:315:60:250           # the stone edge at the left, the wheel's near rim and paddles at the right (s35)
c "$A" set-shentan-geng-l3 640:360:672:120   # the dry furrowed field beyond the right frame, the edge of the wheel at the left
c "$A" set-shentan-tian-l3 640:360:672:0     # the pale sky over the tall right frame's top beam
# the half-built site (the wheel not yet on)
c "$G" set-shentan-gongdi-an-l2   640:360:0:220    # the left: the steps, the landing, the left frame, the bare axle on its trestle
c "$G" set-shentan-gongdi-mu-l2   640:360:672:300  # the right bank: the pile of timbers, the big grey boulder at the pond's edge
c "$G" set-shentan-gongdi-tian-l2 640:360:672:0    # the pale sky over the tall right frame's top beam
c "$G" set-shentan-gongdi-geng-l2 640:360:672:120  # the dry furrowed field beyond the right frame
# the tenth morning (shentan_crops.sh's grade)
D="$O/set-shentan-chen-l3.png"
ffmpeg -v error -y -i "$A" -vf "eq=saturation=0.30:contrast=0.65:brightness=-0.06:gamma=1.0,colorbalance=rs=0.04:bs=-0.04:rm=0.12:gm=0.05:bm=-0.12:rh=0.12:gh=0.06:bh=-0.14" -flags +bitexact -fflags +bitexact "$D"
c "$D" set-shentan-chen-bian-l3 560:315:60:250        # as set-shentan-bian-l3, at dawn (s30)
c "$D" set-shentan-chen-an-l3   640:360:0:250  # as set-shentan-an-l3, at dawn (s29)
