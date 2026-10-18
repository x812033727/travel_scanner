from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from urllib.parse import urlsplit
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


# How a page of a host is read: the story region and what is left out of it.
PAGE_KEYS = (
    "article_tags",
    "article_ids",
    "article_classes",
    "exclude_tags",
    "exclude_ids",
    "exclude_classes",
)


def test_sources_sharing_a_host_agree_on_how_its_pages_are_read() -> None:
    # The scanner and revalidation look a page's source up by host and keep one source per
    # host, whichever enabled row comes last (scanner.scan_source, validation._source_index).
    # Two listings on one host are fine (blog.google has two) as long as either row would
    # read the host's pages the same way. A row whose feed summary is the evidence must be
    # alone on its host: the other row's pages would be compared against a summary.
    by_host: dict[str, list[SourceWrite]] = {}
    for row in sources_cli.load_file(sources_cli.DEFAULT_FILE):
        if row.enabled:
            by_host.setdefault(urlsplit(row.url).hostname or "", []).append(row)
    shared = {host: found for host, found in by_host.items() if len(found) > 1}
    assert shared, "the file has hosts with two listings; an empty result means a broken test"
    for host, found in shared.items():
        first = found[0]
        for row in found:
            assert not row.config.get("evidence_from_feed_summary"), (host, row.name)
            assert (row.role, row.is_first_party) == (first.role, first.is_first_party), host
            assert {key: row.config.get(key) for key in PAGE_KEYS} == {
                key: first.config.get(key) for key in PAGE_KEYS
            }, (host, row.name)


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


@pytest.mark.asyncio
async def test_run_selects_one_exact_url_for_dry_run_and_apply_without_other_writes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'sources.db'}")
    tables = cast(list[Table], [User.__table__, NewsSource.__table__, AdminAuditLog.__table__])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        session.add(User(email="owner@example.com", password_hash="unused", is_admin=True))
        session.add_all(
            [
                NewsSource(
                    name=row.name,
                    url=row.url,
                    format=row.format,
                    role=row.role,
                    vertical=row.vertical,
                    is_first_party=row.is_first_party,
                    enabled=row.enabled,
                    scan_interval_minutes=60,
                    allowed_redirect_hosts_json=[],
                    config_json=row.config,
                )
                for row in rows()
            ]
        )
        await session.commit()
    desired = [row.model_copy(update={"scan_interval_minutes": 120}) for row in rows()]
    source_file = tmp_path / "reviewed.json"
    source_file.write_text(
        json.dumps({"sources": [row.model_dump(mode="json") for row in desired]}),
        encoding="utf-8",
    )
    monkeypatch.setattr(sources_cli, "SessionFactory", factory)
    monkeypatch.setattr(sources_cli, "engine", engine)
    monkeypatch.setattr(sources_cli, "validate_source_configuration", refuse_press)

    dry = await sources_cli.run(source_file, apply=False, actor_email=None, source_url=GOOD)
    async with factory() as session:
        before = {
            row.url: row.scan_interval_minutes
            for row in await session.scalars(select(NewsSource))
        }
        before_audits = list(await session.scalars(select(AdminAuditLog.action)))
    applied = await sources_cli.run(
        source_file, apply=True, actor_email="owner@example.com", source_url=GOOD
    )
    async with factory() as session:
        after = {
            row.url: row.scan_interval_minutes
            for row in await session.scalars(select(NewsSource))
        }
        audits = list(await session.scalars(select(AdminAuditLog.action)))
    await engine.dispose()

    assert [item["url"] for item in dry["sources"]] == [GOOD]
    assert dry["sources"][0]["valid"] is True
    assert dry["not_in_file"] == []
    assert before == {GOOD: 60, BAD: 60}
    assert before_audits == []
    assert [item["url"] for item in applied["sources"]] == [GOOD]
    assert applied["not_in_file"] == []
    assert after == {GOOD: 120, BAD: 60}
    assert audits == ["news_source_updated"]


@pytest.mark.asyncio
async def test_targeted_definition_update_reloads_feed_without_cached_validators(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'sources.db'}")
    tables = cast(list[Table], [User.__table__, NewsSource.__table__, AdminAuditLog.__table__])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    future = datetime(2099, 1, 1, tzinfo=UTC)
    async with factory() as session:
        session.add(User(email="owner@example.com", password_hash="unused", is_admin=True))
        session.add_all(
            [
                NewsSource(
                    name=row.name,
                    url=row.url,
                    format=row.format,
                    role=row.role,
                    vertical=row.vertical,
                    is_first_party=row.is_first_party,
                    enabled=True,
                    allowed_redirect_hosts_json=[],
                    config_json=row.config,
                    etag='"cached"',
                    last_modified="Wed, 01 Jan 2025 00:00:00 GMT",
                    next_scan_at=future,
                )
                for row in rows()
            ]
        )
        await session.commit()
    desired = rows()
    desired[0] = desired[0].model_copy(
        update={"allowed_redirect_hosts": ["new.example"], "config": {"article_classes": ["story"]}}
    )
    desired[1] = desired[1].model_copy(update={"scan_interval_minutes": 120})
    source_file = tmp_path / "reviewed.json"
    source_file.write_text(
        json.dumps({"sources": [row.model_dump(mode="json") for row in desired]}),
        encoding="utf-8",
    )

    async def validate_selected(source: NewsSource, **_kwargs: Any) -> None:
        assert source.url == GOOD

    monkeypatch.setattr(sources_cli, "SessionFactory", factory)
    monkeypatch.setattr(sources_cli, "engine", engine)
    monkeypatch.setattr(service, "validate_source_configuration", validate_selected)
    started = datetime.now(UTC)
    report = await sources_cli.run(
        source_file,
        apply=True,
        actor_email="owner@example.com",
        source_url=GOOD,
        preserve_on_validation_failure=True,
    )
    finished = datetime.now(UTC)
    async with factory() as session:
        stored = {row.url: row for row in await session.scalars(select(NewsSource))}
        audits = list(await session.scalars(select(AdminAuditLog.action)))
        assert stored[GOOD].allowed_redirect_hosts_json == ["new.example"]
        assert stored[GOOD].config_json == {"article_classes": ["story"]}
        assert stored[GOOD].etag is None
        assert stored[GOOD].last_modified is None
        assert started <= stored[GOOD].next_scan_at.replace(tzinfo=UTC) <= finished
        assert stored[BAD].scan_interval_minutes == 60
        assert stored[BAD].etag == '"cached"'
        assert stored[BAD].last_modified == "Wed, 01 Jan 2025 00:00:00 GMT"
        assert stored[BAD].next_scan_at.replace(tzinfo=UTC) == future
    await engine.dispose()
    assert report["summary"]["failed_validation"] == 0
    assert [item["url"] for item in report["sources"]] == [GOOD]
    assert audits == ["news_source_updated"]


