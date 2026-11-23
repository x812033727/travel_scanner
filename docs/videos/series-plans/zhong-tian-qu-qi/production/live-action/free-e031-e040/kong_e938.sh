#!/bin/bash
# e038 r2 after the independent review (必改 1, 6; the coordinator's paid Qwen edits, colab/runs/e938-live/qwen/step2, step3):
# free grade and crops of the three new pictures. Each a new id, lanczos to 1312x736 (rules 19, 35).
# The sickroom set-xujia-tangfang-kong-chen-l1 (day, 9381221) / -kong-l1 (night, 9381224): the small table is gone, the floor in
# front of the whole bed is clear; a small low stool with one white candle stands in the corner at the bed's foot (LEFT), unlit
# by day, the only warm light by night; the plank door at the far left, the window, the pink quilt and the pillow at the RIGHT.
#   set-xujia-tangfang-kong-xi-l1: the day picture warmed to late afternoon (the same grade as xujia_tangfang_e938.sh's -xi)
#   crops of each of -kong-chen (s01-s04), -kong-xi (s05-s11) and -kong (night, s12-s19):
#     -chuang: the bed, its quilt and pillow under the window (the girl in bed; Xu Yan kneeling before it)   640:360 at 520,250
#     -men:    the plank door at the left, the cracked wall, the stool with its candle, the foot of the bed  640:360 at 0,300
#     -zhen:   the pillow end of the bed, the bed head rail and the wall                                  480:270 at 820,330
# The gate set-chengmen-ye2-l1 (9381215): both leaves of the big arched gate shut, the small side door right of the arch swung
# out, two torches, the stone ball post, the moon high at the right; the waist-high barrier of crossed stakes now runs from the
# foot of the right torch across the paved road to the right edge, blocking the way to the side door.
#     set-chengmen-ye2-zha-l1:   the side door, its torch and the barrier across the road (s22, s27)      800:450 at 380,286
#     set-chengmen-ye2-qiang-l1: the lit wall, the right torch, the top of the barrier (the captain, s23, s26)  560:315 at 460,250
#     set-chengmen-ye2-men-l1:   the two shut leaves, the side door, the left torch (s24, s28)            640:360 at 0,220
#     set-chengmen-ye2-lu-l1:    the far end of the barrier, the long wall and the road (s25)             560:315 at 752,300
#     set-chengmen-ye2-zha2-l1:  e938 fix1: the side door, its torch and the whole barrier with the wall above it, wider
#                                than -zha, room on the far side for the horse (fix1 s22, s27)               1000:562 at 312,174
# Usage: bash kong_e938.sh REFS_LIVE_DIR OUTDIR
set -e
L=$1; O=$2
ffmpeg -v error -y -i "$L/set-xujia-tangfang-kong-chen-l1.png" -vf "eq=gamma=0.86:saturation=1.15,colorbalance=rs=0.24:gs=0.05:bs=-0.26:rm=0.16:gm=0.02:bm=-0.18:rh=0.10:bh=-0.12" -flags +bitexact -fflags +bitexact "$O/set-xujia-tangfang-kong-xi-l1.png"
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
for k in kong-chen kong-xi kong; do
  src="$L/set-xujia-tangfang-$k-l1.png"; [ $k = kong-xi ] && src="$O/set-xujia-tangfang-kong-xi-l1.png"
  c "$src" set-xujia-tangfang-$k-chuang-l1 640:360:520:250
  c "$src" set-xujia-tangfang-$k-men-l1    640:360:0:300
  c "$src" set-xujia-tangfang-$k-zhen-l1   480:270:820:330
done
G="$L/set-chengmen-ye2-l1.png"
c "$G" set-chengmen-ye2-zha-l1   800:450:380:286
c "$G" set-chengmen-ye2-qiang-l1 560:315:460:250
c "$G" set-chengmen-ye2-men-l1   640:360:0:220
c "$G" set-chengmen-ye2-lu-l1    560:315:752:300
c "$G" set-chengmen-ye2-zha2-l1  1000:562:312:174
