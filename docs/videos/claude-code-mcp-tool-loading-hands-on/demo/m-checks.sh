#!/usr/bin/env bash
# Every check for the MCP tool-loading video that calls no model, in one go: versions and flags,
# the seed's hashes, sizes and widths, the MCP server run by hand with the size of its
# definitions for each N, the reader script on made-up streams, the logging hook, the
# after-session readers and the rule script on made-up records, a dry build of every arm, and
# the bookkeeping of session.sh (a name is never overwritten, --dry never touches the records,
# nothing is built inside a git repository even when the path has a space in it, a folder the
# script did not build is never deleted, a session is refused when the API host is not
# anthropic.com, a change outside the project is reported, the record carries no user name, host
# name or address even when stderr spells them, and a run stopped half way leaves a record that
# is already scrubbed).
# No session is started. No plugin is installed, enabled, disabled or listed, no MCP
# configuration but the seed's own is read, and no git command is run: the "inside a
# repository" case is a temporary folder with an empty .git folder in it.
#
#   WORK=<work> bash <seed>/m-checks.sh > <work>/_tools/logs/m-checks.txt 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-mcp-tool-loading-hands-on}"
export WORK="$work"
export DRY="${DRY:-$work/run/dry}"
user="$(basename "$HOME")"
cd "$seed" || exit 2

run() { echo "\$ $1"; eval "$1"; echo "[exit $?]"; echo; }

echo "# $(date -u +%Y-%m-%dT%H:%M:%SZ) | every command below is run from <seed>"
echo
run 'claude --version'
run 'node --version'
run 'bash --version | head -1'
run 'find --version | head -1; sort --version | head -1; sha256sum --version | head -1; timeout --version | head -1'
run "claude --help | grep -E -- '^  --(tools|allowedTools|permission-mode|setting-sources|strict-mcp-config|mcp-config|no-session-persistence|debug-file|model|max-budget-usd|include-hook-events|output-format|verbose)[ ,]' | cut -c1-78"
run 'node measure-seed.mjs'
run 'node check-server.mjs | cut -c1-330'
run 'node check-ctx-cost.mjs | cut -c1-200'
run 'node check-seen.mjs | cut -c1-200'
run 'node check-after.mjs | cut -c1-330'
for arm in base off d2 d10 d40 u2 u10 u40 use-d40 use-u40 d0 a40 on; do
  run "bash session.sh dry-$arm $arm --dry"
done
run 'bash session.sh dry-bad d5 --dry; bash session.sh dry-bad use-d0 --dry'
# What a viewer sees in the project before any session.
run 'bash session.sh dry-d10 d10 --dry > /dev/null; (cd "$DRY/lab" && find . -type f | sort && cat .mcp.json)'

