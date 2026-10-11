#!/usr/bin/env bash
# One headless Claude Code session for the MCP tool-loading video, in a project rebuilt from the
# seed.
#
#   bash <seed>/session.sh <name> <arm> [--dry] [--force]
#
# Every arm starts from the same throwaway project (gear-desk: a README, a package.json, a small
# MCP server's program, its list of forty tools and its data under server/, and a logging hook
# that is the instrument, not a part). An arm then differs in the server it attaches and in one
# variable:
#
# arm       .mcp.json                  passed to claude          variable                    asked
# base      none                       -                         -                           idle.txt
# off       none                       -                         ENABLE_TOOL_SEARCH=false    idle.txt
# d<N>      gear with N tools          --mcp-config .mcp.json    -                           idle.txt
# u<N>      gear with N tools          --mcp-config .mcp.json    ENABLE_TOOL_SEARCH=false    idle.txt
# use-d<N>  as d<N>                    as d<N>                   -                           use.txt
# use-u<N>  as u<N>                    as u<N>                   ENABLE_TOOL_SEARCH=false    use.txt
# prepared, not in the run list:
# a<N>      gear with N tools          --mcp-config .mcp.json    ENABLE_TOOL_SEARCH=auto     idle.txt
# on        none                       -                         ENABLE_TOOL_SEARCH=true     idle.txt
#
# N is 0, 2, 10 or 40: the server lists the first N of its forty tools. d is the default
# (tools deferred, found through ToolSearch), u loads every definition up front. idle.txt is one
# line that uses no tool, so the first request of two arms differs only by what the arm attaches;
# use.txt asks for one lookup with one tool of the server.
# Every arm: -p, --model sonnet, --permission-mode default (Manual), --setting-sources
# project,local, --strict-mcp-config, the same built-in tools (Read Glob Grep Edit Write Skill
# Agent/Task ToolSearch, no Bash), auto memory off, claude.ai connectors off, and the same single
# allow rule: the one MCP tool use.txt names. Nothing else is pre-approved, so an edit or a write
# is refused in a session nobody can answer.
#
# The project's logging hook stops a file tool aimed outside the project before it runs (the
# hook exits 2 and writes BLOCKED), and runner/after.mjs says STOP when one was tried.
#
# The seed keeps the server's configuration under a name Claude Code does not look for
# (parts/mcp.n10.json) and the logging hook under watch/; this script puts them where Claude Code
# looks, in a folder outside any repository. No plugin is installed, enabled or listed, and no
# MCP configuration but the seed's own is read, printed or copied.
#
# --dry    builds the project in <dry>, prints the command, starts no session, calls no model,
#          and touches neither <lab> nor <logs>.
# --force  a name that already has records is refused; with --force the old records are moved
#          to <logs>/replaced/<name>.<time>/ first. Nothing is ever deleted from <logs>.
#
# WORK, LAB, LOGS, DRY, MODEL and BUDGET may be set in the environment. The run folders default
# to a temporary directory, and the script refuses to build or record inside a git repository
# (it looks for a .git entry in the folder and every folder above it; it starts no git command).
# The project folder is deleted and rebuilt for every session, so never point LAB or DRY at a
# folder of your own: a folder that holds something this script did not build is refused
# (exit 5), not deleted. With ANTHROPIC_BASE_URL set to a host that is not anthropic.com the
# script refuses to start a session (exit 6): tool search is then off by default and every arm
# would measure something else.
#
# The record <logs>/<name>.session.txt is written through the same replacements as it grows
# (folders, user, host, addresses, long ids), so a run that is stopped half way leaves no raw
# line in it. A record whose last line is not "# <name> | end ..." is an interrupted run.
set -u
name="${1:?name, for example z1}"
arm="${2:?arm: base, off, d2, d10, d40, u2, u10, u40, use-d40, use-u40 (or d0, a40, on)}"
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
work="${WORK:-${TMPDIR:-/tmp}/claude-code-mcp-tool-loading-hands-on}"
LAB="${LAB:-$work/run/lab}"
LOGS="${LOGS:-$work/run/logs}"
DRY="${DRY:-$work/run/dry}"
MODEL="${MODEL:-sonnet}"
BUDGET="${BUDGET:-1}"
TOOLS="Read,Glob,Grep,Edit,Write,Skill,Agent,Task,ToolSearch"
ALLOWED="mcp__gear__find_gear"
# CLAUDE is only ever replaced by m-checks.sh, which tests the bookkeeping with a command that does nothing.
CLAUDE="${CLAUDE:-claude}"

