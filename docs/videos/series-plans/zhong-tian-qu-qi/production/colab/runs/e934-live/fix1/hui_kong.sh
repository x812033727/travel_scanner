#!/bin/bash
# e934 fix1 s37 (free): set-hantian-hui-kong-l1 = set-hantian-hui-l1 crop=448:252:150:0, lanczos to 1312x736: only the darkening
# grey-blue sky over the fields (no hills, houses, tree or furrows). d1 sent set-hantian-hui-tian-l1 (sky, far hills, houses and a
# strip of field): both takes put little Xiaohe standing on the field with the horizon at her waist, while s34 and s39 have her
# on Xu Yan's shoulders. Written as the colour of the sky only (bible rule 35, as e934 s03 and e933 s27).
# Usage: bash hui_kong.sh refs-live/set-hantian-hui-l1.png refs-live/set-hantian-hui-kong-l1.png
set -e
ffmpeg -v error -y -i "$1" -vf "crop=448:252:150:0,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$2"
