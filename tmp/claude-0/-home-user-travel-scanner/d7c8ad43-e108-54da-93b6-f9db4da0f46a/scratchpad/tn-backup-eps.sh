#!/usr/bin/env bash
for ep in 001 002 003; do MIN_FILES=20 bash /tmp/claude-0/-home-user-travel-scanner/d7c8ad43-e108-54da-93b6-f9db4da0f46a/scratchpad/tn-backup-ep.sh $ep 2>&1 | tail -1; done
echo "== ep backups done $(date -u +%T)"
