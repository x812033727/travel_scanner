#!/bin/bash
# arc 4 (2026-11-19, e034 r2 d1 prep): free crops of set-hantian-l1 (round 1, 37038: the three small dry fields of Liuxi in a
# low golden light, rows of cracked furrows with short dry stubble, a low grassy ridge across the middle, a big old tree with
# yellow leaves at the right, a row of small houses and far hills at the left and middle) and one grey grade, each a new id,
# lanczos to 1312x736 (rules 19, 35). e034 s27-s36 (the water reaching the fields at sunset) and s37-s40 (the swarm over the
# northern hills eats the sunset: the grade darkens and drains the picture).
#   -geng: the left: near furrows, the grassy ridge, the far field, the houses and hills on top (s27, s29, s34, s35)
#   -liu:  the right: the big tree, the grassy bank under it, the furrows (s30-s32, Qian Yuanwai on the bank)
#   -tian: the middle: sky, far hills and houses over a strip of field (s28, s33)
#   -di:   the furrows only (s36)
#   -hui (the whole picture, s40), -hui-tian (s37, s38), -hui-geng (s39): the grey grade and its crops.
# First (2026-11-19, looked at 4x): ffmpeg delogo paints out three tiny dark verticals on the far field line (a figure-like post
# at x 822-836, y 372-394; a thin pole at x 739-751; a thin pole by the right-hand houses at x 590-602) (rules 13, 34: nobody
# extra in the frame, nothing modern); the patches are soft and only seen when magnified.
# Usage: bash hantian_crops.sh refs-live/set-hantian-l1.png OUTDIR
set -e
S=$1; O=$2; A="$O/.hantian-clean.png"
ffmpeg -v error -y -i "$S" -vf "delogo=x=822:y=372:w=14:h=22,delogo=x=739:y=364:w=12:h=32,delogo=x=590:y=346:w=12:h=26" -flags +bitexact -fflags +bitexact "$A"
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
c "$A" set-hantian-geng-l1 640:360:0:300
c "$A" set-hantian-liu-l1  560:315:752:200
c "$A" set-hantian-tian-l1 640:360:330:150
c "$A" set-hantian-di-l1   640:360:300:376
H="$O/set-hantian-hui-l1.png"
ffmpeg -v error -y -i "$A" -vf "eq=brightness=-0.16:saturation=0.40:contrast=0.85:gamma=0.90,colorbalance=rs=0.02:bs=0.03:rm=0.02:bm=0.02" -flags +bitexact -fflags +bitexact "$H"
c "$H" set-hantian-hui-tian-l1 640:360:330:150
c "$H" set-hantian-hui-geng-l1 640:360:0:300
rm -f "$A"
