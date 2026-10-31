#!/usr/bin/env bash
# place the 1080p finals as <workdir>/clips/sNN-t1.mp4; s17 and s27 lose their opening set-plate frames
set -u
W=/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh
A=$W/colab/a
P=$W/colab/pilot-a
mkdir -p $W/clips
put() { [ -f "$1" ] && { [ "$1" -nt "$W/clips/$2-t1.mp4" ] || [ ! -f "$W/clips/$2-t1.mp4" ]; } && cp "$1" "$W/clips/$2-t1.mp4" && echo "placed $2"; }
for f in $A/final/s*_1080.mp4; do s=$(basename $f _1080.mp4); case $s in s17|s27) ;; *) put $f $s ;; esac; done
put $P/retake/final/s08_1080.mp4 s08
put $P/retake/final/s09_1080.mp4 s09
put $P/final/s21_1080.mp4 s21
# s17: the first 0.6 s are the empty pool; s27: frames 20-119 hold the drawing, before and after are the plate
[ -f $A/final/s17_1080.mp4 ] && [ ! -f $W/clips/s17-t1.mp4 ] && ffmpeg -v error -y -ss 0.625 -i $A/final/s17_1080.mp4 -c:v libx264 -crf 14 -preset slow -c:a aac $W/clips/s17-t1.mp4 && echo "placed s17 (trimmed 0.625 s)"
[ -f $A/final/s27_1080.mp4 ] && [ ! -f $W/clips/s27-t1.mp4 ] && ffmpeg -v error -y -i $A/final/s27_1080.mp4 -vf "trim=start_frame=20:end_frame=120,setpts=PTS-STARTPTS" -af "atrim=start=0.8333:end=5,asetpts=PTS-STARTPTS" -c:v libx264 -crf 14 -preset slow -c:a aac $W/clips/s27-t1.mp4 && echo "placed s27 (frames 20-119)"
echo "clips: $(ls $W/clips/s*-t1.mp4 | wc -l)/41"
