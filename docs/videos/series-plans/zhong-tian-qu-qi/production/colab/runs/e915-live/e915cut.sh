#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e915/zhong-tian-qu-qi-e915-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e015-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e915-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e915-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 15: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 15"; exit 1; }
# e915 trims and seeds the edit table assumes (edit-dh-e915-live.json _note): picks.json as refine-prep.py 15 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv in that order -- the fix1 retakes s08 s10 s21 s25 s26 s41
# (9151201/9151202) play whole (no trim, 0 0 below); review3-trims.tsv (first cut): s22 end 6.125 (a -9 dB knock at c5.90-6.00
# fell on the cut; 見 ends draft 5.45), s32 end 6.375 (the post list: her mouth slackens at 6.5; 字 ends c6.00).
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001 (e912 review 3: -ss keeps a
# frame at/after start, -to drops a frame whose end passes it); 0 = no end (the clip's end).
# Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.0,6.584),'s02':(0.5,6.584),'s03':(0.0,8.0),'s04':(0.5,8.0),'s05':(0.25,6.584),'s06':(1.125,6.5),'s07':(0.25,6.584),
 's08':(0,0),'s09':(0.75,4.5),'s10':(0,0),'s11':(0.25,6.375),'s12':(1.0,6.584),'s13':(0.5,5.167),'s14':(0.75,6.584),'s15':(1.0,8.0),
 's16':(0.0,6.584),'s17':(0.25,8.0),'s18':(0.0,7.0),'s19':(0.5,5.0),'s20':(0.0,4.75),'s21':(0,0),'s22':(0.25,6.125),
 's23':(2.25,6.584),'s24':(1.0,8.0),'s25':(0,0),'s26':(0,0),'s27':(0.75,5.5),'s28':(0.5,5.0),'s29':(0.25,6.584),'s30':(0.0,6.584),
 's31':(0.5,6.0),'s32':(0.25,6.375),'s33':(1.0,4.75),'s34':(1.0,6.375),'s35':(2.5,6.584),'s36':(0.5,8.0),'s37':(0.25,6.584),
 's38':(0.5,8.0),'s39':(0.0,6.584),'s40':(1.375,8.0),'s41':(0,0),'s42':(1.0,6.584)}
seed={'s01':9151102,'s05':9151102,'s07':9151102,'s08':9151202,'s09':9151102,'s10':9151201,'s11':9151102,'s13':9151102,
 's15':9151102,'s16':9151102,'s17':9151102,'s19':9151102,'s21':9151201,'s24':9151102,'s25':9151201,'s26':9151202,'s30':9151102,
 's32':9151102,'s33':9151102,'s34':9151102,'s37':9151102,'s38':9151102,'s39':9151102,'s41':9151202,'s42':9151102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9151101)' for s in p if s not in seed and p[s]['seed']!=9151101]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# no vidstab: cut-qa's jitter() on every staged clip reads 0.00-0.05 (s02 s37 0.05, s14 0.04), nothing hops frame to frame
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e015-r2/overlays.json $P/hailuo/edit-dh-e915-live.json $E $E/cut/e915-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e915-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3: attack 8 ms -- with 5 ms
# the e913 re-cut's AAC overshot to -3.11 dBTP and loudnorm2 went dynamic; 8 ms held it to -3.84 dBTP, linear; kept for e914, e915
# END: s42 is Lai San's own voice (his last word 通 ends c5.38); the picture fades over c5.00-5.56 (vf fade=t=out:st=5.000:d=0.56,
# the clip's end, so nothing is held in view) and min 6.5 holds about 0.94 s of black after it, so the low accent laid at c5.45
# (gong_02 + impactSoft_heavy_000) and the tension cue ring out in the dark. The sound fades over the last 1.0 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e915-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e915-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e915-live.lim.mp4 && mv $E/cut/e915-live.lim.mp4 $E/cut/e915-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e915-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e915-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e915-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
