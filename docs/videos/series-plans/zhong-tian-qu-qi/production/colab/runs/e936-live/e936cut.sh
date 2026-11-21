#!/usr/bin/env bash
# e936 成片（真人版第一版）：照 e935cut.sh。剪接表 hailuo/edit-dh-e936-live.json 由 scratchpad e936c/（mkov936.py＋music／beds／spots／
# lineat／vol／pushes.json → overrides.json，mkedit936.py＋note.txt → 剪接表）產生；所有決定與量測寫在剪接表的 _note。
# 本腳本不花錢：不用 Colab、RunPod、站台 TTS，不重做精修。
set -u
R=/home/user/travel_scanner; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e936/zhong-tian-qu-qi-e936-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e036-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e936-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e936-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# 精修片由 live-action/stage.py 36 放好（精修畫面＋草稿原聲＋剪點 -> clips/sNN-t1.mp4）。picks.json 是 refine-prep 照
# picks-merged.tsv → fix1 → fix2 → fix3/review-picks.tsv 寫的（s01 s04 s11b s12b s18 s20 s26 s28 s31 是 fix1、s02 是 fix3 開門版 9361231）；
# 第一版的 cut-trims.tsv 由 scratchpad e936c/applytrims.py 套上（原檔 e936c/bak/picks.json）。缺片或 picks.json 比片新就重跑。
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 36 || exit 1; }
# music/ 是手做的目錄：zhong-tian-qu-qi-e935-dh/music 的連結整個複製（cp -a）。
[ -d /root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/music ] || { echo "zhong-tian-qu-qi-e936-dh/music/ 不在（cp -a e935-dh/music）"; exit 1; }
# 本集自己的音效（剪接表 sfx_dirs 第二個目錄 $E/sfx-local/），都從 Flow Music 音效庫切：
# abacus-s05（插鏡金算盤，前 6 秒）、abacus-s14（帳桌木算盤，20 秒起 6.5 秒）、brush-s16（brush-writing 2.5 秒起；前 2.5 秒幾乎無聲）／brush-s17（10 秒起，帳桌毛筆）、
# drum-far（war-drum take1 低通 900 Hz、高通 60：山上遠處的鼓，s33–s38 的床）、drum-near（war-drum take1 0.7 秒起 3 秒低通 2500；take2 前 2.5 秒是空的：s36 火光的重音）。
L=$E/sfx-local; mkdir -p $L
FM=/root/mokaair-work/videos/_series/zhong-tian-qu-qi/music/flow-music-20261118
mk(){ [ -f $L/$1.wav ] || ffmpeg -nostdin -v error -y ${3:+-ss $3} ${4:+-t $4} -i $FM/zhongtian-sfx-$2.m4a -ac 2 -ar 48000 -af "$5" $L/$1.wav || exit 1; }
mk abacus-s05 abacus-take1 0 6 "volume=10dB,afade=t=out:st=5.4:d=0.6"
mk abacus-s14 abacus-take1 20 6.5 "volume=8dB,afade=t=in:d=0.1,afade=t=out:st=5.9:d=0.6"
mk brush-s16 brush-writing-take1 2.5 6 "volume=6dB,afade=t=out:st=5.4:d=0.6"
mk brush-s17 brush-writing-take1 10 2 "volume=6dB,afade=t=in:d=0.05,afade=t=out:st=1.7:d=0.3"
mk drum-far war-drum-take1 "" "" "lowpass=f=900,highpass=f=60,afade=t=in:d=2"
mk drum-near war-drum-take1 0.7 3 "lowpass=f=2500,afade=t=out:st=2.4:d=0.6"
# 剪接表假設的剪點與種子（picks.json）。整格：容差 0.001；只警告不停。
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.75,6.583),'s02':(0.5,6.583),'s03':(1.25,7.25),'s04':(0.25,6.25),'s05':(0.5,6.0),'s06':(0.75,6.583),'s07':(0.5,6.583),'s08':(0.25,4.583),'s09':(2.75,8.0),'s10':(1.5,8.0),'s11':(0.0,8.25),'s11b':(1.75,6.583),'s12':(1.25,6.583),'s12b':(1.5,6.583),'s13':(2.75,6.583),'s14':(0.0,5.5),'s15':(0.0,2.0),'s16':(0.5,5.5),'s17':(0.0,2.0),'s18':(0.0,6.583),'s19':(1.75,6.583),'s20':(1.5,6.583),'s21':(1.75,6.583),'s22':(0.0,5.5),'s23':(0.5,6.583),'s24':(2.75,8.0),'s25':(1.5,6.583),'s26':(1.25,10.125),'s27':(1.0,5.0),'s28':(0.0,6.5),'s29':(0.0,5.0),'s30':(1.25,8.0),'s31':(1.0,6.583),'s32':(2.25,6.583),'s33':(1.25,4.583),'s34':(0.75,6.0),'s35':(1.25,8.0),'s36':(2.5,4.5),'s37':(1.0,3.0),'s38':(0.25,5.0)}
seed={'s01':9361212,'s02':9361231,'s04':9361211,'s11':9361102,'s11b':9361212,'s12':9361102,'s12b':9361212,'s14':9361102,'s18':9361211,'s20':9361212,'s21':9361102,'s23':9361102,'s26':9361211,'s28':9361212,'s31':9361212,'s32':9361102,'s33':9361102,'s34':9361102,'s35':9361102,'s36':9361102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9361101)' for s in p if s not in seed and p[s]['seed']!=9361101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (none may)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# 剪接表鋪的錄音在 audio/ 改寫過（原檔 audio/orig/；scratchpad e936c/levall.sh → lev936.py，_note〈錄音〉）：整平到 −13.5 LUFS 的
# a01 a06 a07 a10 a12 a16 a17 a18、a03（來源 a03-p77）、a28（來源重錄 a28-p118）、a35（來源 a35-p88）、a04 a22 a23 a27 a31 a32 a15（PRE 變調），
# 系統 a11 a29（PRE rubberband 1.20）到 −14.0。少了改寫就停。
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e936-dh/audio
for n in 01 03 04 06 07 10 11 12 15 16 17 18 22 23 27 28 29 31 32 35; do [ -f $A/orig/zq936a$n.wav ] || { echo "audio/zq936a$n.wav is not the leveled file (no orig/ copy)"; exit 1; }; done
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos nice node assemble-v4.mjs $VJ $R/docs/videos/zhong-tian-qu-qi-e036-r2/overlays.json $P/hailuo/edit-dh-e936-live.json $E $E/cut/e936-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e936-live.mp4 ] || exit 1
# loudnorm2 之前的取樣峰值限制器（e923 起 limit 0.55、attack 8 ms），聲音最後 0.6 秒淡出（s38 停在最高點，只收最後一點）。
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e936-live.mp4); FS=$(python3 -c "print(f'{$D-0.6:.3f}')")
ffmpeg -v error -y -i $E/cut/e936-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=0.6" $E/cut/e936-live.lim.mp4 && mv $E/cut/e936-live.lim.mp4 $E/cut/e936-live.mp4
ffmpeg -hide_banner -i $E/cut/e936-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e936-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e936-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VJ 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VJ $E/review/continuity-v1 2>&1 | tail -4
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
