#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e929/zhong-tian-qu-qi-e929-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e029-r2/video.json
# POLISH+SWAP 2026-11-22: the 2026-11-17 cut files (lines.json, srt, final.log; its mp4 is review-zt/ep/e029/final.mp4, the
# restore had no cut mp4 here) go to cut/old-1117 once and carry a .keep (never removed); a later run replaces its own cut.
mkdir -p $E/cut
[ -d $E/cut/old-1117 ] || { mkdir -p $E/cut/old-1117; mv $E/cut/e929-live.* $E/cut/final.log $E/cut/old-1117/ 2>/dev/null; touch $E/cut/old-1117/.keep; }
# SWAP wave 3 2026-11-22: the delivered POLISH+SWAP cut (07:02, 171.38 s) goes to cut/old-w2 once, with a .keep
[ -d $E/cut/old-w2 ] || { mkdir -p $E/cut/old-w2; mv $E/cut/e929-live.* $E/cut/final.log $E/cut/old-w2/ 2>/dev/null; touch $E/cut/old-w2/.keep; }
rm -f $E/cut/e929-live.* $E/cut/final.log; rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 29 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 29 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e929-dh/audio and $E/music -> zhong-tian-qu-qi-e929-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e929, the e927/e928 way). stage.py also applies s10's crop=870:493:45:25
# (fix1: the paper fills every frame from the crop on). Every effect is in the series library except murmur929.wav (the
# square's crowd: twelve of this episode's recordings reversed and filtered, unintelligible; zhong-tian-qu-qi-e929-dh/sfx,
# the edit table's second sfx dir; REVIEW 3 adds hooves929.wav there: hooves_trot 0-3.959 s, -24 dB rising to -16 by 1.7 s, faded
# out over the last 0.6 s, laid at s31 c3.3 to s32 c0.8). s31's vf reads the refined s32 picture directly (runpod/a/st2/refined/s32.mp4).
# POLISH+SWAP 2026-11-22: the refine sources (runpod/a/st2) are not on this machine, so the script no longer re-stages by
# itself -- it stops and says so (the e926 way)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 29"; exit 1; }
# e929 trims and seeds the edit table assumes (edit-dh-e929-live.json _note): picks.json as refine-prep.py 29 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e929-live: refine-prep.py 29 picks-merged.tsv
# fix1/review-picks.tsv review3-trims.tsv, then stage.py 29; fix1 replaced s10 and s11, the two paper inserts). review3-trims.tsv
# (first cut): s28 5.167 -> 4.584 and s29 7.000 -> 6.500 (a laid recording left more than ~1 s of the shot without a line),
# s34 4.584 -> 4.250 (the take's 囡囡 ends at c1.88; the take stays: a31 lowered 4-5 semitones was heard as 媽媽);
# s32 2.000-4.500 -> 3.458-4.708 (s31's vf lays the refined s32 at draft 2.000-3.458 over s31 from c5.000, where Wei turns to
# the lens, while his take's line runs on; s32 then plays on from frame 83). Only s10 carries a crop (fix1).
# REVIEW 3 (review3-plan.md; rows in review3-trims.tsv): s03 start 0.750 -> 0.000 (both reviews: the bite into the cake is
# frames 0-3 of the refine; the take is silent to 1.70), s02 4.500 -> 4.250, s04 5.750 -> 5.292, s05 3.000 -> 2.500,
# s12 start 2.750 -> 3.000 (review 2: no take word in any cut-away span, every take there under -40 dB).
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop).
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(2.458,6.417),'s02':(0.0,4.25),'s03':(0.0,6.417),'s04':(0.25,5.292),'s05':(0.0,2.5),'s06':(1.875,7.792),'s07':(0.375,6.584),'s08':(1.791,5.875),'s09':(0.0,2.5),'s10':(1.708,6.584),'s11':(1.666,6.0),'s12':(3.0,5.25),'s13':(1.375,6.334),'s14':(0.25,5.0),'s15':(0.0,5.167),'s16':(0.5,5.0),'s17':(1.25,6.584),'s18':(0.625,6.584),'s19':(0.375,6.292),'s20':(0.375,6.417),'s21':(1.25,6.584),'s22':(1.75,6.584),'s23':(0.708,6.417),'s24':(0.0,4.75),'s25':(0.333,7.875),'s26':(0.0,5.0),'s27':(0.0,4.5),'s28':(0.0,4.584),'s29':(0.0,6.5),'s30':(0.0,5.5),'s31':(1.25,7.709),'s32':(3.458,4.708),'s33':(0.5,4.5),'s34':(1.5,4.25),'s35':(2.0,6.667)}
seed={'s01':9291102,'s03':9291102,'s09':9291102,'s10':9291201,'s11':9291201,'s19':9291102,'s20':9291102,'s26':9291102,'s30':9291102,'s32':9291102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9291101)' for s in p if s not in seed and p[s]['seed']!=9291101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (only s10 may)' for s in p if p[s].get('crop') and s!='s10']
bad+=[f's10 crop {p[\"s10\"].get(\"crop\")} (want 870:493:45:25)' for _ in [0] if 's10' in p and p['s10'].get('crop')!='870:493:45:25']
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-22 (edit table _note). SWAP: clips/sNN-t5.mp4 (runpod/polish/picks.json, already trimmed; wave 1
# fix-polish/review-picks.tsv: s07 9299102 whole, s11 9299102 0-4.458, s21 9299101 whole, s33 9299102 whole; round2: s26
# 9299202 0-4.75; wave 2 round4: s10 9299401 from 1.0) win over t1; picks.json and the want table above describe the t1
# staging. Clips cut here (the assembler takes the highest take number and has no per-shot trim; each remade when missing or
# older than its t5 -- delete one to re-cut):
#  s10-t6 = t5 from 1.5 (draft 2.5, POST-SWAP: the first 2.5 s of the draft read as a sticker on the paper; 97 frames);
#  s33-t6 = t5 0-4.0 (the ledger slips c0.5-1.75 and is clamped by c2.0; a30 c0.3-3.12; the old shot's 4.0 s, 96 frames).
C=$E/clips; X264="-c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k"
cutclip() { [ -f $C/$1-t6.mp4 ] && [ $C/$1-t6.mp4 -nt $C/$1-$2.mp4 ] || ffmpeg -v error -y -ss $3 -i $C/$1-$2.mp4 -t $4 -frames:v $(python3 -c "print(round($4*24))") $X264 $C/$1-t6.mp4; }
cutclip s10 t5 1.5 4.042; cutclip s33 t5 0 4.0
# SWAP wave 3 2026-11-22 (round5/review-picks.tsv): s27 9299501 0-4.583, s30 9299502 0-5.5, s35 9299502 1.0-8.0 are
# clips/sNN-t5.mp4 as staged, whole -- no t6 for them (this script never cut one), so the assembler takes the t5.
# s27's handoff sound: one crinkle of the real-set paper packet (zhongtian-sfx-paper-packet-01 5.30-5.66 s, crinkle
# 0.04-0.28 s in, a tick at 0.28) into zhong-tian-qu-qi-e929-dh/sfx/packet929.wav; made when missing.
PK=/root/mokaair-work/videos/zhong-tian-qu-qi-e929-dh/sfx/packet929.wav
[ -f $PK ] || ffmpeg -v error -y -ss 5.30 -t 0.36 -i /root/mokaair-work/videos/_sfx/zhongtian-real-20261121/zhongtian-sfx-paper-packet-01.wav -af "afade=t=in:d=0.03,afade=t=out:st=0.30:d=0.06" -ar 48000 $PK
# s31's cover (the bow of s32, refined draft 2.000-3.458) was read from runpod/a/st2/refined/s32.mp4, which is not on this
# machine. It is taken back from the published cut (ep/e029/final.mp4 154.000-155.458, 35 frames: s31 starts at 149.000 and
# the cover at its c5.000) with the dh grade and the vignette undone (vignette mode=backward, then gamma, then contrast and
# saturation inverted), so the assembler's grade and vignette give the published picture again; the warm colorbalance is
# already in it, so s31's vf no longer adds it.
CV=$E/runpod/s32-cover-from-final.mp4
[ -f $CV ] || ffmpeg -v error -y -ss 154.000 -i /root/mokaair-work/review-zt/ep/e029/final.mp4 -an -frames:v 35 -vf "vignette=angle=PI/5:mode=backward,eq=gamma=1.020408,eq=contrast=0.952381:saturation=1.086957,format=yuv420p" -c:v libx264 -crf 12 -preset slow -pix_fmt yuv420p $CV
# nothing is dropped in e929 (DROP empty; all 35 shots are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# REVIEW 3 (review 2 medium 2): s29's first panel row 鬥商總帳：許記三百三十兩，魏記一百六十五兩 (21 characters at 52 px, ~1090 px)
# ran past panelFilters()' fixed 1000 px box. $OV is overlays.json with that row split in two at the colon, words unchanged
# (鬥商總帳 / 許記三百三十兩，魏記一百六十五兩 at ~830 px / 任務完成): three rows, 262 px tall, panel_y 700 -> bottom edge 962.
# overlays.json is r2.py's and the animated cut's, so the live cut reads the split copy; panelFilters() is not changed. The
# assembler draws a panel's rows together (0.1 s apart from panel_from), so 任務完成 comes in with the rest (accepted).
OV=$E/overlays-live.json
python3 -c "
import json;o=json.load(open('$R/docs/videos/zhong-tian-qu-qi-e029-r2/overlays.json'));r=o['s29']
assert r[0]['text']=='鬥商總帳：許記三百三十兩，魏記一百六十五兩' and r[1]['text']=='任務完成', r
o['s29']=[{'text':'鬥商總帳','kind':'task'},{'text':'許記三百三十兩，魏記一百六十五兩','kind':'task'},r[1]]
json.dump(o,open('$OV','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $OV $P/hailuo/edit-dh-e929-live.json $E $E/cut/e929-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e929-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END: s35 is the suspense tail (Tang Xiaotang behind Xu Yan, a32 ends ~c3.5, he turns his head): the low hit and gong_02 at
# c3.6, the picture fades out over c4.267-4.667 (vf) and min holds black while the gong rings out; the sound fades over the
# last 1.0 s. REVIEW 3: min 8.1 -> 7.1 (2.43 s of black; the gong, 4.5 s long, is faded over c6.1-7.1, 2.5-3.5 s into its ring).
# SWAP wave 3: the new s35 is 7.0 s and plays whole at 1x (slow_shot 1.0), fades over c6.6-7.0, min 9.417 keeps the same
# 2.417 s of black; the hit, gong and cliffhanger stay at c3.6 (a32 ends c3.49); the gong rings out by c8.1, inside the black.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e929-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e929-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e929-live.lim.mp4 && mv $E/cut/e929-live.lim.mp4 $E/cut/e929-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e929-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e929-live.mp4
# POLISH+SWAP 2026-11-22 (e912/e923 lesson): the true peak after loudnorm2; above -1.5 dBTP a second sample-peak limiter at 0.7
TP=$(ffmpeg -hide_banner -nostats -i $E/cut/e929-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e929-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e929-live.lim.mp4 && mv $E/cut/e929-live.lim.mp4 $E/cut/e929-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -nostats -i $E/cut/e929-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e929-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
