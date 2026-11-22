#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e916/zhong-tian-qu-qi-e916-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e016-r2/video.json
# POLISH+SWAP 2026-11-21: the 2026-11-16 cut files (lines.json, srt, final.log; the mp4 is review-zt/ep/e016/final.mp4) go to
# cut/old-1116 once, with a .keep (kept for the backup); an old-* holding a .keep is never removed. A later run moves its own
# previous cut to old-HHMM after removing the non-kept old-* (at most one old cut besides the kept one: the disk is short).
mkdir -p $E/cut
[ -d $E/cut/old-1116 ] || { mkdir -p $E/cut/old-1116; mv $E/cut/e916-live.* $E/cut/final.log $E/cut/old-1116/ 2>/dev/null; touch $E/cut/old-1116/.keep; }
[ -f $E/cut/e916-live.mp4 ] && { for d in $E/cut/old-*; do [ -f $d/.keep ] || rm -rf $d; done; mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e916-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 16 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 16 rewrites picks.json)
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 16 || exit 1; }
# e916 trims and seeds the edit table assumes (edit-dh-e916-live.json _note): picks.json as refine-prep.py 16 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv in that order (run in colab/runs/e916-live) -- the fix1 retakes
# s26 s27 s32 s39 s42 (9161201/9161202); review3-trims.tsv (first cut): s02 s03 s10 s23 s24 s29 s30 s34 s38 ends, 0.55-0.65 s
# after the last word. REVIEW 3 (review3-plan.md, both cut reviews): then review4-trims.tsv (s05 start 2.375, s09 start 2.0,
# s15 start 0.625, s17 start 0.75, s31 end 5.75, s39 end 4.0). s12 stays in picks.json (staged, unused) but is cut from the
# episode: video-live.json below is video.json without it. Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001 (e912
# review 3: -ss keeps a frame at/after start, -to drops a frame whose end passes it); 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0,5),'s02':(0,5.25),'s03':(1.75,6.125),'s04':(0.5,4),'s05':(2.375,6.584),'s06':(0.625,5.75),'s07':(2.125,7),
 's08':(1.75,6.584),'s09':(2.0,8),'s10':(0,4.125),'s11':(0,6.584),'s12':(0.5,4),'s13':(0,7.25),'s14':(0,4.25),'s15':(0.625,6.584),
 's16':(0,4.5),'s17':(0.75,6.584),'s18':(1.25,4.5),'s19':(0.5,4.5),'s20':(0,6.584),'s21':(0.25,4.25),'s22':(0,5.167),'s23':(0,7.5),
 's24':(0.25,4.25),'s25':(1.25,6.584),'s26':(0,6),'s27':(0,5.75),'s28':(0.25,4.584),'s29':(0.5,5.375),'s30':(0,4.5),
 's31':(0.75,5.75),'s32':(0.5,5.5),'s33':(0,4.334),'s34':(0,3.375),'s35':(0,6.584),'s36':(1.5,6.584),'s37':(0.25,4.5),
 's38':(0.75,5.625),'s39':(1,4.0),'s40':(0,4.75),'s41':(0,5.5),'s42':(0.25,5)}
seed={'s01':9161102,'s02':9161102,'s03':9161102,'s06':9161102,'s07':9161102,'s10':9161102,'s11':9161102,'s13':9161102,'s14':9161102,
 's15':9161102,'s18':9161102,'s19':9161102,'s26':9161201,'s27':9161202,'s28':9161102,'s30':9161102,'s31':9161102,'s32':9161202,
 's33':9161102,'s35':9161102,'s37':9161102,'s39':9161201,'s40':9161102,'s41':9161102,'s42':9161201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9161101)' for s in p if s not in seed and p[s]['seed']!=9161101]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-21 (edit table _note). SWAP: s29 and s40 are the fixp retakes clips/sNN-t5.mp4 (runpod/polish/picks.json,
