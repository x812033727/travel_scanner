#!/usr/bin/env bash
cd /home/user/travel_scanner
while pgrep -f "chainQ.sh|chainQ2.sh|chainQ3.sh" >/dev/null; do sleep 30; done
KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 905 fix2
echo "=== e905 fix2 done $(date -u +%T)"