@pytest.mark.asyncio
async def test_run_rejects_an_exact_url_missing_from_the_file_before_opening_a_session(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    source_file = tmp_path / "reviewed.json"
    source_file.write_text(
        json.dumps({"sources": [row.model_dump(mode="json") for row in rows()]}),
        encoding="utf-8",
    )

    def unexpected_session() -> None:
        raise AssertionError("A missing source must not open a database session")

    monkeypatch.setattr(sources_cli, "SessionFactory", unexpected_session)
    with pytest.raises(SystemExit, match="Source URL is not listed"):
        await sources_cli.run(
            source_file, apply=True, actor_email="owner@example.com", source_url=GOOD + "/"
        )


@pytest.mark.asyncio
async def test_strict_targeted_validation_failure_preserves_existing_source_and_other_rows(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'sources.db'}")
    tables = cast(list[Table], [User.__table__, NewsSource.__table__, AdminAuditLog.__table__])
    async with engine.begin() as connection:
        await connection.run_sync(lambda sync: Base.metadata.create_all(sync, tables=tables))
    factory = async_sessionmaker(engine, expire_on_commit=False)
    future = datetime(2099, 1, 1, tzinfo=UTC)
    async with factory() as session:
        session.add(User(email="owner@example.com", password_hash="unused", is_admin=True))
        session.add_all(
            [
                NewsSource(
                    name=row.name,
                    url=row.url,
                    format=row.format,
                    role=row.role,
                    vertical=row.vertical,
                    is_first_party=row.is_first_party,
                    enabled=True,
                    allowed_redirect_hosts_json=["old.example"] if row.url == GOOD else [],
                    config_json=row.config,
                    last_status="succeeded",
                    etag='"old"',
                    last_modified="Wed, 01 Jan 2025 00:00:00 GMT",
                    next_scan_at=future,
                )
                for row in rows()
            ]
        )
        await session.commit()
    desired = rows()
    desired[0] = desired[0].model_copy(
        update={"allowed_redirect_hosts": ["new.example"]}
    )
    desired[1] = desired[1].model_copy(update={"scan_interval_minutes": 120})
    source_file = tmp_path / "reviewed.json"
    source_file.write_text(
        json.dumps({"sources": [row.model_dump(mode="json") for row in desired]}),
        encoding="utf-8",
    )

    async def refuse_selected(source: NewsSource, **_kwargs: Any) -> None:
        assert source.url == GOOD
        raise AppError(422, "news_source_validation_failed", "target robots refused")

    monkeypatch.setattr(sources_cli, "SessionFactory", factory)
    monkeypatch.setattr(sources_cli, "engine", engine)
    monkeypatch.setattr(service, "validate_source_configuration", refuse_selected)
    report = await sources_cli.run(
        source_file,
        apply=True,
        actor_email="owner@example.com",
        source_url=GOOD,
        preserve_on_validation_failure=True,
    )
    async with factory() as session:
        stored = {row.url: row for row in await session.scalars(select(NewsSource))}
        audits = list(await session.scalars(select(AdminAuditLog.action)))
        assert stored[GOOD].enabled is True
        assert stored[GOOD].allowed_redirect_hosts_json == ["old.example"]
        assert stored[GOOD].last_status == "succeeded"
        assert stored[GOOD].etag == '"old"'
        assert stored[GOOD].last_modified == "Wed, 01 Jan 2025 00:00:00 GMT"
        assert stored[GOOD].next_scan_at.replace(tzinfo=UTC) == future
        assert stored[BAD].scan_interval_minutes == 60
    await engine.dispose()
    assert report["sources"] == [
        {
            "name": "Official",
            "url": GOOD,
            "action": "update",
            "enabled": True,
            "preserved": True,
            "error": "target robots refused",
        }
    ]
    assert report["summary"]["failed_validation"] == 1
    assert report["not_in_file"] == []
    assert audits == []


def test_strict_cli_prints_failure_and_exits_nonzero(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    async def failed_run(*_args: Any, **_kwargs: Any) -> dict[str, Any]:
        return {"summary": {"failed_validation": 1}, "sources": [{"error": "refused"}]}

    monkeypatch.setattr(sources_cli, "run", failed_run)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sources_cli", "--source-url", GOOD, "--preserve-on-validation-failure"],
    )
    with pytest.raises(SystemExit) as error:
        sources_cli.main()
    assert error.value.code == 1
    assert '"error": "refused"' in capsys.readouterr().out
