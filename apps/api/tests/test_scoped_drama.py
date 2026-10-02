"""Offline regression checks for isolated, reviewed, bounded media operations.

Real SQLite ORM rows and the existing submit_job/store/meter run with a fake
provider and Redis. PostgreSQL session locking is checked separately; no test
claims to verify regional availability, image quality, or actual vendor billing.
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import fakeredis
import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy import func, inspect, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.config import Settings
from app.db import Base
from app.models import AdminAuditLog, AdminRoleAssignment, User, VideoProject, VideoReview
from app.video_automation.models import (
    VideoAutomationSettings,
    VideoDramaDoc,
    VideoDramaSeries,
)
from app.video_media import jobs, meter
from app.video_media.models import VideoMediaJob
from app.video_media.providers import Polled, Submitted
from app.video_media.settings import MediaSettings
from app.video_media.storage import MediaStore

ROOT = Path(__file__).resolve().parents[3]
PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 30


@pytest.fixture(scope="module")
def runner():
    name = "test_scoped_drama_module"
    spec = importlib.util.spec_from_file_location(name, ROOT / "ops/video/scoped_drama.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Provider:
    name = "fake"

    def __init__(self):
        self.calls = []
        self.polls = []
        self.result = Submitted(inline=PNG, content_type="image/png")

    async def submit(self, request, client):
        self.calls.append(request)
        if isinstance(self.result, Exception):
            raise self.result
        return self.result

    async def poll(self, vendor_ref, client):
        self.polls.append(vendor_ref)
        return Polled(state="running", retry_after=10)


def artifact(runner, root, name, value):
    raw = value if isinstance(value, bytes) else json.dumps(value).encode()
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return {"path": name, "sha256": runner.sha256(raw)}


@pytest_asyncio.fixture
async def case(tmp_path, runner, monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite://")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    factory = async_sessionmaker(engine, class_=runner.ScopedSession, expire_on_commit=False)
    provider = Provider()
    monkeypatch.setattr(jobs, "provider_for", lambda *_: provider)
    redis = fakeredis.aioredis.FakeRedis()
    root = tmp_path / "artifacts"
    root.mkdir()
    source = ROOT / "docs/videos/series-plans/binge-five-20260928/wedding-reckoning/source.mjs"
    manifest = {
        "schema_version": 1,
        "campaign": runner.CAMPAIGN,
        "locale": "zh-TW",
        "source": artifact(runner, root, "source.mjs", source.read_bytes()),
        "episodes": [],
        "series_documents": [],
        "budget": {"manual_reserve_usd": "10"},
        "requests": [],
    }
    async with factory() as session:
        user = User(email="scoped-admin@example.test", is_active=True, is_admin=True)
        session.add(user)
        await session.flush()
        row = VideoAutomationSettings(
            id=1, drama_enabled=False, music_enabled=True, updated_by_user_id=user.id
        )
        session.add(row)
        series = VideoDramaSeries(
            slug="wedding-reckoning",
            title="Wedding",
            premise="Test",
            kind="series",
            status="active",
        )
        session.add(series)
        await session.flush()
        for kind, chapter in (("setting", 0), ("outline", 0), ("chapter", 1)):
            body = (
                {
                    "production_design": {
                        "source_binding": {"source_sha256": runner.SOURCE_OBJECT_SHA}
                    }
                }
                if kind == "setting"
                else {}
            )
            doc = VideoDramaDoc(
                series_id=series.id,
                kind=kind,
                chapter_number=chapter,
                version=1,
                body_md=kind,
                body_json=body,
                status="approved",
                decided_at=datetime.now(UTC),
            )
            session.add(doc)
            await session.flush()
            manifest["series_documents"].append(
                {
                    "id": str(doc.id),
                    "kind": kind,
                    "chapter_number": chapter,
                    "body_sha256": runner.canonical_hash({"body_md": kind, "body_json": body}),
                }
            )
        for index, slug in enumerate(runner.SLUGS, 1):
            project = VideoProject(
                slug=slug,
                title=f"Episode {index}",
                format="drama",
                stage="script",
                series_slug="wedding-reckoning",
                episode_number=index,
            )
            session.add(project)
            await session.flush()
            script = artifact(runner, root, f"e{index}/script.md", b"Reviewed script\n")
            edit = artifact(
                runner,
                root,
                f"e{index}/edit.json",
                {
                    "source_binding": {
                        "source_object_sha256": runner.SOURCE_OBJECT_SHA,
                        "screenplay_sha256": script["sha256"],
                    },
                    "shots": [],
                },
            )
            manifest["episodes"].append({"slug": slug, "script": script, "edit": edit})
            review = VideoReview(
                project_id=project.id,
                gate="script",
                status="approved",
                summary="Reviewed",
                content_sha256=script["sha256"],
                decided_at=datetime.now(UTC),
            )
            session.add(review)
            await session.flush()
            if index == 1:
                manifest["requests"].append(
                    {
                        "id": "zhitang-sheet",
                        "kind": "image",
                        "phase": "pilot",
                        "payload": {
                            "slug": slug,
                            "prompt": "Adult Zhitang character sheet",
                            "purpose": "character_sheet",
                            "shot_id": "look-zhitang",
                            "aspect": "16:9",
                        },
                        "characters": ["zhitang"],
                        "reviews": [{"id": str(review.id), "gate": "script", "artifact": script}],
                    }
                )
        await session.commit()
        actor_id = user.id
    store = MediaStore(tmp_path / "media", max_file_bytes=10000000, max_total_bytes=50000000)
    try:
        yield SimpleNamespace(
            factory=factory,
            manifest=manifest,
            actor_id=actor_id,
            provider=provider,
            redis=redis,
            root=root,
            store=store,
            runner=runner,
        )
    finally:
        await redis.aclose()
        await engine.dispose()


def context(case, session):
    return jobs.MediaContext(
        session=session,
        redis=case.redis,
        store=case.store,
        runtime=Settings(hotspot_guide_gemini_api_key="test-key"),
        media=MediaSettings(),
        row=VideoAutomationSettings(),
    )


async def run(case, *, execute=False, manifest=None, first_shot=False):
    raw = json.dumps(manifest or case.manifest).encode()
    async with case.factory() as session:
        # Offline substitute only. CLI execution obtains a real dedicated PG lock.
        session.info["scoped_drama_lock"] = True
        return await case.runner.run_request(
            context(case, session),
            raw,
            case.root,
            (manifest or case.manifest)["requests"][0]["id"],
            actor_id=case.actor_id,
            execute=execute,
            expected=case.runner.sha256(raw),
            first_shot=first_shot,
        )


async def count(case, model):
    async with case.factory() as session:
        return await session.scalar(select(func.count()).select_from(model))


async def test_preview_has_real_timestamps_but_no_writes_or_provider_calls(case):
    result = await run(case)
    assert result["operation"] == "submit_once"
    assert result["new_reserve_usd"] == "0.134"
    assert result["settings_before_sha256"] == result["settings_after_sha256"]
    assert case.provider.calls == [] and not await case.redis.keys("*")
    assert not case.store.root.exists()
    assert await count(case, AdminAuditLog) == await count(case, VideoMediaJob) == 0


async def test_execute_uses_transient_settings_existing_service_and_ready_dedup(case):
    async with case.factory() as session:
        row = await session.get(VideoAutomationSettings, 1)
        before = case.runner.snapshot(row)
        clone = case.runner.isolated_settings(row)
        assert inspect(clone).transient and clone not in session
        assert clone.clip_model == "veo-3.1-lite-generate-preview"
    first = await run(case, execute=True)
    second = await run(case, execute=True)
    assert first["status"] == "ready" and second["operation"] == "return_ready"
    assert first["job_id"] == second["job_id"] and len(case.provider.calls) == 1
    assert await count(case, VideoMediaJob) == 1 and await count(case, AdminAuditLog) == 2
    assert await meter.used(case.redis, meter.IMAGES) == 1
    async with case.factory() as session:
        row = await session.get(VideoAutomationSettings, 1)
        assert row.drama_enabled is False and case.runner.snapshot(row) == before
        reserve = await session.scalar(
            select(AdminAuditLog).where(AdminAuditLog.action == case.runner.RESERVED)
        )
        assert reserve.metadata_json["reserved_usd"] == "0.134"
        assert reserve.metadata_json["source"]["sha256"] == case.runner.SOURCE_SHA


@pytest.mark.parametrize("change", ["source", "episode", "locale", "artifact", "escape"])
async def test_unreviewed_inputs_spend_nothing(case, change):
    manifest = copy.deepcopy(case.manifest)
    if change == "source":
        manifest["source"]["sha256"] = "0" * 64
    elif change == "episode":
        manifest["requests"][0]["payload"]["slug"] = "unrelated-work"
    elif change == "locale":
        manifest["locale"] = "ja"
    elif change == "artifact":
        (case.root / "e2/edit.json").write_text("changed")
    else:
        manifest["episodes"][0]["edit"]["path"] = "../escape.json"
    with pytest.raises((case.runner.Refused, ValidationError)):
        await run(case, execute=True, manifest=manifest)
    assert case.provider.calls == [] and await count(case, AdminAuditLog) == 0


async def test_expected_raw_hash_and_connection_lock_required(case):
    raw = json.dumps(case.manifest).encode()
    async with case.factory() as session:
        ctx = context(case, session)
        with pytest.raises(case.runner.Refused, match="lock"):
            await case.runner.run_request(
                ctx, raw, case.root, "zhitang-sheet", actor_id=case.actor_id, execute=True
            )
        session.info["scoped_drama_lock"] = True
        with pytest.raises(case.runner.Refused, match="expected-manifest"):
            await case.runner.run_request(
                ctx,
                raw,
                case.root,
                "zhitang-sheet",
                actor_id=case.actor_id,
                execute=True,
                expected="a" * 64,
            )


@pytest.mark.parametrize("change", ["inactive", "deleted", "suspended", "expired_roles"])
async def test_revoked_or_expired_admin_cannot_generate(case, change):
    async with case.factory() as session:
        user = await session.get(User, case.actor_id)
        if change == "inactive":
            user.is_active = False
        elif change == "deleted":
            user.deleted_at = datetime.now(UTC)
        elif change == "suspended":
            user.suspended_at = datetime.now(UTC)
            user.suspended_until = datetime.now(UTC) + timedelta(days=1)
        else:
            session.add(
                AdminRoleAssignment(
                    user_id=user.id,
                    role="content",
                    source="manual",
                    expires_at=datetime.now(UTC) - timedelta(days=1),
                )
            )
        await session.commit()
    with pytest.raises(case.runner.Refused, match="administrator"):
        await run(case, execute=True)
    assert case.provider.calls == []


@pytest.mark.parametrize("gate", ["script", "series", "newer_script", "dropped"])
async def test_actual_latest_gate_approvals_required(case, gate):
    async with case.factory() as session:
        if gate == "series":
            doc = await session.scalar(select(VideoDramaDoc).where(VideoDramaDoc.kind == "setting"))
            doc.status = "review"
        elif gate == "dropped":
            project = await session.scalar(
                select(VideoProject).where(VideoProject.slug == case.runner.SLUGS[0])
            )
            project.dropped_at = datetime.now(UTC)
        else:
            review = await session.scalar(select(VideoReview).where(VideoReview.gate == "script"))
            if gate == "script":
                review.status = "pending"
            else:
                session.add(
                    VideoReview(
                        project_id=review.project_id,
                        gate="script",
                        summary="New",
                        content_sha256="a" * 64,
                        status="pending",
                        created_at=datetime.now(UTC) + timedelta(seconds=1),
                    )
                )
        await session.commit()
    with pytest.raises(case.runner.Refused):
        await run(case, execute=True)
    assert case.provider.calls == []


async def test_orphan_reservation_blocks_changed_request_too(case, monkeypatch):
    async def interrupted(*args):
        raise RuntimeError("process interrupted before job row became visible")

    monkeypatch.setattr(jobs, "submit_job", interrupted)
    with pytest.raises(RuntimeError):
        await run(case, execute=True)
    assert await count(case, AdminAuditLog) == 1 and await count(case, VideoMediaJob) == 0
    changed = copy.deepcopy(case.manifest)
    changed["requests"][0]["payload"]["seed"] = 123
    with pytest.raises(case.runner.Refused, match="unknown/pending"):
        await run(case, execute=True, manifest=changed)
    assert await count(case, AdminAuditLog) == 1


async def test_other_caller_racing_with_submit_cannot_trigger_implicit_failed_retry(
    case, monkeypatch
):
    original = jobs.submit_job

    async def racing(ctx, kind, payload):
        model = jobs._model(ctx.row, kind)[1]
        fields = jobs._request_fields(payload, ctx.row, model)
        digest = jobs.request_hash({"kind": kind, "vendor": "gemini", "model": model.id, **fields})
        ctx.session.add(
            VideoMediaJob(
                slug=payload.slug,
                kind=kind,
                purpose=payload.purpose,
                shot_id=payload.shot_id,
                provider="gemini",
                model=model.id,
                request=fields,
                request_hash=digest,
                status="failed",
                attempts=1,
                polls=0,
                seconds=0,
                usd_estimate=0,
            )
        )
        await ctx.session.commit()
        return await original(ctx, kind, payload)

    monkeypatch.setattr(jobs, "submit_job", racing)
    with pytest.raises(case.runner.Refused, match="another caller"):
        await run(case, execute=True)
    assert case.provider.calls == [] and await meter.used(case.redis, meter.IMAGES) == 0
    async with case.factory() as session:
        job = await session.scalar(select(VideoMediaJob))
        assert job.status == "failed" and job.attempts == 1


@pytest.mark.parametrize("status", ["queued", "failed", "expired", "submitted"])
async def test_unknown_and_terminal_failures_are_never_resubmitted(case, status):
    await run(case, execute=True)
    async with case.factory() as session:
        job = await session.scalar(select(VideoMediaJob))
        job.status = status
        job.vendor_ref = None
        job.usd_estimate = Decimal(0)
        await session.commit()
    with pytest.raises(case.runner.Refused, match="never resubmit"):
        await run(case, execute=True)
    assert len(case.provider.calls) == 1
    async with case.factory() as session:
        total, pilot, _ = await case.runner.exposure(session, Decimal(10))
        assert total == pilot == Decimal("10.134")


async def test_resume_polls_existing_vendor_reference_without_second_reserve(case):
    case.provider.result = Submitted(vendor_ref="existing-operation")
    first = await run(case, execute=True)
    # SQLite strips timezone from DATETIME; normalize only the offline poll clock.
    original_advance = jobs.advance_job

    async def advance(ctx, job):
        if job.submitted_at is not None and job.submitted_at.tzinfo is None:
            job.submitted_at = job.submitted_at.replace(tzinfo=UTC)
        return await original_advance(ctx, job)

    from unittest.mock import patch

    with patch.object(jobs, "advance_job", advance):
        resumed = await run(case, execute=True)
    assert first["job_id"] == resumed["job_id"] and resumed["operation"] == "resume_poll"
    assert len(case.provider.calls) == 1 and case.provider.polls == ["existing-operation"]
    assert await meter.used(case.redis, meter.IMAGES) == 1


async def test_catalog_attempts_and_manual_high_water_cannot_be_refunded_to_zero(case):
    await run(case, execute=True)
    async with case.factory() as session:
        job = await session.scalar(select(VideoMediaJob))
        job.status = "failed"
        job.attempts = 3
        job.usd_estimate = 0
        reserve = await session.scalar(
            select(AdminAuditLog).where(AdminAuditLog.action == case.runner.RESERVED)
        )
        reserve.metadata_json = {**reserve.metadata_json, "manual_reserve_usd": "25"}
        await session.commit()
        total, pilot, _ = await case.runner.exposure(session, Decimal(10))
        assert total == pilot == Decimal("25.402")


@pytest.mark.parametrize("phase,reserve", [("pilot", "100"), ("episodes", "350")])
async def test_caps_include_manual_reserve_before_submission(case, phase, reserve):
    case.manifest["requests"][0]["phase"] = phase
    case.manifest["budget"]["manual_reserve_usd"] = reserve
    with pytest.raises(case.runner.Refused, match="exposure exceeds"):
        await run(case, execute=True)
    assert case.provider.calls == [] and await count(case, AdminAuditLog) == 0


async def clip_case(case):
    request = case.manifest["requests"][0]
    slug = request["payload"]["slug"]
    frame_sha = case.runner.sha256(PNG)
    folder = case.store.root / slug
    folder.mkdir(parents=True)
    (folder / frame_sha).write_bytes(PNG)
    look_sha = case.runner.sha256(PNG + b"look")
    look = artifact(
        case.runner,
        case.root,
        "look.json",
        {"characters": {"zhitang": {"candidates": [{"n": 1, "sha256": look_sha}]}}},
    )
    board = artifact(
        case.runner,
        case.root,
        "board.json",
        {"shots": {"s1": {"sha256": frame_sha, "needs_review": False, "incomplete": False}}},
    )
    episode = case.manifest["episodes"][0]
    edit = json.loads((case.root / episode["edit"]["path"]).read_bytes())
    edit["shots"] = [
        {
            "scene_id": "s1",
            "data": {
                "characters": ["zhitang"],
                "prompt": "Adult Zhitang holding the pen",
                "motion": "Fingers tighten once",
                "camera": "Locked camera",
            },
        }
    ]
    episode["edit"] = artifact(case.runner, case.root, episode["edit"]["path"], edit)
    async with case.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
        look_review = VideoReview(
            project_id=project.id,
            gate="look",
            subject="zhitang",
            status="approved",
            summary="Selected face",
            content_sha256=look["sha256"],
            choice="A",
            payload={"options": [{"key": "A", "index": 1, "file_role": "candidate_a"}]},
            files=[{"role": "candidate_a", "sha256": look_sha}],
            decided_at=datetime.now(UTC),
        )
        board_review = VideoReview(
            project_id=project.id,
            gate="storyboard",
            status="approved",
            summary="Frame reviewed",
            content_sha256=board["sha256"],
            decided_at=datetime.now(UTC),
            payload={"shots": [{"id": "s1", "needs_review": False}]},
        )
        session.add_all([look_review, board_review])
        await session.commit()
        request["reviews"].extend(
            [
                {"id": str(look_review.id), "gate": "look", "subject": "zhitang", "artifact": look},
                {"id": str(board_review.id), "gate": "storyboard", "artifact": board},
            ]
        )
    request["kind"] = "clip"
    request["payload"] = {
        "slug": slug,
        "shot_id": "s1",
        "seconds": 8,
        "resolution": "1080p",
        "first_frame": frame_sha,
        "prompt": "Fingers tighten once. Locked camera",
        "native_audio": False,
    }
    case.provider.result = Submitted(
        inline=b"\x00\x00\x00\x18ftypisom" + b"\x00" * 30, content_type="video/mp4"
    )


async def test_actual_clip_uses_reviewed_cast_frame_lite_and_native_audio(case):
    await clip_case(case)
    result = await run(case, execute=True, first_shot=True)
    assert result["status"] == "ready" and result["new_reserve_usd"] == "0.64"
    generated = case.provider.calls[0]
    assert (generated.model, generated.resolution, generated.seconds, generated.aspect) == (
        "veo-3.1-lite-generate-preview",
        "1080p",
        8,
        "16:9",
    )
    assert generated.native_audio is True and generated.references == ()
    assert await meter.used(case.redis, meter.CLIP_SECONDS) == 8


@pytest.mark.parametrize(
    "change",
    [
        "cast",
        "motion",
        "camera",
        "look_choice",
        "newer_look",
        "wrong_frame",
        "pending_frame",
        "paused_series",
    ],
)
async def test_clip_acceptance_cannot_be_replaced_by_manifest_claims(case, change):
    await clip_case(case)
    request = case.manifest["requests"][0]
    if change == "cast":
        request["characters"] = []
    elif change == "motion":
        request["payload"]["prompt"] = "An unrelated event. Locked camera"
    elif change == "camera":
        request["payload"]["prompt"] = "Fingers tighten once. Spin camera"
    elif change == "wrong_frame":
        other = PNG + b"wrong frame"
        digest = case.runner.sha256(other)
        (case.store.root / case.runner.SLUGS[0] / digest).write_bytes(other)
        request["payload"]["first_frame"] = digest
    else:
        async with case.factory() as session:
            if change == "paused_series":
                series = await session.scalar(select(VideoDramaSeries))
                series.status = "paused"
            elif change == "pending_frame":
                review = await session.scalar(
                    select(VideoReview).where(VideoReview.gate == "storyboard")
                )
                review.payload = {"shots": [{"id": "s1", "needs_review": True}]}
            else:
                review = await session.scalar(select(VideoReview).where(VideoReview.gate == "look"))
                if change == "look_choice":
                    review.choice = "B"
                else:
                    session.add(
                        VideoReview(
                            project_id=review.project_id,
                            gate="look",
                            subject="zhitang",
                            status="pending",
                            summary="New",
                            content_sha256="a" * 64,
                            created_at=datetime.now(UTC) + timedelta(seconds=1),
                        )
                    )
            await session.commit()
    with pytest.raises(case.runner.Refused):
        await run(case, execute=True)
    assert case.provider.calls == [] and await count(case, AdminAuditLog) == 0


async def test_retake_needs_new_manifest_changed_request_and_explicit_prior_job(case):
    first = await run(case, execute=True)
    changed = copy.deepcopy(case.manifest)
    changed["requests"][0]["payload"]["seed"] = 7
    with pytest.raises(case.runner.Refused, match="retake requires"):
        await run(case, execute=True, manifest=changed)
    changed["requests"][0]["retake_of"] = first["job_id"]
    changed["requests"][0]["retake_reason"] = "Explicitly reviewed correction to the face"
    result = await run(case, execute=True, manifest=changed)
    assert result["job_id"] != first["job_id"] and len(case.provider.calls) == 2
    assert result["batch_exposure_usd"] == "10.268"


@pytest.mark.parametrize("change", ["seconds", "resolution", "references", "first-shot"])
async def test_lite_contract_and_first_shot_are_strict(case, change):
    request = case.manifest["requests"][0]
    if change != "first-shot":
        request["kind"] = "clip"
        request["payload"] = {
            "slug": case.runner.SLUGS[0],
            "prompt": "One movement",
            "shot_id": "s1",
            "first_frame": "a" * 64,
            "seconds": 8,
            "resolution": "1080p",
        }
        request["payload"][change] = {
            "seconds": 6,
            "resolution": "720p",
            "references": [{"sha256": "b" * 64}],
        }[change]
    with pytest.raises(case.runner.Refused, match="Lite|first-shot"):
        await run(case, execute=True, first_shot=change == "first-shot")
    assert case.provider.calls == []


async def test_session_advisory_lock_survives_commits_and_unlocks_on_error(runner):
    connection = SimpleNamespace(
        dialect=SimpleNamespace(name="postgresql"),
        scalar=AsyncMock(return_value=True),
        commit=AsyncMock(),
        rollback=AsyncMock(),
        execute=AsyncMock(),
        invalidate=AsyncMock(),
    )
    with pytest.raises(RuntimeError):
        async with runner.campaign_lock(connection):
            await connection.commit()  # A service commit does not release a session lock.
            raise RuntimeError("simulated request interruption")
    assert "pg_try_advisory_lock" in str(connection.scalar.call_args.args[0])
    assert "pg_advisory_unlock" in str(connection.execute.call_args.args[0])
    assert connection.commit.await_count == 3
    connection.scalar.return_value = False
    with pytest.raises(runner.Refused, match="holds the lock"):
        async with runner.campaign_lock(connection):
            pytest.fail("must not enter a concurrent campaign")


def test_parser_defaults_preview_and_schema_is_offline(runner):
    assert runner.parser().parse_args([]).execute is False
    assert runner.Manifest.model_json_schema()["properties"]["locale"]["const"] == "zh-TW"
