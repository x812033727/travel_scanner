"""What /admin/videos does: the pipeline reports and submits, the owner decides.

A review is bound to the SHA-256 of what it shows (the brief, the timeline, the final cut, the
upload package). Submitting different content for the same gate supersedes the pending review;
submitting the same content again returns the review that exists, whatever its state, so a
rejected cut cannot come back as a fresh pending one without changing. Shorts final reviews
also bind the complete QA receipt; changed evidence creates a new review revision before
upload, and its publish review must name that approved final review. Files no live or decided
review refers to are deleted from the store. A video the owner dropped takes no more
submissions or decisions.

Once the owner has uploaded a video themselves and pasted its YouTube address (HANDS-OFF.md
§上傳包與「可以上架」), the row carries ``youtube_video_id`` and ``youtube_publish_at``; the
review files stay downloadable, and ``prune_published_previews`` deletes only the mp4 once the
upload confirmation and the publish time are both at least PREVIEW_RETENTION old.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_automation.judge import (
    PACKAGE_AUTO_APPROVED_NOTE,
    QA_AUTO_APPROVED_NOTE,
    SCRIPT_AUTO_APPROVED_NOTE,
    SHORTS_PACKAGE_AUTO_APPROVED_NOTE,
    SHORTS_QA_AUTO_APPROVED_NOTE,
    pick_choice,
    pick_reason,
    video_series_kind,
)
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaEpisode,
    VideoDramaSeries,
)
from app.video_automation.settings import (
    AUTO_APPROVED_NOTE,
    AUTO_APPROVED_STORYBOARD_NOTE,
    auto_approves_audio,
    auto_approves_final,
    auto_approves_script,
    auto_approves_storyboard,
    auto_picks_look,
    auto_picks_outline,
    look_pick_note,
)
from app.video_media.meter import SlugSpend, spend_by_slug
from app.video_reviews.schemas import (
    DUB_LOCALES,
    LOCALE_PARTS,
    YOUTUBE_VIDEO_ID_PATTERN,
    DecisionIn,
    DropIn,
    DubLocalesIn,
    LanguagePartOut,
    LocaleChoice,
    LocalesIn,
    ProjectIn,
    ProjectOut,
    ProjectSummary,
    ReviewFile,
    ReviewIn,
    ReviewOut,
)
from app.video_reviews.storage import ReviewStore, valid_slug
from app.video_shorts import costs as shorts_costs
from app.video_shorts import slots as shorts_slots
from app.video_shorts.settings import auto_approves_shorts
from app.video_youtube.state import public_state

LIVE = ("pending", "approved", "rejected")
# The list's cap, and how many public Shorts the Shorts tab gets at once: the public ones
# only grow, and the older ones are read from the numbers instead (docs/videos/SHORTS.md).
LIST_LIMIT = 200
PUBLIC_SHORTS_LIMIT = 60
# How long the mp4 of a video that is on YouTube stays in the review store, counted from the
# later of the upload confirmation's decision and the publish time (HANDS-OFF.md). The
# thumbnail, captions and descriptions are small and stay.
PREVIEW_RETENTION = timedelta(days=7)
YOUTUBE_ID = re.compile(YOUTUBE_VIDEO_ID_PATTERN)
YOUTUBE_HOSTS = frozenset(
    {"youtu.be", "youtube.com", "www.youtube.com", "m.youtube.com", "studio.youtube.com"}
)
# youtube.com/<kind>/<id>: shorts, embeds and live pages, and Studio's /video/<id>/edit.
YOUTUBE_PATH_KINDS = frozenset({"shorts", "embed", "live", "video", "v"})
# Gates where approving means choosing one of the offered options (an outline; a character sheet).
CHOICE_GATES = ("outline", "look")
CHOICE_PROMPTS = {"outline": "請從 {} 選一個大綱", "look": "請從 {} 選一張角色設定圖"}
# A languages batch with nothing for the owner to upload is approved as it arrives.
LANGUAGES_AUTO_APPROVED_NOTE = "這一批沒有要你上傳的配音，依規則自動核准"
EPOCH = datetime.min.replace(tzinfo=UTC)


def review_store(settings: Settings) -> ReviewStore:
    return ReviewStore(
        settings.video_review_dir,
        max_file_bytes=settings.video_review_max_file_bytes,
        max_total_bytes=settings.video_review_max_total_bytes,
    )


def outline_choices(payload: dict[str, Any]) -> list[str]:
    """The option keys an outline review offers (A, B, C), from its payload."""
    options = payload.get("options")
    if not isinstance(options, list):
        return []
    return [str(item["key"]) for item in options if isinstance(item, dict) and item.get("key")]


def decision_problem(review: VideoReview, decision: DecisionIn) -> str | None:
    """Why this decision cannot be recorded, or None."""
    if review.status != "pending":
        return "這一項已經決定過或被新版本取代"
    if decision.decision == "reject" and not (decision.note or "").strip():
        return "退回時請寫下原因，工具會把它帶回給撰稿與查核"
    choices = outline_choices(review.payload) if review.gate in CHOICE_GATES else []
    if decision.decision == "approve" and choices and decision.choice not in choices:
        return CHOICE_PROMPTS[review.gate].format("、".join(choices))
    return None


def locale_choices(project: VideoProject) -> dict[str, LocaleChoice]:
    """The owner's language choice as stored (docs/videos/LANGUAGES.md), empty for a shape no
    page wrote."""
    raw = project.locales if isinstance(project.locales, dict) else {}
    try:
        chosen = LocalesIn.model_validate({"locales": raw}).locales
    except ValueError:
        return {}
    return {str(locale): choice for locale, choice in chosen.items()}


def _part_state(value: Any) -> tuple[str | None, str | None]:
    """A part as a languages review reports it: "ready" or {"status": "skipped", "reason"}."""
    if isinstance(value, str):
        return value, None
    if isinstance(value, dict):
        status = value.get("status")
        reason = value.get("reason")
        return (status if isinstance(status, str) else None), (
            reason if isinstance(reason, str) else None
        )
    return None, None


def language_states(
    choices: dict[str, LocaleChoice], reviews: Iterable[VideoReview]
) -> dict[str, dict[str, LanguagePartOut]]:
    """Where each chosen part stands, from the languages reviews (docs/videos/LANGUAGES.md).

    The batches are read oldest first, so a later batch (the languages added after the first)
    speaks last for the parts it names and leaves the rest as they were. A part a batch reports
    "ready" or "skipped" (with the worker's reason) is that; a dub track "ready" in an approved
    batch is "uploaded", since approving the batch is how the owner says they uploaded it;
    a chosen part no batch has reported is "working". Sent-back batches count for nothing.
    """
    states: dict[str, dict[str, LanguagePartOut]] = {
        locale: {part: LanguagePartOut(state="working") for part in choice.chosen()}
        for locale, choice in choices.items()
    }
    batches = sorted(
        (
            review
            for review in reviews
            if review.gate == "languages" and review.status in ("pending", "approved")
        ),
        key=lambda review: review.created_at or EPOCH,
    )
    for review in batches:
        reported = review.payload.get("locales") if isinstance(review.payload, dict) else None
        if not isinstance(reported, dict):
            continue
        for locale, parts in reported.items():
            if locale not in states or not isinstance(parts, dict):
                continue
            fallback = parts.get("reason") if isinstance(parts.get("reason"), str) else None
            for part in LOCALE_PARTS:
                if part not in states[locale] or part not in parts:
                    continue
                state, reason = _part_state(parts[part])
                if state not in ("ready", "skipped"):
                    continue
                if state == "ready" and part == "dub" and review.status == "approved":
                    state = "uploaded"
                states[locale][part] = LanguagePartOut(
                    state=state, reason=(reason or fallback) if state == "skipped" else None
                )
    return states


def languages_need_owner(payload: dict[str, Any]) -> bool:
    """Whether a languages batch carries a dub track, the one part only the owner can upload."""
    reported = payload.get("locales") if isinstance(payload, dict) else None
    if not isinstance(reported, dict):
        return False
    return any(
        _part_state(parts.get("dub"))[0] == "ready"
        for parts in reported.values()
        if isinstance(parts, dict)
    )


def ready_to_upload(
    project: VideoProject,
    publish_approved_at: datetime | None,
    languages: dict[str, dict[str, LanguagePartOut]],
) -> bool:
    """Whether the video may be scheduled (docs/videos/LANGUAGES.md §上架流程): its upload
    confirmation approved, its languages decided and every chosen part ready, skipped or
    uploaded, no YouTube id yet, and not dropped."""
    if project.dropped_at is not None or project.youtube_video_id is not None:
        return False
    if publish_approved_at is None or project.locales_decided_at is None:
        return False
    return all(part.state != "working" for parts in languages.values() for part in parts.values())


def kept_files(reviews: Iterable[VideoReview]) -> set[str]:
    """Keep live previews and evidence for historical decisions, not abandoned drafts."""
    return {
        str(item["sha256"])
        for review in reviews
        if review.status in LIVE or review.decided_at is not None
        for item in review.files
        if isinstance(item, dict) and item.get("sha256")
    }


def _review_out(review: VideoReview) -> ReviewOut:
    return ReviewOut(
        id=review.id,
        gate=review.gate,
        subject=review.subject,
        content_sha256=review.content_sha256,
        summary=review.summary,
        payload=review.payload,
        files=[ReviewFile.model_validate(item) for item in review.files],
        status=review.status,
        choice=review.choice,
        note=review.note,
        decided_at=review.decided_at,
        created_at=review.created_at,
    )


def _summary(
    project: VideoProject,
    pending: int,
    spend: SlugSpend | None = None,
    publish_approved_at: datetime | None = None,
    languages: dict[str, dict[str, LanguagePartOut]] | None = None,
    *,
    compilation: bool = False,
    download_available: bool = False,
    hold: shorts_slots.Hold | None = None,
) -> dict[str, Any]:
    choices = locale_choices(project)
    states = languages if languages is not None else language_states(choices, [])
    is_short = project.shorts_line is not None
    return {
        "shorts_line": project.shorts_line,
        "shorts_series": project.shorts_series,
        "source_slug": project.source_slug,
        "shorts_state": (
            shorts_slots.state_of(project, pending, publish_approved_at, hold)
            if is_short
            else None
        ),
        "slot_at": hold.starts_at if is_short and hold is not None else None,
        "youtube_removed_at": project.youtube_removed_at,
        "compilation": compilation,
        "download_available": download_available,
        "slug": project.slug,
        "title": project.title,
        "format": project.format or "slides",
        "stage": project.stage,
        "checklist": project.checklist,
        "youtube_video_id": project.youtube_video_id,
        "youtube_publish_at": project.youtube_publish_at,
        "publish_approved_at": publish_approved_at,
        "last_synced_at": project.last_synced_at,
        "pending": pending,
        "source_guide": project.source_guide,
        "dropped_at": project.dropped_at,
        "dropped_note": project.dropped_note,
        "retry_request_id": project.retry_request_id,
        "retry_acknowledged_id": project.retry_acknowledged_id,
        "media_usd": spend.usd if spend else 0.0,
        "clip_seconds": spend.clip_seconds if spend else 0,
        "locales": choices,
        "locales_decided_at": project.locales_decided_at,
        "languages": states,
        # A Short's languages are the Shorts settings', not a choice made video by video, so
        # it waits for no decision on the language panel.
        "ready_to_upload": (
            publish_approved_at is not None
            and project.youtube_video_id is None
            and project.dropped_at is None
            if is_short
            else ready_to_upload(project, publish_approved_at, states)
        ),
        "dub_locales": [locale for locale, choice in choices.items() if choice.dub],
        "series_slug": project.series_slug,
        "episode_number": project.episode_number,
        "youtube_sync": public_state(project.youtube_sync),
    }


async def _project(session: AsyncSession, slug: str, *, lock: bool = False) -> VideoProject:
    statement = select(VideoProject).where(VideoProject.slug == slug)
    if lock:
        statement = statement.with_for_update().execution_options(populate_existing=True)
    project: VideoProject | None = (
        await session.scalar(statement)
        if valid_slug(slug)
        else None
    )
    if project is None:
        raise AppError(404, "video_project_not_found", "找不到這支影片")
    return project


def _refuse_dropped(project: VideoProject) -> None:
    if project.dropped_at is not None:
        raise AppError(409, "video_project_dropped", "站主已經放棄這支影片")


async def _reviews(
    session: AsyncSession, project: VideoProject, *, refresh: bool = False
) -> list[VideoReview]:
    statement = (
        select(VideoReview)
        .where(VideoReview.project_id == project.id)
        .order_by(VideoReview.created_at.desc())
    )
    if refresh:
        statement = statement.execution_options(populate_existing=True)
    rows = await session.scalars(statement)
    return list(rows)


async def upsert_project(
    session: AsyncSession, store: ReviewStore, slug: str, payload: ProjectIn
) -> ProjectOut:
    if not valid_slug(slug):
        raise AppError(422, "video_review_bad_slug", "影片代號只能用小寫英文、數字與連字號")
    now = datetime.now(UTC)
    project = await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
    if project is None:
        project = VideoProject(slug=slug, created_at=now)
        session.add(project)
    project.title = payload.title
    project.stage = payload.stage
    project.checklist = [item.model_dump() for item in payload.checklist]
    # The owner records the id on /admin/videos first; a report that does not carry it yet
    # (the worker reads it back a round later) must not clear it.
    if payload.youtube_video_id is not None:
        project.youtube_video_id = payload.youtube_video_id
    if payload.source_guide is not None:
        project.source_guide = payload.source_guide
    if payload.format is not None:
        project.format = payload.format
    if payload.series_slug is not None:
        project.series_slug = payload.series_slug
    if payload.episode_number is not None:
        project.episode_number = payload.episode_number
    if payload.shorts_line is not None:
        project.shorts_line = payload.shorts_line
    if payload.shorts_series is not None:
        project.shorts_series = payload.shorts_series
    if payload.source_slug is not None:
        project.source_slug = payload.source_slug
    # The card pipeline only makes Shorts, and the lists tell a Short by its content line: a
    # row in that format without one would show among the tutorials.
    if project.format == "shorts" and project.shorts_line is None:
        raise AppError(
            422,
            "video_shorts_line_missing",
            "Shorts 要帶內容線（shorts_line：lab、cut 或 drama）",
        )
    # A stale or unrelated report cannot consume a newer retry request.
    if payload.retry_acknowledged_id == project.retry_request_id:
        project.retry_acknowledged_id = payload.retry_acknowledged_id
    project.last_synced_at = now
    project.updated_at = now
    await _decide_story_locales(session, project, now)
    await session.commit()
    # A video on YouTube keeps its upload package for the owner to download; only the mp4 goes,
    # and only after PREVIEW_RETENTION (prune_published_previews), so nothing is deleted here
    # and the store is not touched.
    return await project_view(session, slug)


def publish_approved_at(reviews: Iterable[VideoReview]) -> datetime | None:
    """When the upload confirmation was last approved, or None while it was not."""
    decided = [
        review.decided_at
        for review in reviews
        if review.gate == "publish" and review.status == "approved" and review.decided_at
    ]
    return max(decided) if decided else None


def _confirmations() -> Any:
    """Per video, when its upload confirmation was last approved (a subquery)."""
    return (
        select(VideoReview.project_id, func.max(VideoReview.decided_at).label("decided_at"))
        .where(VideoReview.gate == "publish", VideoReview.status == "approved")
        .group_by(VideoReview.project_id)
        .subquery()
    )


async def project_view(session: AsyncSession, slug: str, work_dir: str | None = None) -> ProjectOut:
    project = await _project(session, slug)
    reviews = await _reviews(session, project)
    pending = sum(1 for review in reviews if review.status == "pending")
    spend = await spend_by_slug(session, [project.slug])
    languages = language_states(locale_choices(project), reviews)
    compiled = work_dir is not None and slug in await compilation_slugs(session)
    held = await shorts_slots.holds(session, [slug]) if project.shorts_line is not None else {}
    return ProjectOut(
        **_summary(
            project,
            pending,
            spend.get(project.slug),
            publish_approved_at(reviews),
            languages,
            compilation=compiled,
            download_available=compiled and download_file(work_dir, slug) is not None,
            hold=held.get(slug),
        ),
        reviews=[_review_out(review) for review in reviews],
    )


async def _language_batches(
    session: AsyncSession, projects: list[VideoProject]
) -> dict[Any, list[VideoReview]]:
    """The languages reviews of these videos, by project id, for the list's states."""
    if not projects:
        return {}
    rows = await session.scalars(
        select(VideoReview).where(
            VideoReview.project_id.in_([project.id for project in projects]),
            VideoReview.gate == "languages",
            VideoReview.status.in_(("pending", "approved")),
        )
    )
    batches: dict[Any, list[VideoReview]] = {}
    for review in rows:
        batches.setdefault(review.project_id, []).append(review)
    return batches


async def compilation_slugs(session: AsyncSession) -> set[str]:
    """The slugs of every compilation video a binge series started (docs/videos/BINGE.md)."""
    rows = await session.scalars(
        select(VideoDramaSeries.compilation_slug).where(
            VideoDramaSeries.compilation_slug.is_not(None)
        )
    )
    return {str(slug) for slug in rows.all() if slug}


def download_file(work_dir: str | None, slug: str) -> Path | None:
    """Where a compilation's 1080p cut sits on the worker's volume, when the API can see it."""
    if not work_dir or not valid_slug(slug):
        return None
    root = Path(work_dir)
    file = root / slug / "upload" / "final.mp4"
    try:
        if not file.is_file() or not file.resolve().is_relative_to(root.resolve()):
            return None
    except OSError:
        return None
    return file


async def download_path(session: AsyncSession, work_dir: str | None, slug: str) -> Path:
    """The compilation cut the owner downloads from /admin/videos, or a 404 that says why."""
    project = await _project(session, slug)
    _refuse_dropped(project)
    if slug not in await compilation_slugs(session):
        raise AppError(404, "video_download_not_found", "只有合集的成片從這裡下載")
    file = download_file(work_dir, slug)
    if file is None:
        raise AppError(404, "video_download_not_found", "成片還不在工人的工作區，或 API 沒有掛載它")
    return file


def _is_public(now: datetime) -> Any:
    """A video whose publish time is past: what the Shorts tab counts as public."""
    return and_(
        VideoProject.youtube_video_id.is_not(None), VideoProject.youtube_publish_at <= now
    )


def _not_public(now: datetime) -> Any:
    return or_(
        VideoProject.youtube_video_id.is_(None),
        VideoProject.youtube_publish_at.is_(None),
        VideoProject.youtube_publish_at > now,
    )


async def list_projects(
    session: AsyncSession,
    *,
    video_format: str | None = None,
    series_slug: str | None = None,
    shorts: str | None = None,
    state: str | None = None,
    limit: int | None = None,
    before: datetime | None = None,
    work_dir: str | None = None,
) -> list[ProjectSummary]:
    """The videos, newest first; a format or a series narrows them (docs/videos/SERIES.md),
    so a hundred episodes do not push the tutorials past the cap. With the worker's work
    directory, a compilation says whether its cut is there to download.

    ``shorts`` keeps the Shorts apart (docs/videos/SHORTS.md): ``exclude`` is every list that
    existed before them, ``only`` is the Shorts tab and the worker's Shorts round. With
    ``only`` the Shorts still to deal with all come, and of the public ones the latest
    PUBLIC_SHORTS_LIMIT; ``state`` keeps one state, and ``limit`` and ``before`` page through
    it (``before`` is the publish time of the last public Short read, or the last report of
    any other).
    """
    now = datetime.now(UTC)
    pending = (
        select(VideoReview.project_id, func.count().label("pending"))
        .where(VideoReview.status == "pending")
        .group_by(VideoReview.project_id)
        .subquery()
    )
    confirmed = _confirmations()
    statement = (
        select(VideoProject, func.coalesce(pending.c.pending, 0), confirmed.c.decided_at)
        .outerjoin(pending, pending.c.project_id == VideoProject.id)
        .outerjoin(confirmed, confirmed.c.project_id == VideoProject.id)
    )
    if video_format is not None:
        statement = statement.where(VideoProject.format == video_format)
    if series_slug is not None:
        statement = statement.where(VideoProject.series_slug == series_slug)
    if shorts == "exclude":
        statement = statement.where(VideoProject.shorts_line.is_(None))
    elif shorts == "only":
        statement = statement.where(VideoProject.shorts_line.is_not(None))
    cap = limit or LIST_LIMIT
    if shorts != "only":
        if before is not None:
            statement = statement.where(VideoProject.last_synced_at < before)
        listed = list(
            (
                await session.execute(
                    statement.order_by(VideoProject.last_synced_at.desc()).limit(cap)
                )
            ).all()
        )
    else:
        listed = []
        if state in (None, "published"):
            public = statement.where(_is_public(now))
            if before is not None and state == "published":
                public = public.where(VideoProject.youtube_publish_at < before)
            listed += list(
                (
                    await session.execute(
                        public.order_by(VideoProject.youtube_publish_at.desc()).limit(
                            limit or PUBLIC_SHORTS_LIMIT
                        )
                    )
                ).all()
            )
        if state != "published":
            waiting = statement.where(_not_public(now))
            if before is not None and state is not None:
                waiting = waiting.where(VideoProject.last_synced_at < before)
            # Read whole and cut after the state is known: a state is not a column, and the
            # Shorts that are not public yet are a few dozen.
            listed = (
                list(
                    (
                        await session.execute(
                            waiting.order_by(VideoProject.last_synced_at.desc()).limit(LIST_LIMIT)
                        )
                    ).all()
                )
                + listed
            )
    spend = await spend_by_slug(session, [project.slug for project, _count, _at in listed])
    batches = await _language_batches(session, [project for project, _count, _at in listed])
    compiled = await compilation_slugs(session) if work_dir is not None else set()
    held = await shorts_slots.holds(
        session, [project.slug for project, _count, _at in listed if project.shorts_line]
    )
    summaries = [
        ProjectSummary(
            **_summary(
                project,
                int(count),
                spend.get(project.slug),
                approved_at,
                language_states(locale_choices(project), batches.get(project.id, [])),
                compilation=project.slug in compiled,
                download_available=project.slug in compiled
                and download_file(work_dir, project.slug) is not None,
                hold=held.get(project.slug),
            )
        )
        for project, count, approved_at in listed
    ]
    if shorts == "only" and state is not None:
        summaries = [item for item in summaries if item.shorts_state == state][:cap]
    return summaries


def _same_qa(first: dict[str, Any], second: dict[str, Any]) -> bool:
    # Key order is irrelevant; JSON preserves booleans versus numbers and list order.
    return json.dumps(first.get("qa"), sort_keys=True, separators=(",", ":")) == json.dumps(
        second.get("qa"), sort_keys=True, separators=(",", ":")
    )


async def _short_revision_allowed(project: VideoProject) -> None:
    """Renew only before any uploader can have acted on the old approved package."""
    if (
        project.youtube_video_id is not None
        or project.youtube_upload_session is not None
        or (project.youtube_sync or {}).get("status") in ("queued", "running")
    ):
        raise AppError(
            409, "video_shorts_review_upload_started",
            "影片已開始上傳或同步，請先核對 YouTube 狀態；目前不能重新送審成片",
        )
    # The VPS sender takes the same project lock before staging or starting an upload.
    from app.video_youtube import vps
    from app.video_youtube.errors import Refused

    try:
        await vps.assert_idle(project.slug, upload=True)
    except Refused as error:
        raise AppError(error.status, error.code, error.detail) from error


def _supersede_short_reviews(
    session: AsyncSession,
    project: VideoProject,
    reviews: list[VideoReview],
    gates: tuple[str, ...],
    new_id: Any,
    now: datetime,
) -> None:
    for older in reviews:
        if older.gate not in gates or older.status not in LIVE:
            continue
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="video_review_superseded",
                target=f"video_review:{older.id}",
                metadata_json={
                    "slug": project.slug, "gate": older.gate,
                    "previous_status": older.status, "replacement_review_id": str(new_id),
                    "sha256": older.content_sha256, "revision": older.revision or 0,
                },
            )
        )
        older.status = "superseded"
        older.updated_at = now


