#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e908/zhong-tian-qu-qi-e908-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e008-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e908-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e908-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# the 42 refined shots must be staged first (live-action/stage.py 8: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 8"; exit 1; }
# POLISH 2026-11-21 (review-zt free fixes; edit table _note POLISH): two shots re-trimmed without stage.py (the refined
# pictures runpod/a/st2 are not on this disk): clips/s01-t2.mp4 = s01-t1 from 1.5 s (2.7 s of silent look before the first
# word -> 1.2 s), clips/s08b-t2.mp4 = s08b-t1 to 6.0 s (the empty money box tail). x264 crf 12, aac 32 kHz; assemble-v4's
# pick() takes the highest -tN, so the -t1 files stay as they were. Made again if missing.
C=$E/clips
[ -f $C/s01-t2.mp4 ]  || ffmpeg -v error -y -i $C/s01-t1.mp4  -ss 1.5 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s01-t2.mp4
[ -f $C/s08b-t2.mp4 ] || ffmpeg -v error -y -i $C/s08b-t1.mp4 -t 6.0  -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s08b-t2.mp4
# the episode sfx dir (third sfx_dirs entry): murmur08.wav (crowd-murmur.py 8 8, the owner's reversed-recordings crowd),
# drum908.wav = a 0.9 s two-hit unit (strong, -6 dB) cut from zhongtian-sfx-war-drum-01 (0.015-0.465 s each, 0.15 s fade);
# the edit table loops it under the s19-s20 gallop (script: 急促的鼓); horse908.wav = hooves_trot 0-1.6 s (four steps,
# fade 0.6) for the horse shifting after Qin Shuang mounts in s18 (no real horse snort in either library).
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e908-dh/sfx; mkdir -p $S
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/murmur08.wav ] || python3 -I $Q/crowd-murmur.py 8 8
[ -f $S/drum908.wav ] || ffmpeg -v error -y -ss 0.015 -t 0.45 -i $X/zhongtian-sfx-war-drum-01.wav -ss 0.015 -t 0.45 -i $X/zhongtian-sfx-war-drum-01.wav -filter_complex "[0]$AF,apad=whole_dur=0.45,afade=t=out:st=0.3:d=0.15[a];[1]$AF,apad=whole_dur=0.45,afade=t=out:st=0.3:d=0.15,volume=-6dB[b];[a][b]concat=n=2:v=0:a=1" $S/drum908.wav
[ -f $S/horse908.wav ] || ffmpeg -v error -y -t 1.6 -i /root/mokaair-work/videos/_series/zhong-tian-qu-qi/sfx/hooves_trot.wav -af "afade=t=out:st=1.0:d=0.6,$AF" $S/horse908.wav
# $VL = video.json with the CC of zq908a32 (s29, CC 30, 23 characters on one line) broken at its full stop
VL=$E/video-live.json
python3 -c "import json;v=json.load(open('$VJ'))
for s in v['scenes']:
  for l in s.get('lines') or []:
    if l['id']=='zq908a32': l['text']=l['text'].replace('天上。欠','天上。\\n欠'); assert '\\n' in l['text']
json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e008-r2/overlays.json $P/hailuo/edit-dh-e908-live.json $E $E/cut/e908-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e908-live.mp4 ] || exit 1
# e908 cut review: assemble-v4's own loudnorm leaves TP about -1.4, loudnorm2 then cannot go linear (TP -2.2) and its
# dynamic fallback put a click at 124.77 (true peak +2.5 dBFS); a sample-peak limiter at -4 dBFS first keeps it linear
# POLISH 2026-11-21: the polish cut came out 0.07 dB on the dynamic side at 0.63 (-2.13 after the gain; no click, 50 ms peaks
# all <= -2.1 dBFS, true peak -1.8); 0.6 (-4.4 dBFS) for the next run
ffmpeg -v error -y -i $E/cut/e908-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=2:release=60:level=false,aresample=48000" $E/cut/e908-live.lim.mp4 && mv $E/cut/e908-live.lim.mp4 $E/cut/e908-live.mp4
ffmpeg -hide_banner -i $E/cut/e908-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e908-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e908-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
