from __future__ import annotations

from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import get_settings
from app.db import Base
from app.models import AdminAuditLog, User
from app.news_automation import service, settings_cli
from app.news_automation.models import NewsAutomationSettings, NewsCandidate, NewsSource
from app.news_automation.schemas import SettingsWrite

BASE: dict[str, Any] = {
    "enabled": True,
    "writer_provider": "minimax",
    "verifier_provider": "minimax",
    "global_concurrency": 2,
    "per_vertical_concurrency": 1,
    "min_shadow_days": 14,
    "min_shadow_candidates": 50,
    "min_human_agreement": 0.95,
    "jev_act_confidence": 0.9,
    "prompt_version": "news-v1",
    "policy_version": "news-policy-v1",
}
READY = {"openai": False, "anthropic": True, "minimax": True, "gemini": True, "jev": True}


def test_the_scanner_is_only_switched_on_with_keys_jev_and_a_capable_vendor() -> None:
    assert settings_cli.blockers(SettingsWrite(**BASE), READY) == []
    assert settings_cli.blockers(
        SettingsWrite(**{**BASE, "writer_provider": "openai"}), READY
    ) == ["writer vendor openai has no API key configured"]
    assert settings_cli.blockers(
        SettingsWrite(**{**BASE, "verifier_provider": "gemini"}), READY
    ) == ["verifier vendor gemini cannot write a news article yet"]
    assert settings_cli.blockers(SettingsWrite(**BASE), {**READY, "jev": False}) == [
        "Jev is not configured (its key is in the admin AI vendor card)"
    ]
    # Switching off never needs anything.
    assert settings_cli.blockers(
        SettingsWrite(**{**BASE, "enabled": False, "writer_provider": "openai"}),
        {**READY, "jev": False},
    ) == []


@pytest.mark.asyncio
async def test_switching_on_goes_through_the_service_and_is_refused_without_keys(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # A file, not memory: every run() disposes the engine, which drops an in-memory database.
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'news.db'}")
    tables = cast(
        list[Table],
        [
            User.__table__,
            NewsAutomationSettings.__table__,
            NewsCandidate.__table__,
            NewsSource.__table__,
            AdminAuditLog.__table__,
        ],
    )
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        session.add(User(email="owner@example.com", password_hash="unused", is_admin=True))
        await session.commit()
    runtime = get_settings().model_copy(
        update={"openai_api_key": None, "minimax_api_key": "set", "jev_api_key": "set"}
    )
    loader = AsyncMock(return_value=runtime)
    monkeypatch.setattr(settings_cli, "load_runtime_settings", loader)
    monkeypatch.setattr(service, "load_runtime_settings", loader)
    monkeypatch.setattr(settings_cli, "SessionFactory", factory)
    monkeypatch.setattr(settings_cli, "engine", engine)

    shown = await settings_cli.run(
        enable=True,
        writer_provider=None,
        writer_model=None,
        verifier_provider=None,
        verifier_model=None,
        apply=False,
        actor_email=None,
    )
    assert shown["settings"]["enabled"] is False
    assert shown["keys_configured"]["openai"] is False
    assert shown["changes"] == {"enabled": True}
    assert "writer vendor openai has no API key configured" in shown["blockers"]
    with pytest.raises(SystemExit, match="Refusing to apply"):
        await settings_cli.run(
            enable=True,
            writer_provider=None,
            writer_model=None,
            verifier_provider=None,
            verifier_model=None,
            apply=True,
            actor_email="owner@example.com",
        )

    applied = await settings_cli.run(
        enable=True,
        writer_provider="minimax",
        writer_model=None,
        verifier_provider="minimax",
        verifier_model=None,
        apply=True,
        actor_email="owner@example.com",
    )
    async with factory() as session:
        row = await session.get(NewsAutomationSettings, 1)
        audits = list(await session.scalars(select(AdminAuditLog.action)))
    await engine.dispose()

    assert applied["applied"] is True
    assert row is not None
    assert (row.enabled, row.mode, row.writer_provider, row.verifier_provider) == (
        True,
        "shadow",
        "minimax",
        "minimax",
    )
    assert not (row.auto_publish_ai or row.auto_publish_tech or row.auto_publish_crypto)
    assert audits == ["news_settings_updated"]
