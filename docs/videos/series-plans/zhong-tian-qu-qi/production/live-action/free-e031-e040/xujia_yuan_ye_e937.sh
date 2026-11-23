#!/bin/bash
# e037 r2 d1 prep (2026-11-23): two more free crops of set-xujia-yuan-ye-dong2-l1 (e931's night yard, the e036 crops are in
# xujia_yuan_ye_e936.sh) for e037 scene 1, the same yard at the same moment as e036's last shot. New ids, lanczos to 1312x736.
#   -shu: the bare tree's branches against the night sky, the far dark hills at the right, the edge of the gate roof at the
#         lower left (the script's 「身後只有柿子樹的枝葉」: Wang Erniu's close-up s02, Xu Yan's close-up s03)
#   -di:  the packed earth of the yard in the warm glow, a few flat stones (the insert s08, ground and light only)
# Usage: bash xujia_yuan_ye_e937.sh refs-live/set-xujia-yuan-ye-dong2-l1.png OUTDIR
set -e
S=$1; O=$2
c() { ffmpeg -v error -y -i "$1" -vf "crop=$3,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$2.png"; }
c "$S" set-xujia-yuan-ye-dong2-shu-l1 560:315:560:0
c "$S" set-xujia-yuan-ye-dong2-di-l1  480:270:300:466
