#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e906/zhong-tian-qu-qi-e906-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e006-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e906-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e906-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e006-r2/overlays.json $P/hailuo/edit-dh-e906-live.json $E $E/cut/e906-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e906-live.mp4 ] || exit 1
bash $Q/loudnorm2.sh $E/cut/e906-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e906-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
