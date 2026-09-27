from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

import pytest
from sqlalchemy import Table, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User
from app.news_automation import service, sources_cli
from app.news_automation.models import NewsSource
from app.news_automation.schemas import SourceWrite
from app.problems import AppError

GOOD = "https://official.example/feed.xml"
BAD = "https://press.example/feed.xml"


def test_the_reviewed_source_file_loads_and_pairs_press_with_first_party_hosts() -> None:
    rows = sources_cli.load_file(sources_cli.DEFAULT_FILE)
    assert len(rows) >= 10
    assert all(row.role == "evidence" for row in rows if row.is_first_party)
    for vertical in ("ai", "crypto"):
        in_vertical = [row for row in rows if row.vertical == vertical]
        assert any(row.is_first_party for row in in_vertical), vertical
        assert any(not row.is_first_party for row in in_vertical), vertical


def rows() -> list[SourceWrite]:
    return [
        SourceWrite(
            name="Official",
            url=GOOD,
            format="rss",
            role="evidence",
            vertical="ai",
            is_first_party=True,
            enabled=True,
        ),
        SourceWrite(
            name="Press",
            url=BAD,
            format="rss",
            role="evidence",
            vertical="ai",
            enabled=True,
            config={"max_entries_per_scan": 10},
        ),
    ]


async def refuse_press(source: NewsSource, **_kwargs: Any) -> None:
    if source.url == BAD:
        raise AppError(422, "news_source_validation_failed", "robots.txt refused")


@pytest.mark.asyncio
async def test_import_is_a_dry_run_until_applied_and_keeps_refused_sources_disabled(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = cast(list[Table], [NewsSource.__table__, AdminAuditLog.__table__])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(sources_cli, "validate_source_configuration", refuse_press)
    monkeypatch.setattr(service, "validate_source_configuration", refuse_press)
    actor = User(id=uuid4(), email="owner@example.com", password_hash="unused")

    async with factory() as session:
        dry = await sources_cli.import_sources(session, rows(), actor=None)
        assert await session.scalar(select(NewsSource.id)) is None
        applied = await sources_cli.import_sources(session, rows(), actor=actor)
        stored = {row.url: row for row in await session.scalars(select(NewsSource))}
        audits = list(await session.scalars(select(AdminAuditLog.action)))
        edited = rows()
        edited[0] = edited[0].model_copy(update={"scan_interval_minutes": 120})
        again = await sources_cli.import_sources(session, edited, actor=actor)
        await session.refresh(stored[GOOD])
    await engine.dispose()

    assert [(item["action"], item["valid"]) for item in dry["sources"]] == [
        ("create", True),
        ("create", False),
    ]
    assert applied["summary"] == {
        "create": 2,
        "update": 0,
        "unchanged": 0,
        "failed_validation": 1,
    }
    assert stored[GOOD].enabled is True
    assert stored[BAD].enabled is False
    assert stored[BAD].last_status == "validation_failed"
    assert stored[BAD].last_error == "robots.txt refused"
    assert stored[BAD].config_json == {"max_entries_per_scan": 10}
    assert audits.count("news_source_created") == 2
    # The refused source is tried again on every run; the edited one is updated.
    assert [item["action"] for item in again["sources"]] == ["update", "update"]
    assert stored[GOOD].scan_interval_minutes == 120


@pytest.mark.asyncio
async def test_run_applies_with_a_persisted_admin_across_a_refused_source(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    engine = create_async_engine("sqlite+aiosqlite://")
    tables = cast(
        list[Table], [User.__table__, NewsSource.__table__, AdminAuditLog.__table__]
    )
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        session.add(
            User(
                email="owner@example.com",
                password_hash="unused",
                is_admin=True,
                is_active=True,
            )
        )
        await session.commit()
    source_file = tmp_path / "sources.json"
    # The refused source comes first, so its rollback happens before the second write.
    ordered = [row.model_dump(mode="json") for row in reversed(rows())]
    source_file.write_text(json.dumps({"sources": ordered}), encoding="utf-8")
    monkeypatch.setattr(sources_cli, "SessionFactory", factory)
    monkeypatch.setattr(sources_cli, "engine", engine)
    monkeypatch.setattr(service, "validate_source_configuration", refuse_press)

    report = await sources_cli.run(source_file, apply=True, actor_email="Owner@Example.com")

    assert [(item["url"], item["enabled"]) for item in report["sources"]] == [
        (BAD, False),
        (GOOD, True),
    ]
