#!/usr/bin/env bash
# after the e905 retakes: the e904 owner-review retakes (s19, s25, s38, s39) on the same pod; then touch a flag
cd /home/user/travel_scanner
L=$HOME/mokaair-work/videos/zhong-tian-qu-qi-e905-dh/runpod/a/st2-chain.log
until grep -q "=== s39 retake done" "$L" 2>/dev/null; do sleep 30; done
KEEP=1 PREFLIGHT=0 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 904 fix1
echo "=== e904 fix1 done $(date -u +%T)"
