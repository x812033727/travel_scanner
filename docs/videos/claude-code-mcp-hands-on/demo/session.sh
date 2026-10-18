#!/usr/bin/env bash
# One headless Claude Code session for the MCP video, in a project rebuilt from the seed.
#
#   bash <seed>/session.sh <name> <arm> [--dry] [--force]
#
# Every arm starts from the same project (gear-lab: the server, its data file, a .mcp.json that
# names the server, and the logging hook) and every arm passes --strict-mcp-config, so no MCP
# server from anywhere else can connect. What differs:
#
# arm      .mcp.json from          passed to claude                          asked
# off      mcp.project.json        no --mcp-config (the file is there, unread) ask.txt
# on       mcp.project.json        --mcp-config .mcp.json, gear's tools allowed ask.txt
# noallow  mcp.project.json        --mcp-config .mcp.json, no allow rule        ask.txt
# miss     mcp.project.json        as on                                        miss.txt
# broken   mcp.broken.json         as on (the file it starts does not exist)    ask.txt
# wide     mcp.wide.json           as on, plus gear-more (ten more tools)       ask.txt
# wideup   mcp.wide.json           as wide, with ENABLE_TOOL_SEARCH=false       ask.txt
# files    mcp.project.json        as off, plus the built-in Read, Glob, Grep   ask.txt
# up       mcp.project.json        as on, with ENABLE_TOOL_SEARCH=false         ask.txt   (prepared, not in the list)
# idle     mcp.project.json        as on                                        idle.txt  (prepared, not in the list)
# rooted   mcp.rooted.json         as on (${CLAUDE_PROJECT_DIR:-.}/server/...)  ask.txt   (only if "on" cannot start the server)
#
# The seed keeps each MCP configuration under a neutral name (variants/mcp.*.json) and the hook
# settings outside any .claude folder, so that a copy of the seed inside a repository offers that
# repository's own Claude Code sessions neither a server nor a hook. This script puts them where
# Claude Code looks: <lab>/.mcp.json, <lab>/.claude/settings.json, <lab>/.claude/hooks/seen.mjs.
#
# --dry    builds the project in <dry>, prints the command, starts no session, calls no model,
#          and touches neither <lab> nor <logs>.
# --force  a name that already has records is refused; with --force the old records are moved
#          to <logs>/replaced/<name>.<time>/ first. Nothing is ever deleted from <logs>.
#
# WORK, LAB, LOGS, DRY, MODEL, BUDGET and TOOLS may be set in the environment (TOOLS=none passes
# --tools ""). The run folders default to a temporary directory, and the script refuses to build
# or record inside a git repository. It never reads, prints or copies any MCP configuration but
# the seed's own.
set -u
name="${1:?name, for example n1}"
arm="${2:?arm: off, on, noallow, miss, broken, wide, wideup, files, up, idle or rooted}"
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
work="${WORK:-${TMPDIR:-/tmp}/claude-code-mcp-hands-on}"
LAB="${LAB:-$work/run/gear-lab}"
LOGS="${LOGS:-$work/run/logs}"
DRY="${DRY:-$work/run/dry-lab}"
MODEL="${MODEL:-sonnet}"
BUDGET="${BUDGET:-1}"
TOOLS="${TOOLS:-ToolSearch}"
[ "$TOOLS" = none ] && TOOLS=""
# CLAUDE is only ever replaced by m-checks.sh, which tests the bookkeeping with a command that does nothing.
CLAUDE="${CLAUDE:-claude}"

mcp="mcp.project.json"; prompt="ask.txt"; config=1; allow="mcp__gear__*"; upfront=""; tools="$TOOLS"; more=""
case "$arm" in
  on) ;;
  off) config="" ;;
  noallow) allow="" ;;
  miss) prompt="miss.txt" ;;
  broken) mcp="mcp.broken.json" ;;
  wide) mcp="mcp.wide.json"; more=1; allow="mcp__gear__*,mcp__gear-more__*" ;;
  wideup) mcp="mcp.wide.json"; more=1; allow="mcp__gear__*,mcp__gear-more__*"; upfront=1 ;;
  files) config=""; tools="${TOOLS:+$TOOLS,}Read,Glob,Grep"; allow="mcp__gear__*,Read,Glob,Grep" ;;
  up) upfront=1 ;;
  idle) prompt="idle.txt" ;;
  rooted) mcp="mcp.rooted.json" ;;
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

rm -rf "$target"
mkdir -p "$target/.claude/hooks"
cp -r "$seed/gear-lab/." "$target/"
cp "$seed/variants/$mcp" "$target/.mcp.json"
[ -n "$more" ] && cp "$seed/variants/more.server.mjs" "$target/server/more.mjs"
cp "$seed/hook-log/settings.json" "$target/.claude/settings.json"
cp "$seed/hook-log/seen.mjs" "$target/.claude/hooks/seen.mjs"

