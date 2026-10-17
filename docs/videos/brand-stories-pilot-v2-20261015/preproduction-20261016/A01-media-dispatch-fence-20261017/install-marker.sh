#!/usr/bin/env bash
# Exact, no-clobber marker installer. Dry-run by default. Never run --apply until the
# reviewed cutover runbook's production preflight and site-owner approval are complete.
set -Eeuo pipefail

job_id=b721a65d-8c8d-4ae8-834c-391cfc267a6f
volume=travel_scanner_video_work
expected_sha=6d6a64a88f066ce62d3ccf2145ab59e052dee0bf76e4da7b68385d93ea6827a5
source_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
source_file="$source_dir/manifest.json"
mode=dry-run
expected_mount=

while (($#)); do
  case "$1" in
    --apply) mode=apply; shift ;;
    --expected-mountpoint)
      (($# >= 2)) || { echo 'missing --expected-mountpoint value' >&2; exit 2; }
      expected_mount=$2; shift 2 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

[[ -n "$expected_mount" ]] || { echo 'pass the independently read Docker volume mountpoint' >&2; exit 2; }
[[ $(id -u) -eq 0 ]] || { echo 'run as root for the exact Docker volume' >&2; exit 2; }
[[ -f "$source_file" && ! -L "$source_file" ]] || { echo 'candidate is not a regular file' >&2; exit 3; }
[[ $(sha256sum -- "$source_file" | cut -d ' ' -f 1) == "$expected_sha" ]] || {
  echo 'candidate SHA-256 drift' >&2; exit 3;
}
[[ $(docker volume inspect --format '{{.Name}}' "$volume") == "$volume" ]] || {
  echo 'Docker volume identity drift' >&2; exit 3;
}
actual_mount=$(docker volume inspect --format '{{.Mountpoint}}' "$volume")
actual_real=$(realpath -e -- "$actual_mount")
expected_real=$(realpath -e -- "$expected_mount")
[[ "$actual_real" == "$expected_real" ]] || { echo 'Docker volume mountpoint drift' >&2; exit 3; }
[[ -d "$actual_real" && ! -L "$actual_real" ]] || { echo 'volume mountpoint is unsafe' >&2; exit 3; }

target_dir="$actual_real/.ops/media-dispatch-fences"
target="$target_dir/$job_id.json"
# This one-off installer refuses pre-existing parents, including a partial prior run.
# Reusing an existing .ops directory could loosen permissions on unrelated files.
for component in "$actual_real/.ops" "$target_dir"; do
  [[ ! -e "$component" && ! -L "$component" ]] || {
    echo 'marker parent already exists; inspect it without changing permissions' >&2; exit 3;
  }
done
[[ ! -e "$target" && ! -L "$target" ]] || { echo 'target already exists; refuse overwrite' >&2; exit 3; }
printf 'mode=%s\nvolume=%s\nmount=%s\ntarget=%s\nmanifest_sha256=%s\n' \
  "$mode" "$volume" "$actual_real" "$target" "$expected_sha"
[[ "$mode" == apply ]] || exit 0

# The cutover operator must already have proven old API exit and obtained an owner-approved,
# durable exact-job Redis hold. This installer cannot establish those external facts itself.
umask 022
# The API runs UID:GID 10001:10001 and mounts this volume read-only. Create only
# absent, traversable directories. Fsync each newly created directory entry before
# claiming the marker survives a host restart; never chmod a pre-existing .ops.
python3 - "$actual_real" <<'PY'
import os
import stat
import sys

root = os.open(sys.argv[1], os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY | os.O_NOFOLLOW)
try:
    if not stat.S_ISDIR(os.fstat(root).st_mode):
        raise SystemExit('volume root is not a directory')
    os.mkdir('.ops', mode=0o755, dir_fd=root)
    os.fsync(root)
    ops = os.open('.ops', os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=root)
    try:
        os.mkdir('media-dispatch-fences', mode=0o755, dir_fd=ops)
        os.fsync(ops)
        fences = os.open('media-dispatch-fences', os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=ops)
        try:
            if stat.S_IMODE(os.fstat(ops).st_mode) != 0o755 or stat.S_IMODE(os.fstat(fences).st_mode) != 0o755:
                raise SystemExit('new marker parents are not mode 0755')
            os.fsync(fences)
        finally:
            os.close(fences)
    finally:
        os.close(ops)
finally:
    os.close(root)
PY
parent_real=$(realpath -e -- "$target_dir")
[[ "$parent_real" == "$actual_real/.ops/media-dispatch-fences" ]] || {
  echo 'marker parent changed during install' >&2; exit 3;
}
temp=$(mktemp -- "$target_dir/.a01-fence.XXXXXXXX")
trap '[[ -z "${temp:-}" ]] || rm -f -- "$temp"' EXIT
install -m 0644 -- "$source_file" "$temp"
[[ $(sha256sum -- "$temp" | cut -d ' ' -f 1) == "$expected_sha" ]] || {
  echo 'temporary marker SHA-256 drift' >&2; exit 3;
}
python3 - "$temp" <<'PY'
import os
import sys

fd = os.open(sys.argv[1], os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
try:
    os.fsync(fd)
finally:
    os.close(fd)
PY
ln -- "$temp" "$target" # atomic, same-volume and no-clobber
rm -- "$temp"
temp=
python3 - "$target_dir" <<'PY'
import os
import sys

fd = os.open(sys.argv[1], os.O_RDONLY | os.O_CLOEXEC | os.O_DIRECTORY | os.O_NOFOLLOW)
try:
    os.fsync(fd)
finally:
    os.close(fd)
PY
python3 - "$target" "$expected_sha" <<'PY'
import hashlib
import os
import stat
import sys

path, expected = sys.argv[1:]
fd = os.open(path, os.O_RDONLY | os.O_CLOEXEC | os.O_NOFOLLOW)
try:
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or not 0 < info.st_size <= 4096:
        raise SystemExit('installed marker is not a bounded regular file')
    data = os.read(fd, 4097)
finally:
    os.close(fd)
if len(data) != info.st_size or hashlib.sha256(data).hexdigest() != expected:
    raise SystemExit('installed marker readback mismatch')
print('installed marker O_NOFOLLOW/regular-file/SHA-256 readback PASS')
PY
