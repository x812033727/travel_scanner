#!/bin/bash
# e037 r2 d1 prep (2026-11-23): free crops of set-xujia-houmen-ye-l1 (screen test round 1, 37038: the Xu farmhouse's back gate by
# night: a long low wall of rough stone running from the far left into the frame, a narrow plank door in it at the RIGHT standing
# ajar inward with warm light inside, split logs stacked against the wall just left of the door, the dark alley running away
# to the LEFT along the wall, bare trees, a full moon high in the middle). Each a new id, lanczos to 1312x736 (rules 19, 35).
#   (the picture itself: the wide of the alley, s31)
#   -men:   the door standing ajar, its warm-lit doorway and the logs beside it (s29, s30)
#   -xiang: the dark alley running away to the left along the wall (seen from the doorway: s32, s33, s34)
#   (a crop of the stone wall right of the door was tried: too dark and flat to read as a place, not made)
# Usage: bash xujia_houmen_e937.sh refs-live/set-xujia-houmen-ye-l1.png OUTDIR
set -e
S=$1; O=$2
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
c "$S" set-xujia-houmen-ye-men-l1   640:360:440:340
c "$S" set-xujia-houmen-ye-xiang-l1 640:360:0:300
