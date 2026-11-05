#!/bin/bash
# Detached episode run: part 1 then part 2 on the same Colab session.
cd /root/mokaair-work/videos/zhong-tian-qu-qi-e031-dh/colab/ref || exit 2
W=/root/mokaair-work/videos/zhong-tian-qu-qi-e031-dh
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
L=$W/colab/ref/run-episode.log
date -u > $L
for p in 1 2; do
  bash $K/h3.sh batch --manifest $W/colab/ref/ref-e031-part$p.json --output-dir $W/clips --progress $W/colab/ref/ref-e031-part$p.progress.json --session zt31 --timeout 21600 >> $L 2>&1
  echo "part$p exit $?" >> $L; date -u >> $L
done
echo "episode done" >> $L
