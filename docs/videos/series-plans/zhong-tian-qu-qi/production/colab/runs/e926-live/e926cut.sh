#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e926/zhong-tian-qu-qi-e926-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e026-r2/video.json
# POLISH+SWAP 2026-11-22: the 2026-11-17 cut files (lines.json, srt, final.log; its mp4 is review-zt/ep/e026/final.mp4) go to
# cut/old-1117 once and carry a .keep (never removed); a later run replaces its own previous cut (no old-HHMM).
mkdir -p $E/cut
[ -d $E/cut/old-1117 ] || { mkdir -p $E/cut/old-1117; mv $E/cut/e926-live.* $E/cut/final.log $E/cut/old-1117/ 2>/dev/null; touch $E/cut/old-1117/.keep; }
rm -f $E/cut/e926-live.* $E/cut/final.log; rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 26; the refine sources are not on this machine, so the script
# no longer re-stages by itself -- it stops and says so)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 26"; exit 1; }
# e926 trims and seeds the edit table assumes (edit-dh-e926-live.json _note): picks.json as refine-prep.py 26 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e926-live: refine-prep.py 26
# picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 26) -- the fix1 retakes s28 (9261201), s35
# (9261202), s40 (9261201); review3-trims.tsv (first cut): s10, s11, s16, s23 end at the take's end 6.584 (the old ends cut
# the second half of each line out of the take's own voice), s30b start 0.708 (the old 1.000 cut 放心 in half), s09 start 0.333 (the old 1.000 cut the first 是我); the silent
# tails over ~1 s cut: s01 end 4.875, s15 end 7.125, s25 end 3.875, s26 end 4.083, s27 end 4.792, s35 end 4.667; REVIEW 3
# (review3-plan.md, both cut reviews): s19 start 1.833, s25 end 3.375, s27 end 4.000, s35 end 4.000, s37 start 1.083,
# s38 start 1.500, s39 end 2.250. Whole frames:
# a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.5,4.875),'s02':(0.25,4.75),'s03':(0.458,4.875),'s04':(0.458,6.334),'s05':(0.416,6.584),'s06':(0.75,5.0),'s07':(1.0,6.0),'s08':(1.0,5.0),'s09':(0.333,6.584),'s10':(1.375,6.584),'s11':(0.458,6.584),'s12':(0.5,5.0),'s13':(0.5,5.25),'s14':(0.625,6.334),'s15':(0.5,7.125),'s16':(1.083,6.584),'s17':(0.458,4.584),'s18':(0.0,6.584),'s19':(1.833,6.584),'s20':(0.5,6.0),'s21':(0.5,5.75),'s22':(0.0,4.334),'s23':(1.583,6.584),'s24':(0.5,6.0),'s25':(0.0,3.375),'s26':(0.0,4.083),'s27':(0.5,4.0),'s28':(1.5,3.75),'s29':(0.458,6.584),'s30':(0.5,5.25),'s30b':(0.708,4.959),'s31':(0.25,3.0),'s32':(0.583,5.875),'s33':(0.5,3.0),'s34':(0.458,6.25),'s35':(0.333,4.0),'s36':(0.5,3.25),'s37':(1.083,6.584),'s38':(1.5,4.584),'s39':(0.0,2.25),'s40':(0.0,8.0)}
seed={'s01':9261102,'s02':9261102,'s03':9261102,'s04':9261102,'s06':9261102,'s07':9261102,'s10':9261102,'s11':9261102,'s12':9261102,'s13':9261102,'s15':9261102,'s16':9261102,'s17':9261102,'s19':9261102,'s20':9261102,'s21':9261102,'s23':9261102,'s27':9261102,'s28':9261201,'s30':9261102,'s30b':9261102,'s32':9261102,'s33':9261102,'s34':9261102,'s35':9261202,'s36':9261102,'s37':9261102,'s38':9261102,'s40':9261201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9261101)' for s in p if s not in seed and p[s]['seed']!=9261101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-22 (edit table _note). SWAP: clips/sNN-t5.mp4 (runpod/polish/picks.json, already trimmed; wave 1
# fix-polish/review-picks.tsv: s25 9269101 0-6.583, s28 9269102 0-2.333, s32 9269102 0.333-5.583, s37 9269101 0.875-6.583,
# s38 9269102 0-6.583, s39 9269101 0-5.167; wave 2 round4/review-picks.tsv: s11 9269402 from 0.375, s27 9269402 whole;
# round5: s08 9269502 0-6.583) win over t1; picks.json and the want table above describe the t1 staging. Clips cut here
# (the assembler takes the highest take number and has no per-shot trim; each remade when missing -- delete one to re-cut):
#  s08-t6 = t5 0-5.0 (the limp: sinks c1.0, 2.1, 4.15; a08 at c1.15 between them); s25-t6 = t5 0-3.5 (a26 2.8 s + tail);
#  s27-t6 = t5 0-4.25 (a28 c0.40-3.57, he bends lower to the end); s38-t6 = t5 1.5-4.75 (staggers, knees c1.6, body c2.1,
#  paper c2.45); s39-t6 = t5 0-3.25 (feet 0-2.0, the paper lifts and the white packet lands c2.4-2.9);
#  s40-t6 = t1 0-5.75 (free fix: the picture fades c5.2-5.7 (vf), min 7.7 holds 2 s of black for the gong at c2.27).
C=$E/clips; X264="-c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k"
cutclip() { [ -f $C/$1-t6.mp4 ] || ffmpeg -v error -y -ss $3 -i $C/$1-$2.mp4 -t $4 -frames:v $(python3 -c "print(round($4*24))") $X264 $C/$1-t6.mp4; }
cutclip s08 t5 0 5.0; cutclip s25 t5 0 3.5; cutclip s27 t5 0 4.25; cutclip s38 t5 1.5 3.25; cutclip s39 t5 0 3.25; cutclip s40 t1 0 5.75
# nothing is dropped in e926 (DROP empty; all 41 shots with s30b are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e026-r2/overlays.json $P/hailuo/edit-dh-e926-live.json $E $E/cut/e926-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e926-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END (POLISH 2026-11-22): s40 the off-screen scream a36 (c0.30-1.66), gasps, hurried steps and the murmur from c1.4, the low
# hit, the gong and z-cue-cliffhanger at c2.27, the picture fades c5.2-5.7 (vf) and min 7.7 holds black while the gong rings
# out; the sound fades over the last 1.0 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e926-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e926-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e926-live.lim.mp4 && mv $E/cut/e926-live.lim.mp4 $E/cut/e926-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e926-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e926-live.mp4
# POLISH+SWAP 2026-11-22 (e912/e923 lesson): the true peak after loudnorm2; above -1.5 dBTP a second sample-peak limiter at 0.7
# touches just those peaks; the delivery wants <= -1 dBTP: printed on the final file
TP=$(ffmpeg -hide_banner -nostats -i $E/cut/e926-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e926-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e926-live.lim.mp4 && mv $E/cut/e926-live.lim.mp4 $E/cut/e926-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -nostats -i $E/cut/e926-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e926-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
