#!/bin/bash
# arc 4 (2026-11-20, e035 r2 d1 prep): free crops of set-xujia-wu-ye-l1 (e922's night room, 37033: earthen brick walls, a small
# window in the back wall at the left showing the dark blue night, a small dark square table in the middle-right with one small
# flame on it, a big clay jar at the left, a clay basin and loose straw on the floor), each a new id, lanczos to 1312x736
# (rules 19, 35; bible rule 42: the room of e035 scene 1). set-xujia-wu-ye-l1 itself and e922's set-xujia-wu-ye-table-l1 are
# sent as they are.
#   -chuang: the window and the brick wall round it, the flame out of the frame (s02, s02b, s06, s10: Xu Yan by the wall)
#   -qiang:  the dark brick wall at the right of the table, the flame out of the frame (s11: Tang Xiaotang's one front face)
#   -zhuo:   the table and its flame with the wall behind (s07: the abacus insert, the tabletop as its ground)
#   -di:     the table's legs and the straw floor under and round it (s05: little Xiaohe under the table, a low angle)
# Usage: bash xujia_wu_ye_crops.sh refs-live/set-xujia-wu-ye-l1.png OUTDIR
set -e
S=$1; O=$2
c() { ffmpeg -v error -y -i "$S" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-xujia-wu-ye-chuang-l1 560:315:170:140
c set-xujia-wu-ye-qiang-l1  520:292:792:200
c set-xujia-wu-ye-zhuo-l1   480:270:540:380
c set-xujia-wu-ye-di-l1     560:315:500:421
