#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e921/zhong-tian-qu-qi-e921-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e021-r2/video.json
# POLISH+SWAP 2026-11-21 (run 2026-11-22): the 2026-11-16 cut files (lines.json, srt, final.log; the mp4 is review-zt/ep/e021/final.mp4)
# go to cut/old-1116 once, with a .keep (kept for the backup); an old-* holding a .keep is never removed. A later run moves its own
# previous cut to old-HHMM after removing the non-kept old-* (at most one old cut besides the kept one: the disk is short).
mkdir -p $E/cut
[ -d $E/cut/old-1116 ] || { mkdir -p $E/cut/old-1116; mv $E/cut/e921-live.* $E/cut/final.log $E/cut/old-1116/ 2>/dev/null; touch $E/cut/old-1116/.keep; }
# SECOND WAVE 2026-11-22: the first-wave POLISH+SWAP cut (03:08, not delivered) goes to cut/old-w1 once, with a .keep.
[ -d $E/cut/old-w1 ] || { mkdir -p $E/cut/old-w1; mv $E/cut/e921-live.* $E/cut/final.log $E/cut/old-w1/ 2>/dev/null; touch $E/cut/old-w1/.keep; }
[ -f $E/cut/e921-live.mp4 ] && { for d in $E/cut/old-*; do [ -f $d/.keep ] || rm -rf $d; done; mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e921-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots are staged by live-action/stage.py 21 (refined picture + draft voice + trim -> clips/sNN-t1.mp4); run it
# when a clip is missing or picks.json is newer than any clip (a re-run of refine-prep.py 21 rewrites picks.json). stage.py
# links $E/audio -> zhong-tian-qu-qi-e921-dh/audio and $E/music -> zhong-tian-qu-qi-e921-dh/music, which is itself a link to
# ../_series/zhong-tian-qu-qi/music (made by hand for e921, the e920 way). Every effect is in the series library.
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 21 || exit 1; }
# e921 trims and seeds the edit table assumes (edit-dh-e921-live.json _note): picks.json as refine-prep.py 21 builds it from
# picks-merged.tsv, fix1/review-picks.tsv and review3-trims.tsv (REVIEW 3, review3-plan.md; run in colab/runs/e921-live:
# refine-prep.py 21 picks-merged.tsv fix1/review-picks.tsv review3-trims.tsv, then stage.py 21) -- the fix1 retakes s28 s37
# (9211201) and s36 (9211202); REVIEW 3 trims s03 s04 s05 s07 s09 s14 s14b (tails) and s28 (head, start 3.333). Whole frames: a start rounded DOWN and an end-before rounded UP to 3
# decimals, tolerance 0.001; 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.25,6.584),'s02':(0,8),'s03':(0,5.75),'s04':(0,5.5),'s05':(0.75,6.083),'s06':(0,6.584),'s07':(0.5,4.5),
 's08':(0,6.584),'s09':(1,5.75),'s10':(1,8),'s11':(0.5,6.584),'s12':(0,6.584),'s13':(0.75,6.584),'s14':(0,6.75),'s14b':(0,6.25),
 's15':(1.916,6.584),'s16':(1.5,4.75),'s17':(0.5,6.584),'s18':(0,6.584),'s19':(0.666,6.584),'s20':(2.5,6.584),'s21':(3.5,6),
 's21b':(0,2),'s22':(3.25,6),'s22b':(1.916,5.917),'s23':(1,5.25),'s24':(0.75,6.584),'s25':(0.25,4),'s26':(0.5,7.584),
 's27':(0,6.584),'s28':(3.333,8),'s28b':(2,5.5),'s29':(0,2.5),'s30':(0.583,6.584),'s31':(1.75,5.5),'s32':(0,6.584),
 's33':(0.75,6.584),'s34':(1,5.5),'s35':(0.75,6.584),'s36':(0,3),'s37':(1.166,8)}
