#!/usr/bin/env bash
# e931 第一版成片（真人版）：照 e930cut.sh。剪接表 hailuo/edit-dh-e931-live.json 由 scratchpad e931c/（mkov931.py → overrides.json，
# mkedit931.py＋note.txt → 剪接表）產生；所有決定與量測寫在剪接表的 _note。不花錢：不用 Colab、RunPod、站台 TTS，不重做精修。
set -u
R=/home/user/travel_scanner; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e931/zhong-tian-qu-qi-e931-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e031-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e931-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e931-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# 精修片由 live-action/stage.py 31 放好（精修畫面＋草稿原聲＋剪點 -> clips/sNN-t1.mp4）；缺片或 picks.json 比片新（重跑過
# refine-prep.py 31）就重跑。stage.py 把 $E/audio、$E/music 連到 zhong-tian-qu-qi-e931-dh/audio、music；music/ 是一個目錄
# （e931 第一版手做）：_series/zhong-tian-qu-qi/music 的 cue-*.mp3 各一個連結，另 cue-drone31.mp3 -> assets/music/e031-e032/cue-suspense.mp3
# （第 31–32 集舊版配樂裡低沉、少起音的那首，當第二場「乾、熱的低音 drone」用）、cue-tension31／cue-comedy31（備用，沒用到）。
# 沒有片段帶 crop（s13 的 1.1 倍裁切、s34／s36 的模糊框都是剪接表的 vf）。
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 31 || exit 1; }
[ -d /root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/music ] || { echo "zhong-tian-qu-qi-e931-dh/music/ 不在（見上面的說明）"; exit 1; }
# 剪接表假設的剪點與種子（picks.json 由 colab/runs/e931-live 的 refine-prep.py 31 picks-merged.tsv fix1/review-picks.tsv
# fix2/review-picks.tsv 產生；fix1 換 s06 s20 s22 s30 s31 s40，fix2 再換 s20 s40 s22）。第一版沒有改剪點（沒有 review3-trims.tsv）。
# 整格：起點往下、終點往上取到小數三位，容差 0.001；只警告不停。
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.5,6.417),'s02':(1.375,6.333),'s03':(0.583,6.5),'s04':(1.0,7.958),'s05':(0.25,5.0),'s06':(1.833,6.542),'s07':(0.0,3.5),'s08':(2.5,6.583),'s09':(2.125,6.542),'s10':(1.5,6.542),'s11':(2.167,7.833),'s12':(1.708,6.25),'s13':(0.417,6.583),'s14':(1.0,5.0),'s15':(0.25,7.5),'s16':(0.25,4.5),'s17':(1.125,6.458),'s18':(1.0,4.5),'s19':(0.5,6.75),'s20':(1.583,6.417),'s21':(0.833,4.0),'s21b':(3.167,5.167),'s22':(0.5,5.75),'s23':(1.25,6.417),'s24':(2.333,6.583),'s25':(2.042,6.083),'s26':(2.583,6.583),'s27':(1.417,6.583),'s28':(0.5,7.5),'s29':(0.0,8.0),'s29b':(0.0,5.167),'s30':(0.833,7.833),'s31':(0.5,4.5),'s32':(0.125,5.0),'s33':(0.0,6.0),'s34':(0.917,8.0),'s35':(2.292,6.25),'s36':(0.542,7.917),'s37':(2.208,7.875),'s38':(1.5,7.875),'s39':(2.5,6.417),'s40':(1.417,5.333),'s41':(0.0,3.833)}
seed={'s06':9311202,'s07':9311102,'s11':9311102,'s12':9311102,'s15':9311102,'s18':9311102,'s20':9311302,'s21b':9311102,'s22':9311301,'s23':9311102,'s24':9311102,'s25':9311102,'s30':9311201,'s31':9311201,'s32':9311102,'s38':9311102,'s40':9311302}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9311101)' for s in p if s not in seed and p[s]['seed']!=9311101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (none may)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# 剪接表鋪的錄音在 audio/ 改寫過（原檔在 audio/orig/；_note〈錄音〉）：a20/a21/a29/a44 是 -p86/-p88/-p85/-p70 調過音量，
# a18、a33 另升調。少了改寫就停。
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e931-dh/audio
for n in 05 13 14 15 16 18 20 21 25 27 28 29 30 31 33 34 44; do [ -f $A/orig/zq931a$n.wav ] || { echo "audio/zq931a$n.wav is not the leveled file (no orig/ copy)"; exit 1; }; done
# e931 沒有拿掉的鏡（DROP 空，43 鏡全用）；$VL 是 video.json 去掉 DROP 的鏡。
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e031-r2/overlays.json $P/hailuo/edit-dh-e931-live.json $E $E/cut/e931-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e931-live.mp4 ] || exit 1
# loudnorm2 之前的取樣峰值限制器（e923 起 limit 0.55、attack 8 ms），聲音最後 1.0 秒淡出（結尾 s41 的黑畫面裡鑼聲收掉）。
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e931-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e931-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e931-live.lim.mp4 && mv $E/cut/e931-live.lim.mp4 $E/cut/e931-live.mp4
ffmpeg -hide_banner -i $E/cut/e931-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e931-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e931-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
