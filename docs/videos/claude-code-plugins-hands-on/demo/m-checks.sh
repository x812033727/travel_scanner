#!/usr/bin/env bash
# Every check for the plugins video that calls no model, in one go: versions and flags, the
# seed's hashes and widths, the guard, the logging hook and the tally on made-up input, the
# arithmetic, a dry build of each arm, the plugin made by hand from project A's .claude/ with the
# commands a viewer types (and compared with the one kit.sh builds), claude plugin validate on
# the good plugin and on eleven broken variants, and the bookkeeping of session.sh (a name is
# never overwritten, --dry never touches the records, nothing is built inside a git repository,
# a change outside the project or inside the plugin is reported, the record carries no user or
# host name).
# No session is started. No plugin is installed, enabled, disabled or listed, no marketplace is
# touched, and no settings file but the seed's own is read.
#
#   WORK=<work> bash <seed>/m-checks.sh > <work>/run/logs/m-checks.txt 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-plugins-hands-on}"
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
run 'find --version | head -1; sort --version | head -1; sha256sum --version | head -1; timeout --version | head -1; diff --version | head -1'
run "claude --help | grep -E -- '^  --(tools|allowedTools|permission-mode|setting-sources|strict-mcp-config|no-session-persistence|debug-file|model|max-budget-usd|plugin-dir|include-hook-events)[ ,]' | cut -c1-78"
run "claude --help | grep -A4 -E -- '^  --plugin-dir' | cut -c1-110"
run 'claude plugin validate --help'
run 'node measure-seed.mjs'
run 'node check-guard.mjs'
run 'node check-seen.mjs'
run 'node check-tally.mjs | cut -c1-230'
run 'node calc.mjs | head -5'
for arm in bare kit origin both guard stale strict slash short; do
  run "bash session.sh dry-$arm $arm --dry"
done

# The plugin made by hand from project A's .claude/, with the commands the official "Convert an
# existing .claude/ setup" section gives. The next commands are typed in project A (<lab>, as the
# origin arm builds it), the way a viewer would type them; the plugin lands next to the project.
run 'bash session.sh dry-origin origin --dry > /dev/null; ls "$DRY"'
(
  cd "$DRY/lab" || exit 2
  echo "# in <lab> (project A):"
  run 'find .claude -type f -not -name seen.mjs -not -name settings.local.json | sort'
  run 'mkdir -p ../ship-kit/.claude-plugin ../ship-kit/hooks ../ship-kit/scripts'
  run 'cp -r .claude/skills .claude/agents ../ship-kit/'
  run 'cp .claude/hooks/guard.mjs ../ship-kit/scripts/'
  # The viewer types the eight lines of the manifest; here they are copied from the seed.
  run 'cp "$seed/parts/manifest.json" ../ship-kit/.claude-plugin/plugin.json; cat ../ship-kit/.claude-plugin/plugin.json'
  run "sed 's#\${CLAUDE_PROJECT_DIR}/.claude/hooks/#\${CLAUDE_PLUGIN_ROOT}/scripts/#' .claude/settings.json > ../ship-kit/hooks/hooks.json"
  run 'diff .claude/settings.json ../ship-kit/hooks/hooks.json'
  run '(cd ../ship-kit && find . -type f | sort)'
)
run 'bash kit.sh good "$DRY/built" && diff -r "$DRY/ship-kit" "$DRY/built"; echo "[diff exit $?: 0 means the plugin made by hand and the one kit.sh builds are the same files]"'
run '(cd "$DRY/lab" && node --test 2>&1 | grep -E "(tests|pass|fail) [0-9]+$|rounds up|retried once" | sed -E "s/ [(][0-9.]+ms[)]//")'
# What a viewer sees in project B before any session, and that its existing test is a real one.
run 'bash session.sh dry-kit kit --dry > /dev/null; (cd "$DRY/lab" && find . -type f -not -path "./.claude/*" | sort)'
run '(cd "$DRY/lab" && cat package.json README.md && cat logs/sync-2026-10-09.log)'
run '(cd "$DRY/lab" && node --test 2>&1 | grep -E "(tests|pass|fail) [0-9]+$|rounds up|retried once" | sed -E "s/ [(][0-9.]+ms[)]//")'
rm -rf "$DRY/built"

