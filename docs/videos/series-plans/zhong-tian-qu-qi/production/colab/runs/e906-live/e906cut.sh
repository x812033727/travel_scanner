#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e906/zhong-tian-qu-qi-e906-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e006-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e906-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e906-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# POLISH 2026-11-21 (review-zt free fixes): s24 and s34 are re-trimmed without stage.py (the refined pictures runpod/a/st2 are
# not on this disk): clips/s24-t2.mp4 = s24-t1 from 1.4 s, clips/s34-t2.mp4 = s34-t1 to 4.9 s (x264 crf 12, aac 32 kHz);
# assemble-v4's pick() takes the highest -tN, so s24-t1/s34-t1 stay as they were. Make them again if missing.
C=$E/clips
[ -f $C/s24-t2.mp4 ] || ffmpeg -v error -y -i $C/s24-t1.mp4 -ss 1.4 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s24-t2.mp4
[ -f $C/s34-t2.mp4 ] || ffmpeg -v error -y -i $C/s34-t1.mp4 -t 4.9 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s34-t2.mp4
# the episode sfx dir (third sfx_dirs entry), cut from _sfx/zhongtian-real-20261121 so each file starts on its hit:
# stamp906 (thumbprint-01 from 0.12 s, the office-stamp thud), drum906 (war-drum-01 0.015-1.215 s, the taiko hit = 午時鼓),
# hoe906 (staff-thud-01 from 1.03 s, the staff strike = hoe planted), abacus906 (abacus-drop-01 0.19-1.09 s, a bead rattle)
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e906-dh/sfx; mkdir -p $S
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/stamp906.wav ] || ffmpeg -v error -y -ss 0.12 -t 0.43 -i $X/zhongtian-sfx-thumbprint-01.wav -af "afade=t=out:st=0.28:d=0.15,$AF" $S/stamp906.wav
[ -f $S/drum906.wav ] || ffmpeg -v error -y -ss 0.015 -t 1.2 -i $X/zhongtian-sfx-war-drum-01.wav -af "afade=t=out:st=0.6:d=0.6,$AF" $S/drum906.wav
[ -f $S/hoe906.wav ] || ffmpeg -v error -y -ss 1.03 -t 0.4 -i $X/zhongtian-sfx-staff-thud-01.wav -af "afade=t=out:st=0.25:d=0.15,$AF" $S/hoe906.wav
[ -f $S/abacus906.wav ] || ffmpeg -v error -y -ss 0.19 -t 0.9 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=out:st=0.5:d=0.4,$AF" $S/abacus906.wav
# $VL = video.json with the CC text of zq906a37 (s37) cut to what the take says: its speech is two phrases, 2.05-3.12 and
# 3.34-4.60 (5 and 7 syllables at the take's own rate), and neither whisper nor the review hears 就是錢員外 (owner to listen)
VL=$E/video-live.json
python3 -c "import json;v=json.load(open('$VJ'))
for s in v['scenes']:
  for l in s.get('lines') or []:
    if l['id']=='zq906a37': l['text']='你看茶樓上，靠著欄杆喝酒的……'
json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e006-r2/overlays.json $P/hailuo/edit-dh-e906-live.json $E $E/cut/e906-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e906-live.mp4 ] || exit 1
bash $Q/loudnorm2.sh $E/cut/e906-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e906-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
