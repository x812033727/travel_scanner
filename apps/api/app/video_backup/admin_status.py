"""Each video's backup as the worker reports it, and whether every one is in Drive: the videos
on YouTube and those ready to upload, so a finished video is in Drive before it is uploaded.

``video_projects.backup`` (migration 0135) is the worker's last report. The site does not take
the worker's "done" on trust alone: it counts the report's contents against what the owner's
language choice asks for (target.missing_files), and a backup that lacks a file is recorded as
partial, which keeps the video's files on the host (the worker's tidy waits for done). A
backup that was complete reads "stale" once the owner chooses another language or a fuller
tier, so the page never says done for less than the settings ask.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_backup import admin_settings as backup_settings
from app.video_backup.admin_settings import parse_time
from app.video_backup.schemas import (
    BackupState,
    BackupView,
    ExpectedParts,
    ReportIn,
    ReviewPackage,
    StatusView,
    WorkerConfig,
    WorkerProbe,
    WorkerVideo,
)
from app.video_backup.target import (
    PathInvalid,
    Target,
    as_dict,
    expected_parts,
    missing_files,
    normalise_path,
    remote_prefix,
    resolve_target,
)
from app.video_reviews.admin_service import language_states, locale_choices, ready_to_upload

# A backup should finish in the rounds after the upload; one queued longer is flagged.
OVERDUE_HOURS = 24
QUEUED: frozenset[str] = frozenset({"pending", "failed", "blocked_quota", "partial"})
STATES: tuple[BackupState, ...] = (
    "done",
    "stale",
    "pending",
    "failed",
    "blocked_quota",
    "partial",
    "not_queued",
    "off",
)


def _now() -> datetime:
    return datetime.now(UTC)


def _record(project: VideoProject) -> dict[str, Any]:
    return dict(project.backup) if isinstance(project.backup, dict) else {}


def _target(project: VideoProject, config: dict[str, Any]) -> Target:
    return resolve_target(
        project,
        tiers=backup_settings.tiers_of(config),
        folder_names=backup_settings.mapping_of(config, "folder_names"),
    )


def _int(value: Any) -> int | None:
    return value if type(value) is int and value >= 0 else None


def backup_view(project: VideoProject, config: dict[str, Any], now: datetime) -> BackupView:
    target = _target(project, config)
    record = _record(project)
    stored = record.get("state")
    copied_tier: Literal["basic", "full"] | None = (
        "basic"
        if record.get("tier") == "basic"
        else "full"
        if record.get("tier") == "full"
        else None
    )
    missing: list[str] = []
    if isinstance(record.get("missing"), list):
        missing = [item for item in record["missing"] if isinstance(item, str)]
    state: BackupState
    if target.tier == "off":
        state = "off"
    elif stored not in ("pending", "done", "failed", "blocked_quota", "partial"):
        state = "not_queued"
    else:
        state = stored
        if stored in ("done", "partial"):
            # Counted again against today's choice: a language chosen after the backup is missing.
            now_missing = missing_files(record.get("contents"), expected_parts(project))
            missing = sorted(set(missing) | set(now_missing))
            if stored == "done" and (
                now_missing or (target.tier == "full" and copied_tier != "full")
            ):
                state = "stale"
                if target.tier == "full" and copied_tier != "full":
                    missing.append("完整層級的 clips、keyframes、characters 等")
    queued_at = parse_time(record.get("queued_at"))
    return BackupView(
        slug=project.slug,
        title=project.title,
        youtube_video_id=project.youtube_video_id,
        series_key=target.series_key,
        folder=target.folder,
        tier=target.tier,
        copied_tier=copied_tier,
        state=state,
        complete=state == "done",
        bytes=_int(record.get("bytes")),
        files=_int(record.get("files")),
        files_hash=record.get("files_hash") if isinstance(record.get("files_hash"), str) else None,
        at=parse_time(record.get("at")),
        checked_at=parse_time(record.get("checked_at")),
        queued_at=queued_at,
        reported_at=parse_time(record.get("reported_at")),
        attempts=_int(record.get("attempts")) or 0,
        error=record.get("error") if isinstance(record.get("error"), str) else None,
        missing=missing,
        overdue=state in QUEUED
        and queued_at is not None
        and now - queued_at > timedelta(hours=OVERDUE_HOURS),
    )


async def ready_unuploaded(session: AsyncSession, slug: str | None = None) -> list[VideoProject]:
    """Videos not on YouTube yet that may be uploaded, by the review list's ready_to_upload rule
    (a Short needs only its upload confirmation). A renewed final cut supersedes the
    confirmation, so a video being revised is not among them. It lives here, not beside
    ready_to_upload, because admin_service.py is bound by the duration review receipt."""
    confirmed = (
        select(VideoReview.project_id, func.max(VideoReview.decided_at).label("decided_at"))
        .where(VideoReview.gate == "publish", VideoReview.status == "approved")
        .group_by(VideoReview.project_id)
        .subquery()
    )
    query = (
        select(VideoProject, confirmed.c.decided_at)
        .join(confirmed, confirmed.c.project_id == VideoProject.id)
        .where(VideoProject.youtube_video_id.is_(None), VideoProject.dropped_at.is_(None))
    )
    if slug is not None:
        query = query.where(VideoProject.slug == slug)
    rows = (await session.execute(query)).all()
    batches: dict[Any, list[VideoReview]] = {}
    if rows:
        reviews = await session.scalars(
            select(VideoReview).where(
                VideoReview.project_id.in_([project.id for project, _at in rows]),
                VideoReview.gate == "languages",
                VideoReview.status.in_(("pending", "approved")),
            )
        )
        for review in reviews:
            batches.setdefault(review.project_id, []).append(review)
    return [
        project
        for project, approved_at in rows
        if project.shorts_line is not None
        or ready_to_upload(
            project,
            approved_at,
            language_states(
                locale_choices(project), batches.get(project.id, []), project.dub_retries or {}
            ),
        )
    ]


async def _eligible(session: AsyncSession) -> list[VideoProject]:
    """Every video with a YouTube id and every one ready to upload, oldest first: those are the
    ones Drive must hold. One being revised drops out until it is ready again, so the worker
    copies its new files over the old ones only then (the old ones go to _舊版)."""
    rows = await session.scalars(
        select(VideoProject).where(VideoProject.youtube_video_id.is_not(None))
    )
    projects = [*rows.all(), *await ready_unuploaded(session)]
    return sorted(projects, key=lambda project: (project.created_at, project.slug))


async def status(session: AsyncSession, *, everything: bool = False) -> StatusView:
    row = await backup_settings.settings_row(session)
    config = backup_settings.config_of(row)
    enabled = backup_settings.enabled_of(row)
    now = _now()
    views = [backup_view(project, config, now) for project in await _eligible(session)]
    counts: dict[BackupState, int] = dict.fromkeys(STATES, 0)
    for item in views:
        counts[item.state] += 1
    return StatusView(
        enabled=enabled,
        path=backup_settings.path_of(config),
        uploaded=len(views),
        counts=counts,
        all_backed_up=enabled and all(item.state in ("done", "off") for item in views),
        overdue_hours=OVERDUE_HOURS,
        videos=[item for item in views if everything or item.state not in ("done", "off")],
    )


async def _project(session: AsyncSession, slug: str) -> VideoProject:
    project = await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
    if project is None:
        raise AppError(404, "video_backup_video_not_found", "找不到這支影片")
    return project


async def video_status(session: AsyncSession, slug: str) -> BackupView:
    project = await _project(session, slug)
    config = backup_settings.config_of(await backup_settings.settings_row(session))
    return backup_view(project, config, _now())


async def review_packages(
    session: AsyncSession, projects: list[VideoProject]
) -> dict[Any, ReviewPackage]:
    """Each imported long video's newest approved upload package, by project id.

    `import --publish` (tools/video/import/import.mjs) sends a package made on another machine,
    a cloud session's Colab drama for one: the host's video_work has none of its files, and the
    backup copies only what video_work holds. The worker fetches these from the review store
    first. A Short, or a package the worker or review-push made, is left out: those are in
    video_work already, or are not this command's layout."""
    ids = [project.id for project in projects if project.shorts_line is None]
    if not ids:
        return {}
    rows = await session.scalars(
        select(VideoReview)
        .where(
            VideoReview.project_id.in_(ids),
            VideoReview.gate == "publish",
            VideoReview.status == "approved",
        )
        .order_by(VideoReview.decided_at.desc(), VideoReview.created_at.desc())
    )
    packages: dict[Any, ReviewPackage] = {}
    seen: set[Any] = set()
    for review in rows:
        if review.project_id in seen:
            continue
        seen.add(review.project_id)
        payload = review.payload if isinstance(review.payload, dict) else {}
        if payload.get("imported") is True:
            packages[review.project_id] = ReviewPackage(
                review_id=str(review.id), content_sha256=review.content_sha256
            )
    return packages


