#!/usr/bin/env bash
set -uo pipefail
W=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/e001
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
P=/home/user/travel_scanner/docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai/production/post
# 等上一輪（run2）收完 session
until [ -s /tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/tasks/bolrxfmgf.output ]; do sleep 20; done
cd $W/retake2
export COLAB_GPU=G4
H3_PROFILE=hero bash $K/bootstrap.sh patch >/dev/null
bash $K/h3.sh start --session tn-e001c --gpu G4 || exit 1
bash $K/h3.sh batch --manifest retake2.json --output-dir out --progress p.json --session tn-e001c
python3 -I $P/st2.py --st1 st1-c12.json --drafts out --work st2 && python3 $K/refine.py --manifest st2/st2-part1.json --check && \
  bash $K/h3.sh refine --manifest st2/st2-part1.json --output-dir st2/refined --session tn-e001c
bash $K/h3.sh stop --session tn-e001c
bash $K/bootstrap.sh patch >/dev/null
ls out st2/refined
bash $K/h3.sh usage | tail -1
