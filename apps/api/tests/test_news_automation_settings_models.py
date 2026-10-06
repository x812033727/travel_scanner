"""The news writer and verifier models are chosen on the AI settings page, not the news page.

So are the final editor's and the judge's. The judge's switch is the news page's, and a save
from either page leaves alone what it does not send.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient, Response
from pydantic import ValidationError
from sqlalchemy import select

from app.auth.service import current_user
from app.config import get_settings
from app.db import get_session
from app.models import AdminAuditLog, User
from app.news_automation import router, schemas, service
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
        # Not the defaults, so a save that put the defaults back would show.
        judge_enabled=True,
        judge_provider="minimax",
        judge_model="MiniMax-M3",
        **_SAVED,
    )


STORED_JUDGE = (True, "minimax", "MiniMax-M3")
# What a page loaded before the judge existed sends to PUT /settings/models.
SIX_KEYS: dict[str, Any] = {
    "writer_provider": "minimax",
    "writer_model": None,
    "verifier_provider": "minimax",
    "verifier_model": "MiniMax-M3",
    "editor_provider": "anthropic",
    "editor_model": "claude-opus-5-5",
}


def _judge(row: NewsAutomationSettings) -> tuple[bool, str, str | None]:
    return (row.judge_enabled, row.judge_provider, row.judge_model)


def _restarted(row: NewsAutomationSettings) -> bool:
    # The stored row was never flushed, so a start date is only there once a save set it.
    return any(
        getattr(row, f"shadow_started_at_{vertical}") is not None
        for vertical in ("ai", "tech", "crypto")
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


async def _put_models(body: dict[str, Any]) -> Response:
    """Save the models as the owner, through the route and the service behind it."""
    owner = _actor()
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]

    async def session() -> Any:
        yield _session()

    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(router.admin_router, prefix="/api/v1")
    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: owner
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://t") as client:
        return await client.put("/api/v1/admin/news/settings/models", json=body)


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
async def test_a_news_settings_save_that_sends_no_judge_field_leaves_the_judge_as_stored(
    stored: NewsAutomationSettings,
) -> None:
    # What a tab opened before the judge existed sends: neither its switch nor its model.
    await service.update_settings(_session(), _actor(), SettingsWrite(**_SAVED))
    assert _judge(stored) == STORED_JUDGE
    assert not _restarted(stored)


@pytest.mark.parametrize(
    ("was", "sent", "expected"),
    [
        (False, {"judge_enabled": True}, True),
        (True, {"judge_enabled": False}, False),
        (True, {}, True),
        (False, {}, False),
        (True, {"judge_enabled": None}, True),
    ],
)
@pytest.mark.asyncio
async def test_the_judge_switch_is_stored_when_sent_and_kept_when_left_out(
    stored: NewsAutomationSettings, was: bool, sent: dict[str, Any], expected: bool
) -> None:
    stored.judge_enabled = was
    await service.update_settings(_session(), _actor(), SettingsWrite(**_SAVED, **sent))
    assert stored.judge_enabled is expected
    assert (stored.judge_provider, stored.judge_model) == ("minimax", "MiniMax-M3")
    # Switching the judge is not a model change either.
    assert not _restarted(stored)


@pytest.mark.asyncio
async def test_a_page_from_before_the_judge_saves_six_model_keys_and_the_judge_stays(
    stored: NewsAutomationSettings,
) -> None:
    unchanged = await _put_models(SIX_KEYS)
    changed = await _put_models({**SIX_KEYS, "editor_provider": "minimax", "editor_model": None})
    assert unchanged.status_code == 200, unchanged.text
    assert changed.status_code == 200, changed.text
    assert (stored.editor_provider, stored.editor_model) == ("minimax", None)
    assert _judge(stored) == STORED_JUDGE
    saved = changed.json()
    assert (saved["judge_enabled"], saved["judge_provider"], saved["judge_model"]) == STORED_JUDGE


@pytest.mark.parametrize(
    ("judge", "expected"),
    [
        ({"judge_provider": "minimax", "judge_model": "MiniMax-M2.7"}, ("minimax", "MiniMax-M2.7")),
        (
            {"judge_provider": "anthropic", "judge_model": "claude-opus-5-5"},
            ("anthropic", "claude-opus-5-5"),
        ),
        # A vendor named without a model means that vendor's default, as for the other roles.
        ({"judge_provider": "minimax"}, ("minimax", None)),
    ],
)
@pytest.mark.asyncio
async def test_changing_only_the_judge_model_saves_it_and_keeps_the_agreement_figures(
    stored: NewsAutomationSettings, judge: dict[str, str], expected: tuple[str, str | None]
) -> None:
    saved = await _put_models({**SIX_KEYS, **judge})
    assert saved.status_code == 200, saved.text
    assert (stored.judge_provider, stored.judge_model) == expected
    # The switch is the news page's: a model save leaves it where it was.
    assert stored.judge_enabled is True
    assert (stored.writer_provider, stored.verifier_model, stored.editor_model) == (
        "minimax",
        "MiniMax-M3",
        "claude-opus-5-5",
    )
    # The judge is not one of the roles the agreement figures measure.
    assert not _restarted(stored)


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


@pytest.mark.asyncio
async def test_saving_the_same_judge_changes_nothing_and_neither_does_a_model_without_its_vendor(
    stored: NewsAutomationSettings,
) -> None:
    session = _session()
    same = ModelsWrite(**SIX_KEYS, judge_provider="minimax", judge_model="MiniMax-M3")
    await service.update_models(session, _actor(), same)
    # The vendor is what says the page knows the judge; a model alone is not a choice.
    await service.update_models(session, _actor(), ModelsWrite(**SIX_KEYS, judge_model="gpt-6-sol"))
    session.commit.assert_not_awaited()
    assert _judge(stored) == STORED_JUDGE


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


def test_a_judge_vendor_sent_empty_is_refused_and_its_model_is_held_to_the_pattern() -> None:
    with pytest.raises(ValidationError, match="judge_provider cannot be empty"):
        SettingsWrite(**_SAVED, judge_provider=None)
    with pytest.raises(ValidationError, match="judge_provider cannot be empty"):
        ModelsWrite(**SIX_KEYS, judge_provider=None)
    with pytest.raises(ValidationError):
        SettingsWrite(**_SAVED, judge_model="a b")
    with pytest.raises(ValidationError):
        ModelsWrite(**SIX_KEYS, judge_provider="openai", judge_model="../v1beta/models/x")
    written = SettingsWrite(**_SAVED, judge_provider="openai", judge_model="  ")
    assert written.judge_model is None
    assert written.sent_models() == {"judge_provider", "judge_model"}


def test_a_model_save_names_exactly_the_models_a_settings_save_may_leave_out() -> None:
    # update_settings takes the keys to keep from ModelsWrite and SettingsWrite reports the
    # sent ones from _MODEL_KEYS, so the two have to be one list.
    assert tuple(ModelsWrite.model_fields) == schemas._MODEL_KEYS
    assert set(schemas._MODEL_KEYS) <= set(SettingsWrite.model_fields)


@pytest.mark.asyncio
async def test_on_a_stored_row_the_judge_outlives_every_save_that_does_not_name_it(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from tests.test_news_pipeline import database

    # A database, not a stand-in row: the columns are NOT NULL and checked there.
    engine, factory = await database()
    monkeypatch.setattr(service, "load_runtime_settings", AsyncMock(return_value=get_settings()))
    as_stored = {
        "writer_provider": "openai",
        "verifier_provider": "openai",
        "editor_provider": "anthropic",
        "editor_model": "claude-opus-5-5",
    }
    async with factory() as session:
        owner = _actor()
        session.add(owner)
        await session.commit()
        fresh = await service.settings_view(session)
        switched_on = await service.update_settings(
            session, owner, SettingsWrite(**_SAVED, judge_enabled=True)
        )
        row = await service.settings_row(session)
        started = [
            getattr(row, f"shadow_started_at_{vertical}") for vertical in ("ai", "tech", "crypto")
        ]
        chosen = await service.update_models(
            session,
            owner,
            ModelsWrite(**as_stored, judge_provider="minimax", judge_model="MiniMax-M3"),
        )
        unmoved = [
            getattr(row, f"shadow_started_at_{vertical}") for vertical in ("ai", "tech", "crypto")
        ]
        # Two pages loaded before the judge existed: the news page, then the AI settings page.
        news_page = await service.update_settings(session, owner, SettingsWrite(**_SAVED))
        models_page = await service.update_models(
            session,
            owner,
            ModelsWrite(**{**as_stored, "editor_provider": "minimax", "editor_model": None}),
        )
        audits = [row.metadata_json for row in await session.scalars(select(AdminAuditLog))]
    await engine.dispose()

    def judge(view: SettingsView) -> tuple[bool, str, str | None]:
        return (view.judge_enabled, view.judge_provider, view.judge_model)

    assert judge(fresh) == (False, "anthropic", "claude-opus-5-5")
    assert judge(switched_on) == (True, "anthropic", "claude-opus-5-5")
    assert judge(chosen) == (True, "minimax", "MiniMax-M3")
    assert unmoved == started
    assert judge(news_page) == (True, "minimax", "MiniMax-M3")
    assert judge(models_page) == (True, "minimax", "MiniMax-M3")
    assert (models_page.editor_provider, models_page.editor_model) == ("minimax", None)
    # Every save records where the switch stands; only the editor change was a major one.
    assert [entry["judge_enabled"] for entry in audits] == [True, True, True, True]
    assert sorted(entry["major_change"] for entry in audits) == [False, False, False, True]


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
