#!/usr/bin/env bash
# e934 成片（真人版第一版）：照 e933cut.sh。剪接表 hailuo/edit-dh-e934-live.json 由 scratchpad e934c/（mkov934.py＋music／beds／spots／vol.json → overrides.json，
# mkedit934.py＋note.txt → 剪接表）產生；所有決定與量測寫在剪接表的 _note。本腳本不花錢：不用 Colab、RunPod、站台 TTS，不重做精修。
set -u
R=/home/user/travel_scanner; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e934/zhong-tian-qu-qi-e934-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e034-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e934-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e934-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# 精修片由 live-action/stage.py 34 放好（精修畫面＋草稿原聲＋剪點 -> clips/sNN-t1.mp4；s09 s37 是 fix1、s28 s32 是 fix1 備案 9341212／9341211，
# fix2 兩輪都不如 fix1，見 colab/runs/e934-live/fix2/plan.md）；缺片或 picks.json 比片新（重跑過 refine-prep.py 34）就重跑。
# stage.py 把 $E/audio、$E/music 連到 zhong-tian-qu-qi-e934-dh/audio、music；music/ 是一個目錄（e934 第一版手做，照 e933）：
# _series/zhong-tian-qu-qi/music 的 cue-*.mp3 各一個連結，cue-drone31／tension31.mp3 -> assets/music/e031-e032/cue-suspense／tension.mp3，
# cue-standoff／farming-montage／face-slap／sweet-romance／scheming／festival.mp3 -> _series/.../music/flow-music-20261118/zhongtian-bed-<名>-take1.m4a，
# cue-cliffhanger／reveal-hit.mp3 -> .../zhongtian-cue-<名>-take1.m4a（Flow Music 庫，ffmpeg 照內容讀，副檔名不影響）。
# 沒有片段帶 crop（s24 水平翻轉、s40 壓暗調灰與淡出都是剪接表的 vf）。
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 34 || exit 1; }
[ -d /root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/music ] || { echo "zhong-tian-qu-qi-e934-dh/music/ 不在（見上面的說明）"; exit 1; }
# 本集自己的音效（剪接表 sfx_dirs 第二個目錄 $E/sfx-local/），從放好的片子切：沒有台詞（s24 s26）、台詞是畫外錄音（s03 s23 s40）、
# 或片中原聲因音高整支靜音（s12 s25）的鏡，片中的環境聲照例跟著靜音，切出來放回去：
#   pin-s03（s03 整支 8 秒，風車呼呼轉與風）、water-s12（s12 c4.0 起，葉板推進水裡）、water-s23（s23 整支，水衝葉板）、
#   water-s24（s24 整支，輪頂瀉水）、water-s26（s26 整支，水頭與跑步）、buzz-s40（s40 整支嗡聲）、
#   buzzloop（s40 c1.5–6.5 的嗡聲接成 18 秒，交叉淡化 0.5 秒，s37–s40 漸大的鋪底）、
#   laugh-s25（石木匠 c0.40–2.30 的大笑，降調 asetrate 0.62、長度不變：片中 278 Hz -> 約 172，接得上錄音 a25 的 153）。
# 片子重放過或檔不在就重切。
L=$E/sfx-local; C=$E/clips; mkdir -p $L
cutw(){ [ $L/$1.wav -nt $C/$2-t1.mp4 ] || ffmpeg -nostdin -v error -y ${3:+-ss $3} ${4:+-to $4} -i $C/$2-t1.mp4 -vn -ac 2 -ar 48000 ${5:+-af $5} $L/$1.wav || exit 1; }
cutw pin-s03 s03; cutw water-s12 s12 4.0 "" "afade=t=in:d=0.2"; cutw water-s23 s23; cutw water-s24 s24; cutw water-s26 s26; cutw buzz-s40 s40
cutw laugh-s25 s25 0.40 2.30 "asetrate=29760,aresample=48000,atempo=1.612903,afade=t=out:st=1.7:d=0.2"
[ $L/buzzloop.wav -nt $C/s40-t1.mp4 ] || { ffmpeg -nostdin -v error -y -ss 1.5 -to 6.5 -i $C/s40-t1.mp4 -vn -ac 2 -ar 48000 $L/_b.wav && \
  ffmpeg -nostdin -v error -y -i $L/_b.wav -i $L/_b.wav -i $L/_b.wav -i $L/_b.wav -filter_complex "[0][1]acrossfade=d=0.5[x];[x][2]acrossfade=d=0.5[y];[y][3]acrossfade=d=0.5" $L/buzzloop.wav && rm -f $L/_b.wav; } || exit 1
