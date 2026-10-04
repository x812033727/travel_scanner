"""Real long-anime source import is atomic, replayable, and cannot launch production."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import sys
from collections.abc import AsyncIterator, Callable
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from sqlalchemy import event, func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db import Base
from app.models import AdminAuditLog, User, VideoProject
from app.video_automation.models import (
    DEFAULT_DRAMA,
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoDramaSeries,
)
from app.video_automation.planning import (
    ACTION,
    bundle_hash,
    import_plan,
    prepare_bundle,
    validate_bundle,
)
from app.video_automation.series import next_job_for

PACK = Path(__file__).resolve().parents[3] / "docs/videos/series-plans/borrowed-dawn"
TABLES = (
    VideoDramaSeries,
    VideoDramaDoc,
    VideoDramaEpisode,
    VideoDramaRequest,
    VideoProject,
    AdminAuditLog,
)


@pytest.fixture(scope="module")
def source_bundle() -> dict[str, Any]:
    return prepare_bundle(PACK)


@pytest.fixture
def bundle(source_bundle: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(source_bundle)


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
    return [int(await session.scalar(select(func.count()).select_from(t)) or 0) for t in TABLES]


async def admin(session: AsyncSession) -> User:
    actor = User(email="anime-review@example.test", is_active=True, is_admin=True)
    session.add(actor)
    await session.commit()
    return actor


def replace_file(bundle: dict[str, Any], name: str, raw: str) -> None:
    """Change a receipt too, so semantic mutation tests cannot pass on a hash guard alone."""
    bundle["files"][name] = raw
    manifest = json.loads(bundle["files"]["manifest.json"])
    for group in ("source_files", "support_files", "generated_files"):
        if name in manifest[group]:
            manifest[group][name] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    bundle["files"]["manifest.json"] = json.dumps(manifest, ensure_ascii=False)


def mutate_json(
    bundle: dict[str, Any], name: str, change: Callable[[dict[str, Any]], None]
) -> None:
    doc = json.loads(bundle["files"][name])
    change(doc)
    replace_file(bundle, name, json.dumps(doc, ensure_ascii=False))


def test_real_source_preserves_original_runtime_and_complete_documents(
    bundle: dict[str, Any],
) -> None:
    result = validate_bundle(bundle)
    assert result.values["target_minutes"] == 22
    assert result.values["lead"] == "ensemble"
    assert result.values["category"] == "anime"
    assert result.values["planning_spec"] == result.plan
    assert len(result.documents) == 12 and len(result.episodes) == 120
    assert sum(len(e["high_tension"]) for e in result.episodes) == 240
    assert result.episodes[-1]["closed_ending"] is True
    assert result.episodes[-1]["tension"][-1] == 2
    reordered = dict(reversed(list(bundle.items())))
    assert bundle_hash(reordered) == bundle_hash(bundle)


@pytest.mark.parametrize("name", ["plan.json", "README.md", "season-10.md", "continuity.csv"])
def test_each_receipt_group_rejects_bad_hash(bundle: dict[str, Any], name: str) -> None:
    bundle["files"][name] += "\n"
    with pytest.raises(ValueError, match="manifest hash mismatch"):
        validate_bundle(bundle)


@pytest.mark.parametrize("mutation", ["missing", "path", "version_bool", "source", "oversized"])
def test_portable_wire_refuses_missing_paths_and_invalid_limits(
    bundle: dict[str, Any], mutation: str
) -> None:
    if mutation == "missing":
        del bundle["files"]["review.md"]
    elif mutation == "path":
        bundle["files"]["../outside"] = "unsafe"
    elif mutation == "version_bool":
        bundle["schema_version"] = True
    elif mutation == "source":
        bundle["source"] = "docs/videos/series-plans/../another"
    else:
        bundle["files"]["README.md"] = "x" * (2 * 1024 * 1024 + 1)
    with pytest.raises(ValueError):
        validate_bundle(bundle)


# Windows lets an account create a symbolic link only with SeCreateSymbolicLinkPrivilege
# (elevation or Developer Mode), but lets any account create a directory junction.
ERROR_PRIVILEGE_NOT_HELD = 1314
LINKS = ("symlink", "junction")
windows_only = pytest.mark.skipif(
    sys.platform != "win32", reason="directory junctions exist only on Windows"
)


def link_readme(pack: Path, kind: str) -> None:
    """Swap README.md for a real link out of the pack, so the refusal reads actual metadata."""
    entry = pack / "README.md"
    entry.unlink()
    if kind == "symlink":
        try:
            entry.symlink_to(PACK / "README.md")
        except OSError as exc:
            if getattr(exc, "winerror", None) != ERROR_PRIVILEGE_NOT_HELD:
                raise
            pytest.skip(
                "this Windows account cannot create symbolic links (WinError 1314, no "
                "SeCreateSymbolicLinkPrivilege); the junction case refuses a real link here"
            )
    elif sys.platform == "win32":
        import _winapi

        outside = pack.parent / "outside"
        outside.mkdir()
        _winapi.CreateJunction(str(outside), str(entry))
        assert entry.is_junction()


@pytest.mark.parametrize(
    "mutation",
    ["symlink", pytest.param("junction", marks=windows_only), "missing", "unexpected"],
)
def test_prepare_checks_actual_directory(tmp_path: Path, mutation: str) -> None:
    pack = tmp_path / PACK.name
    shutil.copytree(PACK, pack)
    if mutation in LINKS:
        link_readme(pack, mutation)
    elif mutation == "missing":
        (pack / "season-10.md").unlink()
    else:
        (pack / "extra.json").write_text("{}")
    with pytest.raises(ValueError, match="symlinks" if mutation in LINKS else "unexpected"):
        prepare_bundle(pack)


@windows_only
def test_prepare_refuses_a_pack_that_is_itself_a_junction(tmp_path: Path) -> None:
    """The bundle's source names the pack directory, so its bytes must not come from elsewhere."""
    elsewhere = tmp_path / "elsewhere"
    shutil.copytree(PACK, elsewhere)
    pack = tmp_path / PACK.name
    if sys.platform == "win32":
        import _winapi

        _winapi.CreateJunction(str(elsewhere), str(pack))
    assert pack.is_junction() and not pack.is_symlink()
    with pytest.raises(ValueError, match="pack must be a real directory"):
        prepare_bundle(pack)


