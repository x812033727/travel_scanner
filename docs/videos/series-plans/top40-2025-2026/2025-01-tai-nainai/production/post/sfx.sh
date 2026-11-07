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
# 報信鈴：三顆小銅鈴，C7、E7、G7 附近各自衰減，略錯開
ffmpeg -v error -y -f lavfi -i "aevalsrc='0.32*sin(2*PI*2093*t)*exp(-4.5*t)+0.18*sin(2*PI*4186*t)*exp(-9*t)+0.26*sin(2*PI*2637*(t-0.045))*exp(-5*(t-0.045))*gte(t,0.045)+0.22*sin(2*PI*3136*(t-0.09))*exp(-5.5*(t-0.09))*gte(t,0.09)':s=48000:d=1.8" \
  -af "aecho=0.6:0.4:40|70:0.25|0.15,afade=t=out:st=1.4:d=0.4" -ac 2 "$OUT/baoxinling.wav"
# 燈亮的低鳴：低音慢慢升起、帶一點泛音，三秒
ffmpeg -v error -y -f lavfi -i "aevalsrc='(0.28*sin(2*PI*110*t)+0.14*sin(2*PI*165*t)+0.07*sin(2*PI*330*t))*(1-exp(-1.6*t))*exp(-0.35*t)':s=48000:d=3.2" \
  -af "lowpass=f=1200,afade=t=out:st=2.4:d=0.8" -ac 2 "$OUT/deng-hum.wav"
# 倒燈油：很細的液體流聲，一秒半
ffmpeg -v error -y -f lavfi -i "anoisesrc=color=pink:amplitude=0.35:d=1.6:seed=11" \
  -af "bandpass=f=2600:width_type=o:w=1.4,tremolo=f=13:d=0.6,afade=t=in:d=0.15,afade=t=out:st=1.1:d=0.5" -ac 2 "$OUT/oil-pour.wav"
ls "$OUT" | wc -l | xargs echo "sfx.sh: files in $OUT:"