# What the log shows instead of this machine's folders, user and host: every spelling of each
# path (POSIX, C:/..., C:\..., C:\\...), then the user name, then the host name on word
# boundaries only (a short host name is otherwise found inside ordinary words), and long ids.
to_native() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1"; }
# esc leaves its answer in ESC: a text with the characters sed reads as a pattern escaped.
esc() {
  local text="$1" at char
  ESC=""
  for ((at = 0; at < ${#text}; at++)); do
    char="${text:at:1}"
    case "$char" in
      '['|']'|'\'|'.'|'*'|'^'|'$'|'#') ESC+="\\$char" ;;
      *) ESC+="$char" ;;
    esac
  done
}
scrub=()
hide() {
  local path="$1" native back double each
  [ -n "$path" ] || return 0
  native="$(to_native "$path")"
  back="${native//\//\\}"
  double="${native//\//\\\\}"
  for each in "$double" "$back" "$native" "$path"; do esc "$each"; scrub+=(-e "s#$ESC#$2#g"); done
}
hide "$target" "<lab>"
hide "$LOGS" "<logs>"
hide "$seed" "<seed>"
hide "$work" "<work>"
hide "$HOME" "<home>"
for word in "$(basename "$HOME")" "${USERNAME:-}" "${USER:-}"; do
  [ "${#word}" -ge 3 ] && { esc "$word"; scrub+=(-e "s#$ESC#<user>#g"); }
done
for word in "${HOSTNAME:-}" "${COMPUTERNAME:-}"; do
  [ "${#word}" -ge 3 ] && { esc "$word"; scrub+=(-e "s#\\b$ESC\\b#<host>#gI"); }
done

# Whether this shell points Claude Code at another API host, said without the value: tool search
# is off by default when it is not an anthropic.com host (the official mcp page).
base="${ANTHROPIC_BASE_URL:-}"; base="${base#*://}"; base="${base%%/*}"; base="${base%%:*}"
case "$base" in
  "") base_kind="not set" ;;
  api.anthropic.com|*.anthropic.com) base_kind="set, to an anthropic.com host" ;;
  *) base_kind="set, NOT to an anthropic.com host" ;;
esac
show() {
  sed "${scrub[@]}" | sed -E \
    -e 's/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/<uuid>/g' \
    -e 's/toolu_[0-9A-Za-z]{6,}/toolu_<id>/g'
}
logs_native="$(to_native "$LOGS")"

# The command, as two arrays: what goes into the environment and what goes to claude.
envs=(CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false "SEEN_LOG=$logs_native/$name.seen.txt")
[ -n "$upfront" ] && envs+=(ENABLE_TOOL_SEARCH=false)
args=(-p --model "$MODEL" --setting-sources project,local --strict-mcp-config)
[ -n "$config" ] && args+=(--mcp-config .mcp.json)
args+=(--tools "$tools")
[ -n "$allow" ] && args+=(--allowedTools "$allow")
args+=(--no-session-persistence --max-budget-usd "$BUDGET" --output-format stream-json --verbose)
args+=(--debug-file "$logs_native/$name.debug.txt")
quoted() {
  local each out=""
  for each in "$@"; do
    case "$each" in
      *[!A-Za-z0-9_./:=,@-]*|"") out="$out \"$each\"" ;;
      *) out="$out $each" ;;
    esac
  done
  printf '%s' "${out# }"
}

# Folders above the project that could hand the session something: counted, never named.
above() {
  local dir total=0 mcpjson=0 settings=0 md=0 agentsmd=0 git=0
  dir="$(dirname "$target")"
  while :; do
    total=$((total + 1))
    [ -f "$dir/.mcp.json" ] && mcpjson=$((mcpjson + 1))
    { [ -f "$dir/.claude/settings.json" ] || [ -f "$dir/.claude/settings.local.json" ]; } && settings=$((settings + 1))
    { [ -f "$dir/CLAUDE.md" ] || [ -f "$dir/.claude/CLAUDE.md" ] || [ -f "$dir/CLAUDE.local.md" ]; } && md=$((md + 1))
    [ -f "$dir/AGENTS.md" ] && agentsmd=$((agentsmd + 1))
    [ -e "$dir/.git" ] && git=$((git + 1))
    [ "$(dirname "$dir")" = "$dir" ] && break
    dir="$(dirname "$dir")"
  done
  echo "$total folders above <lab> | with a .mcp.json: $mcpjson | with .claude settings: $settings | with a CLAUDE.md: $md | with AGENTS.md: $agentsmd | with .git: $git"
}

