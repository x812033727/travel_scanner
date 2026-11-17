#!/bin/bash
# arc 4 (2026-11-17, e031 review 必改 6): the bare branches against the bright hazy sky for the s18 insert (the buds on a twig).
# crop=320:180:480:0 of set-xujia-yuan-han-l1 leaves the sun outside the frame to the right (the -dong-shu box 480:270:560:0
# puts the sun disc in the branches: the buds would go black against it). Lanczos to 1312x736, new id.
# Usage: bash han_extra.sh refs-live/set-xujia-yuan-han-l1.png OUTDIR
set -e
ffmpeg -v error -y -i "$1" -vf "crop=320:180:480:0,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$2/set-xujia-yuan-han-shu-l1.png"
