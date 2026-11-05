#!/usr/bin/env bash
set -u
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
M=/root/mokaair-work/videos/zhong-tian-qu-qi-e033-dh/colab/a/st1
export COLAB_GPU=G4
cd $M
echo "start $(date -u +%FT%TZ)"
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
H3_PROFILE=hero bash $K/bootstrap.sh patch 2>&1 | grep -o "profile=[a-z]*"
bash $K/h3.sh start --session zt33 2>&1 | tail -1
colab sessions 2>&1 | head -1
colab sessions 2>&1 | grep -q "zt33.*Hardware: G4" || { echo "NOT G4, stopping"; bash $K/h3.sh stop --session zt33; exit 3; }
for p in 1 2 3; do
  echo "part$p $(date -u +%T)"
  bash $K/h3.sh batch --manifest ref-e033-part$p.json --output-dir out --progress out/progress-part$p.json --session zt33
  echo "part$p exit=$? $(date -u +%T)"
done
bash $K/h3.sh stop --session zt33 2>&1 | tail -1
python3 ~/.cache/minimax-h3-colab-skill/scripts/runner.py usage --json | tail -1
echo "end $(date -u +%FT%TZ)"
echo ALL_DONE
