#!/usr/bin/env bash
# One headless Claude Code session for the 2026-10-11 runs of the Skills video: the same
# procedure kept in CLAUDE.md beside the same procedure as a skill, on the same request.
# The session's command line is session.sh's, flag for flag; what is new is the arms, a second
# request, and one more check after the session (drift.mjs).
#
#   bash <seed>/session-2.sh <name> <arm> <request> [--dry] [--force]
#
# arm        what the project holds besides the four seed files and the logging hook
# none       nothing
# claudemd   CLAUDE.md with the release procedure (variants/CLAUDE.release.md), no skill
# skill      .claude/skills/release-prep/ (the specific description) and its template.md
# claudemd5  CLAUDE.md with five procedures (variants/CLAUDE.five.md), no skill
# skill5     the same five procedures as five skills
# gated      the skill arm with one more frontmatter line, disable-model-invocation: true
#            (variants/release-prep.gated.skill.md; only made if the plan's condition is met)
#
# request    ship   prompts/ship.txt   0.3.1 要出了，幫我把該改的地方都改好。
#            look   prompts/look.txt   0.3.1 快要出了，先幫我看一下 CHANGELOG 有沒有漏記的。
#            slash  prompts/slash.txt  /release-prep 0.3.1
#
# --dry    builds the project in <dry>, prints the command, starts no session, calls no model,
#          and touches neither <lab> nor <logs>.
# --force  a name that already has records is refused; with --force the old records are moved
#          to <logs>/replaced/<name>.<time>/ first. Nothing is ever deleted from <logs>.
#
# WORK, LAB, LOGS, DRY and MODEL may be set in the environment.
set -u
name="${1:?name, for example md1}"
arm="${2:?arm: none, claudemd, skill, claudemd5, skill5 or gated}"
request="${3:?request: ship, look or slash}"
shift 3
dry=""; force=""
for flag in "$@"; do
  case "$flag" in
    --dry) dry=1 ;;
    --force) force=1 ;;
    *) echo "unknown flag: $flag" >&2; exit 2 ;;
  esac
done

seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-skills-hands-on}"
LAB="${LAB:-$work/run/skill-lab}"
LOGS="${LOGS:-$work/run/logs}"
DRY="${DRY:-$work/run/dry-lab}"
MODEL="${MODEL:-sonnet}"

case "$arm" in
  none|claudemd|skill|claudemd5|skill5|gated) ;;
  *) echo "unknown arm: $arm" >&2; exit 2 ;;
esac
case "$request" in
  ship|look|slash) prompt="$request.txt" ;;
  *) echo "unknown request: $request" >&2; exit 2 ;;
esac

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

native() { (cd "$1" && (pwd -W 2>/dev/null || pwd)); }
home_native="$(native "$HOME")"
user="$(basename "$HOME")"
# What the log shows instead of this machine's folders.
show() { sed -e "s#$target_native#<lab>#g" -e "s#$logs_native#<logs>#g" -e "s#$seed_native#<seed>#g" \
  -e "s#$target#<lab>#g" -e "s#$LOGS#<logs>#g" -e "s#$seed#<seed>#g" \
  -e "s#$home_native#<home>#g" -e "s#$HOME#<home>#g" -e "s#$user#<user>#g"; }

tools="Read,Glob,Grep,Edit,Write,Skill"
place() { mkdir -p "$target/.claude/skills/$1" && cp "$seed/variants/$2" "$target/.claude/skills/$1/SKILL.md"; }

rm -rf "$target"
mkdir -p "$target/.claude/hooks"
cp -r "$seed/skill-lab/." "$target/"
cp "$seed/skill-log/settings.json" "$target/.claude/settings.json"
cp "$seed/skill-log/seen.mjs" "$target/.claude/hooks/seen.mjs"
case "$arm" in
  none) ;;
  claudemd) cp "$seed/variants/CLAUDE.release.md" "$target/CLAUDE.md" ;;
  skill) place release-prep release-prep.specific.skill.md ;;
  gated) place release-prep release-prep.gated.skill.md ;;
  claudemd5) cp "$seed/variants/CLAUDE.five.md" "$target/CLAUDE.md" ;;
  skill5)
    place release-prep release-prep.specific.skill.md
    place changelog-entry changelog-entry.skill.md
    place add-converter add-converter.skill.md
    place bug-report bug-report.skill.md
    place readme-example readme-example.skill.md ;;
esac
if [ -d "$target/.claude/skills/release-prep" ]; then
  cp "$seed/variants/release-prep.template.md" "$target/.claude/skills/release-prep/template.md"
fi

target_native="$(native "$target")"
if [ -d "$LOGS" ]; then logs_native="$(native "$LOGS")"; else logs_native="$LOGS"; fi
seed_native="$(native "$seed")"

# Folders above the project that could hand the session something: counted, never named.
above() {
  local dir total=0 skills=0 commands=0 md=0 agents=0 git=0
  dir="$(dirname "$target")"
  while :; do
    total=$((total + 1))
    [ -d "$dir/.claude/skills" ] && skills=$((skills + 1))
    [ -d "$dir/.claude/commands" ] && commands=$((commands + 1))
    { [ -f "$dir/CLAUDE.md" ] || [ -f "$dir/.claude/CLAUDE.md" ] || [ -f "$dir/CLAUDE.local.md" ]; } && md=$((md + 1))
    [ -f "$dir/AGENTS.md" ] && agents=$((agents + 1))
    [ -e "$dir/.git" ] && git=$((git + 1))
    [ "$(dirname "$dir")" = "$dir" ] && break
    dir="$(dirname "$dir")"
  done
  echo "$total folders above <lab> | with .claude/skills: $skills | with .claude/commands: $commands | with a CLAUDE.md: $md | with AGENTS.md: $agents | with .git: $git"
}

