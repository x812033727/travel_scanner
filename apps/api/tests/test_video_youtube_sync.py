"""Sending a video to the linked channel: checks before, the steps, and runs that stop midway.

docs/videos/HANDS-OFF.md §YouTube API. The runs go against ``FakeGoogle`` (test_video_youtube.py)
on a SQLite database, with an approved upload package in a real review store, and ``run_sync``
is awaited directly instead of being launched as a task.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import select

from app.models import AdminAuditLog, VideoProject, VideoReview
from app.video_reviews.admin_service import review_store
from app.video_reviews.storage import ReviewStore
from app.video_youtube import sync
from app.video_youtube.errors import Refused
from app.video_youtube.schemas import PublishIn
from tests.test_video_youtube import CHANNEL, METADATA, UPLOADED_ID, Site, open_site

SLUG = "ai-model-choice"
STUDIO_ID = "StudioVid01"
MP4 = bytes(range(256)) * 12  # 3,072 bytes: three chunks and a bit at 1,000 bytes a chunk
SRT = "1\n00:00:00,000 --> 00:00:02,000\n字幕\n".encode()
JPEG = b"\xff\xd8\xff\xe0fixture-thumbnail"


@dataclass
class Package:
    project_id: Any
    review_id: Any
    metadata_sha: str
    final_sha: str


def _put(store: ReviewStore, body: bytes) -> str:
    sha = hashlib.sha256(body).hexdigest()
    store.put_part(SLUG, sha, index=0, count=1, size=len(body), data=body)
    return sha


def _entry(role: str, sha: str, body: bytes, content_type: str) -> dict[str, Any]:
    return {"role": role, "sha256": sha, "size": len(body), "content_type": content_type}


async def _package(site: Site, *, youtube_video_id: str | None = None) -> Package:
    """A video whose upload confirmation is approved, its package in the review store."""
    store = review_store(site.settings)
    final_sha = _put(store, MP4)
    metadata = json.dumps({**METADATA, "final_sha256": final_sha}, ensure_ascii=False).encode()
    metadata_sha = _put(store, metadata)
    captions = {locale: SRT + locale.encode() for locale in ("zh-TW", "en", "ja")}
    files = [
        _entry("final", final_sha, MP4, "video/mp4"),
        _entry("thumbnail", _put(store, JPEG), JPEG, "image/jpeg"),
        _entry("metadata", metadata_sha, metadata, "application/json"),
        *(
            _entry(f"captions_{locale}", _put(store, body), body, "text/plain")
            for locale, body in captions.items()
        ),
    ]
    now = datetime.now(UTC)
    project = VideoProject(
        id=uuid4(),
        slug=SLUG,
        title="AI 模型怎麼挑",
        stage="done",
        checklist=[],
        last_synced_at=now,
        youtube_video_id=youtube_video_id,
    )
    review = VideoReview(
        id=uuid4(),
        project_id=project.id,
        gate="publish",
        content_sha256=metadata_sha,
        summary="上傳包",
        payload={"locales": ["zh-TW", "en", "ja"]},
        files=files,
        status="approved",
        decided_at=now,
        created_at=now,
        updated_at=now,
    )
    async with site.factory() as session:
        session.add_all([project, review])
        await session.commit()
    return Package(project.id, review.id, metadata_sha, final_sha)


def _studio_video(site: Site, *, privacy: str = "private", channel: str = CHANNEL) -> None:
    site.google.videos[STUDIO_ID] = {
        "id": STUDIO_ID,
        "snippet": {"title": "final", "description": "", "categoryId": "22", "channelId": channel},
        "status": {"privacyStatus": privacy, "embeddable": True, "license": "youtube"},
    }


def _publish(**fields: Any) -> PublishIn:
    values: dict[str, Any] = {
        "mode": "studio",
        "url": f"https://studio.youtube.com/video/{STUDIO_ID}/edit",
        "visibility": "scheduled",
        "publish_at": datetime.now(UTC) + timedelta(days=1),
        "title": "AI 模型怎麼挑？排行榜第一不一定最好用",
        "description": "改過的說明",
    }
    return PublishIn(**{**values, **fields})


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[Site]:
    async with open_site(monkeypatch, tmp_path) as value:
        yield value


@pytest.fixture
def launched(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    started: list[str] = []
    monkeypatch.setattr(sync, "launch", started.append)
    monkeypatch.setattr(sync, "CHUNK_BYTES", 1000)
    monkeypatch.setattr(sync, "BACKOFF_SECONDS", (0.0, 0.0))
    return started


async def _request(site: Site, payload: PublishIn) -> dict[str, Any]:
    async with site.factory() as session:
        view = await sync.request_sync(
            session, review_store(site.settings), SLUG, site.owner, payload
        )
    assert view.youtube_sync is not None
    return view.youtube_sync


async def _project(site: Site) -> VideoProject:
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
    assert project is not None
    return project


def _steps(project: VideoProject) -> dict[str, str]:
    assert project.youtube_sync is not None
    return {item["id"]: item["state"] for item in project.youtube_sync["steps"]}


# --- a video the owner uploaded in Studio ---------------------------------------------------------


async def test_a_studio_upload_gets_its_details_captions_thumbnail_and_schedule(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _package(site)
    _studio_video(site)
    when = datetime(2030, 1, 2, 12, 0, tzinfo=UTC)
    queued = await _request(site, _publish(publish_at=when))
    assert launched == [SLUG]
    assert queued["status"] == "queued" and queued["request"]["video_id"] == STUDIO_ID
    assert (await _project(site)).youtube_video_id is None, "recorded only once YouTube agrees"

    await sync.run_sync(SLUG, site.factory)

    project = await _project(site)
    assert project.youtube_sync is not None and project.youtube_sync["status"] == "done"
    assert _steps(project) == {"details": "done", "captions": "done", "thumbnail": "done"}
    assert (project.youtube_video_id, project.youtube_publish_at) == (STUDIO_ID, when)
    sent = site.google.updates[-1]
    assert sent["snippet"]["title"] == "AI 模型怎麼挑？排行榜第一不一定最好用"
    assert sent["status"]["privacyStatus"] == "private"
    assert sent["status"]["publishAt"] == "2030-01-02T12:00:00Z"
    assert sent["status"]["embeddable"] is True, "what the owner set in Studio stays"
    assert set(sent["localizations"]) == {"en", "ja"}
    languages = [track["snippet"]["language"] for track in site.google.tracks[STUDIO_ID]]
    assert sorted(languages) == ["en", "ja", "zh-TW"]
    assert site.google.thumbnails[STUDIO_ID] == JPEG
    async with site.factory() as session:
        actions = (await session.scalars(select(AdminAuditLog.action))).all()
    assert "video_youtube_sync_requested" in actions


async def test_captions_the_video_already_has_are_not_uploaded_again(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _package(site)
    _studio_video(site)
    site.google.tracks[STUDIO_ID] = [
        {"snippet": {"language": "zh-TW", "trackKind": "asr"}},
        {"snippet": {"language": "en", "trackKind": "standard"}},
    ]
    await _request(site, _publish())
    await sync.run_sync(SLUG, site.factory)
    inserted = [
        track["snippet"]["language"]
        for track in site.google.tracks[STUDIO_ID]
        if "videoId" in track["snippet"]
    ]
    assert sorted(inserted) == ["ja", "zh-TW"], "the automatic zh-TW track does not count"
    project = await _project(site)
    assert project.youtube_sync is not None
    detail = next(s for s in project.youtube_sync["steps"] if s["id"] == "captions")["detail"]
    assert "en 已經有了" in detail


async def test_a_request_made_under_a_standing_consent_says_so_in_the_audit_log(
    site: Site, launched: list[str]
) -> None:
    """The Shorts calendar sends on the owner's behalf (docs/videos/SHORTS.md §上架)."""
    await site.link()
    await _package(site)
    _studio_video(site)
    behalf = {"auto": True, "consent_id": "0d9f4c1e-consent"}
    site.google.refuse["captions.insert"] = (403, "quotaExceeded")
    async with site.factory() as session:
        await sync.request_sync(
            session, review_store(site.settings), SLUG, site.owner, _publish(), on_behalf=behalf
        )
    await sync.run_sync(SLUG, site.factory)
    async with site.factory() as session:
        await sync.retry_sync(session, SLUG, site.owner, on_behalf=behalf)
    site.google.refuse.clear()
    await sync.run_sync(SLUG, site.factory)
    # The owner's own button, afterwards: nothing of the kind is recorded.
    await _request(site, _publish(visibility="private", publish_at=None))
    async with site.factory() as session:
        entries = (await session.scalars(select(AdminAuditLog))).all()
    requested = [
        entry.metadata_json for entry in entries if entry.action == "video_youtube_sync_requested"
    ]
    automatic = [data for data in requested if data.get("auto")]
    by_hand = [data for data in requested if "auto" not in data]
    assert len(automatic) == 1 and len(by_hand) == 1
    assert automatic[0]["consent_id"] == "0d9f4c1e-consent"
    assert automatic[0]["mode"] == "studio" and automatic[0]["video_id"] == STUDIO_ID
    assert "consent_id" not in by_hand[0]
    (retried,) = [entry for entry in entries if entry.action == "video_youtube_sync_retried"]
    assert retried.metadata_json == {"slug": SLUG, **behalf}
    assert retried.actor_user_id == site.owner.id, "the one who gave the consent"


