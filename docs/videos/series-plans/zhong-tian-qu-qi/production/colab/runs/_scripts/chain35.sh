#!/usr/bin/env bash
# wait for e035 stage 1, make sure its session is stopped, then run the retakes detached
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
while pgrep -f "_runs/st1.sh 35$" >/dev/null || pgrep -f "_runs/st1.sh 35 " >/dev/null; do sleep 30; done
echo "e035 stage 1 ended $(date -u +%T); drafts $(ls /root/mokaair-work/videos/zhong-tian-qu-qi-e035-dh/colab/a/st1/out/*.mp4 | wc -l)/41"
if colab sessions 2>&1 | grep -q "zt35 \|zt35]"; then echo "zt35 still up: stopping"; bash $K/h3.sh stop --session zt35 2>&1 | tail -1; fi
cp /root/mokaair-work/videos/_runs/st1.sh /root/mokaair-work/videos/_runs/st1-run35r.sh
bash /root/mokaair-work/videos/_runs/st1-run35r.sh 35 /root/mokaair-work/videos/zhong-tian-qu-qi-e035-dh/colab/a/retake1 > /root/mokaair-work/videos/zhong-tian-qu-qi-e035-dh/colab/a/retake1/run.log 2>&1
echo "retakes ended $(date -u +%T): $(tail -3 /root/mokaair-work/videos/zhong-tian-qu-qi-e035-dh/colab/a/retake1/run.log | tr '\n' ' ')"
echo CHAIN_DONE
