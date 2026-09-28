"""Real approved review files and database, with only the independent VPS HTTP boundary faked."""

from __future__ import annotations

import hashlib
import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest
from sqlalchemy import select

from app.models import AdminAuditLog, VideoProject, VideoReview
from app.video_reviews.admin_service import review_store
from app.video_youtube import sync, vps
from app.video_youtube.errors import Refused
from app.video_youtube.state import new_state
from tests.test_video_youtube import Site, _app, open_site
from tests.test_video_youtube_sync import SLUG, STUDIO_ID, _package, _publish

CHANNEL = "UC" + "a" * 22
SECRET = "test-service-secret-" * 3


class Remote:
    def __init__(self) -> None:
        self.job: dict[str, Any] | None = None
        self.manifest: dict[str, Any] = {}
        self.calls: list[httpx.Request] = []
        self.uploads: dict[str, bytes] = {}

    def respond(self, request: httpx.Request) -> httpx.Response:
        self.calls.append(request)
        assert request.headers["authorization"] == f"Bearer {SECRET}"
        route = request.url.path
        if request.method == "GET":
            return httpx.Response(200, json={"job": self.job})
        if request.method == "PUT" and "/files/" not in route:
            self.manifest = json.loads(request.content)
            m = self.manifest
            self.job = {
                "id": route.rsplit("/", 1)[1],
                "slug": m["slug"],
                "channel_id": m["channel_id"],
                "review_sha256": m["review_sha256"],
                "video_id": m["video_id"],
                "state": "staging",
                "upload_started": False,
                "files": [{**f, "received": 0} for f in m["files"]],
                "steps": [],
            }
        else:
            assert self.job
            if "/files/" in route:
                sha = route.rsplit("/", 1)[1]
                old = self.uploads.get(sha, b"")
                assert int(request.url.params["offset"]) == len(old)
                self.uploads[sha] = old + request.content
                for f in self.job["files"]:
                    if f["sha256"] == sha:
                        f["received"] = len(self.uploads[sha])
                        if f["received"] == f["size"]:
                            assert hashlib.sha256(self.uploads[sha]).hexdigest() == sha
            elif route.endswith("/queue"):
                assert all(f["size"] == f["received"] for f in self.job["files"])
                self.job["state"] = "queued"
            elif route.endswith("/resume"):
                self.job["video_id"] = (
                    self.job["video_id"] or json.loads(request.content)["video_id"]
                )
                self.job["state"] = "queued"
            elif route.endswith("/cancel"):
                self.job["state"] = "cancelled"
        return httpx.Response(200, json=self.job)


@pytest.fixture
async def fixture(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> AsyncIterator[tuple[Site, Remote]]:
    async with open_site(monkeypatch, tmp_path) as site:
        remote = Remote()
        monkeypatch.setattr(vps, "config", lambda: vps.Config("http://vps.test", SECRET, CHANNEL))
        monkeypatch.setattr(vps, "load_runtime_settings", AsyncMock(return_value=site.settings))
        monkeypatch.setattr(
            vps,
            "http_client",
            lambda: httpx.AsyncClient(transport=httpx.MockTransport(remote.respond)),
        )
        await _package(site)
        yield site, remote


async def begin(site: Site, **kwargs: Any) -> dict[str, Any]:
    async with site.factory() as session:
        return await vps.start(session, SLUG, site.owner, vps.StartIn(**kwargs))


async def test_no_google_oauth_needed_and_staging_resumes_at_vps_offsets(
    fixture: tuple[Site, Remote],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    site, remote = fixture
    monkeypatch.setattr(vps, "CHUNK", 1000)
    result = await begin(site, title="改寫標題", description="完整說明\n00:00 開場")
    assert not result["linked"] and result["job"]["state"] == "staging"
    m = remote.manifest
    assert m["metadata"]["title"] == "改寫標題"
    assert m["metadata"]["description"] == "完整說明\n00:00 開場"
    assert m["metadata"]["contains_synthetic_media"] is False
    assert "zh-TW" not in m["metadata"]["localizations"]
    assert {f["role"] for f in m["files"]} == {
        "final",
        "thumbnail",
        "captions_zh-TW",
        "captions_en",
        "captions_ja",
    }
    assert "visibility" not in m["metadata"]
    assert (await begin(site))["job"]["id"] == result["job"]["id"]
    assert len([r for r in remote.calls if r.method == "PUT"]) == 1
    for _ in range(12):
        async with site.factory() as session:
            result = await vps.stage(session, SLUG)
        if result["job"]["state"] == "queued":
            break
    assert result["job"]["state"] == "queued"
    assert all(len(r.content) <= 1000 for r in remote.calls if "/files/" in r.url.path)
    final = next(f for f in m["files"] if f["role"] == "final")
    offsets = [r.url.params["offset"] for r in remote.calls if r.url.path.endswith(final["sha256"])]
    assert offsets == ["0", "1000", "2000", "3000"]
    async with site.factory() as session:
        assert (await vps.status(session, SLUG))["linked"] is False
        logs = list(await session.scalars(select(AdminAuditLog)))
    assert len(logs) == 1 and SECRET not in str(logs[0].metadata_json)


async def test_existing_video_omits_mp4_and_completed_receipt_is_recorded_once(
    fixture: tuple[Site, Remote],
) -> None:
    site, remote = fixture
    await begin(site, url=f"https://youtu.be/{STUDIO_ID}")
    assert all(f["role"] != "final" for f in remote.manifest["files"])
    assert remote.job
    async with site.factory() as session:
        with pytest.raises(Refused, match="VPS"):
            await vps.action(session, SLUG, site.owner, "record", vps.ResumeIn())
    remote.job["state"] = "done"
    for _ in range(2):
        async with site.factory() as session:
            result = await vps.action(session, SLUG, site.owner, "record", vps.ResumeIn())
        assert result["linked"]
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject))
        assert (
            project and project.youtube_video_id == STUDIO_ID and project.youtube_publish_at is None
        )
        logs = list(
            await session.scalars(
                select(AdminAuditLog).where(AdminAuditLog.action == "video_youtube_linked")
            )
        )
        assert len(logs) == 1