async def worker_config(session: AsyncSession) -> WorkerConfig:
    row = await backup_settings.settings_row(session)
    config = backup_settings.config_of(row)
    problem = backup_settings.problem_of(row)
    path = backup_settings.path_of(config)
    lock = backup_settings.lock_of(config)
    pending = as_dict(config.get("test")) or None
    requested_at = parse_time(pending.get("requested_at")) if pending else None
    videos = []
    eligible = await _eligible(session)
    packages = await review_packages(session, eligible)
    for project in eligible:
        target = _target(project, config)
        videos.append(
            WorkerVideo(
                slug=project.slug,
                youtube_video_id=project.youtube_video_id,
                category=project.category,
                series_key=target.series_key,
                series_slug=project.series_slug,
                episode_number=project.episode_number,
                folder=target.folder,
                shared_folder=target.shared_folder,
                tier=target.tier,
                expected=ExpectedParts(**expected_parts(project)),
                backup=project.backup if isinstance(project.backup, dict) else None,
                review_package=packages.get(project.id),
            )
        )
    return WorkerConfig(
        enabled=backup_settings.enabled_of(row),
        path=path,
        lock_path=lock,
        remote_prefix=remote_prefix(path, lock) if problem is None else None,
        problem=problem,
        test=WorkerProbe(id=pending["id"], requested_at=requested_at)
        if pending and requested_at is not None
        else None,
        videos=videos,
    )