@pytest.mark.parametrize(
    "field,value",
    [
        ("planned_episodes", 119),
        ("planned_episodes", True),
        ("episodes_per_chapter", 10),
        ("lead", "dual-male"),
        ("genre", "xianxia-bonds"),
        ("kind", "story"),
        ("category", "drama"),
        ("open_ended", True),
    ],
)
def test_receipt_cannot_hide_changed_series_contract(
    bundle: dict[str, Any], field: str, value: Any
) -> None:
    mutate_json(bundle, "plan.json", lambda doc: doc.update({field: value}))
    with pytest.raises(ValueError):
        validate_bundle(bundle)


def test_receipt_cannot_hide_shortened_runtime(bundle: dict[str, Any]) -> None:
    mutate_json(bundle, "plan.json", lambda p: p["runtime"].update(story_minutes=8))
    with pytest.raises(ValueError, match="runtime"):
        validate_bundle(bundle)


@pytest.mark.parametrize("name", ["plan.json", "authoring-contract.json"])
def test_source_schema_version_is_not_a_boolean(bundle, name):
    mutate_json(bundle, name, lambda doc: doc.update(schema_version=True))
    with pytest.raises(ValueError, match="schema version"):
        validate_bundle(bundle)


@pytest.mark.parametrize(
    "mutation", ["empty", "duplicate", "note", "duration", "finale", "ensemble"]
)
def test_source_cannot_erase_or_rewrite_known_production_gaps(bundle, mutation):
    def change(plan):
        gaps = plan["production_support"]["gaps"]
        if mutation == "empty":
            gaps.clear()
        elif mutation == "duplicate":
            gaps.append(copy.deepcopy(gaps[0]))
        elif mutation == "note":
            gaps[0]["note"] = ""
        elif mutation == "duration":
            next(g for g in gaps if g["code"] == "episode-duration")[
                "current_drama_max_minutes"
            ] = 22
        elif mutation == "finale":
            next(g for g in gaps if g["code"] == "closed-finale")[
                "current_worker_min_last_tension"
            ] = 2
        else:
            next(g for g in gaps if g["code"] == "ensemble-retention")["current_genre"] = "story"

    mutate_json(bundle, "plan.json", change)
    with pytest.raises(ValueError, match="production gap"):
        validate_bundle(bundle)


