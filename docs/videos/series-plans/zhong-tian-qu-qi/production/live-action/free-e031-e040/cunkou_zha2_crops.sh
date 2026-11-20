#!/bin/bash
# arc 4 (2026-11-20, e035 independent review 建議 1, the coordinator's decision): free crops of set-cunkou-zha2-l1, the paid edit
# of set-cunkou-l1 (Qwen-Image-Edit, one change: the solid palisade under the small tiled roof becomes a pair of gate leaves of
# upright logs with a seam down the middle, two horizontal rails across both leaves held by plain iron fittings at the seam, the
# lower one at waist height being the crossbar; a log fence runs off at the left of the gate and a short stretch stands at the
# lower right; roof, willow, bridge, road, houses, hills and sky as before; seed 9351204, colab/runs/e935-live/cunkou-zha2/).
# Each a new id, lanczos to 1312x736 (rules 19, 35). e035 scene 3 and e036 scene 1 (the same moment) send these; the first
# set-cunkou crops (cunkou_crops.sh: a solid palisade, no gate leaves, no fence) are no longer sent.
#   -men:  the two gate leaves, their rails and iron fittings, the fence at the left, the willow and the bridge (s28, s32, s34)
#   -zha:  the leaves' logs and the lower rail with its iron fitting at the seam close (s35: the insert of the hand on the bar)
#   -ding: the small tiled roof against the orange-red sky (s31: Qian Yuanwai up beside the gate, a low angle)
#   -kong: the orange-red sky over the far hills, the willow's fronds at the left edge (s27, s30: Xu Yan's close-ups)
#   -dao:  the three small houses and the far hills, above the short fence at the lower right (s33)
#   -wai:  the gate's right post only at the left edge, the willow, the ditch and its plank bridge, the dry ground, the houses and
#          the short fence at the right (s29: the refugees beyond the gate; independent review 必改 3)
# set-cunkou-zha2-l1 itself is sent to the wide s26.
# Usage: bash cunkou_zha2_crops.sh refs-live/set-cunkou-zha2-l1.png OUTDIR
set -e
S=$1; O=$2
c() { ffmpeg -v error -y -i "$S" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-cunkou-zha2-men-l1  720:405:0:200
c set-cunkou-zha2-zha-l1  400:225:120:340
c set-cunkou-zha2-ding-l1 640:360:0:40
c set-cunkou-zha2-kong-l1 600:338:700:20
c set-cunkou-zha2-dao-l1  640:270:672:160
c set-cunkou-zha2-wai-l1  720:405:360:220