seed={'s01':9211102,'s02':9211102,'s04':9211102,'s07':9211102,'s10':9211102,'s11':9211102,'s12':9211102,'s13':9211102,
 's14':9211102,'s14b':9211102,'s16':9211102,'s20':9211102,'s21':9211102,'s21b':9211102,'s22':9211102,'s23':9211102,
 's25':9211102,'s27':9211102,'s28':9211201,'s30':9211102,'s31':9211102,'s32':9211102,'s33':9211102,'s36':9211202,'s37':9211201}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9211101)' for s in p if s not in seed and p[s]['seed']!=9211101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s][\"crop\"]} (none expected)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-21 (edit table _note). SWAP: s13 s14b s20 s21b s22 s22b s36 s37 are the fixp retakes clips/sNN-t5.mp4
# (runpod/polish/picks.json, already trimmed: s13 9219102 1.083-6.583, s14b 9219102 0-6.25, s20 9219101 1.917-6.583, s21b 9219101
# 0.583-2.542, s22 9219101 0.375-3.75, s22b 9219101 0.667-4.667, s36 9219102 2.0-6.583, s37 9219102 0.958-8.0; the assembler takes
# the highest take number); picks.json and the want table above still describe the t1 staging, which stays on disk.
# SECOND WAVE 2026-11-22 (round4/round5 review-picks.tsv): s27 = round5 9219501 0.25-6.583, s32 = round4 9219401 1.0-6.583
# (the crop the pick asks for is done by the edit table's vf, not on the clip), s36 = round4 9219401 0-6.583; each replaced the
# clip's earlier t5 (s36) or stands over the t1 (s27, s32). No t6 exists for any of them and none is made here.
for s in s13 s14b s20 s21b s22 s22b s27 s32 s36 s37; do [ -f $E/clips/$s-t5.mp4 ] || { echo "missing clips/$s-t5.mp4"; exit 1; }; done
# the episode sfx dir (third sfx_dirs entry), made if missing: sob921 = Xiaohe's own sob after the kept span of the s21b draft
# (raw 2.55-3.45 s, the same child's voice, pitched x1.3 like the clip voice), laid at s21b c1.15 over the cut into s22;
# steps921 = cloth-shoe steps for s36 (Wei's five steps to the threshold, low-passed concrete steps, and the two thugs' fainter
# steps outside, the second one uneven) out of the series footstep_concrete_000-003.
S=/root/mokaair-work/videos/zhong-tian-qu-qi-e921-dh/sfx; L=/root/mokaair-work/videos/_series/zhong-tian-qu-qi/sfx; mkdir -p $S
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/sob921.wav ] || ffmpeg -v error -y -ss 2.55 -t 0.9 -i /root/mokaair-work/videos/zhong-tian-qu-qi-e921-dh/runpod/live/fixp/out/s21b-9219101.mp4 -vn -af "rubberband=pitch=1.3:formant=preserved,afade=t=in:d=0.05,afade=t=out:st=0.6:d=0.3,$AF" $S/sob921.wav
[ -f $S/steps921.wav ] || ffmpeg -v error -y -i $L/footstep_concrete_000.wav -i $L/footstep_concrete_001.wav -i $L/footstep_concrete_002.wav -i $L/footstep_concrete_003.wav -filter_complex "\
[0:a]asplit=3[w0][w2][w4];[1:a]asplit=2[w1][w3];[2:a]asplit=2[t0][t2];[3:a]asplit=2[t1][t3];\
[w0]adelay=100|100[a0];[w1]adelay=600|600[a1];[w2]adelay=1100|1100[a2];[w3]adelay=1600|1600[a3];[w4]adelay=2100|2100[a4];\
[t0]volume=-9dB,adelay=350|350[b0];[t1]volume=-12dB,adelay=700|700[b1];[t2]volume=-9dB,adelay=1350|1350[b2];[t3]volume=-12dB,adelay=1700|1700[b3];\
[a0][a1][a2][a3][a4][b0][b1][b2][b3]amix=inputs=9:normalize=0,lowpass=f=2500,apad=whole_dur=2.6,$AF" $S/steps921.wav
# steps921b (SECOND WAVE) replaces steps921 for the round4 s36 (6.56 s): Wei's ten cloth-shoe steps every 0.6 s from c0.2 to
# the threshold (c5.6), 0.9 dB softer each as he walks away, and the limping thug's firm step / dragged (-6 dB, low-passed) step
# pairs c0.35-2.60 until he is out at ~c2.8; series footstep_concrete_000-003. (steps921.wav, the first wave's 2.6 s, stays on disk.)
[ -f $S/steps921b.wav ] || ffmpeg -v error -y -i $L/footstep_concrete_000.wav -i $L/footstep_concrete_001.wav -i $L/footstep_concrete_002.wav -i $L/footstep_concrete_003.wav -filter_complex "\
[0:a]asplit=4[f0_0][f0_1][f0_2][f0_3];[1:a]asplit=4[f1_0][f1_1][f1_2][f1_3];[2:a]asplit=4[f2_0][f2_1][f2_2][f2_3];[3:a]asplit=4[f3_0][f3_1][f3_2][f3_3];\
[f0_0]volume=-0.0dB,adelay=200|200[e0];[f1_0]volume=-0.9dB,adelay=800|800[e1];[f2_0]volume=-1.8dB,adelay=1400|1400[e2];[f3_0]volume=-2.7dB,adelay=2000|2000[e3];\
[f0_1]volume=-3.6dB,adelay=2600|2600[e4];[f1_1]volume=-4.5dB,adelay=3200|3200[e5];[f2_1]volume=-5.4dB,adelay=3800|3800[e6];[f3_1]volume=-6.3dB,adelay=4400|4400[e7];\
[f0_2]volume=-7.2dB,adelay=5000|5000[e8];[f1_2]volume=-8.1dB,adelay=5600|5600[e9];\
[f2_2]volume=-9dB,adelay=350|350[e10];[f3_2]volume=-15dB,lowpass=f=900,adelay=800|800[e11];[f0_3]volume=-9dB,adelay=1250|1250[e12];\
[f1_3]volume=-15dB,lowpass=f=900,adelay=1700|1700[e13];[f2_3]volume=-11dB,adelay=2150|2150[e14];[f3_3]volume=-17dB,lowpass=f=900,adelay=2600|2600[e15];\
[e0][e1][e2][e3][e4][e5][e6][e7][e8][e9][e10][e11][e12][e13][e14][e15]amix=inputs=16:normalize=0,lowpass=f=2500,apad=whole_dur=6.6,atrim=0:6.6,$AF" $S/steps921b.wav
# zq921a29 / zq921a32 (voice_off s27 s32) have their leading silence trimmed by hand (audio/README-retakes.txt; untrimmed in audio/orig/).
# no shot is deleted: DROP is empty, so $VL is video.json as written (kept the e916/e920 way so a later REVIEW 3 can drop one)
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
# jitter: cut-qa's jitter() on the staged clips is in the edit table's _note (no deshake unless a clip reads over the bar)
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e021-r2/overlays.json $P/hailuo/edit-dh-e921-live.json $E $E/cut/e921-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e921-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# END (SWAP): s37 is Wei Shaoqing's line on the t5 retake (clip voice), 門 ends ~c6.90 and the take at c7.04; voice_until 7.0 ends
# the subtitle there; the gong and a low hit at c6.95 while the picture holds the take's last frame (a freeze, not an early
# fade: his mouth stops with the take), fades over c7.50-8.00 (vf), and min 11.04 holds ~3 s of black so the gong rings out.
# The sound fades over the last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e921-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e921-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e921-live.lim.mp4 && mv $E/cut/e921-live.lim.mp4 $E/cut/e921-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e921-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e921-live.mp4
# the delivery wants the true peak at or under -1 dBTP: print it (ebur128 true peak on the final file)
ffmpeg -hide_banner -nostats -i $E/cut/e921-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e921-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
