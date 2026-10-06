from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

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


@pytest.mark.parametrize("switch", [{}, {"judge_enabled": None}, {"judge_enabled": False}])
def test_the_judge_vendor_is_not_looked_at_while_the_judge_is_off(switch: dict[str, Any]) -> None:
    for vendor in ("openai", "gemini"):
        payload = SettingsWrite(**{**BASE, **switch, "judge_provider": vendor})
        assert settings_cli.blockers(payload, READY) == []


def test_the_judge_vendor_blocks_once_the_judge_is_switched_on() -> None:
    def judged(vendor: str, **changes: Any) -> SettingsWrite:
        return SettingsWrite(**{**BASE, "judge_enabled": True, "judge_provider": vendor, **changes})

    assert settings_cli.blockers(judged("anthropic"), READY) == []
    assert settings_cli.blockers(judged("openai"), READY) == [
        "judge vendor openai has no API key configured"
    ]
    # Worded for what the judge does: it writes no article.
    assert settings_cli.blockers(judged("gemini"), READY) == [
        "judge vendor gemini cannot judge a news story yet"
    ]
    assert settings_cli.blockers(judged("anthropic", editor_provider="gemini"), READY) == [
        "editor vendor gemini cannot write a news article yet"
    ]
    # The judge never acts while the scanner is off, so switching that off still needs nothing.
    assert settings_cli.blockers(judged("openai", enabled=False), READY) == []


@pytest.mark.parametrize(
    ("flags", "switch"), [([], None), (["--judge-enable"], True), (["--judge-disable"], False)]
)
def test_the_command_line_hands_the_judge_options_to_the_run(
    monkeypatch: pytest.MonkeyPatch, flags: list[str], switch: bool | None
) -> None:
    run = AsyncMock(return_value={})
    monkeypatch.setattr(settings_cli, "run", run)
    monkeypatch.setattr(
        sys, "argv", ["settings_cli", *flags, "--judge-provider", "minimax", "--judge-model", ""]
    )
    settings_cli.main()
    assert run.await_args is not None
    options = run.await_args.kwargs
    assert options["judge_enabled"] is switch
    # An empty model reaches the run as it was typed: it means the vendor's default there.
    assert (options["judge_provider"], options["judge_model"]) == ("minimax", "")
    # The scanner's own switch is another pair of flags.
    assert options["enable"] is None

    monkeypatch.setattr(sys, "argv", ["settings_cli", "--judge-enable", "--judge-disable"])
    with pytest.raises(SystemExit):
        settings_cli.main()


