#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e905/zhong-tian-qu-qi-e905-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e005-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e905-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e905-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# POLISH 2026-11-21 (review-zt free fixes): s05 and s09 are re-trimmed without stage.py (the refined pictures runpod/a/st2 are
# not on this disk): clips/s05-t2.mp4 = s05-t1 from 1.5 s, clips/s09-t2.mp4 = s09-t1 to 3.6 s (x264 crf 12, aac 32 kHz);
# assemble-v4's pick() takes the highest -tN, so s05-t1/s09-t1 stay as they were. Make them again if missing.
C=$E/clips
[ -f $C/s05-t2.mp4 ] || ffmpeg -v error -y -i $C/s05-t1.mp4 -ss 1.5 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s05-t2.mp4
[ -f $C/s09-t2.mp4 ] || ffmpeg -v error -y -i $C/s09-t1.mp4 -t 3.6 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s09-t2.mp4
# the episode sfx dir (third sfx_dirs entry) holds lather905.wav (zhongtian-sfx-soap-lather-01 2.0-4.7 s, fades 0.15/0.4)
# and rooster905.wav (zhongtian-sfx-rooster-village-loop 1.9-4.6 s: the one crow, fades 0.1/0.5)
S=/root/mokaair-work/videos/zhong-tian-qu-qi-e905-dh/sfx; mkdir -p $S
[ -f $S/lather905.wav ] || ffmpeg -v error -y -ss 2.0 -t 2.7 -i /root/mokaair-work/videos/_sfx/zhongtian-real-20261121/zhongtian-sfx-soap-lather-01.wav -af "afade=t=in:d=0.15,afade=t=out:st=2.3:d=0.4,aresample=48000,aformat=channel_layouts=stereo" $S/lather905.wav
[ -f $S/rooster905.wav ] || ffmpeg -v error -y -ss 1.9 -t 2.7 -i /root/mokaair-work/videos/_sfx/zhongtian-real-20261121/zhongtian-sfx-rooster-village-loop.wav -af "afade=t=in:d=0.1,afade=t=out:st=2.2:d=0.5,aresample=48000,aformat=channel_layouts=stereo" $S/rooster905.wav
# $VL = video.json with the CC text of zq905a31 (s32) cut to what the take says: whisper and the review hear
# 三錢？一斗米才幾十文，妳這價…… and nothing of 會不會太高 (the recording is not laid; the take's own voice plays)
VL=$E/video-live.json
python3 -c "import json;v=json.load(open('$VJ'))
for s in v['scenes']:
  for l in s.get('lines') or []:
    if l['id']=='zq905a31': l['text']='三錢？一斗米才幾十文，妳這價……'
json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e005-r2/overlays.json $P/hailuo/edit-dh-e905-live.json $E $E/cut/e905-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e905-live.mp4 ] || exit 1
bash $Q/loudnorm2.sh $E/cut/e905-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e905-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
