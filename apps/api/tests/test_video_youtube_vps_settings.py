"""VPS connection settings use encrypted storage and never guess remote job safety."""

from __future__ import annotations

import json
from collections.abc import AsyncIterator
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.admin.service import decrypt_secrets, load_runtime_settings
from app.models import AdminAuditLog, ProviderConfig
from app.video_youtube import vps, vps_settings
from app.video_youtube.errors import Refused
from tests.test_video_youtube import Site, _app, open_site
from tests.test_video_youtube_sync import SLUG, _package
from tests.test_video_youtube_vps import CHANNEL, SECRET, Remote

PATH = "/api/v1/admin/video-youtube/vps/settings"
URL = "https://uploader.example.test"


@pytest.fixture
async def site(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> AsyncIterator[Site]:
    for name in ("URL", "CHANNEL_ID", "SECRET_FILE", "DESKTOP_URL"):
        monkeypatch.delenv(f"MOKAAIR_VPS_UPLOADER_{name}", raising=False)
    async with open_site(monkeypatch, tmp_path) as value:
        yield value


async def save(site: Site, **fields: Any) -> vps_settings.SettingsView:
    async with site.factory() as session:
        return await vps_settings.save(session, site.owner, vps_settings.SettingsIn(**fields))


async def initial(site: Site) -> vps_settings.SettingsView:
    return await save(
        site, expected_updated_at=None, enabled=True, url=URL, channel_id=CHANNEL, secret=SECRET
    )


def remote_status(monkeypatch: pytest.MonkeyPatch, **values: Any) -> list[httpx.Request]:
    calls: list[httpx.Request] = []

    def respond(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        assert request.method == "GET" and request.url.path == "/status"
        return httpx.Response(200, json={"channel_id": CHANNEL, "browser": "idle", **values})

    monkeypatch.setattr(
        vps,
        "http_client",
        lambda: httpx.AsyncClient(
            transport=httpx.MockTransport(respond),
            follow_redirects=False,
        ),
    )
    return calls


async def test_persistent_secret_is_encrypted_and_never_returned_or_audited(site: Site) -> None:
    saved = await initial(site)
    assert saved.configured and saved.secret_set and saved.source == "database"
    assert saved.updated_at and SECRET not in saved.model_dump_json()
    async with site.factory() as session:
        row = await session.scalar(select(ProviderConfig))
        assert row is not None and row.secret_config_encrypted
        assert SECRET not in row.secret_config_encrypted
        assert decrypt_secrets(row.secret_config_encrypted) == {"secret": SECRET}
        loaded = await vps_settings.resolve(session)
        assert loaded == vps.Config(URL, SECRET, CHANNEL)
        assert SECRET not in repr(loaded)
        # Generic runtime loading ignores this dedicated provider without deleting it.
        await load_runtime_settings(session)
        assert await session.get(ProviderConfig, row.id) is row
        audit = (await session.scalars(select(AdminAuditLog))).all()
        assert audit and SECRET not in json.dumps([item.metadata_json for item in audit])


async def test_only_changed_fields_are_saved_and_stale_write_is_rejected(site: Site) -> None:
    saved = await initial(site)
    changed = await save(
        site,
        expected_updated_at=saved.updated_at,
        secret="  ",
        desktop_url="http://127.0.0.1:6080/vnc.html",
    )
    assert changed.url == URL and changed.secret_set
    assert changed.updated_at != saved.updated_at
    async with site.factory() as session:
        assert (await vps_settings.resolve(session)) == vps.Config(URL, SECRET, CHANNEL)
    with pytest.raises(Refused) as conflict:
        await save(site, expected_updated_at=saved.updated_at, enabled=False)
    assert conflict.value.code == "vps_settings_conflict"
    with pytest.raises(Refused):
        await save(site, expected_updated_at=None, desktop_url="")
    with pytest.raises(ValidationError):
        vps_settings.SettingsIn.model_validate({"enabled": True})


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com",
        "https://user:secret@example.com",
        "https://example.com/rpc",
        "https://example.com?token=secret",
        "https://example.com#token",
        "file:///etc/passwd",
        "http://169.254.169.254",
        "https://169.254.169.254",
        "https://[fe80::1]",
        "https://metadata.google.internal",
        "https://example.com:99999",
        "https://example.com:0",
        "http://0.0.0.0",
        "http://2130706433",
        "https://example.com\\@evil.test",
    ],
)
def test_unsafe_rpc_urls_are_refused(url: str) -> None:
    with pytest.raises(Refused) as refused:
        vps_settings.rpc_url(url)
    assert refused.value.code == "vps_url_invalid"


