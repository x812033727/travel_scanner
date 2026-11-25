#!/bin/bash
# arc 4 (2026-11-19, e033 r2 d1 prep): free crops of the two picked deep-pond pictures and one dawn grade, each a new id with its
# own l1, lanczos to 1312x736 (rules 19, 35: close shots get a crop with real ground, never the whole wide).
#   set-shentan-l1 (round 3, 37041: the whole waterwheel standing in the pond, seen side-on from the near stone edge; two
#   wooden frames, stone steps and a small wooden landing at the left, a big grey boulder at the right, dry furrowed fields)
#   set-shentan-gongdi-l1 (round 5, 37045: the same pond and camera with the wheel taken away: the two frames, a bare axle on a
#   small trestle, a pile of timbers on the right bank)
# The dawn version (e033 s28-s30: the tenth morning) is one grade of set-shentan-l1 (desaturate, flatten, lift, a grey-gold
# cast, the sky toned down) and two crops of it, so the morning does not get the same hard white noon as s31-s40 (e032 review
# 必改 1's lesson: one picture for two times of day draws the wrong light).
# Usage: bash shentan_crops.sh refs-live/set-shentan-l1.png refs-live/set-shentan-gongdi-l1.png OUTDIR
set -e
A=$1; G=$2; O=$3
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
# the finished wheel at noon
c "$A" set-shentan-lun-l1  640:360:380:200   # the lower half of the wheel in the water, its trestle and the tall right frame's post
c "$A" set-shentan-an-l1   640:360:0:250     # the left: the stone steps, the small wooden landing at the water, the left frame and its rope
c "$A" set-shentan-geng-l1 640:360:672:120   # the dry furrowed field beyond the right frame, the edge of the wheel at the left
c "$A" set-shentan-tian-l1 640:360:672:0     # the pale sky over the tall right frame's top beam
# the half-built site (the wheel not yet on)
c "$G" set-shentan-gongdi-an-l1   640:360:0:220    # the left: the steps, the landing, the left frame, the bare axle on its trestle
c "$G" set-shentan-gongdi-mu-l1   640:360:672:300  # the right bank: the pile of timbers, the big grey boulder at the pond's edge
c "$G" set-shentan-gongdi-tian-l1 640:360:672:0    # the pale sky over the tall right frame's top beam
c "$G" set-shentan-gongdi-geng-l1 640:360:672:120  # the dry furrowed field beyond the right frame
# the tenth morning
D="$O/set-shentan-chen-l1.png"
ffmpeg -v error -y -i "$A" -vf "eq=saturation=0.30:contrast=0.65:brightness=-0.06:gamma=1.0,colorbalance=rs=0.04:bs=-0.04:rm=0.12:gm=0.05:bm=-0.12:rh=0.12:gh=0.06:bh=-0.14" -flags +bitexact -fflags +bitexact "$D"
c "$D" set-shentan-chen-lun-l1 640:360:380:200  # as set-shentan-lun-l1, at dawn
c "$D" set-shentan-chen-an-l1  640:360:0:250    # as set-shentan-an-l1, at dawn
