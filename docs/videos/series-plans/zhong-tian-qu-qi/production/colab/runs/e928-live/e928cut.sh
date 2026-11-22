#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e928/zhong-tian-qu-qi-e928-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e028-r2/video.json
# POLISH+SWAP 2026-11-21: the 2026-11-17 cut files (lines.json, srt, final.log; the mp4 is review-zt/ep/e028/final.mp4) go to
# cut/old-1117 once and are kept for the backup; a later run of this script replaces its own previous cut (no old-HHMM).
mkdir -p $E/cut
[ -d $E/cut/old-1117 ] || { mkdir -p $E/cut/old-1117; mv $E/cut/e928-live.* $E/cut/final.log $E/cut/old-1117/ 2>/dev/null; }
rm -f $E/cut/e928-live.* $E/cut/final.log; rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 28 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 28 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e928-dh/audio and $E/music -> zhong-tian-qu-qi-e928-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e928, the e927 way). Every effect is in the series library except
# murmur928.wav (the square's crowd: twelve of this episode's recordings reversed and filtered, unintelligible;
# zhong-tian-qu-qi-e928-dh/sfx, the edit table's second sfx dir).
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 28 --draft-picture s07 || exit 1; }
# e928 trims and seeds the edit table assumes (edit-dh-e928-live.json _note): picks.json as refine-prep.py 28 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (run in colab/runs/e928-live: refine-prep.py 28 picks-merged.tsv
# fix1/review-picks.tsv review3-trims.tsv, then stage.py 28; fix1 replaced s03, s07 and s26). review3-trims.tsv (first cut):
# ends brought in where a laid recording left more than ~1 s of the shot without a line -- s02 4.500 -> 3.750, s07 6.584 -> 6.250,
# s14 5.000 -> 4.584, s15 8.000 -> 7.000, s16 5.250 -> 4.209, s24 5.500 -> 5.000, s26 4.500 -> 3.709, s32 6.584 -> 4.917 (s32's
# take is muted and a29 laid from its mouth). The post list's s08 4.625, s11 4.0, s12 0.875, s15b 4.0, s16 0.708, s28 1.125 were
# already in the picks. No crop in e928. REVIEW 3 (review3-plan.md; rows in review3-trims.tsv): s04 end 3.000 -> 2.000, s06 4.750 -> 4.000,
# s07 back to the d1 fallback 9281101 3.500 -> 6.584 (her face; fix1's knot was tied by a man's hands in Lai San's sleeves), s28 4.625 -> 3.875,
# s30 3.000 -> 2.250, s32 end back to 6.584 (a29 laid in four pieces on the mouth), s33 5.000 -> 4.000. s07's d1 take was never refined
# (the refine was of the fix1 pick, refined/s07.mp4 stays), so stage.py stages it with --draft-picture s07: the draft itself, lanczos to 1312x736.
# Whole frames: a start rounded DOWN and an end-before rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop).
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(2.041,6.584),'s02':(0.0,3.75),'s03':(0.0,2.25),'s03b':(0.0,3.0),'s04':(0.0,2.0),'s05':(1.583,6.584),'s06':(1.25,4.0),'s07':(3.5,6.584),'s08':(0.0,4.625),'s09':(0.0,5.0),'s10':(0.0,3.5),'s11':(0.0,4.0),'s12':(0.875,5.584),'s13':(0.75,6.584),'s14':(1.0,4.584),'s15':(0.0,7.0),'s15b':(0.0,4.0),'s16':(0.708,4.209),'s17':(0.25,5.667),'s18':(0.416,7.834),'s19':(0.541,6.5),'s20':(1.083,8.0),'s21':(0.0,5.5),'s22':(1.416,6.584),'s23':(0.25,6.584),'s24':(0.0,5.0),'s25':(0.458,6.5),'s26':(0.0,3.709),'s27':(0.75,5.5),'s28':(1.125,3.875),'s29':(0.625,6.584),'s30':(0.0,2.25),'s31':(0.75,6.584),'s32':(0.416,6.584),'s33':(0.0,4.0),'s34':(0.0,4.0),'s35':(1.25,8.0),'s36':(0.0,8.0),'s37':(0.0,2.5),'s38':(1.25,6.584),'s39':(0.0,4.0)}
seed={'s01':9281102,'s02':9281102,'s08':9281102,'s09':9281102,'s10':9281102,'s11':9281102,'s19':9281102,'s20':9281102,'s25':9281102,'s29':9281102,'s32':9281102,'s34':9281102,'s36':9281102,'s38':9281102,'s39':9281102,'s03':9281202,'s26':9281201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9281101)' for s in p if s not in seed and p[s]['seed']!=9281101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (want none)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-21 (edit table _note). SWAP: s03 s03b s18 s32 s38 are the fixp retakes clips/sNN-t5.mp4 (already trimmed,
# runpod/polish/picks.json; the assembler takes the highest take number). POLISH (free fix C): s33's empty-chair wide is
# replaced by the head of s39's own take before the crowd raises its hands (s39-t1 0-1.417, frames 0-33, Wei already seated) as
# clips/s33-t2.mp4, and s39 starts on the raised hands (clips/s39-t2.mp4 = s39-t1 from 1.417): made if missing, t1 kept.
C=$E/clips; ENC="-c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000"
[ -f $C/s33-t2.mp4 ] || ffmpeg -v error -threads 2 -y -i $C/s39-t1.mp4 -t 1.417 $ENC $C/s33-t2.mp4
[ -f $C/s39-t2.mp4 ] || ffmpeg -v error -threads 2 -y -ss 1.417 -i $C/s39-t1.mp4 $ENC $C/s39-t2.mp4
# the episode sfx dir (second sfx_dirs entry), made if missing: rooster928 = rooster-village-loop's first crow (2.1-4.2 s,
# fades) for s08's distant cock-crow; bead928 = one bead click out of abacus-drop-01 (0.245-0.325 s, e911's bead recipe) for
# s21's abacus; kneel928 = body-fall-stone-01 0.06-0.46 s (the first impact, fade 0.15) for s03b's knees; murmur928end2 /
# wind928end2 = murmur928end / wind928end from 1.417 s (s39 now starts 1.417 s later; their baked fades move with it), the
# wind faded in over 0.6 s again.
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e928-dh/sfx
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/rooster928.wav ] || ffmpeg -v error -y -ss 2.1 -t 2.1 -i $X/zhongtian-sfx-rooster-village-loop.wav -af "afade=t=in:d=0.05,afade=t=out:st=1.7:d=0.4,$AF" $S/rooster928.wav
[ -f $S/bead928.wav ] || ffmpeg -v error -y -ss 0.245 -t 0.08 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.003,afade=t=out:st=0.04:d=0.04,volume=14dB,$AF" $S/bead928.wav
[ -f $S/kneel928.wav ] || ffmpeg -v error -y -ss 0.06 -t 0.4 -i $X/zhongtian-sfx-body-fall-stone-01.wav -af "afade=t=out:st=0.25:d=0.15,$AF" $S/kneel928.wav
[ -f $S/murmur928end2.wav ] || ffmpeg -v error -y -ss 1.417 -i $S/murmur928end.wav -af "afade=t=in:d=0.05" $S/murmur928end2.wav
[ -f $S/wind928end2.wav ] || ffmpeg -v error -y -ss 1.417 -i $S/wind928end.wav -af "afade=t=in:d=0.6" $S/wind928end2.wav
# nothing is dropped in e928 (DROP empty; all 41 shots are cut in); $VL is video.json without the DROP shots.
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e028-r2/overlays.json $P/hailuo/edit-dh-e928-live.json $E $E/cut/e928-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e928-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6; the AAC encode after it
# overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms; e923 on: limit 0.55.
# END: s39 is the suspense tail (4 s of the crowd pointing at the stage): the low hit and gong_02 at c3.5, the picture fades out over
# c3.60-4.00 (vf); REVIEW 3: the crowd (murmur928end) and the wind (wind928end) fade over c3.6-4.1 so the gong rings out alone, and
# min 7.0 holds 3.0 s of black (gong_02 is down ~24 dB from its peak at c7.0); the sound fades over the last 1.0 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e928-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e928-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e928-live.lim.mp4 && mv $E/cut/e928-live.lim.mp4 $E/cut/e928-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e928-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e928-live.mp4
# the delivery wants the true peak at or under -1 dBTP: print it (ebur128 true peak on the final file)
ffmpeg -hide_banner -nostats -i $E/cut/e928-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | tee /dev/stderr | awk '/Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e928-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
