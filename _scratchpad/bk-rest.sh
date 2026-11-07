#!/usr/bin/env bash
cd /home/user/travel_scanner
while pgrep -f "bk-episode.sh 1" >/dev/null; do sleep 20; done
python3 /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/verify-episode.py zt-live-e001
for x in 2 3 4 5 6; do bash /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/bk-episode.sh $x; python3 /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/verify-episode.py $(printf 'zt-live-e%03d' $x); done
bash /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/bk-episode.sh shared; python3 /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/verify-episode.py zt-shared
python3 /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/coverage.py
echo "=== bk-all-ep done $(date -u +%T)"
