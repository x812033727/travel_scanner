#!/usr/bin/env bash
# One headless Claude Code session for the permission-rules video, in a project rebuilt from the seed.
#
#   bash <seed>/session.sh <name> <arm> [--dry] [--force]
#
# Every arm starts from the same project (fare-lab: a fare calculator with one failing check, a
# rate table, two scripts, a .env of made-up values, and a logging hook) and offers the same six
# built-in tools: Read, Edit, Write, Bash, Glob, Grep. Every arm passes --permission-mode default
# (Manual), --setting-sources project,local and --strict-mcp-config with no MCP configuration.
# What differs is where the permission rules are and what is asked:
#
# arm     the rules file                                  allow rules also by flag   asked
# none    not placed                                      no                         work.txt
# with    rules.main.json as .claude/settings.json        yes (--allowedTools)       work.txt
# proj    rules.main.json as .claude/settings.json        no                         work.txt
# local   rules.main.json inside .claude/settings.local.json  no                     work.txt
# read    as with                                         yes                        read.txt
# bash    as with, and src/fare.mjs already fixed         yes                        bash.txt
# edit    rules.open.json as .claude/settings.json        yes                        edit.txt
# byfile  rules.main.json as .claude/rules.json, passed with --settings  no          work.txt  (prepared, not in the list)
#
# The seed keeps the rules under neutral names (rules/rules.*.json), the hook settings outside any
# .claude folder and the made-up .env as placed/env.fake.txt, so that a copy of the seed inside a
# repository gives that repository's own Claude Code sessions no rule and no hook, and git has no
# .env to ignore. This script puts them where Claude Code looks: <lab>/.claude/settings.json,
# <lab>/.claude/settings.local.json (the logging hook), <lab>/.claude/hooks/seen.mjs, <lab>/.env.
#
# Bash is offered in every arm. What keeps it harmless: the project is a throwaway folder outside
# any repository; the "deploy" script only appends a line to a file inside the project; the .env
# holds made-up strings; no request asks for the network, an install, or anything outside the
# project; no arm uses a bypass mode. After the session this script compares a listing with hashes
# of the folder above the project, and of the seed, with the one it took before.
#
# --dry    builds the project in <dry>, prints the command, starts no session, calls no model,
#          and touches neither <lab> nor <logs>.
# --force  a name that already has records is refused; with --force the old records are moved
#          to <logs>/replaced/<name>.<time>/ first. Nothing is ever deleted from <logs>.
#
# WORK, LAB, LOGS, DRY, MODEL and BUDGET may be set in the environment. The run folders default to
# a temporary directory, and the script refuses to build or record inside a git repository. It
# never reads, prints or copies any settings file but the seed's own.
set -u
name="${1:?name, for example w1}"
arm="${2:?arm: none, with, proj, local, read, bash, edit or byfile}"
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
work="${WORK:-${TMPDIR:-/tmp}/claude-code-permissions-hands-on}"
LAB="${LAB:-$work/run/fare-lab}"
LOGS="${LOGS:-$work/run/logs}"
DRY="${DRY:-$work/run/dry-lab}"
MODEL="${MODEL:-sonnet}"
BUDGET="${BUDGET:-1}"
TOOLS="Read,Edit,Write,Bash,Glob,Grep"
# CLAUDE is only ever replaced by m-checks.sh, which tests the bookkeeping with a command that does nothing.
CLAUDE="${CLAUDE:-claude}"

rules="rules.main.json"; place="project"; byflag=1; prompt="work.txt"; fixed=""
case "$arm" in
  with) ;;
  none) rules=""; place=""; byflag="" ;;
  proj) byflag="" ;;
  local) place="local"; byflag="" ;;
  read) prompt="read.txt" ;;
  bash) prompt="bash.txt"; fixed=1 ;;
  edit) rules="rules.open.json"; prompt="edit.txt" ;;
  byfile) place="byfile"; byflag="" ;;
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
for each in $places; do
  if in_git "$each"; then
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
cp -r "$seed/lab/." "$target/"
cp "$seed/placed/env.fake.txt" "$target/.env"
cp "$seed/placed/env.example.txt" "$target/.env.example"
[ -n "$fixed" ] && cp "$seed/placed/fare.fixed.mjs" "$target/src/fare.mjs"
cp "$seed/hook-log/seen.mjs" "$target/.claude/hooks/seen.mjs"
cp "$seed/hook-log/hooks.json" "$target/.claude/settings.local.json"
case "$place" in
  project) cp "$seed/rules/$rules" "$target/.claude/settings.json" ;;
  byfile) cp "$seed/rules/$rules" "$target/.claude/rules.json" ;;
  local) node "$seed/runner/merge.mjs" "$seed/hook-log/hooks.json" "$seed/rules/$rules" > "$target/.claude/settings.local.json" ;;
esac
# A file next to the project that no session has any business touching.
parent="$(dirname "$target")"
[ -f "$parent/canary.txt" ] || echo "canary: nothing outside the project may change" > "$parent/canary.txt"

# What the log shows instead of this machine's folders, user and host: every spelling of each
# path (POSIX, C:/..., C:\..., C:\\...), then the user name, then the host name on word
# boundaries only, and long ids.
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
for word in "$(basename "$HOME")" "${USERNAME:-}" "${USER:-}"; do
  [ "${#word}" -ge 3 ] && { esc "$word"; scrub+=(-e "s#$ESC#<user>#g"); }
