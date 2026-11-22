#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e912/zhong-tian-qu-qi-e912-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e012-r2/video.json
# POLISH 2026-11-21: at most one old cut is kept (the disk is short): an older cut/old-* goes before this one moves there.
# SWAP 2026-11-21: an old-* holding a .keep file is never removed (old-2107 = the cut before the polish, old-2116 = the
# POLISH cut before the swap; both kept for the backup); only the non-kept ones go
V=${V:-v1}; T=$(date +%H%M); mkdir -p $E/cut; [ -f $E/cut/e912-live.mp4 ] && { for d in $E/cut/old-*; do [ -f $d/.keep ] || rm -rf $d; done; mkdir -p $E/cut/old-$T; mv $E/cut/e912-live.* $E/cut/final.log $E/cut/old-$T/ 2>/dev/null; [ "${KEEP_OLD:-0}" = 1 ] && touch $E/cut/old-$T/.keep; }
# SWAP-2 2026-11-22: KEEP_OLD=1 marks the cut it moves aside with .keep (the delivered SWAP cut, old-HHMM, kept for the
# backup like old-2107 / old-2116). clips/s11-t5.mp4 is now round4's 9129402 3.875-8.0 (4.125 s, runpod/polish/picks.json,
# colab/runs/e912-live/fix-polish/round4/review-picks.tsv); no t6 exists for any e912 shot, so nothing to re-trim
# SWAP 2026-11-21: clips/s11 s17 s21 s22-t5.mp4 (runpod/polish/picks.json, already trimmed: s11 9129101 3.125-8.0,
# s17 9129102 2.5-8.0, s21 9129102 1.25-8.0, s22 9129101 1.75-10.083) win over the t1 files; picks.json and the want
# table below still describe the t1 staging, which stays on disk
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 12: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 12"; exit 1; }
# e912 trims and seeds the edit table assumes (edit-dh-e912-live.json _note): review2-trims.tsv (pick-review + the whisper
# pass: s02 -> 9121202 start 2.0, s26 -> 9121201, s04 2.4583 keeps 好, lines no longer cut in s01 s11 s13 s20 s21 s23 s25 s27,
# s12's invented 了 dropped) and review3-trims.tsv (whole frames; the cut reviews' REVIEW 3: s22 fix2 9121301 start 1.75, s26 end 7.5,
# s33 end 9.0, s35 start 1.5 to the clip's end so the gong rings out with no hold). Tolerance 0.001 so
# review3-trims.tsv's 3-decimal values also pass: a start must be frame/24 rounded DOWN and an end-before rounded UP (input -ss
# keeps frames at/after start, -to drops a frame whose end passes it; 6.3333 < 152/24 lost s01's last frame in the dry run and
# assemble-v4 held it). Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0,6.3333),'s02':(2.0,0),'s03':(2.7917,5.8333),'s04':(2.4583,0),'s05':(0.25,6.5),'s06':(1.5833,7.4167),'s07':(1.5,6.0),
 's08':(2.375,0),'s09':(0.875,4.2083),'s10':(1.5,5.0),'s11':(2.5833,0),'s12':(2.2917,6.5),'s13':(1.375,7.75),'s14':(2.0,5.9167),
 's15':(1.0,4.2083),'s16':(0.375,5.625),'s17':(0.2917,4.8333),'s18':(1.5,4.5),'s19':(1.0833,5.8333),'s20':(0.875,6.0833),'s21':(1.2083,0),
 's22':(1.75,0),'s23':(1.1667,7.8333),'s24':(0,5.5),'s25':(0.75,4.9167),'s26':(0,7.5),'s27':(1.0,7.7083),'s28':(1.0,6.0),'s29':(1.0,6.125),
 's30':(0.2917,7.0),'s31':(0.5,3.4167),'s32':(0.5,4.4167),'s33':(0,9.0),'s34':(1.25,6.25),'s35':(1.5,0)}