# already trimmed: s29 9169101 0.583-5.459, s40 9169102 1.333-6.25; the assembler takes the highest take number); picks.json and
# the want table above still describe the t1 staging, which stays on disk. POLISH (free fix 3): s26 ends 0.583 s earlier
# (clips/s26-t2.mp4 = s26-t1 0-5.417, before Xu's smile; a25 needs 5.655 s, so the shot is slowed 1.044x, a recorded line)
# and s27 0.5 s earlier (clips/s27-t2.mp4 = s27-t1 0-5.25: a26 ends c4.89 + the 0.34 s tail): made if missing, t1 kept.
C=$E/clips; ENC="-c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000"
[ -f $C/s26-t2.mp4 ] || ffmpeg -v error -threads 2 -y -i $C/s26-t1.mp4 -t 5.417 $ENC $C/s26-t2.mp4
[ -f $C/s27-t2.mp4 ] || ffmpeg -v error -threads 2 -y -i $C/s27-t1.mp4 -t 5.25 $ENC $C/s27-t2.mp4
# SWAP2 2026-11-22 (round4, fix-polish/round4/review-picks.tsv): s11 s27 s32 are clips/sNN-t5.mp4 (s11 9169401 already
# trimmed 0.25-5.417; s27 9169402 and s32 9169401 whole, 6.54 s). s27 and s32 are cut down here to t6 (the assembler takes the
# highest take): s27-t6 = t5 0-5.5 (a26 ends c4.89 + 0.6, the hand has stopped at c2.0), s32-t6 = t5 0-5.0 (a30 ends c4.07,
# she holds the sheet up from c2.5; the old s32 was 5.0 s, so murmur16 and the market cue keep their timing). Remade whenever
# the t5 is newer than the t6, so a later t5 never loses to a stale t6.
for st in s27:5.5 s32:5.0; do s=${st%%:*}; t=${st##*:}
  [ -f $C/$s-t6.mp4 ] && [ $C/$s-t6.mp4 -nt $C/$s-t5.mp4 ] || ffmpeg -v error -threads 2 -y -i $C/$s-t5.mp4 -t $t $ENC $C/$s-t6.mp4; done
# the episode sfx dir (second sfx_dirs entry), made if missing: murmur16 = crowd-murmur.py 16 30 (this episode's recordings
# reversed, -19 LUFS) under the school gate s29-s34; rooster916 = rooster-village-loop's first crow (2.1-4.2 s, e928's recipe)
# for s39 -> s40 (dawn); cart916 = ox-cart-01 2.4-5.4 s low-passed at 2.4 kHz and faded out from 0.5 s, the barrow rolling away
# at the start of s08.
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e916-dh/sfx; mkdir -p $S
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/murmur16.wav ] || python3 -I $Q/crowd-murmur.py 16 30
[ -f $S/rooster916.wav ] || ffmpeg -v error -y -ss 2.1 -t 2.1 -i $X/zhongtian-sfx-rooster-village-loop.wav -af "afade=t=in:d=0.05,afade=t=out:st=1.7:d=0.4,$AF" $S/rooster916.wav
[ -f $S/cart916.wav ] || ffmpeg -v error -y -ss 2.4 -t 3.0 -i $X/zhongtian-sfx-ox-cart-01.wav -af "lowpass=f=2400,afade=t=in:d=0.05,afade=t=out:st=0.5:d=2.5,$AF" $S/cart916.wav
# hoof916 = one hoof stamp out of the series hooves_trot (1.1-1.55 s, faded) for s35's parked carriage (no snort in either set)
[ -f $S/hoof916.wav ] || ffmpeg -v error -y -ss 1.1 -t 0.45 -i /root/mokaair-work/videos/_series/zhong-tian-qu-qi/sfx/hooves_trot.wav -af "afade=t=in:d=0.01,afade=t=out:st=0.3:d=0.15,$AF" $S/hoof916.wav
# REVIEW 3: s12 (the insert whose set reads as an outdoor deck) is deleted -- the assembler cuts every scene video.json lists,
# so the cut, audio-qa and the sheets read $VL, video.json without the scenes in DROP (s12 has no lines)
VL=$E/video-live.json; DROP="s12"
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# no vidstab: cut-qa's jitter() on every staged clip reads 0.00 (s02 0.02, s15 0.08), nothing hops frame to frame
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e016-r2/overlays.json $P/hailuo/edit-dh-e916-live.json $E $E/cut/e916-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e916-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3: attack 8 ms (with 5 ms
# the AAC overshot to -3.11 dBTP and loudnorm2 went dynamic; 8 ms held it to -3.84 dBTP, linear); kept since.
# END: s42 is Tang's recording a39 (ends c3.81); the picture fades over c4.20-4.75 (vf fade=t=out:st=4.200:d=0.55) and min 6.25
# (REVIEW 3; was 7.0) holds about 1.5 s of black, so the low accent laid at c3.95 (gong_02 + impactSoft_heavy_000) and the
# tension cue ring out in the dark. The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e916-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e916-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e916-live.lim.mp4 && mv $E/cut/e916-live.lim.mp4 $E/cut/e916-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e916-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e916-live.mp4
# POLISH+SWAP 2026-11-21: s01's take clips at 0 dBFS on a plosive (c3.05, Xu's voice); with the louder music the first
# limiter still lets it through and the AAC re-encode lands it at -0.1 dBTP. A second alimiter after loudnorm2 (0.7 = -3.1 dBFS,
# the e904 way) takes only that peak; the level stays -14.0 LUFS.
ffmpeg -v error -y -i $E/cut/e916-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=5:release=50:level=false,aresample=48000" $E/cut/e916-live.lim2.mp4 && mv $E/cut/e916-live.lim2.mp4 $E/cut/e916-live.mp4
# the delivery wants the true peak at or under -1 dBTP: print it (ebur128 true peak on the final file)
ffmpeg -hide_banner -nostats -i $E/cut/e916-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e916-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
