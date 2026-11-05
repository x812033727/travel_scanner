#!/usr/bin/env bash
set -u
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
A=/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh/colab/a
export COLAB_GPU=G4
echo "start $(date -u +%FT%TZ)"
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
bash $K/h3.sh start --session zt33 2>&1 | tail -1
colab sessions 2>&1 | grep "zt33"
colab sessions 2>&1 | grep -q "zt33.*Hardware: G4" || { echo "NOT G4"; bash $K/h3.sh stop --session zt33; exit 3; }
cd $A/st2
for p in a b c; do
  echo "refine-$p $(date -u +%T)"
  bash $K/h3.sh refine --manifest st2$p.json --output-dir refined-$p --progress refined-$p/progress.json --session zt33 | tail -1
  echo "refine-$p exit=${PIPESTATUS[0]} $(date -u +%T)"
done
mkdir -p $A/final
for p in a b c; do
  echo "upscale-$p $(date -u +%T)"
  bash $K/h3.sh upscale --input-dir refined-$p --output-dir $A/final --session zt33 | tail -1
  echo "upscale-$p exit=${PIPESTATUS[0]} $(date -u +%T)"
done
bash $K/h3.sh stop --session zt33 2>&1 | tail -1
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
echo "end $(date -u +%FT%TZ)"
echo ALL_DONE