count=""; search=""; prompt="idle.txt"; wait=300
case "$arm" in
  base) ;;
  off) search=false ;;
  on) search=true ;;
  d0|d2|d10|d40) count="${arm#d}" ;;
  u0|u2|u10|u40) count="${arm#u}"; search=false ;;
  a0|a2|a10|a40) count="${arm#a}"; search=auto ;;
  use-d2|use-d10|use-d40) count="${arm#use-d}"; prompt="use.txt" ;;
  use-u2|use-u10|use-u40) count="${arm#use-u}"; search=false; prompt="use.txt" ;;
  *) echo "unknown arm: $arm" >&2; exit 2 ;;
esac

# Nothing is built or recorded inside a git repository: a copy of this script that lives in a
# repository must not write into it. A .git entry (a folder, or the file a worktree has) in the
# folder or above it is what marks one.
in_git() {
  local dir="$1"
  while [ ! -d "$dir" ]; do dir="$(dirname "$dir")"; done
  dir="$(cd "$dir" && pwd)"
  while :; do
    [ -e "$dir/.git" ] && return 0
    [ "$(dirname "$dir")" = "$dir" ] && return 1
    dir="$(dirname "$dir")"
  done
}
if [ -n "$dry" ]; then places=("$DRY"); else places=("$LAB" "$LOGS"); fi
for each in "${places[@]}"; do
  if in_git "$each"; then
    echo "refused: a run folder is inside a git repository. Set WORK (or LAB, LOGS, DRY) to a folder outside any repository." >&2
    exit 4
  fi
done

# The project folder is deleted and rebuilt below. A folder that exists, is not empty and does
# not carry this script's own mark is somebody's own: refuse, delete nothing.
if [ -z "$dry" ]; then target="$LAB"; else target="$DRY/lab"; fi
not_ours() { [ -d "$1" ] && [ -n "$(ls -A "$1" 2>/dev/null)" ] && [ ! -f "$1/$2" ]; }
if not_ours "$target" ".claude/hooks/seen.mjs" || { [ -e "$target" ] && [ ! -d "$target" ]; }; then
  echo "refused: the project folder exists and was not built by this script. Nothing was deleted." >&2
  exit 5
fi

# Whether this shell points Claude Code at another API host, said without the value: MCP tool
# search is off by default when it is not an anthropic.com host (the official mcp page).
api="${ANTHROPIC_BASE_URL:-}"; api="${api#*://}"; api="${api%%/*}"; api="${api%%:*}"
case "$api" in
  "") api_kind="not set" ;;
  api.anthropic.com|*.anthropic.com) api_kind="set, to an anthropic.com host" ;;
  *) api_kind="set, NOT to an anthropic.com host" ;;
esac
if [ -z "$dry" ] && [ "$api_kind" = "set, NOT to an anthropic.com host" ]; then
  echo "refused: ANTHROPIC_BASE_URL points at a host that is not anthropic.com, where tool search is off by default. No session was started." >&2
  exit 6
fi

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
fi

# The project: its own files (the MCP server's program, tool list and data are ordinary project
# files in every arm) and the logging hook. Then the arm's server configuration, if it has one.
rm -rf "$target"
mkdir -p "$target/.claude/hooks"
cp -r "$seed/lab/." "$target/"
cp "$seed/watch/watch-hooks.json" "$target/.claude/settings.local.json"
cp "$seed/watch/seen.mjs" "$target/.claude/hooks/seen.mjs"
[ -n "$count" ] && cp "$seed/parts/mcp.n$count.json" "$target/.mcp.json"
# A file next to the project that no session has any business touching.
parent="$(dirname "$target")"
[ -f "$parent/canary.txt" ] || echo "canary: nothing outside the project may change" > "$parent/canary.txt"

