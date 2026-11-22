#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e925/zhong-tian-qu-qi-e925-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e025-r2/video.json
# POLISH+SWAP 2026-11-21/22: the 2026-11-17 cut files (lines.json, srt, final.log; its mp4 is review-zt/ep/e025/final.mp4) go to
# cut/old-1117 once and carry a .keep (never removed); a later run replaces its own previous cut (no old-HHMM).
mkdir -p $E/cut
[ -d $E/cut/old-1117 ] || { mkdir -p $E/cut/old-1117; mv $E/cut/e925-live.* $E/cut/final.log $E/cut/old-1117/ 2>/dev/null; touch $E/cut/old-1117/.keep; }
rm -f $E/cut/e925-live.* $E/cut/final.log; rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 25; the refine sources are not on this machine, so the script
# no longer re-stages by itself -- it stops and says so)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 25"; exit 1; }
# e925 trims and seeds the edit table assumes (edit-dh-e925-live.json _note): picks.json as refine-prep.py 25 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e925-live: refine-prep.py 25
# picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 25) -- the fix1 retakes s06 (9251202), s18
# (9251201), s27 (9251202), s32 (9251202), s33 (9251201); review3-trims.tsv (first cut): s01 end 4.25, s03 2.333-6.584
# (the take's own voice, whole line), s15 and s37 start 0.375 (the first sentence back, cropped in the edit table), s34 and
# s35 end at the take's end; the silent tails over ~1 s cut: s16 end 2.875, s25 end 4.0, s39 end 2.583; REVIEW 3
# (review3-plan.md) changes s01 start 0.125, s02 start 0.75, s12 end 4.25, s26 end 5.75 and s27 2.5-4.0. Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance
# 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.125,4.25),'s02':(0.75,3.0),'s03':(2.333,6.584),'s04':(2.375,6.584),'s05':(0.5,4.0),'s06':(1.0,6.584),'s07':(0.0,4.75),'s08':(1.625,5.0),'s09':(2.5,6.584),'s10':(0.5,5.25),'s11':(0.375,6.584),'s12':(1.5,4.25),'s13':(0.375,6.584),'s14':(0.5,5.25),'s15':(0.375,6.584),'s16':(0.0,2.875),'s17':(0.0,4.25),'s18':(0.375,5.25),'s19':(0.5,4.5),'s20':(0.0,6.584),'s20b':(0.0,5.0),'s21':(0.75,5.25),'s22':(0.5,3.25),'s23':(1.0,5.167),'s23b':(0.0,4.0),'s24':(0.5,4.75),'s25':(1.0,4.0),'s26':(1.75,5.75),'s27':(2.5,4.0),'s28':(0.5,3.0),'s29':(0.0,3.5),'s30':(0.75,4.0),'s31':(0.0,5.167),'s32':(0.0,4.25),'s33':(0.375,8.0),'s34':(0.625,6.584),'s35':(0.75,6.584),'s36':(0.5,4.5),'s37':(0.375,6.584),'s38':(0.0,2.5),'s39':(0.0,2.583),'s40':(0.25,5.375),'s40b':(0.0,8.0)}
seed={'s02':9251102,'s06':9251202,'s07':9251102,'s08':9251102,'s10':9251102,'s11':9251102,'s12':9251102,'s13':9251102,'s14':9251102,'s15':9251102,'s16':9251102,'s17':9251102,'s18':9251201,'s23':9251102,'s23b':9251102,'s24':9251102,'s27':9251202,'s29':9251102,'s30':9251102,'s31':9251102,'s32':9251202,'s33':9251201,'s34':9251102,'s35':9251102,'s36':9251102,'s38':9251102,'s39':9251102,'s40':9251102,'s40b':9251102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9251101)' for s in p if s not in seed and p[s]['seed']!=9251101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-21 (edit table _note). SWAP: clips/s01 s27 s32-t5.mp4 (runpod/polish/picks.json, already trimmed: s01
# 9259101 0.625-4.375, s27 9259102 0.75-2.375, s32 9259102 0-4.458) win over t1; picks.json and the want table above describe
# the t1 staging. Clips cut here from t1 (the assembler takes the highest take number; remade when missing):
#  s16-t2 = t1 from frame 6 (0.25 s; the brush in her hand for two frames, gone, then back -- review light 1);
#  s26-t2 = t1's first 78 frames (3.25 s; draft 5.00: her last frame a closed-mouth look, the grin after it gone -- medium 2);
#  s28-t2 = t1 from frame 26 (1.083 s; the 1.5 s held pose before the flick -- medium 7).
C=$E/clips; X264="-c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k"
[ -f $C/s16-t2.mp4 ] || ffmpeg -v error -y -i $C/s16-t1.mp4 -vf "select='gte(n,6)',setpts=PTS-STARTPTS" -af "atrim=start=0.25,asetpts=PTS-STARTPTS" $X264 $C/s16-t2.mp4
[ -f $C/s26-t2.mp4 ] || ffmpeg -v error -y -i $C/s26-t1.mp4 -frames:v 78 -t 3.25 $X264 $C/s26-t2.mp4
[ -f $C/s28-t2.mp4 ] || ffmpeg -v error -y -i $C/s28-t1.mp4 -vf "select='gte(n,26)',setpts=PTS-STARTPTS" -af "atrim=start=1.0833,asetpts=PTS-STARTPTS" $X264 $C/s28-t2.mp4
# POLISH: s38 is dropped (the hooded cabin boat, the thin leafy canes s39 does not match, the empty jetty -- medium 6; s37 cuts
# to s39's note between the loosened canes) and s22 plays before s21 (the boats come out of the fog, then Erniu shouts by the
# boat that has come in -- medium 4); $VL is video.json in that order without the DROP shots: the cut, audio-qa and the
# sheets read it.
VL=$E/video-live.json; DROP="s38"
python3 -c "
import json;v=json.load(open('$VJ'));d='$DROP'.split();sc=[s for s in v['scenes'] if s.get('id') not in d]
ids=[s.get('id') for s in sc];i,j=ids.index('s21'),ids.index('s22');sc[i],sc[j]=sc[j],sc[i]
v['scenes']=sc;json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
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
# POLISH+SWAP 2026-11-21 (e912 lesson): the true peak after loudnorm2; above -1.5 dBTP a second sample-peak limiter at 0.7 touches
# just those peaks; the delivery wants <= -1 dBTP: printed on the final file
TP=$(ffmpeg -hide_banner -nostats -i $E/cut/e925-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e925-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e925-live.lim.mp4 && mv $E/cut/e925-live.lim.mp4 $E/cut/e925-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -nostats -i $E/cut/e925-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e925-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