async def submit_review(
    session: AsyncSession,
    store: ReviewStore,
    slug: str,
    payload: ReviewIn,
    token: VideoToolToken,
) -> ReviewOut:
    # All review writes take the project before a review lock, also used by the uploaders.
    project = await _project(session, slug, lock=True)
    _refuse_dropped(project)
    missing = [item.sha256 for item in payload.files if store.path(slug, item.sha256) is None]
    if missing:
        raise AppError(
            409, "video_review_files_missing", f"這些檔案還沒上傳完：{', '.join(missing)}"
        )
    reviews = await _reviews(session, project, refresh=True)
    same = next(
        (
            review
            for review in reviews
            if review.gate == payload.gate and review.content_sha256 == payload.content_sha256
        ),
        None,
    )
    now = datetime.now(UTC)
    short_gate = project.shorts_line is not None and payload.gate in ("final", "publish")
    revision = 0
    if short_gate:
        current = next(
            (row for row in reviews if row.gate == payload.gate and row.status in LIVE), None
        )
        if payload.gate == "publish":
            final = next(
                (row for row in reviews if row.gate == "final" and row.status in LIVE), None
            )
            if (
                final is None or final.status != "approved"
                or payload.payload.get("final_review_id") != str(final.id)
            ):
                raise AppError(
                    409, "video_shorts_final_review_stale",
                    "上傳包必須綁定目前已核准的成片審核，請重新執行 push",
                )
        matches = (
            current is not None and current.content_sha256 == payload.content_sha256
            and (
                _same_qa(current.payload, payload.payload)
                if payload.gate == "final"
                else current.payload.get("final_review_id")
                == payload.payload.get("final_review_id")
            )
        )
        same = current if matches else None
        if same is None:
            # Even a pending changed receipt gets a new id, so an owner looking at an
            # older page cannot approve evidence they have not seen.
            await _short_revision_allowed(project)
            revision = 1 + max(
                (row.revision or 0 for row in reviews
                 if row.gate == payload.gate and row.content_sha256 == payload.content_sha256),
                default=-1,
            )
    if same is not None and same.status != "pending":
        await session.commit()  # release the project lock on an idempotent resend
        return _review_out(same)
    if same is not None:
        # The same file sent again while it waits: the newer payload, summary and files
        # replace the older ones (a quality check run after the fact, captions fixed without
        # touching the video), and the rules below run again on them (HANDS-OFF.md).
        same.summary = payload.summary
        same.payload = payload.payload
        same.files = [item.model_dump() for item in payload.files]
        same.updated_at = now
        review = same
    else:
        # A new submission replaces the pending one of the same gate and subject: one look
        # review per character stays open at a time, and the older gates (subject None)
        # behave as before.
        for older in reviews:
            if not short_gate and (
                older.gate == payload.gate
                and older.status == "pending"
                and older.subject == payload.subject
            ):
                older.status = "superseded"
                older.updated_at = now
        review = VideoReview(
            id=uuid4(),
            project_id=project.id,
            gate=payload.gate,
            subject=payload.subject,
            content_sha256=payload.content_sha256,
            revision=revision,
            summary=payload.summary,
            payload=payload.payload,
            files=[item.model_dump() for item in payload.files],
            status="pending",
            submitted_by_token_id=token.id,
            created_at=now,
            updated_at=now,
        )
        if short_gate:
            gates = ("final", "publish") if payload.gate == "final" else ("publish",)
            _supersede_short_reviews(session, project, reviews, gates, review.id, now)
            if payload.gate == "final":
                await shorts_slots.release(session, slug, now)
        session.add(review)
    # The owner chose on 2026-09-25 to let Jev's check stand for them on the narration: when it
    # passed every line and the setting is on, the review is decided as it arrives.
    auto_note = None
    # A drama reads its own switches (docs/videos/DRAMA-FLOW.md §一); a project row from before
    # formats existed reads as a tutorial.
    video_format = project.format or "slides"
    series_slug = project.series_slug
    if payload.gate == "audio" and await auto_approves_audio(
        session, payload.payload, video_format
    ):
        auto_note = AUTO_APPROVED_NOTE
    # A drama's storyboard may stand on the judge's scores when the owner turned that on, or
    # when the series is hands-off (docs/videos/BINGE.md); an illustrated slides video's reads
    # its own switch (docs/videos/ILLUSTRATED.md).
    elif payload.gate == "storyboard" and await auto_approves_storyboard(
        session, payload.payload, series_slug, video_format
    ):
        auto_note = AUTO_APPROVED_STORYBOARD_NOTE
    # A character's sheet is picked by the judge's score when the owner turned that on.
    elif payload.gate == "look" and await auto_picks_look(session, payload.payload, series_slug):
        auto_note = look_pick_note(payload.payload)
        review.choice = str(payload.payload.get("suggested"))
    # An episode's screenplay stands on the checker's coverage on a hands-off series.
    elif payload.gate == "script" and await auto_approves_script(
        session, series_slug, payload.payload
    ):
        auto_note = SCRIPT_AUTO_APPROVED_NOTE
    # The owner decided on 2026-09-27 (docs/videos/HANDS-OFF.md) that Jev chooses the outline
    # and that a final cut and its upload confirmation stand on the automatic checks.
    elif payload.gate == "outline" and await auto_picks_outline(session, payload.payload):
        auto_note = pick_reason(payload.payload)
        review.choice = pick_choice(payload.payload)
    # A Short is held to its own twelve checks and reads its own switch
    # (docs/videos/SHORTS.md §自動品管); a long video's report never approves one, so the
    # rule below is not asked about a Short at all.
    elif payload.gate in ("final", "publish") and project.shorts_line is not None:
        if await auto_approves_shorts(
            session, payload.gate, payload.payload, payload.content_sha256
        ):
            auto_note = (
                SHORTS_QA_AUTO_APPROVED_NOTE
                if payload.gate == "final"
                else SHORTS_PACKAGE_AUTO_APPROVED_NOTE
            )
    elif payload.gate in ("final", "publish") and await auto_approves_final(
        session,
        payload.gate,
        payload.payload,
        payload.content_sha256,
        video_format,
        compilation=slug in await compilation_slugs(session),
    ):
        auto_note = QA_AUTO_APPROVED_NOTE if payload.gate == "final" else PACKAGE_AUTO_APPROVED_NOTE
    # A batch of languages waits for the owner only for a dub track they must upload in Studio;
    # descriptions and captions the site sends itself (docs/videos/LANGUAGES.md).
    elif payload.gate == "languages" and not languages_need_owner(payload.payload):
        auto_note = LANGUAGES_AUTO_APPROVED_NOTE
    if auto_note is not None:
        review.status = "approved"
        review.note = auto_note
        review.decided_at = now
        session.add(
            AdminAuditLog(
                actor_user_id=None,
                action="video_review_auto_approved",
                target=f"video_review:{review.id}",
                metadata_json={"slug": slug, "gate": review.gate, "sha256": review.content_sha256},
            )
        )
        await _short_approved(session, project, review, now)
    project.last_synced_at = now
    await session.commit()
    store.keep_only(slug, kept_files([*reviews, review]))
    return _review_out(review)


