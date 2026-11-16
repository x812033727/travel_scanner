#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e921/zhong-tian-qu-qi-e921-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e021-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e921-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e921-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 21 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 21 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e921-dh/audio and $E/music -> zhong-tian-qu-qi-e921-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e921, the e920 way). Every effect is in the series library.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 21 || exit 1; }
# e921 trims and seeds the edit table assumes (edit-dh-e921-live.json _note): picks.json as refine-prep.py 21 builds it from
# picks-merged.tsv and fix1/review-picks.tsv (run in colab/runs/e921-live) -- the fix1 retakes s28 s37 (9211201) and s36
# (9211202). No review3-trims.tsv yet: when one is written, run refine-prep.py 21 picks-merged.tsv fix1/review-picks.tsv
# review3-trims.tsv, stage.py 21, then this table. Whole frames: a start rounded DOWN and an end-before rounded UP to 3
# decimals, tolerance 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.25,6.584),'s02':(0,8),'s03':(0,6.584),'s04':(0,6.584),'s05':(0.75,6.584),'s06':(0,6.584),'s07':(0.5,5),
 's08':(0,6.584),'s09':(1,6.584),'s10':(1,8),'s11':(0.5,6.584),'s12':(0,6.584),'s13':(0.75,6.584),'s14':(0,8),'s14b':(0,8),
 's15':(1.916,6.584),'s16':(1.5,4.75),'s17':(0.5,6.584),'s18':(0,6.584),'s19':(0.666,6.584),'s20':(2.5,6.584),'s21':(3.5,6),
 's21b':(0,2),'s22':(3.25,6),'s22b':(1.916,5.917),'s23':(1,5.25),'s24':(0.75,6.584),'s25':(0.25,4),'s26':(0.5,7.584),
 's27':(0,6.584),'s28':(2.875,8),'s28b':(2,5.5),'s29':(0,2.5),'s30':(0.583,6.584),'s31':(1.75,5.5),'s32':(0,6.584),
 's33':(0.75,6.584),'s34':(1,5.5),'s35':(0.75,6.584),'s36':(0,3),'s37':(1.166,8)}
seed={'s01':9211102,'s02':9211102,'s04':9211102,'s07':9211102,'s10':9211102,'s11':9211102,'s12':9211102,'s13':9211102,
 's14':9211102,'s14b':9211102,'s16':9211102,'s20':9211102,'s21':9211102,'s21b':9211102,'s22':9211102,'s23':9211102,
 's25':9211102,'s27':9211102,'s28':9211201,'s30':9211102,'s31':9211102,'s32':9211102,'s33':9211102,'s36':9211202,'s37':9211201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9211101)' for s in p if s not in seed and p[s]['seed']!=9211101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# no shot is deleted: DROP is empty, so $VL is video.json as written (kept the e916/e920 way so a later REVIEW 3 can drop one)
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e021-r2/overlays.json $P/hailuo/edit-dh-e921-live.json $E $E/cut/e921-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e921-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# END: s37 is Wei Shaoqing's line on his own take (clip voice), 門 ends ~c6.78 and the take at c6.834; voice_until 6.84 ends
# the subtitle there; the gong and a low hit at c6.86 while the picture holds the take's last frame (a freeze, not an early
# fade: his mouth stops with the take), fades over c7.30-7.80 (vf), and min 10.83 holds ~3 s of black so the gong rings out.
# The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e921-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e921-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e921-live.lim.mp4 && mv $E/cut/e921-live.lim.mp4 $E/cut/e921-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e921-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e921-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e921-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
