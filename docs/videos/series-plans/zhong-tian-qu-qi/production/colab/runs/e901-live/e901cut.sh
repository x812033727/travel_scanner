#!/usr/bin/env bash
# e901cut.sh: the episode-1 live-action cut (written 2026-11-21 for the review-zt polish, the e905cut.sh / e930cut.sh way;
# episode 1 had been cut by hand on 2026-11-09 with the same assemble-v4 call and no script).
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e901/zhong-tian-qu-qi-e901-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e001-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e901-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e901-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# clips/sNN-t1.mp4 are the staged live clips as they came back from the Drive backup (picks.json, fix1-fix7 in
# colab/runs/e901-live); $E/audio and $E/music are links to zhong-tian-qu-qi-e901-dh/audio and /music. Nothing is dropped.
# POLISH 2026-11-21 (review-zt free fixes; edit table _note POLISH): s27 starts 1.5 s later without stage.py
# (clips/s27-t2.mp4 = s27-t1 from 1.5 s, x264 crf 12; assemble-v4's pick() takes the highest -tN, s27-t1 stays as it was).
C=$E/clips
[ -f $C/s27-t2.mp4 ] || ffmpeg -v error -y -i $C/s27-t1.mp4 -ss 1.5 -c:v libx264 -preset slow -crf 12 -pix_fmt yuv420p -r 24 -c:a aac -b:a 192k -ar 32000 $C/s27-t2.mp4
# the episode sfx dir (third sfx_dirs entry): rain901.wav = zhongtian-sfx-rain-thunder-01 11.0-17.4 s (the rain-only stretch,
# no thunder in it; fades 0.3/0.4) under s03; chain901.wav = zhongtian-sfx-iron-chain-01 0.1-1.1 s (one rattle at +0.15-0.4 s)
# for the sheath tapping A-Ling's chain in s26
S=/root/mokaair-work/videos/zhong-tian-qu-qi-e901-dh/sfx; X=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; mkdir -p $S
[ -f $S/rain901.wav ] || ffmpeg -v error -y -ss 11.0 -t 6.4 -i $X/zhongtian-sfx-rain-thunder-01.wav -af "afade=t=in:d=0.3,afade=t=out:st=6.0:d=0.4,aresample=48000,aformat=channel_layouts=stereo" $S/rain901.wav
# SWAP 2026-11-21 (re-shot clips s04 s08b s13 s14 s23 s28 s32 as clips/sNN-t5.mp4, picked in fix-polish/ round1-3; pick()
# takes t5 over t1): bubble901.wav = the series splash_02 low-passed twice at 650 Hz (a muffled underwater burst) for s04's
# eye snap at c0.83, under the synth underwater bed
[ -f $S/bubble901.wav ] || ffmpeg -v error -y -i /root/mokaair-work/videos/_series/zhong-tian-qu-qi/sfx/splash_02.wav -af "lowpass=f=650,lowpass=f=650,afade=t=out:st=0.45:d=0.25,aresample=48000,aformat=channel_layouts=stereo" $S/bubble901.wav
[ -f $S/chain901.wav ] || ffmpeg -v error -y -ss 0.1 -t 1.0 -i $X/zhongtian-sfx-iron-chain-01.wav -af "afade=t=in:d=0.02,afade=t=out:st=0.7:d=0.3,aresample=48000,aformat=channel_layouts=stereo" $S/chain901.wav
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e001-r2/overlays.json $P/hailuo/edit-dh-e901-live.json $E $E/cut/e901-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e901-live.mp4 ] || exit 1
# POLISH: with the music 6 dB up the assembler's own loudnorm (TP -1.5) let the true peak reach -0.9 dBTP (cut-qa wants
# <= -1.0), so the e908-e930 finish follows: a sample-peak limiter (e923 on: attack 8 ms, limit 0.55), then loudnorm2.sh
# (linear, -14 LUFS, TP -2.2). The first cut (2026-11-09) had neither; s38's end hold is the last frame, no fade (as before).
ffmpeg -v error -y -i $E/cut/e901-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000" $E/cut/e901-live.lim.mp4 && mv $E/cut/e901-live.lim.mp4 $E/cut/e901-live.mp4
ffmpeg -hide_banner -i $E/cut/e901-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e901-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e901-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
# loudnorm2.sh keeps the pre-loudnorm cut in cut/pre (the disk is short): gone too (KEEP_PRE=1 keeps it)
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
