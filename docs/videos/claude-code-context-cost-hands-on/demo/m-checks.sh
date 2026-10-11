#!/usr/bin/env bash
# Every check for the context-cost video that calls no model, in one go: versions and flags, the
# seed's hashes, sizes and widths, the reader script on made-up streams, the guard, the note
# hook, the logging hook and the after-session verdict on made-up input, the MCP server run by
# hand, a dry build of each arm, the project's own test, and the bookkeeping of session.sh (a
# name is never overwritten, --dry never touches the records, nothing is built inside a git
# repository even when the path has a space in it, a folder the scripts did not build is never
# deleted, a change outside the project is reported, the record carries no user name, host name
# or address even when stderr spells them, and a run stopped half way leaves a record that is
# already scrubbed).
# No session is started. No plugin is installed, enabled, disabled or listed, no marketplace or
# MCP configuration but the seed's own is read, and no git command is run: the "inside a
# repository" case is a temporary folder with an empty .git folder in it.
#
#   WORK=<work> bash <seed>/m-checks.sh > <work>/run/logs/m-checks.txt 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-context-cost-hands-on}"
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
run "claude --help | grep -E -- '^  --(tools|allowedTools|permission-mode|setting-sources|strict-mcp-config|mcp-config|no-session-persistence|debug-file|model|max-budget-usd|plugin-dir|include-hook-events|output-format|verbose|safe-mode)[ ,]' | cut -c1-78"
run 'node measure-seed.mjs'
run 'node check-ctx-cost.mjs | cut -c1-200'
run 'node check-guard.mjs'
run 'node check-note.mjs'
run 'node check-seen.mjs'
run 'node check-after.mjs | cut -c1-230'
run 'node check-server.mjs | cut -c1-230'
for arm in base memory skill agent mcp hook note plugin all work context slash upfront safe; do
  run "bash session.sh dry-$arm $arm --dry"
done
# What a viewer sees in the project before any session, and that its existing test is a real one.
run 'bash session.sh dry-all all --dry > /dev/null; (cd "$DRY/lab" && find . -type f -not -path "./.claude/hooks/seen.mjs" -not -name settings.local.json | sort)'
run '(cd "$DRY/lab" && cat CLAUDE.md && cat .mcp.json)'
run '(cd "$DRY/lab" && node --test 2>&1 | grep -E "(tests|pass|fail) [0-9]+$|rounds up" | sed -E "s/ [(][0-9.]+ms[)]//")'

