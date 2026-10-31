#!/usr/bin/env bash
# e035 s09 retake through all three stages on one G4 session, then stop it
set -u
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
R=/root/mokaair-work/videos/zhong-tian-qu-qi-e035-dh/colab/a/retake2
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e035-dh/colab/a
export COLAB_GPU=G4
S=zt35s
echo "start $(date -u +%FT%TZ)"
H3_PROFILE=hero bash $K/bootstrap.sh patch 2>&1 | grep -o "profile=[a-z]*"
bash $K/h3.sh start --session $S 2>&1 | tail -1
colab sessions 2>&1 | grep -q "$S.*Hardware: G4" || { echo "NOT G4"; bash $K/h3.sh stop --session $S; exit 3; }
cd $R
python3 -I $K/h3_detached.py ref-e035-part1.json --session $S --poll 30 --attempts 2 2>&1 | tail -2
[ -f out/s09.mp4 ] || { echo "stage 1 failed"; bash $K/h3.sh stop --session $S; exit 4; }
mkdir -p st2/ff st2/prompts st2/refined final
ffmpeg -v error -y -i out/s09.mp4 -frames:v 1 -vf "scale=1312:736:force_original_aspect_ratio=increase:flags=lanczos,crop=1312:736" st2/ff/s09.png
cp $A/st2/prompts/s09.txt st2/prompts/s09.txt
printf '{"jobs":[{"id":"s09","input_video":"%s/out/s09.mp4","first_frame":"ff/s09.png","prompt_file":"prompts/s09.txt","output_name":"s09.mp4","sigma_start":0.5,"steps":10,"seed":330001,"guide":"none"}]}\n' "$R" > st2/st2.json
bash $K/h3.sh refine --manifest st2/st2.json --output-dir st2/refined --session $S --detached 2>&1 | tail -1
mkdir -p up && ln -sf $R/st2/refined/s09.mp4 up/s09.mp4
bash $K/h3.sh upscale --input-dir up --output-dir final --session $S --detached --timeout 1500 2>&1 | tail -1
bash $K/h3.sh stop --session $S 2>&1 | tail -1
ls -la final/s09_1080.mp4
echo ALL_DONE
