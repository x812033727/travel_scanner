#!/usr/bin/env bash
# the remaining retake queue after a container restart (finished outputs are skipped); the pod stays up for the refines
# keep the pod gate token where a container restart cannot take it
K=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/h3r-state; mkdir -p "$K"; [ -L ~/.cache/minimax-h3-runpod ] || { mkdir -p ~/.cache; cp -pn ~/.cache/minimax-h3-runpod/session.json "$K/" 2>/dev/null; rm -rf ~/.cache/minimax-h3-runpod; ln -s "$K" ~/.cache/minimax-h3-runpod; }
cd /home/user/travel_scanner
R=docs/videos/series-plans/zhong-tian-qu-qi/production/colab/runs/_scripts/retake-run.sh
for job in "904 fix1" "903 fix3" "902 fix2" "901 fix3" "906 fix1" "905 fix2"; do
  set -- $job
  KEEP=1 PREFLIGHT=0 bash $R $1 $2
  echo "=== e$1 $2 done $(date -u +%T)"
done
echo "=== queue done $(date -u +%T)"
