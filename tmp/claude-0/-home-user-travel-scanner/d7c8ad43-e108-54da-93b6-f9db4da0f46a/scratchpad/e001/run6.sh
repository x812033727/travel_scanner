#!/usr/bin/env bash
# 第 1 集：重拍 13 支 → 精修沒重拍的 13 鏡 → 等 picks.txt（<鏡>=<retake3/out 的檔>）→ 精修挑好的 → 關 session
set -uo pipefail
W=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/e001
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
P=/home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post
export COLAB_GPU=G4
S=tn-e001b
H3_PROFILE=hero bash $K/bootstrap.sh patch >/dev/null
echo "== retakes $(date -u +%T)"
(cd $W/retake3 && bash $K/h3.sh batch --manifest retake3.json --output-dir out --progress p.json --session $S)
(cd $W && bash $K/h3.sh cuts --input-dir retake3/out --output-dir retake3/trimmed)
echo "== refine the rest $(date -u +%T)"
cd $W
REST=c09,c10,c11,c13,c14,c19,c20,c21,c23,c24,c25,c26,c27
for f in st2/st2-part1.json st2/st2-part2.json; do
  only=$(python3 -c "
import json,sys
want=set(sys.argv[2].split(','))
print(','.join(j['id'] for j in json.load(open(sys.argv[1]))['jobs'] if j['id'] in want))" $f $REST)
  [ -n "$only" ] && bash $K/h3.sh refine --manifest $f --output-dir st2/refined --session $S --only $only
done
echo "== waiting for picks $(date -u +%T)"
for i in $(seq 1 90); do [ -f $W/picks.txt ] && break; sleep 20; done
if [ -f $W/picks.txt ]; then
  takes=$(sed 's/^/--take /' $W/picks.txt | tr '\n' ' ')
  python3 -c "
import json,sys
ids=[l.split('=')[0] for l in open(sys.argv[1]).read().split()]
allj=json.load(open(sys.argv[2]))['jobs']
json.dump({'jobs':[j for j in allj if j['id'] in ids]},open(sys.argv[3],'w'),indent=1)" $W/picks.txt $W/retake3/st1-all.json $W/retake3/st1-picks.json
  python3 -I $P/st2.py --st1 $W/retake3/st1-picks.json --drafts $W/retake3/trimmed $takes --work $W/retake3/st2 && \
  for f in $W/retake3/st2/st2-part*.json; do python3 $K/refine.py --manifest $f --check && bash $K/h3.sh refine --manifest $f --output-dir st2/refined --session $S; done
else
  echo "== no picks.txt after 30 min; stopping without refining the retakes"
fi
bash $K/h3.sh stop --session $S
bash $K/bootstrap.sh patch >/dev/null
echo "== done $(date -u +%T)"; ls st2/refined/*.mp4 | wc -l
bash $K/h3.sh usage | tail -1
