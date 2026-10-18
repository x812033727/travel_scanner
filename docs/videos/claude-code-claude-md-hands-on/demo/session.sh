#!/usr/bin/env bash
# One headless Claude Code session for the CLAUDE.md video, in a project rebuilt from the seed.
#
#   bash <seed>/session.sh <name> <arm> [--dry]
#
# arm      what the project holds besides the four seed files and the load logger
# none     nothing: no CLAUDE.md anywhere in the project
# team     CLAUDE.md (variants/CLAUDE.team.md)
# conflict CLAUDE.md and CLAUDE.local.md (variants/CLAUDE.local.mine.md), which disagree on line 1
# lazy     CLAUDE.md, docs/CLAUDE.md, .claude/rules/checks.md, docs/use.md, checks/text.check.mjs
# off      the same files as team, started with CLAUDE_CODE_DISABLE_CLAUDE_MDS=1
#
# LAB, LOGS and MODEL may be set in the environment. --dry builds the project and prints the
# command without starting a session, so it calls no model.
set -u
name="${1:?name, for example a1}"
arm="${2:?arm: none, team, conflict, lazy or off}"
dry="${3:-}"

seed="$(cd "$(dirname "$0")" && pwd)"
work="$(cd "$seed/../.." && pwd)"
LAB="${LAB:-$work/run/md-lab}"
LOGS="${LOGS:-$work/run/logs}"
MODEL="${MODEL:-sonnet}"

native() { (cd "$1" && (pwd -W 2>/dev/null || pwd)); }
# What the log shows instead of this machine's folders.
show() { sed -e "s#$lab_native#<lab>#g" -e "s#$logs_native#<logs>#g" -e "s#$seed_native#<seed>#g" \
  -e "s#$LAB#<lab>#g" -e "s#$LOGS#<logs>#g" -e "s#$seed#<seed>#g"; }

prompt="add-truncate.txt"
tools="Read,Glob,Grep,Edit,Write"
extra_env=""

rm -rf "$LAB"
mkdir -p "$LAB/.claude/hooks" "$LOGS"
cp -r "$seed/md-lab/." "$LAB/"
cp "$seed/load-log/settings.json" "$LAB/.claude/settings.json"
cp "$seed/load-log/loaded.mjs" "$LAB/.claude/hooks/loaded.mjs"
case "$arm" in
  none) ;;
  team) cp "$seed/variants/CLAUDE.team.md" "$LAB/CLAUDE.md" ;;
  conflict)
    cp "$seed/variants/CLAUDE.team.md" "$LAB/CLAUDE.md"
    cp "$seed/variants/CLAUDE.local.mine.md" "$LAB/CLAUDE.local.md" ;;
  lazy)
    cp "$seed/variants/CLAUDE.team.md" "$LAB/CLAUDE.md"
    mkdir -p "$LAB/docs" "$LAB/checks" "$LAB/.claude/rules"
    cp "$seed/variants/lazy/docs/CLAUDE.subdir.md" "$LAB/docs/CLAUDE.md"
    cp "$seed/variants/lazy/docs/use.md" "$LAB/docs/"
    cp "$seed/variants/lazy/checks/text.check.mjs" "$LAB/checks/"
    cp "$seed/variants/lazy/rules/checks.md" "$LAB/.claude/rules/checks.md"
    prompt="read-two.txt"
    tools="Read,Glob,Grep" ;;
  off)
    cp "$seed/variants/CLAUDE.team.md" "$LAB/CLAUDE.md"
    extra_env="CLAUDE_CODE_DISABLE_CLAUDE_MDS=1" ;;
  *) echo "unknown arm: $arm" >&2; exit 2 ;;
esac

lab_native="$(native "$LAB")"
logs_native="$(native "$LOGS")"
seed_native="$(native "$seed")"
log="$LOGS/$name.session.log"
load_log="$logs_native/$name.loaded.log"
rm -f "$LOGS/$name.loaded.log" "$LOGS/$name.stream.jsonl" "$LOGS/$name.debug.log" "$LOGS/$name.stderr.txt"

