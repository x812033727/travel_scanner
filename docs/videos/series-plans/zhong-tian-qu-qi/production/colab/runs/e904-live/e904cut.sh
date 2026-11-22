#!/usr/bin/env bash
# e904cut.sh: the episode-4 live-action cut (written 2026-11-21 for the review-zt polish, the e901cut.sh / e902cut.sh way;
# episode 4 had been cut by hand on 2026-11-10 with the same assemble-v4 call and no script).
# The hand cut left no video-live.json / live-clips-e904.json in _live-e904: the edit table's _note says the onscreen
# rule ran "against docs/videos/zhong-tian-qu-qi-e004-r2/video.json", and cut/final.log (and ep/e004/work/final.log) list
# all 40 scenes s01-s40 with s12/s23/s40 as stills from first-frames/, so nothing was dropped. $VL is rebuilt the
# e905cut.sh way: video.json copied as it is (DROP empty).
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e904/zhong-tian-qu-qi-e904-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e004-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e904-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e904-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# clips/sNN-t1.mp4 are the staged live clips as they came back from the Drive backup (review-picks-a/-b, fix1-fix4 in
# colab/runs/e904-live); first-frames/ holds the s12/s23/s40 stills; $E/audio and $E/music are links to
# zhong-tian-qu-qi-e904-dh/audio and /music.
# POLISH 2026-11-21 (review-zt free fixes; edit table _note POLISH): s30 starts 2.5 s later without stage.py (the refined
# pictures are not on this disk): clips/s30-t2.mp4 = s30-t1 from 2.5 s, x264 crf 12, aac 32 kHz; assemble-v4's pick()
# takes the highest -tN, so s30-t1 stays as it was. Made again if missing.
C=$E/clips
[ -f $C/s30-t2.mp4 ] || ffmpeg -v error -y -i $C/s30-t1.mp4 -ss 2.5 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s30-t2.mp4
# SWAP 2026-11-21 (review-zt SWAP-BRIEF; runpod/polish/picks.json, fix-polish/review-picks.tsv): s14/s16/s23 are the fixp
# retakes clips/sNN-t5.mp4 (s19 and s40 KEEP). s14 drops the first 0.5 s of its t5 (her lips part at 0-0.5; the inner
# line a16 still fits before her line at 4.20 without speeding up): clips/s14-t6.mp4, made again if missing.
[ -f $C/s14-t6.mp4 ] || ffmpeg -v error -y -i $C/s14-t5.mp4 -ss 0.5 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s14-t6.mp4
# SWAP 2026-11-22 (second wave, round4): s25 is the fixp4 retake clips/s25-t5.mp4 (already trimmed 0.375-5.833 s; no t6
# for s25, so the assembler takes t5 as it is). The delivered first-wave cut was moved by hand to cut/old-w1 (.keep).
VL=$E/video-live.json; DROP=""
# $VL = video.json (DROP empty) with s14 Tang Xiaotang on screen: the t5 retake shows her in the doorway saying a17 with
# her lips, so she joins s14's characters and a17 loses 畫外 (the clip's voice plays; s16 does the same via voice_on).
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d]
for s in v['scenes']:
  if s['id']=='s14':
    s['data']['characters']=['xuyan','tangxiaotang']
    for l in s['lines']:
      if l['id']=='zq904a17': l['emotion']='說話快'
json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e004-r2/overlays.json $P/hailuo/edit-dh-e904-live.json $E $E/cut/e904-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e904-live.mp4 ] || exit 1
# the e901 / e908-e930 finish: a sample-peak limiter (attack 8 ms, limit 0.55), then loudnorm2.sh (linear, -14 LUFS,
# TP -2.2). The first cut (2026-11-10) had neither; the music is 5-6 dB louder now.
ffmpeg -v error -y -i $E/cut/e904-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000" $E/cut/e904-live.lim.mp4 && mv $E/cut/e904-live.lim.mp4 $E/cut/e904-live.mp4
ffmpeg -hide_banner -i $E/cut/e904-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e904-live.mp4
# POLISH run 1: the line above printed -15.83 LUFS / -4.32 dBTP (+1.83 dB, linear), yet the result had a -0.4 dBFS peak at
# 1.0 s (s01's fire-1 crackle; the 2026-11-10 final had it at -2.2 too) and cut-qa failed the loudness check: loudnorm's
# first pass misses that early transient. A second limiter at 0.7 (-3.1 dBFS) only touches it: -14.0 LUFS stays, TP -3.0.
ffmpeg -v error -y -i $E/cut/e904-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e904-live.lim.mp4 && mv $E/cut/e904-live.lim.mp4 $E/cut/e904-live.mp4
ffmpeg -hide_banner -i $E/cut/e904-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|Peak):' | tail -2
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e904-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
