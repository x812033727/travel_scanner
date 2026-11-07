#!/usr/bin/env bash
# 收尾守門：run6 進到「等 picks」或點數 < 2.5 CU 就停 run6、關 session（站主 2026-11-07：用完之前就先收尾）
W=/tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/e001
K=/home/user/travel_scanner/.agents/skills/minimax-h3-colab/scripts
while pgrep -f run6.sh >/dev/null; do
  bal=$(bash $K/h3.sh usage 2>/dev/null | tail -1 | python3 -c "import json,sys;print(json.load(sys.stdin).get('balance',99))" 2>/dev/null || echo 99)
  if grep -q "^== waiting for picks" $W/run6.log || python3 -c "import sys;sys.exit(0 if float('$bal')<2.5 else 1)"; then
    echo "== guard: stopping at balance $bal $(date -u +%T)"
    pkill -f run6.sh; pkill -f "refine.py"; pkill -f "runner.py"; sleep 2
    bash $K/h3.sh stop --session tn-e001b; bash $K/bootstrap.sh patch >/dev/null
    bash $K/h3.sh usage | tail -1; break
  fi
  sleep 60
done
echo "== guard: done $(date -u +%T)"
