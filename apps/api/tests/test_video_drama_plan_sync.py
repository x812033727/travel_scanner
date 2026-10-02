"""Production-plan updates append review history atomically without starting work."""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.video_automation.models import (
    DEFAULT_DRAMA,
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaMessage,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.schemas import SeriesIn
from app.video_automation.series import next_job_for, series_values

ROOT = Path(__file__).resolve().parents[3]
PACK_ROOT = ROOT / "docs/videos/series-plans"
PACKS = [
    PACK_ROOT / "binge-five-20260928/wedding-reckoning",
    PACK_ROOT / "claude-binge-five-20260928/before-the-hammer",
]
TABLES = (
    VideoDramaSeries,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoProject,
    VideoReview,
    AdminAuditLog,
)


@pytest.fixture(scope="module")
def syncer() -> ModuleType:
    name = "test_sync_drama_plan_revisions_module"
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "ops/video/sync_drama_plan_revisions.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest_asyncio.fixture
async def factory() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    try:
        yield maker
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def seeded(factory, syncer):
    async with factory() as session:
        actor = User(email="drama-sync@example.test", is_active=True, is_admin=True)
        session.add(actor)
        session.add(VideoAutomationSettings(id=1, drama_enabled=False, subtitle_burn_in=True))
        await session.flush()
        for pack in PACKS:
            request = SeriesIn.model_validate_json(
                (pack / "series-request.json").read_text("utf-8")
            )
            series = VideoDramaSeries(
                id=uuid4(),
                **series_values(request, datetime.now(UTC)),
                status="setting",
                created_by_user_id=actor.id,
            )
            session.add(series)
            for doc in json.loads((pack / "documents.json").read_text("utf-8"))["documents"]:
                session.add(
                    VideoDramaDoc(
                        id=uuid4(), series_id=series.id, **doc, version=1, status="review"
                    )
                )
        await session.commit()
        actor_id = actor.id
    # Capture hashes from actual stored representations, as the operational snapshot does.
    async with factory() as session:
        works = []
        for row in await session.scalars(select(VideoDramaSeries).order_by(VideoDramaSeries.slug)):
            docs = list(
                await session.scalars(
                    select(VideoDramaDoc).where(VideoDramaDoc.series_id == row.id)
                )
            )
            candidates = [
                {
                    "kind": doc.kind,
                    "chapter_number": doc.chapter_number,
                    "body_md": doc.body_md + "\n製作修訂：中文字幕採可開關 CC。",
                    "body_json": copy.deepcopy(doc.body_json),
                }
                for doc in docs
            ]
            works.append(
                {
                    "slug": row.slug,
                    "expected_series_sha256": syncer.bundle_hash(syncer.row_snapshot(row)),
                    "expected_documents_sha256": syncer.documents_hash(docs),
                    "visual_tier": "clips",
                    "series_updates": {"premise": row.premise + " 製作修訂。", "note": None},
                    "documents": candidates,
                }
            )
    return {"schema_version": 1, "source_git_sha": "a" * 40, "works": works}, actor_id


async def counts(session: AsyncSession) -> list[int]:
    return [
        int(await session.scalar(select(func.count()).select_from(table)) or 0) for table in TABLES
    ]


def full_snapshot(row: Any) -> dict[str, Any]:
    return {column.name: getattr(row, column.name) for column in row.__table__.columns}


async def test_dry_run_keeps_all_rows_and_even_unflushed_caller_state(factory, seeded, syncer):
    bundle, _ = seeded
    async with factory() as session:
        pending = User(email="still-unflushed@example.test")
        session.add(pending)
        report = await syncer.sync_revisions(session, bundle)
        assert pending in session.new
        assert [row["action"] for row in report] == ["revise", "revise"]
        await session.commit()
        assert await counts(session) == [2, 12, 0, 0, 0, 0, 0]
        assert {row.visual_tier for row in await session.scalars(select(VideoDramaSeries))} == {
            "hybrid"
        }


async def test_apply_preserves_history_settings_and_identity_without_worker_jobs(
    factory, seeded, syncer
):
    bundle, actor_id = seeded
    async with factory() as session:
        actor = await session.get(User, actor_id)
        originals = {
            row.id: full_snapshot(row) for row in await session.scalars(select(VideoDramaDoc))
        }
        old_series = {
            row.id: full_snapshot(row) for row in await session.scalars(select(VideoDramaSeries))
        }
        settings = await session.get(VideoAutomationSettings, 1)
        original_settings = full_snapshot(settings)
        reports = await syncer.sync_revisions(session, bundle, actor=actor)
        await session.commit()
    async with factory() as session:
        assert await counts(session) == [2, 24, 0, 0, 0, 0, 2]
        assert full_snapshot(await session.get(VideoAutomationSettings, 1)) == original_settings
        docs = list(await session.scalars(select(VideoDramaDoc)))
        assert all(full_snapshot(row) == originals[row.id] for row in docs if row.id in originals)
        assert all(row.status == "review" and row.decided_at is None for row in docs)
        assert all(row.decided_by_user_id is None for row in docs)
        assert len([row for row in docs if row.version == 2]) == 12
        for series in await session.scalars(select(VideoDramaSeries)):
            old = old_series[series.id]
            actual = full_snapshot(series)
            for changed in ("visual_tier", "premise", "note", "updated_at"):
                actual.pop(changed)
                old.pop(changed)
            assert actual == old
            assert series.visual_tier == "clips" and series.hands_off is False
            work = next(work for work in bundle["works"] if work["slug"] == series.slug)
            assert series.premise == work["series_updates"]["premise"]
            assert series.note is None
            source = {(doc["kind"], doc["chapter_number"]): doc for doc in work["documents"]}
            for doc in (doc for doc in docs if doc.series_id == series.id and doc.version == 2):
                assert doc.body_md == source[(doc.kind, doc.chapter_number)]["body_md"]
                assert doc.body_json == source[(doc.kind, doc.chapter_number)]["body_json"]
            # Even if the site were enabled later, the newest documents still require approval.
            enabled = VideoAutomationSettings(**{**DEFAULT_DRAMA, "drama_enabled": True})
            assert (
                next_job_for(
                    series,
                    [doc for doc in docs if doc.series_id == series.id],
                    [],
                    enabled,
                    started_this_month=0,
                )
                is None
            )
        audits = list(await session.scalars(select(AdminAuditLog)))
        for audit in audits:
            assert audit.actor_user_id == actor_id and audit.action == syncer.ACTION
            meta = audit.metadata_json
            report = next(row for row in reports if audit.target == f"video-series:{row['slug']}")
            assert meta["before"] == report["before"] and meta["after"] == report["after"]
            assert meta["bundle_sha256"] == syncer.bundle_hash(bundle)
            assert meta["source_git_sha"] == bundle["source_git_sha"]
            assert meta["series_updates"] == report["series_updates"]
            assert meta["settings_sha256"] == syncer.bundle_hash(syncer.row_snapshot(settings))
            assert meta["approval_granted"] is False and meta["generation_started"] is False
            assert all(
                row["before_version"] == 1 and row["version"] == 2 for row in meta["revisions"]
            )


@pytest.mark.parametrize("change", ["title", "document", "approved"])
async def test_last_work_collision_stages_no_partial_writes(factory, seeded, syncer, change):
    bundle, actor_id = seeded
    async with factory() as session:
        row = await session.scalar(
            select(VideoDramaSeries).where(VideoDramaSeries.slug == bundle["works"][-1]["slug"])
        )
        doc = await session.scalar(
            select(VideoDramaDoc).where(
                VideoDramaDoc.series_id == row.id, VideoDramaDoc.kind == "setting"
            )
        )
        if change == "title":
            row.title = "Owner changed this after the snapshot"
        elif change == "document":
            doc.body_md += "\nOwner's new draft"
        else:
            doc.status = "approved"
        await session.commit()
        actor = await session.get(User, actor_id)
        with pytest.raises(ValueError, match="snapshot hash differs|undecided review"):
            await syncer.sync_revisions(session, bundle, actor=actor)
        assert not session.new and not session.dirty
        await session.commit()
        assert await counts(session) == [2, 12, 0, 0, 0, 0, 0]
        assert {row.visual_tier for row in await session.scalars(select(VideoDramaSeries))} == {
            "hybrid"
        }


async def test_idempotent_replay_requires_exact_post_state(factory, seeded, syncer):
    bundle, actor_id = seeded
    async with factory() as session:
        actor = await session.get(User, actor_id)
        await syncer.sync_revisions(session, bundle, actor=actor)
        await session.commit()
    async with factory() as session:
        actor = await session.get(User, actor_id)
        reports = await syncer.sync_revisions(session, bundle, actor=actor)
        assert {row["action"] for row in reports} == {"unchanged"}
        await session.commit()
        assert await counts(session) == [2, 24, 0, 0, 0, 0, 2]
        doc = await session.scalar(select(VideoDramaDoc).where(VideoDramaDoc.version == 2))
        doc.body_md += "\nLater owner edit"
        await session.commit()
        with pytest.raises(ValueError, match="previously synchronized work has changed"):
            await syncer.sync_revisions(session, bundle, actor=actor)
        assert not session.new


async def test_bootstrap_admin_and_optional_metadata_patch(factory, seeded, syncer, monkeypatch):
    bundle, actor_id = seeded
    bundle = copy.deepcopy(bundle)
    for work in bundle["works"]:
        del work["series_updates"]
    monkeypatch.setattr(
        "app.config.get_settings",
        lambda: SimpleNamespace(admin_email_set={"drama-sync@example.test"}),
    )
    async with factory() as session:
        actor = await session.get(User, actor_id)
        actor.is_admin = False
        await session.commit()
        original = {
            row.slug: (row.premise, row.note)
            for row in await session.scalars(select(VideoDramaSeries))
        }
        reports = await syncer.sync_revisions(session, bundle, actor=actor)
        await session.commit()
        assert all(row["series_updates"] == {"visual_tier": "clips"} for row in reports)
        for row in await session.scalars(select(VideoDramaSeries)):
            assert (row.premise, row.note) == original[row.slug]
        assert await counts(session) == [2, 24, 0, 0, 0, 0, 2]


async def test_apply_locks_actor_without_deadlocking_audit_foreign_keys(
    factory, seeded, syncer, monkeypatch
):
    bundle, actor_id = seeded
    statements = []
    async with factory() as session:
        actor = await session.get(User, actor_id)
        original_scalar = session.scalar
        original_scalars = session.scalars

        async def scalar(statement, *args, **kwargs):
            statements.append(str(statement.compile(dialect=postgresql.dialect())))
            return await original_scalar(statement, *args, **kwargs)

        async def scalars(statement, *args, **kwargs):
            statements.append(str(statement.compile(dialect=postgresql.dialect())))
            return await original_scalars(statement, *args, **kwargs)

        monkeypatch.setattr(session, "scalar", scalar)
        monkeypatch.setattr(session, "scalars", scalars)
        await syncer.sync_revisions(session, bundle, actor=actor)
        actor_select = next(sql for sql in statements if "FROM users " in sql)
        # SHARE stops revocation, while another admin request's audit FK can take KEY SHARE.
        assert actor_select.endswith("FOR SHARE")
        for table in ("video_automation_settings", "video_drama_series", "video_drama_docs"):
            assert any(f"FROM {table} " in sql and sql.endswith("FOR UPDATE") for sql in statements)


@pytest.mark.parametrize("state", ["deleted", "permanent", "temporary", "expired"])
async def test_admin_account_restrictions_match_login(factory, seeded, syncer, state):
    bundle, actor_id = seeded
    async with factory() as session:
        actor = await session.get(User, actor_id)
        now = datetime.now(UTC)
        if state == "deleted":
            actor.deleted_at = now
        else:
            actor.suspended_at = now - timedelta(days=2)
            if state != "permanent":
                actor.suspended_until = now + timedelta(days=1 if state == "temporary" else -1)
        await session.commit()
        if state == "expired":
            await syncer.sync_revisions(session, bundle, actor=actor)
            await session.commit()
            assert await counts(session) == [2, 24, 0, 0, 0, 0, 2]
        else:
            with pytest.raises(ValueError, match="active administrator"):
                await syncer.sync_revisions(session, bundle, actor=actor)
            assert not session.new
            assert await counts(session) == [2, 12, 0, 0, 0, 0, 0]


@pytest.mark.parametrize(
    "blocker",
    [
        "enabled",
        "active",
        "hands_off",
        "episode",
        "request",
        "discussion",
        "inactive_admin",
        "not_admin",
    ],
)
async def test_preexisting_production_or_discussion_blocks_sync(factory, seeded, syncer, blocker):
    bundle, actor_id = seeded
    async with factory() as session:
        actor = await session.get(User, actor_id)
        series = await session.scalar(select(VideoDramaSeries))
        if blocker == "enabled":
            (await session.get(VideoAutomationSettings, 1)).drama_enabled = True
        elif blocker == "active":
            series.status = "active"
        elif blocker == "hands_off":
            series.hands_off = True
        elif blocker == "episode":
            session.add(
                VideoDramaEpisode(series_id=series.id, number=1, chapter_number=1, title="Existing")
            )
        elif blocker == "request":
            session.add(VideoDramaRequest(series_id=series.id, premise="Already queued"))
        elif blocker == "discussion":
            session.add(
                VideoDramaMessage(
                    series_id=series.id, subject="setting", author="owner", body_md="Please revise"
                )
            )
        elif blocker == "inactive_admin":
            actor.is_active = False
        else:
            actor.is_admin = False
        await session.commit()
        before = await counts(session)
        with pytest.raises(ValueError):
            await syncer.sync_revisions(session, bundle, actor=actor)
        assert not session.new
        await session.commit()
        assert await counts(session) == before


@pytest.mark.parametrize(
    "malformed",
    [
        "missing",
        "duplicate",
        "body",
        "judge",
        "unlisted_field",
        "null_premise",
        "wrong_tier",
        "duplicate_slug",
    ],
)
async def test_schema_and_document_shape_validate_before_any_write(
    factory, seeded, syncer, malformed
):
    bundle, actor_id = seeded
    bundle = copy.deepcopy(bundle)
    work = bundle["works"][-1]
    if malformed == "missing":
        work["documents"].pop()
    elif malformed == "duplicate":
        work["documents"][-1] = work["documents"][0]
    elif malformed == "body":
        work["documents"][0]["body_json"] = {}
    elif malformed == "judge":
        work["documents"][0]["judge"] = None
    elif malformed == "unlisted_field":
        work["series_updates"]["hands_off"] = True
    elif malformed == "null_premise":
        work["series_updates"]["premise"] = None
    elif malformed == "wrong_tier":
        work["visual_tier"] = "hybrid"
    else:
        work["slug"] = bundle["works"][0]["slug"]
    async with factory() as session:
        actor = await session.get(User, actor_id)
        with pytest.raises(ValueError):
            await syncer.sync_revisions(session, bundle, actor=actor)
        assert not session.new and not session.dirty
        await session.commit()
        assert await counts(session) == [2, 12, 0, 0, 0, 0, 0]


async def test_cli_transaction_rolls_back_even_after_all_mutations_flush(
    factory, seeded, syncer, monkeypatch
):
    bundle, _ = seeded

    async def dispose():
        pass

    original = syncer.sync_revisions

    async def fail_after_flush(*args, **kwargs):
        await original(*args, **kwargs)
        raise RuntimeError("Simulated failure before commit")

    monkeypatch.setattr("app.db.SessionFactory", factory)
    monkeypatch.setattr("app.db.engine", SimpleNamespace(dispose=dispose))
    monkeypatch.setattr(syncer, "sync_revisions", fail_after_flush)
    args = argparse.Namespace(
        apply=True,
        expected_sha256=syncer.bundle_hash(bundle),
        actor_email="drama-sync@example.test",
    )
    with pytest.raises(RuntimeError, match="before commit"):
        await syncer._run(args, bundle)
    async with factory() as session:
        assert await counts(session) == [2, 12, 0, 0, 0, 0, 0]
        assert {row.visual_tier for row in await session.scalars(select(VideoDramaSeries))} == {
            "hybrid"
        }


async def test_apply_without_exact_reviewed_bundle_hash_never_opens_database(
    seeded, syncer, monkeypatch
):
    bundle, _ = seeded

    def forbidden():
        raise AssertionError("Must not access the database")

    monkeypatch.setattr("app.db.SessionFactory", forbidden)
    for expected in (None, "0" * 64):
        args = argparse.Namespace(apply=True, expected_sha256=expected, actor_email=None)
        with pytest.raises(ValueError, match="exact bundle"):
            await syncer._run(args, bundle)


async def test_cli_postgres_dry_run_enters_read_only_transaction_before_queries(
    seeded, syncer, monkeypatch
):
    bundle, _ = seeded
    events = []

    class ReadOnlySession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_):
            pass

        def begin(self):
            events.append("begin")
            return self

        def get_bind(self):
            return SimpleNamespace(dialect=SimpleNamespace(name="postgresql"))

        async def execute(self, statement):
            events.append(str(statement))

    async def checked_dry_run(session, plan, *, actor):
        assert actor is None
        assert events == ["begin", "SET TRANSACTION READ ONLY"]
        events.append("preflight")
        return []

    async def dispose():
        events.append("disposed")

    monkeypatch.setattr("app.db.SessionFactory", ReadOnlySession)
    monkeypatch.setattr("app.db.engine", SimpleNamespace(dispose=dispose))
    monkeypatch.setattr(syncer, "sync_revisions", checked_dry_run)
    await syncer._run(argparse.Namespace(apply=False), bundle)
    assert events == ["begin", "SET TRANSACTION READ ONLY", "preflight", "disposed"]
