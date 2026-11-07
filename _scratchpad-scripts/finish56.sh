#!/usr/bin/env bash
# wrap-up: wait for e056 stages 2-3, stop the guard, stop the pod; no e057.
while pgrep -f "st23-retry.sh 56" >/dev/null; do sleep 30; done
pkill -f "speed-guard.sh /root/mokaair-work/videos/zhong-tian-qu-qi-e056-dh" 2>/dev/null
echo "##### e056 st23 ended $(date -u +%T): $(tail -1 /root/mokaair-work/videos/zhong-tian-qu-qi-e056-dh/runpod/a/st23.log)"
ls /root/mokaair-work/videos/zhong-tian-qu-qi-e056-dh/runpod/a/final/*_1080.mp4 | wc -l
bash /home/user/travel_scanner/.agents/skills/minimax-h3-runpod/scripts/h3r.sh stop 2>&1 | tail -2
echo "##### wrap-up done $(date -u +%T)"
