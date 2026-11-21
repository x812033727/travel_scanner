#!/usr/bin/env bash
# e902cut.sh: the episode-2 live-action cut (written 2026-11-21 for the review-zt polish, the e901cut.sh / e905cut.sh way;
# episode 2 had been cut by hand on 2026-11-09 with the same assemble-v4 call and no script).
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e902/zhong-tian-qu-qi-e902-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e002-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e902-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e902-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# clips/sNN-t1.mp4 are the staged live clips as they came back from the Drive backup (picks.json, fix1-fix4 in
# colab/runs/e902-live); $E/audio and $E/music are links to zhong-tian-qu-qi-e902-dh/audio and /music. Nothing is dropped.
# POLISH 2026-11-21 (review-zt free fixes; edit table _note POLISH): four shots re-trimmed without stage.py (the refined
# pictures are not on this disk): s02 to 4.4 s (Erniu's grin at the camera), s13b to 4.9 s (the pout and the dead air),
# s28 from 1.9 s (the fan's writing), s33 to 7.0 s (the hat wing after the line). x264 crf 12, aac 32 kHz; assemble-v4's
# pick() takes the highest -tN, so the -t1 files stay as they were. Made again if missing.
C=$E/clips
[ -f $C/s02-t2.mp4 ]  || ffmpeg -v error -y -i $C/s02-t1.mp4  -t 4.4  -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s02-t2.mp4
[ -f $C/s13b-t2.mp4 ] || ffmpeg -v error -y -i $C/s13b-t1.mp4 -t 4.9  -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s13b-t2.mp4
[ -f $C/s28-t2.mp4 ]  || ffmpeg -v error -y -i $C/s28-t1.mp4  -ss 1.9 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s28-t2.mp4
[ -f $C/s33-t2.mp4 ]  || ffmpeg -v error -y -i $C/s33-t1.mp4  -t 7.0  -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s33-t2.mp4
# the episode sfx dir (third sfx_dirs entry): bead902.wav = one bead click out of zhongtian-sfx-abacus-drop-01 (0.245-0.325 s,
# fade out 0.04, +14 dB to about -3 dBFS peak) for the last bead in s32 (the old impactWood_light_000 there was -37 dB)
S=/root/mokaair-work/videos/zhong-tian-qu-qi-e902-dh/sfx; X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; mkdir -p $S
[ -f $S/bead902.wav ] || ffmpeg -v error -y -ss 0.245 -t 0.08 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.003,afade=t=out:st=0.04:d=0.04,volume=14dB,aresample=48000,aformat=channel_layouts=stereo" $S/bead902.wav
# SWAP 2026-11-21: chain902.wav = the first rattle peak of zhongtian-sfx-iron-chain-01 (0.32-0.82 s, peak 0.08 s in, fade out
# 0.3/0.2) for the rings landing in the dirt in the new s01 (c2.08)
[ -f $S/chain902.wav ] || ffmpeg -v error -y -ss 0.32 -t 0.5 -i $X/zhongtian-sfx-iron-chain-01.wav -af "afade=t=in:d=0.005,afade=t=out:st=0.3:d=0.2,aresample=48000,aformat=channel_layouts=stereo" $S/chain902.wav
# $VL = video.json (left as it is) plus s01i after s01 (SWAP 2026-11-21, fix-polish/round3): the insert of A-ling's right wrist,
# the red band and the pale old scar (the answer to episode 1's hook), her left hand pulling the sleeve over them; no line, so
# assemble-v4 cuts it at its clip's length (clips/s01i-t5.mp4, 4.458 s) and mutes the clip's own sound; music and effects
# are placed on shot starts, so everything after s01 moves with it
VL=$E/video-live.json; DROP=""
python3 -c "
import json
v=json.load(open('$VJ')); d='$DROP'.split()
v['scenes']=[s for s in v['scenes'] if s.get('id') not in d]
i=[s['id'] for s in v['scenes']].index('s01')
v['scenes'].insert(i+1,{'id':'s01i','template':'shot','action_seconds':4.458,'lines':[],'data':{'camera':'Insert extreme close-up from directly above, fixed camera','prompt':'the right wrist of A-ling palm up in her grey-white cotton sleeve, a red pressure band from the iron ring and one thin pale old scar under it, dappled near-noon light on the dirt','motion':'still for a second, then her left hand pulls the grey-white sleeve down over the band and the scar and holds it there','characters':['aling'],'source_note':'fix-polish/round3 s01i 9029302 end-before@4.458'}})
json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e002-r2/overlays.json $P/hailuo/edit-dh-e902-live.json $E $E/cut/e902-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e902-live.mp4 ] || exit 1
# the e901 / e908-e930 finish: a sample-peak limiter (attack 8 ms, limit 0.55), then loudnorm2.sh (linear, -14 LUFS, TP -2.2).
# The first cut (2026-11-09) had neither.
ffmpeg -v error -y -i $E/cut/e902-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000" $E/cut/e902-live.lim.mp4 && mv $E/cut/e902-live.lim.mp4 $E/cut/e902-live.mp4
ffmpeg -hide_banner -i $E/cut/e902-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e902-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e902-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
