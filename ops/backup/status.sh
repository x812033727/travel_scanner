#!/usr/bin/env bash
# One look at the nightly backup, for the deploy preflight and the host-ops skill:
#
#   bash /opt/travel-scanner-backup/status.sh
#
# Prints the timer's state and backup.py's own status lines (last success and its age, last
# failure, last skip), then `BACKUP STALE: ...` when the last success is older than 36 hours or
# `BACKUP FAILED: ...` when the last run failed after the last success. Exit 1 on either, or
# when no run was ever recorded, so a check or a cron line can use it. Read-only, no secrets.
set -u

BACKUP_PY=${BACKUP_PY:-/opt/travel-scanner-backup/backup.py}
STATE_DIR=${BACKUP_STATE_DIR:-/var/lib/travel-scanner-backup}
TIMER=travel-scanner-backup.timer
SERVICE=travel-scanner-backup.service

if command -v systemctl >/dev/null 2>&1 && systemctl list-unit-files "$TIMER" 2>/dev/null | grep -q "$TIMER"; then
  echo "timer: enabled=$(systemctl is-enabled "$TIMER" 2>/dev/null) active=$(systemctl is-active "$TIMER" 2>/dev/null) run=$(systemctl is-active "$SERVICE" 2>/dev/null)"
  next=$(systemctl show "$TIMER" -p NextElapseUSecRealtime --value 2>/dev/null)
  [ -n "${next:-}" ] && echo "next run: $next"
else
  echo "timer: not installed"
fi

if [ ! -f "$BACKUP_PY" ]; then
  echo "backup: not installed ($BACKUP_PY missing; ops/backup/README.md)"
  exit 1
fi
python3 "$BACKUP_PY" status --state-dir "$STATE_DIR"