header() {
  echo "# $name | arm $arm | start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## the project before the session (rebuilt from <seed>/gear-lab)"
  echo '$ find . -type f | sort'
  (cd "$target" && find . -type f | sort)
  echo '$ sha256sum (every file, first 16 hex digits)'
  (cd "$target" && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
  echo '$ cat .mcp.json'
  cat "$target/.mcp.json"
  echo "## above the project (counts only)"
  above
  echo "## two variables that change how tools load (never their values): ANTHROPIC_BASE_URL $base_kind | ENABLE_TOOL_SEARCH $([ -n "${ENABLE_TOOL_SEARCH:-}" ] && echo "set (removed for the session)" || echo "not set")"
  echo "## the request ($prompt)"
  cat "$seed/prompts/$prompt"
  echo "## the session"
  echo "\$ env -u ENABLE_TOOL_SEARCH $(quoted "${envs[@]}") \\"
  echo "    timeout 300 claude $(quoted "${args[@]}") \\"
  echo "    < <seed>/prompts/$prompt > <logs>/$name.stream.jsonl 2> <logs>/$name.stderr.txt"
}

if [ -n "$dry" ]; then
  { header; echo "[dry run: no session was started; <lab> here is the dry folder, and <logs> was not touched]"; } | show
  exit 0
fi

log="$LOGS/$name.session.txt"
header > "$log"
[ "$CLAUDE" = claude ] || echo "[the claude command was replaced by \"$CLAUDE\": no session was started, no model was called]" >> "$log"

started=$(date +%s)
(
  cd "$LAB" && env -u ENABLE_TOOL_SEARCH "${envs[@]}" \
    timeout 300 "$CLAUDE" "${args[@]}" \
    < "$seed/prompts/$prompt" > "$LOGS/$name.stream.jsonl" 2> "$LOGS/$name.stderr.txt"
)
code=$?

# Keep the project as the session left it: the next session rebuilds <lab>.
cp -r "$LAB" "$LOGS/$name.lab"

count() { if [ -f "$2" ]; then grep -c -E -- "$1" "$2"; else echo 0; fi; }
{
  echo "[exit $code] ($(( $(date +%s) - started )) s, ended $(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "[stream lines: $(wc -l < "$LOGS/$name.stream.jsonl") | stderr bytes: $(wc -c < "$LOGS/$name.stderr.txt")]"
  echo '$ head -6 <logs>/'"$name"'.stderr.txt (cut at 160 columns)'
  head -6 "$LOGS/$name.stderr.txt" | cut -c1-160
  echo "## what the server kept (server/requests.txt in the project; the file is not in the seed)"
  if [ -s "$LAB/server/requests.txt" ]; then cat "$LAB/server/requests.txt"; else echo "(no such file: the server process never started)"; fi
  if [ -s "$LAB/server/requests-more.txt" ]; then echo "## what the ten-tool server kept (server/requests-more.txt)"; cat "$LAB/server/requests-more.txt"; fi
  echo "## what the logging hook saw (<logs>/$name.seen.txt)"
  if [ -s "$LOGS/$name.seen.txt" ]; then cat "$LOGS/$name.seen.txt"; else echo "(empty: no hook event reached the logger)"; fi
  echo "## anything that is not the seed's, counted from the hook record (each should be 0)"
  echo "lines with (another server): $(count '\(another server\)' "$LOGS/$name.seen.txt") | with (outside the project): $(count '\(outside the project\)' "$LOGS/$name.seen.txt") | instruction files loaded (the project has none): $(count '^InstructionsLoaded' "$LOGS/$name.seen.txt")"
  echo "## from the stream"
  echo "\$ grep -c '\"name\":\"mcp__gear' <logs>/$name.stream.jsonl"
  grep -c '"name":"mcp__gear' "$LOGS/$name.stream.jsonl"
  echo "\$ grep -c '\"name\":\"ToolSearch\"' <logs>/$name.stream.jsonl"
  grep -c '"name":"ToolSearch"' "$LOGS/$name.stream.jsonl"
  echo "\$ node <seed>/tally.mjs <logs>/$name.stream.jsonl"
  node "$seed/tally.mjs" "$LOGS/$name.stream.jsonl"
  echo "## the debug record on MCP"
  echo "\$ grep -ci mcp <logs>/$name.debug.txt"
  grep -ci mcp "$LOGS/$name.debug.txt" 2>/dev/null
  # Only lines that mention MCP and the seed's own server names (the folder name gear-lab does
  # not count); time stamps cut, any bracketed list emptied because a list could hold the names
  # of servers that are not the seed's. Lines about any other server are only counted.
  echo "\$ grep -i mcp <logs>/$name.debug.txt | grep -w -E 'gear(-more)?' | head -14 (time stamps cut, lists emptied, 200 columns)"
  grep -i mcp "$LOGS/$name.debug.txt" 2>/dev/null | sed -E -e 's/gear-lab/<lab-folder>/g' -e 's/^[^ ]+ //' -e 's/\[[^]]*\]/[...]/g' \
    | grep -E '(^|[^A-Za-z0-9_-])gear(-more)?([^A-Za-z0-9_-]|$)' | cut -c1-200 | head -14
  echo "\$ lines that say MCP server \"<name>\" with a name that is not the seed's (count only)"
  grep -o -i -E 'MCP server "[^"]+"' "$LOGS/$name.debug.txt" 2>/dev/null | grep -c -v -E '"gear(-more)?"'
  echo "\$ lines that mention claude.ai connectors (count only)"
  grep -c -i -E 'claude\.ai|claudeai|connector' "$LOGS/$name.debug.txt" 2>/dev/null
  echo "# $name | end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log" 2>&1

show < "$log" > "$log.shown" && mv "$log.shown" "$log"
cat "$log"
