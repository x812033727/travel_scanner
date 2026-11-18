#!/usr/bin/env bash
# todrive.sh [--check] SRC_DIR DEST
#
# Copy the files under SRC_DIR into DEST on the owner's Google Drive, check every one, and leave a
# manifest of all of them (docs/videos/AI-DRAMA-DRIVE.md). DEST is an rclone path or a mounted
# Drive folder, and must be under AI劇/:
#
#   todrive.sh ~/mokaair-work/videos/_live-e901 "aidrama:AI劇/種田娶妻打天下（真人版）/第001集/製作檔/_live-e901"
#   todrive.sh /content/work/tn-e005 "/content/drive/MyDrive/AI/備份/AI劇/恁祖媽今年18/第005集/製作檔/tn-e005"
#   todrive.sh ./flow-music "videobackup:AI劇/_共用素材/music/flow-music-20261117"
#
# The owner's rule is "everything" (2026-11-10). What is not uploaded, all of it in the manifest:
#   - a file the host worker has already put in this episode's folder with the same bytes
#     (owner, 2026-11-18): when DEST is under <episode>/製作檔/, the episode's backup.json and a
#     listing of the folder are read, and a file whose sha256 and size the worker recorded, at a
#     path the folder still holds with the same size and md5, is marked "worker" with that path;
#   - secrets (.env, rclone.conf, key files, credentials*.json) and reinstallable packages
#     (node_modules, .venv), marked "excluded" with the reason.
# todrive-plan.mjs (beside this file) makes the plan; the reasons are there.
#
# Nothing in Drive is ever deleted: `rclone copy`, never sync. A file DEST already has with other
# content is moved to DEST/_舊版/<UTC time>/ before the new one takes its place. Links are kept as
# .rclonelink files, not followed. Files of any size go whole (Drive takes up to 5 TB a file). The
# check compares every uploaded file with DEST by hash and prints "todrive: N files, M differences";
# the exit code is 0 only when M is 0. Only then are manifest.json and SHA256SUMS written to
# DEST/_todrive/<UTC time>/, and the manifest to DEST/_todrive/latest.json.
#
# --check copies nothing: the coverage check, run by an agent that did not make the episode, over
# the same SRC_DIR and DEST. Every file of SRC_DIR has to be in DEST with the same hash, or in the
# worker's copy as it is in the folder now; a worker copy that changed or went is a difference.
#
# The remote comes from rclone's environment: a cloud session has RCLONE_CONFIG_VIDEOBACKUP_* set by
# the owner (docs/videos/AI-DRAMA-DRIVE.md §session 用的權杖). TODRIVE_RCLONE_CONFIG may name a config
# file instead. The token never goes into the repository or a chat.
set -euo pipefail
CHECK_ONLY=0
if [ "${1:-}" = "--check" ]; then CHECK_ONLY=1; shift; fi
[ $# -eq 2 ] || { echo "usage: $0 [--check] SRC_DIR DEST" >&2; exit 2; }
SRC=${1%/}; DEST=${2%/}
[ -d "$SRC" ] || { echo "no such directory: $SRC" >&2; exit 2; }
command -v rclone >/dev/null || { echo "rclone is not installed (https://rclone.org/install/)" >&2; exit 2; }
command -v node >/dev/null || { echo "node is not installed; todrive-plan.mjs needs it" >&2; exit 2; }
case "$DEST" in
  *AI劇/*) ;;
  *) echo "DEST must be under AI劇/ (docs/videos/AI-DRAMA-DRIVE.md): $DEST" >&2; exit 2 ;;
esac
case "$DEST" in *..*) echo "DEST must not contain ..: $DEST" >&2; exit 2 ;; esac
if [ -n "${TODRIVE_RCLONE_CONFIG:-}" ]; then export RCLONE_CONFIG=$TODRIVE_RCLONE_CONFIG; fi
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
OLD=_舊版
RECORDS=_todrive
COMMON=(--links --tpslimit 5 --retries 5)
WORK=$(mktemp -d); trap 'rm -rf "$WORK"' EXIT
TS=$(date -u +%Y%m%dT%H%M%SZ)

# The episode's worker copy, when DEST is one of its 製作檔 folders. Either read may fail (no backup
# yet, a _共用 folder): then nothing is compared and every file is uploaded.
PLAN_ARGS=(--source "$(basename "$SRC")")
case "$DEST" in
  */製作檔/*|*/製作檔)
    EPISODE=${DEST%%/製作檔*}
    if rclone copyto "$EPISODE/backup.json" "$WORK/backup.json" >/dev/null 2>&1 \
      && rclone lsjson -R --hash --files-only "$EPISODE" --exclude "/製作檔/**" --exclude "/$OLD/**" >"$WORK/listing.json" 2>/dev/null; then
      PLAN_ARGS+=(--worker "$WORK/backup.json" --listing "$WORK/listing.json")
    fi
    ;;
esac
counts=$(node "$HERE/todrive-plan.mjs" "$SRC" "$WORK/plan" "${PLAN_ARGS[@]}")
count() { printf '%s' "$counts" | node -e 'let s="";process.stdin.on("data",(d)=>s+=d).on("end",()=>console.log(JSON.parse(s)[process.argv[1]]))' "$1"; }
files=$(count files); uploads=$(count upload); held=$(count worker); excluded=$(count excluded)

if [ "$CHECK_ONLY" -eq 0 ]; then
  rclone copy "$SRC" "$DEST" --files-from "$WORK/plan/upload.txt" --checksum --drive-chunk-size 64M "${COMMON[@]}" \
    --backup-dir "$DEST/$OLD/$TS"
fi
out="$WORK/check.log"
set +e
rclone check "$SRC" "$DEST" --one-way --files-from "$WORK/plan/upload.txt" "${COMMON[@]}" >"$out" 2>&1
code=$?
set -e
diffs=$(grep -oE '[0-9]+ differences found' "$out" | grep -oE '^[0-9]+' | tail -1 || true)
[ -n "$diffs" ] || diffs=$([ "$code" -eq 0 ] && echo 0 || echo "?")
grep -E 'ERROR' "$out" | head -20 >&2 || true
echo "todrive: $files files, $diffs differences ($SRC -> $DEST)"
echo "todrive: $uploads uploaded, $held already in the host backup, $excluded excluded"
[ "$code" -eq 0 ] && [ "$diffs" = "0" ] || exit 1
if [ "$CHECK_ONLY" -eq 0 ]; then
  rclone copyto "$WORK/plan/manifest.json" "$DEST/$RECORDS/$TS/manifest.json" "${COMMON[@]}"
  rclone copyto "$WORK/plan/SHA256SUMS" "$DEST/$RECORDS/$TS/SHA256SUMS" "${COMMON[@]}"
  rclone copyto "$WORK/plan/manifest.json" "$DEST/$RECORDS/latest.json" "${COMMON[@]}"
  echo "todrive: manifest in $DEST/$RECORDS/$TS/"
fi
