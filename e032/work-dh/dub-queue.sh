#!/bin/bash
# Run dub.sh for every locale whose translation exists and whose track does not, one at a time.
R=/home/user/travel_scanner; D=$R/docs/videos/zhong-tian-qu-qi-e032; C=/root/mokaair-work/videos/zhong-tian-qu-qi-e032-dh/cut
cd $R
for l in en ja ko es pt id vi th; do
  [ -f $D/dub.$l.json ] || continue
  [ -f $C/e032-dh.$l.m4a ] && continue
  echo "=== $l $(date -u +%H:%M)"; bash docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub.sh 032 $l 2>&1 | tail -4; echo "=== $l exit ${PIPESTATUS[0]}"
done
echo "queue end $(date -u +%H:%M)"
