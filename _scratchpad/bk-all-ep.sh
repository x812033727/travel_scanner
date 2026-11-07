#!/usr/bin/env bash
cd /home/user/travel_scanner
run() { bash /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/bk-episode.sh "$@"; b=$( [ "$1" = shared ] && echo zt-shared || { [ "$1" = old ] && echo zt-live-e$2 || printf 'zt-live-e%03d' $1; } ); python3 /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/verify-episode.py $b; }
for x in 1 2 3 4 5 6; do run $x; done
for e in $(ls -d /root/mokaair-work/videos/zhong-tian-qu-qi-e0[0-9][0-9] | grep -oE '[0-9]{3}$'); do run old $e; done
run shared
python3 /tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad/coverage.py
echo "=== bk-all-ep done $(date -u +%T)"