# 剪接表假設的剪點與種子（picks.json 由 colab/runs/e934-live 的 refine-prep.py 34 picks-merged.tsv fix1/review-picks.tsv
# fix2/review-picks.tsv cut-trims.tsv 產生；印出的 refine 沒跑）。cut-trims.tsv 是第一版剪接改的剪點：s08 終點 10.125→7.5。
# 整格：起點往下、終點往上取到小數三位，容差 0.001；只警告不停。
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.0,4.0),'s02':(1.5,6.583),'s03':(0.0,8.0),'s04':(0.75,6.25),'s05':(1.875,8.0),'s06':(1.0,6.583),'s07':(3.5,8.0),'s08':(0.0,7.5),'s09':(0.0,8.0),'s10':(2.25,6.583),'s11':(0.208,6.583),'s12':(0.125,6.583),'s13':(1.208,8.0),'s14':(0.0,6.375),'s15':(1.5,8.0),'s16':(2.0,6.583),'s17':(1.5,8.0),'s18':(0.542,6.583),'s19':(2.333,6.583),'s20':(0.75,6.583),'s21':(1.0,8.0),'s22':(0.458,6.583),'s23':(0.0,6.583),'s24':(0.0,5.167),'s25':(0.0,8.0),'s26':(2.75,5.167),'s27':(0.25,8.0),'s28':(0.875,8.0),'s29':(0.25,6.5),'s30':(1.875,8.0),'s31':(1.25,6.583),'s32':(0.0,7.5),'s33':(0.0,10.125),'s34':(0.292,6.583),'s35':(2.0,6.583),'s36':(2.0,6.583),'s37':(0.583,6.583),'s38':(1.0,6.25),'s39':(1.25,8.0),'s40':(0.0,6.75)}
seed={'s01':9341102,'s07':9341102,'s08':9341102,'s09':9341211,'s12':9341102,'s13':9341102,'s14':9341102,'s20':9341102,'s21':9341102,'s24':9341102,'s25':9341102,'s27':9341102,'s28':9341212,'s30':9341102,'s32':9341211,'s34':9341102,'s35':9341102,'s36':9341102,'s37':9341211,'s39':9341102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9341101)' for s in p if s not in seed and p[s]['seed']!=9341101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (none may)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# 剪接表鋪的錄音在 audio/ 改寫過（原檔在 audio/orig/；_note〈錄音〉）：整平到 −13.5 LUFS 的 a02（重錄版）a08 a10 a12 a13 a33、
# a17（重錄版，rubberband 1.42）、a19（重錄版，rubberband 1.10）、a20（來源 a20-p85）、a24（來源 a24-p119）、
# a25（rubberband 1.31＋atempo 1.15）、a40（asetrate 0.86），系統 a07 a09 a32 到 −13.8。少了改寫就停。
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e934-dh/audio
for n in 02 07 08 09 10 12 13 17 19 20 24 25 32 33 40; do [ -f $A/orig/zq934a$n.wav ] || { echo "audio/zq934a$n.wav is not the leveled file (no orig/ copy)"; exit 1; }; done
# e934 沒有拿掉的鏡（DROP 空，40 鏡全用）；$VL 是 video.json 去掉 DROP 的鏡。
VL=$E/video-live.json; DROP=""
python3 -c "import json,sys;v=json.load(open('$VJ'));d='$DROP'.split();v['scenes']=[s for s in v['scenes'] if s.get('id') not in d];json.dump(v,open('$VL','w'),ensure_ascii=False,indent=1)"
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos nice node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e034-r2/overlays.json $P/hailuo/edit-dh-e934-live.json $E $E/cut/e934-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e934-live.mp4 ] || exit 1
# loudnorm2 之前的取樣峰值限制器（e923 起 limit 0.55、attack 8 ms），聲音最後 1.0 秒淡出（結尾 s40 淡出後的黑畫面）。
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e934-live.mp4); FS=$(python3 -c "print(f'{$D-1.0:.3f}')")
ffmpeg -v error -y -i $E/cut/e934-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=1.0" $E/cut/e934-live.lim.mp4 && mv $E/cut/e934-live.lim.mp4 $E/cut/e934-live.mp4
ffmpeg -hide_banner -i $E/cut/e934-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e934-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e934-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
