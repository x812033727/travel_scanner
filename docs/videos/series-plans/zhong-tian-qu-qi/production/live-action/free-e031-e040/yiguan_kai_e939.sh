#!/bin/bash
# e039 r2 after the independent review (必改 1, option A): the free crop of the paid Qwen edit set-yiguan-men-ye-kai-l1 (the clinic's
# two plank leaves pushed inward, warm lamp glow in the doorway; colab/runs/e939-live/qwen, scratchpad e939qwen.sh STEP=a / pick-a),
# with the same geometry as e938's -men crop of set-yiguan-men-ye-l1 (roads_e938.sh), so the step, the post and the door stay where
# they were. New id, lanczos to 1312x736. The whole -kai picture goes to s09.
#   set-yiguan-men-ye-kai-men-l1: the open clinic door, its stone step and the square stone hitching post at its left
#                                 (s01, s04, s05, s07, s08)                                                640:360 at 672,300
# Usage: bash yiguan_kai_e939.sh REFS_LIVE_DIR OUTDIR
set -e
L=$1; O=$2
ffmpeg -v error -y -i "$L/set-yiguan-men-ye-kai-l1.png" -vf "crop=640:360:672:300,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/set-yiguan-men-ye-kai-men-l1.png"