async def _short_approved(
    session: AsyncSession, project: VideoProject, review: VideoReview, now: datetime
) -> None:
    """What follows a Short's approval, whoever gave it (docs/videos/SHORTS.md): the final
    cut's reported usage goes into the ledger, and an approved upload package takes the Short
    to its slot, or to the library while the run has none for it. The caller commits."""
    if project.shorts_line is None:
        return
    if review.gate == "final":
        await shorts_costs.record_usage(
            session, project.slug, review.payload, review.content_sha256, now
        )
        await shorts_costs.record_media(session, project.slug, now)
    elif review.gate == "publish":
        await shorts_slots.assign_approved(session, project, now)


async def decide(
    session: AsyncSession, slug: str, review_id: Any, user: User, decision: DecisionIn
) -> ReviewOut:
    project = await _project(session, slug, lock=True)
    _refuse_dropped(project)
    review = await session.scalar(
        select(VideoReview)
        .where(VideoReview.id == review_id, VideoReview.project_id == project.id)
        .with_for_update()
        .execution_options(populate_existing=True)
    )
    if review is None:
        raise AppError(404, "video_review_not_found", "找不到這一項審核")
    problem = decision_problem(review, decision)
    if problem:
        raise AppError(409, "video_review_not_decidable", problem)
    now = datetime.now(UTC)
    review.status = "approved" if decision.decision == "approve" else "rejected"
    review.choice = decision.choice if review.gate in CHOICE_GATES else None
    review.note = (decision.note or "").strip() or None
    review.decided_at = now
    review.decided_by_user_id = user.id
    review.updated_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action=f"video_review_{review.status}",
            target=f"video_review:{review.id}",
            metadata_json={
                "slug": slug,
                "gate": review.gate,
                "sha256": review.content_sha256,
                "choice": review.choice,
            },
        )
    )
    if review.status == "approved":
        await _short_approved(session, project, review, now)
    await session.commit()
    return _review_out(review)


