#!/usr/bin/env python3
"""Host-only A01 project STOP fence; candidate, not installed.

The marker is armed before STOP is lifted. On any interrupted review, `restore`
relinks the original STOP inode, or creates a conservative replacement if the
held link was lost. No provider, database, Docker or repository call is made.
"""

from __future__ import annotations

import json
import os
import stat
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


SLUG = "story-rolling-suitcase-v2"


@dataclass(frozen=True)
class Paths:
    workdir: Path = Path(
        "/var/lib/docker/volumes/travel_scanner_video_work/_data/"
        "story-rolling-suitcase-v2"
    )
    release_dir: Path = Path("/root/mokaair-a01-round12-20261017-fe35369c")

    @property
    def stop(self) -> Path:
        return self.workdir / "STOP"

    @property
    def held(self) -> Path:
        return self.workdir / "STOP.a01-round12-held"

    @property
    def marker(self) -> Path:
        return self.release_dir / "a01-stop-recovery-armed.json"


def _lstat(path: Path) -> os.stat_result | None:
    try:
        return path.lstat()
    except FileNotFoundError:
        return None


def _directory(path: Path) -> None:
    info = _lstat(path)
    if info is None or not stat.S_ISDIR(info.st_mode):
        raise RuntimeError(f"expected a real directory: {path}")


def _regular(path: Path, *, required: bool) -> os.stat_result | None:
    info = _lstat(path)
    if info is None:
        if required:
            raise RuntimeError(f"required file missing: {path}")
        return None
    if not stat.S_ISREG(info.st_mode):
        raise RuntimeError(f"expected a regular file, not a symlink or device: {path}")
    return info


def _sync_dir(path: Path) -> None:
    if os.name == "nt":  # The real host is Linux; portable tests exercise the state transitions.
        return
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _write_exclusive(path: Path, data: bytes) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        with os.fdopen(fd, "wb", closefd=False) as output:
            output.write(data)
            output.flush()
        os.fsync(fd)
    finally:
        os.close(fd)
    _sync_dir(path.parent)


def arm(paths: Paths = Paths()) -> str:
    """Persist marker and original STOP hard link, while STOP still protects A01."""
    _directory(paths.workdir)
    _directory(paths.release_dir)
    _regular(paths.stop, required=True)
    if _regular(paths.marker, required=False) is not None:
        raise RuntimeError("A01 guard is already armed; recover it before a new run")
    if _regular(paths.held, required=False) is not None:
        raise RuntimeError("A01 held STOP already exists; inspect the prior run")
    record = {
        "slug": SLUG,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "stop": str(paths.stop),
        "held": str(paths.held),
    }
    _write_exclusive(paths.marker, (json.dumps(record, sort_keys=True) + "\n").encode())
    os.link(paths.stop, paths.held, follow_symlinks=False)
    _sync_dir(paths.workdir)
    return "armed; original STOP remains present"


def lift(paths: Paths = Paths()) -> str:
    """Only a supervised review runner calls this after all other guards are live."""
    _regular(paths.marker, required=True)
    before = _regular(paths.stop, required=True)
    held = _regular(paths.held, required=True)
    if before is None or held is None or (before.st_dev, before.st_ino) != (held.st_dev, held.st_ino):
        raise RuntimeError("STOP changed after arming; do not lift it")
    os.unlink(paths.stop)
    _sync_dir(paths.workdir)
    return "A01 STOP temporarily lifted; marker and original inode retained"


def restore(paths: Paths = Paths()) -> str:
    """Idempotent ExecStopPost or manual recovery; STOP must remain protected."""
    marker = _regular(paths.marker, required=False)
    _directory(paths.workdir)
    if _regular(paths.stop, required=False) is not None:
        return "A01 STOP already present"
    if _regular(paths.held, required=False) is not None:
        try:
            os.link(paths.held, paths.stop, follow_symlinks=False)
        except FileExistsError:
            _regular(paths.stop, required=True)
        _sync_dir(paths.workdir)
        return "A01 original STOP restored"
    if marker is None:
        raise RuntimeError("A01 STOP and held link absent; manual recovery required")
    try:
        _write_exclusive(
            paths.stop,
            b"A01 manual review interrupted; hold until receipt and job reconciliation.\n",
        )
    except FileExistsError:
        _regular(paths.stop, required=True)
    return "A01 conservative STOP restored; original held link missing"


def finish(paths: Paths = Paths()) -> str:
    """Only after STOP is read back and both Docker restart policies are restored."""
    _regular(paths.marker, required=True)
    _regular(paths.stop, required=True)
    os.unlink(paths.marker)
    _sync_dir(paths.release_dir)
    if _regular(paths.held, required=False) is not None:
        os.unlink(paths.held)
        _sync_dir(paths.workdir)
    return "guard disarmed; A01 STOP remains present"


def status(paths: Paths = Paths()) -> str:
    return json.dumps(
        {
            "slug": SLUG,
            "armed": _regular(paths.marker, required=False) is not None,
            "stop": _regular(paths.stop, required=False) is not None,
            "held": _regular(paths.held, required=False) is not None,
        },
        sort_keys=True,
    )


def main(argv: list[str]) -> int:
    commands = {"arm": arm, "lift": lift, "restore": restore, "finish": finish, "status": status}
    if len(argv) != 1 or argv[0] not in commands:
        print("usage: a01_stop_guard.py arm|lift|restore|finish|status", file=sys.stderr)
        return 2
    try:
        print(commands[argv[0]]())
    except (OSError, RuntimeError) as error:
        print(f"A01 STOP GUARD FAILED: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