# What the log shows instead of this machine's folders, user and host: every spelling of each
# path (POSIX, C:/..., C:\..., C:\\...), then the user name in any letter case, the host name on
# word boundaries only, the account's address when the shell carries one, anything else shaped
# like an address, and long ids.
to_native() { cygpath -m "$1" 2>/dev/null || printf '%s' "$1"; }
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
for word in "${CLAUDE_CODE_USER_EMAIL:-}"; do
  [ "${#word}" -ge 3 ] && { esc "$word"; scrub+=(-e "s#$ESC#<address>#gI"); }
done
for word in "$(basename "$HOME")" "${USERNAME:-}" "${USER:-}"; do
  [ "${#word}" -ge 3 ] && { esc "$word"; scrub+=(-e "s#$ESC#<user>#gI"); }
done
for word in "${HOSTNAME:-}" "${COMPUTERNAME:-}"; do
  [ "${#word}" -ge 3 ] && { esc "$word"; scrub+=(-e "s#\\b$ESC\\b#<host>#gI"); }
done
show() {
  sed "${scrub[@]}" | sed -E \
    -e 's/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/<address>/g' \
    -e 's/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/<uuid>/g' \
    -e 's/toolu_[0-9A-Za-z]{6,}/toolu_<id>/g' \
    -e 's/agent-[0-9a-f]{6,}/agent-<id>/g'
}
logs_native="$(to_native "$LOGS")"

# Variables this shell would hand the session, by name only: a shell opened from the desktop app
# carries dozens, and some change what a session loads or how its requests grow. The values are
# never read here. Eight of them are taken out of the session's environment whatever they hold:
# each would change every arm (tool search, experimental betas, how long an MCP description may
# be, how long the first turn waits for a server, bare mode, safe mode, no CLAUDE.md, no caching).
REMOVED=(ENABLE_TOOL_SEARCH CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS CLAUDE_CODE_MAX_MCP_DESCRIPTION_LENGTH CLAUDE_CODE_MCP_STARTUP_WAIT_MS CLAUDE_CODE_SIMPLE CLAUDE_CODE_SAFE_MODE CLAUDE_CODE_DISABLE_CLAUDE_MDS DISABLE_PROMPT_CACHING)
unsets=()
for each in "${REMOVED[@]}"; do unsets+=(-u "$each"); done
handed="$(compgen -e | grep -E '^(CLAUDE_|CLAUDECODE$|ANTHROPIC_|MCP_|MAX_MCP_|ENABLE_|DISABLE_|API_TIMEOUT|MAX_THINKING)' | sort | tr '\n' ' ')"
taken=""
for each in "${REMOVED[@]}"; do [ -n "${!each+x}" ] && taken="$taken $each"; done

# The command, as two arrays: what goes into the environment and what goes to claude.
envs=(CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false)
envs+=("CLAUDE_CODE_SUBAGENT_MODEL=$MODEL" CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1)
envs+=("SEEN_LOG=$logs_native/$name.seen.txt")
[ -n "$search" ] && envs+=("ENABLE_TOOL_SEARCH=$search")
args=(-p --model "$MODEL" --permission-mode default --setting-sources project,local --strict-mcp-config)
[ -n "$count" ] && args+=(--mcp-config .mcp.json)
args+=(--tools "$TOOLS" --allowedTools "$ALLOWED")
args+=(--no-session-persistence --max-budget-usd "$BUDGET" --output-format stream-json --verbose --include-hook-events)
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
  local dir total=0 skills=0 agents=0 settings=0 md=0 agentsmd=0 mcpjson=0 plug=0 git=0
  # The shell's own spelling of the folder, so the count does not depend on how WORK was typed
  # (C:/... and /c/... are the same place).
  dir="$(cd "$(dirname "$target")" && pwd)"
  while :; do
    total=$((total + 1))
    [ -d "$dir/.claude/skills" ] && skills=$((skills + 1))
    [ -d "$dir/.claude/agents" ] && agents=$((agents + 1))
    { [ -f "$dir/.claude/settings.json" ] || [ -f "$dir/.claude/settings.local.json" ]; } && settings=$((settings + 1))
    { [ -f "$dir/CLAUDE.md" ] || [ -f "$dir/.claude/CLAUDE.md" ] || [ -f "$dir/CLAUDE.local.md" ]; } && md=$((md + 1))
    [ -f "$dir/AGENTS.md" ] && agentsmd=$((agentsmd + 1))
    [ -f "$dir/.mcp.json" ] && mcpjson=$((mcpjson + 1))
    [ -d "$dir/.claude-plugin" ] && plug=$((plug + 1))
    [ -e "$dir/.git" ] && git=$((git + 1))
    [ "$(dirname "$dir")" = "$dir" ] && break
    dir="$(dirname "$dir")"
  done
  echo "$total folders above <lab> | with .claude/skills: $skills | with .claude/agents: $agents | with .claude settings: $settings | with a CLAUDE.md: $md | with AGENTS.md: $agentsmd | with a .mcp.json: $mcpjson | with .claude-plugin: $plug | with .git: $git"
}

