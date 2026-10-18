#!/usr/bin/env bash
# Every check for the subagents video that calls no model, in one go: versions and flags, the
# seed's hashes and widths, the log files against the generator and against a second count, the
# logging hook on made-up events, the tally script on made-up sessions, the arithmetic, a dry
# build of each arm's project, `claude plugin validate` on four of them, and the bookkeeping of
# session.sh (a name is never overwritten, --dry never touches the records, nothing is built
# inside a git repository). No session is started.
#
#   bash <seed>/m-checks.sh > <work>/run/logs/m-checks.log 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-subagents-hands-on}"
export DRY="${DRY:-$work/run/dry-lab}"
user="$(basename "$HOME")"
cd "$seed" || exit 2

run() { echo "\$ $1"; eval "$1"; echo "[exit $?]"; echo; }
# claude plugin validate prints the folder it was given, in this machine's spelling.
mask() { sed -E -e 's#^(Validating [a-z]+( in)?:) .*dry-lab#\1 <lab>#' -e "s#$user#<user>#g" | grep -v '^$'; }
# Builds one arm's project in the dry folder and validates its agents; prints validate's own exit code.
validate() {
  local arm="$1"; shift
  bash session.sh "dry-$arm" "$arm" --dry > /dev/null
  (cd "$DRY" && claude plugin validate "$@" .claude/agents 2>&1; echo "[validate exit $?]") | mask
}

echo "# $(date -u +%Y-%m-%dT%H:%M:%SZ) | every command below is run from <seed>"
echo
run 'claude --version'
run 'node --version'
run 'bash --version | head -1'
run 'find --version | head -1; sort --version | head -1; head --version | head -1; grep --version | head -1'
run "claude --help | grep -E -- '^  --(agents?|tools|allowedTools|setting-sources|strict-mcp-config|no-session-persistence|debug-file|model|max-budget-usd|forward-subagent-text)[ ,]' | cut -c1-78"
run 'claude plugin validate --help | head -4'
run 'node measure-seed.mjs'
run 'node gen-logs.mjs --check'
run 'node check-logs.mjs'
run 'node check-seen.mjs'
run 'node check-tally.mjs | cut -c1-240'
run 'node calc.mjs | head -5'
for arm in inline auto named write claudemd builtin omit broken nodesc; do
  run "bash session.sh dry-$arm $arm --dry | sed -n '/^\\\$ find/,/^\\\$ sha256sum/p;/^## the request/,/^## the session/p;/--tools/p'"
done
run "bash session.sh dry-named named --dry | sed -n '/^## above/,\$p'"
run '(cd "$DRY" && cat .claude/agents/log-scout.md)'
for arm in auto omit broken nodesc; do
  run "validate $arm"
done
run 'validate nodesc --strict'
run 'bash session.sh dry-inline inline --dry > /dev/null; (cd "$DRY" && find . -type f -not -path "./.claude/*" | sort && wc -l logs/*.log | tail -1 && head -8 logs/queue-2026-10-01.log)'

# The bookkeeping, with a command that does nothing in place of claude. <scratch> is a
# temporary folder: <scratch>/lab is the project and <scratch>/logs holds the records.
scratch="$(mktemp -d)"
guard() { LAB="$scratch/lab" LOGS="$scratch/logs" CLAUDE=true bash session.sh "$@"; }
records() { (cd "$scratch/logs" && ls | sort | tr '\n' ' '; echo); }
aside() { (cd "$scratch/logs/replaced" && ls */ | sort | tr '\n' ' '; echo); }
run 'guard g1 inline > /dev/null 2>&1; records'
run 'guard g1 inline > /dev/null; echo "[session.sh exit $?]"; records'
run 'guard g1 inline --dry | tail -1; records'
run 'guard g1 inline --force 2>&1 > /dev/null | sed -E "s#g1\.[0-9TZ]+#g1.<time>#"; records; aside'
# A run folder inside a git repository is refused before anything is built.
mkdir -p "$scratch/repo" && git -C "$scratch/repo" init -q
run 'LAB="$scratch/repo/lab" LOGS="$scratch/logs" CLAUDE=true bash session.sh g2 inline; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'DRY="$scratch/repo/dry" bash session.sh g2 inline --dry; echo "[session.sh exit $?]"; ls "$scratch/repo"'
# What the scrubbing leaves of this machine in a record made with the stand-in command.
run 'grep -c -i -E "$user|$(hostname)" "$scratch/logs/g1.session.log"; grep -c -E "<lab>|<logs>|<seed>" "$scratch/logs/g1.session.log"'
rm -rf "$scratch" "$DRY"
