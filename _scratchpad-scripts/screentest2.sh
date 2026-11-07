#!/usr/bin/env bash
# live-action screen test v2 (text-only, grey canvas as image 1), then stop the pod
K=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/h3r-state; mkdir -p "$K"; [ -L ~/.cache/minimax-h3-runpod ] || { mkdir -p ~/.cache; cp -pn ~/.cache/minimax-h3-runpod/session.json "$K/" 2>/dev/null; rm -rf ~/.cache/minimax-h3-runpod; ln -s "$K" ~/.cache/minimax-h3-runpod; }
cd /root/mokaair-work/videos/_series/zhong-tian-qu-qi/live-screen-test-v2
H=/home/user/travel_scanner/.agents/skills/minimax-h3-runpod/scripts/h3r.sh
for m in portraits figures sets; do bash $H images --manifest $m.json --output-dir out --progress out/progress-$m.json --keep --label zt-live-screen-test --slug zhong-tian-qu-qi; done
bash $H stop
echo "=== screen test v2 done $(date -u +%T)"
