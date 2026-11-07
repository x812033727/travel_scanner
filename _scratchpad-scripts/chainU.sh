#!/usr/bin/env bash
# after chainT: e902 fix3 (12 redesigned shots / 24 drafts)
K=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/h3r-state; mkdir -p "$K"; [ -L ~/.cache/minimax-h3-runpod ] || { mkdir -p ~/.cache; cp -pn ~/.cache/minimax-h3-runpod/session.json "$K/" 2>/dev/null; rm -rf ~/.cache/minimax-h3-runpod; ln -s "$K" ~/.cache/minimax-h3-runpod; }
cd /home/user/travel_scanner
while pgrep -f "chainR.sh|chainS.sh|chainT.sh" >/dev/null; do sleep 60; done
KEEP=1 bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 902 fix3
echo "=== e902 fix3 done $(date -u +%T)"
