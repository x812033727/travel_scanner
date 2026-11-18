#!/usr/bin/env bash
# e932 成片（真人版第一版）：照 e931cut.sh。剪接表 hailuo/edit-dh-e932-live.json 由 scratchpad e932c/（mkov932.py → overrides.json，
# mkedit932.py＋note.txt → 剪接表）產生；所有決定與量測寫在剪接表的 _note。本腳本不花錢：不用 Colab、RunPod、站台 TTS，不重做精修。
set -u
R=/home/user/travel_scanner; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e932/zhong-tian-qu-qi-e932-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e032-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e932-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e932-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# 精修片由 live-action/stage.py 32 放好（精修畫面＋草稿原聲＋剪點 -> clips/sNN-t1.mp4；s01 是 fix2 9321301、s19／s25 是 fix1 9321202、s21／s26／s26b 是 fix3 9321401／9321403／9321405 的精修）；
# 缺片或 picks.json 比片新（重跑過 refine-prep.py 32）就重跑。stage.py 把 $E/audio、$E/music 連到 zhong-tian-qu-qi-e932-dh/audio、music；
# music/ 是一個目錄（e932 第一版手做，同 e931）：_series/zhong-tian-qu-qi/music 的 cue-*.mp3 各一個連結，另 cue-drone31.mp3 ->
# assets/music/e031-e032/cue-suspense.mp3、cue-tension31.mp3 -> …/cue-tension.mp3、cue-comedy31.mp3 -> …/cue-comedy.mp3（第 31–32 集舊版配樂）。
# 沒有片段帶 crop（s05 s08 s13 s29 的靜態裁切、s24 耳緣提紅、s37 淡出都是剪接表的 vf）。
# REVIEW 3 的畫面修改也都是剪接表的 vf：s36 門口兩人的移動虛焦框、s33／s36 調暗調暖、s24 提紅 rs 0.28、s14 的金色泥降飽和壓暗
# （遮罩在 960×540 算，maskedmerge）。s21 s26 s26b 的金色泥遮罩在 FIX3 拿掉（重拍片的泥已是深褐；s21 整鏡均勻調暖）。
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 32 || exit 1; }
# s26／s26b 的 vf 是兩段式 vidstab（被扛著的近景逐格晃，cut-qa jitter 0.16／0.17）：第一段的轉換檔放在 $E/stab/，片子重放過或檔不在就重算
# （放大到 1920×1080 之後算，跟組片程式套 vf 的畫面一樣）。
mkdir -p $E/stab; for s in s26 s26b; do [ -f $E/stab/$s.trf ] && [ $E/stab/$s.trf -nt $E/clips/$s-t1.mp4 ] || ffmpeg -nostdin -v error -y -i $E/clips/$s-t1.mp4 -vf "scale=1920:1080:flags=lanczos,vidstabdetect=shakiness=6:accuracy=15:result=$E/stab/$s.trf" -f null - || exit 1; done
[ -d /root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/music ] || { echo "zhong-tian-qu-qi-e932-dh/music/ 不在（見上面的說明）"; exit 1; }
# 剪接表假設的剪點與種子（picks.json 由 colab/runs/e932-live 的 refine-prep.py 32 picks-merged.tsv fix1/review-picks.tsv
# fix2/review-picks.tsv review3-trims.tsv fix3/review-picks.tsv 產生；fix1 換 s19 s25 為 9321202（s01 的 fix1 9321202 不用），fix2 換 s01 為 9321301）。
# REVIEW 3（review3-plan.md）改了 8 鏡的剪點：s01 起點 0→1.0、s05 0→1.0、s30 1.0→3.0（剪掉鋤頭穿臉），s25 終點 6.0→5.5、s25b 6.583→6.0、
# s26 8.0→6.5、s26b 6.583→5.833、s32 6.583→6.208；種子不變。
# FIX3 MUD RETAKE（review3-plan.md〈fix3 泥重拍〉，fix3/review-picks.tsv 排在 review3-trims.tsv 之後）：s21 換 9321401（0.375–7.875，
# 同長 7.5 秒；原聲 0.48 硬起，0.500 會切字）、s26 換 9321403（0–6.5）、s26b 換 9321405（0–5.833）；三鏡的金色泥遮罩拿掉。
# 整格：起點往下、終點往上取到小數三位，容差 0.001；只警告不停。
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.0,5.0),'s02':(1.0,6.542),'s03':(1.5,6.583),'s04':(1.0,6.583),'s05':(1.0,8.0),'s06':(2.583,6.542),'s07':(1.0,7.375),'s08':(1.75,6.583),'s09':(0.583,6.542),'s10':(1.5,7.25),'s11':(1.083,7.125),'s12':(1.0,6.583),'s13':(1.0,8.0),'s14':(1.0,6.5),'s15':(0.375,6.583),'s16':(1.667,3.75),'s17':(1.5,6.583),'s18':(0.667,6.5),'s19':(0.25,5.0),'s20':(0.5,3.5),'s21':(0.375,7.875),'s22':(1.25,6.583),'s23':(0.375,3.625),'s24':(0.5,4.875),'s25':(0.0,5.5),'s25b':(0.0,6.0),'s26':(0.0,6.5),'s26b':(0.0,5.833),'s27':(1.5,8.0),'s28':(1.75,8.0),'s29':(0.5,6.583),'s30':(3.0,6.583),'s31':(1.5,6.583),'s32':(0.0,6.208),'s33':(1.75,7.583),'s34':(0.0,7.667),'s35':(0.5,10.125),'s36':(1.0,7.917),'s37':(0.0,4.5)}
seed={'s01':9321301,'s04':9321102,'s05':9321102,'s06':9321102,'s14':9321102,'s16':9321102,'s19':9321202,'s21':9321401,'s25':9321202,'s25b':9321102,'s26':9321403,'s26b':9321405,'s28':9321102,'s34':9321102,'s36':9321102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9321101)' for s in p if s not in seed and p[s]['seed']!=9321101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (none may)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# 剪接表鋪的錄音在 audio/ 改寫過（原檔在 audio/orig/；_note〈錄音〉）：a22 a23 a25（系統）、a24（心裡話，另升 ×1.15）、a26（心裡話）、
# a32（畫外，重錄版）整平到 −13.5 LUFS。少了改寫就停。
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e932-dh/audio
for n in 22 23 24 25 26 32; do [ -f $A/orig/zq932a$n.wav ] || { echo "audio/zq932a$n.wav is not the leveled file (no orig/ copy)"; exit 1; }; done
# e932 沒有拿掉的鏡（DROP 空，39 鏡全用）；$VL 是 video.json 去掉 DROP 的鏡。
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e032-r2/overlays.json $P/hailuo/edit-dh-e932-live.json $E $E/cut/e932-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e932-live.mp4 ] || exit 1
# loudnorm2 之前的取樣峰值限制器（e923 起 limit 0.55、attack 8 ms），聲音最後 1.0 秒淡出（結尾 s37 淡出後的黑畫面）。
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e932-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e932-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e932-live.lim.mp4 && mv $E/cut/e932-live.lim.mp4 $E/cut/e932-live.mp4
ffmpeg -hide_banner -i $E/cut/e932-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e932-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e932-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
