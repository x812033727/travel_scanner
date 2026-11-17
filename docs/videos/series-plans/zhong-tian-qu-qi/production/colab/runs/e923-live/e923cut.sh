#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e923/zhong-tian-qu-qi-e923-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e023-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e923-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e923-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 23 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 23 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e923-dh/audio and $E/music -> zhong-tian-qu-qi-e923-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e923, the e921 way). Every effect is in the series library.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 23 || exit 1; }
# e923 trims and seeds the edit table assumes (edit-dh-e923-live.json _note): picks.json as refine-prep.py 23 builds it from
# picks-merged.tsv and fix1/review-picks.tsv (first cut: no review3-trims.tsv yet; when one is written, run in
# colab/runs/e923-live: refine-prep.py 23 picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 23, and
# update this table) -- the fix1 retakes s17 (9231202), s31 (9231201) and s38 (9231201). Whole frames: a start rounded DOWN
# and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.833,6.584),'s02':(0.5,2.959),'s03':(0,4.417),'s04':(0.5,3),'s05':(1,6.584),'s06':(2,4.459),'s07':(1.75,6.584),'s08':(1.833,6.584),'s09':(0.708,6.584),'s10':(0,4.5),'s11':(0,2.5),'s12':(1.208,6.584),'s13':(0,6.584),'s13b':(0,4.5),'s14':(0,5.584),'s15':(0,4.5),'s16':(0.958,6.584),'s17':(0.5,6.584),'s18':(0,4.417),'s19':(0.5,6.584),'s20':(0,7),'s21':(0,6.584),'s22':(0,5),'s23':(1.083,6.584),'s24':(0,4.459),'s25':(0,5.792),'s26':(1.625,6.584),'s27':(0,5.042),'s28':(0,6.584),'s29':(0,4.625),'s30':(1.625,6.584),'s31':(1,6.584),'s32':(1,6.584),'s33':(0,3.709),'s34':(0.875,6.584),'s35':(0.25,5.167),'s36':(0,6),'s37':(0,6.584),'s38':(0,6.584),'s39':(0.75,3.25),'s40':(0,8)}
seed={'s01':9231102,'s09':9231102,'s10':9231102,'s13':9231102,'s16':9231102,'s17':9231202,'s18':9231102,'s19':9231102,'s20':9231102,'s23':9231102,'s24':9231102,'s31':9231201,'s33':9231102,'s34':9231102,'s38':9231201,'s40':9231102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9231101)' for s in p if s not in seed and p[s]['seed']!=9231101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# no shot is deleted: DROP is empty, so $VL is video.json as written (kept the e916/e920 way so a later review can drop one)
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e023-r2/overlays.json $P/hailuo/edit-dh-e923-live.json $E $E/cut/e923-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e923-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# END: s41 is the wide shot from behind on the pier; Xu's off-screen shout a37 ends at c2.77, a low hit and the gong at
# c2.95, the picture fades over c3.60-4.20 (vf) and min 7.20 holds 3 s of black so the gong rings out (the take ends at
# c4.50, so the black is the fade plus tpad). The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e923-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e923-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e923-live.lim.mp4 && mv $E/cut/e923-live.lim.mp4 $E/cut/e923-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e923-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e923-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e923-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
