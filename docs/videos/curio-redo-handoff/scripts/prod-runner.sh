#!/bin/bash
S=/tmp/claude-0/-home-user-travel-scanner/da8d724d-688a-5de8-b279-1942feab337d/scratchpad
cd $S/wt-beat; export NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 PLAYWRIGHT_BROWSERS_PATH=$S/pw
touch $S/prod-started.txt
while true; do
  next=$(grep -vxF -f $S/prod-started.txt $S/prod-queue.txt | head -1)
  if [ -n "$next" ] && [ "$(pgrep -fc 'prod-one.sh')" -lt 2 ]; then
    echo "$next" >> $S/prod-started.txt
    nohup bash $S/prod-one.sh $next >> $S/prod-$next.log 2>&1 &
  fi
  [ -z "$next" ] && [ "$(pgrep -fc 'prod-one.sh')" -eq 0 ] && break
  sleep 20
done
echo RUNNER DONE >> $S/prod-runner.log
