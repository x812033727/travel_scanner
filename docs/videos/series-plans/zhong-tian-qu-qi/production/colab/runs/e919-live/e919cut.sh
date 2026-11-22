#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e919/zhong-tian-qu-qi-e919-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e019-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e919-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e919-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 19 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 19 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e919-dh/audio and $E/music -> zhong-tian-qu-qi-e919-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e919, the e917/e918 way). Every sound is in the series sfx library.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 19 || exit 1; }
# e919 trims and seeds the edit table assumes (edit-dh-e919-live.json _note): picks.json as refine-prep.py 19 builds it from
# picks-merged.tsv and fix1/review-picks.tsv in that order (run in colab/runs/e919-live) -- the fix1 retakes s09 s16
# (9191201) and s34 (9191202), then review3-trims.tsv (REVIEW 3, review3-plan.md: s08 s09 s29 s33 s35 s36 s38 tails):
# refine-prep.py 19 picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv (a fallback is never written with @), stage.py 19.
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not
# stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.5,5.875),'s02':(1.125,8),'s03':(0,6.584),'s04':(2.25,6.584),'s05':(0.5,10.125),'s06':(0,7.375),'s07':(0.75,5.125),
 's08':(0.5,3),'s09':(0.875,5.25),'s10':(0,6),'s11':(0.875,6.375),'s12':(0,10.125),'s13':(0.5,5.25),'s14':(0.25,6.584),
 's15':(0.75,6.584),'s16':(0.75,8),'s17':(1.625,8),'s18':(1.375,6.5),'s19':(0.375,7.875),'s20':(0,6.584),'s21':(0.5,6.584),
 's22':(0,6.584),'s23':(0.25,8),'s24':(0.75,8),'s25':(3,6.584),'s26':(1.875,8),'s27':(2.5,6.584),'s28':(1.875,6.584),
 's29':(0.75,5),'s30':(0.5,6.125),'s31':(1,6.584),'s32':(0.5,6.584),'s33':(0,5.833),'s34':(0,10.125),'s35':(0,7),
 's36':(0,6.5),'s37':(1.958,6.584),'s38':(0,7),'s39':(0.5,6),'s40':(0.375,6.125),'s41':(0.75,6.584)}
seed={'s01':9191102,'s02':9191102,'s09':9191201,'s11':9191102,'s15':9191102,'s16':9191201,'s17':9191102,'s18':9191102,
 's23':9191102,'s24':9191102,'s26':9191102,'s28':9191102,'s30':9191102,'s31':9191102,'s32':9191102,'s33':9191102,
 's34':9191202,'s36':9191102,'s37':9191102,'s38':9191102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9191101)' for s in p if s not in seed and p[s]['seed']!=9191101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# SWAP 2026-11-21 (review-zt SWAP-BRIEF, merged with the free fixes; runpod/polish/picks.json, fix-polish/review-picks.tsv):
# s01 s20 s21 s26 are the fixp retakes clips/sNN-t5.mp4 (seed 9199101, already trimmed: assemble-v4's pick() takes the
# highest -tN, so the t1 files stay as they were); s31 is not reshot (Aling's half-up hair is the series rule).
# SWAP wave 2 2026-11-22 (round4 fix-polish/round4/review-picks.tsv): s16 s32 are clips/sNN-t5.mp4 (fixp4 9199401, already
# trimmed: s16 0.083-8.0, s32 1.25-6.583); no t6 is cut for this episode. The beds are the Flow z-bed-*/z-cue-* (owner 2026-11-22).
# POLISH+SWAP 2026-11-21 (edit table _note POLISH+SWAP). The episode sfx dir (third sfx_dirs entry), made if missing:
# staff919 = staff-thud-01 from 1.03 s (the strike, e911's staff911) for the constables' staves at s04; flog919 = five
# flogging-far hits 1.05 s apart, low-passed and echoed (far off) under s25/s26; murmur19 = crowd-murmur.py 19 5 (the
# episode's own recordings reversed, owner 2026-11-21) for the street at s37.
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e919-dh/sfx; mkdir -p $S
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/staff919.wav ] || ffmpeg -v error -y -ss 1.03 -t 0.4 -i $X/zhongtian-sfx-staff-thud-01.wav -af "afade=t=out:st=0.25:d=0.15,$AF" $S/staff919.wav
[ -f $S/flog919.wav ] || ffmpeg -v error -y -i $X/zhongtian-sfx-flogging-far-01.wav -i $X/zhongtian-sfx-flogging-far-02.wav -i $X/zhongtian-sfx-flogging-far-03.wav -i $X/zhongtian-sfx-flogging-far-04.wav -i $X/zhongtian-sfx-flogging-far-05.wav \
  -filter_complex "[0]adelay=0|0[a];[1]adelay=1050|1050[b];[2]adelay=2100|2100[c];[3]adelay=3150|3150[d];[4]adelay=4200|4200[e];[a][b][c][d][e]amix=inputs=5:normalize=0,lowpass=f=2500,aecho=0.8:0.5:60|140:0.3|0.2,$AF" $S/flog919.wav
[ -f $S/murmur19.wav ] || python3 -I $P/colab/runs/_scripts/crowd-murmur.py 19 5
# no shot is deleted: the cut, audio-qa and the sheets read video.json itself
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e019-r2/overlays.json $P/hailuo/edit-dh-e919-live.json $E $E/cut/e919-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e919-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 on: attack 8 ms.
# END: s41 is Tang's question a45 laid on her back (nospeak, the take's own murmur muted); the gong at c5.15 after
# 讓嗎 ends, the picture freezes on c4.458 (REVIEW 3: his mouth opens from c4.5, over 讓嗎) and fades over c5.30-5.80
# (vf), and min 8.6 holds ~2.8 s of black (slow_shot s41 1.0: the picture is not slowed to fill it) so the gong rings out
# in the dark. The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e919-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e919-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e919-live.lim.mp4 && mv $E/cut/e919-live.lim.mp4 $E/cut/e919-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e919-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e919-live.mp4
# the finished file's true peak must stay under -1 dBTP (SWAP-BRIEF); print it with the sample peak
ffmpeg -hide_banner -i $E/cut/e919-live.mp4 -map 0:a -af ebur128=peak=true+sample -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e919-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
