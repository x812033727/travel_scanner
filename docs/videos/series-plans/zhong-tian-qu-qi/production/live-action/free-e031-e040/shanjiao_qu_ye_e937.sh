#!/bin/bash
# e037 r2 d1 prep (2026-11-23): free pictures of the new channel by night and at the first grey of dawn for e037 scene 2 (the
# head of the new channel, the fourth watch to just before dawn) and the end of scene 3 (the same place at dawn). The source is
# the paid night picture set-shanjiao-qu-ye-l1 (screen test round 5, 37046), cleaned by shanjiao_qu_ye_clean.py of what the e036
# reviews took out of the day picture (the guard rail, the flat upright board, the skyline bumps) and of its crescent moon (e036
# showed a full moon); the day crops' geometry (shanjiao_qu.sh), each a new id, lanczos to 1312x736 (rules 19, 35):
#   -ye2:       the cleaned night picture (the wides: s10, s13, s21)
#   -ye2-geng:  the long mound of dug earth and the heap of dry straw on the left bank (the earth ridge the script calls 土埂:
#               the defenders' line; s11, s12, s14, s20, s24, s26, s27, s28)
#   -ye2-zhuo:  the flat dry field and the line of dark pines at the far left, the end of the mound at the lower right (the side
#               the raiders come from: s17, s18, s19, s21, s22, s25)
#   -ye2-tian:  the right bank, the plank across the channel and the dark paddy (the close-ups facing the field: s15, s16, s16b)
#   -ye2-cao:   the heap of dry straw close (the insert s23, ground and light only)
#   -ye2-kong:  the night sky over the tops of the pines (the low angle s20)
#   -chen:      the cleaned night picture lifted to the cold grey-blue just before dawn, a pale grey-white band low over the far
#               pines and the field (eq gamma, desaturated, a geq glow centred at 47 % of the height), and its crops
#               -chen-geng, -chen-zhuo, -chen-tian (the same geometry) for s35-s40
# Usage: bash shanjiao_qu_ye_e937.sh refs-live/set-shanjiao-qu-ye-l1.png OUTDIR
set -e
S=$1; O=$2
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
Y="$O/set-shanjiao-qu-ye2-l1.png"
python3 -I "$(dirname "$0")/shanjiao_qu_ye_clean.py" "$S" "$Y"
c "$Y" set-shanjiao-qu-ye2-geng-l1 560:315:40:400
c "$Y" set-shanjiao-qu-ye2-zhuo-l1 640:360:0:200
c "$Y" set-shanjiao-qu-ye2-tian-l1 560:315:752:330
c "$Y" set-shanjiao-qu-ye2-cao-l1  352:198:380:340
c "$Y" set-shanjiao-qu-ye2-kong-l1 640:360:240:0
C="$O/set-shanjiao-qu-chen-l1.png"
ffmpeg -v error -y -i "$Y" -vf "format=rgb24,eq=gamma=1.55:saturation=0.5:brightness=0.04,geq=r='min(255,r(X,Y)+70*max(0,1-abs(Y-H*0.47)/(H*0.30)))':g='min(255,g(X,Y)+72*max(0,1-abs(Y-H*0.47)/(H*0.30)))':b='min(255,b(X,Y)+66*max(0,1-abs(Y-H*0.47)/(H*0.30)))',colorbalance=rs=0.02:bs=0.04:rm=0.03:bm=0.02" -frames:v 1 -flags +bitexact -fflags +bitexact "$C"
c "$C" set-shanjiao-qu-chen-geng-l1 560:315:40:400
c "$C" set-shanjiao-qu-chen-zhuo-l1 640:360:0:200
c "$C" set-shanjiao-qu-chen-tian-l1 560:315:752:330
