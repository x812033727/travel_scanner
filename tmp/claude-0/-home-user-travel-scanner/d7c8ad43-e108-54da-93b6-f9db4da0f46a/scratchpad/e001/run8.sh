#!/usr/bin/env bash
# 新帳號：16 支重拍（每鏡兩個 take）＋不用重拍的 13 鏡精修；每支單獨送、9 分鐘逾時就重啟 kernel 重試一次
set -uo pipefail
W=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/e001
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
export COLAB_GPU=G4
S=tn-e001e
H3_PROFILE=hero bash $K/bootstrap.sh patch >/dev/null
bash $K/h3.sh start --session $S --gpu G4 || exit 1
one() {  # one <dir> <manifest> <id>  — 單支草稿
  local d=$1 m=$2 id=$3
  python3 -c "import json,sys;d=json.load(open(sys.argv[1]));json.dump({'jobs':[j for j in d['jobs'] if j['id']==sys.argv[2]]},open(sys.argv[3],'w'))" $d/$m $id $d/one-$id.json
  for try in 1 2; do
    (cd $d && timeout 540 bash $K/h3.sh batch --manifest one-$id.json --output-dir out --progress one-$id.p.json --session $S >/dev/null 2>&1)
    [ -s $d/out/$id.mp4 ] && { echo "== draft $id ok (try $try) $(date -u +%T)"; return 0; }
    echo "== draft $id failed or timed out (try $try); restarting kernel"; timeout 120 colab restart-kernel --session $S >/dev/null 2>&1; sleep 10
  done
}
ref() {  # ref <manifest> <id> <outdir>  — 單支精修
  local m=$1 id=$2 o=$3
  for try in 1 2; do
    (cd $W && timeout 540 bash $K/h3.sh refine --manifest $m --output-dir $o --session $S --only $id >/dev/null 2>&1)
    [ -s $o/$id.mp4 ] && [ $o/$id.mp4 -nt $m ] && { echo "== refined $id ok (try $try) $(date -u +%T)"; return 0; }
    echo "== refine $id failed or timed out (try $try); restarting kernel"; timeout 120 colab restart-kernel --session $S >/dev/null 2>&1; sleep 10
  done
}
for id in $(python3 -c "import json;print(' '.join(j['id'] for j in json.load(open('$W/retake6/retake6.json'))['jobs']))"); do one $W/retake6 retake6.json $id; done
(cd $W && bash $K/h3.sh cuts --input-dir retake6/out --output-dir retake6/trimmed | grep -v "no cut")
echo "== drafts done $(date -u +%T)"
for id in; do
  m=$W/st2/st2-part1.json; grep -q "\"id\": \"$id\"" $m || m=$W/st2/st2-part2.json
  ref $m $id $W/st2/refined
done
echo "== rest refined $(date -u +%T); waiting for picks.txt"
for i in $(seq 1 45); do [ -f $W/picks6.txt ] && break; sleep 20; done
if [ -f $W/picks6.txt ]; then
  takes=$(sed 's/^/--take /' $W/picks6.txt | tr '\n' ' ')
  python3 -c "
import json,sys
ids=[l.split('=')[0] for l in open(sys.argv[1]).read().split()]
json.dump({'jobs':[j for j in json.load(open(sys.argv[2]))['jobs'] if j['id'] in ids]},open(sys.argv[3],'w'),indent=1)" $W/picks6.txt $W/retake6/st1-all.json $W/retake6/st1-picks.json
  rm -rf $W/retake6/st2; python3 -I /home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post/st2.py --st1 $W/retake6/st1-picks.json --drafts $W/retake6/trimmed $takes --work $W/retake6/st2
  for f in $W/retake6/st2/st2-part*.json; do python3 $K/refine.py --manifest $f --check || continue
    for id in $(python3 -c "import json,sys;print(' '.join(j['id'] for j in json.load(open(sys.argv[1]))['jobs']))" $f); do ref $f $id $W/st2/refined; done
  done
else echo "== no picks after 15 min"; fi
bash $K/h3.sh stop --session $S; bash $K/bootstrap.sh patch >/dev/null
echo "== done $(date -u +%T) refined $(ls $W/st2/refined/*.mp4 | wc -l)"; bash $K/h3.sh usage | tail -1
