#!/usr/bin/env python3
"""Safely stage the exact reviewed r4 archive on the host, without models.

--check reads only. --stage writes a new `payload/` under the pinned release
directory. Run only after this package and the host write were approved.
"""

from __future__ import annotations

import hashlib
import os
import stat
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath


RELEASE = Path("/root/mokaair-a01-round12-20261017-fe35369c")
ARCHIVE = RELEASE / "round12-r4-full-payload.tar.gz"
DEST = RELEASE / "payload"
EXPECTED_SHA = "ae7483b2867bd0dd479fe6177c7261be2e7abb47d6fe53c3c21bb89943833792"
MAX_FILES = 1200
MAX_BYTES = 400 * 1024 * 1024
EXPECTED_MEMBERS = 1351
EXPECTED_FILES = 979
EXPECTED_DIRS = 372


def regular(path: Path) -> None:
    if not stat.S_ISREG(path.lstat().st_mode):
        raise RuntimeError(f"not a regular file: {path}")


def inspect() -> list[tarfile.TarInfo]:
    if not stat.S_ISDIR(RELEASE.lstat().st_mode):
        raise RuntimeError("release path is not a real directory")
    regular(ARCHIVE)
    if hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() != EXPECTED_SHA:
        raise RuntimeError("r4 archive SHA mismatch")
    with tarfile.open(ARCHIVE, mode="r:gz") as archive:
        members = archive.getmembers()
    if len(members) != EXPECTED_MEMBERS:
        raise RuntimeError("archive member count drift; expected 979 files and 372 directories")
    names: set[str] = set()
    files = 0
    size = 0
    for member in members:
        path = PurePosixPath(member.name)
        if (path.is_absolute() or ".." in path.parts or not path.parts or
                path.parts[0] != "payload" or member.name in names):
            raise RuntimeError(f"unsafe or duplicate archive path: {member.name}")
        names.add(member.name)
        if member.isfile():
            files += 1
            size += member.size
        elif not member.isdir():
            raise RuntimeError(f"link or special archive member: {member.name}")
        if files > MAX_FILES or size > MAX_BYTES:
            raise RuntimeError("payload exceeds bounded file or byte count")
    if files != EXPECTED_FILES:
        raise RuntimeError("archive regular-file count drift")
    if len(members) - files != EXPECTED_DIRS or "payload" not in names:
        raise RuntimeError("archive directory count or root drift")
    return members


def stage(members: list[tarfile.TarInfo]) -> None:
    try:
        DEST.lstat()
    except FileNotFoundError:
        pass
    else:
        raise RuntimeError("host payload destination already exists; inspect it")
    temporary = Path(tempfile.mkdtemp(prefix=".a01-round12-payload-", dir=RELEASE))
    # Failure deliberately leaves only a release-local temporary directory for
    # inspection; the runner requires the final destination and exact hashes.
    with tarfile.open(ARCHIVE, mode="r:gz") as archive:
        for member in members:
            relative = PurePosixPath(member.name)
            target = temporary.joinpath(*relative.parts)
            if member.isdir():
                target.mkdir(mode=0o755, parents=True, exist_ok=True)
                os.chmod(target, 0o755)
                continue
            target.parent.mkdir(mode=0o755, parents=True, exist_ok=True)
            source = archive.extractfile(member)
            if source is None:
                raise RuntimeError(f"archive regular file unreadable: {member.name}")
            fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
            try:
                with os.fdopen(fd, "wb", closefd=False) as output:
                    while chunk := source.read(1024 * 1024):
                        output.write(chunk)
                    output.flush()
                os.fchmod(fd, 0o644)
                os.fsync(fd)
            finally:
                os.close(fd)
    os.rename(temporary / "payload", DEST)
    temporary.rmdir()
    fd = os.open(RELEASE, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)
    print(f"A01_HOST_PAYLOAD_STAGED {DEST} sha256={EXPECTED_SHA} files={EXPECTED_FILES}")


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in ("--check", "--stage"):
        print("usage: a01_stage_payload.py --check|--stage", file=sys.stderr)
        return 2
    try:
        members = inspect()
        if sys.argv[1] == "--check":
            print(f"A01_HOST_PAYLOAD_ARCHIVE_CHECKED sha256={EXPECTED_SHA} files={EXPECTED_FILES}")
        else:
            stage(members)
        return 0
    except (OSError, RuntimeError, tarfile.TarError) as error:
        print(f"A01 HOST PAYLOAD STAGE FAILED: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
