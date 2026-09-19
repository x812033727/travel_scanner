"""The deploy hold every multi-phase release on the production host must own.

The host has two deployment paths that cannot see each other. The one-shot script
``/root/deploy-travel-scanner.sh`` fast-forwards to ``origin/main`` and rebuilds every
application container. A staged release driver (``prepare`` -> CI -> ``activate`` ->
``dry-run`` -> ``drafts`` -> ``publish-articles`` -> ``publish-index``) checks at the start
of each phase that the containers are still the ones the previous phase left behind.
Both take ``/var/lock/travel-scanner-deploy.lock``, but a driver holds it only while a
phase runs; between phases the script could rebuild the containers, and on 2026-09-14
it did, so ``activate`` refused and the release needed a hand-written reconcile step.

Since then the script exits 3 with ``NOT DEPLOYING: another release is in progress``
while ``/root/travel-scanner-deploy.hold`` exists, and prints the file's first 600 bytes
as the reason. This module is the shared way a driver creates, checks and removes that
file (``docs/ai-news-2026-ytd/release_hold.py`` was the first, task-local copy of the
same contract):

* ``acquire`` in ``prepare``, once the shared locks are held and before anything is
  built or recorded as the baseline;
* ``verify`` at the start of ``activate`` and of every content phase;
* ``clear`` after the last phase has succeeded. Never on failure or rollback: the file
  stays until a human has inspected the release directory (see ``README.md``).

The file has two lines. The first is for people, at most 600 bytes, and is what the
deploy script prints. The second is JSON with ``target``, ``release_dir``, ``owner``,
``phases`` and ``created_at``; ``verify`` and ``clear`` compare ``target`` and
``release_dir`` and nothing else, so a hold written by an older driver with the same
two keys is recognised. Neither line may carry a secret or anything from ``.env``.

Standard library only and no ``fcntl``: the host runs Python 3.14 and the tests also
run on Windows. Nothing here takes a lock. The caller must already hold the four
shared locks named in ``README.md``; that is what makes read-then-write safe.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path

HOLD_PATH = Path("/root/travel-scanner-deploy.hold")
FIRST_LINE_LIMIT = 600  # bytes; the deploy script prints at most this much of the file
OWNER_LIMIT = 64  # characters
REFUSED_EXIT = 3  # the deploy script's own exit code for "another release is in progress"

_TARGET = re.compile(r"[0-9a-f]{40}")
_ONE_LINE = re.compile(r"[^\x00-\x1f\x7f]+")


class HoldError(RuntimeError):
    """The hold file is not in the state this release needs."""


class HeldByAnother(HoldError):
    """The hold exists but names another release, or was written by hand."""

    def __init__(self, hold_path: Path, first_line: str) -> None:
        self.hold_path = hold_path
        self.first_line = first_line
        reason = first_line or "(empty file)"
        super().__init__(f"{hold_path} is held by someone else: {reason}")


class HoldMissing(HoldError):
    """The hold this release created is gone."""

    def __init__(self, hold_path: Path) -> None:
        self.hold_path = hold_path
        super().__init__(
            f"{hold_path} does not exist; this release no longer holds the deploy hold"
        )


def acquire(
    release_dir: str | os.PathLike[str],
    target_sha: str,
    owner: str,
    phases: Iterable[str],
    *,
    hold_path: str | os.PathLike[str] = HOLD_PATH,
    now: dt.datetime | None = None,
) -> str:
    """Create the hold for one release and return ``"created"``.

    Returns ``"resumed"`` instead when the file already names this same ``release_dir``
    and ``target_sha`` (a driver run again after an interrupted phase); the file is left
    as it was. Raises :class:`HeldByAnother` when it names anything else, including a
    hold a person wrote by hand. Never overwrites.
    """
    record = _record(release_dir, target_sha, owner, phases, now)
    content = _render(record)
    path = Path(hold_path)
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        first_line, existing = _read(path)
        if existing is not None and _same_release(existing, record):
            return "resumed"
        raise HeldByAnother(path, first_line) from None
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    # Release drivers run under umask 077; the deploy script reads the file as root, but
    # anyone else on the host should be able to read why deploys are refused.
    os.chmod(path, 0o644)
    return "created"


def verify(
    release_dir: str | os.PathLike[str],
    target_sha: str,
    *,
    hold_path: str | os.PathLike[str] = HOLD_PATH,
) -> dict[str, object]:
    """Check, at the start of a phase, that the hold still names this release.

    Returns the JSON record. Raises :class:`HoldMissing` when the file is gone and
    :class:`HeldByAnother` when it names another release or cannot be parsed.
    """
    path = Path(hold_path)
    expected = {"release_dir": _release_dir(release_dir), "target": _target(target_sha)}
    if not path.exists():
        raise HoldMissing(path)
    first_line, record = _read(path)
    if record is None or not _same_release(record, expected):
        raise HeldByAnother(path, first_line)
    return record


def clear(
    release_dir: str | os.PathLike[str],
    target_sha: str,
    *,
    hold_path: str | os.PathLike[str] = HOLD_PATH,
) -> str:
    """Remove the hold once the last phase has succeeded.

    Deletes only a file that names this release and returns ``"cleared"``. Returns
    ``"missing"`` when there is nothing to remove, so a driver can report it without
    failing a release that has already finished. Raises :class:`HeldByAnother` and
    leaves the file alone when it names anyone else.
    """
    path = Path(hold_path)
    try:
        verify(release_dir, target_sha, hold_path=path)
    except HoldMissing:
        return "missing"
    path.unlink()
    return "cleared"


def read(hold_path: str | os.PathLike[str] = HOLD_PATH) -> tuple[str, dict[str, object] | None]:
    """Return the hold's first line and its JSON record, or ``("", None)`` when absent.

    The record is ``None`` for a file without a parseable second line, such as one a
    person wrote by hand; such a file still blocks deploys and is still respected here.
    """
    path = Path(hold_path)
    if not path.exists():
        return "", None
    return _read(path)


def _record(
    release_dir: str | os.PathLike[str],
    target_sha: str,
    owner: str,
    phases: Iterable[str],
    now: dt.datetime | None,
) -> dict[str, object]:
    names = [str(phase) for phase in phases]
    if not names or any(not _ONE_LINE.fullmatch(name) for name in names):
        raise ValueError("phases must be a non-empty sequence of single-line names")
    if not isinstance(owner, str) or not _ONE_LINE.fullmatch(owner) or len(owner) > OWNER_LIMIT:
        raise ValueError(f"owner must be one line of at most {OWNER_LIMIT} characters")
    moment = now if now is not None else dt.datetime.now(dt.UTC)
    if moment.tzinfo is None:
        raise ValueError("now must be timezone-aware")
    return {
        "target": _target(target_sha),
        "release_dir": _release_dir(release_dir),
        "owner": owner,
        "phases": names,
        "created_at": moment.astimezone(dt.UTC).isoformat(timespec="seconds"),
    }


def _target(target_sha: str) -> str:
    if not isinstance(target_sha, str) or not _TARGET.fullmatch(target_sha):
        raise ValueError("target_sha must be the 40-character lowercase commit hash")
    return target_sha


def _release_dir(release_dir: str | os.PathLike[str]) -> str:
    path = Path(release_dir)
    text = str(path)
    if not path.is_absolute() or not _ONE_LINE.fullmatch(text):
        raise ValueError("release_dir must be an absolute path on one line")
    return text


def _render(record: dict[str, object]) -> str:
    phases = list(record["phases"])  # type: ignore[call-overload]
    shown = "→".join(phases) if len(phases) <= 3 else f"{phases[0]}→…→{phases[-1]}"
    target = str(record["target"])
    first_line = (
        f"{record['owner']} 正在發布 {target[:12]}（{record['release_dir']}，階段 {shown}，"
        f"開始於 {record['created_at']}）；檢查該目錄後才能刪除本檔"
    )
    if len(first_line.encode("utf-8")) > FIRST_LINE_LIMIT:
        raise ValueError(
            f"the hold's first line would exceed {FIRST_LINE_LIMIT} bytes; "
            "shorten owner or release_dir"
        )
    return first_line + "\n" + json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"


def _read(path: Path) -> tuple[str, dict[str, object] | None]:
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    first_line = lines[0] if lines else ""
    if len(lines) < 2:
        return first_line, None
    try:
        record = json.loads(lines[1])
    except ValueError:
        return first_line, None
    if not isinstance(record, dict) or not {"target", "release_dir"} <= set(record):
        return first_line, None
    return first_line, record


def _same_release(record: Mapping[str, object], other: Mapping[str, object]) -> bool:
    return (
        record.get("target") == other["target"]
        and record.get("release_dir") == other["release_dir"]
    )


def main(argv: list[str] | None = None) -> int:
    """A small command line for rehearsals and for a driver written in another language."""
    parser = argparse.ArgumentParser(
        description="Create, check or remove the production deploy hold.",
        epilog=f"A refusal exits {REFUSED_EXIT}, like the deploy script itself.",
    )
    parser.add_argument("--hold-path", type=Path, default=HOLD_PATH)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("acquire", "verify", "clear"):
        command = commands.add_parser(name)
        command.add_argument("release_dir")
        command.add_argument("target_sha")
        if name == "acquire":
            command.add_argument("owner")
            command.add_argument("phases", nargs="+")
    commands.add_parser("show")
    args = parser.parse_args(argv)
    try:
        if args.command == "acquire":
            print(
                acquire(
                    args.release_dir,
                    args.target_sha,
                    args.owner,
                    args.phases,
                    hold_path=args.hold_path,
                )
            )
        elif args.command == "verify":
            print(
                json.dumps(
                    verify(args.release_dir, args.target_sha, hold_path=args.hold_path),
                    ensure_ascii=False,
                )
            )
        elif args.command == "clear":
            print(clear(args.release_dir, args.target_sha, hold_path=args.hold_path))
        else:
            first_line, record = read(args.hold_path)
            if not first_line and record is None:
                print(f"no hold at {args.hold_path}")
            else:
                print(first_line)
                if record is not None:
                    print(json.dumps(record, ensure_ascii=False))
    except (HoldError, ValueError) as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return REFUSED_EXIT
    return 0


if __name__ == "__main__":
    sys.exit(main())
