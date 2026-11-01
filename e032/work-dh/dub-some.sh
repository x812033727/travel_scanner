#!/bin/bash
# dub-some.sh <locales...> : run dub.sh 032 for each, one at a time
cd /home/user/travel_scanner
for l in "$@"; do echo "=== $l $(date -u +%H:%M)"; bash docs/videos/series-plans/zhong-tian-qu-qi/production/hailuo/local/dub.sh 032 $l 2>&1 | grep -E "do not fit|^zq32|lines, |recorded|exit" ; echo "=== $l exit ${PIPESTATUS[0]}"; done; echo "queue end $(date -u +%H:%M)"
