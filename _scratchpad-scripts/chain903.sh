#!/usr/bin/env bash
# wait for the e902 refine driver to exit, then run the e903 stage-1 drafts (pod stops at the end)
while pgrep -f "route_a_st23.sh 902" >/dev/null; do sleep 30; done
cd /home/user/travel_scanner && bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 903 v1
