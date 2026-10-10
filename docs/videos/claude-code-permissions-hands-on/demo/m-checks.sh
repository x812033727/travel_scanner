#!/usr/bin/env bash
# Every check for the permission-rules video that calls no model, in one go: versions and flags,
# the seed's hashes and widths, the logging hook on made-up events, the tally script on made-up
# sessions, the arithmetic, a dry build of each arm's project, what a viewer types before any
# Claude Code session (the failing check, the two scripts, the rules file), and the bookkeeping
# of session.sh (a name is never overwritten, --dry never touches the records, nothing is built
# inside a git repository, a change outside the project is reported, the record carries no user
# or host name).
# No session is started, and nothing that reads, prints or changes a settings file other than
# the seed's own is run.
#
#   WORK=<work> bash <seed>/m-checks.sh > <work>/run/logs/m-checks.txt 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-permissions-hands-on}"
export DRY="${DRY:-$work/run/dry-lab}"
export NPM_CONFIG_UPDATE_NOTIFIER=false
user="$(basename "$HOME")"
cd "$seed" || exit 2

run() { echo "\$ $1"; eval "$1"; echo "[exit $?]"; echo; }

echo "# $(date -u +%Y-%m-%dT%H:%M:%SZ) | every command below is run from <seed>"
echo
run 'claude --version'
run 'node --version; npm --version'
run 'bash --version | head -1'
run 'find --version | head -1; sort --version | head -1; cat --version | head -1; sha256sum --version | head -1; timeout --version | head -1'
run "claude --help | grep -E -- '^  --(tools|allowedTools|disallowedTools|permission-mode|permission-prompts|setting-sources|settings|strict-mcp-config|no-session-persistence|debug-file|model|max-budget-usd)[ ,]' | cut -c1-78"
run "claude --help | grep -A3 -E -- '^  --permission-mode' | cut -c1-110"
run 'node measure-seed.mjs'
run 'node check-seen.mjs'
run 'node check-tally.mjs | cut -c1-230'
run 'node calc.mjs | head -5'
run 'node runner/allow-list.mjs rules/rules.main.json; node runner/allow-list.mjs --count rules/rules.main.json; node runner/allow-list.mjs rules/rules.open.json; node runner/allow-list.mjs --count rules/rules.open.json'
for arm in none with proj local read bash edit byfile; do
  run "bash session.sh dry-$arm $arm --dry | sed -n '/^\\\$ find/,/^\\\$ sha256sum/p;/^\\\$ cat .claude\\/settings.json/,/^## above/p;/^## the session/,\$p'"
done
run 'bash session.sh dry-with with --dry'
run 'bash session.sh dry-local local --dry > /dev/null; node runner/allow-list.mjs --count "$DRY/.claude/settings.local.json"; grep -c seen.mjs "$DRY/.claude/settings.local.json"'
# What a viewer types before any Claude Code session, in the project as the "with" arm builds it.
run 'bash session.sh dry-with with --dry > /dev/null; (cd "$DRY" && find . -type f -not -path "./.claude/hooks/*" -not -name settings.local.json | sort)'
run '(cd "$DRY" && cat .claude/settings.json)'
run '(cd "$DRY" && cat data/rates.csv && cat .env)'
run '(cd "$DRY" && npm test; echo "[npm exit $?]")'
run '(cd "$DRY" && bash scripts/report.sh)'
run '(cd "$DRY" && sum="$(mktemp)" && find . -type f | sort | xargs sha256sum > "$sum"; bash scripts/deploy.sh; sed -E "s/[0-9]{2}:[0-9]{2}:[0-9]{2}Z/<time>Z/" deploy-record.txt; echo "files that differ from before the script ran:"; find . -type f | sort | xargs sha256sum | diff "$sum" - | cut -c1-2,68-; rm "$sum")'
run '(cd "$DRY" && node tools/append.mjs && tail -2 data/rates.csv)'
run 'bash session.sh dry-bash bash --dry > /dev/null; (cd "$DRY" && npm test; echo "[npm exit $?]"; diff <(sed -n 13p "$seed/lab/src/fare.mjs") <(sed -n 13p src/fare.mjs); true)'

# The bookkeeping, with a command that does nothing in place of claude. <scratch> is a
# temporary folder: <scratch>/run/lab is the project and <scratch>/run/logs holds the records.
scratch="$(mktemp -d)"
guard() { LAB="$scratch/run/fare-lab" LOGS="$scratch/run/logs" DRY="$scratch/run/dry-lab" CLAUDE="${STANDIN:-true}" bash session.sh "$@"; }
records() { (cd "$scratch/run/logs" && ls | sort | tr '\n' ' '; echo); }
aside() { (cd "$scratch/run/logs/replaced" && ls */ | sort | tr '\n' ' '; echo); }
run 'guard g1 with > /dev/null 2>&1; records'
run 'guard g1 with > /dev/null; echo "[session.sh exit $?]"; records'
run 'guard g1 with --dry | tail -1; records'
run 'guard g1 with --force 2>&1 > /dev/null | sed -E "s#g1\.[0-9TZ]+#g1.<time>#"; records; aside'
# A run folder inside a git repository is refused before anything is built.
mkdir -p "$scratch/repo" && git -C "$scratch/repo" init -q
run 'LAB="$scratch/repo/lab" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 with; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'DRY="$scratch/repo/dry" bash session.sh g2 with --dry; echo "[session.sh exit $?]"; ls "$scratch/repo"'
# A stand-in that writes one file next to the project: the record must say CHANGED.
printf '#!/usr/bin/env bash\necho intruder > ../intruder.txt\n' > "$scratch/standin.sh"; chmod +x "$scratch/standin.sh"
run 'STANDIN="$scratch/standin.sh" guard g3 none > /dev/null 2>&1; grep -A2 "^## outside the project" "$scratch/run/logs/g3.session.txt" | sed -E "s/[0-9a-f]{16}/<digest>/g"'
run 'grep -A2 "^## outside the project" "$scratch/run/logs/g1.session.txt" | sed -E "s/[0-9a-f]{16}/<digest>/g"'
# What the scrubbing leaves of this machine in a record made with the stand-in command: the
# user name anywhere and the host name as a whole word are counted, never printed.
run 'grep -c -i -E "$user|\b${HOSTNAME:-no-host-name}\b" "$scratch/run/logs/g1.session.txt"; grep -c -E "<lab>|<logs>|<seed>" "$scratch/run/logs/g1.session.txt"'
run 'sed -n "/^\[the claude command/,\$p" "$scratch/run/logs/g1.session.txt" | cut -c1-200 | head -60'
rm -rf "$scratch" "$DRY"