@pytest.mark.parametrize(
    "url",
    [
        "http://mokaair-studio-uploader:8789",
        "http://10.42.0.2:8789",
        "http://127.0.0.1:8789",
        "http://[::1]:8789",
        "https://uploader.example.com",
    ],
)
def test_private_rpc_and_public_https_are_allowed(url: str) -> None:
    assert vps_settings.rpc_url(url) == url


@pytest.mark.parametrize(
    "change",
    [
        {"url": "https://other.example.test", "secret": "new-service-secret-" * 3},
        {"channel_id": "UC" + "b" * 22},
        {"secret": "new-service-secret-" * 3},
        {"enabled": False},
    ],
)
@pytest.mark.parametrize("active_jobs", [1, None, False, -1])
async def test_connection_changes_refuse_active_or_unknown_jobs(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
    change: dict[str, Any],
    active_jobs: Any,
) -> None:
    saved = await initial(site)
    calls = remote_status(monkeypatch, active_jobs=active_jobs)
    with pytest.raises(Refused) as refused:
        await save(site, expected_updated_at=saved.updated_at, **change)
    assert refused.value.code == "vps_settings_busy"
    assert len(calls) == 1 and str(calls[0].url) == URL + "/status"
    assert calls[0].headers["authorization"] == f"Bearer {SECRET}"
    async with site.factory() as session:
        assert (await vps_settings.resolve(session)) == vps.Config(URL, SECRET, CHANNEL)


