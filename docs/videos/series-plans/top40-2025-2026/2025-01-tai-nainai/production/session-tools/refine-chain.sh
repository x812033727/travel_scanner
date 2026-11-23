#!/usr/bin/env bash
# 精修 chain：refine-chain.sh <工作資料夾> <st2 manifest…>；輸出到 <工作資料夾>/refined；SS 是開著的 session；STOP=1 跑完關機。
set -uo pipefail; shopt -s nullglob
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
SS=${SS:-tn-v2}; D=$1; shift; mkdir -p $D/refined; bad=0
for f in "$@"; do python3 $K/refine.py --manifest $f --check >/dev/null || { echo "== bad manifest $f"; continue; }
  for id in $(python3 -c "import json;print(' '.join(j['id'] for j in json.load(open('$f'))['jobs']))"); do
    [ -f $D/refined/$id.mp4 ] && [ $D/refined/$id.mp4 -nt $f ] && continue
    for try in 1 2; do (cd $D && timeout 540 bash $K/h3.sh refine --manifest $f --output-dir refined --session $SS --only $id >/dev/null 2>&1)
      [ $D/refined/$id.mp4 -nt $f ] && { echo "== refined $id ok (try $try) $(date -u +%T)"; break; }
      echo "== refine $id failed (try $try)"; [ $try = 2 ] && bad=$((bad+1)); timeout 120 colab restart-kernel --session $SS >/dev/null 2>&1; sleep 10; done
    [ $D/refined/$id.mp4 -nt $f ] && bad=0; [ $bad -ge 3 ] && { echo "== ABORT"; break 2; }
  done
done
echo "== refine chunk done $(date -u +%T)"
[ "${STOP:-0}" = 1 ] && { bash $K/h3.sh stop --session $SS; [ "${UNPATCH:-0}" = 1 ] && bash $K/bootstrap.sh patch >/dev/null; bash $K/h3.sh usage | tail -1; }
