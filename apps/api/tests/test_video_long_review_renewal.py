"""Owner-only renewal keeps approved evidence and closes the old upload path."""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select

from app.models import VideoProject, VideoReview
from app.problems import AppError
from app.video_reviews import admin_api
from app.video_reviews import admin_service as service
from app.video_reviews.schemas import FinalRenewalIn, ProjectIn, ReviewIn, ReviewOut
from app.video_youtube.errors import Refused
from tests.test_video_review_renewal import (
    SLUG,
    Site,
    _audits,
    _decide,
    _file,
    _final,
    _rows,
    _submit,
)
from tests.test_video_review_renewal import (
    site as _site,
)
from tests.test_video_reviews import _app

site = _site  # Reuse the real database fixture without collecting its module's tests.


async def _initial(site: Site) -> ReviewOut:
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.format, project.shorts_line = "slides", None
        project.locales = {"en": {"captions": True}}
        project.locales_decided_at = datetime.now(UTC)
        project.checklist = [
            {"key": "audio", "label": "Audio", "done": True},
            {"key": "final_video_approved", "label": "Final", "done": True},
            {"key": "package", "label": "Package", "done": True},
        ]
        await session.commit()
    pending = await _submit(site, _final(site, "A"))
    approved = await _decide(site, pending.id, "approve", "Original owner approval")
    async with site.factory() as session:
        initial = await session.get(VideoReview, approved.id)
        assert initial is not None
        for gate in ("publish", "languages", "dubs"):
            session.add(VideoReview(
                project_id=initial.project_id,
                gate=gate, content_sha256=hashlib.sha256(gate.encode()).hexdigest(),
                summary=gate, status="approved", decided_at=datetime.now(UTC),
                payload={"locales": {"en": {"captions": "ready"}}}, files=[],
            ))
        await session.commit()
    return approved


def _candidate(site: Site, name: str = "new") -> ReviewIn:
    return ReviewIn.model_validate({
        "gate": "final", "content_sha256": hashlib.sha256(name.encode()).hexdigest(),
        "summary": "New branded cut", "payload": {"qa": {"ok": True}},
        "files": [_file(site, name.encode(), "preview", "video/mp4")],
    })


async def _request(site: Site) -> FinalRenewalIn:
    async with site.factory() as session:
        state = await service.final_renewal_state(session, SLUG)
    return FinalRenewalIn(
        expected_version=state.version, expected_final_review_id=state.final_review_id,
        expected_final_sha256=state.final_sha256, reason="Use the new channel introduction",
        review=_candidate(site),
    )


async def _renew(site: Site, request: FinalRenewalIn) -> ReviewOut:
    async with site.factory() as session:
        return await service.renew_final(session, site.store, SLUG, site.owner, request)


