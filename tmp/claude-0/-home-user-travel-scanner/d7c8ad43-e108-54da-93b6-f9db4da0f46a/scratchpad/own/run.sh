#!/usr/bin/env bash
# 模型原聲重拍（站主 2026-11-07）：第 1、2 集說話的鏡帶台詞，各兩個 take；每支單獨送、10 分鐘逾時重啟重試；完成後關 session、備份
set -uo pipefail
S=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
export COLAB_GPU=G4; SS=${SESSION:-tn-own1}
H3_PROFILE=hero bash $K/bootstrap.sh patch >/dev/null
[ -n "${REUSE:-}" ] || bash $K/h3.sh start --session $SS --gpu G4 || exit 1
for E in e001 e002; do
  D=$S/own/$E
  for id in $(python3 -c "import json;print(' '.join(j['id'] for j in json.load(open('$D/retake.json'))['jobs']))"); do
    [ -s $D/out/$id.mp4 ] && continue
    python3 -c "import json,sys;d=json.load(open(sys.argv[1]));json.dump({'jobs':[j for j in d['jobs'] if j['id']==sys.argv[2]]},open(sys.argv[3],'w'))" $D/retake.json $id $D/one-$id.json
    for try in 1 2; do
      (cd $D && timeout 600 bash $K/h3.sh batch --manifest one-$id.json --output-dir out --progress one-$id.p.json --session $SS >/dev/null 2>&1)
      [ -s $D/out/$id.mp4 ] && { echo "== $E $id ok (try $try) $(date -u +%T)"; break; }
      echo "== $E $id failed (try $try)"; timeout 120 colab restart-kernel --session $SS >/dev/null 2>&1; sleep 10
    done
  done
  (cd $D && bash $K/h3.sh cuts --input-dir out --output-dir trimmed | grep -v "no cut")
done
bash $K/h3.sh stop --session $SS; bash $K/bootstrap.sh patch >/dev/null
echo "== drafts done $(date -u +%T)"; bash $K/h3.sh usage | tail -1