async def drop_project(
    session: AsyncSession, store: ReviewStore, slug: str, user: User, payload: DropIn
) -> ProjectOut:
    """Stop a video for good: nothing waits on the owner any more and its previews go.

    Its row stays, so the next automatic draft still sees its topic as made.
    """
    project = await _project(session, slug)
    if project.dropped_at is not None:
        return await project_view(session, slug)
    now = datetime.now(UTC)
    for review in await _reviews(session, project):
        if review.status == "pending":
            review.status = "superseded"
            review.updated_at = now
    project.dropped_at = now
    project.dropped_note = payload.note.strip()
    project.dropped_by_user_id = user.id
    project.updated_at = now
    if project.shorts_line is not None:
        # A dropped Short leaves its slot to the next one in the library.
        await shorts_slots.release(session, slug, now)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_project_dropped",
            target=f"video_project:{project.id}",
            metadata_json={"slug": slug},
        )
    )
    await _skip_abandoned_episode(session, project, user, now)
    await session.commit()
    store.keep_only(slug, set())
    return await project_view(session, slug)


async def _episode_of(
    session: AsyncSession, project: VideoProject
) -> tuple[VideoDramaEpisode, VideoDramaSeries] | None:
    """The episode this video is being made as and its series, both locked, or None.

    Only a video that reports itself as an episode is looked up (a Short or a tutorial never
    is one); the episode is then the server's own row whose slug is the video's. The series is
    locked before the episode, the order app.video_automation.series takes them in.
    """
    if project.series_slug is None or project.shorts_line is not None:
        return None
    series = await session.scalar(
        select(VideoDramaSeries)
        .join(VideoDramaEpisode, VideoDramaEpisode.series_id == VideoDramaSeries.id)
        .where(VideoDramaEpisode.slug == project.slug)
        .with_for_update(of=VideoDramaSeries)
    )
    if series is None:
        return None
    episode = await session.scalar(
        select(VideoDramaEpisode)
        .where(VideoDramaEpisode.series_id == series.id, VideoDramaEpisode.slug == project.slug)
        .with_for_update()
    )
    return None if episode is None else (episode, series)


