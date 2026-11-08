#!/usr/bin/env bash
# coverage.sh REF SRC_DIR PREFIX
#
# Coverage check for ../BACKUP-BRANCHES.md: every file under SRC_DIR must exist on REF
# at PREFIX/, either as itself (same blob) or as a .SPLIT note whose sha256 matches the
# reassembled .partNN pieces. Reads only git objects, so the agent that did not make the
# episode can run it against the pushed branch:
#
#   git fetch origin transfer/curio-h24
#   coverage.sh FETCH_HEAD ~/mokaair-work/videos/curio-h24 curio-h24
#
# Prints MISSING / MISMATCH lines and the two counts; exits non-zero unless both are 0.
# Without SRC_DIR (pass "-") it only checks the branch itself: every .SPLIT note matches
# its parts. That is the check to run when the work folder is already gone.
set -euo pipefail
parts() { # $1 = commit, $2 = path of the split original: its .partNN pieces in order
  git ls-tree --name-only "$1" -- "$(dirname "$2")/" | awk -v p="$2.part" 'index($0, p) == 1 && substr($0, length(p) + 1) ~ /^[0-9]+$/' | sort
}
[ $# -eq 3 ] || { echo "usage: $0 REF SRC_DIR|- PREFIX" >&2; exit 2; }
REF=$1; SRC=${2%/}; PRE=${3%/}
C=$(git rev-parse --verify "$REF^{commit}")
missing=0; bad=0
split_ok() { # $1 = path of the original file inside the tree
  local note got
  note=$(git cat-file -p "$C:$1.SPLIT" 2>/dev/null | sed -n 's/^sha256 //p') || return 1
  got=$(parts "$C" "$1" | while read -r p; do git cat-file -p "$C:$p"; done | sha256sum | cut -d' ' -f1)
  [ -n "$note" ] && [ "$note" = "$got" ] && { [ -z "${2:-}" ] || [ "$2" = "$note" ]; }
}
if [ "$SRC" = "-" ]; then
  while read -r s; do
    split_ok "${s%.SPLIT}" || { echo "MISMATCH ${s#"$PRE"/} (split)"; bad=$((bad + 1)); }
  done < <(git ls-tree -r --name-only "$C" -- "$PRE" | grep '\.SPLIT$' || true)
  echo "split notes checked; mismatches: $bad"
  [ "$bad" -eq 0 ]; exit
fi
[ -d "$SRC" ] || { echo "no such directory: $SRC" >&2; exit 2; }
declare -A tree
while IFS= read -r p; do tree[$p]=1; done < <(git ls-tree -r --name-only "$C" -- "$PRE")
while IFS= read -r -d '' f; do
  rel=${f#"$SRC"/}; path=$PRE/$rel
  if [ -n "${tree[$path]:-}" ]; then
    [ "$(git rev-parse "$C:$path")" = "$(git hash-object "$f")" ] || { echo "MISMATCH $rel"; bad=$((bad + 1)); }
  elif [ -n "${tree[$path.SPLIT]:-}" ]; then
    split_ok "$path" "$(sha256sum "$f" | cut -d' ' -f1)" || { echo "MISMATCH $rel (split)"; bad=$((bad + 1)); }
  else
    echo "MISSING $rel"; missing=$((missing + 1))
  fi
done < <(find "$SRC" -type f -print0)
echo "missing: $missing  mismatches: $bad"
[ "$missing" -eq 0 ] && [ "$bad" -eq 0 ]
