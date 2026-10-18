#!/usr/bin/env bash
# One headless Claude Code session for the subagents video, in a project rebuilt from the seed.
#
#   bash <seed>/session.sh <name> <arm> [--dry] [--force]
#
# arm       what the project holds besides the seed files and the logging hook, and what is asked
# inline    no agent file; the tool that starts a subagent is NOT offered; ask.txt
# auto      .claude/agents/log-scout.md; ask.txt (the request does not mention the agent)
# named     the same files as auto; named.txt (the request names log-scout)
# write     the same files as auto; write.txt (asks log-scout, which has no Write, to write a file)
# claudemd  the same files as auto, and a CLAUDE.md with one rule; named.txt
# builtin   no agent file; the tool that starts a subagent IS offered; ask.txt
# omit      the same files as claudemd, but the agent file sets omitClaudeMd: true; named.txt
# broken    the agent file with a quote that is never closed in its description   (--dry only: these
# nodesc    the agent file without a description line                              two are for validate)
#
# The seed keeps the agent files under neutral names (variants/*.agent.md) and the CLAUDE.md as
# variants/CLAUDE.canary.md, so that copying the seed into a repository does not hand that
# repository's sessions an agent or an instruction file. This script puts them where Claude Code
# looks: <lab>/.claude/agents/log-scout.md and <lab>/CLAUDE.md.
#
# --dry    builds the project in <dry>, prints the command, starts no session, calls no model,
#          and touches neither <lab> nor <logs>.
# --force  a name that already has records is refused; with --force the old records are moved
#          to <logs>/replaced/<name>.<time>/ first. Nothing is ever deleted from <logs>.
#
# WORK, LAB, LOGS, DRY, MODEL and BUDGET may be set in the environment. The run folders default to
# a temporary directory, and the script refuses to build or record inside a git repository.
set -u
name="${1:?name, for example n1}"
arm="${2:?arm: inline, auto, named, write, claudemd, builtin, omit; broken or nodesc with --dry}"
shift 2
dry=""; force=""
for flag in "$@"; do
  case "$flag" in
    --dry) dry=1 ;;
    --force) force=1 ;;
    *) echo "unknown flag: $flag" >&2; exit 2 ;;
  esac
done

seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-subagents-hands-on}"
LAB="${LAB:-$work/run/log-lab}"
LOGS="${LOGS:-$work/run/logs}"
DRY="${DRY:-$work/run/dry-lab}"
MODEL="${MODEL:-sonnet}"
BUDGET="${BUDGET:-2}"
# CLAUDE is only ever replaced by m-checks.sh, which tests the bookkeeping with a command that does nothing.
CLAUDE="${CLAUDE:-claude}"

case "$arm" in
  inline|auto|named|write|claudemd|builtin|omit) ;;
  broken|nodesc) [ -n "$dry" ] || { echo "arm $arm is for --dry only" >&2; exit 2; } ;;
  *) echo "unknown arm: $arm" >&2; exit 2 ;;
esac

# Nothing is built or recorded inside a git repository: a copy of this script that lives in a
# repository must not write into it.
in_git() {
  local dir="$1"
  while [ ! -d "$dir" ]; do dir="$(dirname "$dir")"; done
  [ "$(git -C "$dir" rev-parse --is-inside-work-tree 2>/dev/null)" = "true" ]
}
if [ -n "$dry" ]; then places="$DRY"; else places="$LAB $LOGS"; fi
for place in $places; do
  if in_git "$place"; then
    echo "refused: a run folder is inside a git repository. Set WORK (or LAB, LOGS, DRY) to a folder outside any repository." >&2
    exit 4
  fi
done

if [ -z "$dry" ]; then
  mkdir -p "$LOGS"
  old="$(find "$LOGS" -maxdepth 1 -name "$name.*" | sort)"
  if [ -n "$old" ]; then
    if [ -z "$force" ]; then
      echo "refused: $name already has records in <logs> ($(echo "$old" | wc -l) entries)." >&2
      echo "Pick another name (for example ${name}r), or pass --force to move them aside." >&2
      exit 3
    fi
    aside="$LOGS/replaced/$name.$(date -u +%Y%m%dT%H%M%SZ)"
    mkdir -p "$aside"
    echo "$old" | while read -r each; do mv "$each" "$aside/"; done
    echo "moved the old records of $name to <logs>/replaced/$(basename "$aside")/" >&2
  fi
  target="$LAB"
else
  target="$DRY"
fi

prompt="ask.txt"
tools="Read,Glob,Grep,Edit,Write,Agent,Task"
place() { mkdir -p "$target/.claude/agents" && cp "$seed/variants/$1" "$target/.claude/agents/log-scout.md"; }

