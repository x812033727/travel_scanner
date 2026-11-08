#!/usr/bin/env bash
# tobranch.sh BRANCH SRC_DIR PREFIX MESSAGE
#
# Add every file under SRC_DIR to BRANCH at PREFIX/ as one new commit on top of the
# branch (fast-forward only, never a force push), then check every file against the
# pushed blobs. Files over 95 MB are split into 90 MiB PREFIX/<file>.partNN pieces
# with a PREFIX/<file>.SPLIT note (sha256 of the original and the restore command).
#
#   tobranch.sh transfer/curio-h24 ~/mokaair-work/videos/curio-h24 curio-h24 "curio-h24: final approved"
#
# PREFIX is relative to ~/mokaair-work/videos/ (see ../BACKUP-BRANCHES.md), never an
# absolute path. Commit trailers come from TOBRANCH_TRAILERS (e.g. the session's
# Co-Authored-By and Claude-Session lines); nothing session-specific is hardcoded.
# Runs from inside any checkout of the repository; the working tree is not touched.
# GitHub refuses a push over 2 GB, so new blobs are committed and pushed in batches of
# about TOBRANCH_BATCH_BYTES (default 1.5 GB); each batch is its own fast-forward commit.
set -euo pipefail
parts() { # $1 = commit, $2 = path of the split original: its .partNN pieces in order
  git ls-tree --name-only "$1" -- "$(dirname "$2")/" | awk -v p="$2.part" 'index($0, p) == 1 && substr($0, length(p) + 1) ~ /^[0-9]+$/' | sort
}
[ $# -eq 4 ] || { echo "usage: $0 BRANCH SRC_DIR PREFIX MESSAGE" >&2; exit 2; }
B=$1; SRC=${2%/}; PRE=${3%/}; MSG=$4
[ -d "$SRC" ] || { echo "no such directory: $SRC" >&2; exit 2; }
case "$PRE" in /*|..|../*|*/..|*/../*) echo "PREFIX must be relative: $PRE" >&2; exit 2;; esac
[ "$PRE" = "." ] && PRE=""
J=${PRE:+$PRE/}  # PREFIX "." puts the files at the root of the branch
LIMIT=$((95 * 1000 * 1000))
cd "$(git rev-parse --show-toplevel)"
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
# New objects go to a temporary object directory (the repo's own is an alternate), so a backup
# never leaves a second copy of an episode in .git: a container's disk allowance ran out on
# 2026-11-08 after a few episode pushes. Nothing here moves a ref or writes FETCH_HEAD.
REPO_OBJECTS=$(cd "$(git rev-parse --git-common-dir)" && pwd)/objects
export GIT_OBJECT_DIRECTORY=$WORK/objects GIT_ALTERNATE_OBJECT_DIRECTORIES=$REPO_OBJECTS
mkdir -p "$GIT_OBJECT_DIRECTORY"
remote_head() { git ls-remote origin "refs/heads/$B" | cut -f1; }
P=$(remote_head)
if [ -n "$P" ]; then git fetch -q --refmap= --no-write-fetch-head origin "refs/heads/$B"; fi
export GIT_INDEX_FILE=$WORK/index
if [ -n "$P" ]; then git read-tree "$P"; fi
BATCH=${TOBRANCH_BATCH_BYTES:-1500000000}
START=$P
n=0; pending=0; batch=0
flush() { # commit and push what is in the index so far
  local T C
  T=$(git write-tree)
  if [ -n "$P" ] && [ "$(git rev-parse "$P^{tree}")" = "$T" ]; then return 0; fi
  batch=$((batch + 1))
  C=$(printf '%s%s\n%s' "$MSG" "$([ "$batch" -gt 1 ] && echo " (batch $batch)")" "${TOBRANCH_TRAILERS:+
$TOBRANCH_TRAILERS
}" | git commit-tree "$T" ${P:+-p "$P"})
  git push -q origin "$C:refs/heads/$B"
  # push also sets refs/remotes/origin/$B, which would point into the temporary objects
  git update-ref -d "refs/remotes/origin/$B" 2>/dev/null || true
  P=$C; pending=0
}
while IFS= read -r -d '' f; do
  rel=${f#"$SRC"/}
  size=$(stat -c %s "$f")
  if [ "$pending" -gt 0 ] && [ $((pending + size)) -gt "$BATCH" ]; then flush; fi
  pending=$((pending + size))
  if [ "$size" -gt "$LIMIT" ]; then
    git rm -q --cached --ignore-unmatch "$J$rel" >/dev/null
    git ls-files -z -- "$J$rel.part*" | xargs -0 -r git rm -q --cached >/dev/null
    rm -f "$WORK"/part*; split -b 90M -d -a 2 "$f" "$WORK/part"
    for p in "$WORK"/part*; do
      h=$(git hash-object -w "$p")
      git update-index --add --cacheinfo "100644,$h,$J$rel.${p##*/}"; n=$((n + 1))
    done
    name=$(basename "$rel")
    printf 'sha256 %s\nsize %s\nrestore: cat "%s".part* > "%s"\n' \
      "$(sha256sum "$f" | cut -d' ' -f1)" "$(stat -c %s "$f")" "$name" "$name" > "$WORK/note"
    h=$(git hash-object -w "$WORK/note"); git update-index --add --cacheinfo "100644,$h,$J$rel.SPLIT"
  else
    h=$(git hash-object -w "$f"); git update-index --add --cacheinfo "100644,$h,$J$rel"; n=$((n + 1))
  fi
done < <(find "$SRC" -type f ! -name 'LEASE*' -print0)
flush
unset GIT_INDEX_FILE
if [ "$P" = "$START" ]; then echo "nothing new for $B"; exit 0; fi
C=$P
[ "$(remote_head)" = "$C" ] || { echo "PUSH MISMATCH on $B" >&2; exit 1; }
echo "pushed $B $C ($n blobs from $SRC, $batch commit(s))"
# Verify every file against the pushed commit; split files by reassembling the parts.
bad=0
while IFS= read -r -d '' f; do
  rel=${f#"$SRC"/}
  if [ "$(stat -c %s "$f")" -gt "$LIMIT" ]; then
    want=$(sha256sum "$f" | cut -d' ' -f1)
    note=$(git cat-file -p "$C:$J$rel.SPLIT" 2>/dev/null | sed -n 's/^sha256 //p')
    got=$(parts "$C" "$J$rel" | while read -r p; do git cat-file -p "$C:$p"; done | sha256sum | cut -d' ' -f1)
    [ "$want" = "$note" ] && [ "$want" = "$got" ] || { echo "MISMATCH $rel (split)"; bad=$((bad + 1)); }
  else
    [ "$(git rev-parse -q --verify "$C:$J$rel" 2>/dev/null)" = "$(git hash-object "$f")" ] || { echo "MISMATCH $rel"; bad=$((bad + 1)); }
  fi
done < <(find "$SRC" -type f ! -name 'LEASE*' -print0)
echo "verify mismatches: $bad"
[ "$bad" -eq 0 ]
