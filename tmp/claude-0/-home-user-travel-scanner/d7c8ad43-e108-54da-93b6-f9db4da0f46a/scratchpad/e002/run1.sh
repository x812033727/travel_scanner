#!/usr/bin/env bash
# 第 2 集草稿：每支單獨送、9 分鐘逾時就重啟 kernel 重試；cuts；關 session；備份
set -uo pipefail
W=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/e002
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
export COLAB_GPU=G4; S=tn-e002a
H3_PROFILE=hero bash $K/bootstrap.sh patch >/dev/null
bash $K/h3.sh start --session $S --gpu G4 || exit 1
cd $W
for id in $(python3 -c "import json;print(' '.join(j['id'] for j in json.load(open('st1-all.json'))['jobs']))"); do
  [ -s out/$id.mp4 ] && continue
  python3 -c "import json,sys;d=json.load(open('st1-all.json'));json.dump({'jobs':[j for j in d['jobs'] if j['id']==sys.argv[1]]},open('one-'+sys.argv[1]+'.json','w'))" $id
  for try in 1 2; do
    timeout 600 bash $K/h3.sh batch --manifest one-$id.json --output-dir out --progress one-$id.p.json --session $S >/dev/null 2>&1
    [ -s out/$id.mp4 ] && { echo "== draft $id ok (try $try) $(date -u +%T)"; break; }
    echo "== draft $id failed (try $try)"; timeout 120 colab restart-kernel --session $S >/dev/null 2>&1; sleep 10
  done
done
bash $K/h3.sh cuts --input-dir out --output-dir trimmed --manifest st1-all.json | grep -v "no cut"
bash $K/h3.sh stop --session $S; bash $K/bootstrap.sh patch >/dev/null
echo "== drafts done $(date -u +%T) $(ls out/*.mp4 | wc -l)"; bash $K/h3.sh usage | tail -1
