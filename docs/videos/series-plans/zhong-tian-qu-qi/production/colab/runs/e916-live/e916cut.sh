#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e916/zhong-tian-qu-qi-e916-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e016-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e916-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e916-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 16 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 16 rewrites picks.json)
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 16 || exit 1; }
# e916 trims and seeds the edit table assumes (edit-dh-e916-live.json _note): picks.json as refine-prep.py 16 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv in that order (run in colab/runs/e916-live) -- the fix1 retakes
# s26 s27 s32 s39 s42 (9161201/9161202); review3-trims.tsv (first cut): s02 s03 s10 s23 s24 s29 s30 s34 s38 ends, 0.55-0.65 s
# after the last word. Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001 (e912
# review 3: -ss keeps a frame at/after start, -to drops a frame whose end passes it); 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0,5),'s02':(0,5.25),'s03':(1.75,6.125),'s04':(0.5,4),'s05':(1.875,6.584),'s06':(0.625,5.75),'s07':(2.125,7),
 's08':(1.75,6.584),'s09':(1,8),'s10':(0,4.125),'s11':(0,6.584),'s12':(0.5,4),'s13':(0,7.25),'s14':(0,4.25),'s15':(0.25,6.584),
 's16':(0,4.5),'s17':(0,6.584),'s18':(1.25,4.5),'s19':(0.5,4.5),'s20':(0,6.584),'s21':(0.25,4.25),'s22':(0,5.167),'s23':(0,7.5),
 's24':(0.25,4.25),'s25':(1.25,6.584),'s26':(0,6),'s27':(0,5.75),'s28':(0.25,4.584),'s29':(0.5,5.375),'s30':(0,4.5),
 's31':(0.75,6.584),'s32':(0.5,5.5),'s33':(0,4.334),'s34':(0,3.375),'s35':(0,6.584),'s36':(1.5,6.584),'s37':(0.25,4.5),
 's38':(0.75,5.625),'s39':(1,5),'s40':(0,4.75),'s41':(0,5.5),'s42':(0.25,5)}
seed={'s01':9161102,'s02':9161102,'s03':9161102,'s06':9161102,'s07':9161102,'s10':9161102,'s11':9161102,'s13':9161102,'s14':9161102,
 's15':9161102,'s18':9161102,'s19':9161102,'s26':9161201,'s27':9161202,'s28':9161102,'s30':9161102,'s31':9161102,'s32':9161202,
 's33':9161102,'s35':9161102,'s37':9161102,'s39':9161201,'s40':9161102,'s41':9161102,'s42':9161201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9161101)' for s in p if s not in seed and p[s]['seed']!=9161101]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# no vidstab: cut-qa's jitter() on every staged clip reads 0.00 (s02 0.02, s15 0.08), nothing hops frame to frame
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e016-r2/overlays.json $P/hailuo/edit-dh-e916-live.json $E $E/cut/e916-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e916-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3: attack 8 ms (with 5 ms
# the AAC overshot to -3.11 dBTP and loudnorm2 went dynamic; 8 ms held it to -3.84 dBTP, linear); kept since.
# END: s42 is Tang's recording a39 (ends c3.81); the picture fades over c4.20-4.75 (vf fade=t=out:st=4.200:d=0.55) and min 7.0
# holds about 2.25 s of black, so the low accent laid at c3.95 (gong_02 + impactSoft_heavy_000) and the tension cue ring out in
# the dark. The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e916-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e916-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e916-live.lim.mp4 && mv $E/cut/e916-live.lim.mp4 $E/cut/e916-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e916-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e916-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e916-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
