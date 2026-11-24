#!/bin/bash
# e039 r2 d1 prep (2026-11-24, free): one crop of the night sickroom set-xujia-tangfang-kong-l1 (e938's paid Qwen edit 9381224:
# the table gone, the stool with its lit candle at the bed's foot) for the insert s19 (rule 35: an insert gets the close ground
# of its background, never the whole room). New id, lanczos to 1312x736.
#   set-xujia-tangfang-kong-bei-l1: the pink quilted cover and the dark wooden bed rail close, in the warm small light (s19)   352:198 at 600,440
# After the independent review (必改 4: a close-up in front of the bed shows an empty bed): window-and-wall crops with no bed in them,
# from the night picture and from its first-light twin set-xujia-tangfang-kong-chen-l1 (e938's paid edit 9381221):
#   -kong-chuang2-l1 / -kong-chen-chuang2-l1: the small window and the back wall above the bed, the bed out of frame  560:315 at 620,60
#   -kong-qiang-l1 / -kong-chen-qiang-l1: the right half of the window and the wall above the pillow, the pillow out of frame  480:270 at 820,100
# Usage: bash xujia_tangfang_e939.sh REFS_LIVE_DIR OUTDIR
set -e
L=$1; O=$2
ffmpeg -v error -y -i "$L/set-xujia-tangfang-kong-l1.png" -vf "crop=352:198:600:440,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/set-xujia-tangfang-kong-bei-l1.png"
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
for k in kong kong-chen; do
  c "$L/set-xujia-tangfang-$k-l1.png" set-xujia-tangfang-$k-chuang2-l1 560:315:620:60
  c "$L/set-xujia-tangfang-$k-l1.png" set-xujia-tangfang-$k-qiang-l1   480:270:820:100
done
