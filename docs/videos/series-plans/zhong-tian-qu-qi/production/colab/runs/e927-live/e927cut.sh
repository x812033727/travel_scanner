#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e927/zhong-tian-qu-qi-e927-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e027-r2/video.json
# POLISH+SWAP 2026-11-22: the 2026-11-17 cut files (lines.json, srt, final.log; its mp4 is review-zt/ep/e027/final.mp4) go to
# cut/old-1117 once and carry a .keep (never removed); a later run's previous cut goes to cut/prev-HHMM (nothing is deleted).
mkdir -p $E/cut
[ -d $E/cut/old-1117 ] || { mkdir -p $E/cut/old-1117; mv $E/cut/e927-live.* $E/cut/final.log $E/cut/old-1117/ 2>/dev/null; touch $E/cut/old-1117/.keep; }
ls $E/cut/e927-live.* >/dev/null 2>&1 && { PV=$E/cut/prev-$(date +%H%M); mkdir -p $PV; mv $E/cut/e927-live.* $E/cut/final.log $PV/ 2>/dev/null; }
rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 27 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 27 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e927-dh/audio and $E/music -> zhong-tian-qu-qi-e927-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e927, the e926 way). Every effect is in the series library except snort927.wav (s21's sneer, cut
# from the laugh dropped off a20; zhong-tian-qu-qi-e927-dh/sfx, the edit table's second sfx dir).
# POLISH+SWAP 2026-11-22: the refine sources are not on this machine, so the script no longer re-stages by itself -- it stops and says so
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 27"; exit 1; }
# e927 trims and seeds the edit table assumes (edit-dh-e927-live.json _note): picks.json as refine-prep.py 27 builds it from
# picks-merged.tsv and review3-trims.tsv (run in colab/runs/e927-live: refine-prep.py 27 picks-merged.tsv review3-trims.tsv,
# then stage.py 27; no fix round in e927). review3-trims.tsv (first cut): s01 end 3.500 -> 6.375, s12 end 4.917 -> 6.584 and
# s27 end 5.125 -> 6.584 (the picks were cut to lay recordings; the takes' own voices go on to 誰家的糖，吃倒了人, 去綢緞莊等我
# and 沒讓人看見吧), s21 start 1.208 -> 1.000 (a20-trim and the snort fit without a held frame); REVIEW 3 (review3-plan.md): s03 end
# 6.209 -> 5.500, s10 end 3.500 -> 3.000, s16 start 0.791 -> 1.291, s26 end 4.000 -> 3.250, s29 end 4.000 -> 3.000. s19 keeps its crop
# 800:452:0:0 from picks-merged.tsv (stage.py crops and scales it 1.2x; the white banner with false characters is out).
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop).
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.083,6.375),'s02':(0.0,3.584),'s03':(0.75,5.5),'s04':(0.0,3.0),'s05':(0.5,4.5),'s06':(0.541,7.792),'s07':(1.541,6.375),'s08':(0.875,5.0),'s09':(0.0,3.0),'s10':(0.5,3.0),'s11':(0.5,5.0),'s12':(1.208,6.584),'s13':(0.5,4.5),'s14':(0.0,6.459),'s15':(0.333,6.584),'s16':(1.291,8.0),'s17':(0.5,5.667),'s18':(0.25,6.584),'s19':(0.0,8.0),'s20':(0.333,4.709),'s21':(1.0,5.875),'s22':(1.0,4.5),'s23':(0.25,6.334),'s24':(0.75,6.459),'s25':(1.125,4.667),'s26':(0.0,3.25),'s27':(0.291,6.584),'s28':(1.5,6.584),'s29':(0.0,3.0),'s30':(0.375,6.292),'s31':(2.5,6.584),'s32':(0.5,5.917),'s33':(2.125,6.584),'s34':(0.583,6.584),'s35':(0.0,3.0),'s36':(2.166,6.167),'s37':(0.0,8.0)}
seed={'s01':9271102,'s05':9271102,'s06':9271102,'s08':9271102,'s09':9271102,'s11':9271102,'s12':9271102,'s13':9271102,'s15':9271102,'s17':9271102,'s20':9271102,'s22':9271102,'s24':9271102,'s25':9271102,'s26':9271102,'s28':9271102,'s29':9271102,'s31':9271102,'s33':9271102,'s34':9271102,'s35':9271102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9271101)' for s in p if s not in seed and p[s]['seed']!=9271101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (want 800:452:0:0 on s19 only)' for s in p if p[s].get('crop')!=('800:452:0:0' if s=='s19' else None)]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-22 (edit table _note). SWAP: clips/sNN-t5.mp4 (runpod/polish/picks.json, already trimmed; wave 1
# fix-polish/review-picks.tsv: s06 9279102 from 0.708, s07 9279102 whole (its line ends 0.16 s before the last frame -- never
# trim its tail, POST-SWAP e027), s08 9279101 0.333-5.5; wave 2 round4/review-picks.tsv: s30 9279401 from 0.25) win over t1;
# picks.json and the want table above describe the t1 staging. Clips made here (the assembler takes the highest take number
# and has no per-shot trim; each remade only when missing -- delete one to re-make):
#  s01-t6 = s01-t1 with the picture of c1.292-3.292 (frames 31-78) replaced by e926 s40-t1 c4.0-6.0 (the customer down in the
#   street, three or four people round him; free fix A: four shots in the first 10 s, the 2.4 s pause gets a picture, the
#   27 <- 26 joint is shown); the sound is s01-t1's own, untouched (clip_af s01 still splits it at 1.2 s);
#  s03-t6 = s03-t1 0-4.542 (109 frames; free fix E: the mouth opens again from frame 109 = c4.54);
#  s35-t6 = s35-t1 1.833-3.0 (28 frames; free fix F: only the stretch where the hairpin shadow is there throughout; min 1.25).
C=$E/clips; X264="-c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k"
cutclip() { [ -f $C/$1-t6.mp4 ] || nice ffmpeg -v error -y -ss $3 -i $C/$1-$2.mp4 -t $4 -frames:v $(python3 -c "print(round($4*24))") $X264 $C/$1-t6.mp4; }
cutclip s03 t1 0 4.542; cutclip s35 t1 1.833 1.167
E26=/root/mokaair-work/videos/_live-e926/zhong-tian-qu-qi-e926-dh/clips/s40-t1.mp4
[ -f $C/s01-t6.mp4 ] || nice ffmpeg -v error -y -i $C/s01-t1.mp4 -i $E26 -filter_complex "[0:v]split[v0][v2];[v0]trim=start_frame=0:end_frame=31,setpts=PTS-STARTPTS[p0];[1:v]trim=start=4.0:duration=2.0,setpts=PTS-STARTPTS,fps=24,scale=1312:736,setsar=1[p1];[v2]trim=start_frame=79,setpts=PTS-STARTPTS[p2];[p0][p1][p2]concat=n=3:v=1:a=0,format=yuv420p[v]" -map "[v]" -map 0:a -c:v libx264 -crf 14 -preset slow -c:a aac -b:a 192k -shortest $C/s01-t6.mp4
# episode sounds (zhong-tian-qu-qi-e927-dh/sfx, made by hand 2026-11-22, see _note): laugh927 (s21's own laugh x0.70),
# wardrum927 (four rising hits of war-drum-01), ting927 (impactPlate_light_000 high-passed), murmur27 (crowd-murmur.py 27 20)
S9=/root/mokaair-work/videos/zhong-tian-qu-qi-e927-dh/sfx
for f in laugh927 wardrum927 ting927; do [ -f $S9/$f.wav ] || { echo "missing $S9/$f.wav (see the edit table _note)"; exit 1; }; done
[ -f $S9/murmur27.wav ] || python3 -I $Q/crowd-murmur.py 27 20
# nothing is dropped in e927 (DROP empty; all 37 shots are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e027-r2/overlays.json $P/hailuo/edit-dh-e927-live.json $E $E/cut/e927-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e927-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END: s37 is the suspense tail (8 s): A-ling's cold a32 under the veil, the swish as she raises the sheathed knife (c1.0; the stick slaps are out, REVIEW 3),
# the low hit and the gong at c5.5; REVIEW 3: a slow 1.00 -> 1.06 push, the picture fades out over c5.60-6.00 (vf, while the
# knife is still in frame) and min 10.0 holds black while the gong rings out (gong_02 ends at c10.0); the sound fades over the last 1.0 s.
# POLISH+SWAP 2026-11-22 (free fix I): min 8.5 -- 2.5 s of black; the rising drum c4.0-5.5 into the gong, which the 1.0 s fade ends.
# POLISH+SWAP 2026-11-22 (free fix I): CC 1 split in two -- 讓開！ on its own (0.40-1.20) and 誰家的糖，吃倒了人？ from 3.45 (the
# take says 誰 at c3.54); the audio is untouched. The srt is rewritten and the mp4's mov_text track replaced from it.
python3 - "$E/cut/e927-live.zh-TW.srt" <<'PYS'
import re,sys
p=sys.argv[1]; b=open(p,encoding='utf-8').read().strip().split('\n\n')
f=lambda t:sum(float(x)*m for x,m in zip(t.replace(',','.').split(':'),(3600,60,1)))
g=lambda v:'%02d:%02d:%02d,%03d'%(int(v//3600),int(v%3600//60),int(v%60),round((v-int(v))*1000)%1000)
cues=[(c.split('\n')[1],'\n'.join(c.split('\n')[2:])) for c in b]
t0,txt=cues[0]
if txt=='讓開！誰家的糖，吃倒了人？':
    a,e=[f(x) for x in t0.split(' --> ')]
    cues[0:1]=[(f'{g(a)} --> {g(1.20)}','讓開！'),(f'{g(3.45)} --> {g(e)}','誰家的糖，吃倒了人？')]
    print('CC 1 split:',cues[0][0],'|',cues[1][0])
else: print('CC 1 not split (text:',txt,')')
open(p,'w',encoding='utf-8').write('\n\n'.join(f'{i+1}\n{t}\n{x}' for i,(t,x) in enumerate(cues))+'\n')
PYS
ffmpeg -v error -y -i $E/cut/e927-live.mp4 -i $E/cut/e927-live.zh-TW.srt -map 0:v -map 0:a -map 1:0 -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=chi -movflags +faststart $E/cut/e927-live.sub.mp4 && mv $E/cut/e927-live.sub.mp4 $E/cut/e927-live.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e927-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e927-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e927-live.lim.mp4 && mv $E/cut/e927-live.lim.mp4 $E/cut/e927-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e927-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e927-live.mp4
# POLISH+SWAP 2026-11-22 (e912/e923 lesson): the true peak after loudnorm2; above -1.5 dBTP a second sample-peak limiter at 0.7
# touches just those peaks; the delivery wants <= -1 dBTP: printed on the final file
TP=$(ffmpeg -hide_banner -nostats -i $E/cut/e927-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e927-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e927-live.lim.mp4 && mv $E/cut/e927-live.lim.mp4 $E/cut/e927-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -nostats -i $E/cut/e927-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e927-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