# The bookkeeping, with a command that does nothing in place of claude. <scratch> is a
# temporary folder: <scratch>/run/lab is the project and <scratch>/run/logs holds the records.
scratch="$(mktemp -d)"
guard() { LAB="$scratch/run/lab" KIT="$scratch/run/ship-kit" LOGS="$scratch/run/logs" DRY="$scratch/run/dry" CLAUDE="${STANDIN:-true}" bash session.sh "$@"; }
records() { (cd "$scratch/run/logs" && ls | sort | tr '\n' ' '; echo); }
aside() { (cd "$scratch/run/logs/replaced" && ls */ | sort | tr '\n' ' '; echo); }
run 'guard g1 plugin > /dev/null 2>&1; records'
run 'guard g1 plugin > /dev/null; echo "[session.sh exit $?]"; records'
run 'guard g1 plugin --dry | tail -1; records'
run 'guard g1 plugin --force 2>&1 > /dev/null | sed -E "s#g1\.[0-9TZ]+#g1.<time>#"; records; aside'
# A run folder inside a git repository is refused before anything is built. No git command is
# run: an empty .git folder is what the scripts look for.
mkdir -p "$scratch/repo/.git"
run 'LAB="$scratch/repo/lab" KIT="$scratch/run/ship-kit" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 plugin; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'LAB="$scratch/run/lab" KIT="$scratch/repo/ship-kit" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 plugin; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'LAB="$scratch/run/lab" KIT="$scratch/run/ship-kit" LOGS="$scratch/repo/deep/logs" CLAUDE=true bash session.sh g2 plugin; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'DRY="$scratch/repo/dry" bash session.sh g2 plugin --dry; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'bash kit.sh "$scratch/repo/ship-kit"; echo "[kit.sh exit $?]"; ls "$scratch/repo"'
# The same refusal when the path has a space in it: the path is checked whole, not in pieces.
mkdir -p "$scratch/with space/repo/.git"
run 'DRY="$scratch/with space/repo/dry" bash session.sh g2 base --dry; echo "[session.sh exit $?]"; ls "$scratch/with space/repo"'
# A folder that holds something these scripts did not build is refused, and nothing in it is
# deleted: as the project, as the plugin folder of session.sh, and as the folder given to kit.sh.
mkdir -p "$scratch/mine/notes" "$scratch/kept/notes"; echo mine > "$scratch/mine/notes/keep.txt"; echo mine > "$scratch/kept/notes/keep.txt"
run 'LAB="$scratch/mine" KIT="$scratch/run/ship-kit" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 base; echo "[session.sh exit $?]"; ls "$scratch/mine/notes"'
run 'LAB="$scratch/run/lab" KIT="$scratch/kept" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 base; echo "[session.sh exit $?]"; ls "$scratch/kept/notes"'
run 'bash kit.sh "$scratch/kept"; echo "[kit.sh exit $?]"; ls "$scratch/kept/notes"'
# A stand-in that writes one file next to the project and one into the plugin: both must say CHANGED.
printf '#!/usr/bin/env bash\necho intruder > ../intruder.txt\necho intruder > ../ship-kit/scripts/intruder.txt\n' > "$scratch/standin.sh"; chmod +x "$scratch/standin.sh"
run 'STANDIN="$scratch/standin.sh" guard g3 plugin > /dev/null 2>&1; grep -A3 "^## outside the project" "$scratch/run/logs/g3.session.txt" | sed -E "s/[0-9a-f]{16}/<digest>/g"'
run 'grep -A3 "^## outside the project" "$scratch/run/logs/g1.session.txt" | sed -E "s/[0-9a-f]{16}/<digest>/g"'
# What the scrubbing leaves of this machine in a record made with the stand-in command: lines
# with the user name in any letter case, the host name as a whole word, or anything shaped like
# an address are counted, never printed. Then the same count for a stand-in that writes those
# names to stderr in eight spellings (the record keeps the first eight lines of stderr), and the
# number of lines that carry a placeholder instead.
names_left() { grep -c -i -E "$user|\\b${HOSTNAME:-no-host-name}\\b|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}" "$1"; }
run 'names_left "$scratch/run/logs/g1.session.txt"; grep -c -E "<lab>|<plugin>|<logs>|<seed>" "$scratch/run/logs/g1.session.txt"'
run 'STANDIN="$seed/standin-names.sh" guard g4 base > /dev/null 2>&1; grep -E "^\[stream lines" "$scratch/run/logs/g4.session.txt"; names_left "$scratch/run/logs/g4.session.txt"; grep -c -E "^(home|mixed|back|url|upper|host|address|account) .*<(home|user|host|address)>" "$scratch/run/logs/g4.session.txt"'
# A run that is stopped while the session is running: the record it leaves is already scrubbed
# and has no end line. The stand-in only sleeps for 20 seconds; session.sh alone is stopped, by
# its own process id, and nothing else.
printf '#!/usr/bin/env bash\nsleep 20\n' > "$scratch/sleeper.sh"; chmod +x "$scratch/sleeper.sh"
interrupted() {
  LAB="$scratch/run/lab" KIT="$scratch/run/ship-kit" LOGS="$scratch/run/logs" DRY="$scratch/run/dry" CLAUDE="$scratch/sleeper.sh" bash session.sh g5 base > /dev/null 2>&1 &
  local pid=$! waited=0 record="$scratch/run/logs/g5.session.txt"
  while [ ! -f "$scratch/run/logs/g5.stream.jsonl" ] && [ "$waited" -lt 180 ]; do sleep 1; waited=$((waited + 1)); done
  kill -9 "$pid" 2>/dev/null; wait "$pid" 2>/dev/null
  echo "the session had started when session.sh was stopped: $([ -f "$scratch/run/logs/g5.stream.jsonl" ] && echo yes || echo no)"
  echo "g5.session.txt: lines with this machine's names $(names_left "$record") | lines with a placeholder $(grep -c -E "<lab>|<logs>|<seed>" "$record") | an end line: $(grep -c "^# g5 | end" "$record")"
  sleep 24   # the sleeper ends by itself; only then can the scratch folder be removed
}
run 'interrupted'
run 'sed -n "/^\[the claude command/,\$p" "$scratch/run/logs/g1.session.txt" | cut -c1-200 | head -70'
rm -rf "$scratch" "$DRY"
