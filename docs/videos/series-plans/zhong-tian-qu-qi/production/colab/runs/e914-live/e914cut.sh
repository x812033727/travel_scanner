#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e914/zhong-tian-qu-qi-e914-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e014-r2/video.json
# POLISH+SWAP 2026-11-21: the 2026-11-15 cut files (lines.json, srt, final.log; its mp4 is review-zt/ep/e014/final.mp4) go to
# cut/old-1115 once and carry a .keep (never removed); a later run replaces its own previous cut (no old-HHMM).
mkdir -p $E/cut
[ -d $E/cut/old-1115 ] || { mkdir -p $E/cut/old-1115; mv $E/cut/e914-live.* $E/cut/final.log $E/cut/old-1115/ 2>/dev/null; touch $E/cut/old-1115/.keep; }
# SWAP wave 2 2026-11-22 (round4: s20 s27 s30 s32 s33): the wave-1 cut (223.31 s, made 2026-11-22, not delivered) goes to
# cut/old-w1 once and carries a .keep (never removed)
[ -d $E/cut/old-w1 ] || { mkdir -p $E/cut/old-w1; mv $E/cut/e914-live.* $E/cut/final.log $E/cut/old-w1/ 2>/dev/null; touch $E/cut/old-w1/.keep; }
# SWAP wave 3 2026-11-22 (round7: s12 = 9149702 t5, made 09:23): the wave-2 cut (223.63 s, delivered) goes to cut/old-w3 once
# and carries a .keep (never removed). s12 has no t6 (this script never trimmed one for it), so the new t5 is taken as it is.
[ -d $E/cut/old-w3 ] || { mkdir -p $E/cut/old-w3; mv $E/cut/e914-live.* $E/cut/final.log $E/cut/old-w3/ 2>/dev/null; touch $E/cut/old-w3/.keep; }
# GAP SFX 2026-11-22 (review-zt/GAP-BRIEF.md): the delivered wave-3 cut (223.13 s, review 45dc2535) goes to cut/old-gap once
# and carries a .keep (never removed)
[ -d $E/cut/old-gap ] || { mkdir -p $E/cut/old-gap; mv $E/cut/e914-live.* $E/cut/final.log $E/cut/old-gap/ 2>/dev/null; touch $E/cut/old-gap/.keep; }
rm -f $E/cut/e914-live.* $E/cut/final.log; rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 14: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 14"; exit 1; }
# e914 trims and seeds the edit table assumes (edit-dh-e914-live.json _note): picks.json as refine-prep.py 14 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv in that order -- the fix1 retakes s24 s30 s32 (9141201, no trim
# in fix1) trimmed there, s16 start 1.75 (the extra hand on the abacus, gone by 2.25), s29 start 0.875 (不是 at 1.00-1.30 was cut out by
# 2.625), s42 end 5.417 (the pick's suggested earlier end).
# REVIEW 3 (cut-review.md + cut-review-2.md, coordinator's picks): s05 start 2.25, s11 end 5.375, s14 end 6.5, s15 end 6.625,
# s16 start 2.0 (a16 at 1.2x), s17 end 4.125, s24 end 7.4, s42 start 1.5 with no end (a41 at 1.05x; Xu's hands off the notice).
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001 (e912 review 3: -ss keeps a
# frame at/after start, -to drops a frame whose end passes it); 0 = no end (the clip's end).
# Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.0,4.75),'s02':(0.875,6.375),'s03':(0.5,6.375),'s04':(0.75,6.5),'s05':(2.25,6.375),'s06':(1.5,7.875),'s07':(3.0,6.584),
 's08':(0.5,3.584),'s09':(0.5,6.125),'s10':(2.0,7.5),'s11':(0.625,5.375),'s12':(1.375,7.75),'s13':(0.75,6.125),'s14':(1.0,6.5),
 's15':(0.375,6.625),'s16':(2.0,6.584),'s17':(0.625,4.125),'s18':(0.625,6.625),'s19':(0.125,6.375),'s20':(0.25,5.875),
 's21':(0.75,5.375),'s22':(1.75,6.584),'s23':(0.125,5.25),'s24':(0.5,7.4),'s25':(1.5,6.125),'s26':(1.0,7.875),'s27':(1.0,7.584),
 's28':(1.875,6.375),'s29':(0.875,6.584),'s30':(0,5.5),'s31':(1.5,7.75),'s32':(0.75,0),'s33':(0.5,5.0),'s34':(1.0,4.5),
 's35':(2.5,6.584),'s36':(1.5,4.5),'s37':(0.375,7.875),'s38':(0.875,8.0),'s39':(1.0,8.0),'s40':(1.5,5.5),'s41':(1.5,6.25),
 's42':(1.5,0)}
seed={'s03':9141102,'s11':9141102,'s13':9141101,'s14':9141102,'s15':9141102,'s16':9141102,'s18':9141102,'s22':9141102,'s24':9141201,
 's29':9141102,'s30':9141201,'s31':9141102,'s32':9141201,'s35':9141102,'s37':9141102,'s38':9141102,'s40':9141102,'s41':9141101,'s42':9141102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9141101)' for s in p if s not in seed and p[s]['seed']!=9141101]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# SWAP wave 3 2026-11-22: s12 is the round7 retake clips/s12-t5.mp4 (fix-polish/round7/review-picks.tsv, 0.667-6.542, 5.875 s).