def _refuse_incomplete(payload: ReportIn) -> None:
    if payload.files_hash is None or payload.bytes is None or not payload.files:
        raise AppError(
            422,
            "video_backup_report_incomplete",
            "完成或部分完成的備份要附上 files_hash、bytes 與檔案數",
        )
    if payload.contents is None:
        raise AppError(422, "video_backup_report_incomplete", "完成或部分完成的備份要附上 contents")


async def report(
    session: AsyncSession, tool: VideoToolToken, slug: str, payload: ReportIn
) -> BackupView:
    """The worker's account of one video's backup. A "done" that lacks a file the owner's
    choice asks for is stored as partial, with what is missing."""
    project = await _project(session, slug)
    if project.youtube_video_id is None and not await ready_unuploaded(session, slug):
        # Neither on YouTube nor ready: never finished, or being revised since the round began.
        raise AppError(
            409, "video_backup_not_ready", "這支影片還沒上傳 YouTube，也還不能上架，不用備份"
        )
    row = await backup_settings.settings_row(session)
    config = backup_settings.config_of(row)
    target = _target(project, config)
    if target.tier == "off":
        raise AppError(409, "video_backup_tier_off", "這個系列設定為不備份")
    try:
        folder = normalise_path(payload.folder)
    except PathInvalid as error:
        raise AppError(422, "video_backup_folder_invalid", str(error)) from None
    if folder != target.folder:
        # The worker read the settings before the owner renamed the series; it reads them again.
        raise AppError(
            409,
            "video_backup_folder_changed",
            f"這支影片的備份資料夾是 {target.folder}，不是 {folder}；請重新讀取設定",
        )
    previous = _record(project)
    now = _now()
    record: dict[str, Any] = {
        **previous,
        "state": payload.state,
        "folder": folder,
        "tier": payload.tier,
        "attempts": payload.attempts,
        "error": payload.error,
        "reported_at": now.isoformat(),
    }
    if payload.state in ("done", "partial"):
        _refuse_incomplete(payload)
        assert payload.contents is not None
        contents = payload.contents.model_dump()
        missing = sorted(
            set(payload.missing) | set(missing_files(contents, expected_parts(project)))
        )
        changed = (
            previous.get("files_hash") != payload.files_hash or previous.get("state") != "done"
        )
        record.update(
            bytes=payload.bytes,
            files=payload.files,
            files_hash=payload.files_hash,
            contents=contents,
            missing=missing,
            checked_at=now.isoformat(),
        )
        if missing:
            record.update(
                state="partial",
                error=payload.error or f"雲端缺少 {len(missing)} 個檔案：{'、'.join(missing[:5])}",
            )
        else:
            record.update(state="done", error=None, attempts=0)
            if changed or not previous.get("at"):
                record["at"] = now.isoformat()
    elif payload.state == "pending":
        if previous.get("state") in (None, "done", "partial") or not previous.get("queued_at"):
            record["queued_at"] = now.isoformat()
    elif payload.state == "failed" and previous.get("state") != "failed":
        session.add(
            AdminAuditLog(
                actor_user_id=tool.created_by_user_id,
                action="video_backup_failed",
                target=f"video_backup:{slug}",
                metadata_json={"error": payload.error, "attempts": payload.attempts},
            )
        )
    record.setdefault("queued_at", now.isoformat())
    project.backup = record
    await backup_settings.record_space(session, payload.free_bytes, payload.total_bytes)
    await session.commit()
    return backup_view(project, config, now)