@pytest.mark.asyncio
async def test_renewal_preserves_decisions_and_requires_fresh_owner_review(
    site: Site, monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = await _initial(site)
    before = await _rows(site)
    auto = AsyncMock(return_value=True)
    monkeypatch.setattr(service, "auto_approves_final", auto)
    request = await _request(site)
    renewed = await _renew(site, request)
    assert renewed.status == "pending" and renewed.decided_at is None
    assert renewed.payload["manual_review"] is True and "qa" not in renewed.payload
    assert renewed.payload["manual_review_qa"] == {"ok": True}
    auto.assert_not_awaited()
    site.idle.assert_awaited_once()
    rows = {row.id: row for row in await _rows(site)}
    for older in before:
        assert rows[older.id].status == "superseded"
        assert rows[older.id].decided_at == older.decided_at
        assert rows[older.id].payload == older.payload and rows[older.id].files == older.files
    assert rows[original.id].note == "Original owner approval"
    assert all(site.store.path(SLUG, item["sha256"]) for item in rows[original.id].files)
    assert service.publish_approved_at(rows.values()) is None
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None and project.stage == "final video approved"
        assert project.checklist[0]["done"] is True
        assert all(not item["done"] for item in project.checklist[1:])
        assert service.language_states(service.locale_choices(project), rows.values())["en"][
            "captions"
        ].state == "working"
    assert [row.action for row in await _audits(site)].count("video_review_superseded") == 4
    with pytest.raises(AppError, match="影片或審核已變更"):
        await _renew(site, request)


@pytest.mark.asyncio
async def test_on_youtube_next_step_with_explicitly_unfinished_checklist_can_renew(
    site: Site,
) -> None:
    await _initial(site)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.stage = "on YouTube"
        project.checklist = [*project.checklist, {
            "key": "on_youtube", "label": "On YouTube", "done": False,
        }]
        await session.commit()
    renewed = await _renew(site, await _request(site))
    rows = await _rows(site)
    assert renewed.status == "pending" and renewed.payload["manual_review"] is True
    assert service.publish_approved_at(rows) is None
    assert all(row.status == "superseded" for row in rows if row.id != renewed.id)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None and project.stage == "final video approved"
        assert project.youtube_video_id is None and project.youtube_sync is None


@pytest.mark.asyncio
@pytest.mark.parametrize("done_values", [[], [True], [False, True], [False, False], [0], [None]])
async def test_on_youtube_ambiguous_or_completed_checklist_still_refuses(
    site: Site, done_values: list[Any],
) -> None:
    await _initial(site)
    request = await _request(site)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        project.stage = "on YouTube"
        project.checklist = [
            {"key": "on_youtube", "label": "On YouTube", "done": value} for value in done_values
        ]
        await session.commit()
    with pytest.raises(AppError) as error:
        await _renew(site, request)
    assert error.value.code == "video_final_renewal_upload_started"
    assert all(row.status == "approved" for row in await _rows(site))


@pytest.mark.asyncio
@pytest.mark.parametrize("changed", ["project", "review", "new_review", "id", "sha"])
async def test_concurrent_state_or_identity_change_refuses_without_writes(
    site: Site, changed: str,
) -> None:
    original = await _initial(site)
    request = await _request(site)
    async with site.factory() as session:
        if changed == "project":
            project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
            assert project is not None
            project.locales = {"ja": {"captions": True}}
        elif changed == "review":
            review = await session.get(VideoReview, original.id)
            assert review is not None
            review.payload = {"changed": True}
        elif changed == "new_review":
            review = await session.get(VideoReview, original.id)
            assert review is not None
            session.add(VideoReview(
                project_id=review.project_id, gate="audio", content_sha256="e" * 64,
                summary="New narration evidence", status="pending", payload={}, files=[],
            ))
        elif changed == "id":
            request.expected_final_review_id = site.owner.id
        else:
            request.expected_final_sha256 = "e" * 64
        await session.commit()
    with pytest.raises(AppError) as error:
        await _renew(site, request)
    assert error.value.code == "video_final_renewal_stale"
    assert (await _rows(site))[0].status == "approved"
    site.idle.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize("field,value", [
    ("youtube_video_id", "dQw4w9WgXcQ"),
    ("youtube_upload_session", "https://example.test/resumable"),
    ("youtube_sync", {"status": "queued"}),
    ("youtube_sync", {"status": "failed"}),
    ("stage", "on YouTube"),
    ("stage", "done"),
    ("youtube_publish_at", datetime.now(UTC)),
    ("shorts_line", "drama"),
    ("dropped_at", datetime.now(UTC)),
])
async def test_upload_signals_shorts_and_dropped_project_refuse(
    site: Site, field: str, value: Any,
) -> None:
    await _initial(site)
    request = await _request(site)
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None
        setattr(project, field, value)
        await session.commit()
    with pytest.raises(AppError):
        await _renew(site, request)
    assert all(row.status == "approved" for row in await _rows(site))


@pytest.mark.asyncio
async def test_vps_activity_and_invalid_attachment_refuse_without_changing_history(
    site: Site,
) -> None:
    await _initial(site)
    request = await _request(site)
    site.idle.side_effect = Refused(409, "vps_job_exists", "Already staging")
    with pytest.raises(AppError) as error:
        await _renew(site, request)
    assert error.value.code == "vps_job_exists"
    site.idle.side_effect = None
    file = request.review.files[0]
    path = site.store.path(SLUG, file.sha256)
    assert path is not None
    path.write_bytes(b"changed bytes")
    with pytest.raises(AppError) as error:
        await _renew(site, request)
    assert error.value.code == "video_final_renewal_files_invalid"
    assert all(row.status == "approved" for row in await _rows(site))


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid", ["old_sha", "no_preview", "duplicate", "size", "vps_down"])
async def test_incomplete_or_reused_candidate_never_replaces_approval(
    site: Site, invalid: str,
) -> None:
    await _initial(site)
    request = await _request(site)
    if invalid == "old_sha":
        request.review.content_sha256 = request.expected_final_sha256
    elif invalid == "no_preview":
        request.review.files = []
    elif invalid == "duplicate":
        request.review.files *= 2
    elif invalid == "size":
        request.review.files[0].size += 1
    else:
        site.idle.side_effect = Refused(503, "vps_unavailable", "Cannot verify idle")
    with pytest.raises(AppError):
        await _renew(site, request)
    assert len(await _rows(site)) == 4
    assert all(row.status == "approved" for row in await _rows(site))


@pytest.mark.asyncio
async def test_worker_cannot_change_or_auto_approve_the_held_review(site: Site) -> None:
    await _initial(site)
    request = await _request(site)
    renewed = await _renew(site, request)
    resent = await _submit(site, request.review)
    assert resent.id == renewed.id and resent.payload == renewed.payload
    assert resent.status == "pending"
    for gate in ("final", "publish", "languages", "dubs"):
        body = _candidate(site, "another").model_copy(update={"gate": gate})
        with pytest.raises(AppError) as error:
            await _submit(site, body)
        assert error.value.code == "video_final_renewal_review_required"
    with pytest.raises(AppError):
        await _decide(site, request.expected_final_review_id, "approve", "Old page")


@pytest.mark.asyncio
async def test_later_submission_preserves_superseded_undecided_renewal_evidence(
    site: Site, monkeypatch: pytest.MonkeyPatch,
) -> None:
    await _initial(site)
    pending_file = _file(site, b"old pending language evidence", "captions_en", "text/plain")
    async with site.factory() as session:
        language = await session.scalar(select(VideoReview).where(VideoReview.gate == "languages"))
        assert language is not None
        language.status, language.decided_at = "pending", None
        language.files = [pending_file]
        await session.commit()
    first = await _renew(site, await _request(site))
    again = await _request(site)
    again.review = _candidate(site, "second replacement")
    await _renew(site, again)
    monkeypatch.setattr(service, "auto_approves_audio", AsyncMock(return_value=False))
    await _submit(site, ReviewIn(
        gate="audio", content_sha256="f" * 64, summary="A later unrelated submission"
    ))
    assert site.store.path(SLUG, pending_file["sha256"]) is not None
    assert site.store.path(SLUG, first.files[0].sha256) is not None
    rows = {row.id: row for row in await _rows(site)}
    assert rows[first.id].status == "superseded" and rows[first.id].decided_at is None


@pytest.mark.asyncio
@pytest.mark.parametrize("partial_report", [True, False])
async def test_worker_report_does_not_restore_old_completed_stage(
    site: Site, monkeypatch: pytest.MonkeyPatch, partial_report: bool,
) -> None:
    await _initial(site)
    await _renew(site, await _request(site))
    monkeypatch.setattr(service, "_decide_story_locales", AsyncMock())
    monkeypatch.setattr(service, "project_view", AsyncMock())
    async with site.factory() as session:
        await service.upsert_project(session, site.store, SLUG, ProjectIn(
            title="Video", stage="on YouTube", checklist=[*([
                {"key": "final_video_approved", "label": "Final", "done": True}
            ] if not partial_report else []),
                {"key": "on_youtube", "label": "Uploaded", "done": True},
            ],
        ))
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None and project.stage == "final video approved"
        assert all(not item["done"] for item in project.checklist)


@pytest.mark.asyncio
@pytest.mark.parametrize("gate", ["languages", "dubs"])
async def test_renewed_language_manifest_must_identify_the_approved_replacement(
    site: Site, gate: str,
) -> None:
    await _initial(site)
    request = await _request(site)
    renewed = await _renew(site, request)
    await _decide(site, renewed.id, "approve", "Watched the replacement")
    for stale in (True, False):
        manifest = json.dumps({"source": {"final": {
            "review_id": str(renewed.id),
            "content_sha256": request.expected_final_sha256 if stale else renewed.content_sha256,
        }}}).encode()
        file = _file(site, manifest, "languages_manifest", "application/json")
        body = ReviewIn.model_validate({
            "gate": gate, "content_sha256": file["sha256"], "summary": "Language batch",
            "payload": {"final_review_id": str(renewed.id)}, "files": [file],
        })
        if stale:
            with pytest.raises(AppError) as error:
                await _submit(site, body)
            assert error.value.code == "video_final_renewal_source_stale"
        else:
            assert (await _submit(site, body)).status in ("pending", "approved")


@pytest.mark.asyncio
async def test_after_owner_approval_only_new_final_bound_packages_can_be_submitted(
    site: Site,
) -> None:
    await _initial(site)
    renewed = await _renew(site, await _request(site))
    await _decide(site, renewed.id, "approve", "Watched the replacement")
    for stale in (True, False):
        meta = json.dumps({"final_sha256": "e" * 64 if stale else renewed.content_sha256}).encode()
        file = _file(site, meta, "metadata", "application/json")
        body = ReviewIn.model_validate({
            "gate": "publish", "content_sha256": file["sha256"], "summary": "New package",
            "payload": {"final_review_id": str(renewed.id)}, "files": [file],
        })
        if stale:
            with pytest.raises(AppError) as error:
                await _submit(site, body)
            assert error.value.code == "video_final_renewal_source_stale"
        else:
            assert (await _submit(site, body)).status == "pending"


@pytest.mark.asyncio
async def test_routes_require_manager_and_validate_final_only(
    site: Site, monkeypatch: pytest.MonkeyPatch,
) -> None:
    await _initial(site)
    body = (await _request(site)).model_dump(mode="json")
    renewed = await _renew(site, FinalRenewalIn.model_validate(body))
    state = AsyncMock(return_value={
        "version": body["expected_version"],
        "final_review_id": body["expected_final_review_id"],
        "final_sha256": body["expected_final_sha256"],
    })
    renewal = AsyncMock(return_value=renewed)
    monkeypatch.setattr(service, "final_renewal_state", state)
    monkeypatch.setattr(service, "renew_final", renewal)
    monkeypatch.setattr(admin_api, "_store", AsyncMock(return_value=site.store))
    url = f"/api/v1/admin/videos/{SLUG}/final-renewal"
    async with AsyncClient(
        transport=ASGITransport(app=_app(site.owner)), base_url="http://test"
    ) as c:
        assert (await c.get(url)).status_code == 403
        assert (await c.post(url, json=body)).status_code == 403
    state.assert_not_awaited()
    renewal.assert_not_awaited()
    site.owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    body["review"]["gate"] = "publish"
    async with AsyncClient(
        transport=ASGITransport(app=_app(site.owner)), base_url="http://test"
    ) as c:
        assert (await c.post(url, json=body)).status_code == 422
    renewal.assert_not_awaited()
    body["review"]["gate"] = "final"
    async with AsyncClient(
        transport=ASGITransport(app=_app(site.owner)), base_url="http://test"
    ) as c:
        assert (await c.get(url)).json()["version"] == body["expected_version"]
        response = await c.post(url, json=body)
    assert response.status_code == 201 and response.json()["status"] == "pending"
    renewal.assert_awaited_once()
