#!/bin/bash
# e039 r2 d1 prep (2026-11-24, free): one crop of the night sickroom set-xujia-tangfang-kong-l1 (e938's paid Qwen edit 9381224:
# the table gone, the stool with its lit candle at the bed's foot) for the insert s19 (rule 35: an insert gets the close ground
# of its background, never the whole room). New id, lanczos to 1312x736.
#   set-xujia-tangfang-kong-bei-l1: the pink quilted cover and the dark wooden bed rail close, in the warm small light (s19)   352:198 at 600,440
# Usage: bash xujia_tangfang_e939.sh REFS_LIVE_DIR OUTDIR
set -e
L=$1; O=$2
ffmpeg -v error -y -i "$L/set-xujia-tangfang-kong-l1.png" -vf "crop=352:198:600:440,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/set-xujia-tangfang-kong-bei-l1.png"
