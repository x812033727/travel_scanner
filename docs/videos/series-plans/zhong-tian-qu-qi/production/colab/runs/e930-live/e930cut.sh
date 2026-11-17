#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e930/zhong-tian-qu-qi-e930-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e030-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e930-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e930-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 30 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 30 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e930-dh/audio and $E/music -> zhong-tian-qu-qi-e930-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e930, the e927-e929 way). No shot carries a crop. Every effect is in the
# series library except murmur930.wav (the square's crowd: twelve of this episode's recordings reversed and filtered,
# unintelligible; zhong-tian-qu-qi-e930-dh/sfx, the edit table's second sfx dir; the e929 murmur recipe, since murmur929.wav
# is no longer on this disk).
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 30 || exit 1; }
# e930 trims and seeds the edit table assumes (edit-dh-e930-live.json _note): picks.json as refine-prep.py 30 builds it from
# picks-merged.tsv, fix1/review-picks.tsv, fix2/review-picks.tsv and review3-trims.tsv (run in colab/runs/e930-live:
# refine-prep.py 30 picks-merged.tsv fix1/review-picks.tsv fix2/review-picks.tsv review3-trims.tsv, then stage.py 30; fix1
# replaced s29 and s32, fix2 s41). review3-trims.tsv (first cut): s01 1.333 -> 1.875 (the take keeps its own voice: whisper
# hears 窮 and 秀才 short of its tone only, so zq930a01 is not laid and the pick's own cut comes back; picks-merged.tsv's s01 row
# carries both pairs and refine-prep keeps the last one, the laid-recording fallback).
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop).
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.875,6.25),'s02':(0.0,4.5),'s03':(1.833,6.583),'s04':(0.375,6.583),'s05':(1.167,6.583),'s06':(0.208,6.583),'s07':(0.875,6.333),'s08':(0.25,5.75),'s09':(1.25,3.25),'s10':(1.375,7.417),'s11':(0.625,6.583),'s12':(1.792,6.583),'s13':(1.083,6.583),'s14':(0.5,4.5),'s15':(2.708,8.0),'s16':(2.583,6.583),'s17':(0.0,4.5),'s18':(1.75,6.583),'s19':(0.583,6.583),'s20':(1.0,4.5),'s21':(0.0,6.583),'s21b':(0.0,4.042),'s22':(1.625,4.75),'s23':(1.333,6.583),'s24':(0.75,6.25),'s25':(0.708,6.417),'s26':(0.958,6.542),'s27':(0.083,6.25),'s28':(0.25,4.5),'s29':(2.083,6.583),'s30':(0.75,8.0),'s31':(1.0,6.583),'s32':(2.5,5.0),'s33':(0.25,5.75),'s34':(2.042,6.5),'s35':(1.292,6.583),'s36':(1.667,6.583),'s37':(0.583,6.583),'s38':(0.25,2.5),'s39':(0.667,3.167),'s40':(1.375,4.5),'s41':(2.5,8.0)}
seed={'s01':9301102,'s03':9301102,'s04':9301102,'s06':9301102,'s08':9301102,'s09':9301102,'s11':9301102,'s12':9301102,'s15':9301102,'s21':9301102,'s21b':9301102,'s26':9301102,'s27':9301102,'s29':9301201,'s30':9301102,'s31':9301102,'s32':9301201,'s38':9301102,'s40':9301102,'s41':9301301}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9301101)' for s in p if s not in seed and p[s]['seed']!=9301101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (none may)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# the recordings the edit table lays were rewritten in audio/ (originals in audio/orig/; _note RECORDINGS): a14 and a26 are now
# s15's and s26's own take voices with one word spliced in from the recording (voice_off s15 s26). Stop if a rewrite is missing.
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e930-dh/audio
for n in 02 08 13 14 16 19 20 21 22 24 26 28 32 36; do [ -f $A/orig/zq930a$n.wav ] || { echo "audio/zq930a$n.wav is not the leveled/spliced file (no orig/ copy)"; exit 1; }; done
# nothing is dropped in e930 (DROP empty; all 42 shots are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e030-r2/overlays.json $P/hailuo/edit-dh-e930-live.json $E $E/cut/e930-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e930-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END (e929's template): s41 is the arc's last shot and the hook (the yard after Wei's 你……怎麼會在這裡: Xu turns to the gate,
# A-Ling at the well, Wei frozen at the gate): gong_02 rings from c4.0, the picture fades out over c5.10-5.50 (vf) and min holds
# black while the gong rings out; the sound fades over the last 1.0 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e930-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e930-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e930-live.lim.mp4 && mv $E/cut/e930-live.lim.mp4 $E/cut/e930-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e930-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e930-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e930-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