done
for word in "${HOSTNAME:-}" "${COMPUTERNAME:-}"; do
  [ "${#word}" -ge 3 ] && { esc "$word"; scrub+=(-e "s#\\b$ESC\\b#<host>#gI"); }
done
show() {
  sed "${scrub[@]}" | sed -E \
    -e 's/[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}/<uuid>/g' \
    -e 's/toolu_[0-9A-Za-z]{6,}/toolu_<id>/g'
}
logs_native="$(to_native "$LOGS")"

# The command, as two arrays: what goes into the environment and what goes to claude.
envs=(CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false NPM_CONFIG_UPDATE_NOTIFIER=false "SEEN_LOG=$logs_native/$name.seen.txt")
args=(-p --model "$MODEL" --permission-mode default --setting-sources project,local --strict-mcp-config)
args+=(--tools "$TOOLS")
[ "$place" = byfile ] && args+=(--settings .claude/rules.json)
if [ -n "$byflag" ]; then
  args+=(--allowedTools)
  while IFS= read -r each; do args+=("$each"); done < <(node "$seed/runner/allow-list.mjs" "$seed/rules/$rules")
fi
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

# The folder above the project without the project, the records and the dry folder; and the
# seed. Each as "N files, digest": the digest is over every file's name and SHA-256.
outside() {
  local where="$1" list
  list="$(cd "$where" && find . -mindepth 1 \( -path "./$(basename "$LAB")" -o -path "./$(basename "$LOGS")" -o -path "./$(basename "$DRY")" \) -prune -o -type f -print | sort | xargs -r sha256sum)"
  echo "$(printf '%s\n' "$list" | grep -c .) files, digest $(printf '%s\n' "$list" | sha256sum | cut -c1-16)"
}

header() {
  echo "# $name | arm $arm | start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## the project before the session (rebuilt from <seed>/lab)"
  echo '$ find . -type f | sort'
  (cd "$target" && find . -type f | sort)
  echo '$ sha256sum (every file, first 16 hex digits)'
  (cd "$target" && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
  echo '$ cat .claude/settings.json'
  if [ -f "$target/.claude/settings.json" ]; then cat "$target/.claude/settings.json"; else echo "(no such file in this arm)"; fi
  echo "## permission rules in .claude/settings.local.json (the logging hook lives there): $(node "$seed/runner/allow-list.mjs" --count "$target/.claude/settings.local.json")"
  echo "## above the project (counts only)"
  above
  echo "## the request ($prompt)"
  cat "$seed/prompts/$prompt"
  echo "## the session"
  echo "\$ env $(quoted "${envs[@]}") \\"
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

before_parent="$(outside "$parent")"
before_seed="$(outside "$seed")"
started=$(date +%s)
(
  cd "$LAB" && env "${envs[@]}" \
    timeout 300 "$CLAUDE" "${args[@]}" \
    < "$seed/prompts/$prompt" > "$LOGS/$name.stream.jsonl" 2> "$LOGS/$name.stderr.txt"
)
code=$?
after_parent="$(outside "$parent")"
after_seed="$(outside "$seed")"

# Keep the project as the session left it: the next session rebuilds <lab>.
cp -r "$LAB" "$LOGS/$name.lab"

count() { if [ -f "$2" ]; then grep -c -E -- "$1" "$2"; else echo 0; fi; }
same() { [ "$1" = "$2" ] && echo "unchanged ($1)" || echo "CHANGED: before $1 | after $2  <- STOP and look"; }
{
  echo "[exit $code] ($(( $(date +%s) - started )) s, ended $(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "[stream lines: $(wc -l < "$LOGS/$name.stream.jsonl") | stderr bytes: $(wc -c < "$LOGS/$name.stderr.txt")]"
  echo '$ head -8 <logs>/'"$name"'.stderr.txt (cut at 200 columns)'
  head -8 "$LOGS/$name.stderr.txt" | cut -c1-200
  echo "## outside the project"
  echo "the folder above <lab>, without <lab>, the records and the dry folder: $(same "$before_parent" "$after_parent")"
  echo "the seed: $(same "$before_seed" "$after_seed")"
  echo "## what the logging hook saw (<logs>/$name.seen.txt)"
  if [ -s "$LOGS/$name.seen.txt" ]; then cat "$LOGS/$name.seen.txt"; else echo "(empty: no hook event reached the logger)"; fi
  echo "## anything that is not the seed's, counted from the hook record (each should be 0)"
  echo "lines with an MCP tool: $(count 'mcp__\(a server\)' "$LOGS/$name.seen.txt") | with (outside the project): $(count '\(outside the project\)' "$LOGS/$name.seen.txt") | instruction files loaded (the project has none): $(count '^InstructionsLoaded' "$LOGS/$name.seen.txt")"
  echo "## from the stream and the project as the session left it"
  echo "\$ node <seed>/tally.mjs <logs>/$name.stream.jsonl"
  node "$seed/tally.mjs" "$LOGS/$name.stream.jsonl"
  echo "## the debug record and stderr on permission rules (counts; only the seed's own rules are ever printed)"
  node "$seed/runner/rules-seen.mjs" "$seed/rules/${rules:-rules.main.json}" "$LOGS/$name.debug.txt" "$LOGS/$name.stderr.txt"
  echo "# $name | end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log" 2>&1

show < "$log" > "$log.shown" && mv "$log.shown" "$log"
cat "$log"
