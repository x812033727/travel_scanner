#!/bin/bash
# e038 r2 d1 prep (2026-11-23): free crops of the three night pictures of e038 scenes 2 and 3 (screen test of arc 4:
# set-guandao-ye-l1 37039, set-chengmen-ye-l1 37038 with its plaque painted out, set-yiguan-men-ye-l1 37039). Each a new id,
# lanczos to 1312x736 (rules 19, 35). Bible rule 41: the ride is seen side-on, right to left (Liuxi at the right, the county
# town at the left); rule 33: nothing hung (no notice board, no signboard, no milestone).
#   set-guandao-ye-ce-l1:  the left half: the long line of dark poplars running across the frame, the flat dark field before it
#                          and the night sky above (the side-on gallop, s20)
#   set-guandao-ye-ce2-l1: (independent review 必改 4) the poplar line, the flat ground at its foot and the night sky only, the
#                          road receding to the right cut away but a corner (the side-on gallop along the track, s20; -ce no longer sent)
#   set-guandao-ye-shu-l1: closer on the poplar line and the field (the rider waist-up beside the horse's head and neck, s21)
#   set-chengmen-ye-zha-l1: the half-swung gate leaf and its torch at the left, the waist-high barrier of crossed wooden stakes
#                          running across the frame, the paving before it (the halt, the charge, s22, s27)
#   set-chengmen-ye-qiang-l1: the lit brick wall, the right torch in its iron holder, the top of the barrier (the captain, s23, s26)
#   set-chengmen-ye-men-l1: the closed left leaf, the half-swung right leaf and the left torch (the young guard, the gate, s24, s28)
#   set-chengmen-ye-lu-l1:  the far end of the barrier, the long dark wall and the road back toward the right (A-ling on the
#                          horse facing left, s25)
#   set-yiguan-men-ye-men-l1: the near two-leaf plank door, its two stone steps and the square stone hitching post at its left
#                          (s29, s30, s33, s36)
#   set-yiguan-men-ye-feng-l1: the seam between the two door leaves, close (the insert, s31)
#   set-yiguan-men-ye-jie-l1: the stone-paved street running away to the far end at the left (the crossbowmen, s32, s35, s37, s38)
#   set-yiguan-men-ye-di-l1:  the stone paving, close (the insert of the crossbows, s34)
# Usage: bash roads_e938.sh REFS_LIVE_DIR OUTDIR
set -e
L=$1; O=$2
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
c "$L/set-guandao-ye-l1.png" set-guandao-ye-ce-l1      720:405:0:210
c "$L/set-guandao-ye-l1.png" set-guandao-ye-shu-l1     560:315:40:200
c "$L/set-guandao-ye-l1.png" set-guandao-ye-ce2-l1     520:292:0:228
c "$L/set-chengmen-ye-l1.png" set-chengmen-ye-zha-l1   736:414:400:310
c "$L/set-chengmen-ye-l1.png" set-chengmen-ye-qiang-l1 480:270:430:260
c "$L/set-chengmen-ye-l1.png" set-chengmen-ye-men-l1   560:315:150:300
c "$L/set-chengmen-ye-l1.png" set-chengmen-ye-lu-l1    560:315:752:330
c "$L/set-yiguan-men-ye-l1.png" set-yiguan-men-ye-men-l1  640:360:672:300
c "$L/set-yiguan-men-ye-l1.png" set-yiguan-men-ye-feng-l1 352:198:800:330
c "$L/set-yiguan-men-ye-l1.png" set-yiguan-men-ye-jie-l1  640:360:100:260
c "$L/set-yiguan-men-ye-l1.png" set-yiguan-men-ye-di-l1   480:270:240:466
