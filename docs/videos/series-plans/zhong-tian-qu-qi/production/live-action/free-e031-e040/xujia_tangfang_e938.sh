#!/bin/bash
# e038 r2 d1 prep (2026-11-23): the sickroom of e038 scene 1 (bible rule 42 / 〈場景〉: Tang Xiaotang's room picture
# set-xujia-tangfang-l2 by night and its free dawn grade set-xujia-tangfang-chen-l1 by day; the door at the LEFT, the bed
# against the back wall under the window, its pillow end at the RIGHT, the small table in the right front with one candle).
# Three groups, each a new id, lanczos to 1312x736 (rules 19, 35):
#   set-xujia-tangfang-xi-l1: the dawn grade warmed to the low orange light of late afternoon (s05-s11: the script's 傍晚),
#     window paper glowing warm, the candle still unlit (the script's lit lamp is not written)
#   crops of each of -chen (s01-s04), -xi (s05-s11) and the night picture -l2 (s12-s19):
#     -chuang: the bed with its quilt and pillow under the lower part of the window, the table's near corner (the girl in bed)
#     -men:    the plank door at the left, the cracked wall and the foot of the bed (the people who come in)
#     -zhen:   the pillow end of the bed, the bed head and the corner of the table (close-ups on the pillow and at the bedside)
# Usage: bash xujia_tangfang_e938.sh refs-live/set-xujia-tangfang-chen-l1.png refs-live/set-xujia-tangfang-l2.png OUTDIR
set -e
C=$1; N=$2; O=$3
ffmpeg -v error -y -i "$C" -vf "eq=gamma=0.86:saturation=1.15,colorbalance=rs=0.24:gs=0.05:bs=-0.26:rm=0.16:gm=0.02:bm=-0.18:rh=0.10:bh=-0.12" -flags +bitexact -fflags +bitexact "$O/set-xujia-tangfang-xi-l1.png"
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
for k in chen xi; do
  src="$C"; [ $k = xi ] && src="$O/set-xujia-tangfang-xi-l1.png"
  c "$src" set-xujia-tangfang-$k-chuang-l1 640:360:480:300
  c "$src" set-xujia-tangfang-$k-men-l1    560:315:0:180
  c "$src" set-xujia-tangfang-$k-zhen-l1   480:270:800:330
done
c "$N" set-xujia-tangfang-chuang-l1 640:360:480:300
c "$N" set-xujia-tangfang-men-l1    560:315:0:180
c "$N" set-xujia-tangfang-zhen-l1   480:270:800:330
