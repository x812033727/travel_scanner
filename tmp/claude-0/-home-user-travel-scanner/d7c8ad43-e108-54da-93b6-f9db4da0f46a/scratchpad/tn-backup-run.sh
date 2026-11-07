#!/usr/bin/env bash
for ep in 001 002 003; do MIN_FILES=$([ $ep = 003 ] && echo 20 || echo 200) bash /tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/tn-backup-ep.sh $ep 2>&1 | tail -2; done
bash /tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/tn-backup-series.sh 2>&1 | tail -1
echo "== backups done $(date -u +%T)"
