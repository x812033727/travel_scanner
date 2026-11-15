#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e912/zhong-tian-qu-qi-e912-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e012-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e912-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e912-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 12: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 12"; exit 1; }
# e912 trims (edit-dh-e912-live.json _note, colab/runs/e912-live/review3-trims.tsv): a whisper pass on the drafts found
# picks.json cutting spoken lines in s11 (喔 to 7.92), s13 (當著大家點一點 to 7.71), s20 (您急著上哪去 to 6.00), s23 (本官全當沒來過
# to 7.75) and s27 (人 to 7.65), and an invented syllable at the head of s12 (了, 2.00-2.25); s19 starts a frame before its first
# word (1.12); static tails cut in s02, s09, s24; s35 starts at 1.5 so the last hit rings out under the fade (no hold).
# Every start is rounded DOWN and every end-before UP to a whole 24 fps frame (input -ss keeps frames at/after start, -to
# drops a frame whose end passes it: 6.083 lost s20's last frame in the dry run). Warn (not stop) if picks.json lacks them.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0,4.625),'s02':(0,5.0),'s03':(2.791,5.834),'s04':(1.375,0),'s05':(0.25,6.5),'s06':(1.583,7.417),'s07':(1.5,6.0),
 's08':(2.375,0),'s09':(0.875,3.75),'s10':(1.5,5.0),'s11':(2.583,0),'s12':(2.291,6.5),'s13':(1.375,7.75),'s14':(2.0,5.917),
 's15':(1.0,4.209),'s16':(0.375,5.625),'s17':(0.291,4.834),'s18':(1.5,4.5),'s19':(1.083,5.834),'s20':(0.875,6.084),'s21':(1.125,6.0),
 's22':(0,0),'s23':(1.166,7.834),'s24':(0,6.0),'s25':(0.75,4.834),'s26':(0,0),'s27':(1.0,7.709),'s28':(1.0,6.0),'s29':(1.0,6.125),
 's30':(0.291,7.0),'s31':(0.5,3.417),'s32':(0.5,4.417),'s33':(0,0),'s34':(1.25,6.25),'s35':(1.5,6.0)}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.0005 or abs(p[s]['trim'].get('end-before',0)-b)>0.0005]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e012-r2/overlays.json $P/hailuo/edit-dh-e912-live.json $E $E/cut/e912-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e912-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (the e908 cut review found a click from its dynamic fallback;
# e909 review 3: at -4 dBFS the true peak -3.58 plus the +1.43 dB gain overshot TP -2.2 by 0.05 and loudnorm went dynamic;
# e910 review 3: with louder accents and beds the same limiter left a true peak of -2.39 (input -15.25 LUFS, +1.25 dB to go),
# loudnorm2 went dynamic and the cut clicked to +3.6 dBFS at 3.8 s. The overshoot is made by the AAC encode after the limiter
# (the limited PCM measures -4.3 dBTP): attack 2 ms -> -2.3, 0.5 ms -> -1.8, 5 ms -> -4.2 on the s01 footsteps, so the attack
# is 5 ms (limit still 0.6 = -4.4 dBFS; 0.5 lost 0.7 LU and stayed at -2.9 dBTP))
ffmpeg -v error -y -i $E/cut/e912-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=5:release=60:level=false,aresample=48000" $E/cut/e912-live.lim.mp4 && mv $E/cut/e912-live.lim.mp4 $E/cut/e912-live.mp4
bash $Q/loudnorm2.sh $E/cut/e912-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e912-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
