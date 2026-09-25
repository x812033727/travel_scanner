"""The video automation settings: what they accept, who may change them, and the audio rule."""

from __future__ import annotations

import hashlib
import os
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError
from sqlalchemy import select

from app.auth.service import current_user
from app.config import Settings
from app.db import SessionFactory, engine, get_session
from app.models import AdminAuditLog, User, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_automation import admin_api
from app.video_automation import settings as service
from app.video_automation.models import (
    DEFAULT_CAPTION_LOCALES,
    DEFAULT_STAGE_MODELS,
    DEFAULT_TOPIC_AVOID,
    DEFAULT_TOPIC_SCOPE,
    DEFAULT_VOICE,
    VideoAutomationSettings,
)
from app.video_automation.schemas import SettingsView, SettingsWrite, VoiceOptionsView
from app.video_reviews import admin_service as reviews
from app.video_reviews.schemas import ProjectIn, ReviewIn
from app.video_reviews.storage import ReviewStore
from app.video_speech import admin_api as speech_api


def _values(**changes: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "enabled": False,
        "draft_interval_hours": 72,
        "topics_per_run": 1,
        "max_waiting_drafts": 3,
        "topic_scope": list(DEFAULT_TOPIC_SCOPE),
        "topic_avoid": list(DEFAULT_TOPIC_AVOID),
        "topic_from_site": True,
        "topic_from_search": True,
        "stage_models": {stage: dict(choice) for stage, choice in DEFAULT_STAGE_MODELS.items()},
        "voice": dict(DEFAULT_VOICE),
        "target_minutes_min": 8,
        "target_minutes_max": 12,
        "caption_locales": list(DEFAULT_CAPTION_LOCALES),
        "max_drafts_per_month": 8,
        "monthly_token_budget_millions": 20,
        "max_verify_rounds": 3,
        "max_retake_rounds": 2,
        "auto_approve_audio": True,
    }
    values.update(changes)
    return values


def test_the_defaults_are_a_valid_setting_the_server_can_run() -> None:
    payload = SettingsWrite(**_values())
    runtime = Settings(azure_speech_voices="zh-TW-HsiaoChenNeural")
    assert service.settings_problems(payload, runtime) == []
    assert payload.stage_models["verifier"].model == "claude-opus-5-5"
    assert payload.voice.name == "Sulafat"


