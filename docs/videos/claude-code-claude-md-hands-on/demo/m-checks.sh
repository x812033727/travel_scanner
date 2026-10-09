#!/usr/bin/env bash
# Every check for the CLAUDE.md video that calls no model, in one go: versions, the seed's
# hashes, the load logger on made-up events, the tally script on made-up streams, the
# arithmetic, and a dry build of each arm's project (no session is started).
#
#   bash <seed>/m-checks.sh > <work>/run/logs/m-checks.log 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="$(cd "$seed/../.." && pwd)"
export LAB="${LAB:-$work/run/md-lab}"
export LOGS="${LOGS:-$work/run/logs}"
cd "$seed" || exit 2

run() { echo "\$ $1"; eval "$1"; echo "[exit $?]"; echo; }

echo "# $(date -u +%Y-%m-%dT%H:%M:%SZ) | every command below is run from <seed>"
echo
run 'claude --version'
run 'node --version'
run 'bash --version | head -1'
run 'find --version | head -1; sort --version | head -1; head --version | head -1'
run "claude --help | grep -E -- '^  --(tools|allowedTools|setting-sources|strict-mcp-config|no-session-persistence|include-hook-events|debug-file|model)[ ,]'"
run 'node measure-seed.mjs'
run 'node check-loaded.mjs'
run 'node check-tally.mjs'
run 'node calc.mjs'
for arm in none team conflict lazy off; do
  run "bash session.sh dry-$arm $arm --dry | sed -n '/^\\\$ find/,/^\\\$ sha256sum/p'"
done
run "bash session.sh dry-team team --dry | sed -n '/^## the session/,\$p'"
run "(cd \"\$LAB\" && cat CLAUDE.md)"
run "bash session.sh dry-lazy lazy --dry > /dev/null; (cd \"\$LAB\" && node --test 'checks/*.check.mjs' 2>&1 | head -5)"
rm -rf "$LAB"
rm -f "$LOGS"/dry-*.session.log
