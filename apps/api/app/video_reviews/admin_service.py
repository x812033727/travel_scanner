"""What /admin/videos does: the pipeline reports and submits, the owner decides.

A review is bound to the SHA-256 of what it shows (the brief, the timeline, the final cut, the
upload package). Submitting different content for the same gate supersedes the pending review;
submitting the same content again returns the review that exists, whatever its state, so a
rejected cut cannot come back as a fresh pending one without changing. Files no live review
refers to are deleted from the store.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_reviews.schemas import (
    DecisionIn,
    ProjectIn,
    ProjectOut,
    ProjectSummary,
    ReviewFile,
    ReviewIn,
    ReviewOut,
)
from app.video_reviews.storage import ReviewStore, valid_slug

LIVE = ("pending", "approved", "rejected")


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
    choices = outline_choices(review.payload) if review.gate == "outline" else []
    if decision.decision == "approve" and choices and decision.choice not in choices:
        return f"請從 {'、'.join(choices)} 選一個大綱"
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


def _summary(project: VideoProject, pending: int) -> dict[str, Any]:
    return {
        "slug": project.slug,
        "title": project.title,
        "stage": project.stage,
        "checklist": project.checklist,
        "youtube_video_id": project.youtube_video_id,
        "last_synced_at": project.last_synced_at,
        "pending": pending,
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
    project.youtube_video_id = payload.youtube_video_id
    project.last_synced_at = now
    project.updated_at = now
    await session.commit()
    if project.youtube_video_id:
        # On YouTube now: the previews have done their job.
        store.keep_only(slug, set())
    return await project_view(session, slug)


async def project_view(session: AsyncSession, slug: str) -> ProjectOut:
    project = await _project(session, slug)
    reviews = await _reviews(session, project)
    pending = sum(1 for review in reviews if review.status == "pending")
    return ProjectOut(
        **_summary(project, pending),
        reviews=[_review_out(review) for review in reviews],
    )


async def list_projects(session: AsyncSession) -> list[ProjectSummary]:
    pending = (
        select(VideoReview.project_id, func.count().label("pending"))
        .where(VideoReview.status == "pending")
        .group_by(VideoReview.project_id)
        .subquery()
    )
    rows = await session.execute(
        select(VideoProject, func.coalesce(pending.c.pending, 0))
        .outerjoin(pending, pending.c.project_id == VideoProject.id)
        .order_by(VideoProject.last_synced_at.desc())
        .limit(200)
    )
    return [ProjectSummary(**_summary(project, int(count))) for project, count in rows.all()]


async def submit_review(
    session: AsyncSession,
    store: ReviewStore,
    slug: str,
    payload: ReviewIn,
    token: VideoToolToken,
) -> ReviewOut:
    project = await _project(session, slug)
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
    if same is not None:
        return _review_out(same)
    now = datetime.now(UTC)
    for review in reviews:
        if review.gate == payload.gate and review.status == "pending":
            review.status = "superseded"
            review.updated_at = now
    review = VideoReview(
        project_id=project.id,
        gate=payload.gate,
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
    project.last_synced_at = now
    await session.commit()
    store.keep_only(slug, kept_files([*reviews, review]))
    return _review_out(review)


async def decide(
    session: AsyncSession, slug: str, review_id: Any, user: User, decision: DecisionIn
) -> ReviewOut:
    project = await _project(session, slug)
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
    review.choice = decision.choice if review.gate == "outline" else None
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
