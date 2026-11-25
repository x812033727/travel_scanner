#!/bin/bash
# arc 4 (2026-11-20, e035 r2 d1 prep): free crops of set-cunkou-l1 (screen test round 2, 37040: a free-standing palisade gate of
# upright logs with crossed braces and a small tiled roof at the LEFT, a weeping willow in the middle, a plank bridge over a dry
# stone-lined ditch, a dirt road curving away to three small mud-brick houses at the RIGHT, dry fields and far hills under an
# orange-red evening sky; no fences either side of the gate, no gate tower), each a new id, lanczos to 1312x736 (rules 19, 35).
# e035 scene 3 (the village entrance five days later at dusk; e036 scene 1 the same moment).
#   -men:  the gate, its braces and crossbar, the willow's trunk and the bridge (s28, s29, s32, s34: toward the gate)
#   -zha:  the gate's logs and its thick horizontal crossbar close (s35: the insert of the hand on the bar)
#   -ding: the gate's tiled roof against the orange-red sky (s31: Qian Yuanwai up beside the gate, a low angle)
#   -kong: the orange-red sky over the far hills, the willow's fronds at the left edge (s27, s30: Xu Yan's close-ups)
#   -dao:  the dirt road and the three houses at the right (s33: A-ling from the village road)
# set-cunkou-l1 itself is sent to the wide s26.
# Usage: bash cunkou_crops.sh refs-live/set-cunkou-l1.png OUTDIR
set -e
S=$1; O=$2
c() { ffmpeg -v error -y -i "$S" -vf "crop=$2,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/$1.png"; }
c set-cunkou-men-l1  720:405:0:200
c set-cunkou-zha-l1  400:225:150:380
c set-cunkou-ding-l1 640:360:0:40
c set-cunkou-kong-l1 600:338:700:20
c set-cunkou-dao-l1  640:360:672:300