{
  echo "# $name | arm $arm | start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## the project before the session (rebuilt from <seed>/md-lab)"
  echo '$ find . -type f | sort'
  (cd "$LAB" && find . -type f | sort)
  echo '$ sha256sum (every file, first 16 hex digits)'
  (cd "$LAB" && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
  echo "## the request ($prompt)"
  cat "$seed/prompts/$prompt"
  echo "## what the session inherits from this shell (names only, then four values)"
  env | grep -E '^(CLAUDE|ANTHROPIC)' | cut -d= -f1 | sort | tr '\n' ' '
  echo
  for each in CLAUDECODE CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_SIMPLE CLAUDE_EFFORT; do echo "$each=${!each-<unset>}"; done
  echo "## the session"
  echo "\$ env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 LOAD_LOG=<logs>/$name.loaded.log $extra_env \\"
  echo "    timeout 300 claude -p --model $MODEL --setting-sources project,local --strict-mcp-config \\"
  echo "    --tools \"$tools\" --allowedTools \"$tools\" --no-session-persistence \\"
  echo "    --output-format stream-json --verbose --include-hook-events \\"
  echo "    --debug-file <logs>/$name.debug.log \\"
  echo "    < <seed>/prompts/$prompt > <logs>/$name.stream.jsonl 2> <logs>/$name.stderr.txt"
} > "$log"

if [ "$dry" = "--dry" ]; then
  echo "[dry run: no session was started]" >> "$log"
  show < "$log"
  exit 0
fi

started=$(date +%s)
(
  cd "$LAB" && env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 LOAD_LOG="$load_log" $extra_env \
    timeout 300 claude -p --model "$MODEL" --setting-sources project,local --strict-mcp-config \
    --tools "$tools" --allowedTools "$tools" --no-session-persistence \
    --output-format stream-json --verbose --include-hook-events \
    --debug-file "$logs_native/$name.debug.log" \
    < "$seed/prompts/$prompt" > "$LOGS/$name.stream.jsonl" 2> "$LOGS/$name.stderr.txt"
)
code=$?

{
  echo "[exit $code] ($(( $(date +%s) - started )) s, ended $(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "[stream lines: $(wc -l < "$LOGS/$name.stream.jsonl") | stderr bytes: $(wc -c < "$LOGS/$name.stderr.txt")]"
  echo "## the project after the session"
  echo "\$ find . -type f -not -path './.claude/*' | sort"
  (cd "$LAB" && find . -type f -not -path './.claude/*' | sort)
  echo '$ head -5 CHANGELOG.md'
  (cd "$LAB" && head -5 CHANGELOG.md)
  echo '$ sha256sum CHANGELOG.md src/text.mjs (first 16 hex digits)'
  (cd "$LAB" && sha256sum CHANGELOG.md src/text.mjs | cut -c1-16,65-)
  for each in $(cd "$LAB" && find . -type f \( -name '*.check.mjs' -o -name '*.test.mjs' -o -name '*.spec.mjs' \) | sort); do
    echo "\$ node --test $each 2>&1 | grep -E ' (pass|fail) [0-9]+\$'"
    (cd "$LAB" && node --test "$each" 2>&1 | grep -E ' (pass|fail) [0-9]+$')
  done
  echo "## instruction files the logger saw (<logs>/$name.loaded.log)"
  if [ -s "$LOGS/$name.loaded.log" ]; then cat "$LOGS/$name.loaded.log"; else echo "(empty: no InstructionsLoaded event reached the logger)"; fi
  echo "## in the stream"
  echo "\$ grep -c '\"hook_event\":\"InstructionsLoaded\"' <logs>/$name.stream.jsonl"
  grep -c '"hook_event":"InstructionsLoaded"' "$LOGS/$name.stream.jsonl"
  echo "\$ node <seed>/tally.mjs <logs>/$name.stream.jsonl"
  node "$seed/tally.mjs" "$LOGS/$name.stream.jsonl"
  echo "## the debug log's own line about instruction files above the project"
  grep -h 'fs.ancestors' "$LOGS/$name.debug.log" 2>/dev/null | sed -E 's/^[^ ]+ //' | sort | uniq -c
  echo "# $name | end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log" 2>&1

show < "$log"