def test_character_id_format_matches_the_source_contract(bundle):
    mutate_json(bundle, "setting.json", lambda s: s["characters"][0].update(id="INVALID/CAST"))
    with pytest.raises(ValueError, match="character ID format"):
        validate_bundle(bundle)


@pytest.mark.parametrize(
    "mutation",
    [
        "cast",
        "cast_duplicate",
        "premature_payoff",
        "unknown_setup",
        "flat_curve",
        "bool_curve",
        "missing_tension",
        "same_event",
        "state",
        "number_bool",
        "missing_episode",
        "local_payoff",
        "ending_type",
        "closed_early",
    ],
)
def test_rehashed_narrative_errors_are_refused(bundle: dict[str, Any], mutation: str) -> None:
    def change(season: dict[str, Any]) -> None:
        e = season["episodes"][0]
        if mutation == "cast":
            e["characters"] = ["invented-person"]
        elif mutation == "cast_duplicate":
            e["characters"].append(e["characters"][0])
        elif mutation == "premature_payoff":
            e["payoffs"] = ["m02"]
        elif mutation == "unknown_setup":
            e["setups"].append("m99")
        elif mutation == "flat_curve":
            e["tension"] = [4] * 5
        elif mutation == "bool_curve":
            e["tension"][0] = True
        elif mutation == "missing_tension":
            e["high_tension"].pop()
        elif mutation == "same_event":
            e["high_tension"][1]["event"] = e["high_tension"][0]["event"]
        elif mutation == "state":
            e["state"].pop("evidence")
        elif mutation == "number_bool":
            e["number"] = True
        elif mutation == "missing_episode":
            season["episodes"].pop()
        elif mutation == "local_payoff":
            for row in season["episodes"][:4]:
                row["payoffs"] = []
                row["general_payoffs"] = []
        elif mutation == "ending_type":
            season["episodes"][1]["cliffhanger"]["type"] = e["cliffhanger"]["type"]
        else:
            e["closed_ending"] = True

    mutate_json(bundle, "season-01.json", change)
    with pytest.raises(ValueError):
        validate_bundle(bundle)


@pytest.mark.parametrize(
    "mutation", ["finale_danger", "finale_open", "thread_final", "thread_dates"]
)
def test_fully_closed_finale_and_thread_recovery_are_required(
    bundle: dict[str, Any], mutation: str
) -> None:
    def final(season: dict[str, Any]) -> None:
        e = season["episodes"][-1]
        if mutation == "finale_danger":
            e["cliffhanger"]["type"] = "danger"
            e["tension"][-1] = 5
        elif mutation == "finale_open":
            e["closed_ending"] = False
        else:
            e["payoffs"].remove("m03")

    if mutation == "thread_dates":
        mutate_json(
            bundle,
            "setting.json",
            lambda s: s["mysteries"][0].update(introduced_in=49, resolved_in=48),
        )
    else:
        mutate_json(bundle, "season-10.json", final)
    with pytest.raises(ValueError):
        validate_bundle(bundle)


