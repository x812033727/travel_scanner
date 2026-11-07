#!/usr/bin/env bash
set -uo pipefail
W=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/e001
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
P=/home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post
export COLAB_GPU=G4; S=tn-e001e
python3 -c "
import json,sys
ids=['c09','c22','c23','c27','c14','c15','c20']
json.dump({'jobs':[j for j in json.load(open(sys.argv[1]))['jobs'] if j['id'] in ids]},open(sys.argv[2],'w'),indent=1)" $W/retake8/st1-all.json $W/retake8/st1-picks9.json
rm -rf $W/retake8/st2
python3 -I $P/st2.py --st1 $W/retake8/st1-picks9.json --drafts $W/retake8/trimmed \
  --take c09=$W/retake6/trimmed/c09-r1.mp4 --take c22=$W/retake6/trimmed/c22-r1.mp4 --take c23=$W/retake6/trimmed/c23-r1.mp4 \
  --take c27=$W/retake6/trimmed/c27-r1.mp4 --take c14=$W/retake7/trimmed/c14-r2.mp4 --take c15=$W/retake7/trimmed/c15-r1.mp4 \
  --take c20=$W/retake8/trimmed/c20-r1.mp4 --work $W/retake8/st2 || { bash $K/h3.sh stop --session $S; exit 1; }
M=$W/retake8/st2/st2-part1.json
python3 $K/refine.py --manifest $M --check || { bash $K/h3.sh stop --session $S; exit 1; }
for id in c09 c14 c15 c20 c22 c23 c27; do
  for try in 1 2; do
    (cd $W && timeout 540 bash $K/h3.sh refine --manifest $M --output-dir st2/refined --session $S --only $id >/dev/null 2>&1)
    [ st2/refined/$id.mp4 -nt $M ] 2>/dev/null || [ $W/st2/refined/$id.mp4 -nt $M ] && { echo "== refined $id ok (try $try) $(date -u +%T)"; break; }
    echo "== refine $id timed out (try $try)"; timeout 120 colab restart-kernel --session $S >/dev/null 2>&1; sleep 10
  done
done
bash $K/h3.sh stop --session $S; bash $K/bootstrap.sh patch >/dev/null
echo "== done $(date -u +%T)"; bash $K/h3.sh usage | tail -1
