#!/usr/bin/env bash
# One headless Claude Code session for the plugins video, in a project rebuilt from the seed.
#
#   bash <seed>/session.sh <name> <arm> [--dry] [--force]
#
# Two throwaway projects and one plugin are assembled from the seed's neutral file names:
#   project A, trip-queue (lab-a/):  the project the three parts were written in
#   project B, fare-sync  (lab-b/):  a second project that has none of them
#   the plugin, ship-kit  (kit.sh):  the same three parts, a manifest, one hook path changed
# The three parts are a skill (release-prep, with its template), a subagent (log-scout) and a
# hook (guard.mjs on Edit|Write). In a project they live in .claude/; in the plugin they live in
# skills/, agents/, hooks/hooks.json and scripts/.
#
# arm     project  the parts in .claude/  plugin loaded with --plugin-dir   asked
# bare    B        no                     none                              ship-b.txt
# kit     B        no                     ship-kit                          ship-b.txt
# origin  A        yes                    none                              ship-a.txt
# both    A        yes                    ship-kit                          ship-a.txt
# guard   B        no                     ship-kit                          guard-b.txt
# stale   B        no                     ship-kit, hooks file not adapted  guard-b.txt
# strict  B        no                     ship-kit                          ship-b.txt   (reads are not pre-approved)
# slash   B        no                     ship-kit                          slash-b.txt
# short   B        no                     ship-kit                          short-b.txt  (prepared, not in the list)
#
# Every arm: -p, --model sonnet, --permission-mode default (Manual), --setting-sources
# project,local, --strict-mcp-config with no MCP configuration, the tools Read Glob Grep Edit
# Write Skill Agent(Task) and no Bash. Every project also carries a logging hook of its own
# (.claude/settings.local.json and .claude/hooks/seen.mjs): it is the instrument, not a part.
#
# No plugin is installed, enabled or listed, no marketplace is touched, and no settings file but
# the seed's own is read, printed or copied. The plugin is loaded for the one session with
# --plugin-dir and is never written to: this script compares its files before and after.
#
# --dry    builds the project (and the plugin) in <dry>, prints the command, starts no session,
#          calls no model, and touches neither <lab>, <plugin> nor <logs>.
# --force  a name that already has records is refused; with --force the old records are moved
#          to <logs>/replaced/<name>.<time>/ first. Nothing is ever deleted from <logs>.
#
# WORK, LAB, KIT, LOGS, DRY, MODEL and BUDGET may be set in the environment. PLUGINS_ROOT=empty
# also points CLAUDE_CODE_PLUGIN_CACHE_DIR at an empty folder next to the project (a fallback
# for a machine whose own installed plugins show up in the init event; not used by default).
# The run folders default to a temporary directory, and the script refuses to build or record
# inside a git repository.
set -u
name="${1:?name, for example k1}"
arm="${2:?arm: bare, kit, origin, both, guard, stale, strict, slash or short}"
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
work="${WORK:-${TMPDIR:-/tmp}/claude-code-plugins-hands-on}"
LAB="${LAB:-$work/run/lab}"
KIT="${KIT:-$work/run/ship-kit}"
LOGS="${LOGS:-$work/run/logs}"
DRY="${DRY:-$work/run/dry}"
MODEL="${MODEL:-sonnet}"
BUDGET="${BUDGET:-1}"
TOOLS="Read,Glob,Grep,Edit,Write,Skill,Agent,Task"
# CLAUDE is only ever replaced by m-checks.sh, which tests the bookkeeping with a command that does nothing.
CLAUDE="${CLAUDE:-claude}"

project="b"; own=""; variant="good"; prompt="ship-b.txt"; allowed="$TOOLS"
case "$arm" in
  kit) ;;
  bare) variant="" ;;
  origin) project="a"; own=1; variant=""; prompt="ship-a.txt" ;;
  both) project="a"; own=1; prompt="ship-a.txt" ;;
  guard) prompt="guard-b.txt" ;;
  stale) variant="stale"; prompt="guard-b.txt" ;;
  strict) allowed="Edit,Write,Skill,Agent,Task" ;;
  slash) prompt="slash-b.txt" ;;
  short) prompt="short-b.txt" ;;
  *) echo "unknown arm: $arm" >&2; exit 2 ;;
