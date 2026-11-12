#!/usr/bin/env bash
# 《恁祖媽今年18》的音效庫：從《種田》的 CC0 音效庫挑可用的，加上全季的招牌音效（ffmpeg 合成，每次一樣）。
#   bash sfx.sh [<out dir>]   預設 ${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}/_series/tai-nainai/sfx
# 《種田》的庫在 ${VIDEO_WORKDIR}/_series/zhong-tian-qu-qi/sfx（docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/sfx-synth.sh 重建）。
# 招牌音效全季同一個檔（bible〈配樂、音效、剪接〉）：報信鈴（三顆銅鈴）、燈亮的低鳴；另有倒燈油的細流。
set -euo pipefail
ROOT=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}
SRC=$ROOT/_series/zhong-tian-qu-qi/sfx
OUT=${1:-$ROOT/_series/tai-nainai/sfx}
mkdir -p "$OUT"
for f in footstep_wood_000 footstep_concrete_000 footstep_concrete_001 creak1 creak2 creak3 door_close_01 metalLatch \
         paper_02 paper_03 impactWood_light_000 impactWood_light_001 impactWood_medium_000 impactPlate_light_000 \
         dishes_01 dishes_02 cloth1 cloth2 handleCoins bookFlip1 bookPlace1 impactWood_heavy_000 impactPlate_light_000 \
         metalPot1 metalPot2 impactSoft_heavy_000 wooded_box_open impactMetal_light_000; do
  [ -f "$SRC/$f.wav" ] || { echo "sfx.sh: $SRC/$f.wav missing; rebuild the 種田 library first" >&2; exit 1; }
  cp "$SRC/$f.wav" "$OUT/"
done
# 報信鈴：真的鈴鐺錄音（站主 2026-11-08：鈴鐺聲怪怪的。第一、二版是正弦波合成的音階，像電子門鈴）。
# 來源：Wikimedia Commons「File:Sleigh bells.wav」，作者 The Midnite Wolf，CC0；用的是 Commons 轉檔的 mp3
# （原 wav 下載被限流）。存在 $OUT/src/commons-sleigh-bells-cc0.mp3（備份分支 transfer/tn-series-assets 有）。舊的合成版留在 src/*-synth-v1.wav。
BELL="$OUT/src/commons-sleigh-bells-cc0.mp3"
[ -f "$BELL" ] || { echo "sfx.sh: $BELL missing (restore it from transfer/tn-series-assets)" >&2; exit 1; }
# 錄音很小聲（平均約 −46 dB），切掉 350 Hz 以下、加閘門壓底噪再放大
ffmpeg -v error -y -ss 4.40 -to 7.00 -i "$BELL" -af "highpass=f=350,agate=threshold=0.004:ratio=4:release=80,volume=21dB,afade=t=in:d=0.01,afade=t=out:st=2.2:d=0.4,aresample=48000" -ac 2 "$OUT/baoxinling.wav"
# 跑步時書包上的鈴輕輕晃：錄音裡一小下
ffmpeg -v error -y -ss 1.15 -to 1.95 -i "$BELL" -af "highpass=f=350,agate=threshold=0.004:ratio=4:release=80,volume=25dB,afade=t=in:d=0.01,afade=t=out:st=0.55:d=0.25,aresample=48000" -ac 2 "$OUT/baoxinling-shake.wav"
# 燈亮的低鳴：低音慢慢升起、帶一點泛音，三秒
ffmpeg -v error -y -f lavfi -i "aevalsrc='(0.28*sin(2*PI*110*t)+0.14*sin(2*PI*165*t)+0.07*sin(2*PI*330*t))*(1-exp(-1.6*t))*exp(-0.35*t)':s=48000:d=3.2" \
  -af "lowpass=f=1200,afade=t=out:st=2.4:d=0.8" -ac 2 "$OUT/deng-hum.wav"
# 倒燈油：很細的液體流聲，一秒半
ffmpeg -v error -y -f lavfi -i "anoisesrc=color=pink:amplitude=0.35:d=1.6:seed=11" \
  -af "bandpass=f=2600:width_type=o:w=1.4,tremolo=f=13:d=0.6,afade=t=in:d=0.15,afade=t=out:st=1.1:d=0.5" -ac 2 "$OUT/oil-pour.wav"
# 手機撥號：三個按鍵音，再一聲掛斷（第 2 集 c04）
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.25*(sin(2*PI*697*t)+sin(2*PI*1209*t))*(between(t,0,0.09)+between(t,0.18,0.27)+between(t,0.36,0.45))+0.2*sin(2*PI*480*t)*between(t,0.9,1.15)':s=48000:d=1.3" -ac 2 "$OUT/phone-dial.wav"
# 遠處的警笛：兩個音高來回，經過低通與殘響，像在巷口（第 2 集 c05、c08）
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.3*sin(2*PI*(700+250*sin(2*PI*0.5*t))*t)':s=48000:d=6" -af "lowpass=f=1800,aecho=0.8:0.6:120|240:0.4|0.25,afade=t=in:d=1.5,afade=t=out:st=4.5:d=1.5" -ac 2 "$OUT/siren-far.wav"
# 三十個抽屜的木聲鼓點（第 3 集 c05，招牌音效）：同一聲木頭輕敲，前快後穩，約六秒
f="$OUT/impactWood_light_000.wav"; inputs=(); filt=""; n=0
for ms in 0 180 330 520 680 860 1010 1200 1350 1540 1700 1880 2030 2240 2400 2600 2760 2960 3120 3330 3500 3720 3880 4100 4280 4500 4680 4920 5120 5400; do
  inputs+=(-i "$f"); filt="${filt}[${n}:a]adelay=${ms}|${ms},volume=$(awk "BEGIN{print 0.6+0.4*(($n%3)==0)}")[d${n}];"; n=$((n+1)); done
ffmpeg -v error -y "${inputs[@]}" -filter_complex "${filt}$(for i in $(seq 0 $((n-1))); do printf "[d$i]"; done)amix=inputs=$n:normalize=0,afade=t=out:st=5.6:d=0.4" -ac 2 "$OUT/drawers-30.wav"
# 福伯懷錶的滴答（招牌音效）：每秒一聲細的金屬滴答，四秒
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.5*sin(2*PI*4200*t)*exp(-180*mod(t,1))+0.3*sin(2*PI*2900*(t-0.5))*exp(-200*mod(t-0.5,1))*gte(t,0.5)':s=48000:d=4" -af "highpass=f=1500" -ac 2 "$OUT/pocketwatch-tick.wav"
# 劃火柴：一下擦、一團火著
ffmpeg -v error -y -f lavfi -i "anoisesrc=color=white:amplitude=0.6:d=1.2:seed=7" -af "bandpass=f=3500:width_type=o:w=2,volume='if(lt(t,0.12),1.0,0.35*exp(-2*(t-0.12)))':eval=frame,afade=t=out:st=0.9:d=0.3" -ac 2 "$OUT/match-strike.wav"
# 報信鈴在鐵皮桶裡悶悶一響（招牌音效的悶版）
ffmpeg -v error -y -i "$OUT/baoxinling.wav" -af "lowpass=f=3000,aecho=0.6:0.5:25:0.4,volume=16dB" -ac 2 "$OUT/baoxinling-muffled.wav"  # 錄音版的鈴在 900 Hz 以下幾乎沒有聲音
ls "$OUT" | wc -l | xargs echo "sfx.sh: files in $OUT:"
