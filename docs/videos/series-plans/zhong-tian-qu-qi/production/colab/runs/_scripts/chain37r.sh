#!/usr/bin/env bash
# when e036's stages 2+3 have finished, retake e037 s29/s37 (stage 1) on the freed slot, then run e037 stages 2+3
set -u
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
L=/root/mokaair-work/videos/zhong-tian-qu-qi-e036-dh/colab/a/run23.log
until grep -q ALL_DONE "$L" 2>/dev/null; do sleep 30; done
echo "e036 stages 2+3 done $(date -u +%T)"
export COLAB_GPU=G4
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e037-dh/colab/a; R=$A/retake1; S=zt37t
H3_PROFILE=hero bash $K/bootstrap.sh patch 2>&1 | grep -o "profile=[a-z]*"
bash $K/h3.sh start --session $S 2>&1 | tail -1
cd $R && python3 -I $K/h3_detached.py ref-e037-retake1.json --session $S --poll 30 --attempts 2 2>&1 | tail -2
bash $K/h3.sh stop --session $S 2>&1 | tail -1
ov=""; for s in s29 s37; do [ -f $R/out/$s.mp4 ] && ov="$ov $s:$R/out/$s.mp4:330007"; done
echo "retakes:$ov"
python3 /root/mokaair-work/videos/_runs/mk-st2.py 37 $ov | tail -2
cp /root/mokaair-work/videos/_runs/st23.sh /root/mokaair-work/videos/_runs/st23-37.sh
bash /root/mokaair-work/videos/_runs/st23-37.sh 37 > $A/run23.log 2>&1
echo "e037 stages 2+3 ended $(date -u +%T): $(ls $A/final/*_1080.mp4 2>/dev/null | wc -l)/45 finals"
echo CHAIN_DONE