async def test_origin_change_needs_explicit_secret_and_uses_old_origin_for_safety_check(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    saved = await initial(site)
    calls = remote_status(monkeypatch, active_jobs=0)
    with pytest.raises(Refused) as refused:
        await save(site, expected_updated_at=saved.updated_at, url="https://other.example.test")
    assert refused.value.code == "vps_secret_required" and calls == []
    new_secret = "different-service-secret-" * 3
    updated = await save(
        site,
        expected_updated_at=saved.updated_at,
        url="https://other.example.test",
        secret=new_secret,
    )
    assert updated.url == "https://other.example.test" and len(calls) == 1
    assert calls[0].headers["authorization"] == f"Bearer {SECRET}"
    async with site.factory() as session:
        assert (await vps_settings.resolve(session)) == vps.Config(updated.url, new_secret, CHANNEL)


async def test_mistyped_channel_fails_test_but_empty_authenticated_queue_allows_correction(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mistyped_channel = "UC" + "b" * 22
    await save(
        site,
        expected_updated_at=None,
        enabled=True,
        url=URL,
        channel_id=mistyped_channel,
        secret=SECRET,
    )
    calls = remote_status(monkeypatch, active_jobs=0)
    async with site.factory() as session:
        result = await vps_settings.test_connection(session, site.owner)
    assert result.last_test_status == "failed"
    corrected = await save(site, expected_updated_at=result.updated_at, channel_id=CHANNEL)
    assert corrected.channel_id == CHANNEL and corrected.last_test_status is None
    assert len(calls) == 2
    assert all(str(call.url) == URL + "/status" for call in calls)
    assert all(call.headers["authorization"] == f"Bearer {SECRET}" for call in calls)
    async with site.factory() as session:
        assert (await vps_settings.resolve(session)) == vps.Config(URL, SECRET, CHANNEL)
        tested = await vps_settings.test_connection(session, site.owner)
        assert tested.last_test_status == "success"


@pytest.mark.parametrize(
    ("status", "code"),
    [
        ({"active_jobs": 1}, "vps_settings_busy"),
        ({"active_jobs": None}, "vps_settings_busy"),
        ({"active_jobs": False}, "vps_settings_busy"),
        ({"active_jobs": 0.0}, "vps_settings_busy"),
        ({"active_jobs": -1}, "vps_settings_busy"),
        ({"active_jobs": 0, "channel_id": None}, "vps_status_invalid"),
        ({"active_jobs": 0, "channel_id": ""}, "vps_status_invalid"),
        ({"active_jobs": 0, "channel_id": 42}, "vps_status_invalid"),
        ({"active_jobs": 0, "channel_id": "UCbad"}, "vps_status_invalid"),
    ],
)
async def test_mistyped_channel_correction_still_requires_valid_empty_remote_queue(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
    status: dict[str, Any],
    code: str,
) -> None:
    mistyped_channel = "UC" + "b" * 22
    saved = await save(
        site,
        expected_updated_at=None,
        enabled=True,
        url=URL,
        channel_id=mistyped_channel,
        secret=SECRET,
    )
    calls = remote_status(monkeypatch, **status)
    with pytest.raises(Refused) as refused:
        await save(site, expected_updated_at=saved.updated_at, channel_id=CHANNEL)
    assert refused.value.code == code
    assert len(calls) == 1 and calls[0].headers["authorization"] == f"Bearer {SECRET}"
    async with site.factory() as session:
        assert (await vps_settings.resolve(session)) == vps.Config(URL, SECRET, mistyped_channel)


async def test_environment_fallback_and_database_disable_are_distinct(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    file = tmp_path / "secret"
    file.write_text(SECRET)
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_URL", URL)
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_SECRET_FILE", str(file))
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_CHANNEL_ID", CHANNEL)
    remote_status(monkeypatch, active_jobs=0)
    async with site.factory() as session:
        assert (await vps_settings.view(session)).source == "environment"
        result = await vps_settings.test_connection(session, site.owner)
        assert result.last_test_status == "success" and result.source == "environment"
        assert result.browser_status == "idle" and result.active_jobs == 0
        assert "Google" in (result.last_test_message or "")
    disabled = await save(site, expected_updated_at=result.updated_at, enabled=False)
    assert not disabled.enabled and disabled.source == "database"
    async with site.factory() as session:
        assert await vps_settings.resolve(session) is None
        await vps.assert_idle(session, SLUG)


async def test_probe_failure_is_sanitized_and_does_not_claim_google_login(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    await initial(site)
    monkeypatch.setattr(
        vps,
        "http_client",
        lambda: httpx.AsyncClient(
            transport=httpx.MockTransport(lambda _: httpx.Response(401, json={"code": SECRET})),
        ),
    )
    async with site.factory() as session:
        result = await vps_settings.test_connection(session, site.owner)
    assert result.last_test_status == "failed" and result.last_tested_at
    assert SECRET not in result.model_dump_json()
    async with site.factory() as session:
        assert (await vps_settings.view(session)).last_test_status == "failed"


async def test_incomplete_environment_is_readable_but_runtime_and_switching_fail_closed(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_URL", URL)
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_CHANNEL_ID", CHANNEL)
    async with site.factory() as session:
        shown = await vps_settings.view(session)
        assert shown.url == URL and shown.enabled and not shown.secret_set
        assert not shown.configured
        with pytest.raises(Refused):
            await vps_settings.resolve(session)
        result = await vps_settings.test_connection(session, site.owner)
        assert result.last_test_status == "failed"
    with pytest.raises(Refused):
        await save(
            site,
            expected_updated_at=result.updated_at,
            secret=SECRET,
            url="https://new.example.test",
        )


async def test_invalid_legacy_urls_are_not_echoed_to_browser_links(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_URL", f"https://user:{SECRET}@example.test")
    monkeypatch.setenv("MOKAAIR_VPS_UPLOADER_DESKTOP_URL", "javascript:alert(1)")
    async with site.factory() as session:
        shown = await vps_settings.view(session)
    assert not shown.configured and not shown.url and not shown.desktop_url
    assert SECRET not in shown.model_dump_json()


async def test_runtime_config_is_loaded_once_and_pinned_for_a_job_request(
    site: Site,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    await initial(site)
    await _package(site)
    remote = Remote()
    monkeypatch.setattr(
        vps,
        "http_client",
        lambda: httpx.AsyncClient(
            transport=httpx.MockTransport(remote.respond),
        ),
    )
    monkeypatch.setattr(vps, "load_runtime_settings", AsyncMock(return_value=site.settings))
    resolver = AsyncMock(wraps=vps_settings.resolve)
    monkeypatch.setattr(vps_settings, "resolve", resolver)
    async with site.factory() as session:
        await vps.start(session, SLUG, site.owner, vps.StartIn())
    assert resolver.await_count == 1
    assert remote.calls and all(
        request.url.host == "uploader.example.test" for request in remote.calls
    )
    assert not site.google.calls


@pytest.mark.parametrize(
    "roles,readable,writeable",
    [
        ({"owner"}, True, True),
        ({"content"}, True, False),
        ({"viewer"}, True, False),
        (set(), False, False),
    ],
)
async def test_settings_routes_apply_explicit_read_and_manage_permissions(
    site: Site,
    roles: set[str],
    readable: bool,
    writeable: bool,
) -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=_app(roles, site)),
        base_url="http://test",
    ) as client:
        read = await client.get(PATH)
        assert read.status_code == (200 if readable else 403)
        saved = await client.put(PATH, json={"expected_updated_at": None, "enabled": False})
        assert saved.status_code == (200 if writeable else 403)
        tested = await client.post(PATH + "/test")
        assert tested.status_code == (200 if writeable else 403)


async def test_missing_revision_and_extra_secret_fields_are_rejected_at_the_api(site: Site) -> None:
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=_app({"owner"}, site)),
        base_url="http://test",
    ) as client:
        assert (await client.put(PATH, json={"enabled": False})).status_code == 422
        assert (
            await client.put(
                PATH,
                json={
                    "expected_updated_at": None,
                    "google_password": "never-store-this",
                },
            )
        ).status_code == 422