run 'bash validate-all.sh'

# The bookkeeping, with a command that does nothing in place of claude. <scratch> is a
# temporary folder: <scratch>/run/lab is the project and <scratch>/run/logs holds the records.
scratch="$(mktemp -d)"
guard() { LAB="$scratch/run/lab" KIT="$scratch/run/ship-kit" LOGS="$scratch/run/logs" DRY="$scratch/run/dry" CLAUDE="${STANDIN:-true}" bash session.sh "$@"; }
records() { (cd "$scratch/run/logs" && ls | sort | tr '\n' ' '; echo); }
aside() { (cd "$scratch/run/logs/replaced" && ls */ | sort | tr '\n' ' '; echo); }
run 'guard g1 kit > /dev/null 2>&1; records'
run 'guard g1 kit > /dev/null; echo "[session.sh exit $?]"; records'
run 'guard g1 kit --dry | tail -1; records'
run 'guard g1 kit --force 2>&1 > /dev/null | sed -E "s#g1\.[0-9TZ]+#g1.<time>#"; records; aside'
# A run folder inside a git repository is refused before anything is built.
mkdir -p "$scratch/repo" && git -C "$scratch/repo" init -q
run 'LAB="$scratch/repo/lab" KIT="$scratch/run/ship-kit" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 kit; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'LAB="$scratch/run/lab" KIT="$scratch/repo/ship-kit" LOGS="$scratch/run/logs" CLAUDE=true bash session.sh g2 kit; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'DRY="$scratch/repo/dry" bash session.sh g2 kit --dry; echo "[session.sh exit $?]"; ls "$scratch/repo"'
run 'bash kit.sh good "$scratch/repo/ship-kit"; echo "[kit.sh exit $?]"; ls "$scratch/repo"'
# A stand-in that writes one file next to the project and one into the plugin: both must say CHANGED.
printf '#!/usr/bin/env bash\necho intruder > ../intruder.txt\necho intruder > ../ship-kit/scripts/intruder.txt\n' > "$scratch/standin.sh"; chmod +x "$scratch/standin.sh"
run 'STANDIN="$scratch/standin.sh" guard g3 kit > /dev/null 2>&1; grep -A3 "^## outside the project" "$scratch/run/logs/g3.session.txt" | sed -E "s/[0-9a-f]{16}/<digest>/g"'
run 'grep -A3 "^## outside the project" "$scratch/run/logs/g1.session.txt" | sed -E "s/[0-9a-f]{16}/<digest>/g"'
# The optional empty plugins root: only the variable and the folder, with the stand-in command.
run 'PLUGINS_ROOT=empty guard g4 kit > /dev/null 2>&1; grep -c "CLAUDE_CODE_PLUGIN_CACHE_DIR=" "$scratch/run/logs/g4.session.txt"; grep "empty plugins root" "$scratch/run/logs/g4.session.txt"; grep -c "CLAUDE_CODE_PLUGIN_CACHE_DIR=" "$scratch/run/logs/g1.session.txt"'
# What the scrubbing leaves of this machine in a record made with the stand-in command: the
# user name anywhere and the host name as a whole word are counted, never printed.
run 'grep -c -i -E "$user|\b${HOSTNAME:-no-host-name}\b" "$scratch/run/logs/g1.session.txt"; grep -c -E "<lab>|<plugin>|<logs>|<seed>" "$scratch/run/logs/g1.session.txt"'
run 'sed -n "/^\[the claude command/,\$p" "$scratch/run/logs/g1.session.txt" | cut -c1-200 | head -70'
rm -rf "$scratch" "$DRY"
