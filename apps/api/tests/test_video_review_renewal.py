"""Shorts review identity uses the current QA as well as the unchanged MP4.

These always-on tests exercise real database rows and review-store files. PostgreSQL lock
serialization is covered separately in test_video_reviews_integration.py.
"""

from __future__ import annotations

import hashlib
from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import UUID, uuid4

import pytest
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User, VideoProject, VideoReview, VideoToolToken
from app.problems import AppError
from app.video_automation.judge import SHORTS_QA_ITEMS
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import DecisionIn, ReviewIn, ReviewOut
from app.video_reviews.storage import ReviewStore
from app.video_shorts import costs
from app.video_shorts.models import VideoShortsSlot
from app.video_youtube import vps
from app.video_youtube.errors import Refused

SLUG = "shorts-review-renewal"
FINAL_BYTES = b"the same final MP4"
FINAL_SHA = hashlib.sha256(FINAL_BYTES).hexdigest()
MODELS = (User, VideoToolToken, VideoProject, VideoReview, AdminAuditLog, VideoShortsSlot)


@dataclass
class Site:
    factory: async_sessionmaker[AsyncSession]
    owner: User
    token: VideoToolToken
    store: ReviewStore
    idle: AsyncMock


@pytest.fixture
async def site(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> AsyncIterator[Site]:
    engine = create_async_engine("sqlite+aiosqlite://")

    def restore_utc(target: Any, _context: Any, *_more: Any) -> None:
        for column in target.__table__.columns:
            value = getattr(target, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                setattr(target, column.name, value.replace(tzinfo=UTC))

    for model in MODELS:
        event.listen(model, "load", restore_utc)
        event.listen(model, "refresh", restore_utc)
    async with engine.begin() as connection:
        await connection.run_sync(
            lambda sync: Base.metadata.create_all(
                sync, tables=[model.__table__ for model in MODELS]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    owner = User(id=uuid4(), email="renewal-owner@example.test", password_hash="unused")
    token = VideoToolToken(id=uuid4(), name="tool", token_hash="a" * 64, token_prefix="mkv_test")
    async with factory() as session:
        session.add_all(
            [
                owner,
                token,
                VideoProject(
                    slug=SLUG, title="Short", stage="final", format="shorts", shorts_line="lab"
                ),
            ]
        )
        await session.commit()

    async def auto_short(
        _session: AsyncSession, gate: str, payload: dict[str, Any], _sha: str
    ) -> bool:
        report = payload.get("qa" if gate == "final" else "package", {})
        return report.get("ok") is True and all(
            item.get("ok") is True for item in report.get("items", [])
        )

    monkeypatch.setattr(service, "auto_approves_shorts", auto_short)
    monkeypatch.setattr(service, "auto_approves_final", AsyncMock(return_value=False))
    monkeypatch.setattr(service, "compilation_slugs", AsyncMock(return_value=set()))
    monkeypatch.setattr(costs, "record_usage", AsyncMock())
    monkeypatch.setattr(costs, "record_media", AsyncMock())
    idle = AsyncMock()
    monkeypatch.setattr(vps, "assert_idle", idle)
    try:
        yield Site(
            factory,
            owner,
            token,
            ReviewStore(tmp_path, max_file_bytes=10**6, max_total_bytes=10**7),
            idle,
        )
    finally:
        for model in MODELS:
            event.remove(model, "load", restore_utc)
            event.remove(model, "refresh", restore_utc)
        await engine.dispose()


def _file(site: Site, body: bytes, role: str, content_type: str) -> dict[str, Any]:
    sha = hashlib.sha256(body).hexdigest()
    site.store.put_part(SLUG, sha, index=0, count=1, size=len(body), data=body)
    return {"role": role, "sha256": sha, "size": len(body), "content_type": content_type}


def _final(site: Site, version: str, *, passed: bool = True) -> ReviewIn:
    return ReviewIn(
        gate="final",
        content_sha256=FINAL_SHA,
        summary=f"QA {version}",
        payload={
            "qa": {
                "ok": passed,
                "kind": "shorts",
                "line": "lab",
                "final_sha256": FINAL_SHA,
                "inputs": {
                    "version": 1,
                    "files": {"script.json": hashlib.sha256(version.encode()).hexdigest()},
                },
                "items": [
                    {"id": name, "ok": passed or name != "policy", "detail": "checked"}
                    for name in SHORTS_QA_ITEMS
                ],
            }
        },
        files=[
            _file(site, FINAL_BYTES, "preview", "video/mp4"),
            _file(site, version.encode(), "evidence_verify", "application/json"),
        ],
    )


def _publish(final_id: UUID | None) -> ReviewIn:
    return ReviewIn(
        gate="publish",
        content_sha256="b" * 64,
        summary="The same metadata",
        payload={
            **({"final_review_id": str(final_id)} if final_id is not None else {}),
            "package": {"ok": True, "items": [{"id": "files", "ok": True}]},
        },
    )


async def _submit(site: Site, payload: ReviewIn) -> ReviewOut:
    async with site.factory() as session:
        return await service.submit_review(session, site.store, SLUG, payload, site.token)


async def _decide(site: Site, review_id: UUID, decision: str, note: str) -> ReviewOut:
    async with site.factory() as session:
        return await service.decide(
            session,
            SLUG,
            review_id,
            site.owner,
            DecisionIn.model_validate({"decision": decision, "note": note}),
        )


async def _rows(site: Site) -> list[VideoReview]:
    async with site.factory() as session:
        return list(await session.scalars(select(VideoReview).order_by(VideoReview.created_at)))


async def _audits(site: Site) -> list[AdminAuditLog]:
    async with site.factory() as session:
        return list(await session.scalars(select(AdminAuditLog).order_by(AdminAuditLog.created_at)))


@pytest.mark.asyncio
async def test_new_failed_qa_replaces_a_pass_without_reusing_its_approval(site: Site) -> None:
    passed = await _submit(site, _final(site, "A"))
    assert passed.status == "approved"
    failed_input = _final(site, "A", passed=False)
    failed = await _submit(site, failed_input)
    assert failed.id != passed.id
    assert failed.status == "pending"
    assert failed.payload["qa"]["inputs"] == passed.payload["qa"]["inputs"]
    assert (await _submit(site, failed_input)).id == failed.id
    rows = await _rows(site)
    assert [(row.revision, row.status) for row in rows] == [(0, "superseded"), (1, "pending")]
    assert rows[0].decided_at == passed.decided_at
    assert rows[0].note == passed.note
    audits = await _audits(site)
    assert [row.action for row in audits].count("video_review_auto_approved") == 1
    assert any(row.action == "video_review_superseded" for row in audits)
    assert site.idle.await_args is not None
    assert isinstance(site.idle.await_args.args[0], AsyncSession)
    assert site.idle.await_args.args[1:] == (SLUG,)
    assert site.idle.await_args.kwargs == {"upload": True}


@pytest.mark.asyncio
async def test_corrected_qa_replaces_rejection_and_keeps_its_decision_and_file(site: Site) -> None:
    old_input = _final(site, "A", passed=False)
    waiting = await _submit(site, old_input)
    rejected = await _decide(site, waiting.id, "reject", "The evidence is incorrect.")
    corrected = await _submit(site, _final(site, "B"))
    assert corrected.id != rejected.id and corrected.status == "approved"
    rows = {row.id: row for row in await _rows(site)}
    assert rows[rejected.id].status == "superseded"
    assert rows[rejected.id].decided_by_user_id == site.owner.id
    assert rows[rejected.id].decided_at == rejected.decided_at
    assert rows[rejected.id].note == "The evidence is incorrect."
    assert rows[rejected.id].files == [file.model_dump() for file in old_input.files]
    assert site.store.path(SLUG, old_input.files[1].sha256) is not None
    assert any(
        row.action == "video_review_rejected" and row.target == f"video_review:{rejected.id}"
        for row in await _audits(site)
    )


@pytest.mark.asyncio
async def test_a_b_a_allocates_a_third_revision_instead_of_resurrecting_history(site: Site) -> None:
    first = await _submit(site, _final(site, "A"))
    second = await _submit(site, _final(site, "B"))
    third = await _submit(site, _final(site, "A"))
    assert len({first.id, second.id, third.id}) == 3
    assert third.payload == first.payload
    assert [(row.revision, row.status) for row in await _rows(site)] == [
        (0, "superseded"),
        (1, "superseded"),
        (2, "approved"),
    ]


@pytest.mark.asyncio
async def test_changed_pending_qa_gets_a_new_identity_and_stale_owner_decision_fails(
    site: Site,
) -> None:
    first = await _submit(site, _final(site, "A", passed=False))
    second = await _submit(site, _final(site, "B", passed=False))
    assert first.id != second.id and second.status == "pending"
    with pytest.raises(AppError) as error:
        await _decide(site, first.id, "approve", "An old browser page")
    assert error.value.status == 409
    assert error.value.code == "video_review_not_decidable"
    assert (await _rows(site))[-1].status == "pending"


@pytest.mark.asyncio
async def test_manual_approval_of_current_failed_qa_remains_idempotent(site: Site) -> None:
    body = _final(site, "A", passed=False)
    pending = await _submit(site, body)
    approved = await _decide(site, pending.id, "approve", "Owner checked the exception.")
    again = await _submit(site, body)
    assert again.id == approved.id
    assert again.status == "approved" and again.payload["qa"]["ok"] is False
    assert again.note == "Owner checked the exception."
    assert len(await _rows(site)) == 1
    assert len(await _audits(site)) == 1


@pytest.mark.asyncio
async def test_final_renewal_releases_slot_and_requires_new_publish_identity(site: Site) -> None:
    first_input = _final(site, "A")
    first = await _submit(site, first_input)
    published = await _submit(site, _publish(first.id))
    assert published.status == "approved"
    async with site.factory() as session:
        session.add(
            VideoShortsSlot(
                starts_at=datetime.now(UTC) + timedelta(days=1),
                status="assigned",
                project_slug=SLUG,
                line="lab",
            )
        )
        await session.commit()
    old_audits = {row.id for row in await _audits(site)}
    renewed = await _submit(site, _final(site, "B"))
    rows = {row.id: row for row in await _rows(site)}
    assert rows[first.id].status == rows[published.id].status == "superseded"
    assert rows[published.id].decided_at == published.decided_at
    assert rows[published.id].note == published.note
    assert old_audits.issubset({row.id for row in await _audits(site)})
    assert site.store.path(SLUG, first_input.files[1].sha256) is not None
    async with site.factory() as session:
        slot = await session.scalar(select(VideoShortsSlot))
        assert slot is not None and slot.status == "open" and slot.project_slug is None
    for stale_id in (None, first.id):
        with pytest.raises(AppError) as error:
            await _submit(site, _publish(stale_id))
        assert error.value.status == 409
        assert error.value.code == "video_shorts_final_review_stale"
    replacement = await _submit(site, _publish(renewed.id))
    assert replacement.id != published.id and replacement.status == "approved"
    assert replacement.content_sha256 == published.content_sha256
    assert (await _submit(site, _publish(renewed.id))).id == replacement.id
    publish_rows = [row for row in await _rows(site) if row.gate == "publish"]
    assert [row.revision for row in publish_rows] == [0, 1]


@pytest.mark.asyncio
async def test_publish_requires_current_final_to_be_approved(site: Site) -> None:
    pending = await _submit(site, _final(site, "A", passed=False))
    with pytest.raises(AppError) as error:
        await _submit(site, _publish(pending.id))
    assert error.value.code == "video_shorts_final_review_stale"
    assert len(await _rows(site)) == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("state", ["video", "upload", "queued", "running", "vps"])
async def test_upload_activity_refuses_renewal_without_changing_history(
    site: Site, state: str
) -> None:
    first = await _submit(site, _final(site, "A"))
    if state == "vps":
        site.idle.side_effect = Refused(409, "vps_job_exists", "Upload is running")
    else:
        async with site.factory() as session:
            project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
            assert project is not None
            if state == "video":
                project.youtube_video_id = "dQw4w9WgXcQ"
            elif state == "upload":
                project.youtube_upload_session = "https://example.test/resumable"
            else:
                project.youtube_sync = {"status": state}
            await session.commit()
    with pytest.raises(AppError) as error:
        await _submit(site, _final(site, "B", passed=False))
    assert error.value.status == 409
    assert error.value.code == (
        "vps_job_exists" if state == "vps" else "video_shorts_review_upload_started"
    )
    rows = await _rows(site)
    assert len(rows) == 1 and rows[0].id == first.id and rows[0].status == "approved"
    assert len(await _audits(site)) == 1


@pytest.mark.asyncio
async def test_long_video_keeps_its_existing_same_hash_semantics(site: Site) -> None:
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.format = "slides"
        project.shorts_line = None
        await session.commit()
    first = await _submit(site, _final(site, "A", passed=False))
    changed = await _submit(site, _final(site, "B", passed=False))
    assert changed.id == first.id and changed.payload != first.payload
    await _decide(site, changed.id, "reject", "Long cut needs edits.")
    again = await _submit(site, _final(site, "C"))
    assert again.id == first.id and again.status == "rejected"
    assert again.payload == changed.payload
    assert len(await _rows(site)) == 1
    site.idle.assert_not_awaited()
