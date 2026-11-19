#!/bin/bash
# arc 4 (2026-11-19, e033 r2 d1 prep): the night hall for e033 c05-c11 (the beam taken down by torchlight). citang_ye_clean.py
# paints the beam's crack strokes out of the free night hall set-citang-ye-l1 (as citang_huang.py step (b) does for the dusk
# hall) -> set-citang-ye2-l1; then four crops of it (the plain wall under the beam is lit by the candles only, so -huang-qiang serves the night too: its crop box is right of the doorway zone and byte for byte the same) with the same boxes as citang_huang.sh's dusk crops, so a night shot frames
# the hall the way e032's dusk shots and e033 s01-s04 do. Each a new id with its own l1, lanczos to 1312x736. The torches are
# written in each shot, held one to a person (rule 37), never painted on.
# Usage: bash citang_ye_crops.sh refs-live/set-citang-ye-l1.png OUTDIR
set -e
Q=$1; O=$2; HERE=$(cd "$(dirname "$0")" && pwd)
F="$O/set-citang-ye2-l1.png"
python3 -I "$HERE/citang_ye_clean.py" "$Q" "$F" > /dev/null
c() { ffmpeg -v error -y -i "$F" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-citang-ye2-men-l1   512:288:60:180    # the doorway at night: the lattice leaf, the dark opening, the leaf swung back
c set-citang-ye2-liang-l1 640:360:580:0     # the dark main beam across the top of the wall, the tablets' tops below
c set-citang-ye2-tang-l1  832:468:480:268   # the altar side of the hall with its stone floor, no doorway
c set-citang-ye2-zuo-l1   640:360:400:300   # the swung-back leaf and the dark post, the table's left end, a candle, tablets
