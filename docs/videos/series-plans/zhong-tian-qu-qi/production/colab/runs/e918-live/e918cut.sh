#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e918/zhong-tian-qu-qi-e918-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e018-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e918-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e918-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 18 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 18 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e918-dh/audio and $E/music -> zhong-tian-qu-qi-e918-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e918, the e917 way). $E/sfx holds blowout.wav (a synthesized puff for
# s18's lamp, the library has none): the edit table lists it as a second sfx dir.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 18 || exit 1; }
# e918 trims and seeds the edit table assumes (edit-dh-e918-live.json _note): picks.json as refine-prep.py 18 builds it from
# picks-merged.tsv, fix1/review-picks.tsv, fix2/review-picks.tsv and review3-trims.tsv in that order (run in
# colab/runs/e918-live) -- the fix1 retakes s35 s40 (9181202) and the fix2 retake s37 (9181302, the kneeling back view; the
# fix1 refine is kept as runpod/a/st2/refined/s37-9181202.mp4); s20's fixed crop 834:472:126:0 and s09's 640:362:300:50
# (REVIEW 3) are in picks.json. The first cut had no review3-trims.tsv; REVIEW 3 (review3-plan.md, both cut reviews) trims
# s01 s05 s12 s16 s19 s23 s39, each checked frame by frame and, where a line runs, against faster-whisper word times (no
# word cut). After any change: refine-prep.py 18 ... review3-trims.tsv, stage.py 18 (s37 must stay 9181302), this table. Whole frames: a start rounded DOWN and an end-before
# rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1,4),'s02':(0,10.125),'s03':(0.5,5.5),'s04':(0.25,4.25),'s05':(0.5,5),'s06':(0.5,6),'s07':(1.875,6.584),
 's08':(1.25,6.584),'s09':(0,5.042),'s10':(0.25,6.5),'s11':(0.125,6.584),'s12':(0,2),'s13':(0.5,4.5),'s14':(0.125,6.584),
 's15':(0.375,6.25),'s16':(0.75,6),'s17':(0.5,4.584),'s18':(0,6),'s19':(1.5,6.584),'s20':(0.25,6.25),'s21':(0.625,6.25),
 's22':(0.375,4.625),'s23':(0,4.625),'s24':(0,6.584),'s25':(0.25,8),'s26':(0,6.584),'s27':(1.5,6.584),'s28':(0.875,4.625),
 's29':(0.5,4),'s30':(0.375,6.584),'s31':(0.25,7.5),'s32':(0.25,6.584),'s33':(0.125,6.584),'s34':(1,6.584),'s35':(0,6.584),
 's36':(1.25,8),'s37':(0,6.584),'s37b':(1.25,7.75),'s38':(0.25,4.75),'s39':(0,5.5),'s40':(0.75,6.584)}
seed={'s02':9181102,'s03':9181102,'s05':9181102,'s09':9181102,'s12':9181102,'s14':9181102,'s15':9181102,'s16':9181102,
 's17':9181102,'s18':9181102,'s19':9181102,'s21':9181102,'s22':9181102,'s25':9181102,'s32':9181102,'s35':9181202,'s36':9181102,
 's37':9181302,'s37b':9181102,'s40':9181202}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9181101)' for s in p if s not in seed and p[s]['seed']!=9181101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# no shot is deleted: the cut, audio-qa and the sheets read video.json itself
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e018-r2/overlays.json $P/hailuo/edit-dh-e918-live.json $E $E/cut/e918-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e918-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# END: s40 is Qian's whisper a39 on his own take (clip voice, x1.35); the gong at c5.75 after 河 (ends c5.73), the picture
# fades over c5.75-6.25 (vf fade, REVIEW 3; was 5.50) and min 9.25 holds ~3 s of black (voice_until 5.75 ends the subtitle on 河) so the gong and the cue ring out in the dark. The sound fades
# over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e918-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e918-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e918-live.lim.mp4 && mv $E/cut/e918-live.lim.mp4 $E/cut/e918-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e918-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e918-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e918-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
