#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e910/zhong-tian-qu-qi-e910-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e010-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e910-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e910-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 10: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 10"; exit 1; }
# e910 dry run: the old trims cut the end of a spoken line (s05 7.4, s21 7.3, s26 7.2) or end on a part frame that holds one
# frame (s10 5.4); s17 is review2-trims.tsv's 5.6;
# edit-dh-e910-live.json's _note has the values -- warn (not stop) if picks.json still has the old ones
python3 -c "
import json;p=json.load(open('$E/picks.json'));want={'s05':7.75,'s10':5.417,'s17':5.6,'s21':7.75,'s26':7.375}
bad=[f'{s} end-before {p[s][\"trim\"].get(\"end-before\")} (want {v})' for s,v in want.items() if abs(p[s]['trim'].get('end-before',0)-v)>0.02]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e010-r2/overlays.json $P/hailuo/edit-dh-e910-live.json $E $E/cut/e910-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e910-live.mp4 ] || exit 1
# a -4.4 dBFS sample-peak limiter before loudnorm2 keeps it linear (the e908 cut review found a click from its dynamic fallback;
# e909 review 3: at -4 dBFS the true peak -3.58 plus the +1.43 dB gain overshot TP -2.2 by 0.05 and loudnorm went dynamic)
ffmpeg -v error -y -i $E/cut/e910-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=2:release=60:level=false,aresample=48000" $E/cut/e910-live.lim.mp4 && mv $E/cut/e910-live.lim.mp4 $E/cut/e910-live.mp4
bash $Q/loudnorm2.sh $E/cut/e910-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e910-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
