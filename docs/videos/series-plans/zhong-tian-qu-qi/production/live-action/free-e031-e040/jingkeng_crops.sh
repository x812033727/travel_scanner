#!/bin/bash
# arc 4 (2026-11-18, e032 r2): four close crops of the round-2 winner set-jingkeng-l1 (seed 37040, an edit of set-hantian-l1:
# one row of well pits and earth heaps running from the near left away to the far right across a cracked dry field, a golden
# willow at the right, a low sun from the left). Each is a new id with its own l1, lanczos to 1312x736 (rule 19, 35: close
# shots get a crop with real ground, never the whole wide).
# Usage: bash jingkeng_crops.sh refs-live/set-jingkeng-l1.png OUTDIR
set -e
Q=$1; O=$2
c() { ffmpeg -v error -y -i "$Q" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-jingkeng-kou-l1  640:360:0:376     # the near pit: its dark square mouth, the long wooden pole along its far rim, a wooden tub, the first heaps
c set-jingkeng-dui-l1  640:360:440:280   # the row of earth heaps running away to the right across the furrows, far roofs and hills
c set-jingkeng-tian-l1 640:360:672:150   # open sky, the willow and the dry field at the right: s24 (only sky and field behind her)
c set-jingkeng-di-l1   352:198:880:538   # cracked dry furrows with short dead stalks: s21 (looking down on him lying on the earth)
