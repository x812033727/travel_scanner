#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e922/zhong-tian-qu-qi-e922-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e022-r2/video.json
# POLISH+SWAP 2026-11-22: the 2026-11-17 cut files (lines.json, srt, final.log; its mp4 is review-zt/ep/e022/final.mp4) go to
# cut/old-1117 once and carry a .keep (never removed); a later run replaces its own previous cut (no old-HHMM).
mkdir -p $E/cut
[ -d $E/cut/old-1117 ] || { mkdir -p $E/cut/old-1117; mv $E/cut/e922-live.* $E/cut/final.log $E/cut/old-1117/ 2>/dev/null; touch $E/cut/old-1117/.keep; }
rm -f $E/cut/e922-live.* $E/cut/final.log; rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 22; the refine sources are not on this machine, so the script
# no longer re-stages by itself -- it stops and says so)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 22"; exit 1; }
# e922 trims and seeds the edit table assumes (edit-dh-e922-live.json _note): picks.json as refine-prep.py 22 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e922-live: refine-prep.py 22
# picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 22) -- the fix1 retakes s09 (9221201) and s32
# (9221202); review3-trims.tsv (first cut) shortens the silent tails of s01 s03 s05 s09 s11 s13 s14 s15 s17 s19 s20 s26
# s30 s31 s35 s35b s40 s41; REVIEW 3 (review3-plan.md) re-trims s07 (end 3.5), s14 (end 4.667), s33 (start 2.0), s38
# (end 3.084) and moves s39 to 1.5-3.5 (the empty moored boat out). Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance
# 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.25,5.875),'s02':(1.916,6.584),'s03':(0,4.625),'s04':(0.75,3.5),'s05':(0,5.542),'s06':(0,8),'s07':(0,3.5),
 's08':(0.75,8),'s09':(0,3.583),'s10':(0.75,8),'s11':(0,4),'s12':(1.25,6.584),'s13':(0,4.333),'s14':(0,4.667),
 's15':(0.5,4.958),'s16':(2,6.584),'s17':(0,6.708),'s18':(0.625,6.584),'s19':(0,4.125),'s20':(0.75,3.667),
 's21':(0.5,6.584),'s22':(0.5,6.584),'s23':(0.416,6.584),'s24':(0.5,6.584),'s25':(0.5,5),'s26':(0,5.833),
 's27':(0,6.584),'s28':(0.75,3),'s29':(0,2.5),'s30':(0,7.542),'s31':(0,5.25),'s32':(0.5,5.25),'s33':(2,6.584),
 's34':(1.25,4.5),'s35':(0,5.958),'s35b':(0,4),'s36':(0.916,6.584),'s37':(1.25,6),'s38':(0,3.084),'s39':(1.5,3.5),
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
# POLISH+SWAP 2026-11-22 (edit table _note). SWAP: clips/sNN-t5.mp4 (runpod/polish/picks.json, already trimmed; wave 1
# fix-polish/review-picks.tsv: s22 9229101 0.583-6.25; wave 2 round4/review-picks.tsv: s17 9229401 0-7.0, s33 9229401
# 0.5-6.583, s40 9229402 0.25-4.75; round5: s14 9229502 1.791-6.583) win over t1; picks.json and the want table above
# describe the t1 staging. Clips cut here from t1 (the assembler takes the highest take number; remade when missing):
#  s19-t2 = t1 (4.125 s) + t1 1.75-4.125 played backwards (2.375 s) = 6.5 s: s20 is dropped and its a18 follows a17 off
#   screen over the abacus insert; the draft's longer take is not on this machine, and from c1.0 the hand only grips the
#   abacus, so the reversed part reads as the same hold (review C);
#  s39-t2 = t1's first 42 frames (1.75 s; the bow of the moored boat at the right edge from c1.8 goes -- review G).
C=$E/clips; X264="-c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k"
[ -f $C/s19-t2.mp4 ] || ffmpeg -v error -y -i $C/s19-t1.mp4 -f lavfi -t 6.5 -i anullsrc=r=48000:cl=stereo -filter_complex "[0:v]split[a][b];[b]trim=start=1.75,setpts=PTS-STARTPTS,reverse[r];[a][r]concat=n=2:v=1:a=0,fps=24,trim=duration=6.5[v]" -map "[v]" -map 1:a $X264 -shortest $C/s19-t2.mp4
[ -f $C/s39-t2.mp4 ] || ffmpeg -v error -y -i $C/s39-t1.mp4 -frames:v 42 -t 1.75 $X264 $C/s39-t2.mp4
# REVIEW-POLISH drops s38 (the 3D-render courtyard; s37 追啊！燈籠就在屋簷下 cuts to s39 on the jetty -- review B) and s20 (the
# outdoor wall, another jacket, no soup pot -- review C); s20's line zq922a18 moves to the end of s19 (off screen, line_at 3.9).
# picks.json and the want table keep both shots (staged, just not cut in); $VL is video.json without them.
VL=$E/video-live.json; DROP="s20 s38"
python3 -c "
import json;v=json.load(open('$VJ'));sc={s.get('id'):s for s in v['scenes']}
sc['s19'].setdefault('lines',[]).extend(sc['s20'].get('lines',[]));sc['s20']['lines']=[]
d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
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
# POLISH+SWAP 2026-11-22 (e912/e923 lesson): the true peak after loudnorm2; above -1.5 dBTP a second sample-peak limiter at 0.7
# touches just those peaks; the delivery wants <= -1 dBTP: printed on the final file
TP=$(ffmpeg -hide_banner -nostats -i $E/cut/e922-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e922-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e922-live.lim.mp4 && mv $E/cut/e922-live.lim.mp4 $E/cut/e922-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -nostats -i $E/cut/e922-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e922-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