esac

# Nothing is built or recorded inside a git repository: a copy of this script that lives in a
# repository must not write into it.
in_git() {
  local dir="$1"
  while [ ! -d "$dir" ]; do dir="$(dirname "$dir")"; done
  [ "$(git -C "$dir" rev-parse --is-inside-work-tree 2>/dev/null)" = "true" ]
}
if [ -n "$dry" ]; then places="$DRY"; else places="$LAB $KIT $LOGS"; fi
for each in $places; do
  if in_git "$each"; then
    echo "refused: a run folder is inside a git repository. Set WORK (or LAB, KIT, LOGS, DRY) to a folder outside any repository." >&2
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
  target="$LAB"; kit="$KIT"
else
  target="$DRY/lab"; kit="$DRY/ship-kit"
fi

# The project: its own files, the files the repository copy keeps under other names (an existing
# test, two nightly logs), and the logging hook. In arms origin and both, also the three parts.
rm -rf "$target"
mkdir -p "$target/.claude/hooks" "$target/logs"
cp -r "$seed/lab-$project/." "$target/"
if [ "$project" = a ]; then
  cp "$seed/placed/a.queue-test.mjs.txt" "$target/src/queue.test.mjs"
  cp "$seed/placed/a.jobs-1.txt" "$target/logs/queue-2026-10-08.log"
  cp "$seed/placed/a.jobs-2.txt" "$target/logs/queue-2026-10-09.log"
else
  cp "$seed/placed/b.fares-test.mjs.txt" "$target/src/fares.test.mjs"
  cp "$seed/placed/b.jobs-1.txt" "$target/logs/sync-2026-10-08.log"
  cp "$seed/placed/b.jobs-2.txt" "$target/logs/sync-2026-10-09.log"
fi
cp "$seed/watch/watch-hooks.json" "$target/.claude/settings.local.json"
cp "$seed/watch/seen.mjs" "$target/.claude/hooks/seen.mjs"
if [ -n "$own" ]; then
  mkdir -p "$target/.claude/skills/release-prep" "$target/.claude/agents"
  cp "$seed/parts/release-prep.skill.md" "$target/.claude/skills/release-prep/SKILL.md"
  cp "$seed/parts/release-prep.template.md" "$target/.claude/skills/release-prep/template.md"
  cp "$seed/parts/log-scout.agent.md" "$target/.claude/agents/log-scout.md"
  cp "$seed/parts/guard.mjs" "$target/.claude/hooks/guard.mjs"
  cp "$seed/parts/hooks.project.json" "$target/.claude/settings.json"
fi
# The plugin, or no folder at all in the arms that load none.
rm -rf "$kit"
if [ -n "$variant" ]; then bash "$seed/kit.sh" "$variant" "$kit" || exit $?; fi
# A file next to the project that no session has any business touching.
parent="$(dirname "$target")"
[ -f "$parent/canary.txt" ] || echo "canary: nothing outside the project may change" > "$parent/canary.txt"
plugins_root=""
if [ "${PLUGINS_ROOT:-}" = empty ]; then plugins_root="$parent/plugins-root"; mkdir -p "$plugins_root"; fi

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
hide "$kit" "<plugin>"
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
    -e 's/toolu_[0-9A-Za-z]{6,}/toolu_<id>/g' \
    -e 's/agent-[0-9a-f]{6,}/agent-<id>/g'
}
logs_native="$(to_native "$LOGS")"
kit_native="$(to_native "$kit")"

