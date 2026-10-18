#!/usr/bin/env bash
# Every check for the MCP video that calls no model, in one go: versions and flags, the seed's
# hashes and widths, the data file against its generator, the server run by hand with JSON-RPC
# messages on its stdin, the logging hook on made-up events, the tally script on made-up
# sessions, the arithmetic, a dry build of each arm's project, the hand test a viewer types, and
# the bookkeeping of session.sh (a name is never overwritten, --dry never touches the records,
# nothing is built inside a git repository, the record carries no user or host name).
# No session is started, and no `claude mcp` subcommand that reads or writes configuration is run.
#
#   WORK=<work> bash <seed>/m-checks.sh > <work>/run/logs/m-checks.txt 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-mcp-hands-on}"
export DRY="${DRY:-$work/run/dry-lab}"
user="$(basename "$HOME")"
cd "$seed" || exit 2

run() { echo "\$ $1"; eval "$1"; echo "[exit $?]"; echo; }

echo "# $(date -u +%Y-%m-%dT%H:%M:%SZ) | every command below is run from <seed>"
echo
run 'claude --version'
run 'node --version'
run 'bash --version | head -1'
run 'find --version | head -1; sort --version | head -1; head --version | head -1; cat --version | head -1'
run "claude --help | grep -E -- '^  --(mcp-config|strict-mcp-config|tools|allowedTools|setting-sources|no-session-persistence|debug-file|model|max-budget-usd)[ ,]' | cut -c1-78"
run "claude mcp --help | grep -E '^  (add|add-json|get|list|remove|reset-project-choices) ' | cut -c1-78"
run 'node measure-seed.mjs'
run 'node gen-stock.mjs --check'
run 'node check-server.mjs'
run 'node check-seen.mjs'
run 'node check-tally.mjs | cut -c1-260'
run 'node calc.mjs | head -5'
for arm in off on noallow miss broken wide wideup files up idle rooted; do
  run "bash session.sh dry-$arm $arm --dry | sed -n '/^\\\$ find/,/^\\\$ sha256sum/p;/^\\\$ cat .mcp.json/,/^}/p;/^## the request/,\$p'"
done
run 'bash session.sh dry-on on --dry'
# What a viewer types before any Claude Code session: the project as it stands, the data file,
# the configuration, and the server answering four messages from a file.
run 'bash session.sh dry-on on --dry > /dev/null; (cd "$DRY" && find . -type f -not -path "./.claude/*" | sort && wc -l server/gear.mjs server/stock.tsv && head -5 server/stock.tsv)'
run '(cd "$DRY" && cat .mcp.json)'
run '(cd "$DRY" && node server/gear.mjs < server/hand.jsonl | cut -c1-68; echo "[node exit ${PIPESTATUS[0]}]"; sed -E "s/\+ *[0-9]+ms/+<n>ms/" server/requests.txt)'
run '(cd "$DRY" && node server/gear.mjs < server/hand.jsonl | tail -1)'
# The command a broken .mcp.json would start, run directly. Node prints the full path of the
# missing file; everything after "Cannot find module" is replaced before it is shown.
gone() {
  (cd "$DRY" && node server/gone.mjs; echo "[node exit $?]") 2>&1 \
    | grep -E '^Error|code:|node exit' | sed -E 's#(Cannot find module).*#\1 <the full path of server/gone.mjs>#'
}
echo '# gone: (cd <lab> && node server/gone.mjs; echo "[node exit $?]"), the lines that start with Error or hold code:'
run 'gone'

# The bookkeeping, with a command that does nothing in place of claude. <scratch> is a
# temporary folder: <scratch>/lab is the project and <scratch>/logs holds the records.
scratch="$(mktemp -d)"
guard() { LAB="$scratch/lab" LOGS="$scratch/logs" CLAUDE=true bash session.sh "$@"; }
records() { (cd "$scratch/logs" && ls | sort | tr '\n' ' '; echo); }
aside() { (cd "$scratch/logs/replaced" && ls */ | sort | tr '\n' ' '; echo); }
run 'guard g1 on > /dev/null 2>&1; records'
run 'guard g1 on > /dev/null; echo "[session.sh exit $?]"; records'
run 'guard g1 on --dry | tail -1; records'
run 'guard g1 on --force 2>&1 > /dev/null | sed -E "s#g1\.[0-9TZ]+#g1.<time>#"; records; aside'
# A run folder inside a git repository is refused before anything is built.
mkdir -p "$scratch/repo" && git -C "$scratch/repo" init -q
run 'LAB="$scratch/repo/lab" LOGS="$scratch/logs" CLAUDE=true bash session.sh g2 on; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'DRY="$scratch/repo/dry" bash session.sh g2 on --dry; echo "[session.sh exit $?]"; ls "$scratch/repo"'
# What the scrubbing leaves of this machine in a record made with the stand-in command: the
# user name anywhere and the host name as a whole word are counted, never printed.
run 'grep -c -i -E "$user|\b${HOSTNAME:-no-host-name}\b" "$scratch/logs/g1.session.txt"; grep -c -E "<lab>|<logs>|<seed>" "$scratch/logs/g1.session.txt"'
run 'sed -n "/^\[the claude command/,\$p" "$scratch/logs/g1.session.txt" | cut -c1-200 | head -40'
rm -rf "$scratch" "$DRY"
