#!/bin/bash
# arc 4 (2026-11-17): crops of the round-1 winner set-xujia-yuan-han-l1 (seed 37038, an edit of
# set-xujia-yuan-dong-qing2-l1 with the same layout), same crop boxes as the -dong-* set (e930tools/crops.sh, crops2.sh)
set -e
Q=$1; O=$2
c() { ffmpeg -v error -y -i "$Q" -vf "crop=$2,scale=1312:736:flags=lanczos" "$O/$1.png"; }
c set-xujia-yuan-han-men-l1   512:288:380:148
c set-xujia-yuan-han-jing-l1  480:270:832:446
c set-xujia-yuan-han-qiang-l1 288:162:1024:280
c set-xujia-yuan-han-wu-l1    640:360:0:240
c set-xujia-yuan-han-di-l1    304:171:386:565