def test_rebuilt_finale_twins_cannot_conflict_with_declared_finale_tension(bundle):
    season = json.loads(bundle["files"]["season-10.json"])
    old_curve = season["episodes"][-1]["tension"].copy()
    season["episodes"][-1]["tension"][-1] = 1
    new_curve = season["episodes"][-1]["tension"]
    markdown = bundle["files"]["season-10.md"].replace(
        "**五段張力：**" + " → ".join(map(str, old_curve)),
        "**五段張力：**" + " → ".join(map(str, new_curve)),
    )
    assert markdown != bundle["files"]["season-10.md"]
    replace_file(bundle, "season-10.json", json.dumps(season, ensure_ascii=False))
    replace_file(bundle, "season-10.md", markdown)
    documents = json.loads(bundle["files"]["documents.json"])
    final_document = documents["documents"][-1]
    assert final_document["kind"] == "chapter" and final_document["chapter_number"] == 10
    final_document.update(body_json=season, body_md=markdown)
    replace_file(bundle, "documents.json", json.dumps(documents, ensure_ascii=False))
    # All affected source hashes and readable/JSON twins now agree. Only the
    # truthful production limitation still declares the actual closing score 2.
    with pytest.raises(ValueError, match="finale tension differs from declared"):
        validate_bundle(bundle)


@pytest.mark.parametrize("name", ["setting.md", "season-06.md", "outline.md", "continuity.csv"])
def test_rehashed_readable_document_drift_is_refused(bundle: dict[str, Any], name: str) -> None:
    replace_file(bundle, name, bundle["files"][name] + "A conflicting revision.\n")
    with pytest.raises(ValueError, match="rendered content differs"):
        validate_bundle(bundle)


def test_rehashed_structured_document_drift_is_refused(bundle: dict[str, Any]) -> None:
    mutate_json(bundle, "documents.json", lambda d: d["documents"][0].update(body_json={}))
    with pytest.raises(ValueError, match="twins differ"):
        validate_bundle(bundle)


def test_redundant_json_does_not_accept_boolean_for_episode_number(bundle: dict[str, Any]) -> None:
    mutate_json(
        bundle, "outline.json", lambda d: d["chapters"][0]["episodes"][0].update(number=True)
    )
    with pytest.raises(ValueError, match="projection differs"):
        validate_bundle(bundle)


@pytest.mark.parametrize("raw", ['{"title":"a","title":"b"}', '{"value":NaN}'])
def test_invalid_json_values_cannot_be_rehashed_into_a_valid_pack(bundle, raw):
    replace_file(bundle, "plan.json", raw)
    with pytest.raises(ValueError, match="duplicate JSON key|nonfinite"):
        validate_bundle(bundle)


async def test_dryrun_does_not_write_or_flush_caller_pending_changes(factory, bundle, monkeypatch):
    async with factory() as session:
        pending = User(email="pending-anime@example.test")
        session.add(pending)
        flush = AsyncMock(side_effect=AssertionError("dryrun attempted a flush"))
        monkeypatch.setattr(session, "flush", flush)
        writes: list[str] = []
        bind = session.get_bind()

        def record(_connection, _cursor, statement, _parameters, _context, _many):
            if statement.lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                writes.append(statement)

        event.listen(bind, "before_cursor_execute", record)
        try:
            report = await import_plan(session, bundle)
            assert report["applied"] is False and report["action"] == "create"
            assert pending in session.new and len(session.new) == 1
            assert not writes
            flush.assert_not_awaited()
        finally:
            event.remove(bind, "before_cursor_execute", record)
        await session.rollback()
        assert await counts(session) == [0] * len(TABLES)


