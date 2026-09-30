"""/admin/videos against PostgreSQL: report, upload, submit, supersede, decide, read back."""

from __future__ import annotations

import asyncio
import hashlib
import os
from collections.abc import AsyncIterator
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import select

from app.db import SessionFactory, engine
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_automation import settings as automation
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import DecisionIn, DropIn, LocalesIn, ProjectIn, ReviewIn, ReviewOut
from app.video_reviews.storage import ReviewStore
from app.video_youtube import vps

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
async def test_blocked_video_retry_is_one_request_until_worker_acknowledges_it(
    tmp_path: Path,
) -> None:
    slug = f"retry-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000, max_total_bytes=50_000)
    async with SessionFactory() as session:
        owner = User(email=f"retry-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()
        blocked = ProjectIn(title="A blocked video", stage="blocked", checklist=[])
        await service.upsert_project(session, store, slug, blocked)

        first = await service.retry_project(session, slug, owner)
        second = await service.retry_project(session, slug, owner)
        assert first.retry_request_id is not None
        assert second.retry_request_id == first.retry_request_id
        assert second.retry_acknowledged_id is None
        listed = next(item for item in await service.list_projects(session) if item.slug == slug)
        assert listed.retry_request_id == first.retry_request_id

        # An unrelated acknowledgement cannot consume the pending request.
        await service.upsert_project(
            session, store, slug,
            ProjectIn(title="A blocked video", stage="retrying", retry_acknowledged_id=uuid4()),
        )
        assert (await service.project_view(session, slug)).retry_acknowledged_id is None
        with pytest.raises(AppError) as not_blocked:
            await service.retry_project(session, slug, owner)
        assert not_blocked.value.code == "video_retry_not_blocked"

        await service.upsert_project(
            session, store, slug,
            ProjectIn(
                title="A blocked video",
                stage="retrying",
                retry_acknowledged_id=first.retry_request_id,
            ),
        )
        await service.upsert_project(session, store, slug, blocked)
        again = await service.retry_project(session, slug, owner)
        assert again.retry_request_id not in (None, first.retry_request_id)
        assert again.retry_acknowledged_id == first.retry_request_id

        audit = await session.scalars(
            select(AdminAuditLog.action).where(AdminAuditLog.target.like("video_project:%"))
        )
        assert list(audit).count("video_project_retry_requested") >= 2


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
        # Since the hands-off work (docs/videos/HANDS-OFF.md) a published video keeps its previews
        # until it has been on YouTube for seven days; prune_published_previews removes the mp4
        # then (tests/test_video_reviews_youtube.py), so reporting the id alone deletes nothing.
        assert store.path(slug, new_cut) is not None, "reporting the id keeps the previews"


@pytest.mark.asyncio(loop_scope="module")
async def test_a_dropped_video_stays_listed_with_its_article_and_takes_nothing_more(
    tmp_path: Path,
) -> None:
    slug = f"it-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    async with SessionFactory() as session:
        owner = User(email=f"video-drop-{uuid4()}@example.com", password_hash="unused")
        token = VideoToolToken(name="it", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        session.add_all([owner, token])
        await session.commit()

        article = "ai-news-gemini-student-offer-20260820"
        await service.upsert_project(
            session,
            store,
            slug,
            ProjectIn(title="Google AI 學生方案", stage="outline", source_guide=article),
        )
        again = await service.upsert_project(
            session, store, slug, ProjectIn(title="Google AI 學生方案", stage="outline")
        )
        assert again.source_guide == article, "a report without the article keeps it"
        outline = ReviewIn(
            gate="outline",
            content_sha256="4" * 64,
            summary="大綱",
            payload={"options": [{"key": "A"}, {"key": "B"}]},
        )
        pending = await service.submit_review(session, store, slug, outline, token)

        dropped = await service.drop_project(
            session, store, slug, owner, DropIn(note="第二批已經做了這題")
        )
        assert dropped.dropped_at is not None and dropped.pending == 0
        assert dropped.reviews[0].id == pending.id and dropped.reviews[0].status == "superseded"
        with pytest.raises(AppError) as refused:
            await service.submit_review(session, store, slug, outline, token)
        assert refused.value.code == "video_project_dropped"

        listed = next(item for item in await service.list_projects(session) if item.slug == slug)
        assert (listed.source_guide, listed.dropped_note) == (article, "第二批已經做了這題")
        audit = await session.scalars(
            select(AdminAuditLog.action).where(AdminAuditLog.actor_user_id == owner.id)
        )
        assert list(audit) == ["video_project_dropped"]


@pytest.mark.asyncio(loop_scope="module")
async def test_the_owner_s_languages_reach_the_worker_and_its_batch_comes_back_to_be_uploaded(
    tmp_path: Path,
) -> None:
    """docs/videos/LANGUAGES.md: the choice after the final cut, the worker's batch, the states
    on the list, the upload confirmation, and "ready to upload" once every part is done."""
    slug = f"it-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    async with SessionFactory() as session:
        owner = User(email=f"video-languages-{uuid4()}@example.com", password_hash="unused")
        token = VideoToolToken(name="it", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        session.add_all([owner, token])
        await session.commit()

        reported = await service.upsert_project(
            session, store, slug, ProjectIn(title="AI 模型怎麼挑", stage="final")
        )
        assert reported.locales == {} and reported.locales_decided_at is None
        assert not reported.ready_to_upload, "the owner has not decided the languages"

        chosen = await service.set_locales(
            session,
            slug,
            owner,
            LocalesIn.model_validate(
                {"locales": {"ko": {"dub": True}, "en": {"metadata": True, "captions": True}}}
            ),
        )
        assert list(chosen.locales) == ["en", "ko"] and chosen.locales_decided_at is not None
        assert chosen.dub_locales == ["ko"]
        assert {part: out.state for part, out in chosen.languages["ko"].items()} == {
            "captions": "working",
            "dub": "working",
        }
        listed = next(item for item in await service.list_projects(session) if item.slug == slug)
        assert list(listed.locales) == ["en", "ko"], "the worker's list carries the choice"
        assert listed.languages["en"]["metadata"].state == "working"
        again = await service.upsert_project(
            session, store, slug, ProjectIn(title="AI 模型怎麼挑", stage="languages")
        )
        assert list(again.locales) == ["en", "ko"], "the pipeline's reports never touch it"

        # The upload confirmation is approved, but the languages are still in the making.
        package = await service.submit_review(
            session,
            store,
            slug,
            ReviewIn(gate="publish", content_sha256="5" * 64, summary="上傳包", payload={}),
            token,
        )
        await service.decide(session, slug, package.id, owner, DecisionIn(decision="approve"))
        assert not (await service.project_view(session, slug)).ready_to_upload

        track = _upload(store, slug, b"korean track")
        batch = await service.submit_review(
            session,
            store,
            slug,
            ReviewIn(
                gate="languages",
                content_sha256="6" * 64,
                summary="語言：en 標題說明與 CC；ko CC 與配音",
                payload={
                    "locales": {
                        "en": {"metadata": "ready", "captions": "ready"},
                        "ko": {"captions": "ready", "dub": "ready"},
                    }
                },
                files=[
                    {"role": "dub_ko", "sha256": track, "size": 12, "content_type": "audio/mp4"}
                ],
            ),
            token,
        )
        assert batch.status == "pending", "a dub track waits for the owner to upload it"
        before = await service.project_view(session, slug)
        assert before.languages["ko"]["dub"].state == "ready"
        assert before.ready_to_upload, "every chosen part is made; the owner may schedule it"
        uploaded = await service.decide(
            session, slug, batch.id, owner, DecisionIn(decision="approve", note="已在 Studio 上傳")
        )
        assert (uploaded.status, uploaded.choice, uploaded.note) == (
            "approved",
            None,
            "已在 Studio 上傳",
        )
        after = next(item for item in await service.list_projects(session) if item.slug == slug)
        assert after.languages["ko"]["dub"].state == "uploaded"
        assert after.languages["en"]["metadata"].state == "ready"
        path, content_type = await service.file_for_admin(session, store, slug, track)
        assert path.read_bytes() == b"korean track" and content_type == "audio/mp4"

        # A language added later: a second batch without a dub track is approved on arrival.
        added = await service.set_locales(
            session,
            slug,
            owner,
            LocalesIn.model_validate(
                {
                    "locales": {
                        "en": {"metadata": True, "captions": True},
                        "ko": {"captions": True, "dub": True},
                        "ja": {"metadata": True},
                    }
                }
            ),
        )
        assert added.languages["ja"]["metadata"].state == "working" and not added.ready_to_upload
        assert added.languages["ko"]["dub"].state == "uploaded", "the first batch still counts"
        later = await service.submit_review(
            session,
            store,
            slug,
            ReviewIn(
                gate="languages",
                content_sha256="7" * 64,
                summary="語言：ja 標題說明",
                payload={"locales": {"ja": {"metadata": "ready"}}},
            ),
            token,
        )
        assert (later.status, later.note) == ("approved", service.LANGUAGES_AUTO_APPROVED_NOTE)
        final = await service.project_view(session, slug)
        assert final.languages["ja"]["metadata"].state == "ready" and final.ready_to_upload

        audit = list(
            await session.scalars(
                select(AdminAuditLog).where(AdminAuditLog.actor_user_id == owner.id)
            )
        )
        assert sorted(row.action for row in audit) == [
            "video_locales_set",
            "video_locales_set",
            "video_review_approved",
            "video_review_approved",
        ]
        picked = next(row for row in audit if row.action == "video_locales_set")
        assert picked.metadata_json["slug"] == slug and "ko" in picked.metadata_json["locales"]

        await service.drop_project(session, store, slug, owner, DropIn(note="不做了"))
        with pytest.raises(AppError) as refused:
            await service.set_locales(session, slug, owner, LocalesIn.model_validate({}))
        assert refused.value.code == "video_project_dropped"


@pytest.mark.asyncio(loop_scope="module")
async def test_a_drama_keeps_one_look_review_per_character_and_can_auto_approve_its_storyboard(
    tmp_path: Path,
) -> None:
    slug = f"it-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    async with SessionFactory() as session:
        owner = User(email=f"video-drama-{uuid4()}@example.com", password_hash="unused")
        token = VideoToolToken(name="it", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        session.add_all([owner, token])
        await session.commit()
        await service.upsert_project(
            session,
            store,
            slug,
            # A drama reports its format (review-push and the worker both do): its storyboard
            # reads the drama's switch, an illustrated slides video's its own.
            ProjectIn(title="drama", stage="look", checklist=[], format="drama"),
        )

        def look(subject: str, content: str) -> ReviewIn:
            return ReviewIn(
                gate="look",
                subject=subject,
                content_sha256=content * 64,
                summary=f"sheets for {subject}",
                payload={"options": [{"key": "A"}, {"key": "B"}, {"key": "C"}]},
            )

        first = await service.submit_review(session, store, slug, look("jingwei", "1"), token)
        other = await service.submit_review(session, store, slug, look("yandi", "2"), token)
        second = await service.submit_review(session, store, slug, look("jingwei", "3"), token)
        view = await service.project_view(session, slug)
        statuses = {review.id: (review.status, review.subject) for review in view.reviews}
        assert statuses[first.id] == ("superseded", "jingwei")
        assert statuses[other.id] == ("pending", "yandi"), "another character's review stays"
        assert statuses[second.id] == ("pending", "jingwei")
        with pytest.raises(AppError) as no_choice:
            await service.decide(session, slug, second.id, owner, DecisionIn(decision="approve"))
        assert no_choice.value.code == "video_review_not_decidable"
        chosen = await service.decide(
            session, slug, second.id, owner, DecisionIn(decision="approve", choice="C")
        )
        assert (chosen.status, chosen.choice, chosen.subject) == ("approved", "C", "jingwei")

        board = {"shots": [{"id": "opening"}], "judge": {"overall": 9, "problems": []}}
        waiting = await service.submit_review(
            session,
            store,
            slug,
            ReviewIn(gate="storyboard", content_sha256="4" * 64, summary="board", payload=board),
            token,
        )
        assert waiting.status == "pending", "off by default: the owner looks at the keyframes"

        row = await automation.settings_row(session, lock=True)
        row.auto_approve_storyboard = True
        row.judge_min_score = 8
        await session.commit()
        approved = await service.submit_review(
            session,
            store,
            slug,
            ReviewIn(gate="storyboard", content_sha256="5" * 64, summary="board", payload=board),
            token,
        )
        assert approved.status == "approved"
        assert approved.note == automation.AUTO_APPROVED_STORYBOARD_NOTE
        row = await automation.settings_row(session, lock=True)
        row.auto_approve_storyboard = False
        row.judge_min_score = 7
        await session.commit()


def _renewal_review(version: str) -> ReviewIn:
    return ReviewIn(
        gate="final",
        content_sha256="e" * 64,
        summary=f"QA {version}",
        payload={"qa": {"ok": False, "inputs": {"version": 1, "files": {"script": version}}}},
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_concurrent_identical_short_renewals_create_one_new_current_review(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    slug = f"renewal-race-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000, max_total_bytes=50_000)
    monkeypatch.setattr(service, "auto_approves_shorts", AsyncMock(return_value=False))
    monkeypatch.setattr(vps, "assert_idle", AsyncMock())
    async with SessionFactory() as session:
        token = VideoToolToken(name="renewal", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        project = VideoProject(
            slug=slug, title="Renewal", stage="final", format="shorts", shorts_line="lab",
        )
        session.add_all([token, project])
        await session.commit()
        original = await service.submit_review(session, store, slug, _renewal_review("A"), token)

    locked = asyncio.Event()
    release = asyncio.Event()

    async def hold_first(_slug: str, *, upload: bool = False) -> None:
        assert _slug == slug and upload
        locked.set()
        await release.wait()

    idle = AsyncMock(side_effect=hold_first)
    monkeypatch.setattr(vps, "assert_idle", idle)

    async def renew() -> ReviewOut:
        async with SessionFactory() as session:
            return await service.submit_review(session, store, slug, _renewal_review("B"), token)

    first = asyncio.create_task(renew())
    try:
        await asyncio.wait_for(locked.wait(), timeout=10)
        second = asyncio.create_task(renew())
        await asyncio.sleep(0)
    finally:
        release.set()
    results = await asyncio.wait_for(asyncio.gather(first, second), timeout=10)
    assert results[0].id == results[1].id != original.id
    idle.assert_awaited_once_with(slug, upload=True)
    async with SessionFactory() as session:
        rows = list(await session.scalars(
            select(VideoReview).where(VideoReview.project_id == project.id)
            .order_by(VideoReview.revision)
        ))
        assert [(row.revision, row.status) for row in rows] == [
            (0, "superseded"), (1, "pending"),
        ]
        assert rows[1].payload == _renewal_review("B").payload


@pytest.mark.asyncio(loop_scope="module")
async def test_concurrent_owner_decision_refreshes_a_preloaded_superseded_review(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    slug = f"renewal-owner-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000, max_total_bytes=50_000)
    monkeypatch.setattr(service, "auto_approves_shorts", AsyncMock(return_value=False))
    monkeypatch.setattr(vps, "assert_idle", AsyncMock())
    async with SessionFactory() as session:
        owner = User(email=f"renewal-{uuid4()}@example.test", password_hash="unused")
        token = VideoToolToken(name="renewal", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        project = VideoProject(
            slug=slug, title="Renewal", stage="final", format="shorts", shorts_line="lab",
        )
        session.add_all([owner, token, project])
        await session.commit()
        original = await service.submit_review(session, store, slug, _renewal_review("A"), token)

    locked = asyncio.Event()
    release = asyncio.Event()

    async def hold_renewal(_slug: str, *, upload: bool = False) -> None:
        assert _slug == slug and upload
        locked.set()
        await release.wait()

    monkeypatch.setattr(vps, "assert_idle", hold_renewal)

    async def renew() -> ReviewOut:
        async with SessionFactory() as session:
            return await service.submit_review(session, store, slug, _renewal_review("B"), token)

    async with SessionFactory() as owner_session:
        stale = await owner_session.get(VideoReview, original.id)
        assert stale is not None and stale.status == "pending"
        renewing = asyncio.create_task(renew())
        try:
            await asyncio.wait_for(locked.wait(), timeout=10)
            deciding = asyncio.create_task(service.decide(
                owner_session, slug, original.id, owner, DecisionIn(decision="approve"),
            ))
            await asyncio.sleep(0)
        finally:
            release.set()
        results = await asyncio.wait_for(
            asyncio.gather(renewing, deciding, return_exceptions=True), timeout=10,
        )
        assert isinstance(results[0], ReviewOut)
        assert results[0].id != original.id and results[0].status == "pending"
        assert isinstance(results[1], AppError)
        assert results[1].status == 409 and results[1].code == "video_review_not_decidable"
        assert stale.status == "superseded", "the locked lookup must refresh the identity map"
    async with SessionFactory() as session:
        rows = list(await session.scalars(
            select(VideoReview).where(VideoReview.project_id == project.id)
            .order_by(VideoReview.revision)
        ))
        assert [row.status for row in rows] == ["superseded", "pending"]
        assert all(row.decided_at is None for row in rows)
