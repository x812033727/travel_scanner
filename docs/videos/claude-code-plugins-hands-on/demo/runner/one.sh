#!/usr/bin/env bash
# runner: one session, then the after-session checks. Never --dry, never --force.
#   bash one.sh <name> <arm>
set -u
here="$(cd "$(dirname "$0")" && pwd)"
W="$(cd "$here/../.." && pwd)"
seed="$W/_tools/seed"
logs="$W/run/logs"
name="$1"; arm="$2"
mkdir -p "$here/out"
if [ -e "$here/out/$name.printed.txt" ]; then echo "refused by one.sh: $name was already started once"; exit 3; fi
WORK="$W" bash "$seed/session.sh" "$name" "$arm" > "$here/out/$name.printed.txt" 2> "$here/out/$name.printed.err.txt"
code=$?
echo "[session.sh exit $code] printed $(wc -l < "$here/out/$name.printed.txt") lines, stderr $(wc -c < "$here/out/$name.printed.err.txt") bytes"
[ -s "$here/out/$name.printed.err.txt" ] && head -5 "$here/out/$name.printed.err.txt"
[ -f "$logs/$name.stream.jsonl" ] || exit 1
node "$seed/runner/models.mjs" "$logs/$name.stream.jsonl"
echo "[models.mjs exit $?]"
node "$here/scan.mjs" "$name"
echo "[scan.mjs exit $?]"
