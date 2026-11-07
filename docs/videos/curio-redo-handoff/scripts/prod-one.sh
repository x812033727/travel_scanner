#!/bin/bash
S=/tmp/claude-0/-home-user-travel-scanner/da8d724d-688a-5de8-b279-1942feab337d/scratchpad
cd $S/wt-beat; export NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 PLAYWRIGHT_BROWSERS_PATH=$S/pw
s=$1
for step in "keyframes --takes 3" "tts"; do echo "== $s $step $(date +%T)"; node tools/video/cli.mjs $step --slug $s; echo "STEP ${step%% *} exit $?"; done
echo "ONE DONE $s"
