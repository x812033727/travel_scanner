"""What /admin/videos does: the pipeline reports and submits, the owner decides.

A review is bound to the SHA-256 of what it shows (the brief, the timeline, the final cut, the
upload package). Submitting different content for the same gate supersedes the pending review;
submitting the same content again returns the review that exists, whatever its state, so a
rejected cut cannot come back as a fresh pending one without changing. Files no live review
refers to are deleted from the store. A video the owner dropped takes no more submissions or
decisions.

Once the owner has uploaded a video themselves and pasted its YouTube address (HANDS-OFF.md
§上傳包與「可以上架」), the row carries ``youtube_video_id`` and ``youtube_publish_at``; the
review files stay downloadable, and ``prune_published_previews`` deletes only the mp4 once the
upload confirmation and the publish time are both at least PREVIEW_RETENTION old.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit
from uuid import uuid4

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_automation.judge import (
    PACKAGE_AUTO_APPROVED_NOTE,
    QA_AUTO_APPROVED_NOTE,
    SCRIPT_AUTO_APPROVED_NOTE,
    pick_choice,
    pick_reason,
)
from app.video_automation.models import VideoDramaSeries
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
    YOUTUBE_VIDEO_ID_PATTERN,
    DecisionIn,
    DropIn,
    DubLocalesIn,
    ProjectIn,
    ProjectOut,
    ProjectSummary,
    ReviewFile,
    ReviewIn,
    ReviewOut,
)
from app.video_reviews.storage import ReviewStore, valid_slug

LIVE = ("pending", "approved", "rejected")
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


def kept_files(reviews: Iterable[VideoReview]) -> set[str]:
    """Files a live review still shows; everything else in the project's store can go."""
    return {
        str(item["sha256"])
        for review in reviews
        if review.status in LIVE
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
    compilation: bool = False,
    download_available: bool = False,
) -> dict[str, Any]:
    return {
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
        "media_usd": spend.usd if spend else 0.0,
        "clip_seconds": spend.clip_seconds if spend else 0,
        "dub_locales": list(project.dub_locales or []),
        "series_slug": project.series_slug,
        "episode_number": project.episode_number,
    }


async def _project(session: AsyncSession, slug: str) -> VideoProject:
    project: VideoProject | None = (
        await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
        if valid_slug(slug)
        else None
    )
    if project is None:
        raise AppError(404, "video_project_not_found", "找不到這支影片")
    return project


def _refuse_dropped(project: VideoProject) -> None:
    if project.dropped_at is not None:
        raise AppError(409, "video_project_dropped", "站主已經放棄這支影片")


async def _reviews(session: AsyncSession, project: VideoProject) -> list[VideoReview]:
    rows = await session.scalars(
        select(VideoReview)
        .where(VideoReview.project_id == project.id)
        .order_by(VideoReview.created_at.desc())
    )
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
    project.last_synced_at = now
    project.updated_at = now
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
    compiled = work_dir is not None and slug in await compilation_slugs(session)
    return ProjectOut(
        **_summary(
            project,
            pending,
            spend.get(project.slug),
            publish_approved_at(reviews),
            compilation=compiled,
            download_available=compiled and download_file(work_dir, slug) is not None,
        ),
        reviews=[_review_out(review) for review in reviews],
    )


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


async def list_projects(
    session: AsyncSession,
    *,
    video_format: str | None = None,
    series_slug: str | None = None,
    limit: int = 200,
    work_dir: str | None = None,
) -> list[ProjectSummary]:
    """The videos, newest first; a format or a series narrows them (docs/videos/SERIES.md),
    so a hundred episodes do not push the tutorials past the cap. With the worker's work
    directory, a compilation says whether its cut is there to download."""
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
    rows = await session.execute(
        statement.order_by(VideoProject.last_synced_at.desc()).limit(limit)
    )
    listed = list(rows.all())
    spend = await spend_by_slug(session, [project.slug for project, _count, _at in listed])
    compiled = await compilation_slugs(session) if work_dir is not None else set()
    return [
        ProjectSummary(
            **_summary(
                project,
                int(count),
                spend.get(project.slug),
                approved_at,
                compilation=project.slug in compiled,
                download_available=project.slug in compiled
                and download_file(work_dir, project.slug) is not None,
            )
        )
        for project, count, approved_at in listed
    ]


