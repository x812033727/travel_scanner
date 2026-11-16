#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e920/zhong-tian-qu-qi-e920-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e020-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e920-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e920-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 20 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 20 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e920-dh/audio and $E/music -> zhong-tian-qu-qi-e920-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e920, the e917/e918 way). Every effect is in the series library.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 20 || exit 1; }
# e920 trims and seeds the edit table assumes (edit-dh-e920-live.json _note): picks.json as refine-prep.py 20 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv in that order (run in colab/runs/e920-live) -- the fix1 retakes
# s33 s37b (9201201). REVIEW 3 (review3-plan.md, both cut reviews): s23 is the d1 draft 9201101 again (the guild master's palm on
# a stack of blue books, as s19-s22; refined once on Colab with q-e920s23refine.sh; the fix1 refine, the bundle, is kept as
# runpod/a/st2/refined/s23-9201201.mp4), and s07 s12 s19 s28 s30 are trimmed, each checked frame by frame and against
# faster-whisper word times. No crop= in any pick. After any change: refine-prep.py 20 picks-merged.tsv
# fix1/review-picks.tsv review3-trims.tsv, stage.py 20, this table. Whole frames: a start rounded DOWN and an end-before
# rounded UP to 3 decimals, tolerance 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(3,6.584),'s02':(1.25,5.375),'s03':(0.416,6.584),'s04':(0,8),'s05':(1.5,6.584),'s06':(1.5,5.917),'s07':(1,6.584),
 's08':(0.5,4.75),'s09':(0,6.584),'s10':(2.125,6.584),'s11':(0.916,6.584),'s12':(0,5),'s13':(0.5,6.584),'s14':(0.5,5.5),
 's15':(0,3.25),'s16':(0.5,3),'s17':(2.083,6.584),'s18':(1.5,5),'s19':(1,8),'s20':(0.5,6.584),'s21':(0.166,5.75),
 's22':(0.75,6.584),'s23':(0,6.584),'s24':(0,5.5),'s25':(1,6.584),'s26':(0,6.584),'s27':(0,10.125),'s28':(0.5,6.5),
 's29':(0.166,4.875),'s30':(0.25,5),'s31':(1.916,6.584),'s32':(1,4.75),'s33':(0.416,6.584),'s34':(1.416,6.584),
 's35':(0.375,6.584),'s36':(0.5,8),'s37':(2,4.5),'s37b':(3.583,6.584),'s38':(2.5,6.584)}
seed={'s01':9201102,'s04':9201102,'s05':9201102,'s07':9201102,'s08':9201102,'s09':9201102,'s14':9201102,'s15':9201102,
 's16':9201102,'s17':9201102,'s18':9201102,'s27':9201102,'s33':9201201,'s34':9201102,'s35':9201102,'s36':9201102,
 's37':9201102,'s37b':9201201,'s38':9201102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9201101)' for s in p if s not in seed and p[s]['seed']!=9201101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# REVIEW 3: s37 (the CG hand catching a palm-sized abacus, half the size of s37b's) is deleted -- the assembler cuts every scene
# video.json lists, so the cut, audio-qa and the sheets read $VL, video.json without the scenes in DROP (s37 has no lines; it
# stays in picks.json, staged and unused), the e916 way
VL=$E/video-live.json; DROP="s37"
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e020-r2/overlays.json $P/hailuo/edit-dh-e920-live.json $E $E/cut/e920-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e920-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# END (the close of arc 2): s38 is Wei Shaoqing's line on his own take (clip voice), 家 ends ~c3.80; the gong and a low hit at
# c3.85, the picture fades over c3.85-4.35 (vf fade, voice_until 3.85 ends the subtitle on 家) and min 7.875 (REVIEW 3; was
# 7.375) holds ~3.5 s of black (the take ends at 4.06, the assembler clones its last frame under the fade) so the gong and the tension cue ring out
# in the dark. The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e920-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e920-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e920-live.lim.mp4 && mv $E/cut/e920-live.lim.mp4 $E/cut/e920-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e920-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e920-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e920-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
