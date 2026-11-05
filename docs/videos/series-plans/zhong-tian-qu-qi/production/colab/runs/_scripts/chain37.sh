#!/usr/bin/env bash
# when e036's stage 1 has finished (ALL_DONE in its log), start e037's stage 1 on the freed slot
L=/root/mokaair-work/videos/zhong-tian-qu-qi-e036-dh/colab/a/st1/run.log
until grep -q ALL_DONE "$L" 2>/dev/null; do sleep 30; done
echo "e036 stage 1 done $(date -u +%T)"
cp /root/mokaair-work/videos/_runs/st1.sh /root/mokaair-work/videos/_runs/st1-37.sh
M=/root/mokaair-work/videos/zhong-tian-qu-qi-e037-dh/colab/a/st1
bash /root/mokaair-work/videos/_runs/st1-37.sh 37 > $M/run.log 2>&1
echo "e037 stage 1 ended $(date -u +%T): $(ls $M/out/*.mp4 2>/dev/null | wc -l)/45 drafts"
echo CHAIN_DONE
