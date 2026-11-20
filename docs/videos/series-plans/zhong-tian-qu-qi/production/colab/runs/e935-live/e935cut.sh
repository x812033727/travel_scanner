#!/usr/bin/env bash
# e935 成片（真人版第一版）：照 e934cut.sh。剪接表 hailuo/edit-dh-e935-live.json 由 scratchpad e935c/（mkov935.py＋music／beds／spots／vol.json → overrides.json，
# mkedit935.py＋note.txt → 剪接表）產生；所有決定與量測寫在剪接表的 _note。本腳本不花錢：不用 Colab、RunPod、站台 TTS，不重做精修。
set -u
R=/home/user/travel_scanner; P=$R/docs/videos/series-plans/zhong-tian-qu-qi/production; Q=$P/colab/runs/_scripts
E=/root/mokaair-work/videos/_live-e935/zhong-tian-qu-qi-e935-dh; VJ=$R/docs/videos/zhong-tian-qu-qi-e035-r2/video.json
mkdir -p $E/cut; [ -f $E/cut/e935-live.mp4 ] && { mkdir -p $E/cut/old-$(date +%H%M); mv $E/cut/e935-live.* $E/cut/final.log $E/cut/old-$(date +%H%M)/ 2>/dev/null; }
rm -rf $E/segments-v4
# 精修片由 live-action/stage.py 35 放好（精修畫面＋草稿原聲＋剪點 -> clips/sNN-t1.mp4；picks.json 由 colab/runs/e935-live 的
# refine-prep.py 35 picks-merged.tsv fix1/review-picks.tsv fix2/review-picks.tsv cut-trims.tsv review3-trims.tsv fix3/review-picks.tsv 產生
# （scratchpad e935refine.sh 的讀檔順序）：s23 s34 是 fix1、s17b 是 fix2 9351222、s01 s24 s25 s30 s32 是 fix3（REVIEW 3））；
# 缺片或 picks.json 比片新就重跑。stage.py 把 $E/audio、$E/music 連到 zhong-tian-qu-qi-e935-dh/audio、music；
# music/ 是手做的目錄（照 e934：e934-dh/music 的連結全抄，另加 Flow Music 庫的 cue-village-comedy／night-village／farewell／system-whimsy.mp3
# -> zhongtian-bed-<名>-take1.m4a，cue-heart／comedy／face-slap／system-short.mp3 -> zhongtian-cue-<名>-take1.m4a）。
stale=$(python3 -c "import json,os;e='$E';p=json.load(open(e+'/picks.json'));t=os.path.getmtime(e+'/picks.json');print(' '.join(s for s in p if not os.path.exists(f'{e}/clips/{s}-t1.mp4') or os.path.getmtime(f'{e}/clips/{s}-t1.mp4')<t))")
[ -z "$stale" ] || { echo "staging (stale: $stale)"; python3 $P/live-action/stage.py 35 || exit 1; }
[ -d /root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/music ] || { echo "zhong-tian-qu-qi-e935-dh/music/ 不在（見上面的說明）"; exit 1; }
# s14 遠山蝗群加深用第 34 集 s40 的蝗群（剪接表 vf s14 的 movie=），複製一份在 $E/vfx/，不跟第 34 集的 clips/ 綁在一起。
[ -f $E/vfx/locust-e934s40.mp4 ] || { mkdir -p $E/vfx; cp /root/mokaair-work/videos/_live-e934/zhong-tian-qu-qi-e934-dh/clips/s40-t1.mp4 $E/vfx/locust-e934s40.mp4 || exit 1; }
# REVIEW 3：s06 窗的黑點層 vfx/specks-s06.mp4（scratchpad e935r3/specks.py 4.6 880 220 1420 1000 935061 18）要在。
[ -f $E/vfx/specks-s06.mp4 ] || { echo "vfx/specks-s06.mp4 不在（scratchpad e935r3/specks.py）"; exit 1; }
# 本集自己的音效（剪接表 sfx_dirs 第二個目錄 $E/sfx-local/）：沒有片中人聲的鏡（無台詞、台詞是錄音），組片程式把片中聲音整支靜音，
# 片中有用的聲音切出來放回去：duck-s12（開籠、鴨群）、duck-s13（鴨子撲翅）、whistle-s17（短哨 c1.0–2.0）、duck-s17b、duck-s19、duck-s20、
# peck-s21（鴨嘴一啄）、water-s23（水聲鴨叫）；whistle1（s17 c0.85–1.75 的一聲哨，s19 s20 用）；
# abacus-s07（Flow Music 庫 zhongtian-sfx-abacus 前 7.5 秒，+12 dB）；rasp-in（第 34 集 sfx-local 的 buzzloop 低通 1800 Hz：屋外蝗群撲窗，隔著牆）。
L=$E/sfx-local; C=$E/clips; mkdir -p $L
cutw(){ [ $L/$1.wav -nt $C/$2-t1.mp4 ] || ffmpeg -nostdin -v error -y ${3:+-ss $3} ${4:+-to $4} -i $C/$2-t1.mp4 -vn -ac 2 -ar 48000 ${5:+-af $5} $L/$1.wav || exit 1; }
cutw duck-s12 s12; cutw duck-s13 s13; cutw whistle-s17 s17; cutw duck-s17b s17b; cutw duck-s19 s19; cutw duck-s20 s20; cutw peck-s21 s21; cutw water-s23 s23
cutw whistle1 s17 0.85 1.75 "afade=t=in:d=0.02,afade=t=out:st=0.75:d=0.15"
FM=/root/mokaair-work/videos/_series/zhong-tian-qu-qi/music/flow-music-20261118
[ -f $L/abacus-s07.wav ] || ffmpeg -nostdin -v error -y -t 7.5 -i $FM/zhongtian-sfx-abacus-take1.m4a -ac 2 -ar 48000 -af "volume=12dB,afade=t=out:st=6.9:d=0.6" $L/abacus-s07.wav || exit 1
[ -f $L/rasp-in.wav ] || ffmpeg -nostdin -v error -y -i /root/mokaair-work/videos/_live-e934/zhong-tian-qu-qi-e934-dh/sfx-local/buzzloop.wav -ac 2 -ar 48000 -af "lowpass=f=1800,highpass=f=120" $L/rasp-in.wav || exit 1
# 剪接表假設的剪點與種子（picks.json；第一版的 cut-trims.tsv 由 applytrims.py 套上，REVIEW 3 起 cut-trims.tsv、review3-trims.tsv
# 都在 refine-prep 的讀檔順序裡，refine-prep 重跑也保留；第一版的 picks.json 在 e935c/bak/）。整格：起點往下、終點往上取到小數三位，容差 0.001；只警告不停。
python3 -c "
import json;p=json.load(open('$E/picks.json'))
want={'s01':(0.0,7.0),'s02':(1.75,6.25),'s02b':(1.25,6.583),'s03':(0.5,5.75),'s04':(0.75,6.583),'s05':(1.25,6.583),'s06':(2.0,6.583),'s07':(0.0,6.25),'s08':(1.5,6.583),'s09':(0.0,5.208),'s10':(1.375,6.583),'s11':(0.0,3.0),'s11b':(0.5,5.25),'s12':(0.0,5.167),'s12b':(0.0,6.25),'s13':(0.0,4.0),'s14':(0.0,5.25),'s15':(1.75,6.583),'s16':(3.25,6.583),'s17':(0.0,4.0),'s17b':(1.0,6.0),'s18':(1.75,6.583),'s19':(0.0,5.167),'s20':(0.0,6.0),'s20b':(0.0,6.583),'s21':(0.75,4.25),'s22':(1.5,9.5),'s23':(0.0,6.75),'s24':(1.0,7.875),'s25':(1.0,6.583),'s26':(0.0,6.583),'s27':(0.5,4.25),'s28':(0.0,5.5),'s29':(0.0,4.0),'s30':(0.0,9.375),'s31':(1.5,8.0),'s32':(1.0,6.583),'s33':(1.5,6.583),'s34':(0.0,6.583),'s35':(0.0,6.75)}
seed={'s01':9351238,'s17b':9351222,'s23':9351212,'s30':9351230,'s34':9351212,'s24':9351234,'s32':9351231,'s02':9351102,'s02b':9351102,'s03':9351102,'s10':9351102,'s11':9351102,'s11b':9351102,'s15':9351102,'s16':9351102,'s18':9351102,'s20':9351102,'s25':9351236,'s27':9351102,'s31':9351102,'s33':9351102,'s35':9351102}
bad=[f'{s} start {p[s][\"trim\"].get(\"start\",0)} end-before {p[s][\"trim\"].get(\"end-before\",0)} (want {a} {b})' for s,(a,b) in want.items()
     if s in p and (abs(p[s]['trim'].get('start',0)-a)>0.001 or abs(p[s]['trim'].get('end-before',0)-b)>0.001)]
