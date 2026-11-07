#!/usr/bin/env bash
set -uo pipefail
W=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/e001
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
P=/home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post
export COLAB_GPU=G4
S=tn-e001b
cd $W
H3_PROFILE=hero bash $K/bootstrap.sh patch >/dev/null
# c12 兩個 take 的草稿
(cd retake2 && bash $K/h3.sh batch --manifest retake2.json --output-dir out --progress p.json --session $S)
python3 -I $P/st2.py --st1 retake2/st1-c12.json --drafts retake2/out --work retake2/st2
# 還沒補的鏡（跳過已完成與舊的 c12）
done_ids=$(ls st2/refined/*.mp4 2>/dev/null | xargs -n1 basename | sed 's/\.mp4$//' | tr '\n' ' ')
for f in st2/st2-part1.json st2/st2-part2.json; do
  only=$(python3 -c "
import json,sys
d=set(sys.argv[2].split()); d.add('c12')
print(','.join(j['id'] for j in json.load(open(sys.argv[1]))['jobs'] if j['id'] not in d))" $f "$done_ids")
  [ -n "$only" ] && bash $K/h3.sh refine --manifest $f --output-dir st2/refined --session $S --only $only
done
bash $K/h3.sh refine --manifest retake2/st2/st2-part1.json --output-dir retake2/st2/refined --session $S
bash $K/h3.sh stop --session $S
bash $K/bootstrap.sh patch >/dev/null
ls st2/refined/*.mp4 | wc -l; ls retake2/st2/refined
bash $K/h3.sh usage | tail -1
