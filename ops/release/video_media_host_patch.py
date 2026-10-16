"""Incremental API media drain installer for a host script already patched by #1527.

Importing or running ``--render`` is read-only. ``--install`` is a separate,
owner-approved host action: it takes the deploy flock, binds the exact current
host script and stage helper hashes, backs up, and installs atomically.
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

import video_stage_host_patch as stage

HOST_SCRIPT = Path("/root/deploy-travel-scanner.sh")
STAGE_HELPER = Path(stage.HELPER_LITERAL)
STAGE_HELPER_SHA256 = "6ea459ddb128fecb4a90ff1d0028046b8d477a58454f25d37286ea045284e2a5"
HELPER_LITERAL = "/opt/travel-scanner-deploy/video_media_drain.sh"
HELPER = Path(HELPER_LITERAL)
HELPER_SHA256 = "12aebe004394b7aa756f67e0d778296311e8c2bf1d44f91abb45a9f94149bf29"
LOCK = Path("/var/lock/travel-scanner-deploy.lock")

STAGE_TRAP = "trap 'rm -f -- \"$VIDEO_STAGE_DRAIN_READY_FILE\"' EXIT\n"
MEDIA_SETUP = (
    "unset VIDEO_MEDIA_GUARD_REPO VIDEO_MEDIA_GUARD_COMPOSE_FILE VIDEO_MEDIA_DRAIN_MARKER\n"
    "VIDEO_MEDIA_DRAIN_NONCE=$VIDEO_STAGE_DRAIN_NONCE\n"
    "VIDEO_MEDIA_DRAIN_LOCAL_SHA=$LOCAL_SHA\n"
    "VIDEO_MEDIA_DRAIN_READY_FILE=/run/travel-scanner-deploy/video-api-drain.ready.$VIDEO_MEDIA_DRAIN_NONCE\n"
    "export VIDEO_MEDIA_DRAIN_NONCE VIDEO_MEDIA_DRAIN_LOCAL_SHA VIDEO_MEDIA_DRAIN_READY_FILE\n"
    "trap 'rm -f -- \"$VIDEO_STAGE_DRAIN_READY_FILE\" \"$VIDEO_MEDIA_DRAIN_READY_FILE\"' EXIT\n"
)
STAGE_NORMAL_CALL = f"if ! {stage.HELPER_LITERAL} --normal; then\n"
NORMAL_START_ANCHOR = (
    'log "building and starting (profiles: $PROFILE news)"\n'
    "if ! compose up --build -d; then\n"
)


def _restore(reason: str) -> str:
    """Return the reviewed pre-recreate failure path; never restart a dubious API."""
    return (
        "  if (( BEHIND > 0 )); then\n"
        f'    git reset --hard "$LOCAL_SHA" --quiet || fail "{reason}; checkout reset failed. Log: $LOG_FILE"\n'
        f'    ensure_readable || fail "{reason}; checkout permissions failed. Log: $LOG_FILE"\n'
        "  fi\n"
        '  restored_sha=$(git rev-parse HEAD) || fail "cannot read restored checkout. Log: $LOG_FILE"\n'
        '  restored_status=$(git status --porcelain) || fail "cannot read restored status. Log: $LOG_FILE"\n'
        '  [[ $restored_sha == "$LOCAL_SHA" && -z $restored_status ]] || fail '
        f'"{reason}; checkout restoration not clean. Log: $LOG_FILE"\n'
    )


PRECHECK_AND_BUILD = (
    f"if ! {HELPER_LITERAL} --precheck; then\n"
    '  log "video media precheck refused before managed stop; inspect API and exact queued jobs"\n'
    + _restore("video media precheck refused")
    + '  fail "video media precheck refused; no API stop requested. Log: $LOG_FILE"\n'
    "fi\n"
    'log "building images before draining video services"\n'
    "if ! compose build; then\n"
    '  log "image prebuild failed; no managed stop requested"\n'
    + _restore("image prebuild failed")
    + '  fail "image prebuild failed before video drains. Log: $LOG_FILE"\n'
    "fi\n"
)
NORMAL_MEDIA_AND_UP = (
    f"if ! {HELPER_LITERAL} --normal; then\n"
    '  log "video media API drain refused; API may be stopped; reconcile marker, jobs and receipts"\n'
    + _restore("video media API drain refused")
    + '  fail "video media API drain refused; do not force a restart. Log: $LOG_FILE"\n'
    "fi\n"
    'log "starting prebuilt images (profiles: $PROFILE news)"\n'
    "if ! compose up --no-build -d; then\n"
)
ROLLBACK_BUILD_ANCHOR = (
    '  ensure_readable || fail "$why; rollback checkout permissions failed; '
    'worker may be stopped. Log: $LOG_FILE"\n'
)
ROLLBACK_UP_ANCHOR = (
    '  compose up --build -d || fail "$why, and the rollback rebuild also failed - '
    'MANUAL INTERVENTION NEEDED. Log: $LOG_FILE"\n'
)
ROLLBACK_MEDIA_AND_UP = (
    f'  {HELPER_LITERAL} --rollback || fail "$why; video media API did not drain before rollback; '
    'reconcile marker and jobs. Log: $LOG_FILE"\n'
    '  compose up --no-build -d || fail "$why, and the rollback start also failed - '
    'MANUAL INTERVENTION NEEDED. Log: $LOG_FILE"\n'
)


def _replace_once(source: str, old: str, new: str, label: str) -> str:
    if source.count(old) != 1:
        raise ValueError(f"expected exactly one reviewed {label} anchor")
    return source.replace(old, new)


def patch_script(original: str) -> str:
    """Patch only the reviewed #1527 output; unknown script drift is a refusal."""
    if HELPER_LITERAL in original:
        raise ValueError("host script already mentions the media drain helper")
    if original.count(stage.HELPER_LITERAL) != 2:
        raise ValueError("host script is not the reviewed #1527 stage-drain output")
    for anchor, label in (
        (stage.NORMAL_HOOK, "stage normal"),
        (stage.ROLLBACK_HOOK, "stage rollback"),
        (stage.NO_ROLLBACK_HOOK, "no-rollback"),
    ):
        if original.count(anchor) != 1:
            raise ValueError(f"expected exactly one reviewed {label} section")

    normal = stage.NORMAL_HOOK
    normal = _replace_once(normal, STAGE_TRAP, MEDIA_SETUP, "stage trap")
    normal = _replace_once(
        normal, STAGE_NORMAL_CALL, PRECHECK_AND_BUILD + STAGE_NORMAL_CALL, "stage call"
    )
    normal = _replace_once(
        normal, NORMAL_START_ANCHOR, NORMAL_MEDIA_AND_UP, "normal compose up"
    )

    rollback = stage.ROLLBACK_HOOK
    rollback = _replace_once(
        rollback,
        ROLLBACK_BUILD_ANCHOR,
        ROLLBACK_BUILD_ANCHOR
        + '  compose build || fail "$why; rollback image prebuild failed; API/worker state needs reconciliation. Log: $LOG_FILE"\n',
        "rollback readable",
    )
    rollback = _replace_once(
        rollback, ROLLBACK_UP_ANCHOR, ROLLBACK_MEDIA_AND_UP, "rollback compose up"
    )
    no_rollback = stage.NO_ROLLBACK_HOOK.replace(
        "The video worker may be stopped or missing.",
        "The video AI worker and API may be stopped or missing.",
    )
    if no_rollback == stage.NO_ROLLBACK_HOOK:
        raise ValueError("unreviewed no-rollback warning")
    return (
        original.replace(stage.NORMAL_HOOK, normal)
        .replace(stage.ROLLBACK_HOOK, rollback)
        .replace(stage.NO_ROLLBACK_HOOK, no_rollback)
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


def install(
    host_script: Path,
    expected_sha256: str,
    *,
    stage_helper: Path = STAGE_HELPER,
    helper: Path = HELPER,
    lock: Path = LOCK,
) -> Path:
    # Linux-only host installer; render and unit tests run on Windows too.
    import fcntl

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
        if hashlib.sha256(stage_helper.read_bytes()).hexdigest() != STAGE_HELPER_SHA256:
            raise ValueError("installed #1527 stage helper is not the reviewed bytes")
        if stat.S_IMODE(stage_helper.stat().st_mode) != 0o700:
            raise ValueError("installed #1527 stage helper mode is not 0700")
        patched = patch_script(original.decode("utf-8")).encode("utf-8")
        helper_data = Path(__file__).with_name("video_media_drain.sh").read_bytes()
        if hashlib.sha256(helper_data).hexdigest() != HELPER_SHA256:
            raise ValueError("media helper bytes differ from the independently reviewed SHA-256")
        if not helper_data.startswith(b"#!/usr/bin/env bash\n"):
            raise ValueError("media helper has no bash shebang")
        for data in (helper_data, patched):
            subprocess.run(["bash", "-n"], input=data, check=True)
        stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        backup = host_script.with_name(f"{host_script.name}.before-video-media-drain-{stamp}")
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
                raise RuntimeError("installed host script readback mismatch")
        except Exception as error:
            try:
                _write_atomic(host_script, original, 0o700)
                if hashlib.sha256(host_script.read_bytes()).hexdigest() != actual:
                    raise RuntimeError("restored host script hash mismatch")
            except Exception as restore_error:
                raise RuntimeError(
                    f"media install failed ({error}); host restoration failed; backup: {backup}"
                ) from restore_error
            raise
        return backup


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host-script", type=Path, default=HOST_SCRIPT)
    parser.add_argument("--render", action="store_true", help="print guarded script; no writes")
    parser.add_argument("--install", action="store_true", help="explicit owner approval required")
    parser.add_argument("--expected-sha256", help="exact #1527-patched host script SHA-256")
    args = parser.parse_args()
    if args.render == args.install:
        parser.error("choose exactly one of --render and --install")
    if args.render:
        print(patch_script(args.host_script.read_text(encoding="utf-8")), end="")
        return
    if not args.expected_sha256 or len(args.expected_sha256) != 64:
        parser.error("--install requires a reviewed --expected-sha256")
    backup = install(args.host_script, args.expected_sha256)
    print(f"installed; rollback backup: {backup}")


if __name__ == "__main__":
    main()