@pytest.mark.parametrize(
    "changes",
    [
        {"target_minutes_min": 13, "target_minutes_max": 12},
        {"topic_from_site": False, "topic_from_search": False},
        {"caption_locales": ["en", "en"]},
        {"caption_locales": ["zh-TW"]},
        {"stage_models": {"writer": {"provider": "anthropic", "model": "claude-sonnet-5"}}},
        {"draft_interval_hours": 1},
        {"topic_scope": []},
        {"topic_scope": ["x" * 41]},
        {"voice": {**DEFAULT_VOICE, "rate": "fast"}},
        {"unknown": 1},
    ],
)
def test_settings_that_cannot_be_stored_are_refused(changes: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        SettingsWrite(**_values(**changes))


def test_models_and_voices_the_server_cannot_run_are_named() -> None:
    runtime = Settings(azure_speech_voices="zh-TW-HsiaoChenNeural")
    models = {stage: dict(choice) for stage, choice in DEFAULT_STAGE_MODELS.items()}
    models["writer"] = {"provider": "anthropic", "model": "gpt-6-astra"}
    models["verifier"] = {"provider": "gemini", "model": "gemini-2.5-pro"}
    problems = service.settings_problems(
        SettingsWrite(**_values(stage_models=models, voice={**DEFAULT_VOICE, "name": "Nobody"})),
        runtime,
    )
    assert len(problems) == 3
    assert any("writer" in problem and "gpt-6-astra" in problem for problem in problems)
    assert any("gemini-2.5-pro" in problem for problem in problems), (
        "a retired model is not offered"
    )
    azure = {"provider": "azure", "name": "zh-TW-YunJheNeural", "rate": "+5%"}
    assert service.settings_problems(SettingsWrite(**_values(voice=azure)), runtime) == [
        "zh-TW-YunJheNeural 不在 Azure 語音的允許清單裡"
    ]


def test_only_vendors_with_a_key_are_offered_as_configured() -> None:
    runtime = Settings(anthropic_api_key="a", hotspot_guide_gemini_api_key="g")
    assert service.configured_providers(runtime) == ["anthropic", "gemini"]
    options = service.model_options()
    assert "claude-opus-5-5" in {option.value for option in options["anthropic"]}
    assert all(option.status != "retired" for choices in options.values() for option in choices)


def test_the_audio_check_passes_only_when_every_line_was_checked_and_none_flagged() -> None:
    passed = {"check": {"lines": 157, "checked": 157, "flagged": 0}, "flagged_lines": []}
    assert service.audio_check_passed(passed)
    assert not service.audio_check_passed({**passed, "check": {**passed["check"], "flagged": 1}})
    assert not service.audio_check_passed({**passed, "check": {**passed["check"], "checked": 150}})
    assert not service.audio_check_passed({**passed, "flagged_lines": [{"id": "k7p2"}]})
    assert not service.audio_check_passed({"check": {"lines": 0, "checked": 0, "flagged": 0}})
    assert not service.audio_check_passed({})


def _app(user: User | None = None) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    app.include_router(admin_api.admin_router, prefix="/api/v1")

    async def session() -> Any:
        yield AsyncMock()

    app.dependency_overrides[get_session] = session
    if user is not None:
        app.dependency_overrides[current_user] = lambda: user
    return app


@pytest.mark.asyncio
async def test_a_viewer_reads_the_settings_and_only_a_settings_manager_changes_them(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    view = AsyncMock(
        return_value=SettingsView(
            **_values(),
            model_options=service.model_options(),
            configured_providers=["anthropic"],
            voice_options=VoiceOptionsView(gemini=["Sulafat"], gemini_models=[], azure=[]),
            updated_at=None,
        )
    )
    update = AsyncMock()
    monkeypatch.setattr(service, "settings_view", view)
    monkeypatch.setattr(service, "update_settings", update)
    url = "/api/v1/admin/video-automation/settings"
    async with AsyncClient(
        transport=ASGITransport(app=_app(viewer)), base_url="http://t"
    ) as client:
        read = await client.get(url)
        refused = await client.put(url, json=_values(enabled=True))
    assert read.status_code == 200 and read.json()["voice"]["name"] == "Sulafat"
    assert refused.status_code == 403
    update.assert_not_awaited()


@pytest.mark.asyncio
async def test_the_tool_route_needs_a_video_tool_token() -> None:
    async with AsyncClient(transport=ASGITransport(app=_app()), base_url="http://t") as client:
        response = await client.get("/api/v1/video/automation/settings")
        videos = await client.get("/api/v1/video/automation/videos")
    assert response.status_code == 401 and videos.status_code == 401


@pytest.mark.asyncio
async def test_the_worker_lists_every_video_dropped_ones_included(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    listed = AsyncMock(return_value=[])
    monkeypatch.setattr(admin_api, "list_projects", listed)
    app = _app()
    token = VideoToolToken(id=uuid4(), name="worker", token_hash="h", token_prefix="mkv_w")
    app.dependency_overrides[speech_api.video_tool] = lambda: token
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        response = await client.get("/api/v1/video/automation/videos")
    assert response.status_code == 200 and response.json() == []
    listed.assert_awaited_once()


# Against PostgreSQL, as CI runs it.
integration = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1", reason="requires PostgreSQL"
)


@pytest_asyncio.fixture(loop_scope="module")
async def clean_settings() -> AsyncIterator[None]:
    yield
    async with SessionFactory() as session:
        row = await session.get(VideoAutomationSettings, 1)
        if row is not None:
            await session.delete(row)
            await session.commit()
    await engine.dispose()


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_settings_start_from_defaults_save_with_an_audit_entry_and_read_back(
    clean_settings: None,
) -> None:
    async with SessionFactory() as session:
        owner = User(email=f"video-automation-{uuid4()}@example.com", password_hash="unused")
        session.add(owner)
        await session.commit()
        first = await service.settings_view(session)
        assert first.enabled is False and first.draft_interval_hours == 72
        saved = await service.update_settings(
            session, owner, SettingsWrite(**_values(enabled=True, draft_interval_hours=48))
        )
        assert saved.enabled and saved.draft_interval_hours == 48
        audit = await session.scalar(
            select(AdminAuditLog)
            .where(AdminAuditLog.action == "video_automation_settings_updated")
            .order_by(AdminAuditLog.created_at.desc())
        )
        assert audit is not None
        assert audit.metadata_json["changed"] == ["draft_interval_hours", "enabled"]


@integration
@pytest.mark.asyncio(loop_scope="module")
async def test_narration_jev_passed_is_approved_as_it_arrives_unless_the_owner_turned_it_off(
    clean_settings: None, tmp_path: Path
) -> None:
    slug = f"it-{uuid4().hex[:12]}"
    store = ReviewStore(tmp_path, max_file_bytes=10_000_000, max_total_bytes=50_000_000)
    passed = {"check": {"lines": 3, "checked": 3, "flagged": 0}, "flagged_lines": []}
    async with SessionFactory() as session:
        owner = User(email=f"video-automation-{uuid4()}@example.com", password_hash="unused")
        token = VideoToolToken(name="it", token_hash=uuid4().hex * 2, token_prefix="mkv_it")
        session.add_all([owner, token])
        await session.commit()
        await reviews.upsert_project(
            session, store, slug, ProjectIn(title="t", stage="audio", checklist=[])
        )

        def review(body: bytes, payload: dict[str, Any]) -> ReviewIn:
            return ReviewIn(
                gate="audio",
                content_sha256=hashlib.sha256(body).hexdigest(),
                summary="narration",
                payload=payload,
                files=[],
            )

        approved = await reviews.submit_review(session, store, slug, review(b"a", passed), token)
        assert approved.status == "approved" and approved.note == service.AUTO_APPROVED_NOTE
        flagged = {**passed, "check": {**passed["check"], "flagged": 1}}
        waiting = await reviews.submit_review(session, store, slug, review(b"b", flagged), token)
        assert waiting.status == "pending"

        await service.update_settings(
            session, owner, SettingsWrite(**_values(auto_approve_audio=False))
        )
        off = await reviews.submit_review(session, store, slug, review(b"c", passed), token)
        assert off.status == "pending", "with the setting off the owner decides"
