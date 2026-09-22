#!/usr/bin/env bash
# Read-only survey of the production host before a deploy. Nothing here writes.
#
#   <SSH> -m host-preflight.sh                          file reads only
#   <SSH> "bash -s -- --full" < host-preflight.sh        also driver processes and containers
#
# The file-read half is what the permission classifier has always let through; the --full half
# (ps/docker) has been refused once as a production read, which is why it is opt-in.
# Contains no credentials; the SSH command prefix lives in the operator's own notes.
set -u

HOLD=/root/travel-scanner-deploy.hold
LOCK=/var/lock/travel-scanner-deploy.lock
REPO=/root/travel_scanner
LOGDIR=/root/deploy-logs

echo "== host preflight $(date -u +%FT%TZ) =="

if [ -f "$HOLD" ]; then
  echo "HOLD FILE PRESENT ($HOLD, $(date -u -r "$HOLD" +%FT%TZ)):"
  head -c 600 "$HOLD" | tr '\n' ' '
  echo
else
  echo "hold file: none"
fi

if flock -n "$LOCK" true 2>/dev/null; then
  echo "deploy lock: free"
else
  echo "deploy lock: HELD (a deploy or a release phase is running right now)"
fi

echo "-- rule 1: state.json modified <24h with built_at but no activated_at/failed_at --"
flagged=0
while IFS= read -r state; do
  [ -n "$state" ] || continue
  if grep -q '"built_at"' "$state" && ! grep -q '"activated_at"' "$state" && ! grep -q '"failed_at"' "$state"; then
    echo "FLAGGED $(dirname "$state")  (state.json modified $(date -u -r "$state" +%FT%TZ))"
    flagged=1
  fi
done < <(find /root -maxdepth 2 -path '/root/mokaair-*' -name state.json -mmin -1440 2>/dev/null)
[ "$flagged" -eq 0 ] && echo "none"

echo "-- release dirs touched in the last 24h (any driver type; markers: state.json host-state publisher-state publication-*.json) --"
touched=0
while IFS= read -r dir; do
  [ -n "$dir" ] || continue
  touched=1
  markers=""
  [ -f "$dir/state.json" ] && markers="$markers state.json"
  [ -d "$dir/host-state" ] && markers="$markers host-state"
  [ -d "$dir/publisher-state" ] && markers="$markers publisher-state"
  ls "$dir"/publication-*.json >/dev/null 2>&1 && markers="$markers publication-json"
  echo "$(date -u -r "$dir" +%FT%TZ)  $dir  [${markers# }]"
done < <(find /root -maxdepth 1 -type d -name 'mokaair-*' -mmin -1440 2>/dev/null | sort)
[ "$touched" -eq 0 ] && echo "none"

echo "-- git --"
if [ -d "$REPO/.git" ]; then
  live=$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null)
  echo "live HEAD: $live  $(git -C "$REPO" log -1 --format=%s 2>/dev/null)"
  remote=$(git -C "$REPO" ls-remote origin refs/heads/main 2>/dev/null | cut -c1-7)
  echo "origin/main: ${remote:-unknown}"
  dirty=$(git -C "$REPO" status --porcelain 2>/dev/null | head -5)
  if [ -n "$dirty" ]; then echo "WORK TREE DIRTY (the deploy script refuses):"; echo "$dirty"; else echo "work tree: clean"; fi
else
  echo "repo not found at $REPO"
fi

echo "-- disk --"
df -h / | tail -1

echo "-- last deploy log --"
last=$(ls -t "$LOGDIR"/*.log 2>/dev/null | head -1)
if [ -n "$last" ]; then echo "$last"; tail -3 "$last"; else echo "none"; fi

if [ "${1:-}" = "--full" ]; then
  echo "-- driver processes --"
  pgrep -af 'release[_]host|publish[_]host|deploy[_]release|release[_]phase|publish[_]bundle' || echo "none"
  echo "-- containers --"
  docker compose -f "$REPO/docker-compose.prod.yml" ps --format '{{.Name}}\t{{.Image}}\t{{.Status}}' 2>/dev/null || echo "compose ps failed"
fi
echo "== end =="