async def test_real_import_is_paused_and_replay_keeps_all_original_source(factory, bundle):
    async with factory() as session:
        actor = await admin(session)
        report = await import_plan(session, bundle, actor=actor)
        assert report["action"] == "create" and report["sha256"] == bundle_hash(bundle)
        await session.commit()
        row = await session.scalar(select(VideoDramaSeries))
        assert row is not None
        assert row.planning_only is True and row.category == "anime"
        assert row.target_minutes == 22 and row.status == "paused" and row.lead == "ensemble"
        assert row.planning_spec == json.loads(bundle["files"]["plan.json"])
        assert row.created_by_user_id == actor.id
        assert row.hands_off is False and row.compilation is False and row.force_next is False
        docs = list(await session.scalars(select(VideoDramaDoc)))
        episodes = list(
            await session.scalars(select(VideoDramaEpisode).order_by(VideoDramaEpisode.number))
        )
        wanted = validate_bundle(bundle)
        source_docs = {(d["kind"], d.get("chapter_number", 0)): d for d in wanted.documents}
        assert len(docs) == 12
        for doc in docs:
            source = source_docs[(doc.kind, doc.chapter_number)]
            assert doc.body_md == source["body_md"] and doc.body_json == source["body_json"]
            assert doc.status == "review" and doc.decided_at is None
            assert doc.decided_by_user_id is None and doc.version == 1
        for episode, source in zip(episodes, wanted.episodes, strict=True):
            assert episode.beats == source and episode.status == "planned"
            assert episode.slug is None and episode.request_id is None
            assert episode.started_at is None and episode.finished_at is None
        audit = await session.scalar(select(AdminAuditLog))
        assert audit is not None and audit.action == ACTION and audit.actor_user_id == actor.id
        assert audit.metadata_json["bundle_sha256"] == bundle_hash(bundle)
        assert audit.metadata_json["manifest_sha256"] == wanted.manifest_sha256
        settings = VideoAutomationSettings(**{**DEFAULT_DRAMA, "drama_enabled": True})
        assert next_job_for(row, docs, episodes, settings, started_this_month=0) is None
        assert await counts(session) == [1, 12, 120, 0, 0, 1]
        replay = await import_plan(session, bundle, actor=actor)
        assert replay["action"] == "unchanged"
        await session.commit()
        assert await counts(session) == [1, 12, 120, 0, 0, 1]


@pytest.mark.parametrize(
    "mutation",
    [
        "series_title",
        "spec",
        "approval",
        "markdown",
        "structured",
        "missing_doc",
        "episode",
        "episode_status",
        "missing_episode",
        "audit",
        "audit_source",
        "request",
        "video",
    ],
)
async def test_existing_changed_plan_refuses_every_write(factory, bundle, mutation):
    async with factory() as session:
        actor = await admin(session)
        await import_plan(session, bundle, actor=actor)
        await session.commit()
        row = await session.scalar(select(VideoDramaSeries))
        doc = await session.scalar(select(VideoDramaDoc))
        episode = await session.scalar(select(VideoDramaEpisode))
        audit = await session.scalar(select(AdminAuditLog))
        assert row is not None and doc is not None and episode is not None and audit is not None
        if mutation == "series_title":
            row.title = "Owner revision"
        elif mutation == "spec":
            row.planning_spec = {"owner": "changed"}
        elif mutation == "approval":
            doc.status = "approved"
        elif mutation == "markdown":
            doc.body_md += "\nOwner changed this."
        elif mutation == "structured":
            doc.body_json = {}
        elif mutation == "missing_doc":
            await session.delete(doc)
        elif mutation == "episode":
            episode.beats = {"owner": "changed"}
        elif mutation == "episode_status":
            episode.status = "ready"
        elif mutation == "missing_episode":
            await session.delete(episode)
        elif mutation == "audit":
            audit.metadata_json = {"bundle_sha256": "wrong"}
        elif mutation == "audit_source":
            audit.metadata_json = {**audit.metadata_json, "source": "another source"}
        elif mutation == "request":
            session.add(
                VideoDramaRequest(
                    premise="Other production",
                    series_id=row.id,
                    target_minutes=3,
                    style_preset="anime-2d",
                )
            )
        else:
            session.add(
                VideoProject(
                    slug="borrowed-dawn-e001",
                    title="Other production",
                    series_slug=row.slug,
                    stage="brief drafted",
                )
            )
        await session.commit()
        before = await counts(session)
        with pytest.raises(ValueError, match="existing"):
            await import_plan(session, bundle, actor=actor)
        assert not session.new and not session.dirty and not session.deleted
        await session.commit()
        assert await counts(session) == before


