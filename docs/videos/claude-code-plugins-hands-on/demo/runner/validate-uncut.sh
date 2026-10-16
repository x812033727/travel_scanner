#!/usr/bin/env bash
# runner: claude plugin validate on seed-built variants, without validate-all.sh's cut at 240
# columns (one of its messages is longer). Builds each with the seed's kit.sh in <dry>/v, hides
# the folder as <v>, removes it afterwards. No session, no model.
#   bash validate-uncut.sh <variant> [<variant> ...]
set -u
here="$(cd "$(dirname "$0")" && pwd)"
W="$(cd "$here/../.." && pwd)"
seed="$W/_tools/seed"
base="$W/run/dry/v"
native="$(cygpath -m "$base")"
back="${native//\//\\}"
hide() { sed -e "s#$(printf '%s' "$back" | sed -e 's/[\\.*^$#[]/\\&/g')#<v>#g" -e "s#$native#<v>#g" -e "s#$base#<v>#g" -e 's#<v>[\\/]#<v>/#g' -e 's#\\#/#g'; }
for variant in "$@"; do
  bash "$seed/kit.sh" "$variant" "$base/$variant" || exit $?
  echo "\$ claude plugin validate <v>/$variant"
  text="$(claude plugin validate "$native/$variant" 2>&1; echo "[validate exit $?]")"
  printf '%s\n' "$text" | hide
  echo "longest line: $(printf '%s\n' "$text" | hide | awk '{ if (length($0) > m) m = length($0) } END { print m }') characters"
  echo
done
rm -rf "$base"
rmdir "$W/run/dry" 2>/dev/null
exit 0
