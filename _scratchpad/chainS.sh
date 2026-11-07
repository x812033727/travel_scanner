#!/usr/bin/env bash
# after chainR: e904 fix2 (10 shots / 20 drafts from the independent pick)
# keep the pod gate token where a container restart cannot take it
K=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/h3r-state; mkdir -p "$K"; [ -L ~/.cache/minimax-h3-runpod ] || { mkdir -p ~/.cache; cp -pn ~/.cache/minimax-h3-runpod/session.json "$K/" 2>/dev/null; rm -rf ~/.cache/minimax-h3-runpod; ln -s "$K" ~/.cache/minimax-h3-runpod; }
cd /home/user/travel_scanner
while pgrep -f chainR.sh >/dev/null; do sleep 60; done
R=docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh
KEEP=1 bash $R 904 fix2
echo "=== e904 fix2 done $(date -u +%T)"