async def test_caller_rollback_removes_all_imported_records(factory, bundle):
    async with factory() as session:
        actor = await admin(session)
        await import_plan(session, bundle, actor=actor)
        assert await counts(session) == [1, 12, 120, 0, 0, 1]
        await session.rollback()
    async with factory() as session:
        assert await counts(session) == [0] * len(TABLES)


async def test_orphaned_import_audit_is_not_silently_reused(factory, bundle):
    async with factory() as session:
        actor = await admin(session)
        session.add(
            AdminAuditLog(
                actor_user_id=actor.id,
                action=ACTION,
                target="video-series:borrowed-dawn",
                metadata_json={},
            )
        )
        await session.commit()
        with pytest.raises(ValueError, match="orphaned"):
            await import_plan(session, bundle, actor=actor)
        assert not session.new
        await session.commit()
        assert await counts(session) == [0, 0, 0, 0, 0, 1]


@pytest.mark.parametrize("existing", [False, True])
async def test_independent_started_request_using_exact_series_slug_collides(
    factory, bundle, existing
):
    async with factory() as session:
        actor = await admin(session)
        if existing:
            await import_plan(session, bundle, actor=actor)
            await session.commit()
        request = VideoDramaRequest(
            slug="borrowed-dawn",
            series_id=None,
            status="started",
            premise="Independent existing request",
            target_minutes=3,
            style_preset="anime-2d",
        )
        session.add(request)
        await session.commit()
        before = await counts(session)
        assert before[4] == 0  # A request can be claimed before its project is registered.
        for actor_arg in (None, actor):
            with pytest.raises(ValueError, match="production records collide"):
                await import_plan(session, bundle, actor=actor_arg)
            assert not session.new and not session.dirty and not session.deleted
        await session.commit()
        assert await counts(session) == before
        assert request.slug == "borrowed-dawn" and request.status == "started"


async def test_failure_after_parent_flush_is_fully_rolled_back(factory, bundle, monkeypatch):
    async with factory() as session:
        actor = await admin(session)
        original = session.flush
        calls = 0

        async def fail_late(*args, **kwargs):
            nonlocal calls
            calls += 1
            await original(*args, **kwargs)
            if calls == 2:
                raise RuntimeError("Interrupted after children flush")

        monkeypatch.setattr(session, "flush", fail_late)
        with pytest.raises(RuntimeError, match="Interrupted"):
            await import_plan(session, bundle, actor=actor)
        await session.rollback()
    async with factory() as session:
        assert await counts(session) == [0] * len(TABLES)


async def test_non_admin_cannot_apply(factory, bundle):
    async with factory() as session:
        actor = User(email="ordinary-anime@example.test", is_active=True, is_admin=False)
        session.add(actor)
        await session.commit()
        with pytest.raises(ValueError, match="administrator"):
            await import_plan(session, bundle, actor=actor)
        assert not session.new
        await session.commit()
        assert await counts(session) == [0] * len(TABLES)


async def test_invalid_final_document_refuses_before_database_writes(factory, bundle):
    mutate_json(bundle, "documents.json", lambda d: d["documents"].pop())
    async with factory() as session:
        actor = await admin(session)
        with pytest.raises(ValueError):
            await import_plan(session, bundle, actor=actor)
        assert not session.new
        await session.commit()
        assert await counts(session) == [0] * len(TABLES)
