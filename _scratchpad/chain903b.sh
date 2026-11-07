#!/usr/bin/env bash
# wait for the e902 refine driver to exit, run the e903 stage-1 drafts, then stop the pod (review takes a while)
while pgrep -f "route_a_st23.sh 902" >/dev/null; do sleep 30; done
cd /home/user/travel_scanner && bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 903 v1
echo "=== stop $(date -u +%T)"; bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh stop
