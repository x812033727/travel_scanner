#!/usr/bin/env bash
# Classify an inbox with Claude Code: no screen, no tools.
inbox=${1:-inbox.txt}
out=runs/$(date +%Y%m%d-%H%M%S).json
mkdir -p runs
cat "$inbox" | claude -p "$(cat prompt.txt)" \
  --model haiku --tools "" --max-turns 4 \
  --output-format json --json-schema "$(cat schema.json)" \
  > "$out" 2> "$out.err"
node check.mjs "$out" $? "$inbox"
