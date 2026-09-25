"""/admin/videos against PostgreSQL: report, upload, submit, supersede, decide, read back."""

from __future__ import annotations

import hashlib
import os
from collections.abc import AsyncIterator
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import select

from app.db import SessionFactory, engine
from app.models import AdminAuditLog, User, VideoToolToken
from app.problems import AppError
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import DecisionIn, ProjectIn, ReviewIn
from app.video_reviews.storage import ReviewStore

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    yield
    await engine.dispose()


def _upload(store: ReviewStore, slug: str, body: bytes) -> str:
    sha = hashlib.sha256(body).hexdigest()
    store.put_part(slug, sha, index=0, count=1, size=len(body), data=body)
    return sha


@pytest.mark.asyncio(loop_scope="module")
async def test_a_video_goes_from_report_to_decision_and_back_to_the_pipeline(
    tmp_path: Path,
) -> None:
    slug = f"it-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    async with SessionFactory() as session:
        owner = User(email=f"video-review-{uuid4()}@example.com", password_hash="unused")
        token = VideoToolToken(name="it", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        session.add_all([owner, token])
        await session.commit()

        with pytest.raises(AppError) as unknown:
            await service.project_view(session, slug)
        assert unknown.value.status == 404

        reported = await service.upsert_project(
            session,
            store,
            slug,
            ProjectIn(
                title="AI 模型怎麼挑",
                stage="final",
                checklist=[{"key": "brief", "label": "企劃", "done": True}],
            ),
        )
        assert reported.title == "AI 模型怎麼挑" and reported.pending == 0

        missing = ReviewIn(
            gate="final",
            content_sha256="c" * 64,
            summary="成片",
            files=[{"role": "preview", "sha256": "d" * 64, "size": 3, "content_type": "video/mp4"}],
        )
        with pytest.raises(AppError) as not_uploaded:
            await service.submit_review(session, store, slug, missing, token)
        assert not_uploaded.value.code == "video_review_files_missing"

        old_cut = _upload(store, slug, b"old cut")
        first = await service.submit_review(
            session,
            store,
            slug,
            ReviewIn(
                gate="final",
                content_sha256="1" * 64,
                summary="成片第一版",
                files=[
                    {"role": "preview", "sha256": old_cut, "size": 7, "content_type": "video/mp4"}
                ],
            ),
            token,
        )
        new_cut = _upload(store, slug, b"new cut!")
        second_in = ReviewIn(
            gate="final",
            content_sha256="2" * 64,
            summary="成片第二版",
            files=[{"role": "preview", "sha256": new_cut, "size": 8, "content_type": "video/mp4"}],
        )
        second = await service.submit_review(session, store, slug, second_in, token)
        again = await service.submit_review(session, store, slug, second_in, token)
        assert again.id == second.id, "the same content is not a new review"
        assert store.path(slug, old_cut) is None, "the superseded cut's file is gone"
        assert store.path(slug, new_cut) is not None

        outline = await service.submit_review(
            session,
            store,
            slug,
            ReviewIn(
                gate="outline",
                content_sha256="3" * 64,
                summary="大綱",
                payload={"options": [{"key": "A"}, {"key": "B"}]},
            ),
            token,
        )
        listed = await service.list_projects(session)
        mine = next(project for project in listed if project.slug == slug)
        assert mine.pending == 2

        view = await service.project_view(session, slug)
        statuses = {review.id: review.status for review in view.reviews}
        assert statuses[first.id] == "superseded" and statuses[second.id] == "pending"

        with pytest.raises(AppError) as no_choice:
            await service.decide(session, slug, outline.id, owner, DecisionIn(decision="approve"))
        assert no_choice.value.code == "video_review_not_decidable"
        chosen = await service.decide(
            session, slug, outline.id, owner, DecisionIn(decision="approve", choice="B")
        )
        rejected = await service.decide(
            session, slug, second.id, owner, DecisionIn(decision="reject", note="片頭太長")
        )
        assert (chosen.status, chosen.choice) == ("approved", "B")
        assert (rejected.status, rejected.note) == ("rejected", "片頭太長")
        with pytest.raises(AppError):
            await service.decide(session, slug, second.id, owner, DecisionIn(decision="approve"))

        path, content_type = await service.file_for_admin(session, store, slug, new_cut)
        assert path.read_bytes() == b"new cut!" and content_type == "video/mp4"
        with pytest.raises(AppError):
            await service.file_for_admin(session, store, slug, old_cut)

        audit = await session.scalars(
            select(AdminAuditLog.action).where(AdminAuditLog.actor_user_id == owner.id)
        )
        assert sorted(audit) == ["video_review_approved", "video_review_rejected"]

        published = await service.upsert_project(
            session,
            store,
            slug,
            ProjectIn(title="AI 模型怎麼挑", stage="published", youtube_video_id="abcDEF123_-"),
        )
        assert published.youtube_video_id == "abcDEF123_-"
        assert store.path(slug, new_cut) is None, "published videos keep no previews"