# SWAP wave 2 2026-11-22: s20 s27 s30 s32 s33 are the round4 retakes clips/sNN-t5.mp4 (fix-polish/round4/review-picks.tsv,
# already trimmed; no t6 for them).
# POLISH+SWAP 2026-11-21 (edit table _note). SWAP: s03 s11 s13 s37 s40 s42 are the fixp retakes clips/sNN-t5.mp4 (already
# trimmed, runpod/polish/picks.json; the assembler takes the highest take number); picks.json and the want table above still
# describe the t1 staging, which stays on disk. s40: clips/s40-t6.mp4 = s40-t5 0-4.5 s (frames 0-107; the take is a static 6.17 s
# and a39 + her breaths need 4.4 s), made if missing, t5 kept.
C=$E/clips; ENC="-c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000"
[ -f $C/s40-t6.mp4 ] || ffmpeg -v error -threads 2 -y -i $C/s40-t5.mp4 -t 4.5 $ENC $C/s40-t6.mp4
# the episode sfx dir (third sfx_dirs entry), made if missing (站主 2026-11-22: the nearest real recording where the libraries
# have none): bead914 = one bead click out of abacus-drop-01 (0.245-0.325 s, e911/e928's bead recipe) for the abacus in s16 s22 s24;
# thud914 = staff-thud-01 from 1.03 s, 0.4 s (e912's recipe) for Erniu's pestle in s15; drum914 = war-drum-01 0-0.6 s low-passed
# at 500 Hz, faded 0.3-0.6 s, for s01's watch drum (laid with impactSoft_heavy_000 in place of impactWood_heavy_001, same peak)
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e914-dh/sfx; mkdir -p $S
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/bead914.wav ] || ffmpeg -v error -y -ss 0.245 -t 0.08 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.003,afade=t=out:st=0.04:d=0.04,volume=14dB,$AF" $S/bead914.wav
[ -f $S/thud914.wav ] || ffmpeg -v error -y -ss 1.03 -t 0.4 -i $X/zhongtian-sfx-staff-thud-01.wav -af "afade=t=out:st=0.25:d=0.15,$AF" $S/thud914.wav
[ -f $S/drum914.wav ] || ffmpeg -v error -y -t 0.6 -i $X/zhongtian-sfx-war-drum-01.wav -af "lowpass=f=500,afade=t=out:st=0.3:d=0.3,$AF" $S/drum914.wav
# GAP SFX 2026-11-22 (gap-20261122, the owner's Pixabay additions to the set): bamboo914 = bamboo-leaves-loop (30.12 s) 0-29 s
# then 10-29.6 s through a 2 s equal-power crossfade (46.6 s, no hard loop seam over s01-s09's 45.17 s), highpass 250 Hz twice
# (the 20-55 Hz rumble read as 'Vehicle'), a slow 3:1 compressor for the 6-9 s gust (-26.7 LUFS, LRA 3.0), 0.5 s fade-in
[ -f $S/bamboo914.wav ] || ffmpeg -v error -y -i $X/zhongtian-sfx-bamboo-leaves-loop.wav -i $X/zhongtian-sfx-bamboo-leaves-loop.wav -filter_complex "[0:a]atrim=0:29,asetpts=PTS-STARTPTS[a];[1:a]atrim=10:29.6,asetpts=PTS-STARTPTS[b];[a][b]acrossfade=d=2:c1=qsin:c2=qsin,highpass=f=250:poles=2,highpass=f=250:poles=2,acompressor=threshold=0.03:ratio=3:attack=200:release=1500:makeup=1,afade=t=in:d=0.5,$AF" $S/bamboo914.wav
# no vidstab this time: cut-qa's jitter() on every staged clip reads 0.00-0.04 (s22 0.04), nothing hops frame to frame
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e014-r2/overlays.json $P/hailuo/edit-dh-e914-live.json $E $E/cut/e914-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e914-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3: attack 8 ms -- with 5 ms
# the e913 re-cut's AAC overshot to -3.11 dBTP and loudnorm2 went dynamic; 8 ms held it to -3.84 dBTP, linear; kept for e914
# END (REVIEW 3): s42 is a recorded-line shot (a41 at 1.05x laid at c0.05, Tang's back, last word ends c4.81); the picture fades
# over c4.84-5.44 (vf fade=t=out:st=4.840:d=0.6) and min 6.667 holds about 1.2 s of black after it, so the low accent laid at
# c4.85 (gong_02 + impactSoft_heavy_000) rings out (cut-review 2 medium 7: it had 0.58 s). The sound fades over the last 1.0 s.
# GAP SFX 2026-11-22: limit 0.6 -> 0.55 (-5.2 dBFS, e901-e906's value): with the bamboo bed the AAC overshot to -3.13 dBTP,
# loudnorm2 needed -2.05 > -2.2 and went dynamic (gain 0.5-6.8 dB per second on that run, kept in cut/old-gap1)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e914-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e914-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e914-live.lim.mp4 && mv $E/cut/e914-live.lim.mp4 $E/cut/e914-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e914-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e914-live.mp4
# POLISH+SWAP 2026-11-21 (e912 lesson): the true peak after loudnorm2; above -1.5 dBTP a second sample-peak limiter at 0.7 touches
# just those peaks; the delivery wants <= -1 dBTP: printed on the final file
TP=$(ffmpeg -hide_banner -nostats -i $E/cut/e914-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e914-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e914-live.lim.mp4 && mv $E/cut/e914-live.lim.mp4 $E/cut/e914-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -nostats -i $E/cut/e914-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e914-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
