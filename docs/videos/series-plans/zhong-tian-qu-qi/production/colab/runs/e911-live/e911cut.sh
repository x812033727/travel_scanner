#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e911/zhong-tian-qu-qi-e911-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e011-r2/video.json
V=${V:-v1}; mkdir -p $E/cut; [ -f $E/cut/e911-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e911-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
# keep one earlier cut only (the disk is shared with the other episodes' polish cuts); an old-* holding a .keep file
# (SWAP 2026-11-21: the pre-swap POLISH cut old-2204 and old-2155, kept for the backup) is never removed
for d in $(ls -d $E/cut/old-* 2>/dev/null | sort | head -n -1); do [ -f $d/.keep ] || rm -rf $d; done
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 11: refined picture + draft voice + trim/crop -> clips/sNN-t1.mp4)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 11"; exit 1; }
# e911 trims (edit-dh-e911-live.json _note): a whisper pass on the drafts found picks.json / pick-review cutting spoken lines
# (s10 s11 s20 s25 s26 s31 s32 s33 s35), pick-review's smile trims (s13 s14 s17 s21 s30), and every start rounded DOWN and
# every end-before rounded UP to a whole 24 fps frame (input -ss keeps frames at/after start, -to drops a frame whose end
# passes it: 0.792 lost s03's frame 19, 7.708 left s11 a frame short). Warn (not stop) if picks.json does not have them.
# REVIEW 3 (cut-review.md + cut-review-2.md, review3-trims.tsv): s01 4.25 (the grab on the c0.3 hit), s04 4.5, s09 6.25, s12 5.0,
# s21 4.292 (a18 atempo 1.19, no hold), s26 1.75 and s31 2.291 (spears at the head), s29 7.5.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(4.25,6.417),'s02':(0,2.791),'s03':(0.791,5.583),'s04':(0,4.5),'s05':(0.875,7.5),'s06':(3.375,7.5),'s07':(0,3.375),
 's08':(0.583,0),'s09':(0.75,6.25),'s10':(2.0,0),'s11':(2.625,7.709),'s12':(0,5.0),'s13':(2.583,0),'s14':(0,5.417),'s15':(0,4.584),
 's16':(0,0),'s17':(0.375,5.792),'s18':(0,3.5),'s19':(1.0,6.0),'s20':(0.5,7.834),'s21':(0,4.292),'s22':(0.375,4.625),'s23':(0.583,5.583),
 's24':(1.375,6.791),'s25':(3.0,10.084),'s26':(1.75,0),'s27':(0,2.0),'s28':(0,10.084),'s29':(0,7.5),'s30':(0.791,7.125),'s31':(2.291,0),
 's32':(2.791,7.708),'s33':(0.75,7.0),'s34':(0.375,3.584),'s35':(1.791,0)}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.0005 or abs(p[s]['trim'].get('end-before',0)-b)>0.0005]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH 2026-11-21 (review-zt free fixes; edit table _note POLISH). The episode sfx dir (third sfx_dirs entry), cut from
# _sfx/zhongtian-real-20261121: bead911 = one bead click out of abacus-drop-01 (0.245-0.325 s, e902's bead902 recipe) for
# s27/s34; staff911 = staff-thud-01 from 1.03 s (the strike, e906's hoe906) for Qin Shuang's stick in s34; grp911 =
# footsteps-group-04 0-1.9 s (a group shuffling back, fade 0.5) for the constables in s11 and s22.
X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; S=/root/mokaair-work/videos/zhong-tian-qu-qi-e911-dh/sfx; mkdir -p $S
AF="aresample=48000,aformat=channel_layouts=stereo"
[ -f $S/bead911.wav ] || ffmpeg -v error -y -ss 0.245 -t 0.08 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.003,afade=t=out:st=0.04:d=0.04,volume=14dB,$AF" $S/bead911.wav
[ -f $S/staff911.wav ] || ffmpeg -v error -y -ss 1.03 -t 0.4 -i $X/zhongtian-sfx-staff-thud-01.wav -af "afade=t=out:st=0.25:d=0.15,$AF" $S/staff911.wav
[ -f $S/grp911.wav ] || ffmpeg -v error -y -t 1.9 -i $X/zhongtian-sfx-footsteps-group-04.wav -af "afade=t=in:d=0.05,afade=t=out:st=1.4:d=0.5,$AF" $S/grp911.wav
# vf.s16 reads a moving alpha mask (the spear between the two heads, tracked on the published final): made if missing
mkdir -p $E/vfx; [ -f $E/vfx/s16-spear-mask.mkv ] || python3 $P/colab/runs/e911-live/s16-spear-mask.py $E/vfx/s16-spear-mask.mkv
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e011-r2/overlays.json $P/hailuo/edit-dh-e911-live.json $E $E/cut/e911-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e911-live.mp4 ] || exit 1
# POLISH 2026-11-21: CC 31 (zq911a32, s35) ends at s35 c4.70 (review e011 item 10: 185.2 s). voice_until s35 4.7 stops the
# speech span at the take's last syllable (c4.35), so the srt end is set here, 0.35 s past the voice, from final.log's s35 start.
python3 -c "
import re
log=open('$E/cut/final.log').read(); t=float(re.search(r'^s35 ([\d.]+) ',log,re.M).group(1))+4.70
p='$E/cut/e911-live.zh-TW.srt'; b=open(p,encoding='utf-8').read().rstrip().split('\n\n')
h,m=divmod(round(t*1000),3600000); m,ms=divmod(m,60000); sec,ms=divmod(ms,1000)
L=b[-1].split('\n'); assert '名冊就不查' in L[2], L; L[1]=L[1].split(' --> ')[0]+f' --> {h:02d}:{m:02d}:{sec:02d},{ms:03d}'
b[-1]='\n'.join(L); open(p,'w',encoding='utf-8').write('\n\n'.join(b)+'\n'); print('CC 31', L[1])"
# a sample-peak limiter before loudnorm2 keeps it linear (the e908 cut review found a click from its dynamic fallback;
# e909 review 3: at -4 dBFS the true peak -3.58 plus the +1.43 dB gain overshot TP -2.2 by 0.05 and loudnorm went dynamic;
# e910 review 3: with louder accents and beds the same limiter left a true peak of -2.39 (input -15.25 LUFS, +1.25 dB to go),
# loudnorm2 went dynamic and the cut clicked to +3.6 dBFS at 3.8 s. The overshoot is made by the AAC encode after the limiter
# (the limited PCM measures -4.3 dBTP): attack 2 ms -> -2.3, 0.5 ms -> -1.8, 5 ms -> -4.2 on the s01 footsteps, so the attack
# is 5 ms (limit still 0.6 = -4.4 dBFS; 0.5 lost 0.7 LU and stayed at -2.9 dBTP))
ffmpeg -v error -y -i $E/cut/e911-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=5:release=60:level=false,aresample=48000" $E/cut/e911-live.lim.mp4 && mv $E/cut/e911-live.lim.mp4 $E/cut/e911-live.mp4
ffmpeg -hide_banner -i $E/cut/e911-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e911-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e911-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
