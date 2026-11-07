#!/usr/bin/env bash
set -uo pipefail
W=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/e001
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
P=/home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post
cd $W
export COLAB_GPU=G4
bash $K/h3.sh start --session tn-e001b --gpu G4 || exit 1
bash $K/h3.sh batch --manifest retake/retake.json --output-dir retake/out --progress retake/p.json --session tn-e001b
ls retake/out
python3 -I $P/st2.py --st1 retake/st1-all.json --drafts trimmed --take c12=$W/retake/out/c12.mp4 --take c23=$W/retake/out/c23.mp4 --work st2 || { bash $K/h3.sh stop --session tn-e001b; exit 1; }
for f in st2/st2-part*.json; do python3 $K/refine.py --manifest $f --check || { bash $K/h3.sh stop --session tn-e001b; exit 1; }; done
for f in st2/st2-part*.json; do bash $K/h3.sh refine --manifest $f --output-dir st2/refined --session tn-e001b; done
bash $K/h3.sh stop --session tn-e001b
bash $K/bootstrap.sh patch >/dev/null
ls st2/refined/*.mp4 | wc -l
bash $K/h3.sh usage | tail -1