# Three places outside the project: the folder above it without the project, the records and
# the dry folder; the seed; and the records of every other run. Each as "N files, digest": the digest is over every file's name and SHA-256.
listing() { (cd "$1" && find . -mindepth 1 "${@:2}" -type f -print | sort | xargs -r sha256sum); }
count_of() { echo "$(printf '%s\n' "$1" | grep -c .) files, digest $(printf '%s\n' "$1" | sha256sum | cut -c1-16)"; }
outside() {
  count_of "$(listing "$1" \( -path "./$(basename "$LAB")" -o -path "./$(basename "$LOGS")" -o -path "./$(basename "$DRY")" \) -prune -o)"
}
others() { count_of "$(listing "$LOGS" -path "./$name.*" -prune -o)"; }
whole() { if [ -d "$1" ]; then count_of "$(listing "$1")"; else echo "no such folder"; fi; }

header() {
  echo "# $name | arm $arm | start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## the project before the session (rebuilt from <seed>/lab, <seed>/watch and <seed>/parts)"
  echo '$ find . -type f | sort'
  (cd "$target" && find . -type f | sort)
  echo '$ sha256sum (every file, first 16 hex digits)'
  (cd "$target" && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
  echo "## the server this arm attaches"
  if [ -n "$count" ]; then echo "gear, the first $count of its 40 tools (.mcp.json is <seed>/parts/mcp.n$count.json)"; else echo "(none: this arm has no .mcp.json and passes no --mcp-config)"; fi
  echo "## above the project (counts only)"
  above
  echo "## two variables that change how MCP tools load (never the first one's value): ANTHROPIC_BASE_URL $api_kind | ENABLE_TOOL_SEARCH in this shell $([ -n "${ENABLE_TOOL_SEARCH:-}" ] && echo "set (removed for the session)" || echo "not set") | this arm sets it to: ${search:-nothing (unset, the default)}"
  echo "## variables this shell hands the session (names only, never values; the list depends on the shell): ${handed:-none }| of them removed for the session:${taken:- none}"
  echo "## the request ($prompt)"
  cat "$seed/prompts/$prompt"
  echo "## the session"
  echo "\$ env $(quoted "${unsets[@]}") $(quoted "${envs[@]}") \\"
  echo "    timeout $wait claude $(quoted "${args[@]}") \\"
  echo "    < <seed>/prompts/$prompt > <logs>/$name.stream.jsonl 2> <logs>/$name.stderr.txt"
}

if [ -n "$dry" ]; then
  { header; echo "[dry run: no session was started; <lab> here is in the dry folder, and <logs> was not touched]"; } | show
  exit 0
fi

# Every line goes into the record through show, as it is written: a run that is stopped half
# way (a closed terminal, a tool's time limit) leaves no line with this machine's names in it.
log="$LOGS/$name.session.txt"
header | show > "$log"
[ "$CLAUDE" = claude ] || echo "[the claude command was replaced by \"$CLAUDE\": no session was started, no model was called]" | show >> "$log"

before_parent="$(outside "$parent")"
before_seed="$(whole "$seed")"
before_above="$(above)"
before_logs="$(others)"
started=$(date +%s)
(
  cd "$LAB" && env "${unsets[@]}" "${envs[@]}" \
    timeout "$wait" "$CLAUDE" "${args[@]}" \
    < "$seed/prompts/$prompt" > "$LOGS/$name.stream.jsonl" 2> "$LOGS/$name.stderr.txt"
)
code=$?
after_parent="$(outside "$parent")"
after_seed="$(whole "$seed")"
after_above="$(above)"
after_logs="$(others)"

# Keep the project as the session left it: the next session rebuilds <lab>.
cp -r "$LAB" "$LOGS/$name.lab"

count_lines() { if [ -f "$2" ]; then grep -c -E -- "$1" "$2"; else echo 0; fi; }
same() { [ "$1" = "$2" ] && echo "unchanged ($1)" || echo "CHANGED: before $1 | after $2  <- STOP and look"; }
kept() { if [ -s "$1" ]; then cat "$1"; else echo "$2"; fi; }
{
  echo "[exit $code] ($(( $(date +%s) - started )) s, ended $(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "[stream lines: $(wc -l < "$LOGS/$name.stream.jsonl") | stderr bytes: $(wc -c < "$LOGS/$name.stderr.txt")]"
  echo '$ head -8 <logs>/'"$name"'.stderr.txt (cut at 200 columns)'
  head -8 "$LOGS/$name.stderr.txt" | cut -c1-200
  echo "## outside the project"
  echo "the folder above <lab>, without <lab>, the records and the dry folder: $(same "$before_parent" "$after_parent")"
  echo "the seed: $(same "$before_seed" "$after_seed")"
  echo "the records of every other run in <logs>: $(same "$before_logs" "$after_logs")"
  echo "the counts of Claude Code folders and files above <lab>: $([ "$before_above" = "$after_above" ] && echo "unchanged" || echo "CHANGED  <- STOP and look")"
  echo "## what the project's logging hook saw (<logs>/$name.seen.txt)"
  kept "$LOGS/$name.seen.txt" "(empty: no hook event reached the logger)"
  echo "## what the MCP server kept (server/requests.txt in the project; the file is not in the seed)"
  kept "$LAB/server/requests.txt" "(no such file: the server process never started)"
  echo "## anything that is not the seed's, counted from the logging hook's record (each should be 0; after.mjs below says STOP for them)"
  echo "lines with (another agent): $(count_lines '\(another agent\)' "$LOGS/$name.seen.txt") | with another MCP server's tool: $(count_lines 'mcp__\((a server|other)\)' "$LOGS/$name.seen.txt") | with (outside the project...): $(count_lines '\(outside the project' "$LOGS/$name.seen.txt") | file-tool calls the hook stopped (BLOCKED): $(count_lines 'BLOCKED$' "$LOGS/$name.seen.txt") | instruction files loaded: $(count_lines '^InstructionsLoaded' "$LOGS/$name.seen.txt")"
  echo "## each request of the main conversation (the script a viewer runs on a stream of their own)"
  echo "\$ node <seed>/ctx-cost.mjs <logs>/$name.stream.jsonl"
  node "$seed/ctx-cost.mjs" "$LOGS/$name.stream.jsonl"
  echo "## the init event against the arm, what was searched for and called"
  echo "\$ node <seed>/runner/after.mjs <logs>/$name.stream.jsonl"
  node "$seed/runner/after.mjs" "$LOGS/$name.stream.jsonl"
  echo "## the debug record and stderr (counts and numbers; no line of them is printed)"
  echo "\$ node <seed>/runner/debug-seen.mjs <logs>/$name.debug.txt <logs>/$name.stderr.txt"
  node "$seed/runner/debug-seen.mjs" "$LOGS/$name.debug.txt" "$LOGS/$name.stderr.txt"
  echo "## what was said: every result text"
  echo "\$ node <seed>/runner/said.mjs <logs>/$name.stream.jsonl"
  node "$seed/runner/said.mjs" "$LOGS/$name.stream.jsonl"
  echo "# $name | end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} 2>&1 | show >> "$log"

cat "$log"