async def submit_review(
    session: AsyncSession,
    store: ReviewStore,
    slug: str,
    payload: ReviewIn,
    token: VideoToolToken,
) -> ReviewOut:
    project = await _project(session, slug)
    _refuse_dropped(project)
    missing = [item.sha256 for item in payload.files if store.path(slug, item.sha256) is None]
    if missing:
        raise AppError(
            409, "video_review_files_missing", f"這些檔案還沒上傳完：{', '.join(missing)}"
        )
    reviews = await _reviews(session, project)
    same = next(
        (
            review
            for review in reviews
            if review.gate == payload.gate and review.content_sha256 == payload.content_sha256
        ),
        None,
    )
    now = datetime.now(UTC)
    if same is not None and same.status != "pending":
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
            if (
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
            summary=payload.summary,
            payload=payload.payload,
            files=[item.model_dump() for item in payload.files],
            status="pending",
            submitted_by_token_id=token.id,
            created_at=now,
            updated_at=now,
        )
        session.add(review)
    # The owner chose on 2026-09-25 to let Jev's check stand for them on the narration: when it
    # passed every line and the setting is on, the review is decided as it arrives.
    auto_note = None
    series_slug = project.series_slug
    if payload.gate == "audio" and await auto_approves_audio(session, payload.payload):
        auto_note = AUTO_APPROVED_NOTE
    # A drama's storyboard may stand on the judge's scores when the owner turned that on, or
    # when the series is hands-off (docs/videos/BINGE.md).
    elif payload.gate == "storyboard" and await auto_approves_storyboard(
        session, payload.payload, series_slug
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
    elif payload.gate in ("final", "publish") and await auto_approves_final(
        session,
        payload.gate,
        payload.payload,
        payload.content_sha256,
        compilation=slug in await compilation_slugs(session),
    ):
        auto_note = QA_AUTO_APPROVED_NOTE if payload.gate == "final" else PACKAGE_AUTO_APPROVED_NOTE
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
    project.last_synced_at = now
    await session.commit()
    store.keep_only(slug, kept_files([*reviews, review]))
    return _review_out(review)


async def decide(
    session: AsyncSession, slug: str, review_id: Any, user: User, decision: DecisionIn
) -> ReviewOut:
    project = await _project(session, slug)
    _refuse_dropped(project)
    review = await session.scalar(
        select(VideoReview)
        .where(VideoReview.id == review_id, VideoReview.project_id == project.id)
        .with_for_update()
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
    session.add(
        AdminAuditLog(
            actor_user_id=user.id,
            action="video_project_dropped",
            target=f"video_project:{project.id}",
            metadata_json={"slug": slug},
        )
    )
    await session.commit()
    store.keep_only(slug, set())
    return await project_view(session, slug)


async def set_dub_locales(
    session: AsyncSession, slug: str, user: User, payload: DubLocalesIn
) -> ProjectOut:
    """The owner picks which languages this video gets dubbed in (docs/videos/DUBS.md).

    Every video is made in Traditional Chinese; the worker makes a track for each language chosen
    here once the final cut is approved, and the owner uploads them in YouTube Studio. The choice
    is the owner's alone: the pipeline's reports never touch it, and a dropped video takes none.
    """
    project = await _project(session, slug)
    _refuse_dropped(project)
    chosen: list[str] = list(payload.locales)
    if chosen != list(project.dub_locales or []):
        project.dub_locales = chosen
        project.updated_at = datetime.now(UTC)
        session.add(
            AdminAuditLog(
                actor_user_id=user.id,
                action="video_dub_locales_set",
                target=f"video_project:{project.id}",
                metadata_json={"slug": slug, "locales": chosen},
            )
        )
        await session.commit()
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