async def _skip_abandoned_episode(
    session: AsyncSession, project: VideoProject, user: User, now: datetime
) -> None:
    """Skip the episode a dropped video was being made as (docs/videos/STORY.md §伺服器).

    Nothing else will make it under this slug, and a started one would hold its place in
    ``series_max_in_flight`` for ever. Every kind of series: the next episode of a long series
    waits for the one before to be done or skipped, so it may start now, as it may after the
    owner skips an episode on the series page. An episode already done stays done. When it was
    the series' last open episode the series finishes, as ``skip_episode`` has it. The caller
    commits.
    """
    # Imported here: app.video_automation.series imports this module.
    from app.video_automation.series import EPISODE_OPEN, finish_if_complete

    found = await _episode_of(session, project)
    if found is None:
        return
    episode, series = found
    if episode.status not in EPISODE_OPEN:
        return
    episode.status = "skipped"
    episode.updated_at = now
    episodes = await session.scalars(
        select(VideoDramaEpisode).where(VideoDramaEpisode.series_id == series.id)
    )
    finish_if_complete(series, list(episodes), now)
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_series_episode_skipped",
            target=f"video-series:{series.slug}",
            metadata_json={"number": episode.number, "dropped_video": project.slug},
        )
    )


async def _apply_locales(
    session: AsyncSession, project: VideoProject, user: User, payload: LocalesIn
) -> None:
    """Store the owner's language choice, note when they first decided, and log the change."""
    if (project.format or "slides") == "drama" and any(
        choice.dub for choice in payload.locales.values()
    ):
        raise AppError(
            422,
            "video_locales_dub_not_for_drama",
            "漫劇的配音是第二期（docs/videos/DUBS.md），這裡先只能選標題說明與 CC",
        )
    chosen: dict[str, Any] = {
        locale: choice.model_dump() for locale, choice in payload.locales.items()
    }
    if chosen == dict(project.locales or {}) and project.locales_decided_at is not None:
        return
    _record_locales(session, project, chosen, datetime.now(UTC), user)
    await session.commit()


