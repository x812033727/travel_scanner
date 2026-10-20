#!/usr/bin/env bash
# run.sh <name> <arm>   arms: skill | vague | paste | bare | slash
set -u
L="$(cd "$(dirname "$0")" && pwd)"
name="$1"; arm="$2"; dir="$L/runs/$name"
if [ -e "$dir" ]; then echo "refused: $name already has records"; exit 3; fi
mkdir -p "$dir"; lab="$dir/lab"; cp -r "$L/seed" "$lab"; mkdir -p "$lab/.claude"
printf '%s\n' '{ "disableBundledSkills": true, "syncClaudeAiSkills": false }' > "$lab/.claude/settings.json"
case "$arm" in
  skill|slash) mkdir -p "$lab/.claude/skills"; cp -r "$L/skills/good/monthly-report" "$lab/.claude/skills/";;
  vague) mkdir -p "$lab/.claude/skills"; cp -r "$L/skills/vague/monthly-report" "$lab/.claude/skills/";;
  paste|bare) ;;
  *) echo "unknown arm $arm"; exit 2;;
esac
case "$arm" in paste) prompt="$L/prompts/paste.txt";; slash) prompt="$L/prompts/slash.txt";; *) prompt="$L/prompts/vague.txt";; esac
cp "$prompt" "$dir/prompt.txt"
(cd "$lab" && find . -type f | sort | xargs sha256sum) > "$dir/before.sha256"
{
  echo "name: $name"; echo "arm: $arm"; echo "started: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "claude: $(claude --version)"; echo "node: $(node --version)"; echo "os: $(uname -srm)"
  echo "prompt_file: $(basename "$prompt") ($(wc -m < "$prompt") chars)"
  echo 'command: env -u CLAUDE_CODE_SESSION_ID claude -p "$(cat prompt)" --model sonnet --permission-mode default --tools "Read,Glob,Grep,Edit,Write,Bash,Skill" --allowedTools "Read,Glob,Grep,Edit,Write,Bash(node *),Bash(mkdir *),Bash(cat *),Bash(ls *)" --output-format stream-json --verbose --no-session-persistence --setting-sources project --strict-mcp-config --max-turns 40 --max-budget-usd 1 < /dev/null'
} > "$dir/meta.txt"
cd "$lab"
env -u CLAUDE_CODE_SESSION_ID timeout 900 claude -p "$(cat "$prompt")" --model sonnet --permission-mode default \
  --tools "Read,Glob,Grep,Edit,Write,Bash,Skill" \
  --allowedTools "Read,Glob,Grep,Edit,Write,Bash(node *),Bash(mkdir *),Bash(cat *),Bash(ls *)" \
  --output-format stream-json --verbose --no-session-persistence --setting-sources project --strict-mcp-config \
  --max-turns 40 --max-budget-usd 1 < /dev/null > "$dir/stream.jsonl" 2> "$dir/stderr.txt"
code=$?
echo "exit: $code" >> "$dir/meta.txt"; echo "finished: $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$dir/meta.txt"
(cd "$lab" && find . -type f -not -path './.claude/*' | sort | xargs sha256sum) > "$dir/after.sha256"
echo "$name $arm exit $code"
