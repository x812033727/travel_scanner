#!/usr/bin/env bash
# e937 成片（真人版第一版）：照 e936cut.sh。剪接表 hailuo/edit-dh-e937-live.json 由 scratchpad e937c/（mkov937.py＋music／beds／spots／
# lineat／vol.json → overrides.json，mkedit937.py＋note.txt → 剪接表）產生；所有決定與量測寫在剪接表的 _note 與 colab/runs/e937-live/cut-notes.md。
# 本腳本不花錢：不用 Colab、RunPod、站台 TTS，不重做精修。
set -u
R=/home/user/travel_scanner; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e937/zhong-tian-qu-qi-e937-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e037-r2/video.json
C=/tmp/claude-0/-home-user-travel-scanner/31162243-7ed2-5899-b9c2-443c1f2a5c1a/scratchpad/e937c
mkdir -p $E/cut; [ -f $E/cut/e937-live.mp4 ] && { o=$E/cut/old-$(date +%H%M); mkdir -p $o; mv $E/cut/e937-live.* $E/cut/final.log $o/ 2>/dev/null; }
rm -rf $E/segments-v4
# 精修片由 live-action/stage.py 37 放好（精修畫面＋草稿原聲＋剪點 -> clips/sNN-t1.mp4）。picks.json 是 refine-prep 照
# picks-merged.tsv → fix1 → fix2/review-picks.tsv 寫的（s09b s10 s14 s16b s21 s26 s36 s37 是 fix1、s27 s27b 是 fix2 9371221）；
# 第一版的 cut-trims.tsv（八鏡：s03 s16 s23 s33 s35 s38 s39 剪尾、s26 剪在槍尾尖露出之前）由 scratchpad e937c/applytrims.py 套上（原檔 e937c/bak/picks.json）。缺片或 picks.json 比片新就重跑。
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 37 || exit 1; }
# music/ 是手做的目錄：zhong-tian-qu-qi-e936-dh/music 的連結整個複製（cp -a），另加 cue-battle.mp3 → Flow zhongtian-bed-battle-take1.m4a。
M=/root/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/music
[ -d $M ] || { echo "zhong-tian-qu-qi-e937-dh/music/ 不在（cp -a e936-dh/music）"; exit 1; }
[ -e $M/cue-battle.mp3 ] || ln -s ../../_series/zhong-tian-qu-qi/music/flow-music-20261118/zhongtian-bed-battle-take1.m4a $M/cue-battle.mp3
# 本集自己的音效（剪接表 sfx_dirs 第二個目錄 $E/sfx-local/）：drum-far（遠處山上的鼓，s01–s09b 的床）、drum-near（s40 的低音重音），切法照 e936。
# 人群聲（第三個目錄 zhong-tian-qu-qi-e937-dh/sfx/）：站主規則只用本集錄音倒放（crowd-murmur.py 37 → murmur37.wav）：s17–s18 流寇、s21–s22、s31 巷子、s35 歡呼。
# 其他音效暫用系列庫 _series/zhong-tian-qu-qi/sfx（真實音效庫 _sfx-zhongtian-real-20261121 不在這台機器上，見 cut-notes.md）。
L=$E/sfx-local; mkdir -p $L
FM=/root/mokaair-work/videos/_series/zhong-tian-qu-qi/music/flow-music-20261118
mk(){ [ -f $L/$1.wav ] || ffmpeg -nostdin -v error -y ${3:+-ss $3} ${4:+-t $4} -i $FM/zhongtian-sfx-$2.m4a -ac 2 -ar 48000 -af "$5" $L/$1.wav || exit 1; }
mk drum-far war-drum-take1 "" "" "lowpass=f=900,highpass=f=60,afade=t=in:d=2"
mk drum-near war-drum-take1 0.7 3 "lowpass=f=2500,afade=t=out:st=2.4:d=0.6"
# REVIEW 3（2026-11-23）：定點音效改用真實音效庫 _series/zhong-tian-qu-qi/sfx-real-20261121（剪接表 sfx_dirs 第一個；協調者 11-23 抓到本機），
# 檔名 zhongtian-sfx-*；庫裡沒有的（石灰炸開、槍挑刀、潑水、刀鞘敲腕、跑步腳步）用最接近的庫裡聲音，缺口列在 review3-plan.md 給站主用 Flow 做。
[ -f /root/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/sfx/murmur37.wav ] || python3 -I $Q/crowd-murmur.py 37 12 || exit 1
# 終驗後（2026-11-23，final-check 輕微 4）：s26 改剪 2.333–3.541（picks.json 直接改，原檔 e937c/bak-final/picks.json）——槍尾金屬尖與地平線亮點都不露，鏡長仍 1.21 秒（MIN 1.2）。
# 剪接表假設的剪點與種子（picks.json）。整格：容差 0.001；只警告不停。
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(1.5,6.583),'s02':(1.25,6.583),'s03':(0.0,4.25),'s04':(1.0,8.0),'s05':(0.5,7.5),'s06':(3.0,8.0),'s07':(0.75,6.583),'s08':(0.5,5.0),'s09':(1.5,8.0),'s09b':(0.5,4.0),'s10':(2.25,6.583),'s11':(1.0,6.583),'s12':(1.25,6.583),'s13':(1.5,6.583),'s14':(1.75,6.583),'s15':(1.0,6.583),'s16':(0.5,4.25),'s16b':(0.0,4.0),'s17':(0.5,5.167),'s18':(1.5,6.0),'s19':(0.75,6.583),'s20':(3.0,4.75),'s21':(0.0,4.0),'s22':(1.5,5.5),'s23':(0.75,5.5),'s24':(3.0,8.0),'s25':(1.0,6.583),'s26':(2.333,3.541),'s27':(0.5,2.25),'s27b':(0.75,6.583),'s28':(0.25,5.0),'s29':(0.0,6.583),'s30':(1.25,6.583),'s31':(1.0,6.583),'s32':(1.25,6.25),'s33':(0.5,4.5),'s34':(0.5,4.583),'s35':(2.0,5.75),'s36':(1.5,6.583),'s37':(0.25,8.0),'s38':(0.5,3.5),'s39':(0.0,2.0),'s40':(0.25,6.583)}
seed={'s09':9371231,'s12':9371231,'s19':9371231,'s32':9371231,'s06':9371102,'s09b':9371211,'s10':9371212,'s14':9371211,'s16':9371102,'s16b':9371211,'s18':9371232,'s20':9371102,'s21':9371212,'s24':9371102,'s25':9371102,'s26':9371212,'s27':9371231,'s27b':9371221,'s28':9371232,'s31':9371231,'s34':9371102,'s36':9371211,'s37':9371211,'s38':9371102,'s39':9371102,'s40':9371102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9371101)' for s in p if s not in seed and p[s]['seed']!=9371101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (none may)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# 剪接表鋪的錄音在 audio/ 改寫過（原檔 audio/orig/；scratchpad e937c/levall937.sh → lev937.py，cut-notes〈錄音〉）：整平到 −13.5 LUFS 的
# a08（PRE rubberband 1.04）a18（來源 a18-p80）a21（1.17）a22（0.82）a26（1.085）a30（來源 a30-p115＋0.95）a32 a33（1.18）a38、a20（−12.5，重錄原樣）、
# 心裡話 a17（−13.0）、遠處 a31（1.06＋帶通＋回聲，−16.5）、系統 a03（0.93）a16（0.89）a36 a37 到 −14.0。少了改寫就停。
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e937-dh/audio
for n in 01 03 08 16 17 18 20 21 22 26 30 31 32 33 36 37 38; do [ -f $A/orig/zq937a$n.wav ] || { echo "audio/zq937a$n.wav is not the leveled file (no orig/ copy)"; exit 1; }; done
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos nice node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e037-r2/overlays.json $P/hailuo/edit-dh-e937-live.json $E $E/cut/e937-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e937-live.mp4 ] || exit 1
# REVIEW 3（審 1 該改 12）：CC「扔！」只停 0.46 秒 → 延到 1.0 秒（不碰下一條），srt 改寫後換掉片裡的 mov_text 軌（影音不重編）
python3 - $E/cut/e937-live.zh-TW.srt <<'PY' || exit 1
import re,sys
f=sys.argv[1]; t=open(f,encoding="utf-8").read()
ts=lambda s:sum(float(x)*m for x,m in zip(s.replace(",",".").split(":"),(3600,60,1)))
fm=lambda v:f"{int(v//3600):02d}:{int(v%3600//60):02d}:{int(v%60):02d},{round(v%1*1000):03d}"
cues=[list(m) for m in re.findall(r"(\d+)\n([\d:,]+) --> ([\d:,]+)\n(.*?)\n(?:\n|$)",t,re.S)]
for i,c in enumerate(cues):
    if c[3].strip()=="扔！":
        nxt=ts(cues[i+1][1]) if i+1<len(cues) else 1e9
        c[2]=fm(min(ts(c[1])+1.0,nxt-0.05)); print("CC 扔！ ->",c[1],c[2])
