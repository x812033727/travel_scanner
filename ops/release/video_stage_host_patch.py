"""Review and install the video-stage warm-drain hook in the host-only deploy script.

The host's /root/deploy-travel-scanner.sh is deliberately outside Git. Installation
is an explicit root action, pinned to the previously reviewed SHA-256. Importing or
running ``--render`` makes no writes. ``--install`` takes the deploy lock, saves a
byte-for-byte backup, installs the reviewed helper, and replaces the host script.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path

HOST_SCRIPT = Path("/root/deploy-travel-scanner.sh")
# Keep the rendered shell path POSIX on Windows too. Path.__str__ would turn it
# into a Windows-rooted path when patch_script is run in local review.
HELPER_LITERAL = "/opt/travel-scanner-deploy/video_stage_drain.sh"
HELPER = Path(HELPER_LITERAL)
LOCK = Path("/var/lock/travel-scanner-deploy.lock")

ROLLBACK_ANCHOR = (
    '  git reset --hard "$LOCAL_SHA" --quiet\n'
    '  ensure_readable\n'
    '  compose up --build -d || fail "$why, and the rollback rebuild also failed - '
    'MANUAL INTERVENTION NEEDED. Log: $LOG_FILE"\n'
)
NORMAL_ANCHOR = (
    'ensure_readable\n'
    'log "building and starting (profiles: $PROFILE news)"\n'
    'if ! compose up --build -d; then\n'
)
ROLLBACK_HOOK = (
    '  git reset --hard "$LOCAL_SHA" --quiet || fail "$why; rollback checkout reset failed; '
    'worker may be stopped. Log: $LOG_FILE"\n'
    '  ensure_readable || fail "$why; rollback checkout permissions failed; '
    'worker may be stopped. Log: $LOG_FILE"\n'
    f'  {HELPER_LITERAL} --rollback || fail "$why; video AI worker did not drain before rollback; '
    'checkout is at original SHA, worker may be stopped. Log: $LOG_FILE"\n'
    '  compose up --build -d || fail "$why, and the rollback rebuild also failed - '
    'MANUAL INTERVENTION NEEDED. Log: $LOG_FILE"\n'
)
NORMAL_HOOK = (
    'ensure_readable\n'
    # The installed helper has offline-test overrides; production must inspect
    # the same repository, compose project and marker as this host script.
    'unset VIDEO_STAGE_GUARD_REPO VIDEO_STAGE_GUARD_COMPOSE_FILE VIDEO_STAGE_DRAIN_MARKER\n'
    'VIDEO_STAGE_DRAIN_NONCE=$(cat /proc/sys/kernel/random/uuid) || fail "cannot create video drain nonce"\n'
    'VIDEO_STAGE_DRAIN_LOCAL_SHA=$LOCAL_SHA\n'
    'VIDEO_STAGE_DRAIN_READY_FILE=/run/travel-scanner-deploy/video-ai-drain.ready.$VIDEO_STAGE_DRAIN_NONCE\n'
    'export VIDEO_STAGE_DRAIN_NONCE VIDEO_STAGE_DRAIN_LOCAL_SHA VIDEO_STAGE_DRAIN_READY_FILE\n'
    'trap \'rm -f -- "$VIDEO_STAGE_DRAIN_READY_FILE"\' EXIT\n'
    f'if ! {HELPER_LITERAL} --normal; then\n'
    '  log "video AI warm drain refused; worker state unknown and may be stopped"\n'
    '  if (( BEHIND > 0 )); then\n'
    '    git reset --hard "$LOCAL_SHA" --quiet || fail "video drain refused and checkout reset failed; '
    'worker may be stopped. Log: $LOG_FILE"\n'
    '    ensure_readable || fail "video drain refused and checkout permissions failed; '
    'worker may be stopped. Log: $LOG_FILE"\n'
    '  fi\n'
    '  restored_sha=$(git rev-parse HEAD) || fail "video drain refused and checkout readback failed; '
    'worker may be stopped. Log: $LOG_FILE"\n'
    '  restored_status=$(git status --porcelain) || fail "video drain refused and checkout status failed; '
    'worker may be stopped. Log: $LOG_FILE"\n'
    '  [[ $restored_sha == "$LOCAL_SHA" && -z $restored_status ]] || fail '
    '"video drain refused; checkout restore did not read back cleanly; '
    'worker may be stopped. Log: $LOG_FILE"\n'
    '  fail "video AI worker did not drain before compose up; checkout restored to original SHA; '
    'worker may be stopped. Log: $LOG_FILE"\n'
    'fi\n'
    'log "building and starting (profiles: $PROFILE news)"\n'
    'if ! compose up --build -d; then\n'
)
NO_ROLLBACK_ANCHOR = (
    '    fail "$why - left in place because --no-rollback was given. Roll back manually with:\n'
    '    git -C $REPO reset --hard $LOCAL_SHA && cd $REPO && docker compose -f '
    '$COMPOSE_FILE --profile $PROFILE --profile news --profile video up --build -d"\n'
)
NO_ROLLBACK_HOOK = (
    '    fail "$why; --no-rollback left the new checkout in place. The video worker may be '
    'stopped or missing. Reconcile its exact container, RQ and DB receipts before any '
    'recovery; use a guarded deployment under the deploy lock, never a raw compose up. '
    'Log: $LOG_FILE"\n'
)


def patch_script(original: str) -> str:
    if HELPER_LITERAL in original:
        raise ValueError("host script already mentions the video-stage drain helper")
    for anchor in (ROLLBACK_ANCHOR, NORMAL_ANCHOR, NO_ROLLBACK_ANCHOR):
        if original.count(anchor) != 1:
            raise ValueError(f"expected exactly one reviewed host-script anchor: {anchor[:40]!r}")
    return (
        original.replace(ROLLBACK_ANCHOR, ROLLBACK_HOOK)
        .replace(NORMAL_ANCHOR, NORMAL_HOOK)
        .replace(NO_ROLLBACK_ANCHOR, NO_ROLLBACK_HOOK)
    )


def _write_atomic(path: Path, data: bytes, mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(name, mode)
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def install(host_script: Path, expected_sha256: str, *, helper: Path = HELPER, lock: Path = LOCK) -> Path:
    # Linux-only because production installation must serialize with both manual
    # and automatic deploys. Unit tests exercise patch_script on every platform.
    import fcntl  # noqa: PLC0415

    with lock.open("a+b") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RuntimeError("deploy lock is held; no installation") from error
        original = host_script.read_bytes()
        actual = hashlib.sha256(original).hexdigest()
        if actual != expected_sha256:
            raise ValueError(f"host script SHA-256 changed: {actual}; expected {expected_sha256}")
        if stat.S_IMODE(host_script.stat().st_mode) != 0o700:
            raise ValueError("host script mode is not the reviewed 0700")
        patched = patch_script(original.decode("utf-8")).encode("utf-8")
        helper_data = Path(__file__).with_name("video_stage_drain.sh").read_bytes()
        if not helper_data.startswith(b"#!/usr/bin/env bash\n"):
            raise ValueError("reviewed helper has no bash shebang")
        for data in (helper_data, patched):
            subprocess.run(["bash", "-n"], input=data, check=True)  # noqa: S603
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        backup = host_script.with_name(f"{host_script.name}.before-video-stage-drain-{stamp}")
        if backup.exists():
            raise FileExistsError(backup)
        shutil.copy2(host_script, backup)
        os.chmod(backup, 0o600)
        if hashlib.sha256(backup.read_bytes()).hexdigest() != actual:
            raise RuntimeError("host script backup hash mismatch; no installation")
        try:
            _write_atomic(helper, helper_data, 0o700)
            _write_atomic(host_script, patched, 0o700)
            if hashlib.sha256(host_script.read_bytes()).digest() != hashlib.sha256(patched).digest():
                raise RuntimeError("host script did not read back as the installed bytes")
        except Exception as error:
            # A copied helper with the original host script is inert, but a
            # partial/changed host script must never be left live. Restore the
            # exact reviewed baseline under the same deploy flock.
            try:
                _write_atomic(host_script, original, 0o700)
                if hashlib.sha256(host_script.read_bytes()).hexdigest() != actual:
                    raise RuntimeError("restored host script hash mismatch")
            except Exception as restore_error:
                raise RuntimeError(
                    f"install failed ({error}); host script restoration failed; backup: {backup}"
                ) from restore_error
            raise
        return backup


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host-script", type=Path, default=HOST_SCRIPT)
    parser.add_argument("--render", action="store_true", help="print the guarded script, no writes")
    parser.add_argument("--install", action="store_true", help="apply only after owner approval")
    parser.add_argument("--expected-sha256", help="required for installation; pin read-only baseline")
    args = parser.parse_args()
    if args.render == args.install:
        parser.error("choose exactly one of --render and --install")
    if args.render:
        print(patch_script(args.host_script.read_text(encoding="utf-8")), end="")
        return
    if not args.expected_sha256 or len(args.expected_sha256) != 64:
        parser.error("--install requires the reviewed --expected-sha256")
    backup = install(args.host_script, args.expected_sha256)
    print(f"installed; rollback backup: {backup}")


if __name__ == "__main__":
    main()
