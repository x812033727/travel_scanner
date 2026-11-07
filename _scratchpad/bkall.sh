#!/usr/bin/env bash
# full backup of every r2 work folder + series refs (2026-11-07), then verify each against the disk
S=/tmp/claude-0/-home-user-travel-scanner/920e1ef4-ec17-537b-bdd8-529e9301e4f3/scratchpad
cd /home/user/travel_scanner
for n in 1 2 3 4 5 6; do
  dirs="zhong-tian-qu-qi-e90$n-dh"; [ -d ~/mokaair-work/videos/zhong-tian-qu-qi-e00$n-r2 ] && dirs="$dirs zhong-tian-qu-qi-e00$n-r2"
  bash $S/bk-media.sh zt-e90$n-media-20261107 $dirs
  echo "VERIFY e90$n $(python3 $S/verify-bk.py zt-e90$n-media-20261107 $dirs 2>&1 | tail -1)"
done
bash $S/bk-media.sh zt-series-media-20261107 _series
echo "VERIFY series $(python3 $S/verify-bk.py zt-series-media-20261107 _series 2>&1 | tail -1)"
echo "=== bkall done $(date -u +%T)"
