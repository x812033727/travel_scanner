#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e923/zhong-tian-qu-qi-e923-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e023-r2/video.json
# POLISH+SWAP 2026-11-21/22: the 2026-11-17 cut files (lines.json, srt, final.log; its mp4 is review-zt/ep/e023/final.mp4) go to
# cut/old-1117 once and carry a .keep (never removed); a later run replaces its own previous cut (no old-HHMM).
mkdir -p $E/cut
[ -d $E/cut/old-1117 ] || { mkdir -p $E/cut/old-1117; mv $E/cut/e923-live.* $E/cut/final.log $E/cut/old-1117/ 2>/dev/null; touch $E/cut/old-1117/.keep; }
# SWAP 2026-11-22 (wave 2: s27 s28 s40 round5/round6): the POLISH+SWAP wave-1 cut (203.67 s) goes to cut/old-w1 once (.keep)
[ -d $E/cut/old-w1 ] || { mkdir -p $E/cut/old-w1; mv $E/cut/e923-live.* $E/cut/final.log $E/cut/old-w1/ 2>/dev/null; touch $E/cut/old-w1/.keep; }
rm -f $E/cut/e923-live.* $E/cut/final.log; rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 23; the refine sources are not on this machine, so the script
# no longer re-stages by itself -- it stops and says so)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 23"; exit 1; }
# e923 trims and seeds the edit table assumes (edit-dh-e923-live.json _note): picks.json as refine-prep.py 23 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e923-live: refine-prep.py 23
# picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 23) -- the fix1 retakes s17 (9231202), s31
# (9231201) and s38 (9231201); review3-trims.tsv (first cut) shortens the silent tails of s10 s13 s17 s19 s20 s21 s35;
# REVIEW 3 (review3-plan.md) re-trims s07 (start 2.25), s27 (end 4.709) and s29 (end 4.292). Whole frames: a start rounded DOWN
# and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.833,6.584),'s02':(0.5,2.959),'s03':(0,4.417),'s04':(0.5,3),'s05':(1,6.584),'s06':(2,4.459),'s07':(2.25,6.584),'s08':(1.833,6.584),'s09':(0.708,6.584),'s10':(0,4.042),'s11':(0,2.5),'s12':(1.208,6.584),'s13':(0,5.875),'s13b':(0,4.5),'s14':(0,5.584),'s15':(0,4.5),'s16':(0.958,6.584),'s17':(0.5,5.292),'s18':(0,4.417),'s19':(0.5,6),'s20':(0,6.5),'s21':(0,6),'s22':(0,5),'s23':(1.083,6.584),'s24':(0,4.459),'s25':(0,5.792),'s26':(1.625,6.584),'s27':(0,4.709),'s28':(0,6.584),'s29':(0,4.292),'s30':(1.625,6.584),'s31':(1,6.584),'s32':(1,6.584),'s33':(0,3.709),'s34':(0.875,6.584),'s35':(0.25,4.709),'s36':(0,6),'s37':(0,6.584),'s38':(0,6.584),'s39':(0.75,3.25),'s40':(0,8)}
seed={'s01':9231102,'s09':9231102,'s10':9231102,'s13':9231102,'s16':9231102,'s17':9231202,'s18':9231102,'s19':9231102,'s20':9231102,'s23':9231102,'s24':9231102,'s31':9231201,'s33':9231102,'s34':9231102,'s38':9231201,'s40':9231102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9231101)' for s in p if s not in seed and p[s]['seed']!=9231101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-21/22 (edit table _note). SWAP: clips/sNN-t5.mp4 (runpod/polish/picks.json, already trimmed; wave 1
# fix-polish/review-picks.tsv: s06 9239101 0.5-4.167 (used whole, 3.67 s: the pull over the gunwale is c1.75-3.5), s33 9239101
# 0.5-4.75, s37 9239102 0.333-6.583; wave 2 fix-polish/round4/review-picks.tsv: s23 9239401 0.625-6.125, s31 9239401 0-5.75;
# round5: s27 9239502 0.5-5.25, s40 9239502 0-8.0 (no crop any more); round6: s28 9239602 0.791-6.583) win
# over t1; picks.json and the want table above describe the t1 staging. No t2/t6 is cut from any clip of this episode.
# The episode sfx dir (third sfx_dirs entry) holds two sounds cut from the real set's abacus-drop-01 (prayer beads, the set has
# no abacus; e902/e906 way): bead923.wav = one bead click 0.245-0.325 s +14 dB; abacus923.wav = the rattle 0.15-1.35 s.
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e923-dh/sfx; mkdir -p $S
[ -f $S/bead923.wav ] || ffmpeg -v error -y -ss 0.245 -t 0.08 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.003,afade=t=out:st=0.04:d=0.04,volume=14dB,aresample=48000,aformat=channel_layouts=stereo" $S/bead923.wav
[ -f $S/abacus923.wav ] || ffmpeg -v error -y -ss 0.15 -t 1.2 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.02,afade=t=out:st=0.9:d=0.3,aresample=48000,aformat=channel_layouts=stereo" $S/abacus923.wav
# REVIEW 3 drops s04 (both cut reviews: Tang is missing under the awning; no line; its splash_01 is out of the edit table).
# picks.json and the want table keep s04 (staged, just not cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP="s04"
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e023-r2/overlays.json $P/hailuo/edit-dh-e923-live.json $E $E/cut/e923-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e923-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# e923: limit 0.55 (-5.2 dBFS): at 0.6 the fourth run's AAC encode came back at 0.01 dBTP (s05's clip voice at 14.3 s, s28,
# s36 at 0.86 sample peak) and loudnorm2 went dynamic; s05's clip voice also gets clip_af alimiter 0.89.
# POLISH 2026-11-21: s40 crop 1.15x (the self-appearing red blot out), panel off at c6.0, picture fade c6.0-8.0, min 10.0 -> 9.6
# (black ~1.6 s; the gong at c5.6 has rung ~2.5 s when the 1.5 s sound fade starts). Old note:
# END: s40 is the inn wide shot after the thumbprint; the system pair a37+a38 (panel only, red frame) ends at c5.30, a low
# hit and the gong at c5.60, the picture fades over c6.00-6.60 (vf) and min 10.00 holds ~3.4 s of black so the gong rings
# out (REVIEW 3: 9.00 -> 10.00, the 1.5 s sound fade now starts ~2.9 s after the gong at ~-30 dB; the take ends at c8.00). The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e923-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e923-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e923-live.lim.mp4 && mv $E/cut/e923-live.lim.mp4 $E/cut/e923-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e923-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e923-live.mp4
# POLISH+SWAP 2026-11-21 (e912 lesson): the true peak after loudnorm2; above -1.5 dBTP a second sample-peak limiter at 0.7 touches
# just those peaks; the delivery wants <= -1 dBTP: printed on the final file
TP=$(ffmpeg -hide_banner -nostats -i $E/cut/e923-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e923-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e923-live.lim.mp4 && mv $E/cut/e923-live.lim.mp4 $E/cut/e923-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -nostats -i $E/cut/e923-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e923-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
