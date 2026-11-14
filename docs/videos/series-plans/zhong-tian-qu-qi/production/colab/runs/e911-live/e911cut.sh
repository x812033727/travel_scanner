#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e911/zhong-tian-qu-qi-e911-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e011-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e911-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e911-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 11: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 11"; exit 1; }
# e911 trims (edit-dh-e911-live.json _note): a whisper pass on the drafts found picks.json / pick-review cutting spoken lines
# (s10 s11 s20 s25 s26 s31 s32 s33 s35), pick-review's smile trims (s13 s14 s17 s21 s30), and every start rounded DOWN and
# every end-before rounded UP to a whole 24 fps frame (input -ss keeps frames at/after start, -to drops a frame whose end
# passes it: 0.792 lost s03's frame 19, 7.708 left s11 a frame short). Warn (not stop) if picks.json does not have them.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(3.375,6.417),'s02':(0,2.791),'s03':(0.791,5.583),'s04':(0,5.417),'s05':(0.875,7.5),'s06':(3.375,7.5),'s07':(0,3.375),
 's08':(0.583,0),'s09':(0.75,6.75),'s10':(2.0,0),'s11':(2.625,7.709),'s12':(0,6.0),'s13':(2.583,0),'s14':(0,5.417),'s15':(0,4.584),
 's16':(0,0),'s17':(0.375,5.792),'s18':(0,3.5),'s19':(1.0,6.0),'s20':(0.5,7.834),'s21':(0,4.25),'s22':(0.375,4.625),'s23':(0.583,5.583),
 's24':(1.375,6.791),'s25':(3.0,10.084),'s26':(1.0,0),'s27':(0,2.0),'s28':(0,10.084),'s29':(0,0),'s30':(0.791,7.125),'s31':(0.625,0),
 's32':(2.791,7.708),'s33':(0.75,7.0),'s34':(0.375,3.584),'s35':(1.791,0)}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.0005 or abs(p[s]['trim'].get('end-before',0)-b)>0.0005]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e011-r2/overlays.json $P/hailuo/edit-dh-e911-live.json $E $E/cut/e911-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e911-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (the e908 cut review found a click from its dynamic fallback;
# e909 review 3: at -4 dBFS the true peak -3.58 plus the +1.43 dB gain overshot TP -2.2 by 0.05 and loudnorm went dynamic;
# e910 review 3: with louder accents and beds the same limiter left a true peak of -2.39 (input -15.25 LUFS, +1.25 dB to go),
# loudnorm2 went dynamic and the cut clicked to +3.6 dBFS at 3.8 s. The overshoot is made by the AAC encode after the limiter
# (the limited PCM measures -4.3 dBTP): attack 2 ms -> -2.3, 0.5 ms -> -1.8, 5 ms -> -4.2 on the s01 footsteps, so the attack
# is 5 ms (limit still 0.6 = -4.4 dBFS; 0.5 lost 0.7 LU and stayed at -2.9 dBTP))
ffmpeg -v error -y -i $E/cut/e911-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=5:release=60:level=false,aresample=48000" $E/cut/e911-live.lim.mp4 && mv $E/cut/e911-live.lim.mp4 $E/cut/e911-live.mp4
bash $Q/loudnorm2.sh $E/cut/e911-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e911-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