rm -rf "$target"
mkdir -p "$target/.claude/hooks"
cp -r "$seed/log-lab/." "$target/"
cp "$seed/agent-log/settings.json" "$target/.claude/settings.json"
cp "$seed/agent-log/seen.mjs" "$target/.claude/hooks/seen.mjs"
case "$arm" in
  inline) tools="Read,Glob,Grep,Edit,Write" ;;
  builtin) ;;
  auto) place log-scout.agent.md ;;
  named) place log-scout.agent.md; prompt="named.txt" ;;
  write) place log-scout.agent.md; prompt="write.txt" ;;
  claudemd) place log-scout.agent.md; cp "$seed/variants/CLAUDE.canary.md" "$target/CLAUDE.md"; prompt="named.txt" ;;
  omit) place log-scout.omit.agent.md; cp "$seed/variants/CLAUDE.canary.md" "$target/CLAUDE.md"; prompt="named.txt" ;;
  broken) place log-scout.broken.agent.md ;;
  nodesc) place log-scout.nodesc.agent.md ;;
esac

# What the log shows instead of this machine's folders, user and host: every spelling of each
# path (POSIX, C:/..., C:\..., C:\\...), then the user name, the host name, and long ids.
to_native() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1"; }
esc() { printf '%s' "$1" | sed -e 's/[][\\.*^$#]/\\&/g'; }
scrub=()
hide() {
  local path="$1" native back double each
  [ -n "$path" ] || return 0
  native="$(to_native "$path")"
  back="${native//\//\\}"
  double="${native//\//\\\\}"
  for each in "$double" "$back" "$native" "$path"; do scrub+=(-e "s#$(esc "$each")#$2#g"); done
}
hide "$target" "<lab>"
hide "$LOGS" "<logs>"
hide "$seed" "<seed>"
hide "$work" "<work>"
hide "$HOME" "<home>"
for word in "$(basename "$HOME")" "${USERNAME:-}" "${USER:-}"; do
  [ "${#word}" -ge 3 ] && scrub+=(-e "s#$(esc "$word")#<user>#g")
done
for word in "$(hostname 2>/dev/null)" "${COMPUTERNAME:-}"; do
  [ "${#word}" -ge 3 ] && scrub+=(-e "s#$(esc "$word")#<host>#g")
done
show() {
  sed "${scrub[@]}" | sed -E \
    -e 's/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/<uuid>/g' \
    -e 's/agent-[0-9a-f]{6,}/agent-<id>/g'
}
logs_native="$(to_native "$LOGS")"

# Folders above the project that could hand the session something: counted, never named.
above() {
  local dir total=0 agents=0 skills=0 md=0 agentsmd=0 git=0
  dir="$(dirname "$target")"
  while :; do
    total=$((total + 1))
    [ -d "$dir/.claude/agents" ] && agents=$((agents + 1))
    [ -d "$dir/.claude/skills" ] && skills=$((skills + 1))
    { [ -f "$dir/CLAUDE.md" ] || [ -f "$dir/.claude/CLAUDE.md" ] || [ -f "$dir/CLAUDE.local.md" ]; } && md=$((md + 1))
    [ -f "$dir/AGENTS.md" ] && agentsmd=$((agentsmd + 1))
    [ -e "$dir/.git" ] && git=$((git + 1))
    [ "$(dirname "$dir")" = "$dir" ] && break
    dir="$(dirname "$dir")"
  done
  echo "$total folders above <lab> | with .claude/agents: $agents | with .claude/skills: $skills | with a CLAUDE.md: $md | with AGENTS.md: $agentsmd | with .git: $git"
}

