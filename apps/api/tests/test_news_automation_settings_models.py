"""The news writer and verifier models are chosen on the AI settings page, not the news page."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from pydantic import ValidationError

from app.auth.service import current_user
from app.db import get_session
from app.models import User
from app.news_automation import router, service
from app.news_automation.models import NewsAutomationSettings
from app.news_automation.schemas import ModelsWrite, SettingsView, SettingsWrite
from app.problems import AppError, app_error_handler

_SAVED = {
    "enabled": True,
    "mode": "automatic",
    "global_concurrency": 2,
    "per_vertical_concurrency": 1,
    "min_shadow_days": 14,
    "min_shadow_candidates": 30,
    "min_human_agreement": 0.9,
    "jev_act_confidence": 0.8,
    "auto_publish_ai": True,
    "auto_publish_tech": False,
    "auto_publish_crypto": False,
    "prompt_version": "news-v1",
    "policy_version": "news-policy-v1",
}


def _row() -> NewsAutomationSettings:
    return NewsAutomationSettings(
        id=1,
        writer_provider="minimax",
        writer_model=None,
        verifier_provider="minimax",
        verifier_model="MiniMax-M3",
        editor_provider="anthropic",
        editor_model="claude-opus-5-5",
        **_SAVED,
    )


def _view(row: NewsAutomationSettings) -> SettingsView:
    return SettingsView(
        **{key: getattr(row, key) for key in SettingsWrite.model_fields},
        gates={},
        model_options={},
        default_models={},
        updated_at=datetime(2026, 9, 25, tzinfo=UTC),
    )


@pytest.fixture
def stored(monkeypatch: pytest.MonkeyPatch) -> NewsAutomationSettings:
    row = _row()
    monkeypatch.setattr(service, "settings_row", AsyncMock(return_value=row))
    monkeypatch.setattr(service, "settings_view", AsyncMock(side_effect=lambda _s: _view(row)))
    monkeypatch.setattr(service, "gate_for", AsyncMock(return_value=Mock(eligible=True)))
    return row


def _session() -> AsyncMock:
    session = AsyncMock()
    session.add = Mock()
    return session


def _actor() -> User:
    return User(id=uuid4(), email="owner@example.com", password_hash="unused")


@pytest.mark.asyncio
async def test_a_news_settings_save_without_models_keeps_them_and_stays_automatic(
    stored: NewsAutomationSettings,
) -> None:
    await service.update_settings(_session(), _actor(), SettingsWrite(**_SAVED))
    assert (stored.writer_provider, stored.writer_model) == ("minimax", None)
    assert stored.verifier_model == "MiniMax-M3"
    assert (stored.editor_provider, stored.editor_model) == ("anthropic", "claude-opus-5-5")
    # Leaving the models out is not a model change, so the agreement figures keep counting.
    assert stored.mode == "automatic" and stored.auto_publish_ai is True
    assert stored.shadow_started_at_ai is None


@pytest.mark.asyncio
async def test_changing_a_model_from_ai_settings_keeps_publishing_and_restarts_the_agreement(
    stored: NewsAutomationSettings,
) -> None:
    await service.update_models(
        _session(),
        _actor(),
        ModelsWrite(
            writer_provider="openai",
            writer_model="gpt-6-sol",
            verifier_provider="minimax",
            verifier_model="MiniMax-M3",
            editor_provider="openai",
            editor_model="gpt-6-sol",
        ),
    )
    assert (stored.writer_provider, stored.writer_model) == ("openai", "gpt-6-sol")
    assert (stored.editor_provider, stored.editor_model) == ("openai", "gpt-6-sol")
    assert stored.global_concurrency == 2 and stored.enabled is True
    # Since #763 the final editor and Jev decide each article, so a model change leaves
    # automatic publishing on and only restarts the agreement figures.
    assert stored.mode == "automatic" and stored.auto_publish_ai is True
    assert stored.shadow_started_at_ai is not None


@pytest.mark.asyncio
async def test_saving_the_same_models_changes_nothing(stored: NewsAutomationSettings) -> None:
    session = _session()
    same = ModelsWrite(
        writer_provider="minimax",
        verifier_provider="minimax",
        verifier_model="MiniMax-M3",
        editor_provider="anthropic",
        editor_model="claude-opus-5-5",
    )
    await service.update_models(session, _actor(), same)
    session.commit.assert_not_awaited()
    assert stored.mode == "automatic"


def test_a_provider_sent_empty_is_refused() -> None:
    with pytest.raises(ValidationError):
        SettingsWrite(**_SAVED, writer_provider=None)
    with pytest.raises(ValidationError):
        ModelsWrite(
            writer_provider="openai",
            verifier_provider="minimax",
            editor_provider="anthropic",
            writer_model="a b",
        )


@pytest.mark.asyncio
async def test_only_a_content_manager_changes_the_news_models(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    update = AsyncMock(return_value=_view(_row()))
    monkeypatch.setattr(service, "update_models", update)

    async def session() -> Any:
        yield AsyncMock()

    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(router.admin_router, prefix="/api/v1")
    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: viewer
    body = {
        "writer_provider": "openai",
        "verifier_provider": "minimax",
        "editor_provider": "anthropic",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        refused = await client.put("/api/v1/admin/news/settings/models", json=body)
        viewer._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
        saved = await client.put("/api/v1/admin/news/settings/models", json=body)
    assert refused.status_code == 403
    assert saved.status_code == 200, saved.text
    update.assert_awaited_once()
