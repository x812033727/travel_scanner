#!/bin/bash
# sheet.sh shot seed fps [cols] [width]
S=$1; SEED=$2; FPS=${3:-2}; COLS=${4:-4}; W=${5:-480}
IN=/root/mokaair-work/videos/zhong-tian-qu-qi-e902-dh/runpod/a/fix2/out/$S-$SEED.mp4
OUT=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/pick902/dense/$S-$SEED.jpg
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $IN)
N=$(python3 -c "import math;print(math.ceil($D*$FPS))")
ROWS=$(( (N+COLS-1)/COLS ))
ffmpeg -v error -y -i $IN -vf "fps=$FPS,scale=$W:-1,drawtext=text='%{pts\:hms}':x=5:y=5:fontsize=20:fontcolor=yellow:box=1:boxcolor=black,tile=${COLS}x${ROWS}" -frames:v 1 $OUT 2>&1 || ffmpeg -v error -y -i $IN -vf "fps=$FPS,scale=$W:-1,tile=${COLS}x${ROWS}" -frames:v 1 $OUT
echo $OUT
