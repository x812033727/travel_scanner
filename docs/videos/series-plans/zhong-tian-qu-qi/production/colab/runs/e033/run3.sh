#!/usr/bin/env bash
# stage 3 in batches of five, each with a time limit and up to three tries
set -u
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh/colab/a
export COLAB_GPU=G4
S=zt33u
echo "start $(date -u +%FT%TZ)"
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
ensure() { colab sessions 2>&1 | grep -q "$S.*Hardware: G4" || bash $K/h3.sh start --session $S 2>&1 | tail -1; colab sessions 2>&1 | grep -q "$S.*Hardware: G4"; }
ensure || { echo "NOT G4"; exit 3; }
cd $A/st3
for d in up-*; do
  for try in 1 2 3; do
    left=0; for f in $d/*.mp4; do n=$(basename ${f%.mp4}); [ -f $A/final/${n}_1080.mp4 ] || left=$((left+1)); done
    [ $left -eq 0 ] && break
    ensure || { echo "session lost, cannot restart"; break 2; }
    echo "$d try $try ($left left) $(date -u +%T)"
    timeout 1800 bash $K/h3.sh upscale --input-dir $d --output-dir $A/final --session $S --timeout 1500 2>&1 | tail -1
    echo "$d exit=$? $(date -u +%T)"
  done
done
echo "have $(ls $A/final/*_1080.mp4 2>/dev/null | wc -l)/38"
bash $K/h3.sh stop --session $S 2>&1 | tail -1
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
echo "end $(date -u +%FT%TZ)"
echo ALL_DONE
