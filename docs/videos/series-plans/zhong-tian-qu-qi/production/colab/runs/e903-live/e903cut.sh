#!/usr/bin/env bash
# e903cut.sh: the episode-3 live-action cut (written 2026-11-21 for the review-zt polish, the e901cut.sh / e902cut.sh way;
# episode 3 had been cut by hand on 2026-11-09 with the same assemble-v4 call and no script).
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e903/zhong-tian-qu-qi-e903-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e003-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e903-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e903-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# clips/sNN-t1.mp4 are the staged live clips as they came back from the Drive backup (picks.json, fix1-fix4 in
# colab/runs/e903-live, already trimmed and cropped); $E/audio and $E/music are links to zhong-tian-qu-qi-e903-dh/audio
# and /music. Nothing is dropped.
# POLISH 2026-11-21 (review-zt free fixes; edit table _note POLISH): four shots re-trimmed without stage.py (the refined
# pictures are not on this disk), times in the staged clip: s01 to 2.2 s (cut once the knife has stopped quivering),
# s02 from 1.5 s (Qin Shuang's walk-in and reach; she speaks at 1.63 and to the clip's end), s03 0.292-2.917 s (7 and 70
# frames: the sleeve yank; Xiao He has not started to run, so her run-off and its footstep are cut) so s04 comes in at 9.92 s (RULES 6: four shots
# in the first 10 s from episode 3 on; the review's s02 from 1.0 and s03 0.3-4.6 put s04 at 12.13 s); s09 from 1.0 s
# (the villagers standing inside the yard; he speaks at 1.98). x264 crf 12, aac 32 kHz; assemble-v4's pick() takes the
# highest -tN, so the -t1 files stay as they were. Made again if missing.
# SWAP 2026-11-22 (second wave, fix-polish/round4): clips/s06-t5.mp4 (seed 9039402, start@0 end-before@6.583, picked
# whole) overrides s06-t1; no t6 was ever cut for s06, nothing to redo. The delivered cut is moved to cut/old-HHMM and
# marked .keep by hand.
C=$E/clips
[ -f $C/s01-t2.mp4 ] || ffmpeg -v error -y -i $C/s01-t1.mp4 -t 2.2 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s01-t2.mp4
[ -f $C/s02-t2.mp4 ] || ffmpeg -v error -y -i $C/s02-t1.mp4 -ss 1.5 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s02-t2.mp4
[ -f $C/s03-t2.mp4 ] || ffmpeg -v error -y -i $C/s03-t1.mp4 -ss 0.292 -t 2.625 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s03-t2.mp4
[ -f $C/s09-t2.mp4 ] || ffmpeg -v error -y -i $C/s09-t1.mp4 -ss 1.0 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s09-t2.mp4
# the episode sfx dir (third sfx_dirs entry): abacus903.wav = zhongtian-sfx-abacus-drop-01 0.15-1.35 s (the beads' rattle,
# fades 0.02/0.3; the set has no abacus, this is the e910 stand-in) for s10 and s24 in place of handleCoins (coins);
# murmur03.wav = crowd-murmur.py 3 3.2 (the villagers at the fence in s10, this episode's recordings reversed, -19 LUFS)
S=/root/mokaair-work/videos/zhong-tian-qu-qi-e903-dh/sfx; X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; mkdir -p $S
[ -f $S/abacus903.wav ] || ffmpeg -v error -y -ss 0.15 -t 1.2 -i $X/zhongtian-sfx-abacus-drop-01.wav -af "afade=t=in:d=0.02,afade=t=out:st=0.9:d=0.3,aresample=48000,aformat=channel_layouts=stereo" $S/abacus903.wav
[ -f $S/murmur03.wav ] || python3 -I $Q/crowd-murmur.py 3 3.2
# GAP SFX 2026-11-22 (review-zt/GAP-BRIEF.md, gap-20261122/README.md; set manifest 2740ddbb...): brush903.wav =
# zhongtian-sfx-brush-writing-03 0-2.05 s (the bristle strokes before the loud tap at 2.1, fades 0.05/0.3) for s13's brush
# on the paper c0.8-2.9 in place of paper_03; bucket903.wav = zhongtian-sfx-water-bucket-loop 0.78-1.28 s (one slosh and its
# decay, fades 0.02/0.15) for s26 in place of splash_02. s31's door is zhongtian-sfx-old-door-03 straight from the set.
[ -f $S/brush903.wav ] || ffmpeg -v error -y -t 2.05 -i $X/zhongtian-sfx-brush-writing-03.wav -af "afade=t=in:d=0.05,afade=t=out:st=1.75:d=0.3,aresample=48000,aformat=channel_layouts=stereo" $S/brush903.wav
[ -f $S/bucket903.wav ] || ffmpeg -v error -y -ss 0.78 -t 0.5 -i $X/zhongtian-sfx-water-bucket-loop.wav -af "afade=t=in:d=0.02,afade=t=out:st=0.35:d=0.15,aresample=48000,aformat=channel_layouts=stereo" $S/bucket903.wav
# s31's laid line zq903a28 (Xu Yan from behind, -21 dB in the cut against A-Ling's -13 after it) is 3 LU louder:
# audio/zq903a28.wav is rewritten from audio/orig/zq903a28.wav with a compressor's makeup and a limiter (the e910 way: a
# plain volume would clip, the recording peaks at 0 dBFS, and the final limiter would eat it); -17.8 -> -14.6 LUFS, peak -1.0.
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e903-dh/audio; mkdir -p $A/orig
[ -f $A/orig/zq903a28.wav ] || { cp -p $A/zq903a28.wav $A/orig/zq903a28.wav && ffmpeg -v error -y -i $A/orig/zq903a28.wav -af "acompressor=threshold=0.125:ratio=4:attack=5:release=80:makeup=2.7,alimiter=limit=0.89:level=false" -c:a pcm_s16le $A/zq903a28.wav; }
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e003-r2/overlays.json $P/hailuo/edit-dh-e903-live.json $E $E/cut/e903-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e903-live.mp4 ] || exit 1
# the e901 / e908-e930 finish: a sample-peak limiter (attack 8 ms), then loudnorm2.sh (linear, -14 LUFS, TP -2.2). Limit 0.53,
# not 0.55: at 0.55 the polished cut measured -2.17 dBTP after the gain and loudnorm2 went dynamic.
# The first cut (2026-11-09) had neither. SWAP 2026-11-22: 0.53 -> 0.51, with the Flow beds 0.53 measured -2.04 dBTP after
# the gain (loudnorm2 dynamic).
ffmpeg -v error -y -i $E/cut/e903-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.51:attack=8:release=60:level=false,aresample=48000" $E/cut/e903-live.lim.mp4 && mv $E/cut/e903-live.lim.mp4 $E/cut/e903-live.mp4
ffmpeg -hide_banner -i $E/cut/e903-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e903-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e903-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
