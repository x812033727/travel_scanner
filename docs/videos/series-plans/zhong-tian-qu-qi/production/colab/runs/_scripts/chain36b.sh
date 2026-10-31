#!/usr/bin/env bash
# when e035's stages 2+3 have finished (ALL_DONE in its log), run e036's stages 2+3 on the freed slot
L=/root/mokaair-work/videos/zhong-tian-qu-qi-e035-dh/colab/a/run23.log
until grep -q ALL_DONE "$L" 2>/dev/null; do sleep 30; done
echo "e035 stages 2+3 done $(date -u +%T)"
cp /root/mokaair-work/videos/_runs/st23.sh /root/mokaair-work/videos/_runs/st23-36.sh
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e036-dh/colab/a
bash /root/mokaair-work/videos/_runs/st23-36.sh 36 > $A/run23.log 2>&1
echo "e036 stages 2+3 ended $(date -u +%T): $(ls $A/final/*_1080.mp4 2>/dev/null | wc -l)/39 finals"
echo CHAIN_DONE
