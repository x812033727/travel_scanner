"""Read-only, exact-job checks for the A01 media dispatch fence.

Run in the API container. ``propose`` prints canonical JSON for a candidate marker;
``validate`` compares a candidate file to the current database row; ``check`` additionally
requires that exact file on the API's existing read-only video-work mount. None of these
commands advances a media job or calls a vendor.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
from pathlib import Path
from typing import Any
from uuid import UUID

from redis.asyncio import Redis
from sqlalchemy import func, select

from app.config import get_settings
from app.db import SessionFactory
from app.video_media.cutover_intake import IntakeFenceError, inspect_intake
from app.video_media.dispatch_fence import (
    PINNED_JOB_ID,
    DispatchFenceError,
    expected_manifest,
    fence_path,
    inspect_installed_fence,
    inspect_manifest,
)
from app.video_media.jobs import B25_CUTOVER_SLUG, MediaJobFailed, refuse_b25_cutover_media
from app.video_media.models import VideoMediaJob


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    subcommands = command.add_subparsers(dest="action", required=True)
    for name in ("propose", "validate", "check"):
        sub = subcommands.add_parser(name)
        sub.add_argument("--job-id", type=UUID, required=True)
        if name == "validate":
            sub.add_argument("--manifest", type=Path, required=True)
        if name == "check":
            sub.add_argument("--expect-operator-lock", action="store_true")
    return command


def canonical_manifest(job: VideoMediaJob) -> str:
    return (
        json.dumps(
            expected_manifest(job), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        + "\n"
    )


def b25_guard_receipt() -> dict[str, str | bool]:
    """Exercise the compiled, read-only B25 refusal without touching a job or vendor."""
    try:
        refuse_b25_cutover_media(B25_CUTOVER_SLUG)
    except MediaJobFailed as error:
        if (error.status, error.code) != (423, "video_media_b25_cutover_paused"):
            raise DispatchFenceError("b25_direct_guard_changed") from error
    else:
        raise DispatchFenceError("b25_direct_guard_missing")
    refuse_b25_cutover_media("a01-fence-control-slug")
    return {"slug": B25_CUTOVER_SLUG, "compiled_guard": True}


async def run(args: argparse.Namespace) -> dict[str, Any] | str:
    if args.job_id != PINNED_JOB_ID:
        raise DispatchFenceError("wrong_job_id")
    async with SessionFactory() as session:
        active_count = (
            select(func.count())
            .select_from(VideoMediaJob)
            .where(VideoMediaJob.status.in_(("queued", "submitted")))
            .scalar_subquery()
        )
        # One statement keeps the exact row and global active-media count on one DB snapshot.
        result = await session.execute(
            select(VideoMediaJob, active_count).where(VideoMediaJob.id == args.job_id)
        )
        record = result.one_or_none()
        if record is None:
            raise DispatchFenceError("job_missing")
        job, active_media_count = record
        # A submitted job must never be treated as an unspent queued request.
        expected_manifest(job)
        if args.action == "propose":
            return canonical_manifest(job)
        settings = get_settings()
        root = settings.video_work_dir
        if args.action == "validate":
            digest = inspect_manifest(job, args.manifest)
            enforced = False
            lock_absent: bool | None = None
            paid_intake: dict[str, Any] | None = None
        else:
            digest = inspect_installed_fence(job, root)
            enforced = True
            try:
                intake = inspect_intake(root)
            except IntakeFenceError as error:
                raise DispatchFenceError(f"paid_intake_{error.reason}") from error
            paid_intake = {
                "state": intake.state,
                "bootstrap_id": intake.bootstrap_id,
                "plan_sha256": intake.plan_sha256,
                "target_sha": intake.target_sha,
                "nonce_sha256": intake.nonce_sha256,
                "marker_sha256": intake.marker_sha256,
                "armed_sha256": intake.armed_sha256,
            }
            if active_media_count != 1:
                raise DispatchFenceError("active_media_count_changed")
            # The old API may already have entered _submit when an operator installs the
            # marker. A queued row by itself does not prove that no call is in flight.
            async with Redis.from_url(settings.redis_url, socket_timeout=5) as redis:
                lock_absent = not bool(await redis.exists(f"video-media:lock:{job.id}"))
                if getattr(args, "expect_operator_lock", False) and lock_absent:
                    raise DispatchFenceError("operator_lock_missing")
                if not getattr(args, "expect_operator_lock", False) and not lock_absent:
                    raise DispatchFenceError("media_job_lock_present")
        return {
            "schema_version": 1,
            "enforced": enforced,
            "fence_sha256": digest,
            "fence_path": str(fence_path(root)),
            "media_lock_absent": lock_absent,
            "operator_lock_expected": bool(getattr(args, "expect_operator_lock", False)),
            "active_media_count": active_media_count,
            "b25_direct_intake": b25_guard_receipt(),
            "paid_intake": paid_intake,
            "job": {
                "id": str(job.id),
                "slug": job.slug,
                "request_hash": job.request_hash,
                "kind": job.kind,
                "provider": job.provider,
                "model": job.model,
                "status": job.status,
                "vendor_ref": job.vendor_ref,
                "submitted_at": job.submitted_at.isoformat() if job.submitted_at else None,
            },
            "code": {
                "jobs_sha256": hashlib.sha256(
                    (Path(__file__).with_name("jobs.py")).read_bytes()
                ).hexdigest(),
                "dispatch_fence_sha256": hashlib.sha256(
                    (Path(__file__).with_name("dispatch_fence.py")).read_bytes()
                ).hexdigest(),
                "admin_api_sha256": hashlib.sha256(
                    (Path(__file__).with_name("admin_api.py")).read_bytes()
                ).hexdigest(),
                "cutover_intake_sha256": hashlib.sha256(
                    (Path(__file__).with_name("cutover_intake.py")).read_bytes()
                ).hexdigest(),
            },
        }


def main() -> int:
    args = parser().parse_args()
    try:
        result = asyncio.run(run(args))
    except DispatchFenceError as error:
        print(json.dumps({"error": "video_media_dispatch_fence_invalid", "reason": error.reason}))
        return 3
    except Exception as error:
        print(
            json.dumps(
                {"error": "video_media_dispatch_fence_unavailable", "reason": type(error).__name__}
            )
        )
        return 4
    if isinstance(result, str):
        print(result, end="")
    else:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
