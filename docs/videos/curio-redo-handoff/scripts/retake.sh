#!/bin/bash
S=/tmp/claude-0/-home-user-travel-scanner/da8d724d-688a-5de8-b279-1942feab337d/scratchpad
cd $S/wt-beat
export NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 PLAYWRIGHT_BROWSERS_PATH=$S/pw
s=$1
until grep -q "STEP tts exit" $S/prod-$s.log; do sleep 20; done
echo "== retake $s $(date +%T)"
node tools/video/cli.mjs keyframes --slug $s --takes 3 --seed-offset 3
echo "RETAKE exit $?"
