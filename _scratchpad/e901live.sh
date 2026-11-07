#!/usr/bin/env bash
# e001 live action drafts (owner 2026-11-07: 開始拍第1集, cap US$28); retake-run retries on no stock; pod stops after
K=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/h3r-state; mkdir -p "$K"; [ -L ~/.cache/minimax-h3-runpod ] || { mkdir -p ~/.cache; cp -pn ~/.cache/minimax-h3-runpod/session.json "$K/" 2>/dev/null; rm -rf ~/.cache/minimax-h3-runpod; ln -s "$K" ~/.cache/minimax-h3-runpod; }
cd /home/user/travel_scanner
VIDEO_WORKDIR=/root/mokaair-work/videos bash docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh 901 ../live/d1
bash .agents/skills/minimax-h3-runpod/scripts/h3r.sh stop 2>/dev/null
echo "=== e901 live drafts done $(date -u +%T)"
