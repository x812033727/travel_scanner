#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e924/zhong-tian-qu-qi-e924-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e024-r2/video.json
# POLISH+SWAP 2026-11-21: the 2026-11-17 cut files (lines.json, srt, final.log; the mp4 is review-zt/ep/e024/final.mp4) go to
# cut/old-1117 once, with a .keep (kept for the backup); an old-* holding a .keep is never removed. A later run moves its own
# previous cut to old-HHMM after removing the non-kept old-* (at most one old cut besides the kept one: the disk is short).
mkdir -p $E/cut
[ -d $E/cut/old-1117 ] || { mkdir -p $E/cut/old-1117; mv $E/cut/e924-live.* $E/cut/final.log $E/cut/old-1117/ 2>/dev/null; touch $E/cut/old-1117/.keep; }
[ -f $E/cut/e924-live.mp4 ] && { for d in $E/cut/old-*; do [ -f $d/.keep ] || rm -rf $d; done; mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e924-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 24 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 24 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e924-dh/audio and $E/music -> zhong-tian-qu-qi-e924-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e924, the e923 way). Every effect is in the series library.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 24 || exit 1; }
# e924 trims and seeds the edit table assumes (edit-dh-e924-live.json _note): picks.json as refine-prep.py 24 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e924-live: refine-prep.py 24
# picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 24) -- the fix1 retakes s17, s34, s35 (9241201);
# review3-trims.tsv (first cut) shortens the silent tails over ~1 s; REVIEW 3 (review3-plan.md) adds s10 end 4.5,
# s14 end 5.125, s19 start 1.917, s22 start 1.083 and s31 start 1.0. Whole frames: a start rounded DOWN and an end-before
# rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0,5.542),'s02':(2,4.5),'s03':(1.583,6.584),'s04':(0.5,6.584),'s05':(0,6.584),'s06':(0.708,7.334),'s07':(1.375,6.584),'s08':(0,5.167),'s09':(0,5.042),'s10':(0.5,4.5),'s11':(2.25,6.584),'s12':(0,4.417),'s13':(0.25,4),'s14':(0,5.125),'s15':(0.583,5.625),'s15b':(0,6.709),'s16':(0,4.584),'s17':(0,4.5),'s18':(1.166,6.584),'s19':(1.917,8),'s20':(1,6.584),'s21':(0.5,3.5),'s22':(1.083,6.584),'s23':(1.666,6.584),'s24':(0,4),'s25':(0.791,5.459),'s26':(1.5,4.334),'s27':(0.791,6.584),'s28':(0,8),'s29':(0,6),'s30':(0,5.25),'s31':(1,6.584),'s32':(0.5,6),'s33':(2.25,4.25),'s34':(0.875,5.167),'s35':(1.166,6.584),'s36':(1,8)}
seed={'s03':9241102,'s04':9241102,'s06':9241102,'s10':9241102,'s11':9241102,'s12':9241102,'s13':9241102,'s14':9241102,'s15':9241102,'s28':9241102,'s31':9241102,'s32':9241102,'s36':9241102,'s17':9241201,'s34':9241201,'s35':9241201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9241101)' for s in p if s not in seed and p[s]['seed']!=9241101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-21 (edit table _note). SWAP: s19 and s24 are the fixp retakes clips/sNN-t5.mp4 (runpod/polish/picks.json,
# already trimmed: s19 9249101 1.458-7.25, s24 9249101 0-4.5; the assembler takes the highest take number); picks.json and the
# want table above still describe the t1 staging, which stays on disk. SWAP wave 2 (2026-11-22): s34 is the fixp4 retake
# clips/s34-t5.mp4 (9249401 0-4.5, already trimmed; t1 kept); no t6 is cut for any e924 shot. POLISH (free fix 4): s01 ends at 5.208 (clips/s01-t2.mp4
# = s01-t1 0-5.208, 125 frames: a01 laid at 0.30 ends 4.98 + the 0.22 tail, so nothing is held); made if missing, t1 kept.
C=$E/clips; ENC="-c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000"
[ -f $C/s01-t2.mp4 ] || ffmpeg -v error -threads 2 -y -i $C/s01-t1.mp4 -t 5.208 $ENC $C/s01-t2.mp4
# the episode sfx dir (second sfx_dirs entry), made if missing: murmur24 = crowd-murmur.py 24 64 (this episode's recordings
# reversed, -19 LUFS) under the street s01-s12 (the review's market crowd; ancient-market-loop is barred)
[ -f /root/mokaair-work/videos/zhong-tian-qu-qi-e924-dh/sfx/murmur24.wav ] || python3 -I $Q/crowd-murmur.py 24 64
# nothing is dropped in e924 (DROP empty; all 37 shots with s15b are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e024-r2/overlays.json $P/hailuo/edit-dh-e924-live.json $E $E/cut/e924-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e924-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END: s36 is Wei Shaoqing's line at the window; his clip voice ends ~c6.53 (voice_until 6.60 ends a35's subtitle there),
# the low hit and the gong at c6.62, the picture fades over c6.60-7.00 (vf, the take ends at c7.00) and min 10.50 holds
# ~3.5 s of black; REVIEW 3: the sound fades over the last 1.0 s (was 1.5), so the fade still starts ~2.9 s after the gong
# (gong_02 at about -30 there, as e923) -- with min 9.5 it would start 1.4 s after it (-19) and cut the gong.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e924-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e924-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e924-live.lim.mp4 && mv $E/cut/e924-live.lim.mp4 $E/cut/e924-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e924-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e924-live.mp4
# POLISH+SWAP 2026-11-21: a second alimiter after loudnorm2 (0.7 = -3.1 dBFS, the e904/e916 way) takes any peak the AAC
# re-encode lifts past the first one with the louder music; the level stays -14.0 LUFS.
ffmpeg -v error -y -i $E/cut/e924-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=5:release=50:level=false,aresample=48000" $E/cut/e924-live.lim2.mp4 && mv $E/cut/e924-live.lim2.mp4 $E/cut/e924-live.mp4
# the delivery wants the true peak at or under -1 dBTP: print it (ebur128 true peak on the final file)
ffmpeg -hide_banner -nostats -i $E/cut/e924-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e924-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