header() {
  echo "# $name | arm $arm | start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## the project before the session (rebuilt from <seed>/log-lab)"
  echo '$ find . -type f | sort'
  (cd "$target" && find . -type f | sort)
  echo '$ sha256sum (every file, first 16 hex digits)'
  (cd "$target" && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
  echo "## above the project (counts only)"
  above
  echo "## the request ($prompt)"
  cat "$seed/prompts/$prompt"
  echo "## the session"
  echo "\$ env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SEEN_LOG=<logs>/$name.seen.log \\"
  echo "    CLAUDE_CODE_SUBAGENT_MODEL=$MODEL CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 \\"
  echo "    timeout 600 claude -p --model $MODEL --setting-sources project,local --strict-mcp-config \\"
  echo "    --tools \"$tools\" --allowedTools \"$tools\" --no-session-persistence \\"
  echo "    --max-budget-usd $BUDGET --output-format stream-json --verbose \\"
  echo "    --debug-file <logs>/$name.debug.log \\"
  echo "    < <seed>/prompts/$prompt > <logs>/$name.stream.jsonl 2> <logs>/$name.stderr.txt"
}

if [ -n "$dry" ]; then
  { header; echo "[dry run: no session was started; <lab> here is the dry folder, and <logs> was not touched]"; } | show
  exit 0
fi

log="$LOGS/$name.session.log"
header > "$log"
[ "$CLAUDE" = claude ] || echo "[the claude command was replaced by \"$CLAUDE\": no session was started, no model was called]" >> "$log"

started=$(date +%s)
(
  cd "$LAB" && env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SEEN_LOG="$logs_native/$name.seen.log" \
    CLAUDE_CODE_SUBAGENT_MODEL="$MODEL" CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1 \
    timeout 600 "$CLAUDE" -p --model "$MODEL" --setting-sources project,local --strict-mcp-config \
    --tools "$tools" --allowedTools "$tools" --no-session-persistence \
    --max-budget-usd "$BUDGET" --output-format stream-json --verbose \
    --debug-file "$logs_native/$name.debug.log" \
    < "$seed/prompts/$prompt" > "$LOGS/$name.stream.jsonl" 2> "$LOGS/$name.stderr.txt"
)
code=$?

# Keep the project as the session left it: the next session rebuilds <lab>.
cp -r "$LAB" "$LOGS/$name.lab"

count() { if [ -f "$2" ]; then grep -c -- "$1" "$2"; else echo 0; fi; }
{
  echo "[exit $code] ($(( $(date +%s) - started )) s, ended $(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "[stream lines: $(wc -l < "$LOGS/$name.stream.jsonl") | stderr bytes: $(wc -c < "$LOGS/$name.stderr.txt")]"
  echo "## the project after the session (kept as <logs>/$name.lab)"
  echo "\$ find . -type f -not -path './.claude/*' | sort"
  (cd "$LAB" && find . -type f -not -path './.claude/*' | sort)
  echo '$ head -12 REPORT.md'
  (cd "$LAB" && head -12 REPORT.md 2>&1 | cut -c1-110)
  echo "## what the logging hook saw (<logs>/$name.seen.log)"
  if [ -s "$LOGS/$name.seen.log" ]; then cat "$LOGS/$name.seen.log"; else echo "(empty: no hook event reached the logger)"; fi
  echo "## the personal layer, counted from the hook log (each should be 0)"
  echo "lines with (another agent): $(count '(another agent)' "$LOGS/$name.seen.log") | with (outside the project): $(count '(outside the project)' "$LOGS/$name.seen.log") | instruction files of type User or Managed: $(count -E 'InstructionsLoaded .* (User|Managed) ' "$LOGS/$name.seen.log")"
  echo "## from the stream"
  echo "\$ grep -c -E '\"name\":\"(Agent|Task)\"' <logs>/$name.stream.jsonl"
  grep -c -E '"name":"(Agent|Task)"' "$LOGS/$name.stream.jsonl"
  echo "\$ grep -c '\"parent_tool_use_id\":\"' <logs>/$name.stream.jsonl"
  grep -c '"parent_tool_use_id":"' "$LOGS/$name.stream.jsonl"
  echo "\$ node <seed>/tally.mjs <logs>/$name.stream.jsonl"
  node "$seed/tally.mjs" "$LOGS/$name.stream.jsonl"
  echo "## the debug log on agents"
  echo "\$ grep -ci agent <logs>/$name.debug.log"
  grep -ci agent "$LOGS/$name.debug.log" 2>/dev/null
  # Lines that name the project's agent, with any bracketed or quoted list emptied: a list could
  # hold the names of agents that are not the project's.
  echo "\$ grep -i 'log-scout' <logs>/$name.debug.log | head -8 (time stamps cut, lists emptied)"
  grep -i 'log-scout' "$LOGS/$name.debug.log" 2>/dev/null | sed -E -e 's/^[^ ]+ //' -e 's/\[[^]]*\]/[...]/g' | cut -c1-200 | head -8
  # From every line that mentions agents, only "<source>: <number>" pairs, never names.
  echo "\$ grep -i agent <logs>/$name.debug.log | grep -oiE '(managed|policy|user|project|local|plugin|built-?in|flag|cli)[a-z]*: ?[0-9]+' | sort | uniq -c"
  grep -i agent "$LOGS/$name.debug.log" 2>/dev/null | grep -oiE '(managed|policy|user|project|local|plugin|built-?in|flag|cli)[a-z]*: ?[0-9]+' | sort | uniq -c
  echo "\$ grep 'fs.ancestors' <logs>/$name.debug.log (time stamps cut, counted)"
  grep -h 'fs.ancestors' "$LOGS/$name.debug.log" 2>/dev/null | sed -E 's/^[^ ]+ //' | sort | uniq -c
  echo "# $name | end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log" 2>&1

show < "$log" > "$log.shown" && mv "$log.shown" "$log"
cat "$log"
