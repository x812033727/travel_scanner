"""Host-operator Redis hold for the exact legacy media job during an API cutover.

This file is self-contained so an approved operator can copy it into a still-running,
non-API Python container after the old API has gracefully exited. ``acquire`` creates a
private fsynced receipt file before touching Redis and prints only the nonce hash.
Copy the receipt to a root-owned mode-0600 host file without displaying its contents.
``inspect``/``watch``/``release`` read that receipt from stdin and print no nonce.
The runbook governs when these commands are allowed; this CLI does not stop containers.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import hmac
import json
import os
import re
import secrets
import stat
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from redis.asyncio import Redis

JOB_ID = "b721a65d-8c8d-4ae8-834c-391cfc267a6f"
KEY = f"video-media:lock:{JOB_ID}"
WAITAOF_TIMEOUT_MS = 10_000


class CutoverLockError(Exception):
    pass


def _receipt_from_stdin() -> dict[str, Any]:
    try:
        receipt = json.load(sys.stdin)
    except (ValueError, OSError) as error:
        raise CutoverLockError("invalid_receipt") from error
    if (
        not isinstance(receipt, dict)
        or receipt.get("job_id") != JOB_ID
        or receipt.get("key") != KEY
    ):
        raise CutoverLockError("wrong_receipt_identity")
    nonce = receipt.get("nonce")
    if not isinstance(nonce, str) or re.fullmatch(r"[0-9a-f]{64}", nonce) is None:
        raise CutoverLockError("invalid_receipt_nonce")
    return receipt


def _write_receipt(path: Path, receipt: dict[str, Any], *, exclusive: bool) -> None:
    """Keep the nonce in a private, fsynced container file before the Redis SET."""
    if path.parent != Path("/tmp") or not path.name.startswith("a01-media-cutover-"):  # noqa: S108
        raise CutoverLockError("unsafe_receipt_path")
    cloexec = getattr(os, "O_CLOEXEC", 0)
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    directory_flag = getattr(os, "O_DIRECTORY", 0)
    if not all((cloexec, nofollow, directory_flag)):
        raise CutoverLockError("linux_open_flags_required")
    if exclusive:
        target = path
    else:
        target = path.with_name(f"{path.name}.{secrets.token_hex(8)}.tmp")
    data = (json.dumps(receipt, sort_keys=True) + "\n").encode("utf-8")
    fd = os.open(
        target,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | cloexec | nofollow,
        0o600,
    )
    try:
        os.fchmod(fd, 0o600)
        remaining = memoryview(data)
        while remaining:
            count = os.write(fd, remaining)
            if count <= 0:
                raise CutoverLockError("receipt_short_write")
            remaining = remaining[count:]
        os.fsync(fd)
    finally:
        os.close(fd)
    if not exclusive:
        os.replace(target, path)
    directory = os.open(path.parent, os.O_RDONLY | directory_flag | nofollow)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
        raise CutoverLockError("receipt_not_private_regular_file")


async def acquire(redis: Redis, *, nonce: str | None = None) -> tuple[dict[str, Any], int]:
    """SET NX and WAITAOF on one dedicated Redis connection, then read back the nonce."""
    value = nonce or secrets.token_hex(32)
    if re.fullmatch(r"[0-9a-f]{64}", value) is None:
        raise CutoverLockError("invalid_nonce")
    async with redis.client() as connection:
        if not await connection.set(KEY, value, nx=True):
            raise CutoverLockError("lock_already_exists")
        receipt: dict[str, Any] = {
            "schema_version": 1,
            "job_id": JOB_ID,
            "key": KEY,
            "nonce": value,
            "acquired_at_utc": datetime.now(UTC).isoformat(),
            "waitaof_local": 0,
            "durable": False,
        }
        try:
            ack = await cast(Any, connection).execute_command("WAITAOF", 1, 0, WAITAOF_TIMEOUT_MS)
            local = int(ack[0]) if isinstance(ack, (list, tuple)) and ack else 0
            observed = await connection.get(KEY)
            ttl = await connection.ttl(KEY)
            receipt["waitaof_local"] = local
            receipt["durable"] = (
                local == 1
                and ttl == -1
                and isinstance(observed, bytes)
                and hmac.compare_digest(observed, value.encode("ascii"))
            )
        except Exception:
            # The key may still exist. Always return the nonce so recovery can inspect it.
            return receipt, 3
        return receipt, 0 if receipt["durable"] else 3


async def inspect(redis: Redis, receipt: dict[str, Any]) -> dict[str, Any]:
    nonce = str(receipt["nonce"])
    async with redis.client() as connection:
        observed = await connection.get(KEY)
        ttl = await connection.ttl(KEY)
    if not isinstance(observed, bytes) or not hmac.compare_digest(
        observed, nonce.encode("ascii")
    ):
        raise CutoverLockError("nonce_lost_or_replaced")
    if ttl != -1:
        raise CutoverLockError("lock_has_expiry")
    return {
        "schema_version": 1,
        "job_id": JOB_ID,
        "owned": True,
        "no_expiry": True,
        "nonce_sha256": hashlib.sha256(nonce.encode("ascii")).hexdigest(),
    }


async def release(redis: Redis, receipt: dict[str, Any]) -> dict[str, Any]:
    if receipt.get("durable") is not True or receipt.get("waitaof_local") != 1:
        raise CutoverLockError("acquire_not_durable")
    nonce = str(receipt["nonce"])
    script = (
        "if redis.call('GET', KEYS[1]) == ARGV[1] "
        "then return redis.call('DEL', KEYS[1]) else return 0 end"
    )
    async with redis.client() as connection:
        deleted = await connection.eval(script, 1, KEY, nonce)
        if deleted == 1:
            ack = await cast(Any, connection).execute_command("WAITAOF", 1, 0, WAITAOF_TIMEOUT_MS)
            local = int(ack[0]) if isinstance(ack, (list, tuple)) and ack else 0
            absent = await connection.get(KEY) is None
        else:
            local = 0
            absent = False
    if deleted != 1:
        raise CutoverLockError("nonce_lost_or_replaced")
    if local != 1 or not absent:
        raise CutoverLockError("release_not_durable_or_absent")
    return {
        "schema_version": 1,
        "job_id": JOB_ID,
        "released_own_nonce": True,
        "waitaof_local": local,
        "lock_absent": absent,
    }


async def watch(redis: Redis, receipt: dict[str, Any], *, interval_seconds: float = 2.0) -> None:
    """Continuously fail if ownership changes; the host must also watch this process itself."""
    iteration = 0
    while True:
        await inspect(redis, receipt)
        iteration += 1
        if iteration == 1 or iteration % 15 == 0:
            print(json.dumps({"job_id": JOB_ID, "owned": True, "checks": iteration}), flush=True)
        await asyncio.sleep(interval_seconds)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("action", choices=("acquire", "inspect", "watch", "release"))
    command.add_argument("--receipt-file", type=Path)
    return command


async def run(action: str, receipt_file: Path | None) -> tuple[dict[str, Any] | None, int]:
    url = os.environ.get("REDIS_URL")
    if not url:
        raise CutoverLockError("redis_url_missing")
    # WAITAOF itself may wait ten seconds. The client read timeout must exceed that
    # bound, and an ambiguous timeout must never retry SET/DEL on another connection.
    redis = Redis.from_url(
        url,
        socket_timeout=WAITAOF_TIMEOUT_MS / 1000 + 10,
        socket_connect_timeout=5,
        retry_on_timeout=False,
    )
    try:
        if action == "acquire":
            if receipt_file is None:
                raise CutoverLockError("receipt_file_required")
            nonce = secrets.token_hex(32)
            initial = {
                "schema_version": 1,
                "job_id": JOB_ID,
                "key": KEY,
                "nonce": nonce,
                "acquired_at_utc": datetime.now(UTC).isoformat(),
                "waitaof_local": 0,
                "durable": False,
            }
            _write_receipt(receipt_file, initial, exclusive=True)
            try:
                receipt, code = await acquire(redis, nonce=nonce)
            except CutoverLockError as error:
                if str(error) == "lock_already_exists":
                    await asyncio.to_thread(receipt_file.unlink)
                raise
            _write_receipt(receipt_file, receipt, exclusive=False)
            return {
                "schema_version": 1,
                "job_id": JOB_ID,
                "receipt_file": str(receipt_file),
                "nonce_sha256": hashlib.sha256(nonce.encode("ascii")).hexdigest(),
                "waitaof_local": receipt["waitaof_local"],
                "durable": receipt["durable"],
            }, code
        if receipt_file is not None:
            raise CutoverLockError("receipt_file_only_for_acquire")
        receipt = _receipt_from_stdin()
        if action == "inspect":
            return await inspect(redis, receipt), 0
        if action == "release":
            return await release(redis, receipt), 0
        await watch(redis, receipt)
        return None, 0
    finally:
        await redis.aclose()


def main() -> int:
    args = parser().parse_args()
    try:
        result, code = asyncio.run(run(args.action, args.receipt_file))
    except CutoverLockError as error:
        print(json.dumps({"error": str(error)}))
        return 3
    except Exception as error:
        print(json.dumps({"error": "cutover_lock_unavailable", "type": type(error).__name__}))
        return 4
    if result is not None:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
