#!/usr/bin/env bash
# Every check for the Skills video that calls no model, in one go: versions, the seed's hashes
# and widths, the logging hook on made-up events, the tally script on made-up sessions, the
# arithmetic, a dry build of each arm's project, `claude plugin validate` on six of them, and
# the bookkeeping of session.sh (a name is never overwritten, --dry never touches the records).
# No session is started.
#
#   bash <seed>/m-checks.sh > <work>/run/logs/m-checks.log 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-skills-hands-on}"
export DRY="${DRY:-$work/run/dry-lab}"
user="$(basename "$HOME")"
cd "$seed" || exit 2

run() { echo "\$ $1"; eval "$1"; echo "[exit $?]"; echo; }
# claude plugin validate prints the folder it was given, in this machine's spelling.
mask() { sed -E -e 's#^(Validating [a-z]+( in)?:) .*dry-lab#\1 <lab>#' -e "s#$user#<user>#g" | grep -v '^$'; }
# Builds one arm's project in the dry folder and validates its skills; prints validate's own exit code.
validate() {
  local arm="$1"; shift
  bash session.sh "dry-$arm" "$arm" --dry > /dev/null
  (cd "$DRY" && claude plugin validate "$@" .claude/skills 2>&1; echo "[validate exit $?]") | mask
}

echo "# $(date -u +%Y-%m-%dT%H:%M:%SZ) | every command below is run from <seed>"
echo
run 'claude --version'
run 'node --version'
run 'bash --version | head -1'
run 'find --version | head -1; sort --version | head -1; head --version | head -1; grep --version | head -1'
run "claude --help | grep -E -- '^  --(tools|allowedTools|setting-sources|strict-mcp-config|no-session-persistence|debug-file|model|disable-slash-commands)[ ,]' | cut -c1-78"
run 'claude plugin validate --help | head -4'
run 'node measure-seed.mjs'
run 'node check-seen.mjs'
run 'node check-tally.mjs'
run 'node calc.mjs'
for arm in none skill vague slash claudemd overlap broken typo flat; do
  run "bash session.sh dry-$arm $arm --dry | sed -n '/^\\\$ find/,/^\\\$ sha256sum/p'"
done
run "bash session.sh dry-skill skill --dry | sed -n '/^## above/,\$p' | grep -v -E '^(ANTHROPIC|CLAUDE)[A-Z_]* '"
run '(cd "$DRY" && cat .claude/skills/release-prep/SKILL.md)'
run '(cd "$DRY" && cat .claude/skills/release-prep/template.md)'
for arm in skill vague overlap broken typo flat; do
  run "validate $arm"
done
run 'validate typo --strict'
run 'bash session.sh dry-none none --dry > /dev/null; (cd "$DRY" && find . -type f -not -path "./.claude/*" | sort)'

# The bookkeeping, with a command that does nothing in place of claude. <scratch> is a
# temporary folder: <scratch>/lab is the project and <scratch>/logs holds the records.
scratch="$(mktemp -d)"
guard() { LAB="$scratch/lab" LOGS="$scratch/logs" CLAUDE=true bash session.sh "$@"; }
records() { (cd "$scratch/logs" && ls | sort | tr '\n' ' '; echo); }
aside() { (cd "$scratch/logs/replaced" && ls */ | sort | tr '\n' ' '; echo); }
run 'guard g1 none > /dev/null 2>&1; records'
run 'guard g1 none > /dev/null; echo "[session.sh exit $?]"; records'
run 'guard g1 none --dry | tail -1; records'
run 'guard g1 none --force 2>&1 > /dev/null | sed -E "s#g1\.[0-9TZ]+#g1.<time>#"; records; aside'
rm -rf "$scratch" "$DRY"
