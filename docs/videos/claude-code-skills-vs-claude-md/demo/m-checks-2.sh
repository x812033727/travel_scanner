#!/usr/bin/env bash
# The checks for the 2026-10-11 runs that call no model: versions, the seed's hashes and
# widths, a dry build of each new arm's project, that the five-procedure CLAUDE.md and the five
# skills carry the same text, `claude plugin validate` on the skill projects, and drift.mjs on
# two made-up sessions.
# No session is started.
#
#   WORK=<work> bash <seed>/m-checks-2.sh > <work>/run/logs/m-checks-2.log 2>&1
#
# Each command is printed as typed, then its output, then its exit code.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-skills-hands-on}"
export DRY="${DRY:-$work/run/dry-lab}"
user="$(basename "$HOME")"
cd "$seed" || exit 2

run() { echo "\$ $1"; eval "$1"; echo "[exit $?]"; echo; }
# claude plugin validate prints the folder it was given, in this machine's spelling.
mask() { sed -E -e 's#^(Validating [a-z]+( in)?:) .*dry-lab#\1 <lab>#' -e "s#$user#<user>#g" | grep -v '^$'; }
validate() {
  bash session-2.sh "dry-$1" "$1" ship --dry > /dev/null
  (cd "$DRY" && claude plugin validate .claude/skills 2>&1; echo "[validate exit $?]") | mask
}

echo "# $(date -u +%Y-%m-%dT%H:%M:%SZ) | every command below is run from <seed>"
echo
run 'claude --version'
run 'node --version'
run 'bash --version | head -1'
run 'find --version | head -1; sort --version | head -1; head --version | head -1; grep --version | head -1'
run "node measure-seed.mjs | grep -v ' results/'"
for arm in none claudemd skill claudemd5 skill5; do
  run "bash session-2.sh dry-$arm $arm ship --dry | sed -n '/^\\\$ find/,/^\\\$ sha256sum/p'"
done
run "bash session-2.sh dry-skill skill look --dry | sed -n '/^## above/,\$p'"
run 'node check-five.mjs'
run 'validate skill5'
run 'validate skill'

# drift.mjs on two made-up sessions: one that touched nothing, one that carried out the release.
scratch="$(mktemp -d)"
mkdir -p "$scratch/untouched.lab" "$scratch/released.lab/releases"
cp -r skill-lab/. "$scratch/untouched.lab/"
cp -r skill-lab/. "$scratch/released.lab/"
sed -i 's/"0.3.0"/"0.3.1"/' "$scratch/released.lab/package.json"
printf '# v0.3.1\n' > "$scratch/released.lab/releases/v0.3.1.md"
printf -- '- [fix] made up.\n' >> "$scratch/released.lab/CHANGELOG.md"
line() { printf '{"type":"assistant","message":{"id":"m%s","usage":{"input_tokens":2,"cache_creation_input_tokens":%s,"cache_read_input_tokens":0},"content":[]}}\n' "$1" "$2"; }
{ line 1 100; printf '{"type":"result","result":"made up.","num_turns":1,"total_cost_usd":0,"duration_ms":1000,"usage":{"input_tokens":2,"cache_creation_input_tokens":100,"cache_read_input_tokens":0,"output_tokens":3}}\n'; } > "$scratch/untouched.stream.jsonl"
{ line 1 100; line 2 200; printf '{"type":"result","result":"made up.\\n下一步：補一個測試","num_turns":2,"total_cost_usd":0,"duration_ms":2000,"usage":{"input_tokens":4,"cache_creation_input_tokens":300,"cache_read_input_tokens":0,"output_tokens":6}}\n'; } > "$scratch/released.stream.jsonl"
run "node drift.mjs \"$scratch/untouched.stream.jsonl\" \"$scratch/released.stream.jsonl\""
rm -rf "$scratch" "$DRY"