# The command, as two arrays: what goes into the environment and what goes to claude.
envs=(CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 ENABLE_CLAUDEAI_MCP_SERVERS=false)
envs+=("CLAUDE_CODE_SUBAGENT_MODEL=$MODEL" CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1)
envs+=("SEEN_LOG=$logs_native/$name.seen.txt" "GUARD_LOG=$logs_native/$name.guard.txt" "KIT_DIR=$kit_native")
[ -n "$plugins_root" ] && envs+=("CLAUDE_CODE_PLUGIN_CACHE_DIR=$(to_native "$plugins_root")")
args=(-p --model "$MODEL" --permission-mode default --setting-sources project,local --strict-mcp-config)
args+=(--tools "$TOOLS" --allowedTools "$allowed")
[ -n "$variant" ] && args+=(--plugin-dir "$kit_native")
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
  local dir total=0 skills=0 agents=0 settings=0 md=0 agentsmd=0 plug=0 git=0
  dir="$(dirname "$target")"
  while :; do
    total=$((total + 1))
    [ -d "$dir/.claude/skills" ] && skills=$((skills + 1))
    [ -d "$dir/.claude/agents" ] && agents=$((agents + 1))
    { [ -f "$dir/.claude/settings.json" ] || [ -f "$dir/.claude/settings.local.json" ]; } && settings=$((settings + 1))
    { [ -f "$dir/CLAUDE.md" ] || [ -f "$dir/.claude/CLAUDE.md" ] || [ -f "$dir/CLAUDE.local.md" ]; } && md=$((md + 1))
    [ -f "$dir/AGENTS.md" ] && agentsmd=$((agentsmd + 1))
    [ -d "$dir/.claude-plugin" ] && plug=$((plug + 1))
    [ -e "$dir/.git" ] && git=$((git + 1))
    [ "$(dirname "$dir")" = "$dir" ] && break
    dir="$(dirname "$dir")"
  done
  echo "$total folders above <lab> | with .claude/skills: $skills | with .claude/agents: $agents | with .claude settings: $settings | with a CLAUDE.md: $md | with AGENTS.md: $agentsmd | with .claude-plugin: $plug | with .git: $git"
}

# The folder above the project without the project, the plugin, the records, the dry folder and
# the optional empty plugins root; the plugin; and the seed. Each as "N files, digest": the
# digest is over every file's name and SHA-256.
listing() { (cd "$1" && find . -mindepth 1 "${@:2}" -type f -print | sort | xargs -r sha256sum); }
count_of() { echo "$(printf '%s\n' "$1" | grep -c .) files, digest $(printf '%s\n' "$1" | sha256sum | cut -c1-16)"; }
outside() {
  count_of "$(listing "$1" \( -path "./$(basename "$LAB")" -o -path "./$(basename "$KIT")" -o -path "./$(basename "$LOGS")" -o -path "./$(basename "$DRY")" -o -path "./plugins-root" \) -prune -o)"
}
whole() { if [ -d "$1" ]; then count_of "$(listing "$1")"; else echo "no such folder"; fi; }