bad+=[f'{s} seed {p[s][\"seed\"]} (want {v})' for s,v in seed.items() if s in p and p[s]['seed']!=v]
bad+=[f'{s} seed {p[s][\"seed\"]} (want 9351101)' for s in p if s not in seed and p[s]['seed']!=9351101]
bad+=[f'{s} not in picks.json' for s in want if s not in p]
bad+=[f'{s} in picks.json, not in the want table' for s in p if s not in want]
bad+=[f'{s} has crop {p[s].get(\"crop\")} (none may)' for s in p if p[s].get('crop')]
print('WARNING picks.json trims: '+'; '.join(bad)) if bad else None"
# 剪接表鋪的錄音在 audio/ 改寫過（原檔在 audio/orig/；scratchpad e935c/lev935.py，_note〈錄音〉）：整平到 −13.5 LUFS 的 a03 a05 a09 a11 a14 a17 a20 a24 a27
# a29 a32 a36、a15（來源 a15-p104）、a34（來源 a34-p119＋rubberband 1.04）、a16（rubberband 1.13）、a30（重錄 asetrate 0.715）、
# a33（照 s31 嘴切四段重排，scratchpad e935c/a33-src.wav），系統 a01 a02 a13 a28 a31 到 −14.0。少了改寫就停。
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e935-dh/audio
for n in 01 02 03 05 09 11 13 14 15 16 17 20 24 27 28 29 30 31 32 33 34 36; do [ -f $A/orig/zq935a$n.wav ] || { echo "audio/zq935a$n.wav is not the leveled file (no orig/ copy)"; exit 1; }; done
VL=$VJ
cd $P/hailuo && VIDEO_WORKDIR=/root/mokaair-work/videos nice node assemble-v4.mjs $VL $R/docs/videos/zhong-tian-qu-qi-e035-r2/overlays.json $P/hailuo/edit-dh-e935-live.json $E $E/cut/e935-live.mp4 > $E/cut/final.log 2>&1; tail -3 $E/cut/final.log
[ -f $E/cut/e935-live.mp4 ] || exit 1
# loudnorm2 之前的取樣峰值限制器（e923 起 limit 0.55、attack 8 ms），聲音最後 0.6 秒淡出（s35 停在最高點，只收最後一點）。
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $E/cut/e935-live.mp4); FS=$(python3 -c "print(f'{$D-0.6:.3f}')")
ffmpeg -v error -y -i $E/cut/e935-live.mp4 -map 0 -c copy -c:a aac -b:a 192k -af "alimiter=limit=0.55:attack=8:release=60:level=false,aresample=48000,afade=t=out:st=$FS:d=0.6" $E/cut/e935-live.lim.mp4 && mv $E/cut/e935-live.lim.mp4 $E/cut/e935-live.mp4
ffmpeg -hide_banner -i $E/cut/e935-live.mp4 -map 0:a -af loudnorm=I=-14:TP=-2.2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p' \
 | python3 -c "import json,sys;j=json.load(sys.stdin);i,tp=float(j['input_i']),float(j['input_tp']);print(f'pre-loudnorm2 {i} LUFS {tp} dBTP: {tp-14-i:+.2f} after the gain ->', 'linear' if tp-14-i<=-2.2 else 'DYNAMIC (lower the limiter or its attack)')"
bash $Q/loudnorm2.sh $E/cut/e935-live.mp4
echo "== cut-qa";   python3 $Q/cut-qa.py $E/cut --stem e935-live 2>&1 | tail -20
echo "== cut-jumps"; python3 $Q/cut-jumps.py $E/cut 2>&1 | tail -12
echo "== audio-qa"; python3 $Q/audio-qa.py $E/cut $VL 2>&1 | tail -15
echo "== sheets";   python3 $Q/continuity-sheets.py $E/cut $VL $E/review/continuity-v1 2>&1 | tail -4
[ "${KEEP_SEG:-0}" = 1 ] || rm -rf $E/segments-v4
[ "${KEEP_PRE:-0}" = 1 ] || rm -rf $E/cut/pre
