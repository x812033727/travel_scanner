#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e922/zhong-tian-qu-qi-e922-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e022-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e922-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e922-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 22 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 22 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e922-dh/audio and $E/music -> zhong-tian-qu-qi-e922-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e922, the e921 way). Every effect is in the series library.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 22 || exit 1; }
# e922 trims and seeds the edit table assumes (edit-dh-e922-live.json _note): picks.json as refine-prep.py 22 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e922-live: refine-prep.py 22
# picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 22) -- the fix1 retakes s09 (9221201) and s32
# (9221202); review3-trims.tsv (first cut) shortens the silent tails of s01 s03 s05 s09 s11 s13 s14 s15 s17 s19 s20 s26
# s30 s31 s35 s35b s40 s41. Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance
# 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.25,5.875),'s02':(1.916,6.584),'s03':(0,4.625),'s04':(0.75,3.5),'s05':(0,5.542),'s06':(0,8),'s07':(0,4),
 's08':(0.75,8),'s09':(0,3.583),'s10':(0.75,8),'s11':(0,4),'s12':(1.25,6.584),'s13':(0,4.333),'s14':(0,5.208),
 's15':(0.5,4.958),'s16':(2,6.584),'s17':(0,6.708),'s18':(0.625,6.584),'s19':(0,4.125),'s20':(0.75,3.667),
 's21':(0.5,6.584),'s22':(0.5,6.584),'s23':(0.416,6.584),'s24':(0.5,6.584),'s25':(0.5,5),'s26':(0,5.833),
 's27':(0,6.584),'s28':(0.75,3),'s29':(0,2.5),'s30':(0,7.542),'s31':(0,5.25),'s32':(0.5,5.25),'s33':(1.708,6.584),
 's34':(1.25,4.5),'s35':(0,5.958),'s35b':(0,4),'s36':(0.916,6.584),'s37':(1.25,6),'s38':(0,4),'s39':(3,5),
 's40':(0.5,4.667),'s41':(0,4.5)}
seed={'s02':9221102,'s04':9221102,'s06':9221102,'s09':9221201,'s13':9221102,'s14':9221102,'s15':9221102,'s17':9221102,
 's20':9221102,'s24':9221102,'s27':9221102,'s29':9221102,'s30':9221102,'s31':9221102,'s32':9221202,'s41':9221102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9221101)' for s in p if s not in seed and p[s]['seed']!=9221101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# no shot is deleted: DROP is empty, so $VL is video.json as written (kept the e916/e920 way so a later review can drop one)
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e022-r2/overlays.json $P/hailuo/edit-dh-e922-live.json $E $E/cut/e922-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e922-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# END: s41 is the wide shot from behind on the pier; Xu's off-screen shout a37 ends at c2.77, a low hit and the gong at
# c2.95, the picture fades over c3.60-4.20 (vf) and min 7.20 holds 3 s of black so the gong rings out (the take ends at
# c4.50, so the black is the fade plus tpad). The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e922-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e922-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e922-live.lim.mp4 && mv $E/cut/e922-live.lim.mp4 $E/cut/e922-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e922-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e922-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e922-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
