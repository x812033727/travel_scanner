#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e909/zhong-tian-qu-qi-e909-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e009-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e909-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e909-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# POLISH 2026-11-21 (review-zt free fixes; edit table _note POLISH): the episode sfx dir (fourth sfx_dirs entry), cut from
# _sfx/zhongtian-real-20261121: abacus909 (abacus-drop-01 0.19-1.09 s, the bead rattle, as abacus906) for s05's first door
# and s12, abacus909l (abacus-drop-01 0.15-2.05 s, as abacus10) under s14's clicks, whetstone909 (whetstone-02 0-2.45 s)
# for s05's third door and whetstone909s23 (whetstone-09 0-4.9 s) for s23, in place of the drawKnife strokes.
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e909-dh/sfx; mkdir -p $S
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/abacus909.wav ] || ffmpeg -v error -y -ss 0.19 -t 0.9 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.02,afade=t=out:st=0.5:d=0.4,$AF" $S/abacus909.wav
[ -f $S/abacus909l.wav ] || ffmpeg -v error -y -ss 0.15 -t 1.9 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.02,afade=t=out:st=1.5:d=0.4,$AF" $S/abacus909l.wav
[ -f $S/whetstone909.wav ] || ffmpeg -v error -y -t 2.45 -i $X/zhongtian-sfx-whetstone-02.wav -af "afade=t=out:st=2.15:d=0.3,$AF" $S/whetstone909.wav
[ -f $S/whetstone909s23.wav ] || ffmpeg -v error -y -t 4.9 -i $X/zhongtian-sfx-whetstone-09.wav -af "afade=t=in:d=0.05,afade=t=out:st=4.4:d=0.5,$AF" $S/whetstone909s23.wav
# GAP SFX 2026-11-22 (review-zt/GAP-BRIEF.md, gap-20261122 rows e009 s19-s23 old-door, s01 horse-snort; edit _note GAP SFX):
# horse909 = horse-snort-01 0-0.62 s (one snort, onset 0.04, body to 0.55) for s01; door909a = old-door-01 0-1.0 s (latch
# clack 0.04, second clack 0.36, wood tick 0.74) for s20's door opening; door909b = old-door-03 0.24-0.42 s (the single latch
# clack at 0.28 of the file, 0.04 into the cut) for s23, sized to fit the gap between his words.
[ -f $S/horse909.wav ] || ffmpeg -v error -y -t 0.62 -i $X/zhongtian-sfx-horse-snort-01.wav -af "afade=t=out:st=0.45:d=0.17,$AF" $S/horse909.wav
[ -f $S/door909a.wav ] || ffmpeg -v error -y -t 1.0 -i $X/zhongtian-sfx-old-door-01.wav -af "afade=t=out:st=0.8:d=0.2,$AF" $S/door909a.wav
[ -f $S/door909b.wav ] || ffmpeg -v error -y -ss 0.24 -t 0.18 -i $X/zhongtian-sfx-old-door-03.wav -af "afade=t=in:d=0.01,afade=t=out:st=0.1:d=0.08,$AF" $S/door909b.wav
# the refined shots must be staged first (live-action/stage.py 9: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 9"; exit 1; }
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e009-r2/overlays.json $P/hailuo/edit-dh-e909-live.json $E $E/cut/e909-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e909-live.mp4 ] || exit 1
# POLISH 2026-11-21 CC (audio untouched; times measured on the clips' own voice, 100/40 ms RMS): zq909a12 (s13) is split
# in two, 心算。 (voice c0.90-1.50) to cue start +0.845 s, and 還有，第三頁這筆，三錢記成了三兩。 from +2.425 s (the voiced
# burst at c3.35, 115 Hz with an h onset) to the cue's end -0.125 s (voice ends c7.7); zq909a21 (s22) starts 0.10 s earlier
# (voice c1.90; the review's 138.3 was whisper's word time, 0.7 s before the voice); zq909a19 (s20) ends 1.066 s earlier
# (voice ends c6.1, the review's 131.5). The srt is rewritten and the mp4's mov_text track replaced from it.
python3 - "$E/cut/e909-live.zh-TW.srt" <<'PY'
import re,sys
p=sys.argv[1]; s=open(p,encoding='utf-8').read()
f=lambda t:sum(float(x)*m for x,m in zip(t.replace(',','.').split(':'),(3600,60,1)))
g=lambda v:'%02d:%02d:%02d,%03d'%(int(v//3600),int(v%3600//60),int(v%60),round((v-int(v))*1000)%1000)
cues=[(f(a),f(b),t) for a,b,t in re.findall(r'(\d\d:\d\d:\d\d,\d{3}) --> (\d\d:\d\d:\d\d,\d{3})\n([^\n]*)',s)]
out=[]
for a,b,t in cues:
    if t=='心算。還有，第三頁這筆，三錢記成了三兩。':
        out+=[(a,a+0.845,'心算。'),(a+2.425,b-0.125,'還有，第三頁這筆，三錢記成了三兩。')]; print('a12 CC split ->',g(a),g(a+0.845),g(a+2.425),g(b-0.125)); continue
    if t.startswith('人不在，我明天再問她'): a-=0.10; print('a21 CC start ->',g(a))
    if t.startswith('秦霜，睡了嗎？'): b-=1.066; print('a19 CC end ->',g(b))
    out.append((a,b,t))
open(p,'w',encoding='utf-8').write('\n'.join(f'{i+1}\n{g(a)} --> {g(b)}\n{t}\n' for i,(a,b,t) in enumerate(out)))
PY
ffmpeg -v error -y -i $E/cut/e909-live.mp4 -i $E/cut/e909-live.zh-TW.srt -map 0:v -map 0:a -map 1:0 -c:v copy -c:a copy -c:s mov_text -metadata:s:s:0 language=chi -movflags +faststart $E/cut/e909-live.sub.mp4 && mv $E/cut/e909-live.sub.mp4 $E/cut/e909-live.mp4
# a -4.4 dBFS sample-peak limiter before loudnorm2 keeps it linear (the e908 cut review found a click from its dynamic fallback;
# e909 review 3: at -4 dBFS the true peak -3.58 plus the +1.43 dB gain overshot TP -2.2 by 0.05 and loudnorm went dynamic)
ffmpeg -v error -y -i $E/cut/e909-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=2:release=60:level=false,aresample=48000" $E/cut/e909-live.lim.mp4 && mv $E/cut/e909-live.lim.mp4 $E/cut/e909-live.mp4
ffmpeg -hide_banner -i $E/cut/e909-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e909-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e909-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