header() {
  echo "# $name | arm $arm | request $request | start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "## the project before the session (rebuilt from <seed>/skill-lab)"
  echo '$ find . -type f | sort'
  (cd "$target" && find . -type f | sort)
  echo '$ sha256sum (every file, first 16 hex digits)'
  (cd "$target" && find . -type f | sort | xargs sha256sum | cut -c1-16,65-)
  echo "## above the project (counts only)"
  above
  echo "## the request ($prompt)"
  cat "$seed/prompts/$prompt"
  echo "## what the session inherits from this shell (a count of names, then four values)"
  echo "($(env | grep -cE '^(CLAUDE|ANTHROPIC|SLASH_COMMAND)') names, left out)"
  for each in CLAUDECODE CLAUDE_CODE_ENTRYPOINT CLAUDE_CODE_SIMPLE CLAUDE_EFFORT; do echo "$each=${!each-<unset>}"; done
  echo "## the session"
  echo "\$ env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SKILL_LOG=<logs>/$name.seen.log \\"
  echo "    timeout 300 claude -p --model $MODEL --setting-sources project,local --strict-mcp-config \\"
  echo "    --tools \"$tools\" --allowedTools \"$tools\" --no-session-persistence \\"
  echo "    --output-format stream-json --verbose \\"
  echo "    --debug-file <logs>/$name.debug.log \\"
  echo "    < <seed>/prompts/$prompt > <logs>/$name.stream.jsonl 2> <logs>/$name.stderr.txt"
}

if [ -n "$dry" ]; then
  { header; echo "[dry run: no session was started; <lab> here is the dry folder, and <logs> was not touched]"; } | show
  exit 0
fi

log="$LOGS/$name.session.log"
header > "$log"

started=$(date +%s)
(
  cd "$LAB" && env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 SKILL_LOG="$logs_native/$name.seen.log" \
    timeout 300 claude -p --model "$MODEL" --setting-sources project,local --strict-mcp-config \
    --tools "$tools" --allowedTools "$tools" --no-session-persistence \
    --output-format stream-json --verbose \
    --debug-file "$logs_native/$name.debug.log" \
    < "$seed/prompts/$prompt" > "$LOGS/$name.stream.jsonl" 2> "$LOGS/$name.stderr.txt"
)
code=$?

# Keep the project as the session left it: the next session rebuilds <lab>.
cp -r "$LAB" "$LOGS/$name.lab"

{
  echo "[exit $code] ($(( $(date +%s) - started )) s, ended $(date -u +%Y-%m-%dT%H:%M:%SZ))"
  echo "[stream lines: $(wc -l < "$LOGS/$name.stream.jsonl") | stderr bytes: $(wc -c < "$LOGS/$name.stderr.txt")]"
  echo "## the project after the session (kept as <logs>/$name.lab)"
  echo "\$ find . -type f -not -path './.claude/*' | sort"
  (cd "$LAB" && find . -type f -not -path './.claude/*' | sort)
  echo "\$ grep '\"version\"' package.json"
  (cd "$LAB" && grep '"version"' package.json)
  echo '$ head -8 CHANGELOG.md'
  (cd "$LAB" && head -8 CHANGELOG.md)
  echo "\$ grep 'Latest release' README.md"
  (cd "$LAB" && grep 'Latest release' README.md)
  echo "\$ grep -h '^#' releases/*.md"
  (cd "$LAB" && grep -h '^#' releases/*.md 2>&1)
  echo '$ sha256sum src/units.mjs (first 16 hex digits)'
  (cd "$LAB" && sha256sum src/units.mjs | cut -c1-16,65-)
  echo "## what the logging hook saw (<logs>/$name.seen.log)"
  if [ -s "$LOGS/$name.seen.log" ]; then cat "$LOGS/$name.seen.log"; else echo "(empty: no hook event reached the logger)"; fi
  echo "## from the stream"
  echo "\$ grep -c '\"name\":\"Skill\"' <logs>/$name.stream.jsonl"
  grep -c '"name":"Skill"' "$LOGS/$name.stream.jsonl"
  echo "\$ node <seed>/tally.mjs <logs>/$name.stream.jsonl"
  node "$seed/tally.mjs" "$LOGS/$name.stream.jsonl"
  echo "## against the seed"
  echo "\$ node <seed>/drift.mjs <logs>/$name.stream.jsonl"
  node "$seed/drift.mjs" "$LOGS/$name.stream.jsonl"
  echo "## the debug log on skills"
  echo "\$ grep -E 'Loaded [0-9]+ unique skills|Sending [0-9]+ skills via attachment|SkillTool returning' <logs>/$name.debug.log (time stamps cut)"
  grep -E 'Loaded [0-9]+ unique skills|Sending [0-9]+ skills via attachment|SkillTool returning' "$LOGS/$name.debug.log" 2>/dev/null | sed -E 's/^[^ ]+ //' | cut -c1-200
  echo "# $name | end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} >> "$log" 2>&1

show < "$log" > "$log.shown" && mv "$log.shown" "$log"
cat "$log"
