#!/bin/bash
# arc 4 (2026-11-18, e032 r2): the ancestral hall at dusk (citang_huang.py: the doorway's daylight to a dim orange dusk, the
# crack strokes on the main beam painted out) and seven crops of it, each a new id with its own l1, lanczos to 1312x736.
# Usage: bash citang_huang.sh refs-live/set-citang-l1.png OUTDIR
set -e
Q=$1; O=$2; HERE=$(cd "$(dirname "$0")" && pwd)
F="$O/set-citang-huang-l1.png"
python3 -I "$HERE/citang_huang.py" "$Q" "$F" > /dev/null
c() { ffmpeg -v error -y -i "$F" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-citang-huang-men-l1   512:288:60:180    # the doorway: the lattice leaf at the left, the opening, the leaf swung back at the right
c set-citang-huang-qiang-l1 400:225:900:20    # the plain candle-warmed back wall under the end of the beam (no tablets, no incense, no flame)
c set-citang-huang-liang-l1 640:360:580:0     # the dark main beam across the top of the wall, the tops of the tablets and the incense below
c set-citang-huang-zhuo-l1  640:360:600:250   # the altar table: five plain tablets, the bronze censer with incense, the two candles
c set-citang-huang-tang-l1  832:468:480:268   # the altar side of the hall with its stone floor, no doorway: s33
# e032 r2 review 必改 6 (2026-11-18): the LEFT END of the altar table, where Elder Han kneels side-on looking right at the tablets
c set-citang-huang-zuo-l1   640:360:400:300   # the swung-back door leaf and the dark post at the left, the table's left end, the left candle, the tablets and the censer: s34
c set-citang-huang-zuo2-l1  480:270:520:250   # the table's left end, the left candle, two tablets and the censer: s35
