#!/usr/bin/env bash
set -u
R=/home/user/zt-work; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e917/zhong-tian-qu-qi-e917-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e017-r2/video.json
# POLISH+SWAP 2026-11-21: the 2026-11-16 cut files (lines.json, srt, final.log; its mp4 is review-zt/ep/e017/final.mp4) go to
# cut/old-1116 once and carry a .keep (never removed); a later run replaces its own previous cut (no old-HHMM).
mkdir -p $E/cut
[ -d $E/cut/old-1116 ] || { mkdir -p $E/cut/old-1116; mv $E/cut/e917-live.* $E/cut/final.log $E/cut/old-1116/ 2>/dev/null; touch $E/cut/old-1116/.keep; }
rm -f $E/cut/e917-live.* $E/cut/final.log; rm -rf $E/cut/pre
rm -rf $E/segments-v4
# the refined shots must be staged first (live-action/stage.py 17; the refine sources are not on this machine, so the script
# no longer re-stages by itself -- it stops and says so)
miss=$(python3 -c "import json,os;p=json.load(open('$E/picks.json'));print(' '.join(s for s in p if not os.path.exists('$E/clips/'+s+'-t1.mp4')))")
[ -z "$miss" ] || { echo "not staged: $miss -- run: python3 $P/live-action/stage.py 17"; exit 1; }
# e917 trims and seeds the edit table assumes (edit-dh-e917-live.json _note): picks.json as refine-prep.py 17 builds it from
# picks-merged.tsv, fix1/review-picks.tsv, fix2/review-picks.tsv and review3-trims.tsv in that order (run in
# colab/runs/e917-live) -- the fix1 retakes s17 s21 (9171202) and the fix2 retake s13 (9171301, A-ling's loose hair; the
# earlier refine is kept as runpod/a/st2/refined/s13-9171202.mp4). The first cut had no review3-trims.tsv; REVIEW 3
# (review3-plan.md, both cut reviews) trims s09 s11 s16 s20 s21 s25 s28 s39, each checked with faster-whisper and 50 ms
# RMS on the restaged clip (no word cut). After any change: refine-prep.py 17 ... review3-trims.tsv, stage.py 17, this table. Whole frames: a start rounded DOWN and an
# end-before rounded UP to 3 decimals, tolerance 0.001 (e912 review 3: -ss keeps a frame at/after start, -to drops a frame
# whose end passes it); 0 = no end. Warn (not stop) if picks.json differs.
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.75,4.5),'s02':(0,5.917),'s03':(0.75,5),'s04':(0.75,5),'s05':(0.375,8),'s06':(0.5,4.5),'s07':(0,5.75),
 's08':(1.25,7.5),'s09':(2,5.5),'s10':(0.5,4.5),'s11':(0,4),'s12':(0.75,6.584),'s13':(0.75,5.625),'s14':(0,3.5),
 's15':(0.5,5.5),'s16':(0,6),'s17':(0,6.584),'s18':(0.25,6.584),'s19':(0.375,6.25),'s20':(1,6.584),'s21':(0,3.5),
 's22':(0,6),'s23':(0.75,5.5),'s24':(0,4.5),'s25':(0.5,7.625),'s26':(0.25,8),'s27':(0,5.75),'s28':(0.5,7.5),'s29':(0,6.584),
 's30':(0.5,6.584),'s31':(0.5,5.25),'s32':(0.375,6.584),'s33':(2.75,6.584),'s34':(0.5,6.334),'s35':(0,8),'s36':(0,6.584),
 's37':(0,6.584),'s38':(0,4.5),'s39':(0,9.25),'s40':(0.25,6.584)}
seed={'s02':9171102,'s03':9171102,'s11':9171102,'s13':9171301,'s14':9171102,'s16':9171102,'s17':9171202,'s18':9171102,
 's19':9171102,'s20':9171102,'s21':9171202,'s22':9171102,'s23':9171102,'s24':9171102,'s27':9171102,'s29':9171102,
 's32':9171102,'s36':9171102,'s38':9171102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9171101)' for s in p if s not in seed and p[s]['seed']!=9171101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# POLISH+SWAP 2026-11-21 (edit table _note). SWAP: clips/s02 s06 s14 s18 s25 s39 s40-t5.mp4 (runpod/polish/picks.json, already
