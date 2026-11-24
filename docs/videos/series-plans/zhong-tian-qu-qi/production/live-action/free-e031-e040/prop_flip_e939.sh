#!/bin/bash
# e039 r2 after the independent review (建議 1): the saddled horse prop-zaohongma-an-l1 (e938 fix6 Qwen 9381807) faces LEFT; the way
# back to Liuxi rides left to right, and H3 tends to keep a reference picture's direction (e938 s20). A free horizontal flip, new id:
#   prop-zaohongma-an-r-l1: the same horse, head toward the RIGHT (s08-s13). Checked: the felt pad, the rope girth and the bridle are
#   plain and nearly symmetric, the picture has no writing, the plain grey studio background has no direction.
# Usage: bash prop_flip_e939.sh REFS_LIVE_DIR OUTDIR
set -e
L=$1; O=$2
ffmpeg -v error -y -i "$L/prop-zaohongma-an-l1.png" -vf hflip -flags +bitexact -fflags +bitexact "$O/prop-zaohongma-an-r-l1.png"
