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
         dishes_01 dishes_02 cloth1 cloth2 handleCoins; do
  [ -f "$SRC/$f.wav" ] || { echo "sfx.sh: $SRC/$f.wav missing; rebuild the 種田 library first" >&2; exit 1; }
  cp "$SRC/$f.wav" "$OUT/"
done
# 報信鈴：三顆小銅鈴錯開響兩下（第一版只有高音、太短，站主 2026-11-07：「鈴鐺應該要有聲音」聽不到）
bell() { echo "(0.30*sin(2*PI*$1*(t-$2))*exp(-2.2*(t-$2))+0.20*sin(2*PI*$1*2.76*(t-$2))*exp(-4*(t-$2))+0.12*sin(2*PI*$1*5.4*(t-$2))*exp(-7*(t-$2)))*gte(t,$2)"; }
expr="$(bell 1318 0)+$(bell 1568 0.05)+$(bell 1760 0.09)+0.8*($(bell 1318 0.42)+$(bell 1568 0.46)+$(bell 1760 0.5))"
ffmpeg -v error -y -f lavfi -i "aevalsrc='$expr':s=48000:d=2.6" \
  -af "aecho=0.7:0.5:35|60:0.3|0.2,highpass=f=400,afade=t=out:st=2.0:d=0.6,volume=1.6" -ac 2 "$OUT/baoxinling.wav"
# 跑步時書包上的鈴輕輕晃：同一組鈴、一下、短
expr2="$(bell 1318 0)+$(bell 1568 0.03)+$(bell 1760 0.06)"
ffmpeg -v error -y -f lavfi -i "aevalsrc='$expr2':s=48000:d=0.9" -af "highpass=f=400,afade=t=out:st=0.5:d=0.4" -ac 2 "$OUT/baoxinling-shake.wav"
# 燈亮的低鳴：低音慢慢升起、帶一點泛音，三秒
ffmpeg -v error -y -f lavfi -i "aevalsrc='(0.28*sin(2*PI*110*t)+0.14*sin(2*PI*165*t)+0.07*sin(2*PI*330*t))*(1-exp(-1.6*t))*exp(-0.35*t)':s=48000:d=3.2" \
  -af "lowpass=f=1200,afade=t=out:st=2.4:d=0.8" -ac 2 "$OUT/deng-hum.wav"
# 倒燈油：很細的液體流聲，一秒半
ffmpeg -v error -y -f lavfi -i "anoisesrc=color=pink:amplitude=0.35:d=1.6:seed=11" \
  -af "bandpass=f=2600:width_type=o:w=1.4,tremolo=f=13:d=0.6,afade=t=in:d=0.15,afade=t=out:st=1.1:d=0.5" -ac 2 "$OUT/oil-pour.wav"
ls "$OUT" | wc -l | xargs echo "sfx.sh: files in $OUT:"
