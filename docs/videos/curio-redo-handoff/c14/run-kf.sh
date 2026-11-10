#!/bin/bash
# run-kf.sh SHORT [extra keyframes args...] : waits for other keyframes runs, then draws
S=/tmp/claude-0/-home-user-travel-scanner/da8d724d-688a-5de8-b279-1942feab337d/scratchpad/c14
s=$1; shift; slug=curio-$s-v2; tag=$(date -u +%H%M%S)
while pgrep -f 'cli.mjs keyframes' >/dev/null; do sleep 30; done
cd /home/user/wt-prod; export NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 PLAYWRIGHT_BROWSERS_PATH=/tmp/claude-0/-home-user-travel-scanner/da8d724d-688a-5de8-b279-1942feab337d/scratchpad/pw
for i in 1 2 3; do
  node tools/video/cli.mjs keyframes --slug $slug --takes 3 "$@" > $S/kf-$s.$tag.$i.log 2>&1; rc=$?
  echo "$(date -u +%H:%M:%S) kf $* try$i EXIT $rc" >> $S/run-$s.status
  [ $rc -eq 0 ] || [ $rc -eq 2 ] && break
  grep -qE '502|ECONNRESET|fetch failed|timed out' $S/kf-$s.$tag.$i.log || break
done
echo "$(date -u +%H:%M:%S) KF-DONE $rc" >> $S/run-$s.status
