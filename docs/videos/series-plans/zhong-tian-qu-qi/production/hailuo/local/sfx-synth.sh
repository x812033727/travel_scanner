#!/usr/bin/env bash
# sfx-synth.sh : synthesize the effect sounds the edit sheets name into
# <VIDEO_WORKDIR>/_series/zhong-tian-qu-qi/sfx/<name>.wav (48 kHz stereo), so the series no longer
# depends on another production's CC0 library (ou-de-jianghu-e001/.../sound-library was removed on
# 2026-10-19 and took every e1-24 effect with it). Plain ffmpeg, nothing downloaded; rerun any time.
# Edit sheets point at it with "sfx_dirs": ["<VIDEO_WORKDIR>/_series/zhong-tian-qu-qi/sfx"].
set -eu
V=${VIDEO_WORKDIR:-$HOME/mokaair-work/videos}
D="$V/_series/zhong-tian-qu-qi/sfx"
mkdir -p "$D"
out() { ffmpeg -v error -y -f lavfi -i "$2" -af "aformat=sample_rates=48000:channel_layouts=stereo,$3" -ar 48000 -ac 2 "$D/$1.wav"; echo "$1"; }
P='2*PI'
# A struck object: a decaying tone plus a short noise click.
hit() { # name freq decay dur
  ffmpeg -v error -y -f lavfi -i "aevalsrc=0.7*(sin($P*$2*t)+0.4*sin($P*$2*2.3*t))*exp(-$3*t):d=$4" \
    -f lavfi -i "anoisesrc=color=pink:amplitude=0.6:d=$4" \
    -filter_complex "[1]lowpass=f=$(( $2 * 6 )),volume='exp(-$(( $3 * 3 ))*t)':eval=frame[n];[0][n]amix=inputs=2:normalize=0,aformat=sample_rates=48000:channel_layouts=stereo,afade=t=in:d=0.003" \
    -ar 48000 -ac 2 "$D/$1.wav"; echo "$1"; }
clink() { # one metallic clink at offset T
  echo "if(gte(t,$1),(sin($P*3900*(t-$1))+0.6*sin($P*5300*(t-$1))+0.4*sin($P*2700*(t-$1)))*exp(-55*(t-$1)),0)"; }

out gong_02 "aevalsrc=0.45*(sin($P*196*t)+0.6*sin($P*541*t)+0.35*sin($P*1058*t)+0.3*sin($P*233*t))*exp(-0.8*t)*(1+0.15*sin($P*3.5*t)):d=4.5" "afade=t=in:d=0.004"
for s in 3 9; do out "swish-$s" "anoisesrc=color=white:amplitude=0.8:d=0.45" "bandpass=f=$(( 1200 + s * 120 )):width_type=o:w=1.5,volume='pow(sin(PI*t/0.45),2)':eval=frame"; done
hit impactWood_light_000 520 34 0.25
hit impactWood_light_001 470 30 0.25
hit impactWood_medium_000 320 22 0.35
hit impactWood_medium_001 290 20 0.35
hit impactWood_heavy_000 170 13 0.55
hit impactWood_heavy_001 150 12 0.55
hit impactWood_heavy_002 135 11 0.6
hit impactPlank_medium_000 240 18 0.4
hit impactSoft_heavy_000 80 10 0.5
hit impactPunch_medium_000 95 18 0.3
hit footstep_concrete_001 120 38 0.18
hit footstep_concrete_002 135 40 0.18
hit footstep_concrete_003 110 36 0.18
out handleCoins "aevalsrc='0.25*($(clink 0)+$(clink 0.07)+$(clink 0.16)+$(clink 0.24)+$(clink 0.35))':d=0.8" "afade=t=in:d=0.002"
out handleCoins2 "aevalsrc='0.25*($(clink 0)+$(clink 0.11)+$(clink 0.19)+$(clink 0.3))':d=0.7" "afade=t=in:d=0.002"
out key_open_01 "aevalsrc='0.3*($(clink 0)+$(clink 0.14))':d=0.45" "afade=t=in:d=0.002,lowpass=f=4500"
out paper_02 "anoisesrc=color=white:amplitude=0.5:d=0.35" "highpass=f=2500,volume='pow(sin(PI*t/0.35),2)':eval=frame"
out paper_04 "anoisesrc=color=white:amplitude=0.5:d=0.6" "highpass=f=2200,tremolo=f=14:d=0.7,volume='pow(sin(PI*t/0.6),2)':eval=frame"
out bookFlip2 "anoisesrc=color=white:amplitude=0.5:d=0.7" "highpass=f=1800,tremolo=f=20:d=0.9,volume='pow(sin(PI*t/0.7),2)':eval=frame"
for k in 1 2 3; do out "creak$k" "aevalsrc=0.35*sin($P*(110+20*$k+50*t)*t+2.5*sin($P*(6+$k)*t)):d=0.9" "bandpass=f=$(( 500 + k * 80 )):width_type=o:w=2,afade=t=in:d=0.08,afade=t=out:st=0.6:d=0.3"; done
out birds "aevalsrc='0.18*sin($P*(2900+1300*sin($P*11*t))*t)*gt(sin($P*1.1*t)+0.4*sin($P*2.9*t),0.85)':d=10" "highpass=f=1500"
ffmpeg -v error -y -i "$D/creak2.wav" -i "$D/impactWood_medium_000.wav" -filter_complex "[1]adelay=550|550[b];[0][b]amix=inputs=2:normalize=0" -ar 48000 -ac 2 "$D/wooded_box_open.wav"; echo wooded_box_open
ls "$D" | wc -l
