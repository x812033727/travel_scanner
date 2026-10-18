env CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 timeout 300 \
  claude -p --model sonnet \
  --setting-sources project,local --strict-mcp-config \
  --tools "Read,Glob,Grep,Edit,Write,Skill" \
  --allowedTools "Read,Glob,Grep,Edit,Write,Skill" \
  --no-session-persistence \
  --output-format stream-json --verbose \
  --debug-file ../debug.log \
  < ../ship.txt > ../stream.jsonl 2> ../stderr.txt