@pytest.mark.parametrize(
    ("privacy", "channel", "expected"),
    [
        ("public", CHANNEL, "已經公開"),
        ("unlisted", CHANNEL, "要影片先是「私人」"),
        ("private", "UCsomeoneelse0000000000", "不在連結的頻道"),
    ],
)
async def test_the_site_refuses_a_public_video_or_one_of_another_channel(
    site: Site, launched: list[str], privacy: str, channel: str, expected: str
) -> None:
    await site.link()
    await _package(site)
    _studio_video(site, privacy=privacy, channel=channel)
    await _request(site, _publish())
    await sync.run_sync(SLUG, site.factory)
    project = await _project(site)
    assert project.youtube_sync is not None and project.youtube_sync["status"] == "failed"
    assert expected in project.youtube_sync["error"]
    assert _steps(project)["details"] == "failed"
    assert site.google.updates == [], "nothing was written"
    assert project.youtube_video_id is None


async def test_a_quota_refusal_stops_the_run_and_a_retry_finishes_only_what_was_left(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _package(site)
    _studio_video(site)
    site.google.refuse["captions.insert"] = (403, "quotaExceeded")
    await _request(site, _publish())
    await sync.run_sync(SLUG, site.factory)
    project = await _project(site)
    assert project.youtube_sync is not None and "配額用完" in project.youtube_sync["error"]
    assert _steps(project) == {"details": "done", "captions": "failed", "thumbnail": "pending"}

    site.google.refuse.clear()
    updates = len(site.google.updates)
    async with site.factory() as session:
        view = await sync.retry_sync(session, SLUG, site.owner)
    assert view.youtube_sync is not None and view.youtube_sync["status"] == "queued"
    await sync.run_sync(SLUG, site.factory)
    project = await _project(site)
    assert _steps(project) == {"details": "done", "captions": "done", "thumbnail": "done"}
    assert len(site.google.updates) == updates, "the finished details step is not sent again"
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await sync.retry_sync(session, SLUG, site.owner)
    assert refused.value.code == "video_youtube_sync_done"


async def test_a_channel_without_custom_thumbnails_is_told_how_to_enable_them(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _package(site)
    _studio_video(site)
    site.google.refuse["thumbnails.set"] = (403, "forbidden")
    await _request(site, _publish())
    await sync.run_sync(SLUG, site.factory)
    project = await _project(site)
    assert project.youtube_sync is not None and "電話驗證" in project.youtube_sync["error"]
    assert _steps(project)["thumbnail"] == "failed"


async def test_a_revoked_grant_fails_the_run_and_marks_the_card(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _package(site)
    _studio_video(site)
    await _request(site, _publish())
    site.google.refresh_tokens.clear()
    await sync.run_sync(SLUG, site.factory)
    project = await _project(site)
    assert project.youtube_sync is not None and "重新連結" in project.youtube_sync["error"]
    assert (await site.connection()).problem is not None
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await sync.request_sync(
                session, review_store(site.settings), SLUG, site.owner, _publish()
            )
    assert refused.value.code == "video_youtube_grant_lost"


# --- the site uploads the mp4 ---------------------------------------------------------------------


async def test_the_site_uploads_the_mp4_in_chunks_and_resumes_after_a_dropped_chunk(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    package = await _package(site)
    site.google.drop_chunks = {2}
    await _request(site, _publish(mode="upload", url=None, accept_private_lock=True))
    await sync.run_sync(SLUG, site.factory)
    project = await _project(site)
    assert project.youtube_sync is not None, project
    assert project.youtube_sync["status"] == "done", project.youtube_sync
    assert _steps(project) == {
        "upload": "done",
        "details": "done",
        "captions": "done",
        "thumbnail": "done",
    }
    (uri,) = site.google.sessions
    assert bytes(site.google.sessions[uri]) == MP4, "every byte once, in order"
    assert site.google.session_bodies[uri]["status"]["privacyStatus"] == "private"
    assert (project.youtube_video_id, project.youtube_upload_session) == (UPLOADED_ID, None)
    assert project.youtube_sync["progress"] == {"sent": len(MP4), "total": len(MP4)}
    upload = next(s for s in project.youtube_sync["steps"] if s["id"] == "upload")
    assert "鎖成私人" in upload["detail"]
    assert package.final_sha


async def test_an_interrupted_upload_resumes_its_session_instead_of_uploading_twice(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _package(site)
    # Every chunk after the first keeps dropping: the run gives up with the session kept.
    site.google.drop_chunks = {2, 3, 4}
    await _request(site, _publish(mode="upload", url=None, accept_private_lock=True))
    await sync.run_sync(SLUG, site.factory)
    project = await _project(site)
    assert project.youtube_sync is not None and project.youtube_sync["status"] == "failed"
    assert project.youtube_upload_session and project.youtube_upload_session.endswith(
        next(iter(site.google.sessions))
    )
    (uri,) = site.google.sessions
    assert len(site.google.sessions[uri]) == 1000

    async with site.factory() as session:
        await sync.retry_sync(session, SLUG, site.owner)
    await sync.run_sync(SLUG, site.factory)
    project = await _project(site)
    assert project.youtube_sync is not None and project.youtube_sync["status"] == "done"
    assert len(site.google.sessions) == 1, "the same session, not a second upload"
    assert bytes(site.google.sessions[uri]) == MP4


async def test_an_upload_before_the_audit_needs_the_owners_yes(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _package(site)
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await sync.request_sync(
                session,
                review_store(site.settings),
                SLUG,
                site.owner,
                _publish(mode="upload", url=None),
            )
    assert refused.value.code == "video_youtube_private_lock"
    assert launched == []


# --- checks before anything is sent ---------------------------------------------------------------


async def test_nothing_is_sent_without_a_linked_channel(site: Site, launched: list[str]) -> None:
    await _package(site)
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await sync.request_sync(
                session, review_store(site.settings), SLUG, site.owner, _publish()
            )
    assert refused.value.code == "video_youtube_not_linked"


@pytest.mark.parametrize(
    ("fields", "code"),
    [
        ({"publish_at": None}, "video_youtube_publish_at_missing"),
        ({"publish_at": datetime.now(UTC) + timedelta(minutes=1)}, "video_youtube_publish_at_past"),
        ({"url": "https://example.com/watch?v=StudioVid01"}, "video_youtube_url_invalid"),
        ({"title": "a <b>"}, "video_youtube_text_invalid"),
    ],
)
async def test_the_request_is_checked_before_it_is_recorded(
    site: Site, launched: list[str], fields: dict[str, Any], code: str
) -> None:
    await site.link()
    await _package(site)
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await sync.request_sync(
                session, review_store(site.settings), SLUG, site.owner, _publish(**fields)
            )
    assert refused.value.code == code
    assert (await _project(site)).youtube_sync is None


async def test_a_package_that_is_not_the_approved_one_is_refused(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    package = await _package(site)
    path = review_store(site.settings).path(SLUG, package.metadata_sha)
    assert path is not None
    path.write_bytes(b'{"title": "tampered"}')
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await sync.request_sync(
                session, review_store(site.settings), SLUG, site.owner, _publish()
            )
    assert refused.value.code == "video_youtube_package_invalid"


async def test_a_second_request_waits_for_the_running_one_and_a_lapsed_lease_reads_interrupted(
    site: Site, launched: list[str]
) -> None:
    await site.link()
    await _package(site)
    await _request(site, _publish())
    async with site.factory() as session:
        with pytest.raises(Refused) as refused:
            await sync.request_sync(
                session, review_store(site.settings), SLUG, site.owner, _publish()
            )
    assert refused.value.code == "video_youtube_sync_running"
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject).where(VideoProject.slug == SLUG))
        assert project is not None and project.youtube_sync is not None
        stale = datetime.now(UTC) - timedelta(minutes=10)
        project.youtube_sync = {
            **project.youtube_sync,
            "status": "running",
            "lease_until": stale.isoformat(),
        }
        await session.commit()
    async with site.factory() as session:
        view = await sync.retry_sync(session, SLUG, site.owner)
    assert view.youtube_sync is not None and view.youtube_sync["status"] == "queued"


async def test_a_run_nobody_queued_does_nothing(site: Site, launched: list[str]) -> None:
    await _package(site)
    await sync.run_sync(SLUG, site.factory)
    assert (await _project(site)).youtube_sync is None