header() {
  echo "# $name | arm $arm | start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## the project before the session (project $project, rebuilt from <seed>/lab-$project and <seed>/placed)"
  echo '$ find . -type f | sort'
  (cd "$target" && find . -type f | sort)
  echo '$ sha256sum (every file, first 16 hex digits)'
  (cd "$target" && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
  echo '$ cat .claude/settings.json'
  if [ -f "$target/.claude/settings.json" ]; then cat "$target/.claude/settings.json"; else echo "(no such file in this arm)"; fi
  echo "## the plugin before the session (kit.sh ${variant:-none})"
  if [ -n "$variant" ]; then
    echo '$ find . -type f | sort    (in <plugin>)'
    (cd "$kit" && find . -type f | sort)
    echo '$ sha256sum (every file, first 16 hex digits)'
    (cd "$kit" && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
    echo '$ cat hooks/hooks.json'
    cat "$kit/hooks/hooks.json"
  else
    echo "(this arm loads no plugin, and <plugin> does not exist)"
  fi
  echo "## above the project (counts only)"
  above
  echo "## the request ($prompt)"
  cat "$seed/prompts/$prompt"
  echo "## the session"
  echo "\$ env $(quoted "${envs[@]}") \\"
  echo "    timeout 600 claude $(quoted "${args[@]}") \\"
  echo "    < <seed>/prompts/$prompt > <logs>/$name.stream.jsonl 2> <logs>/$name.stderr.txt"
}

if [ -n "$dry" ]; then
  { header; echo "[dry run: no session was started; <lab> and <plugin> here are in the dry folder, and <logs> was not touched]"; } | show
  exit 0
fi

log="$LOGS/$name.session.txt"
header > "$log"
[ "$CLAUDE" = claude ] || echo "[the claude command was replaced by \"$CLAUDE\": no session was started, no model was called]" >> "$log"

before_parent="$(outside "$parent")"
before_seed="$(whole "$seed")"
before_kit="$(whole "$kit")"
started=$(date +%s)
(
  cd "$LAB" && env "${envs[@]}" \
    timeout 600 "$CLAUDE" "${args[@]}" \
    < "$seed/prompts/$prompt" > "$LOGS/$name.stream.jsonl" 2> "$LOGS/$name.stderr.txt"
)
code=$?
after_parent="$(outside "$parent")"
after_seed="$(whole "$seed")"
after_kit="$(whole "$kit")"

# Keep the project as the session left it: the next session rebuilds <lab>.
cp -r "$LAB" "$LOGS/$name.lab"

count() { if [ -f "$2" ]; then grep -c -E -- "$1" "$2"; else echo 0; fi; }
same() { [ "$1" = "$2" ] && echo "unchanged ($1)" || echo "CHANGED: before $1 | after $2  <- STOP and look"; }
{
  echo "[exit $code] ($(( $(date +%s) - started )) s, ended $(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "[stream lines: $(wc -l < "$LOGS/$name.stream.jsonl") | stderr bytes: $(wc -c < "$LOGS/$name.stderr.txt") | stderr lines that say plugin: $(count -i 'plugin' "$LOGS/$name.stderr.txt"), trust: $(count -i 'trust' "$LOGS/$name.stderr.txt")]"
  echo '$ head -8 <logs>/'"$name"'.stderr.txt (cut at 200 columns)'
  head -8 "$LOGS/$name.stderr.txt" | cut -c1-200
  echo "## outside the project"
  echo "the folder above <lab>, without <lab>, <plugin>, the records and the dry folder: $(same "$before_parent" "$after_parent")"
  echo "the plugin folder: $(same "$before_kit" "$after_kit")"
  echo "the seed: $(same "$before_seed" "$after_seed")"
  [ -n "$plugins_root" ] && echo "the empty plugins root after the session: $(find "$plugins_root" -mindepth 1 | wc -l) entries"
  echo "## what the project's logging hook saw (<logs>/$name.seen.txt)"
  if [ -s "$LOGS/$name.seen.txt" ]; then cat "$LOGS/$name.seen.txt"; else echo "(empty: no hook event reached the logger)"; fi
  echo "## what the guard wrote (<logs>/$name.guard.txt)"
  if [ -s "$LOGS/$name.guard.txt" ]; then cat "$LOGS/$name.guard.txt"; else echo "(empty: the guard never ran, or could not write)"; fi
  echo "## anything that is not the seed's, counted from the logging hook's record (each should be 0)"
  echo "lines with (another skill): $(count '\(another skill\)' "$LOGS/$name.seen.txt") | with (another agent): $(count '\(another agent\)' "$LOGS/$name.seen.txt") | with an MCP tool: $(count 'mcp__\(a server\)' "$LOGS/$name.seen.txt") | with (outside the project): $(count '\(outside the project\)' "$LOGS/$name.seen.txt") | instruction files loaded (no project has one): $(count '^InstructionsLoaded' "$LOGS/$name.seen.txt")"
  echo "## from the stream and the project as the session left it"
  echo "\$ node <seed>/tally.mjs <logs>/$name.stream.jsonl"
  KIT_DIR="$kit_native" node "$seed/tally.mjs" "$LOGS/$name.stream.jsonl"
  echo "## the debug record and stderr on plugins (counts; only the seed's own names are ever printed)"
  node "$seed/runner/loader-seen.mjs" "$LOGS/$name.debug.txt" "$LOGS/$name.stderr.txt"
  echo "# $name | end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log" 2>&1

show < "$log" > "$log.shown" && mv "$log.shown" "$log"
cat "$log"
