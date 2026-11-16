#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e917/zhong-tian-qu-qi-e917-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e017-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e917-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e917-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 17 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 17 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e917-dh/audio and $E/music -> zhong-tian-qu-qi-e917-dh/music, which is itself a link to
# _series/zhong-tian-qu-qi/music (made by hand for e917, the e916 way)
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 17 || exit 1; }
# e917 trims and seeds the edit table assumes (edit-dh-e917-live.json _note): picks.json as refine-prep.py 17 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and fix2/review-picks.tsv in that order (run in colab/runs/e917-live) -- the fix1
# retakes s17 s21 (9171202) and the fix2 retake s13 (9171301, A-ling's loose hair; the earlier refine is kept as
# runpod/a/st2/refined/s13-9171202.mp4). No review3-trims.tsv in the first cut: every clip-voiced staged clip was checked
# with faster-whisper and 50 ms RMS at both ends (heads -43..-74 dB, no word cut). If one is added later, re-run
# refine-prep.py 17 ... review3-trims.tsv and stage.py 17 and update the want table. Whole frames: a start rounded DOWN and an
# end-before rounded UP to 3 decimals, tolerance 0.001 (e912 review 3: -ss keeps a frame at/after start, -to drops a frame
# whose end passes it); 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.75,4.5),'s02':(0,5.917),'s03':(0.75,5),'s04':(0.75,5),'s05':(0.375,8),'s06':(0.5,4.5),'s07':(0,5.75),
 's08':(1.25,7.5),'s09':(0.5,5.5),'s10':(0.5,4.5),'s11':(0,5),'s12':(0.75,6.584),'s13':(0.75,5.625),'s14':(0,3.5),
 's15':(0.5,5.5),'s16':(0,6.584),'s17':(0,6.584),'s18':(0.25,6.584),'s19':(0.375,6.25),'s20':(0,6.584),'s21':(0,4.5),
 's22':(0,6),'s23':(0.75,5.5),'s24':(0,4.5),'s25':(0,7.625),'s26':(0.25,8),'s27':(0,5.75),'s28':(0,7.5),'s29':(0,6.584),
 's30':(0.5,6.584),'s31':(0.5,5.25),'s32':(0.375,6.584),'s33':(2.75,6.584),'s34':(0.5,6.334),'s35':(0,8),'s36':(0,6.584),
 's37':(0,6.584),'s38':(0,4.5),'s39':(0,10.125),'s40':(0.25,6.584)}
seed={'s02':9171102,'s03':9171102,'s11':9171102,'s13':9171301,'s14':9171102,'s16':9171102,'s17':9171202,'s18':9171102,
 's19':9171102,'s20':9171102,'s21':9171202,'s22':9171102,'s23':9171102,'s24':9171102,'s27':9171102,'s29':9171102,
 's32':9171102,'s36':9171102,'s38':9171102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9171101)' for s in p if s not in seed and p[s]['seed']!=9171101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# no shot is deleted (the e916 video-live.json step is not needed): the cut, audio-qa and the sheets read video.json itself
# no vidstab: cut-qa's jitter() on every staged clip reads 0.00 (s11 0.07, s12 0.03, s29 0.01), nothing hops frame to frame
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e017-r2/overlays.json $P/hailuo/edit-dh-e917-live.json $E $E/cut/e917-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e917-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# END: s40 is Xu's inner line a40 (a recording); the picture fades over c4.50-5.05 (vf fade=t=out:st=4.500:d=0.55) and min
# 6.55 holds about 1.5 s of black, so the gong laid at c4.25 (gong_02 + impactSoft_heavy_000) and the tension cue ring out
# in the dark. The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e917-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e917-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e917-live.lim.mp4 && mv $E/cut/e917-live.lim.mp4 $E/cut/e917-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e917-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e917-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e917-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
