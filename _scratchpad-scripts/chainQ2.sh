#!/usr/bin/env bash
# after the retake queue: the e001 fix3 retakes on the same pod (pod stays up for the refines)
cd /home/user/travel_scanner
while pgrep -f chainQ.sh >/dev/null; do sleep 30; done
KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 901 fix3
echo "=== e901 fix3 done $(date -u +%T)"
