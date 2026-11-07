#!/usr/bin/env bash
# e056 stages 2-3 end -> stop its guard -> e001-r2 pilot drafts on the same pod (KEEP=1).
while pgrep -f "st23-retry.sh 56" >/dev/null; do sleep 30; done
pkill -f "speed-guard.sh /root/mokaair-work/videos/zhong-tian-qu-qi-e056-dh" 2>/dev/null
echo "##### e056 st23 ended $(date -u +%T): $(ls /root/mokaair-work/videos/zhong-tian-qu-qi-e056-dh/runpod/a/final/*_1080.mp4 | wc -l) finals"
echo "##### r2 pilot start $(date -u +%T): $(bash /home/user/travel_scanner/.agents/skills/minimax-h3-runpod/scripts/h3r.sh usage 2>&1 | grep -m1 '\"usd\"')"
cd /home/user/travel_scanner && KEEP=1 bash /home/user/travel_scanner/docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 901 pilot > /root/mokaair-work/videos/zhong-tian-qu-qi-e901-dh/runpod/a/pilot/run.log 2>&1
echo "##### r2 pilot drafts done $(date -u +%T): $(tail -1 /root/mokaair-work/videos/zhong-tian-qu-qi-e901-dh/runpod/a/pilot/run.log)"
