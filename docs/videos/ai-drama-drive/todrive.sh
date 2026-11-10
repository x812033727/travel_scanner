#!/usr/bin/env bash
# todrive.sh [--check] SRC_DIR DEST
#
# Copy every file under SRC_DIR into DEST on the owner's Google Drive, then check every one
# (docs/videos/AI-DRAMA-DRIVE.md). DEST is an rclone path or a mounted Drive folder, and must be
# under AI劇/:
#
#   todrive.sh ~/mokaair-work/videos/_live-e901 "aidrama:AI劇/種田娶妻打天下（真人版）/第001集/製作檔/_live-e901"
#   todrive.sh /content/work/tn-e005 "/content/drive/MyDrive/AI/備份/AI劇/恁祖媽今年18/第005集/製作檔/tn-e005"
#
# Nothing in Drive is ever deleted: `rclone copy`, never sync. A file DEST already has with other
# content is moved to DEST/_舊版/<UTC time>/ before the new one takes its place. Links are kept as
# .rclonelink files, not followed. Files of any size go whole (Drive takes up to 5 TB a file), so
# nothing is split. The check compares every file of SRC_DIR with DEST by hash (Drive's md5; a
# mounted folder is read back) and prints "todrive: N files, M differences"; the exit code is 0
# only when M is 0.
#
# --check copies nothing: the coverage check, run by an agent that did not make the episode, over
# the same SRC_DIR and DEST. Every file of SRC_DIR has to be in DEST with the same hash.
#
# The rclone config comes from TODRIVE_RCLONE_CONFIG (or rclone's own default). It is a token the
# owner made for backups; it never goes into the repository or a chat.
set -euo pipefail
CHECK_ONLY=0
if [ "${1:-}" = "--check" ]; then CHECK_ONLY=1; shift; fi
[ $# -eq 2 ] || { echo "usage: $0 [--check] SRC_DIR DEST" >&2; exit 2; }
SRC=${1%/}; DEST=${2%/}
[ -d "$SRC" ] || { echo "no such directory: $SRC" >&2; exit 2; }
command -v rclone >/dev/null || { echo "rclone is not installed (https://rclone.org/install/)" >&2; exit 2; }
case "$DEST" in
  *AI劇/*) ;;
  *) echo "DEST must be under AI劇/ (docs/videos/AI-DRAMA-DRIVE.md): $DEST" >&2; exit 2 ;;
esac
case "$DEST" in *..*) echo "DEST must not contain ..: $DEST" >&2; exit 2 ;; esac
if [ -n "${TODRIVE_RCLONE_CONFIG:-}" ]; then export RCLONE_CONFIG=$TODRIVE_RCLONE_CONFIG; fi
OLD=_舊版
FILTERS=(--exclude "/$OLD/**")
COMMON=(--links --tpslimit 5 --retries 5)
files=$(find "$SRC" \( -type f -o -type l \) -not -path "$SRC/$OLD/*" | wc -l)
if [ "$CHECK_ONLY" -eq 0 ]; then
  TS=$(date -u +%Y%m%dT%H%M%SZ)
  rclone copy "$SRC" "$DEST" --checksum --drive-chunk-size 64M "${COMMON[@]}" \
    --backup-dir "$DEST/$OLD/$TS" "${FILTERS[@]}"
fi
out=$(mktemp); trap 'rm -f "$out"' EXIT
set +e
rclone check "$SRC" "$DEST" --one-way "${COMMON[@]}" "${FILTERS[@]}" >"$out" 2>&1
code=$?
set -e
diffs=$(grep -oE '[0-9]+ differences found' "$out" | grep -oE '^[0-9]+' | tail -1)
[ -n "$diffs" ] || diffs=$([ "$code" -eq 0 ] && echo 0 || echo "?")
grep -E 'ERROR' "$out" | head -20 >&2 || true
echo "todrive: $files files, $diffs differences ($SRC -> $DEST)"
[ "$code" -eq 0 ] && [ "$diffs" = "0" ]
