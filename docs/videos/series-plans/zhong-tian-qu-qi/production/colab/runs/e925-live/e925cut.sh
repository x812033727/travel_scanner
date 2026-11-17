#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e925/zhong-tian-qu-qi-e925-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e025-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e925-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e925-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 25 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 25 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e925-dh/audio and $E/music -> zhong-tian-qu-qi-e925-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e925, the e924 way). Every effect is in the series library.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 25 || exit 1; }
# e925 trims and seeds the edit table assumes (edit-dh-e925-live.json _note): picks.json as refine-prep.py 25 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e925-live: refine-prep.py 25
# picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 25) -- the fix1 retakes s06 (9251202), s18
# (9251201), s27 (9251202), s32 (9251202), s33 (9251201); review3-trims.tsv (first cut): s01 end 4.25, s03 2.333-6.584
# (the take's own voice, whole line), s15 and s37 start 0.375 (the first sentence back, cropped in the edit table), s34 and
# s35 end at the take's end; the silent tails over ~1 s cut: s16 end 2.875, s25 end 4.0, s39 end 2.583. Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance
# 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.5,4.25),'s02':(0.0,3.0),'s03':(2.333,6.584),'s04':(2.375,6.584),'s05':(0.5,4.0),'s06':(1.0,6.584),'s07':(0.0,4.75),'s08':(1.625,5.0),'s09':(2.5,6.584),'s10':(0.5,5.25),'s11':(0.375,6.584),'s12':(1.5,5.167),'s13':(0.375,6.584),'s14':(0.5,5.25),'s15':(0.375,6.584),'s16':(0.0,2.875),'s17':(0.0,4.25),'s18':(0.375,5.25),'s19':(0.5,4.5),'s20':(0.0,6.584),'s20b':(0.0,5.0),'s21':(0.75,5.25),'s22':(0.5,3.25),'s23':(1.0,5.167),'s23b':(0.0,4.0),'s24':(0.5,4.75),'s25':(1.0,4.0),'s26':(1.75,6.584),'s27':(1.5,4.75),'s28':(0.5,3.0),'s29':(0.0,3.5),'s30':(0.75,4.0),'s31':(0.0,5.167),'s32':(0.0,4.25),'s33':(0.375,8.0),'s34':(0.625,6.584),'s35':(0.75,6.584),'s36':(0.5,4.5),'s37':(0.375,6.584),'s38':(0.0,2.5),'s39':(0.0,2.583),'s40':(0.25,5.375),'s40b':(0.0,8.0)}
seed={'s02':9251102,'s06':9251202,'s07':9251102,'s08':9251102,'s10':9251102,'s11':9251102,'s12':9251102,'s13':9251102,'s14':9251102,'s15':9251102,'s16':9251102,'s17':9251102,'s18':9251201,'s23':9251102,'s23b':9251102,'s24':9251102,'s27':9251202,'s29':9251102,'s30':9251102,'s31':9251102,'s32':9251202,'s33':9251201,'s34':9251102,'s35':9251102,'s36':9251102,'s38':9251102,'s39':9251102,'s40':9251102,'s40b':9251102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9251101)' for s in p if s not in seed and p[s]['seed']!=9251101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# nothing is dropped in e925 (DROP empty; all 43 shots with s20b, s23b, s40b are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e025-r2/overlays.json $P/hailuo/edit-dh-e925-live.json $E $E/cut/e925-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e925-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END: s40b is Xu's inner line (laid a38) on his face; the low hit and the gong after it, the picture fades out at the end of
# the take (vf) and min holds black while the gong rings out; the sound fades over the last 1.0 s (e924 REVIEW 3).
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e925-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e925-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e925-live.lim.mp4 && mv $E/cut/e925-live.lim.mp4 $E/cut/e925-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e925-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e925-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e925-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
