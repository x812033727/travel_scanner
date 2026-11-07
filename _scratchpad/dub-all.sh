#!/usr/bin/env bash
cd /home/user/travel_scanner
EP=$1; shift
for L in "$@"; do
  echo "##### $L $(date -u +%T)"
  timeout 1700 bash docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub.sh $EP $L 2>&1 | grep -v "^    at" | tail -12
done
echo "##### all done"
