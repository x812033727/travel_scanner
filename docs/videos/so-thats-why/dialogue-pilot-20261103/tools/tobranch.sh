#!/bin/bash
# tobranch.sh BRANCH SRC_DIR PREFIX MESSAGE : add every file under SRC_DIR to BRANCH at PREFIX/, splitting files over 90 MB into .partNN with a .SPLIT note; verifies every blob.
set -e
B=$1; SRC=$2; PRE=$3; MSG=$4
cd /home/user/travel_scanner
S=${TMPDIR:-/tmp}
git fetch -q origin $B 2>/dev/null && P=$(git rev-parse FETCH_HEAD) || P=
export GIT_INDEX_FILE=$S/tb.$$.index; rm -f $GIT_INDEX_FILE
[ -n "$P" ] && git read-tree $P
TMP=$S/tb.$$.split; mkdir -p $TMP; n=0
while IFS= read -r -d '' f; do
  rel=${f#$SRC/}
  if [ $(stat -c %s "$f") -gt 94371840 ]; then
    rm -f $TMP/part*; split -b 90M -d -a 2 "$f" $TMP/part
    for p in $TMP/part*; do h=$(git hash-object -w $p); git update-index --add --cacheinfo 100644,$h,"$PRE/$rel.${p##*/}"; n=$((n+1)); done
    printf 'sha256 %s\nrestore: cat "%s".part* > "%s"\n' "$(sha256sum "$f"|cut -d' ' -f1)" "$(basename "$rel")" "$(basename "$rel")" > $TMP/note
    h=$(git hash-object -w $TMP/note); git update-index --add --cacheinfo 100644,$h,"$PRE/$rel.SPLIT"
  else
    h=$(git hash-object -w "$f"); git update-index --add --cacheinfo 100644,$h,"$PRE/$rel"; n=$((n+1))
  fi
done < <(find "$SRC" -type f -print0)
T=$(git write-tree)
C=$(printf '%s\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_019ZmEpYzTwJafrPaLRYukag\n' "$MSG" | git commit-tree $T ${P:+-p $P})
unset GIT_INDEX_FILE; rm -rf $TMP $S/tb.$$.index
git push -q origin $C:refs/heads/$B 2>&1 | grep -v '^remote:' || true
git fetch -q origin $B; [ "$(git rev-parse FETCH_HEAD)" = "$C" ] && echo "pushed $B $C ($n blobs from $SRC)" || { echo "PUSH MISMATCH"; exit 1; }
# verify: every non-split file's blob is in the tree
bad=0; while IFS= read -r -d '' f; do rel=${f#$SRC/}; [ $(stat -c %s "$f") -gt 94371840 ] && continue; [ "$(git rev-parse "$C:$PRE/$rel" 2>/dev/null)" = "$(git hash-object "$f")" ] || bad=$((bad+1)); done < <(find "$SRC" -type f -print0)
echo "verify mismatches: $bad"