# The bookkeeping, with a command that does nothing in place of claude. <scratch> is a
# temporary folder: <scratch>/run/lab is the project and <scratch>/run/logs holds the records.
scratch="$(mktemp -d)"
guard() { LAB="$scratch/run/lab" LOGS="$scratch/run/logs" DRY="$scratch/run/dry" CLAUDE="${STANDIN:-true}" bash session.sh "$@"; }
records() { (cd "$scratch/run/logs" && ls | sort | tr '\n' ' '; echo); }
aside() { (cd "$scratch/run/logs/replaced" && ls */ | sort | tr '\n' ' '; echo); }
run 'guard g1 d10 > /dev/null 2>&1; records'
run 'guard g1 d10 > /dev/null; echo "[session.sh exit $?]"; records'
run 'guard g1 d10 --dry | tail -1; records'
run 'guard g1 d10 --force 2>&1 > /dev/null | sed -E "s#g1\.[0-9TZ]+#g1.<time>#"; records; aside'
# A run folder inside a git repository is refused before anything is built. No git command is
# run: an empty .git folder is what the script looks for.
mkdir -p "$scratch/repo/.git"
run 'LAB="$scratch/repo/lab" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 d10; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'LAB="$scratch/run/lab" LOGS="$scratch/repo/deep/logs" CLAUDE=true bash session.sh g2 d10; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'DRY="$scratch/repo/dry" bash session.sh g2 d10 --dry; echo "[session.sh exit $?]"; ls "$scratch/repo"'
# The same refusal when the path has a space in it: the path is checked whole, not in pieces.
mkdir -p "$scratch/with space/repo/.git"
run 'DRY="$scratch/with space/repo/dry" bash session.sh g2 base --dry; echo "[session.sh exit $?]"; ls "$scratch/with space/repo"'
# A folder that holds something this script did not build is refused, and nothing in it is deleted.
mkdir -p "$scratch/mine/notes"; echo mine > "$scratch/mine/notes/keep.txt"
run 'LAB="$scratch/mine" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 base; echo "[session.sh exit $?]"; ls "$scratch/mine/notes"'
# An API host that is not anthropic.com: no session is started (tool search would be off by default).
run 'ANTHROPIC_BASE_URL=http://localhost:9 guard g2 d10; echo "[session.sh exit $?]"; records'
# A stand-in that writes one file next to the project and adds a line to another run's record:
# both must say CHANGED.
printf '#!/usr/bin/env bash\necho intruder > ../intruder.txt\necho intruder >> ../logs/g1.seen.txt\n' > "$scratch/standin.sh"; chmod +x "$scratch/standin.sh"
run 'STANDIN="$scratch/standin.sh" guard g3 d10 > /dev/null 2>&1; grep -A4 "^## outside the project" "$scratch/run/logs/g3.session.txt" | sed -E "s/[0-9a-f]{16}/<digest>/g"'
run 'grep -A4 "^## outside the project" "$scratch/run/logs/g1.session.txt" | sed -E "s/[0-9a-f]{16}/<digest>/g"'
# What the scrubbing leaves of this machine in a record made with the stand-in command: lines
# with the user name in any letter case, the host name as a whole word, or anything shaped like
# an address are counted, never printed. Then the same count for a stand-in that writes those
# names to stderr in eight spellings (the record keeps the first eight lines of stderr), and the
# number of lines that carry a placeholder instead.
names_left() { grep -c -i -E "$user|\\b${HOSTNAME:-no-host-name}\\b|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}" "$1"; }
run 'names_left "$scratch/run/logs/g1.session.txt"; grep -c -E "<lab>|<logs>|<seed>" "$scratch/run/logs/g1.session.txt"'
run 'STANDIN="$seed/standin-names.sh" guard g4 base > /dev/null 2>&1; grep -E "^\[stream lines" "$scratch/run/logs/g4.session.txt"; names_left "$scratch/run/logs/g4.session.txt"; grep -c -E "^(home|mixed|back|url|upper|host|address|account) .*<(home|user|host|address)>" "$scratch/run/logs/g4.session.txt"'
# A run that is stopped while the session is running: the record it leaves is already scrubbed
# and has no end line. The stand-in only sleeps for 20 seconds; session.sh alone is stopped, by
# its own process id, and nothing else.
printf '#!/usr/bin/env bash\nsleep 20\n' > "$scratch/sleeper.sh"; chmod +x "$scratch/sleeper.sh"
interrupted() {
  LAB="$scratch/run/lab" LOGS="$scratch/run/logs" DRY="$scratch/run/dry" CLAUDE="$scratch/sleeper.sh" bash session.sh g5 base > /dev/null 2>&1 &
  local pid=$! waited=0 record="$scratch/run/logs/g5.session.txt"
  while [ ! -f "$scratch/run/logs/g5.stream.jsonl" ] && [ "$waited" -lt 180 ]; do sleep 1; waited=$((waited + 1)); done
  kill -9 "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
  echo "the session had started when session.sh was stopped: $([ -f "$scratch/run/logs/g5.stream.jsonl" ] && echo yes || echo no)"
  echo "g5.session.txt: lines with this machine's names $(names_left "$record") | lines with a placeholder $(grep -c -E "<lab>|<logs>|<seed>" "$record") | an end line: $(grep -c "^# g5 | end" "$record")"
  sleep 24   # the sleeper ends by itself; only then can the scratch folder be removed
}
run 'interrupted'
run 'sed -n "/^\[the claude command/,\$p" "$scratch/run/logs/g1.session.txt" | cut -c1-200 | head -60'
# Only what the dry runs above built is removed from <dry>: the project they built and the
# canary next to it. The folder itself goes only if that leaves it empty, so a DRY that was
# pointed at a folder holding anything else keeps it.
rm -rf "$scratch" "$DRY/lab"
rm -f "$DRY/canary.txt"
rmdir "$DRY" 2>/dev/null || true