# trimmed: s02 9179201 1.958-6.417, s06 9179101 0.375-5.042, s14 9179101 whole, s18 9179102 0.166-, s25 9179202 1.375-7.958,
# s39 9179201 whole 10.11 s, s40 9179101 whole 6.56 s) win over t1; picks.json and the want table above describe the t1 staging.
# Clips cut here (the assembler takes the highest take number; remade when missing):
#  s14-t6 = t5's first 4.0 s (96 frames; the held arm has dropped out of frame by c3.6, the rest is a slow push-in);
#  s01-t2 = t1 from c1.9 at 1.18x (free fix: Xu already running on the jetty; no line, the clip audio is muted anyway);
#  s16-t2 = t1 to 5.417 (130 frames; free fix: the crying face after the eye-wipe held 0.6 s less; his voice ends c3.97).
C=$E/clips; X264="-c:v libx264 -crf 14 -preset slow -pix_fmt yuv420p -c:a aac -b:a 192k"
[ -f $C/s14-t6.mp4 ] || ffmpeg -v error -y -i $C/s14-t5.mp4 -frames:v 96 -t 4.0 $X264 $C/s14-t6.mp4
[ -f $C/s01-t2.mp4 ] || ffmpeg -v error -y -ss 1.9 -i $C/s01-t1.mp4 -vf "setpts=(PTS-STARTPTS)/1.18,fps=24" -af atempo=1.18 $X264 $C/s01-t2.mp4
[ -f $C/s16-t2.mp4 ] || ffmpeg -v error -y -i $C/s16-t1.mp4 -frames:v 130 -t 5.417 $X264 $C/s16-t2.mp4
# recordings rebuilt on the takes' phrase onsets (the REVIEW 3 files kept as audio/orig/zq917a01-r3.wav, zq917a28-r3.wav):
#  a01 (s02, voice_off): 0.53 s of silence before its second phrase so 三張都掛在架子上 opens with his second mouth opening (c2.6);
#  a28 (s30, now voice_off): five phrases moved onto the take's five mouth openings c0.30 / 1.46 / 2.92 / 4.04 / 5.28, so 坊 is whole
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e917-dh/audio
[ -f $A/orig/zq917a01-r3.wav ] && [ $A/zq917a01.wav -nt $A/orig/zq917a01-r3.wav ] || ffmpeg -v error -y -i $A/orig/zq917a01-r3.wav -filter_complex "[0:a]asplit=2[a][b];[a]atrim=0:1.46,asetpts=PTS-STARTPTS[p1];[b]atrim=1.46,asetpts=PTS-STARTPTS,adelay=530:all=1[p2];[p1][p2]concat=n=2:v=0:a=1" $A/zq917a01.wav
[ -f $A/orig/zq917a28-r3.wav ] && [ $A/zq917a28.wav -nt $A/orig/zq917a28-r3.wav ] || ffmpeg -v error -y -i $A/orig/zq917a28-r3.wav -filter_complex "[0:a]asplit=5[a][b][c][d][e];[a]atrim=0.20:0.76,asetpts=PTS-STARTPTS,afade=t=out:st=0.52:d=0.04[p1];[b]atrim=0.76:1.58,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=0.78:d=0.04,adelay=1160:all=1[p2];[c]atrim=1.84:2.42,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=0.54:d=0.04,adelay=2620:all=1[p3];[d]atrim=2.78:3.40,asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st=0.59:d=0.03,adelay=3740:all=1[p4];[e]atrim=3.40:4.10,asetpts=PTS-STARTPTS,afade=t=in:d=0.01,adelay=4980:all=1[p5];[p1][p2][p3][p4][p5]amix=inputs=5:normalize=0:duration=longest" $A/zq917a28.wav
# the episode sfx dir (third sfx_dirs entry): murmur17 (crowd-murmur.py 17 30, the owner's reversed-recordings crowd, -19 LUFS)
# under s06-s10; wring917 = zhongtian-sfx-wring-cloth-01 2.85-4.45 s (one twist and the drip) for s03's wet cloth
S=/root/mokaair-work/videos/zhong-tian-qu-qi-e917-dh/sfx; XS=/root/mokaair-work/videos/_sfx/zhongtian-real-20261121; mkdir -p $S
[ -f $S/murmur17.wav ] || python3 -I $Q/crowd-murmur.py 17 30
[ -f $S/wring917.wav ] || ffmpeg -v error -y -ss 2.85 -t 1.6 -i $XS/zhongtian-sfx-wring-cloth-01.wav -af "afade=t=in:d=0.03,afade=t=out:st=1.3:d=0.3,aresample=48000,aformat=channel_layouts=stereo" $S/wring917.wav
# no shot is deleted (the e916 video-live.json step is not needed): the cut, audio-qa and the sheets read video.json itself
# no vidstab: cut-qa's jitter() on every staged clip reads 0.00 (s11 0.07, s12 0.03, s29 0.01), nothing hops frame to frame
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e017-r2/overlays.json $P/hailuo/edit-dh-e917-live.json $E $E/cut/e917-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e917-live.mp4 ] || exit 1
# a sample-peak limiter before loudnorm2 keeps it linear (e908-e912: attack 5 ms, limit 0.6 = -4.4 dBFS; the AAC encode
# after it overshoots at shorter attacks and loudnorm2 then goes dynamic and clicks). e913 REVIEW 3 on: attack 8 ms.
# END (POLISH+SWAP): the s40 retake lifts the lantern from his chest to his face by c5.5: the gong at c5.6, the picture fades
# c5.70-6.25 and min 9.333 keeps the old 3.1 s of black after it (the sound fade as below)
# END (REVIEW 3): s40 is Xu's inner line a40 (a recording); the picture fades over c4.50-5.05 (vf fade=t=out:st=4.500:d=0.55) and min
# 8.0 holds about 2.95 s of black (REVIEW 3; it was 6.55 and 1.5 s, and the fade cut the gong 1.8 s after its hit), so the
# gong laid at c4.25 (gong_02 + impactSoft_heavy_000) and the tension cue ring out in the dark. The sound fades over the
# last 1.5 s.
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e917-live.mp4); FS=$(python3 -c "print(f'{$D-1.5:.3f}')")
ffmpeg -v error -y -i $E/cut/e917-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.6:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.5" $E/cut/e917-live.lim.mp4 && mv $E/cut/e917-live.lim.mp4 $E/cut/e917-live.mp4
# loudnorm2 is linear only when the measured true peak plus the gain to -14 LUFS stays at or under -2.2 dBTP: print it
ffmpeg -hide_banner -i $E/cut/e917-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e917-live.mp4
# POLISH+SWAP 2026-11-21 (e912 lesson): the true peak after loudnorm2; above -1.5 dBTP a second sample-peak limiter at 0.7 touches
# just those peaks; the delivery wants <= -1 dBTP: printed on the final file
TP=$(ffmpeg -hide_banner -nostats -i $E/cut/e917-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -A1 'True peak:' | grep -oE -- '-?[0-9.]+ dBFS' | tail -1 | cut -d' ' -f1)
echo "after loudnorm2: true peak $TP dBTP"
if python3 -c "import sys;sys.exit(0 if float('$TP')>-1.5 else 1)"; then
 ffmpeg -v error -y -i $E/cut/e917-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.7:attack=8:release=60:level=false,aresample=48000" $E/cut/e917-live.lim.mp4 && mv $E/cut/e917-live.lim.mp4 $E/cut/e917-live.mp4
 echo "second limiter applied"
fi
ffmpeg -hide_banner -nostats -i $E/cut/e917-live.mp4 -map 0:a -af ebur128=peak=true -f null - 2>&1 | grep -E '^\s+(I|LRA|Peak):' | tail -3 \
 | awk '{print} /Peak:/{print ($2<=-1.0)?"true peak ok (<= -1 dBTP)":"TRUE PEAK OVER -1 dBTP"}'
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e917-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
# the segments are 1-2 GB and only the assembler reads them: gone after the checks (KEEP_SEG=1 keeps them for a look)
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
