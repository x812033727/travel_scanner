#!/usr/bin/env bash
# 草稿 chain：draft-chain.sh <工作資料夾> <manifest…>；START=1 開 session、STOP=1 跑完關機（SS 預設 tn-v2）。
# 單鏡 manifest 放在工作資料夾（prompts/ 同一層）；每支 timeout 600、重試一次；連三鏡失敗就停。用 Bash 背景指令跑（不要 setsid）。
set -uo pipefail
S=${TN_WORK:-$HOME/mokaair-work/videos/_tn-work}
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
export COLAB_GPU=G4; SS=${SS:-tn-v2}; D=$1; shift
H3_PROFILE=hero bash $K/bootstrap.sh patch >/dev/null
[ "${START:-0}" = 1 ] && { bash $K/h3.sh start --session $SS --gpu G4 || exit 1; }
mkdir -p $D/out; bad=0
for M in "$@"; do
  for id in $(python3 -c "import json;print(' '.join(j['id'] for j in json.load(open('$M'))['jobs']))"); do
    [ -s $D/out/$id.mp4 ] && continue
    python3 -c "import json,sys;d=json.load(open(sys.argv[1]));json.dump({'jobs':[j for j in d['jobs'] if j['id']==sys.argv[2]]},open(sys.argv[3],'w'))" $M $id $D/one-$id.json
    for try in 1 2; do (cd $D && timeout 600 bash $K/h3.sh batch --manifest one-$id.json --output-dir out --progress one-$id.p.json --session $SS >/dev/null 2>&1)
      [ -s $D/out/$id.mp4 ] && { echo "== $(basename $D) $id ok (try $try) $(date -u +%T)"; break; }
      echo "== $(basename $D) $id failed (try $try)"; [ $try = 2 ] && bad=$((bad+1)); timeout 120 colab restart-kernel --session $SS >/dev/null 2>&1; sleep 10; done
    [ -s $D/out/$id.mp4 ] && bad=0; [ $bad -ge 3 ] && { echo "== ABORT"; break 2; }
  done
done
echo "== $(basename $D) drafts chunk done $(date -u +%T)"
[ "${STOP:-0}" = 1 ] && { bash $K/h3.sh stop --session $SS; [ "${UNPATCH:-0}" = 1 ] && bash $K/bootstrap.sh patch >/dev/null; (cd $D && bash $K/h3.sh cuts --input-dir out --output-dir trimmed | grep -v "no cut"); bash $K/h3.sh usage | tail -1; }
