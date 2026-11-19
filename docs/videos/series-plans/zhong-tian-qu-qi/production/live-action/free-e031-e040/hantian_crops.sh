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
# First: hantian_clean.py paints out three tiny dark verticals on the far field line (a figure-like post at x 825-837, y 376-395;
# a thin goal-post-like frame at x 724-751; a thin pole by the right-hand houses at x 593-603) (rules 13, 34: nobody extra in the
# frame, nothing modern). Until the e034 independent review (建議 7) this was ffmpeg delogo, which left soft grey boxes on the
# horizon (visible in -tian, -liu and -di); hantian_clean.py interpolates straight across each thin box from the pixels just
# outside it, feathered, so the horizon, the tree line and the furrows carry through (rule 33).
# Usage: bash hantian_crops.sh refs-live/set-hantian-l1.png OUTDIR
set -e
S=$1; O=$2; A="$O/.hantian-clean.png"
python3 -I "$(dirname "$0")/hantian_clean.py" "$S" "$A"
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
