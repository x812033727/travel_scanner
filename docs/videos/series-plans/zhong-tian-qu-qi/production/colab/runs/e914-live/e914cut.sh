#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e914/zhong-tian-qu-qi-e914-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e014-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e914-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e914-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 14: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 14"; exit 1; }
# e914 trims and seeds the edit table assumes (edit-dh-e914-live.json _note): picks.json as refine-prep.py 14 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv in that order -- the fix1 retakes s24 s30 s32 (9141201, no trim
# in fix1) trimmed there, s16 start 1.75 (the extra hand on the abacus, gone by 2.25), s29 start 0.875 (不是 at 1.00-1.30 was cut out by
# 2.625), s42 end 5.417 (the pick's suggested earlier end).
# REVIEW 3 (cut-review.md + cut-review-2.md, coordinator's picks): s05 start 2.25, s11 end 5.375, s14 end 6.5, s15 end 6.625,
# s16 start 2.0 (a16 at 1.2x), s17 end 4.125, s24 end 7.4, s42 start 1.5 with no end (a41 at 1.05x; Xu's hands off the notice).
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001 (e912 review 3: -ss keeps a
# frame at/after start, -to drops a frame whose end passes it); 0 = no end (the clip's end).
# Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.0,4.75),'s02':(0.875,6.375),'s03':(0.5,6.375),'s04':(0.75,6.5),'s05':(2.25,6.375),'s06':(1.5,7.875),'s07':(3.0,6.584),
 's08':(0.5,3.584),'s09':(0.5,6.125),'s10':(2.0,7.5),'s11':(0.625,5.375),'s12':(1.375,7.75),'s13':(0.75,6.125),'s14':(1.0,6.5),
 's15':(0.375,6.625),'s16':(2.0,6.584),'s17':(0.625,4.125),'s18':(0.625,6.625),'s19':(0.125,6.375),'s20':(0.25,5.875),
 's21':(0.75,5.375),'s22':(1.75,6.584),'s23':(0.125,5.25),'s24':(0.5,7.4),'s25':(1.5,6.125),'s26':(1.0,7.875),'s27':(1.0,7.584),
 's28':(1.875,6.375),'s29':(0.875,6.584),'s30':(0,5.5),'s31':(1.5,7.75),'s32':(0.75,0),'s33':(0.5,5.0),'s34':(1.0,4.5),
 's35':(2.5,6.584),'s36':(1.5,4.5),'s37':(0.375,7.875),'s38':(0.875,8.0),'s39':(1.0,8.0),'s40':(1.5,5.5),'s41':(1.5,6.25),
 's42':(1.5,0)}
seed={'s03':9141102,'s11':9141102,'s13':9141101,'s14':9141102,'s15':9141102,'s16':9141102,'s18':9141102,'s22':9141102,'s24':9141201,
 's29':9141102,'s30':9141201,'s31':9141102,'s32':9141201,'s35':9141102,'s37':9141102,'s38':9141102,'s40':9141102,'s41':9141101,'s42':9141102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9141101)' for s in p if s not in seed and p[s]['seed']!=9141101]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# no vidstab this time: cut-qa's jitter() on every staged clip reads 0.00-0.04 (s22 0.04), nothing hops frame to frame
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e014-r2/overlays.json $P/hailuo/edit-dh-e914-live.json $E $E/cut/e914-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e914-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3: attack 8 ms -- with 5 ms
# the e913 re-cut's AAC overshot to -3.11 dBTP and loudnorm2 went dynamic; 8 ms held it to -3.84 dBTP, linear; kept for e914
# END (REVIEW 3): s42 is a recorded-line shot (a41 at 1.05x laid at c0.05, Tang's back, last word ends c4.81); the picture fades
# over c4.84-5.44 (vf fade=t=out:st=4.840:d=0.6) and min 6.667 holds about 1.2 s of black after it, so the low accent laid at
# c4.85 (gong_02 + impactSoft_heavy_000) rings out (cut-review 2 medium 7: it had 0.58 s). The sound fades over the last 1.0 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e914-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e914-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e914-live.lim.mp4 && mv $E/cut/e914-live.lim.mp4 $E/cut/e914-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e914-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e914-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e914-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
