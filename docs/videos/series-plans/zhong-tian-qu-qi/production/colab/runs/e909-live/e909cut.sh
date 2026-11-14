#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e909/zhong-tian-qu-qi-e909-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e009-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e909-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e909-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 9: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 9"; exit 1; }
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e009-r2/overlays.json $P/hailuo/edit-dh-e909-live.json $E $E/cut/e909-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e909-live.mp4 ] || exit 1
# a -4 dBFS sample-peak limiter before loudnorm2 keeps it linear (the e908 cut review found a click from its dynamic fallback)
ffmpeg -v error -y -i $E/cut/e909-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.63:attack=2:release=60:level=false,aresample=48000" $E/cut/e909-live.lim.mp4 && mv $E/cut/e909-live.lim.mp4 $E/cut/e909-live.mp4
bash $Q/loudnorm2.sh $E/cut/e909-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e909-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
