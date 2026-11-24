#!/bin/bash
# e039 r2 d1 prep (2026-11-24, free): crops of the barn front set-gucang-wai-l1 (arc 4 screen test round 3, 37042: the picked
# set-hantian-yang-l1 with one low barn of grey weathered planks added at the right, its two plank leaves swung back flat against
# its front on both sides of the dark doorway, the trampled earth before it, the flooded field of young rice seedlings across the
# left half, dry ploughed fields, the village and hills far away, the big golden tree behind the barn; low warm light). Scene 3 of
# e039 (the early morning before the barn; 〈接點〉 39->40). Each a new id, lanczos to 1312x736 (rules 19, 35); the whole picture
# goes to the wide s36.
#   set-gucang-wai-men-l1:  the barn front, its dark doorway between the swung-back leaves and the trampled earth before it
#                           (Elder Han s37, Qin Shuang and Diao Qi s39)                                            640:360 at 672,200
#   set-gucang-wai-tian-l1: the pale sky over the far ploughed fields, the row of village houses and the low hills (the low
#                           angle on Qian Yuanwai at the edge of the rice field, s38)                               640:360 at 0,150
#   set-gucang-wai-qiang-l1: the grey weathered planks of the barn's gable front above the doorway, close (Diao Qi's close-up
#                           s40: 「身後只有穀倉的木板牆」)                                                         288:162 at 915,205
# Usage: bash gucang_wai_e939.sh REFS_LIVE_DIR OUTDIR
set -e
L=$1; O=$2
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
G="$L/set-gucang-wai-l1.png"
c "$G" set-gucang-wai-men-l1   640:360:672:200
c "$G" set-gucang-wai-tian-l1  640:360:0:150
c "$G" set-gucang-wai-qiang-l1 288:162:915:205
