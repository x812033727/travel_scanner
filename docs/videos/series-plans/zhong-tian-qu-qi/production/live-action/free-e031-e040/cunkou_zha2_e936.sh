#!/bin/bash
# arc 4 (2026-11-20, e036 r2 d1 prep): one more free crop of set-cunkou-zha2-l1 (the paid gate edit, cunkou_zha2_crops.sh has the
# rest): a new id, lanczos to 1312x736 (rules 19, 35).
#   -di: the bare dirt road before the gate only (e036 s05: the insert of Tang Xiaotang's gold abacus; rule 35, the ground and the
#        light of the background only)
# Usage: bash cunkou_zha2_e936.sh refs-live/set-cunkou-zha2-l1.png OUTDIR
set -e
S=$1; O=$2
ffmpeg -v error -y -i "$S" -vf "crop=256:144:330:592,scale=1312:736:flags=lanczos" -flags +bitexact -fflags +bitexact "$O/set-cunkou-zha2-di-l1.png"