seed={'s02':9121202,'s22':9121301,'s26':9121201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH 2026-11-21 (review-zt free fixes; edit table _note POLISH): the episode sfx dir (third sfx_dirs entry):
# murmur12.wav (crowd-murmur.py 12 30, the owner's reversed-recordings crowd, -19 LUFS) under s08-s13 for the constables
# round the yard; thud912.wav = zhongtian-sfx-staff-thud-01 from 1.03 s, 0.4 s (e906's hoe906 cut) for Qin's stick block in
# s13. The recordings a13 (rubberband 0.75) and a29 (0.72) are re-made from audio/orig/ (the 11-15 versions in audio/pre-polish/).
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e912-dh/sfx; mkdir -p $S
[ -f $S/murmur12.wav ] || python3 -I $Q/crowd-murmur.py 12 30
[ -f $S/thud912.wav ] || ffmpeg -v error -y -ss 1.03 -t 0.4 -i $X/zhongtian-sfx-staff-thud-01.wav -af "afade=t=out:st=0.25:d=0.15,aresample=48000,aformat=channel_layouts=stereo" $S/thud912.wav
# gong912 / bell912 = gong_01 / impactBell_heavy_001 0-0.55 s, linear fade-out 0.15-0.5 s: s23's releasing hit after
# 不查了 no longer rings over 今晚的事 (review e012 item 2: the long ring at -11..-15 dBFS buried it)
D=/root/mokaair-work/videos/_series/zhong-tian-qu-qi/sfx
[ -f $S/gong912.wav ] || ffmpeg -v error -y -t 0.55 -i $D/gong_01.wav -af "afade=t=out:st=0.15:d=0.35,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=0.55" $S/gong912.wav
[ -f $S/bell912.wav ] || ffmpeg -v error -y -t 0.55 -i $D/impactBell_heavy_001.wav -af "afade=t=out:st=0.15:d=0.35,aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=0.55" $S/bell912.wav
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e012-r2/overlays.json $P/hailuo/edit-dh-e912-live.json $E $E/cut/e912-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e912-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (the e908 cut review found a click from its dynamic fallback;
# e909 review 3: at -4 dBFS the true peak -3.58 plus the +1.43 dB gain overshot TP -2.2 by 0.05 and loudnorm went dynamic;
# e910 review 3: with louder accents and beds the same limiter left a true peak of -2.39 (input -15.25 LUFS, +1.25 dB to go),
# loudnorm2 went dynamic and the cut clicked to +3.6 dBFS at 3.8 s. The overshoot is made by the AAC encode after the limiter
# (the limited PCM measures -4.3 dBTP): attack 2 ms -> -2.3, 0.5 ms -> -1.8, 5 ms -> -4.2 on the s01 footsteps, so the attack
# is 5 ms (limit still 0.6 = -4.4 dBFS; 0.5 lost 0.7 LU and stayed at -2.9 dBTP))
# REVIEW 3 (cut review 1, medium 6): the last 1.0 s fades out so the s35 gong, still ringing under the picture fade, ends
# on silence instead of a cut (the fade is before loudnorm2, whose gain is linear)
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e912-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e912-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=5:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e912-live.lim.mp4 && mv $E/cut/e912-live.lim.mp4 $E/cut/e912-live.mp4
ffmpeg -hide_banner -i $E/cut/e912-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e912-live.mp4
# POLISH 2026-11-21 (e904/e908 lesson): loudnorm's first pass can miss an early transient, so the true peak is measured
# after loudnorm2 and, only if it is above -1.5 dBTP, a second sample-peak limiter at 0.7 (-3.1 dBFS) touches just those peaks
TP=$(ffmpeg -hide_banner -i $E/cut/e912-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e912-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e912-live.lim.mp4 && mv $E/cut/e912-live.lim.mp4 $E/cut/e912-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -i $E/cut/e912-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):' | tail -2
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e912-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