def _record_locales(
    session: AsyncSession,
    project: VideoProject,
    chosen: dict[str, Any],
    now: datetime,
    actor: User | None,
    marks: dict[str, str] | None = None,
) -> None:
    """Store a language choice, note when it was first decided, and log it as
    ``video_locales_set``: the owner's, or with no actor and ``marks`` saying so, the server's
    (``_decide_story_locales``). The caller commits."""
    project.locales = chosen
    project.locales_decided_at = project.locales_decided_at or now
    project.updated_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=actor.id if actor is not None else None,
            action="video_locales_set",
            target=f"video_project:{project.id}",
            metadata_json={"slug": project.slug, "locales": chosen, **(marks or {})},
        )
    )


async def _decide_story_locales(
    session: AsyncSession, project: VideoProject, now: datetime
) -> None:
    """A brand story's languages, decided by the server when its video first reports
    (docs/videos/STORY.md §伺服器).

    A story is hands-off: nobody would choose its languages, and a video without a decision is
    never ready to upload. The server writes what the language panel's "tick the defaults"
    gives a drama, the settings' ``drama_caption_locales`` with titles, descriptions and
    captions and no dub, as the same record the owner's save writes, with the server as its
    author. Once only, and never over a decision; the owner may still change it on the panel.
    A video of any other kind still waits for the owner. The caller commits.
    """
    if project.locales_decided_at is not None or project.dropped_at is not None:
        return
    if project.series_slug is None or project.shorts_line is not None:
        return
    if await video_series_kind(session, project.slug) != "story":
        return
    settings = await session.scalar(
        select(VideoAutomationSettings).where(VideoAutomationSettings.id == 1)
    )
    ticked = settings.drama_caption_locales if settings is not None else []
    chosen: dict[str, Any] = {
        locale: LocaleChoice(metadata=True, captions=True).model_dump()
        for locale in DUB_LOCALES
        if locale in ticked
    }
    # A project first seen in this report gets its id when it is written.
    await session.flush()
    _record_locales(
        session,
        project,
        chosen,
        now,
        None,
        {"decided_by": "server", "from": "drama_caption_locales"},
    )


