#!/bin/bash
# arc 4 (2026-11-19, e034 r2 d1 prep): the deep-pond pictures e034 sends beyond set-shentan-l3 and its e033 crops, all free,
# each a new id, lanczos to 1312x736 (rules 19, 35):
#   set-shentan-shi-l3: a crop of set-shentan-l3 round the big grey boulder at the right (the wheel's lower right paddles at
#     the left, the stone edge and water, the tall frame's posts, the field) for Qin Shuang on the boulder (e034 s10, s18);
#   the sunset of the tenth day (e034 s22-s25): one warm grade of set-shentan-l3 (darker, warmer, the highlights golden, the
#     blue pulled out of the sky) -> set-shentan-xi-l3, and three crops of it: -xi-an (shentan_l3.sh's -an box: the steps, the
#     landing, the left frame, the wheel's rim at the right edge), -xi-lun (the -lun box: the lower half of the wheel and its
#     trestle) and -xi-ye (the top of the wheel: its upper paddles against the sky, for the close-up of the paddles lifting
#     water, which replaces the script's bamboo buckets: the picked wheel has none, bible 〈道具〉);
#   the new channel at sunset (e034 s26): the same grade of set-shentan-qu-l1 (round 4, 37043: a dry earthen channel dug
#     across the furrowed field beside the tall frame's posts and the boulder) -> set-shentan-qu-xi-l1.
# The noon light (e034 s01-s21) sends set-shentan-l3 and its e033 crops as they are (shentan_l3.sh).
# Usage: bash shentan_xi.sh refs-live/set-shentan-l3.png refs-live/set-shentan-qu-l1.png OUTDIR
set -e
A=$1; Q=$2; O=$3
G="eq=brightness=-0.06:saturation=1.10:contrast=1.05:gamma=0.92,colorbalance=rs=0.12:gs=0.02:bs=-0.16:rm=0.16:gm=0.04:bm=-0.16:rh=0.14:gh=0.04:bh=-0.18"
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
c "$A" set-shentan-shi-l3 560:315:752:421   # the big grey boulder at the right, the stone edge and water, the tall frame's posts
X="$O/set-shentan-xi-l3.png"
ffmpeg -v error -y -i "$A" -vf "$G" -flags +bitexact -fflags +bitexact "$X"
c "$X" set-shentan-xi-an-l3  640:360:0:250    # as set-shentan-an-l3, at sunset
c "$X" set-shentan-xi-lun-l3 640:360:380:200  # as set-shentan-lun-l3, at sunset
c "$X" set-shentan-xi-ye-l3  560:315:340:20   # the top of the wheel, its upper paddles against the sky, at sunset
ffmpeg -v error -y -i "$Q" -vf "$G" -flags +bitexact -fflags +bitexact "$O/set-shentan-qu-xi-l1.png"