async def cli_database(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    """What the CLI runs against: an administrator, MiniMax and Jev configured, no OpenAI key."""

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
    return engine, factory


@pytest.mark.asyncio
async def test_switching_on_goes_through_the_service_and_is_refused_without_keys(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    engine, factory = await cli_database(monkeypatch, tmp_path)

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

    # The final editor's vendor (Claude by default) needs to be callable too.
    editor_blocked = await settings_cli.run(
        enable=True,
        writer_provider="minimax",
        writer_model=None,
        verifier_provider="minimax",
        verifier_model=None,
        apply=False,
        actor_email=None,
    )
    assert editor_blocked["blockers"] == ["editor vendor anthropic has no API key configured"]
    applied = await settings_cli.run(
        enable=True,
        writer_provider="minimax",
        writer_model=None,
        verifier_provider="minimax",
        verifier_model=None,
        editor_provider="minimax",
        apply=True,
        actor_email="owner@example.com",
    )
    async with factory() as session:
        row = await session.get(NewsAutomationSettings, 1)
        audits = list(await session.scalars(select(AdminAuditLog.action)))
    await engine.dispose()

    assert applied["applied"] is True
    assert row is not None
    assert (
        row.enabled,
        row.mode,
        row.writer_provider,
        row.verifier_provider,
        row.editor_provider,
    ) == (True, "shadow", "minimax", "minimax", "minimax")
    # The editor's stored model was Claude's; with its vendor changed, MiniMax's default.
    assert applied["changes"]["editor_model"] is None and row.editor_model is None
    assert not (row.auto_publish_ai or row.auto_publish_tech or row.auto_publish_crypto)
    assert audits == ["news_settings_updated"]


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["writer", "verifier", "editor", "judge"])
async def test_a_vendor_changed_without_a_model_takes_the_new_vendors_default(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, role: str
) -> None:
    """As on the admin page. A model id kept across the change would be sent to the new
    vendor, and every call of that role would fail on an id it does not know."""

    engine, factory = await cli_database(monkeypatch, tmp_path)
    vendor, model = f"{role}_provider", f"{role}_model"

    async def cli(**options: Any) -> dict[str, Any]:
        unset = dict.fromkeys(
            ("enable", "writer_provider", "writer_model", "verifier_provider", "verifier_model")
        )
        return await settings_cli.run(
            **{**unset, "apply": True, "actor_email": "owner@example.com", **options}
        )

    async def stored() -> tuple[str, str | None]:
        async with factory() as session:
            row = await session.get(NewsAutomationSettings, 1)
        assert row is not None
        return (getattr(row, vendor), getattr(row, model))

    await cli(**{vendor: "minimax", model: "MiniMax-M3"})
    assert await stored() == ("minimax", "MiniMax-M3")

    # The same vendor named again is no change, and the model stays.
    assert (await cli(**{vendor: "minimax"}))["changes"] == {}
    moved = await cli(**{vendor: "anthropic"})
    assert moved["changes"] == {vendor: "anthropic", model: None}
    assert await stored() == ("anthropic", None)

    # A model named with the new vendor is the one stored.
    named = await cli(**{vendor: "minimax", model: "MiniMax-M3"})
    assert named["changes"] == {vendor: "minimax", model: "MiniMax-M3"}
    assert await stored() == ("minimax", "MiniMax-M3")
    await engine.dispose()


@pytest.mark.asyncio
async def test_the_judge_options_are_checked_reported_and_stored(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    engine, factory = await cli_database(monkeypatch, tmp_path)

    async def cli(**options: Any) -> dict[str, Any]:
        unset = dict.fromkeys(
            ("enable", "writer_provider", "writer_model", "verifier_provider", "verifier_model")
        )
        return await settings_cli.run(
            **{**unset, "apply": False, "actor_email": "owner@example.com", **options}
        )

    def reported(report: dict[str, Any]) -> tuple[Any, ...]:
        return tuple(
            report["settings"][key] for key in ("judge_enabled", "judge_provider", "judge_model")
        )

    async def stored() -> tuple[bool, str, str | None]:
        async with factory() as session:
            row = await session.get(NewsAutomationSettings, 1)
        assert row is not None
        return (row.judge_enabled, row.judge_provider, row.judge_model)

    running = {
        "enable": True,
        "writer_provider": "minimax",
        "verifier_provider": "minimax",
        "editor_provider": "minimax",
    }
    assert reported(await cli()) == (False, "anthropic", "claude-opus-5-5")
    # Claude has no key here, and that only matters once the judge is switched on.
    assert (await cli(**running))["blockers"] == []
    blocked = await cli(**running, judge_enabled=True)
    assert blocked["changes"]["judge_enabled"] is True
    assert blocked["blockers"] == ["judge vendor anthropic has no API key configured"]
    with pytest.raises(SystemExit, match="judge vendor anthropic"):
        await cli(**running, judge_enabled=True, apply=True)
    assert reported(await cli()) == (False, "anthropic", "claude-opus-5-5")

    switched_on = await cli(
        **running,
        judge_enabled=True,
        judge_provider="minimax",
        judge_model="MiniMax-M3",
        apply=True,
    )
    assert switched_on["applied"] is True
    assert reported(switched_on) == (True, "minimax", "MiniMax-M3")
    assert await stored() == (True, "minimax", "MiniMax-M3")

    # A run that does not name the judge leaves it alone.
    other = await cli(writer_model="MiniMax-M3", apply=True)
    assert other["changes"] == {"writer_model": "MiniMax-M3"}
    assert await stored() == (True, "minimax", "MiniMax-M3")

    # An empty model is the vendor's default, and the switch goes off again.
    switched_off = await cli(judge_enabled=False, judge_model="", apply=True)
    assert switched_off["changes"] == {"judge_enabled": False, "judge_model": None}
    assert await stored() == (False, "minimax", None)
    await engine.dispose()
