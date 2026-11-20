#!/bin/bash
# arc 4 (2026-11-20, e036 r2 d1 prep): one more free crop of set-cunkou-zha2-l1 (the paid gate edit, cunkou_zha2_crops.sh has the
# rest): a new id, lanczos to 1312x736 (rules 19, 35).
#   -di: the bare dirt road before the gate only (e036 s05: the insert of Tang Xiaotang's gold abacus; rule 35, the ground and the
#        light of the background only)
# After the e036 independent review (2026-11-20, 必改 1, 3): two crops with no shut gate leaves in them, for the shots after the
# gate is swung back (s02):
#   -wai2:  the corner of the gate's tiled roof at the top left and the crossbar leaning against the post at the left edge, the
#           willow, the ditch and its plank bridge, the road and two houses with the short fence at the right (s02 until the paid
#           open-gate picture exists, s06, s07, s12b)
#   -ding2: the small tiled roof against the orange-red sky only, a strip of its beam at the bottom (s03, s04, s10)
# Usage: bash cunkou_zha2_e936.sh refs-live/set-cunkou-zha2-l1.png OUTDIR
set -e
S=$1; O=$2
ffmpeg -v error -y -i "$S" -vf "crop=256:144:330:592,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/set-cunkou-zha2-di-l1.png"
ffmpeg -v error -y -i "$S" -vf "crop=680:383:440:222,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/set-cunkou-zha2-wai2-l1.png"
ffmpeg -v error -y -i "$S" -vf "crop=448:252:60:12,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/set-cunkou-zha2-ding2-l1.png"
