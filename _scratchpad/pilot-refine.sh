K=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/h3r-state; mkdir -p "$K"; [ -L ~/.cache/minimax-h3-runpod ] || { mkdir -p ~/.cache; cp -pn ~/.cache/minimax-h3-runpod/session.json "$K/" 2>/dev/null; rm -rf ~/.cache/minimax-h3-runpod; ln -s "$K" ~/.cache/minimax-h3-runpod; }
cd /root/mokaair-work/videos/_live-pilot/zhong-tian-qu-qi-e901-dh/runpod/a; mkdir -p st2/refined
for i in $(seq 1 40); do bash /home/user/travel_scanner/.agents/skills/minimax-h3-runpod/scripts/h3r.sh refine --manifest st2/st2-1.json --output-dir st2/refined --progress st2/refined/progress.json --label zt-live-pilot-refine --slug zhong-tian-qu-qi && [ $(ls st2/refined/*.mp4 2>/dev/null | wc -l) -ge 3 ] && break; echo "=== retry $i $(date -u +%T)"; sleep 180; done
bash /home/user/travel_scanner/.agents/skills/minimax-h3-runpod/scripts/h3r.sh stop 2>/dev/null
echo "=== pilot refine done $(date -u +%T)"
