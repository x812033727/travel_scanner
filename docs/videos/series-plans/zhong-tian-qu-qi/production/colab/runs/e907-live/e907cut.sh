#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e907/zhong-tian-qu-qi-e907-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e007-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e907-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e907-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# POLISH 2026-11-21 (review-zt free fixes, edit table _note POLISH): s03, s14 and s18 end earlier without stage.py (the refined
# pictures runpod/a/st2 are not on this disk): clips/sNN-t2.mp4 = sNN-t1 cut to 4.0 / 5.0 / 5.0 s (x264 crf 12, aac 32 kHz);
# assemble-v4's pick() takes the highest -tN, so the -t1 files stay as they were. Made again if missing.
C=$E/clips
for x in s03:4.0 s14:5.0 s18:5.0; do s=${x%%:*}; n=${x#*:}
  [ -f $C/$s-t2.mp4 ] || ffmpeg -v error -y -i $C/$s-t1.mp4 -t $n -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/$s-t2.mp4; done
# the episode sfx dir (third sfx_dirs entry): cart907 (wooden-cart-03 0-7.8 s, fades 0.4/1.0), lather907 (soap-lather-01
# 2.0-4.7 s, fades 0.15/0.4), rooster907 (rooster-village-loop 1.9-4.6 s, the one crow), murmur07 (crowd-murmur.py 7 12:
# the episode's recordings reversed, no readable word)
S=/root/mokaair-work/videos/zhong-tian-qu-qi-e907-dh/sfx; N=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; mkdir -p $S
[ -f $S/cart907.wav ] || ffmpeg -v error -y -ss 0.0 -t 7.8 -i $N/zhongtian-sfx-wooden-cart-03.wav -af "afade=t=in:d=0.4,afade=t=out:st=6.8:d=1.0,aresample=48000,aformat=channel_layouts=stereo" $S/cart907.wav
[ -f $S/lather907.wav ] || ffmpeg -v error -y -ss 2.0 -t 2.7 -i $N/zhongtian-sfx-soap-lather-01.wav -af "afade=t=in:d=0.15,afade=t=out:st=2.3:d=0.4,aresample=48000,aformat=channel_layouts=stereo" $S/lather907.wav
[ -f $S/rooster907.wav ] || ffmpeg -v error -y -ss 1.9 -t 2.7 -i $N/zhongtian-sfx-rooster-village-loop.wav -af "afade=t=in:d=0.1,afade=t=out:st=2.2:d=0.5,aresample=48000,aformat=channel_layouts=stereo" $S/rooster907.wav
[ -f $S/murmur07.wav ] || python3 -I $Q/crowd-murmur.py 7 12
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e007-r2/overlays.json $P/hailuo/edit-dh-e907-live.json $E $E/cut/e907-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e907-live.mp4 ] || exit 1
# CC of zq907a20 (s23, Xu Yan off screen): the recording opens with ~0.7 s of breath and a pause before 這不是 (first voiced
# frame at 1.45 s of the file; whisper of the old final hears the words from 142.61), so the cue starts 1.30 s later than the
# line is laid; the audio is untouched. The srt is rewritten and the mp4's mov_text track replaced from it.
python3 - "$E/cut/e907-live.zh-TW.srt" <<'PY'
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
f=lambda t:sum(float(x)*m for x,m in zip(t.replace(',','.').split(':'),(3600,60,1)))
g=lambda v:'%02d:%02d:%02d,%03d'%(int(v//3600),int(v%3600//60),int(v%60),round((v-int(v))*1000)%1000)
def fix(m):
    a,b,txt=m.group(1),m.group(2),m.group(3)
    if txt.startswith('這不是前天夜裡'): a=g(f(a)+1.30); print('a20 CC ->',a)
    return f'{a} --> {b}\n{txt}'
s=re.sub(r'(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})\n([^\n]*)',fix,s)
open(p,'w',encoding='utf-8').write(s)
PY
ffmpeg -v error -y -i $E/cut/e907-live.mp4 -i $E/cut/e907-live.zh-TW.srt -map 0:v -map 0:a -map 1:0 -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=chi -movflags +faststart $E/cut/e907-live.sub.mp4 && mv $E/cut/e907-live.sub.mp4 $E/cut/e907-live.mp4
bash $Q/loudnorm2.sh $E/cut/e907-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e907-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
