#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e927/zhong-tian-qu-qi-e927-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e027-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e927-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e927-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 27 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 27 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e927-dh/audio and $E/music -> zhong-tian-qu-qi-e927-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e927, the e926 way). Every effect is in the series library except snort927.wav (s21's sneer, cut
# from the laugh dropped off a20; zhong-tian-qu-qi-e927-dh/sfx, the edit table's second sfx dir).
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 27 || exit 1; }
# e927 trims and seeds the edit table assumes (edit-dh-e927-live.json _note): picks.json as refine-prep.py 27 builds it from
# picks-merged.tsv and review3-trims.tsv (run in colab/runs/e927-live: refine-prep.py 27 picks-merged.tsv review3-trims.tsv,
# then stage.py 27; no fix round in e927). review3-trims.tsv (first cut): s01 end 3.500 -> 6.375, s12 end 4.917 -> 6.584 and
# s27 end 5.125 -> 6.584 (the picks were cut to lay recordings; the takes' own voices go on to 誰家的糖，吃倒了人, 去綢緞莊等我
# and 沒讓人看見吧), s21 start 1.208 -> 1.000 (a20-trim and the snort fit without a held frame). s19 keeps its crop
# 800:452:0:0 from picks-merged.tsv (stage.py crops and scales it 1.2x; the white banner with false characters is out).
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop).
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.083,6.375),'s02':(0.0,3.584),'s03':(0.75,6.209),'s04':(0.0,3.0),'s05':(0.5,4.5),'s06':(0.541,7.792),'s07':(1.541,6.375),'s08':(0.875,5.0),'s09':(0.0,3.0),'s10':(0.5,3.5),'s11':(0.5,5.0),'s12':(1.208,6.584),'s13':(0.5,4.5),'s14':(0.0,6.459),'s15':(0.333,6.584),'s16':(0.791,8.0),'s17':(0.5,5.667),'s18':(0.25,6.584),'s19':(0.0,8.0),'s20':(0.333,4.709),'s21':(1.0,5.875),'s22':(1.0,4.5),'s23':(0.25,6.334),'s24':(0.75,6.459),'s25':(1.125,4.667),'s26':(0.0,4.0),'s27':(0.291,6.584),'s28':(1.5,6.584),'s29':(0.0,4.0),'s30':(0.375,6.292),'s31':(2.5,6.584),'s32':(0.5,5.917),'s33':(2.125,6.584),'s34':(0.583,6.584),'s35':(0.0,3.0),'s36':(2.166,6.167),'s37':(0.0,8.0)}
seed={'s01':9271102,'s05':9271102,'s06':9271102,'s08':9271102,'s09':9271102,'s11':9271102,'s12':9271102,'s13':9271102,'s15':9271102,'s17':9271102,'s20':9271102,'s22':9271102,'s24':9271102,'s25':9271102,'s26':9271102,'s28':9271102,'s29':9271102,'s31':9271102,'s33':9271102,'s34':9271102,'s35':9271102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9271101)' for s in p if s not in seed and p[s]['seed']!=9271101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (want 800:452:0:0 on s19 only)' for s in p if p[s].get('crop')!=('800:452:0:0' if s=='s19' else None)]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# nothing is dropped in e927 (DROP empty; all 37 shots are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e027-r2/overlays.json $P/hailuo/edit-dh-e927-live.json $E $E/cut/e927-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e927-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END: s37 is the suspense tail (8 s): A-ling's cold a32 under the veil, two sticks slapped, the sheathed knife slides out,
# the low hit and the gong at c5.5, the picture fades out over c7.60-8.00 (vf) and min 10.0 holds black while the gong rings
# out; the sound fades over the last 1.0 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e927-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e927-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e927-live.lim.mp4 && mv $E/cut/e927-live.lim.mp4 $E/cut/e927-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e927-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e927-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e927-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