open(f,"w",encoding="utf-8").write("".join(f"{c[0]}\n{c[1]} --> {c[2]}\n{c[3]}\n\n" for c in cues).rstrip("\n")+"\n")
PY
ffmpeg -v error -y -i $E/cut/e937-live.mp4 -i $E/cut/e937-live.zh-TW.srt -map 0:v -map 0:a -map 1:s -c copy -c:s mov_text -metadata:s:s:0 language=chi -movflags +faststart $E/cut/e937-live.cc.mp4 && mv $E/cut/e937-live.cc.mp4 $E/cut/e937-live.mp4
# loudnorm2 之前的取樣峰值限制器（e923 起 limit 0.55、attack 8 ms），聲音最後 0.6 秒淡出。
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e937-live.mp4); FS=$(python3 -c "print(f'{$D-0.6:.3f}')")
ffmpeg -v error -y -i $E/cut/e937-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=0.6" $E/cut/e937-live.lim.mp4 && mv $E/cut/e937-live.lim.mp4 $E/cut/e937-live.mp4
ffmpeg -hide_banner -i $E/cut/e937-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e937-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e937-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
echo "== cutf0";    python3 $C/cutf0.py $E/cut/e937-live.mp4 $E/cut/e937-live.lines.json 2>&1 | tail -60
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
