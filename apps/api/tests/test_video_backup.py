"""The video backup: where each video goes in Drive, the owner's card, and the worker's reports.

The site must never read "backed up" for less than the settings ask: a report that lacks a file
the owner's language choice names is stored as partial, and a complete backup reads stale once
the owner asks for more.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.auth.service import current_user
from app.db import Base, get_session
from app.models import AdminAuditLog, ProviderConfig, User, VideoProject, VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_backup import admin_api, settings, status
from app.video_backup.schemas import LockIn, ProbeAnswerIn, ReportIn, SettingsIn
from app.video_backup.target import (
    PathInvalid,
    expected_parts,
    missing_files,
    normalise_path,
    remote_prefix,
    resolve_target,
)
from app.video_speech.admin_api import video_tool

MODELS = (User, VideoProject, ProviderConfig, AdminAuditLog, VideoToolToken)
HASH = "a" * 64
OTHER_HASH = "b" * 64


# --- paths --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "pasted",
    [
        "G:\\我的雲端硬碟\\AI\\備份\\",
        "G:\\My Drive\\AI\\備份",
        "g:/my drive/AI/備份/",
        "/AI/備份/",
        "AI/備份",
        "  AI//備份  ",
        "我的雲端硬碟/AI/備份",
    ],
)
def test_every_way_the_owner_pastes_the_folder_reads_as_one_drive_path(pasted: str) -> None:
    assert normalise_path(pasted) == "AI/備份"


@pytest.mark.parametrize(
    "pasted",
    [
        "",
        "   ",
        "G:\\",
        "G:\\我的雲端硬碟\\",
        "AI/../系統",
        "AI/./備份",
        "AI/備份?",
        "AI/ 備份",
        "AI/備份.",
    ],
)
def test_a_path_that_is_empty_climbs_out_or_cannot_sync_to_windows_is_refused(pasted: str) -> None:
    with pytest.raises(PathInvalid):
        normalise_path(pasted)


def test_the_remote_prefix_is_the_path_below_the_lock_and_nothing_outside_it() -> None:
    assert remote_prefix("AI/備份", "AI/備份") == ""
    assert remote_prefix("AI/備份/影片", "AI/備份") == "影片"
    assert remote_prefix("AI/備份二", "AI/備份") is None, "a sibling that shares the prefix"
    assert remote_prefix("AI", "AI/備份") is None
    assert remote_prefix("AI/備份", None) is None


# --- targets ------------------------------------------------------------------------------------


def project(slug: str, **fields: Any) -> VideoProject:
    values: dict[str, Any] = {
        "title": slug,
        "stage": "published",
        "checklist": [],
        "youtube_video_id": "abcdefghijk",
        "locales": {},
        "dub_retries": {},
        "dub_locales": [],
    }
    values.update(fields)
    return VideoProject(slug=slug, **values)


@pytest.mark.parametrize(
    ("video", "key", "folder", "tier"),
    [
        (project("curio-h01", category="explainer"), "curio", "奇聞檔案局/curio-h01", "basic"),
        (
            project(
                "ou-de-jianghu-ep-3",
                series_slug="ou-de-jianghu",
                episode_number=3,
                category="anime",
            ),
            "ou-de-jianghu",
            "偶的江湖/003-ou-de-jianghu-ep-3",
            "full",
        ),
        (
            project(
                "lab-short-1",
                format="shorts",
                shorts_line="lab",
                shorts_series="ai-lab",
                category="tutorial",
            ),
            "ai-lab",
            "Shorts/ai-lab/lab-short-1",
            "basic",
        ),
        (project("cut-short-1", shorts_line="cut"), "cut", "Shorts/cut/cut-short-1", "basic"),
        (project("ai-term-embedding"), "ai-terms", "AI 名詞十分鐘/ai-term-embedding", "basic"),
        (project("story-costco", category="story"), "story", "品牌故事/story-costco", "basic"),
        (
            project("phone-scanning", category="tutorial"),
            "tutorial",
            "tutorial/phone-scanning",
            "basic",
        ),
        (project("jingwei", format="drama", category="drama"), "drama", "drama/jingwei", "full"),
        (project("nothing-said"), "other", "其他/nothing-said", "basic"),
    ],
)
def test_each_video_is_filed_under_its_series_with_the_owners_default_tier(
    video: VideoProject, key: str, folder: str, tier: str
) -> None:
    target = resolve_target(video)
    assert (target.series_key, target.folder, target.tier) == (key, folder, tier)
    assert target.shared_folder == f"{folder.rsplit('/', 1)[0]}/_共用"


def test_overrides_win_and_a_folder_once_used_survives_a_rename() -> None:
    video = project("curio-h02", category="explainer")
    named = resolve_target(video, tiers={"curio": "full"}, folder_names={"curio": "奇聞"})
    assert (named.folder, named.tier) == ("奇聞/curio-h02", "full")
    video.backup = {"state": "done", "folder": "奇聞檔案局/curio-h02"}
    kept = resolve_target(video, tiers={"curio": "off"}, folder_names={"curio": "奇聞"})
    assert (kept.folder, kept.tier) == ("奇聞檔案局/curio-h02", "off")


def test_the_chosen_languages_name_the_files_a_backup_must_hold() -> None:
    video = project(
        "curio-h03",
        locales={"en": {"metadata": True, "captions": True, "dub": True}, "ja": {"captions": True}},
    )
    expected = expected_parts(video)
    assert expected == {
        "required": ["final.mp4", "metadata.json"],
        "descriptions": ["en"],
        "captions": ["en", "ja"],
        "dubs": ["en"],
    }
    assert missing_files(None, expected) == [
        "final.mp4",
        "metadata.json",
        "descriptions/en.txt",
        "captions/en.srt",
        "captions/ja.srt",
        "dubs/en",
    ]
    contents = {
        "final": True,
        "metadata": True,
        "descriptions": ["en"],
        "captions": ["en"],
        "dubs": [],
        "skipped": {"captions": ["ja"], "dubs": ["en"]},
    }
    assert missing_files(contents, expected) == [], "a part the package skipped with a reason"
    assert missing_files({**contents, "skipped": {}}, expected) == ["captions/ja.srt", "dubs/en"]


def test_a_short_needs_only_its_final_cut_since_its_package_has_no_metadata_json() -> None:
    short = project("lab-short-2", format="shorts", shorts_line="lab")
    expected = expected_parts(short)
    assert expected["required"] == ["final.mp4"]
    assert missing_files({"final": True}, expected) == []
    assert missing_files({}, expected) == ["final.mp4"]


# --- the database --------------------------------------------------------------------------------


@dataclass
class Site:
    factory: async_sessionmaker[AsyncSession]
    owner: User
    token: VideoToolToken

    async def add(self, video: VideoProject) -> None:
        async with self.factory() as session:
            session.add(video)
            await session.commit()

    async def video(self, slug: str) -> VideoProject:
        async with self.factory() as session:
            found = await session.scalar(select(VideoProject).where(VideoProject.slug == slug))
            assert found is not None
            return found

    async def audits(self, action: str) -> list[AdminAuditLog]:
        async with self.factory() as session:
            rows = await session.scalars(
                select(AdminAuditLog).where(AdminAuditLog.action == action)
            )
            return list(rows.all())


@pytest.fixture
async def site() -> AsyncIterator[Site]:
    engine = create_async_engine("sqlite+aiosqlite://")

    # SQLite drops timezone offsets; PostgreSQL hands back aware datetimes.
    def restore_utc(target: Any, _context: Any, *_more: Any) -> None:
        for column in target.__table__.columns:
            value = getattr(target, column.name)
            if isinstance(value, datetime) and value.tzinfo is None:
                setattr(target, column.name, value.replace(tzinfo=UTC))

    for model in MODELS:
        event.listen(model, "load", restore_utc)
    async with engine.begin() as db:
        await db.run_sync(
            lambda sync_db: Base.metadata.create_all(
                sync_db, tables=[model.__table__ for model in MODELS]
            )
        )
    factory = async_sessionmaker(engine, expire_on_commit=False)
    owner = User(id=uuid4(), email="owner@example.test", password_hash="unused", auth_version=1)
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    token = VideoToolToken(
        id=uuid4(),
        name="worker",
        token_hash="c" * 64,
        token_prefix="mkv_test",
        created_by_user_id=owner.id,
    )
    async with factory() as session:
        session.add(User(id=owner.id, email=owner.email, password_hash="unused"))
        session.add(token)
        await session.commit()
    yield Site(factory, owner, token)
    for model in MODELS:
        event.remove(model, "load", restore_utc)
    await engine.dispose()


async def save(site: Site, **fields: Any) -> Any:
    async with site.factory() as session:
        current = await settings.view(session)
        return await settings.save(
            session, site.owner, SettingsIn(expected_updated_at=current.updated_at, **fields)
        )


async def lock(site: Site, path: str | None = "AI/備份", problem: str | None = None) -> Any:
    async with site.factory() as session:
        return await settings.record_lock(session, LockIn(lock_path=path, problem=problem))


async def report(site: Site, slug: str, **fields: Any) -> Any:
    async with site.factory() as session:
        return await status.report(session, site.token, slug, ReportIn(**fields))


def done(folder: str, **contents: Any) -> dict[str, Any]:
    return {
        "state": "done",
        "folder": folder,
        "tier": "basic",
        "bytes": 1000,
        "files": 4,
        "files_hash": HASH,
        "contents": {"final": True, "metadata": True, "thumbnail": True, **contents},
    }


# --- settings -----------------------------------------------------------------------------------


async def test_the_card_starts_off_at_the_owners_folder_and_saves_a_pasted_pc_path(
    site: Site,
) -> None:
    async with site.factory() as session:
        first = await settings.view(session)
    assert (first.enabled, first.path, first.updated_at) == (False, "AI/備份", None)
    assert first.problem == "備份尚未開啟"
    saved = await save(site, enabled=True, path="G:\\我的雲端硬碟\\AI\\備份\\影片\\")
    assert (saved.enabled, saved.path) == (True, "AI/備份/影片")
    assert saved.problem is not None and "VIDEO_BACKUP_LOCK_PATH" in saved.problem
    [audit] = await site.audits("video_backup_settings_updated")
    assert audit.metadata_json["path"] == "AI/備份/影片" and audit.actor_user_id == site.owner.id
    assert (await lock(site)).problem is None, "inside the lock, the worker may copy"


async def test_a_stale_save_conflicts_but_a_worker_round_never_does(site: Site) -> None:
    saved = await save(site, enabled=True)
    await lock(site)
    async with site.factory() as session:
        await settings.request_test(session, site.owner)
    async with site.factory() as session:
        again = await settings.save(
            session,
            site.owner,
            SettingsIn(expected_updated_at=saved.updated_at, tiers={"curio": "full"}),
        )
    assert again.tiers == {"curio": "full"}
    async with site.factory() as session:
        with pytest.raises(AppError) as conflict:
            await settings.save(
                session, site.owner, SettingsIn(expected_updated_at=saved.updated_at, enabled=False)
            )
    assert conflict.value.code == "video_backup_settings_conflict"


async def test_a_path_outside_the_hosts_lock_is_refused_with_how_to_change_it(site: Site) -> None:
    await lock(site, "G:\\我的雲端硬碟\\AI\\備份")
    with pytest.raises(AppError) as outside:
        await save(site, path="AI/別的")
    assert outside.value.code == "video_backup_path_outside_lock"
    assert "rclone-videos.conf" in outside.value.detail
    with pytest.raises(AppError) as invalid:
        await save(site, path="AI/../備份")
    assert invalid.value.code == "video_backup_path_invalid"
    with pytest.raises(AppError) as name:
        await save(site, folder_names={"curio": "奇聞:檔案"})
    assert name.value.code == "video_backup_folder_name_invalid"


async def test_a_host_without_the_rclone_file_says_so_and_the_worker_gets_no_prefix(
    site: Site,
) -> None:
    await save(site, enabled=True)
    view = await lock(site, None)
    assert view.problem is not None and "rclone-videos.conf" in view.problem
    async with site.factory() as session:
        config = await status.worker_config(session)
    assert (config.remote_prefix, config.problem) == (None, view.problem)
    await lock(site, "AI/備份")
    async with site.factory() as session:
        config = await status.worker_config(session)
    assert (config.remote_prefix, config.problem) == ("", None)


async def test_one_test_request_at_a_time_and_only_its_own_answer_closes_it(site: Site) -> None:
    async with site.factory() as session:
        first = await settings.request_test(session, site.owner)
    async with site.factory() as session:
        second = await settings.request_test(session, site.owner)
    assert first.test.pending_id is not None and second.test.pending_id == first.test.pending_id
    async with site.factory() as session:
        assert (await status.worker_config(session)).test is not None
    answer = ProbeAnswerIn(ok=True, message="寫入並刪除 _probe 成功", free_bytes=10, total_bytes=20)
    async with site.factory() as session:
        with pytest.raises(AppError) as unknown:
            await settings.answer_test(session, uuid4(), answer)
    assert unknown.value.status == 404
    async with site.factory() as session:
        answered = await settings.answer_test(session, first.test.pending_id, answer)
    assert (answered.test.pending_id, answered.test.status) == (None, "success")
    assert (answered.space.free_bytes, answered.space.total_bytes) == (10, 20)
    assert len(await site.audits("video_backup_test_requested")) == 1


# --- reports ------------------------------------------------------------------------------------


async def test_a_complete_report_is_done_and_one_missing_a_chosen_dub_is_partial(
    site: Site,
) -> None:
    await site.add(project("curio-h01", locales={"en": {"metadata": True, "dub": True}}))
    folder = "奇聞檔案局/curio-h01"
    short = await report(site, "curio-h01", **done(folder, descriptions=["en"], captions=["en"]))
    assert (short.state, short.complete) == ("partial", False)
    assert short.missing == ["dubs/en"] and short.error and "dubs/en" in short.error
    full = await report(
        site, "curio-h01", **done(folder, descriptions=["en"], captions=["en"], dubs=["en"])
    )
    assert (full.state, full.complete, full.missing, full.error) == ("done", True, [], None)
    assert full.at is not None and full.checked_at is not None
    stored = (await site.video("curio-h01")).backup
    assert (
        stored is not None and stored["files_hash"] == HASH and stored["contents"]["dubs"] == ["en"]
    )


async def test_a_done_backup_reads_stale_once_the_owner_chooses_another_language(
    site: Site,
) -> None:
    await site.add(project("curio-h04"))
    await report(site, "curio-h04", **done("奇聞檔案局/curio-h04"))
    async with site.factory() as session:
        video = await session.scalar(select(VideoProject).where(VideoProject.slug == "curio-h04"))
        assert video is not None
        video.locales = {"ja": {"captions": True}}
        await session.commit()
    async with site.factory() as session:
        view = await status.video_status(session, "curio-h04")
    assert (view.state, view.complete, view.missing) == ("stale", False, ["captions/ja.srt"])


async def test_a_fuller_tier_than_the_one_copied_reads_stale(site: Site) -> None:
    await site.add(project("curio-h05"))
    await report(site, "curio-h05", **done("奇聞檔案局/curio-h05"))
    await save(site, tiers={"curio": "full"})
    async with site.factory() as session:
        view = await status.video_status(session, "curio-h05")
    assert (view.state, view.tier, view.copied_tier) == ("stale", "full", "basic")


async def test_reports_the_site_cannot_trust_are_refused(site: Site) -> None:
    await site.add(project("curio-h06"))
    await site.add(project("not-uploaded", youtube_video_id=None))
    cases = [
        ("not-uploaded", done("其他/not-uploaded"), "video_backup_not_uploaded"),
        ("curio-h06", done("奇聞/curio-h06"), "video_backup_folder_changed"),
        (
            "curio-h06",
            {**done("奇聞檔案局/curio-h06"), "files_hash": None},
            "video_backup_report_incomplete",
        ),
        (
            "curio-h06",
            {**done("奇聞檔案局/curio-h06"), "contents": None},
            "video_backup_report_incomplete",
        ),
        ("curio-h06", done("奇聞檔案局/../curio-h06"), "video_backup_folder_invalid"),
    ]
    for slug, fields, code in cases:
        with pytest.raises(AppError) as refused:
            await report(site, slug, **fields)
        assert refused.value.code == code, fields
    await save(site, tiers={"curio": "off"})
    with pytest.raises(AppError) as off:
        await report(site, "curio-h06", **done("奇聞檔案局/curio-h06"))
    assert off.value.code == "video_backup_tier_off"


async def test_the_first_folder_sticks_after_the_series_is_renamed(site: Site) -> None:
    await site.add(project("curio-h07"))
    await report(site, "curio-h07", state="pending", folder="奇聞檔案局/curio-h07", tier="basic")
    await save(site, folder_names={"curio": "奇聞"})
    kept = await report(site, "curio-h07", **done("奇聞檔案局/curio-h07"))
    assert (kept.folder, kept.state) == ("奇聞檔案局/curio-h07", "done")


async def test_failures_are_audited_once_and_quota_blocks_record_the_free_space(
    site: Site,
) -> None:
    await site.add(project("curio-h08"))
    folder = "奇聞檔案局/curio-h08"
    for attempts in (3, 4):
        failed = await report(
            site,
            "curio-h08",
            state="failed",
            folder=folder,
            tier="basic",
            attempts=attempts,
            error="rclone check: 2 differences",
        )
    assert (failed.state, failed.attempts) == ("failed", 4)
    [audit] = await site.audits("video_backup_failed")
    assert audit.target == "video_backup:curio-h08" and audit.actor_user_id == site.owner.id
    blocked = await report(
        site,
        "curio-h08",
        state="blocked_quota",
        folder=folder,
        tier="basic",
        error="剩 1 GB，這次要 3 GB",
        free_bytes=1,
        total_bytes=15,
    )
    assert blocked.state == "blocked_quota"
    async with site.factory() as session:
        assert (await settings.view(session)).space.free_bytes == 1


async def test_the_summary_says_all_backed_up_only_when_every_uploaded_video_is_done(
    site: Site,
) -> None:
    await save(site, enabled=True)
    await site.add(project("curio-a"))
    await site.add(project("curio-b"))
    await site.add(project("draft-only", youtube_video_id=None))
    await report(site, "curio-a", **done("奇聞檔案局/curio-a"))
    async with site.factory() as session:
        summary = await status.status(session)
    assert (summary.uploaded, summary.all_backed_up) == (2, False)
    assert summary.counts["done"] == 1 and summary.counts["not_queued"] == 1
    assert [video.slug for video in summary.videos] == ["curio-b"]
    await report(site, "curio-b", state="pending", folder="奇聞檔案局/curio-b", tier="basic")
    async with site.factory() as session:
        video = await session.scalar(select(VideoProject).where(VideoProject.slug == "curio-b"))
        assert video is not None and video.backup is not None
        video.backup = {
            **video.backup,
            "queued_at": (datetime.now(UTC) - timedelta(hours=30)).isoformat(),
        }
        await session.commit()
    async with site.factory() as session:
        late = await status.status(session)
    assert late.videos[0].overdue and late.counts["pending"] == 1
    await report(site, "curio-b", **done("奇聞檔案局/curio-b"))
    async with site.factory() as session:
        finished = await status.status(session)
        everything = await status.status(session, everything=True)
    assert finished.all_backed_up and finished.videos == []
    assert [video.slug for video in everything.videos] == ["curio-a", "curio-b"]


async def test_the_worker_config_lists_every_uploaded_video_with_its_target(site: Site) -> None:
    await save(site, enabled=True)
    await lock(site)
    await site.add(project("curio-h09", locales={"ko": {"captions": True}}))
    await site.add(project("draft", youtube_video_id=None))
    async with site.factory() as session:
        config = await status.worker_config(session)
    [video] = config.videos
    assert (video.slug, video.folder, video.tier) == ("curio-h09", "奇聞檔案局/curio-h09", "basic")
    assert video.expected.captions == ["ko"] and video.backup is None


# --- the routes ---------------------------------------------------------------------------------


def app_for(site: Site, roles: set[str]) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.admin_router, prefix="/api/v1")
    app.include_router(admin_api.tool_router, prefix="/api/v1")
    user = User(id=site.owner.id, email="someone@example.test", password_hash="x", auth_version=1)
    user._admin_roles_cache = frozenset(roles)  # type: ignore[attr-defined]

    async def session() -> AsyncIterator[AsyncSession]:
        async with site.factory() as db:
            yield db

    app.dependency_overrides[get_session] = session
    app.dependency_overrides[current_user] = lambda: user
    app.dependency_overrides[video_tool] = lambda: site.token
    return app


async def test_a_reviewer_reads_the_card_and_status_but_cannot_change_or_test(site: Site) -> None:
    transport = ASGITransport(app=app_for(site, {"content"}))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        read = await client.get("/api/v1/admin/video-backup/settings")
        summary = await client.get("/api/v1/admin/video-backup/status")
        probe = await client.get("/api/v1/admin/video-backup/test")
        put = await client.put(
            "/api/v1/admin/video-backup/settings",
            json={"expected_updated_at": None, "enabled": True},
        )
        test = await client.post("/api/v1/admin/video-backup/test")
    assert (read.status_code, summary.status_code, probe.status_code) == (200, 200, 200)
    assert (put.status_code, test.status_code) == (403, 403)


async def test_the_owner_and_the_worker_go_through_the_routes(site: Site) -> None:
    await site.add(project("curio-route"))
    transport = ASGITransport(app=app_for(site, {"owner"}))
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        saved = await client.put(
            "/api/v1/admin/video-backup/settings",
            json={"expected_updated_at": None, "enabled": True, "path": "G:\\My Drive\\AI\\備份"},
        )
        locked = await client.post(
            "/api/v1/video/automation/backup/lock", json={"lock_path": "AI/備份"}
        )
        config = await client.get("/api/v1/video/automation/backup/config")
        reported = await client.post(
            "/api/v1/video/automation/backup/curio-route/report",
            json=done("奇聞檔案局/curio-route"),
        )
        detail = await client.get("/api/v1/admin/video-backup/status/curio-route")
        stray = await client.post(
            "/api/v1/video/automation/backup/Not_A_Slug/report", json=done("x")
        )
        missing = await client.post(
            "/api/v1/video/automation/backup/no-such-video/report", json=done("x")
        )
    assert saved.status_code == 200 and saved.json()["path"] == "AI/備份"
    assert locked.status_code == 200 and locked.json()["problem"] is None
    assert config.status_code == 200 and config.json()["remote_prefix"] == ""
    assert reported.status_code == 200 and reported.json()["state"] == "done"
    assert detail.status_code == 200 and detail.json()["complete"] is True
    assert stray.status_code == 422
    assert missing.status_code == 404 and missing.json()["code"] == "video_backup_video_not_found"
