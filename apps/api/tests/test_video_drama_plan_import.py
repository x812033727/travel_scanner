"""Authored plans appear for review atomically and never become worker jobs on import."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import shutil
import sys
from collections.abc import AsyncIterator
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User, VideoProject, VideoReview
from app.video_automation.models import (
    DEFAULT_DRAMA,
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.series import next_job_for

ROOT = Path(__file__).resolve().parents[3]
PACK_ROOT = ROOT / "docs/videos/series-plans"
PACKS = sorted(
    path.parent
    for batch in ("binge-five-20260928", "claude-binge-five-20260928")
    for path in (PACK_ROOT / batch).glob("*/series-request.json")
)
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
def importer() -> ModuleType:
    name = "test_import_drama_plans_module"
    spec = importlib.util.spec_from_file_location(name, ROOT / "ops/video/import_drama_plans.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def bundle(importer: ModuleType) -> dict[str, Any]:
    assert len(PACKS) == 10
    return importer.load_packs(PACKS)


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


async def counts(session: AsyncSession) -> list[int]:
    return [
        int(await session.scalar(select(func.count()).select_from(table)) or 0) for table in TABLES
    ]


async def admin(session: AsyncSession) -> User:
    actor = User(email="drama-import@example.test", is_active=True, is_admin=True)
    session.add(actor)
    await session.commit()
    return actor


def copied_pack(tmp_path: Path) -> Path:
    source = PACK_ROOT / "binge-five-20260928/wedding-reckoning"
    destination = tmp_path / source.name
    shutil.copytree(source, destination)
    return destination


def rewrite_payload(pack: Path, name: str, payload: dict[str, Any]) -> None:
    """Keep receipt valid so malformed-content tests reach schema validation."""
    content = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    (pack / name).write_text(content, encoding="utf-8", newline="\n")
    manifest_path = pack / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][name] = hashlib.sha256(content.encode("utf-8")).hexdigest()
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")


async def test_dry_run_is_read_only_including_caller_pending_changes(factory, importer, bundle):
    async with factory() as session:
        pending = User(email="unflushed@example.test")
        session.add(pending)
        report = await importer.import_plans(session, bundle)
        assert pending in session.new
        assert len(report) == 10
        assert {row["action"] for row in report} == {"create"}
        assert sum(row["documents"] for row in report) == 60
        # Even a caller committing after the dry run must not create imported records.
        await session.commit()
        assert await counts(session) == [0] * len(TABLES)


async def test_real_packages_import_as_review_docs_and_replay_without_jobs(
    factory, importer, bundle
):
    async with factory() as session:
        actor = await admin(session)
        report = await importer.import_plans(session, bundle, actor=actor)
        assert {row["action"] for row in report} == {"create"}
        await session.commit()

        rows = list(await session.scalars(select(VideoDramaSeries)))
        docs = list(await session.scalars(select(VideoDramaDoc)))
        audits = list(await session.scalars(select(AdminAuditLog)))
        assert await counts(session) == [10, 60, 0, 0, 0, 0, 10]
        assert {row.slug for row in rows} == {path.name for path in PACKS}
        assert {row.status for row in rows} == {"setting"}
        assert all(row.hands_off is False and row.created_by_user_id == actor.id for row in rows)
        assert all(doc.status == "review" and doc.version == 1 for doc in docs)
        assert all(doc.decided_at is None and doc.decided_by_user_id is None for doc in docs)

        settings = VideoAutomationSettings(**{**DEFAULT_DRAMA, "drama_enabled": True})
        for row in rows:
            work_docs = [doc for doc in docs if doc.series_id == row.id]
            source_work = next(
                work for work in bundle["works"] if work["request"]["slug"] == row.slug
            )
            source_docs = {
                (doc["kind"], doc["chapter_number"]): doc for doc in source_work["documents"]
            }
            assert len(work_docs) == 6
            for doc in work_docs:
                source_doc = source_docs[(doc.kind, doc.chapter_number)]
                assert doc.body_md == source_doc["body_md"]
                assert doc.body_json == source_doc["body_json"]
            assert next_job_for(row, work_docs, [], settings, started_this_month=0) is None
        assert {audit.action for audit in audits} == {"video_series_plans_imported"}
        assert {audit.target for audit in audits} == {f"video-series:{row.slug}" for row in rows}
        for audit in audits:
            work = next(
                work
                for work in bundle["works"]
                if audit.target == f"video-series:{work['request']['slug']}"
            )
            assert audit.actor_user_id == actor.id
            assert audit.metadata_json["source"] == work["source"]
            assert audit.metadata_json["work_sha256"] == importer.bundle_hash(work)
            assert audit.metadata_json["bundle_sha256"] == importer.bundle_hash(bundle)

        rerun = await importer.import_plans(session, bundle, actor=actor)
        await session.commit()
        assert {row["action"] for row in rerun} == {"unchanged"}
        assert await counts(session) == [10, 60, 0, 0, 0, 0, 10]


@pytest.mark.parametrize("change", ["title", "approved_document", "edited_document"])
async def test_collision_in_last_work_refuses_entire_batch(factory, importer, bundle, change):
    last_only = {"schema_version": 1, "works": [bundle["works"][-1]]}
    async with factory() as session:
        actor = await admin(session)
        await importer.import_plans(session, last_only, actor=actor)
        await session.commit()
        row = await session.scalar(select(VideoDramaSeries))
        doc = await session.scalar(select(VideoDramaDoc).where(VideoDramaDoc.kind == "setting"))
        assert row is not None and doc is not None
        if change == "title":
            row.title = "Owner changed the title"
        elif change == "approved_document":
            doc.status = "approved"
        else:
            doc.body_md += "\nOwner revision."
        await session.commit()

        with pytest.raises(ValueError, match="existing work differs"):
            await importer.import_plans(session, bundle, actor=actor)
        # Committing after rejection catches any writes staged before preflight finished.
        assert not session.new
        await session.commit()
        assert await counts(session) == [1, 6, 0, 0, 0, 0, 1]
        if change == "title":
            assert row.title == "Owner changed the title"
        elif change == "approved_document":
            assert doc.status == "approved"
        elif change == "edited_document":
            assert doc.body_md.endswith("Owner revision.")


async def test_caller_rollback_removes_whole_import(factory, importer, bundle):
    async with factory() as session:
        actor = await admin(session)
        await importer.import_plans(session, bundle, actor=actor)
        assert await counts(session) == [10, 60, 0, 0, 0, 0, 10]
        await session.rollback()
    async with factory() as session:
        assert await counts(session) == [0] * len(TABLES)


@pytest.mark.parametrize("name", ["series-request.json", "documents.json"])
def test_source_manifest_detects_tampering(tmp_path, importer, name):
    pack = copied_pack(tmp_path)
    target = pack / name
    target.write_text(target.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="manifest hash mismatch"):
        importer.load_packs([pack])


def test_windows_line_endings_preserve_receipt_verification(tmp_path, importer):
    pack = copied_pack(tmp_path)
    for name in ("series-request.json", "documents.json"):
        target = pack / name
        target.write_bytes(target.read_text(encoding="utf-8").replace("\n", "\r\n").encode("utf-8"))
    result = importer.load_packs([pack])
    assert len(result["works"]) == 1


@pytest.mark.parametrize("problem", ["missing", "duplicate", "invalid_body", "hands_off"])
def test_malformed_pack_rejected_even_with_valid_receipt(tmp_path, importer, problem):
    pack = copied_pack(tmp_path)
    name = "series-request.json" if problem == "hands_off" else "documents.json"
    payload = json.loads((pack / name).read_text(encoding="utf-8"))
    if problem == "hands_off":
        payload["hands_off"] = True
    elif problem == "missing":
        payload["documents"].pop()
    elif problem == "duplicate":
        payload["documents"].append(payload["documents"][0])
    else:
        payload["documents"][0]["body_json"] = {}
    rewrite_payload(pack, name, payload)
    with pytest.raises(ValueError):
        importer.load_packs([pack])


async def test_bundle_validation_precedes_all_writes(factory, importer, bundle):
    invalid = copy.deepcopy(bundle)
    invalid["works"][-1]["documents"].pop()
    async with factory() as session:
        actor = await admin(session)
        with pytest.raises(ValueError):
            await importer.import_plans(session, invalid, actor=actor)
        await session.commit()
        assert await counts(session) == [0] * len(TABLES)


def test_duplicate_slugs_rejected(importer):
    with pytest.raises(ValueError, match="duplicate work"):
        importer.load_packs([PACKS[0], PACKS[0]])
