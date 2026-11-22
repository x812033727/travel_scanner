#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e913/zhong-tian-qu-qi-e913-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e013-r2/video.json
# POLISH+SWAP 2026-11-21: at most one old cut is kept (the disk is short): an older cut/old-* goes before this one moves
# there, except an old-* holding a .keep file (a cut kept for the backup), which is never removed
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e913-live.mp4 ] && { for d in $E/cut/old-*; do [ -f $d/.keep ] || rm -rf $d; done; mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e913-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
# POLISH+SWAP 2026-11-21: clips/s08 s14 s16 s20 s28-t5.mp4 (runpod/polish/picks.json, already trimmed: s08 9139101
# 1.791-6.583, s14 9139101 0.125-3.125, s16 9139102 3.416-8.0, s20 9139102 1.75-7.0, s28 9139101 1.166-8.0) win over the
# t1 files; picks.json and the want table below still describe the t1 staging, which stays on disk
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 13: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 13"; exit 1; }
# e913 trims and seeds the edit table assumes (edit-dh-e913-live.json _note): picks.json as changed by review2-trims.tsv
# (s01 start 2.25 -- the draft voice starts at 2.25, 馬 --; s17 and s42 to the clip's end) and the edit table's review3 trims
# (s22 start 0.708 and s27 start 0.458: their first syllable starts at 0.75 / 0.50, so 0.75 / 0.5 began on it; s13 7.5 kept).
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001 (e912 review 3: -ss keeps a
# frame at/after start, -to drops a frame whose end passes it); 0 = no end (the clip's end).
# REVIEW 3 (after cut-review.md and cut-review-2.md; review3-trims.tsv): s24 start 0.75 (一成先不說 back in), the fix3 takes
# trimmed -- s06 end 8.5, s11 start 1.0, s40 end 2.5, s41 end 1.75 -- and their seeds checked like the others.
# Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(2.25,6.5),'s02':(3.0,8.0),'s03':(0.5,6.5),'s04':(3.5,8.0),'s05':(1.0,5.5),'s07':(0,4.5),'s08':(0.25,5.25),'s09':(0.5,6.5),
 's10':(0.5,5.5),'s12':(3.5,8.0),'s13':(2.5,7.5),'s14':(0.25,3.25),'s15':(0,6.5),'s16':(2.375,8.0),'s17':(2.75,0),'s18':(0,8.0),
 's19':(0.5,4.5),'s20':(3.0,7.625),'s21':(2.5,7.25),'s22':(0.708,5.75),'s23':(3.0,8.0),'s24':(0.75,8.0),'s25':(0,5.0),'s26':(4.0,8.0),
 's27':(0.458,5.25),'s28':(1.5,8.0),'s29':(0.5,5.5),'s30':(1.25,5.125),'s31':(0.25,6.25),'s32':(3.25,8.0),'s33':(0.5,5.5),'s34':(1.5,8.0),
 's35':(0,4.5),'s36':(0.5,5.0),'s37':(0.5,5.5),'s38':(0.75,5.75),'s39':(1.75,4.75),'s42':(1.5,0),
 's06':(0,8.5),'s11':(1.0,0),'s40':(0,2.5),'s41':(0,1.75)}
seed={'s05':9131201,'s08':9131201,'s15':9131201,'s22':9131201,'s27':9131201,'s29':9131201,'s35':9131301,'s37':9131301,'s38':9131302,'s42':9131302,'s06':9131401,'s11':9131402,'s40':9131401,'s41':9131402}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# s26 (the overhead drawing insert) jitters frame to frame (cut-qa jitter 0.43 on the draft): the edit table's vf runs
# vidstabtransform on this file, so detect on the staged clip exactly as assemble-v4 feeds it (1920x1080, 24 fps)
# (pick-review: shakiness 8, accuracy 15; on the draft jitter 0.43 -> 0.05). REVIEW 3: the edit table smooths with 4, not 12
# (12 swung the board about 15 px left and right at c2.2-2.8, the hand read as camera motion; 4 holds it to 2-3 px)
ffmpeg -v error -y -i $E/clips/s26-t1.mp4 -vf "scale=1920:1080:flags=lanczos,fps=24,format=yuv420p,vidstabdetect=shakiness=8:accuracy=15:result=$E/s26.trf" -f null - || exit 1
# POLISH+SWAP round 2 (2026-11-22): the episode sfx dir (third sfx_dirs entry): bead913 = one bead click out of the real
# set's abacus-drop-01 (0.245-0.325 s, e911's bead911 recipe) for s09's abacus (was wooden_01, a wood knock)
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e913-dh/sfx; mkdir -p $S
[ -f $S/bead913.wav ] || ffmpeg -v error -y -ss 0.245 -t 0.08 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.003,afade=t=out:st=0.04:d=0.04,volume=14dB,aresample=48000,aformat=channel_layouts=stereo" $S/bead913.wav || exit 1
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e013-r2/overlays.json $P/hailuo/edit-dh-e913-live.json $E $E/cut/e913-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e913-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). REVIEW 3: attack 8 ms -- with 5 ms the
# re-cut's AAC overshot to -3.11 dBTP at 0.64 (an onset in s01's line), -15.36 LUFS + 1.36 dB -> -1.75 > -2.2 and
# loudnorm2 went dynamic (gain spread 6 dB); 8 ms: -3.84 dBTP, -15.36 LUFS -> -2.48, linear
# END: s42 is a clip-voiced shot (never slowed or held), her last word ends at c4.28 and the clip at c5.083, so the last
# 0.6 s fades out with the picture fade in its vf (fade=t=out:st=4.483:d=0.6); a 1.0 s fade as e912 would start on 裡
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e913-live.mp4); FS=$(python3 -c "print(f'{$D-0.6:.3f}')")
ffmpeg -v error -y -i $E/cut/e913-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=0.6" $E/cut/e913-live.lim.mp4 && mv $E/cut/e913-live.lim.mp4 $E/cut/e913-live.mp4
ffmpeg -hide_banner -i $E/cut/e913-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e913-live.mp4
# POLISH+SWAP 2026-11-21 (e904/e908/e912): the true peak is measured after loudnorm2 and, only if it is above -1.5 dBTP,
# a second sample-peak limiter at 0.7 (-3.1 dBFS) touches just those peaks (the upload wants it under -1 dBTP)
TP=$(ffmpeg -hide_banner -i $E/cut/e913-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e913-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e913-live.lim.mp4 && mv $E/cut/e913-live.lim.mp4 $E/cut/e913-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -i $E/cut/e913-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):' | tail -2
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e913-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
