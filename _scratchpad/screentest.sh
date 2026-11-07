#!/usr/bin/env bash
# live-action screen test (owner approved 2026-11-07, cap US$8): portraits then sets on one pod, then stop it
K=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/h3r-state; mkdir -p "$K"; [ -L ~/.cache/minimax-h3-runpod ] || { mkdir -p ~/.cache; cp -pn ~/.cache/minimax-h3-runpod/session.json "$K/" 2>/dev/null; rm -rf ~/.cache/minimax-h3-runpod; ln -s "$K" ~/.cache/minimax-h3-runpod; }
cd /root/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test
H=/home/user/travel_scanner/.agents/skills/minimax-h3-runpod/scripts/h3r.sh
bash $H images --manifest portraits.json --output-dir out --progress out/progress-portraits.json --keep --label zt-live-screen-test --slug zhong-tian-qu-qi
bash $H images --manifest sets.json --output-dir out --progress out/progress-sets.json --keep --label zt-live-screen-test --slug zhong-tian-qu-qi
bash $H stop
echo "=== screen test done $(date -u +%T)"
