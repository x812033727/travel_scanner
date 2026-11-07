#!/usr/bin/env bash
cd /home/user/travel_scanner
for x in shared 1 2 3 4 5 6; do
  bash /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/bk-episode.sh $x
  python3 /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/verify-episode.py $x
done
echo "=== bk-all-ep done $(date -u +%T)"