async def retry_project(session: AsyncSession, slug: str, user: User) -> ProjectOut:
    """Queue one retry for a blocked video; repeated clicks return the same request."""
    if not valid_slug(slug):
        raise AppError(404, "video_project_not_found", "找不到這支影片")
    project = await session.scalar(
        select(VideoProject).where(VideoProject.slug == slug).with_for_update()
    )
    if project is None:
        raise AppError(404, "video_project_not_found", "找不到這支影片")
    _refuse_dropped(project)
    if project.stage != "blocked":
        raise AppError(409, "video_retry_not_blocked", "只有卡住的影片可以重試")
    if project.retry_request_id == project.retry_acknowledged_id:
        project.retry_request_id = uuid4()
        project.updated_at = datetime.now(UTC)
        session.add(
            AdminAuditLog(
                actor_user_id=user.id,
                action="video_project_retry_requested",
                target=f"video_project:{project.id}",
                metadata_json={"slug": slug, "request_id": str(project.retry_request_id)},
            )
        )
        await session.commit()
    return await project_view(session, slug)


async def set_locales(
    session: AsyncSession, slug: str, user: User, payload: LocalesIn
) -> ProjectOut:
    """The owner decides a video's languages on the language panel (docs/videos/LANGUAGES.md).

    Every video is made in Traditional Chinese; here the owner says which of en, ja, ko and
    zh-CN to add and what of each. An empty choice is a decision too ("only Traditional
    Chinese"), and the first save of either kind is what lets the video go up. The worker makes
    only what was chosen, once the final cut is approved; a drama takes no dub yet. The choice is
    the owner's: the pipeline's reports never carry one, and a dropped video takes none. Only a
    brand story, which runs without the owner, has the server decide from the settings when its
    video first reports (``_decide_story_locales``); the owner may change that here too.
    """
    project = await _project(session, slug)
    _refuse_dropped(project)
    await _apply_locales(session, project, user, payload)
    return await project_view(session, slug)


