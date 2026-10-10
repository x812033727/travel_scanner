#!/usr/bin/env bash
# claude plugin validate on the good plugin and on every broken variant kit.sh can build.
# It starts no session and calls no model; validate reads only the folder it is given.
#
#   WORK=<work> bash <seed>/validate-all.sh
#
# Each variant is built in <dry>/v/<variant>; the folder's path is shown as <v>/<variant>.
set -u
seed="$(cd "$(dirname "$0")" && pwd)"
work="${WORK:-${TMPDIR:-/tmp}/claude-code-plugins-hands-on}"
DRY="${DRY:-$work/run/dry}"
base="$DRY/v"
native="$(cygpath -m "$base" 2>/dev/null || printf '%s' "$base")"
back="${native//\//\\}"
hide() { sed -e "s#$(printf '%s' "$back" | sed -e 's/[\\.*^$#[]/\\&/g')#<v>#g" -e "s#$native#<v>#g" -e "s#$base#<v>#g" -e 's#<v>[\\/]#<v>/#g' -e 's#\\#/#g'; }

check() {
  local variant="$1"; shift
  bash "$seed/kit.sh" "$variant" "$base/$variant" || return
  echo "\$ claude plugin validate <v>/$variant $*"
  claude plugin validate "$native/$variant" "$@" 2>&1 | hide | cut -c1-240
  echo "[validate exit ${PIPESTATUS[0]}]"
  echo
}

for variant in good stale badjson noname hookpath minimal typo nowrap noscript badagent inside nomanifest; do
  check "$variant"
done
check good --strict
check minimal --strict
rm -rf "$base"