async def test_api_and_vps_cannot_start_over_each_other(fixture: tuple[Site, Remote]) -> None:
    site, _ = fixture
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject))
        assert project
        project.youtube_sync = new_state({"mode": "upload"})
        await session.commit()
    with pytest.raises(Refused) as denied:
        await begin(site)
    assert denied.value.code == "vps_api_running"
    async with site.factory() as session:
        project = await session.scalar(select(VideoProject))
        assert project
        project.youtube_sync = {"status": "failed"}
        project.youtube_upload_session = "uncertain-api-session"
        await session.commit()
    with pytest.raises(Refused) as uncertain:
        await begin(site)
    assert uncertain.value.code == "vps_video_uncertain"
    await begin(site, url=STUDIO_ID)
    await site.link()
    async with site.factory() as session:
        with pytest.raises(Refused) as conflict:
            await sync.request_sync(
                session, review_store(site.settings), SLUG, site.owner, _publish()
            )
    assert conflict.value.code == "vps_job_exists"


async def test_progress_and_approval_mismatches_are_refused(fixture: tuple[Site, Remote]) -> None:
    site, remote = fixture
    await begin(site)
    assert remote.job
    remote.job["files"][0]["received"] = -1
    async with site.factory() as session:
        with pytest.raises(Refused) as invalid:
            await vps.stage(session, SLUG)
    assert invalid.value.code == "vps_invalid_progress"
    remote.job["files"][0]["received"] = 0
    remote.job["files"][0]["sha256"] = "a" * 64
    async with site.factory() as session:
        with pytest.raises(Refused) as wrong:
            await vps.stage(session, SLUG)
    assert wrong.value.code == "vps_files_changed"
    async with site.factory() as session:
        review = await session.scalar(select(VideoReview))
        assert review
        review.status = "pending"
        await session.commit()
    async with site.factory() as session:
        with pytest.raises(Refused) as revoked:
            await vps.action(session, SLUG, site.owner, "resume", vps.ResumeIn())
    assert revoked.value.code == "vps_not_ready"


async def test_remote_errors_do_not_expose_secrets_and_wrong_channel_is_rejected(
    fixture: tuple[Site, Remote],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    site, remote = fixture
    await begin(site)
    assert remote.job
    remote.job["channel_id"] = "UC" + "b" * 22
    with pytest.raises(Refused) as wrong:
        await vps.latest(SLUG)
    assert wrong.value.code == "vps_invalid_response"
    monkeypatch.setattr(
        vps,
        "http_client",
        lambda: httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(500, json={"code": SECRET, "token": SECRET})
            )
        ),
    )
    with pytest.raises(Refused) as error:
        await vps.latest(SLUG)
    assert SECRET not in str(error.value)


async def test_disabled_mode_and_route_permissions(
    fixture: tuple[Site, Remote],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    site, remote = fixture
    monkeypatch.setattr(vps, "config", lambda: None)
    async with site.factory() as session:
        assert await vps.status(session, SLUG) == {
            "configured": False,
            "job": None,
            "linked": False,
        }
        await vps.assert_idle(SLUG)
    assert not remote.calls
    # viewer may read content, but only owner/content may mutate it.
    for roles, readable in [({"viewer"}, True), (set(), False)]:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=_app(roles, site)), base_url="http://test"
        ) as client:
            path = f"/api/v1/admin/videos/{SLUG}/youtube/vps"
            read = await client.get(path)
            assert read.status_code == (200 if readable else 403)
            for suffix in ("", "/stage", "/resume", "/cancel", "/record"):
                response = await client.post(path + suffix, json={})
                assert response.status_code == 403


def test_operator_config_is_opt_in_and_secrets_are_files(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("MOKAAIR_VPS_UPLOADER_URL", raising=False)
    assert vps.config() is None
    secret = tmp_path / "service-secret"
    secret.write_text(SECRET)
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_URL", "http://127.0.0.1:8789")
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_SECRET_FILE", str(secret))
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_CHANNEL_ID", CHANNEL)
    assert vps.config() == vps.Config("http://127.0.0.1:8789", SECRET, CHANNEL)
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_URL", "http://user:secret@vps.test")
    with pytest.raises(Refused):
        vps.config()