async def set_dub_locales(
    session: AsyncSession, slug: str, user: User, payload: DubLocalesIn
) -> ProjectOut:
    """The dub checkboxes of a page from before the language panel: a ticked language gets all
    three parts, an unticked one loses its dub and keeps the rest (docs/videos/DUBS.md)."""
    project = await _project(session, slug)
    _refuse_dropped(project)
    current = locale_choices(project)
    merged: dict[str, LocaleChoice] = {}
    for locale in DUB_LOCALES:
        choice = current.get(locale, LocaleChoice())
        if locale in payload.locales:
            choice = LocaleChoice(metadata=True, captions=True, dub=True)
        elif choice.dub:
            choice = LocaleChoice(metadata=choice.metadata, captions=choice.captions, dub=False)
        merged[locale] = choice
    await _apply_locales(session, project, user, LocalesIn.model_validate({"locales": merged}))
    return await project_view(session, slug)


async def file_for_admin(
    session: AsyncSession, store: ReviewStore, slug: str, sha256: str
) -> tuple[Any, str]:
    """The path and content type of a file some review of this video shows."""
    project = await _project(session, slug)
    for review in await _reviews(session, project):
        for item in review.files:
            if isinstance(item, dict) and item.get("sha256") == sha256:
                path = store.path(slug, sha256)
                if path is None:
                    break
                return path, str(item["content_type"])
    raise AppError(404, "video_review_file_not_found", "這個檔案已經不在審核區")


# --- on YouTube: the owner's link, and what the store keeps afterwards ---------------------------


def youtube_video_id(value: str) -> str | None:
    """The eleven-character id in what the owner pasted, or None when it names no video.

    Takes ``https://youtu.be/<id>``, ``https://www.youtube.com/watch?v=<id>`` (other parameters
    allowed), ``https://youtube.com/shorts/<id>``, ``https://studio.youtube.com/video/<id>/edit``
    and the bare id. Anything on another host is refused, so a pasted link cannot record an id
    that is not YouTube's.
    """
    text = value.strip()
    if YOUTUBE_ID.fullmatch(text):
        return text
    try:
        parsed = urlsplit(text if "://" in text else f"https://{text}")
        host = (parsed.hostname or "").lower()
    except ValueError:
        return None
    if parsed.scheme not in ("http", "https") or host not in YOUTUBE_HOSTS:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    candidate: str | None = None
    if host == "youtu.be":
        candidate = parts[0] if parts else None
    elif parts[:1] == ["watch"]:
        candidate = next(iter(parse_qs(parsed.query).get("v", [])), None)
    elif len(parts) >= 2 and parts[0] in YOUTUBE_PATH_KINDS:
        candidate = parts[1]
    return candidate if candidate and YOUTUBE_ID.fullmatch(candidate) else None


async def link_youtube(
    session: AsyncSession,
    slug: str,
    user: User,
    video_id: str,
    publish_at: datetime | None,
) -> ProjectOut:
    """The owner uploaded the final cut in Studio: record the video's id and when it goes public.

    Pasting again overwrites (a wrong link is corrected the same way); the worker reads the id
    back on its next round and writes it into the work directory's video.json.
    """
    if publish_at is not None and publish_at.tzinfo is None:
        raise AppError(422, "video_youtube_publish_at_naive", "上架時間要帶時區")
    project = await _project(session, slug)
    _refuse_dropped(project)
    now = datetime.now(UTC)
    project.youtube_video_id = video_id
    project.youtube_publish_at = publish_at
    project.updated_at = now
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_youtube_linked",
            target=f"video_project:{slug}",
            metadata_json={
                "slug": slug,
                "youtube_video_id": video_id,
                "publish_at": publish_at.isoformat() if publish_at else None,
            },
        )
    )
    await session.commit()
    return await project_view(session, slug)


def _is_video(item: Any) -> bool:
    return isinstance(item, dict) and (
        item.get("content_type") == "video/mp4" or item.get("role") == "final"
    )


async def _published_before(session: AsyncSession, cutoff: datetime) -> list[VideoProject]:
    """Videos on YouTube whose upload confirmation was approved on or before ``cutoff``."""
    confirmed = _confirmations()
    rows = await session.scalars(
        select(VideoProject)
        .join(confirmed, confirmed.c.project_id == VideoProject.id)
        .where(VideoProject.youtube_video_id.is_not(None), confirmed.c.decided_at <= cutoff)
    )
    return list(rows)


async def prune_published_previews(
    session: AsyncSession, store: ReviewStore, now: datetime | None = None
) -> dict[str, list[str]]:
    """Delete the mp4 files of videos that have been on YouTube for PREVIEW_RETENTION.

    The rule (HANDS-OFF.md §上傳包與「可以上架」): the video has a ``youtube_video_id``, its
    upload confirmation was approved at least PREVIEW_RETENTION ago and, when the owner set a
    publish time, that time is also at least PREVIEW_RETENTION past. Only files that are
    ``video/mp4`` or play the ``final`` role go; the thumbnail, captions and descriptions stay
    so the owner can still fetch them. Idempotent and cheap, so the list page calls it: a video
    whose mp4 is already gone costs one stat per file. Returns what was removed, by slug.
    """
    now = now or datetime.now(UTC)
    cutoff = now - PREVIEW_RETENTION
    removed: dict[str, list[str]] = {}
    for project in await _published_before(session, cutoff):
        if project.youtube_publish_at is not None and project.youtube_publish_at > cutoff:
            continue
        reviews = await _reviews(session, project)
        videos = {
            str(item["sha256"])
            for review in reviews
            for item in review.files
            if _is_video(item) and item.get("sha256")
        }
        if not any(store.path(project.slug, sha256) is not None for sha256 in videos):
            continue
        gone = store.keep_only(project.slug, kept_files(reviews) - videos)
        if gone:
            removed[project.slug] = gone
    return removed
