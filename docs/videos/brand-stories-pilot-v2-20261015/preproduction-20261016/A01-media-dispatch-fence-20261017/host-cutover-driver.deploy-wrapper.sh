#!/usr/bin/env bash
# Deploy wrapper for the production host. Run it there with the deploy script's own flags:
#
#   <SSH> "bash -s --" < host-deploy.sh
#   <SSH> "bash -s -- --force" < host-deploy.sh
#   <SSH> "bash -s -- --ignore-hold" < host-deploy.sh      only after the owner chose that
#
# Always from a background shell call: a foreground call can hit the tool timeout and drop the
# SSH session mid-deploy. The wrapper runs the script under nohup so a dropped session cannot
# kill the deploy, waits for it, prints the tail of its log without buildkit noise, and ends
# with DEPLOY_EXIT=<code>.
#
# It refuses (exit 9) before touching anything when the hold file exists and --ignore-hold was
# not given, or when the deploy lock is held. --ignore-hold bypasses the deploy script's own
# guard for a hold that appeared after your survey too, which is why this check runs first.
# No pgrep for the script name: this text contains it, and plink sends the whole script as one
# command line, so a process match would find itself. Contains no credentials.
set -u

HOLD=/root/travel-scanner-deploy.hold
LOCK=/var/lock/travel-scanner-deploy.lock
SCRIPT=/root/deploy-travel-scanner.sh
LOGDIR=/root/deploy-logs

ignore=0
for arg in "$@"; do
  [ "$arg" = "--ignore-hold" ] && ignore=1
done

if [ -f "$HOLD" ] && [ "$ignore" -eq 0 ]; then
  echo "REFUSING: hold file present ($HOLD):"
  head -c 600 "$HOLD" | tr '\n' ' '
  echo
  echo "Judge it with references/preflight.md; rerun with --ignore-hold only after the owner chose that."
  exit 9
fi
if ! flock -n "$LOCK" true 2>/dev/null; then
  echo "REFUSING: deploy lock $LOCK is held (a deploy or a release phase is running)"
  exit 9
fi
if [ ! -x "$SCRIPT" ]; then
  echo "REFUSING: $SCRIPT is missing or not executable"
  exit 9
fi

mkdir -p "$LOGDIR"
out="$LOGDIR/wrapper-$(date -u +%Y%m%d_%H%M%S).log"
echo "starting: $SCRIPT $* (wrapper log $out)"
nohup "$SCRIPT" "$@" >"$out" 2>&1 &
pid=$!
wait "$pid"
code=$?
grep -v -E '^#[0-9]+ ' "$out" | tail -60
echo "DEPLOY_EXIT=$code"
exit "$code"
