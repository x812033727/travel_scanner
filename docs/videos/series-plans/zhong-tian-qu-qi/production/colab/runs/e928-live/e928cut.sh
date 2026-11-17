#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e928/zhong-tian-qu-qi-e928-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e028-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e928-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e928-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 28 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 28 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e928-dh/audio and $E/music -> zhong-tian-qu-qi-e928-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e928, the e927 way). Every effect is in the series library except
# murmur928.wav (the square's crowd: twelve of this episode's recordings reversed and filtered, unintelligible;
# zhong-tian-qu-qi-e928-dh/sfx, the edit table's second sfx dir).
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 28 || exit 1; }
# e928 trims and seeds the edit table assumes (edit-dh-e928-live.json _note): picks.json as refine-prep.py 28 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e928-live: refine-prep.py 28 picks-merged.tsv
# fix1/review-picks.tsv review3-trims.tsv, then stage.py 28; fix1 replaced s03, s07 and s26). review3-trims.tsv (first cut):
# ends brought in where a laid recording left more than ~1 s of the shot without a line -- s02 4.500 -> 3.750, s07 6.584 -> 6.250,
# s14 5.000 -> 4.584, s15 8.000 -> 7.000, s16 5.250 -> 4.209, s24 5.500 -> 5.000, s26 4.500 -> 3.709, s32 6.584 -> 4.917 (s32's
# take is muted and a29 laid from its mouth). The post list's s08 4.625, s11 4.0, s12 0.875, s15b 4.0, s16 0.708, s28 1.125 were
# already in the picks. No crop in e928.
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop).
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(2.041,6.584),'s02':(0.0,3.75),'s03':(0.0,2.25),'s03b':(0.0,3.0),'s04':(0.0,3.0),'s05':(1.583,6.584),'s06':(1.25,4.75),'s07':(1.0,6.25),'s08':(0.0,4.625),'s09':(0.0,5.0),'s10':(0.0,3.5),'s11':(0.0,4.0),'s12':(0.875,5.584),'s13':(0.75,6.584),'s14':(1.0,4.584),'s15':(0.0,7.0),'s15b':(0.0,4.0),'s16':(0.708,4.209),'s17':(0.25,5.667),'s18':(0.416,7.834),'s19':(0.541,6.5),'s20':(1.083,8.0),'s21':(0.0,5.5),'s22':(1.416,6.584),'s23':(0.25,6.584),'s24':(0.0,5.0),'s25':(0.458,6.5),'s26':(0.0,3.709),'s27':(0.75,5.5),'s28':(1.125,4.625),'s29':(0.625,6.584),'s30':(0.0,3.0),'s31':(0.75,6.584),'s32':(0.416,4.917),'s33':(0.0,5.0),'s34':(0.0,4.0),'s35':(1.25,8.0),'s36':(0.0,8.0),'s37':(0.0,2.5),'s38':(1.25,6.584),'s39':(0.0,4.0)}
seed={'s01':9281102,'s02':9281102,'s08':9281102,'s09':9281102,'s10':9281102,'s11':9281102,'s19':9281102,'s20':9281102,'s25':9281102,'s29':9281102,'s32':9281102,'s34':9281102,'s36':9281102,'s38':9281102,'s39':9281102,'s03':9281202,'s07':9281201,'s26':9281201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9281101)' for s in p if s not in seed and p[s]['seed']!=9281101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (want none)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# nothing is dropped in e928 (DROP empty; all 41 shots are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e028-r2/overlays.json $P/hailuo/edit-dh-e928-live.json $E $E/cut/e928-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e928-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END: s39 is the suspense tail (4 s of the crowd pointing at the stage): the low hit and gong_02 at c3.5, the picture fades out over
# c3.60-4.00 (vf) and min 8.0 holds black while the gong rings out (gong_02 is 4.5 s, it stops at c8.0); the sound fades over the last 1.0 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e928-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e928-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e928-live.lim.mp4 && mv $E/cut/e928-live.lim.mp4 $E/cut/e928-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e928-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e928-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e928-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
