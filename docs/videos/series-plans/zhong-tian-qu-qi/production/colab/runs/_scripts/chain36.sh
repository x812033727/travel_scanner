#!/usr/bin/env bash
# when e034's stages 2+3 have finished (ALL_DONE in its log), start e036's stage 1 on the freed slot
L=/root/mokaair-work/videos/zhong-tian-qu-qi-e034-dh/colab/a/run23.log
until grep -q ALL_DONE "$L" 2>/dev/null; do sleep 30; done
echo "e034 stages 2+3 done $(date -u +%T)"
cp /root/mokaair-work/videos/_runs/st1.sh /root/mokaair-work/videos/_runs/st1-36.sh
M=/root/mokaair-work/videos/zhong-tian-qu-qi-e036-dh/colab/a/st1
bash /root/mokaair-work/videos/_runs/st1-36.sh 36 > $M/run.log 2>&1
echo "e036 stage 1 ended $(date -u +%T): $(ls $M/out/*.mp4 2>/dev/null | wc -l)/39 drafts"
echo CHAIN_DONE
