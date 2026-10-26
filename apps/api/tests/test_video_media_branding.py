"""/video/media/branding: the worker's current bookends, read-only, for ``branding --pull``."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.config import Settings
from app.db import get_session
from app.models import VideoToolToken
from app.problems import AppError, app_error_handler
from app.video_media import admin_api
from app.video_speech import admin_api as speech_api

INTRO = b"\x00\x00\x00\x18ftypisom" + b"i" * 40
OUTRO = b"\x00\x00\x00\x18ftypisom" + b"o" * 60
SERIES_INTRO = b"\x00\x00\x00\x18ftypisom" + b"s" * 50
PACKAGE_HASH = "a" * 64
SERIES_HASH = "b" * 64


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _app(*, token: bool = True) -> FastAPI:
    app = FastAPI()
    app.add_exception_handler(AppError, app_error_handler)  # type: ignore[arg-type]
    app.include_router(admin_api.media_router, prefix="/api/v1")

    async def session() -> Any:
        fake = AsyncMock()
        fake.scalar = AsyncMock(return_value=None)
        yield fake

    app.dependency_overrides[get_session] = session
    if token:
        app.dependency_overrides[speech_api.video_tool] = lambda: VideoToolToken(
            id=uuid4(), name="t", token_hash="h", token_prefix="mkv_x"
        )
    return app


def _clip(file: str, data: bytes, frames: int) -> dict[str, Any]:
    return {"file": file, "sha256": _sha(data), "frames": frames}


def _install(work: Path) -> None:
    """What ``branding --install`` leaves behind for the channel and for 原來如此."""
    channel = work / "_branding" / PACKAGE_HASH
    channel.mkdir(parents=True)
    (channel / "intro.mp4").write_bytes(INTRO)
    (channel / "outro.mp4").write_bytes(OUTRO)
    (work / "_branding" / "current.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "id": "mokaair-brand-package-v4-endscreen",
                "hash": PACKAGE_HASH,
                "installed_at": "2026-10-12T10:35:01.804Z",
                "intro": _clip(f"{PACKAGE_HASH}/intro.mp4", INTRO, 150),
                "outro": _clip(f"{PACKAGE_HASH}/outro.mp4", OUTRO, 630),
            }
        )
    )
    series = work / "_branding" / SERIES_HASH
    series.mkdir()
    (series / "intro.mp4").write_bytes(SERIES_INTRO)
    (series / "outro.mp4").write_bytes(OUTRO)
    current = work / "_branding" / "series" / "sothatswhy"
    current.mkdir(parents=True)
    (current / "current.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "id": "mokaair-sothatswhy-bookends-v3-endscreen",
                "hash": SERIES_HASH,
                "installed_at": "2026-10-12T10:35:03.022Z",
                "intro": _clip(f"../../{SERIES_HASH}/intro.mp4", SERIES_INTRO, 357),
                "outro": _clip(f"../../{SERIES_HASH}/outro.mp4", OUTRO, 630),
            }
        )
    )


def _rewrite(work: Path, **changes: Any) -> None:
    file = work / "_branding" / "current.json"
    file.write_text(json.dumps({**json.loads(file.read_text()), **changes}))


@pytest.fixture
def work(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    root = tmp_path / "video-work"
    root.mkdir()
    settings = Settings(video_work_dir=str(root))
    monkeypatch.setattr(admin_api, "get_settings", lambda: settings)
    monkeypatch.setattr(admin_api, "enforce_named_rate_limit", AsyncMock())
    return root


async def _get(path: str, *, token: bool = True, **kwargs: Any) -> Any:
    async with AsyncClient(
        transport=ASGITransport(app=_app(token=token)), base_url="http://t"
    ) as client:
        return await client.get(f"/api/v1/video/media{path}", **kwargs)


@pytest.mark.asyncio
async def test_every_branding_route_needs_a_video_tool_token(work: Path) -> None:
    _install(work)
    for path in ("/branding", "/branding/series/sothatswhy", f"/branding/files/{_sha(INTRO)}"):
        response = await _get(path, token=False)
        assert response.status_code == 401, path


@pytest.mark.asyncio
async def test_the_channel_and_series_packages_are_described_as_installed(work: Path) -> None:
    _install(work)
    channel = await _get("/branding")
    series = await _get("/branding/series/sothatswhy")
    assert channel.status_code == 200, channel.text
    assert channel.json() == {
        "series": None,
        "id": "mokaair-brand-package-v4-endscreen",
        "hash": PACKAGE_HASH,
        "installed_at": "2026-10-12T10:35:01.804Z",
        "intro": {"sha256": _sha(INTRO), "frames": 150, "size": len(INTRO)},
        "outro": {"sha256": _sha(OUTRO), "frames": 630, "size": len(OUTRO)},
    }
    assert series.status_code == 200, series.text
    body = series.json()
    assert body["series"] == "sothatswhy" and body["hash"] == SERIES_HASH
    assert body["intro"] == {"sha256": _sha(SERIES_INTRO), "frames": 357, "size": len(SERIES_INTRO)}


@pytest.mark.asyncio
async def test_a_current_file_is_served_by_its_hash_with_ranges(work: Path) -> None:
    _install(work)
    whole = await _get(f"/branding/files/{_sha(OUTRO)}")
    part = await _get(f"/branding/files/{_sha(SERIES_INTRO)}", headers={"Range": "bytes=0-7"})
    assert whole.status_code == 200 and whole.content == OUTRO
    assert whole.headers["content-type"] == "video/mp4"
    assert whole.headers["etag"] == f'"{_sha(OUTRO)}"'
    assert whole.headers["cache-control"] == "private, no-store"
    assert whole.headers["x-content-type-options"] == "nosniff"
    assert part.status_code == 206 and part.content == SERIES_INTRO[:8]


@pytest.mark.asyncio
async def test_only_files_a_current_package_names_are_served(work: Path) -> None:
    _install(work)
    # A cut on the same volume, and an older package's file still on disk: neither is named.
    cut = work / "some-video" / "final.mp4"
    cut.parent.mkdir()
    cut.write_bytes(b"cut")
    old = work / "_branding" / ("c" * 64) / "outro.mp4"
    old.parent.mkdir()
    old.write_bytes(b"old outro")
    for data in (b"cut", b"old outro"):
        response = await _get(f"/branding/files/{_sha(data)}")
        assert response.status_code == 404
        assert response.json()["code"] == "video_branding_file_not_found"
    assert (await _get("/branding/files/..%2F..%2Fetc%2Fpasswd")).status_code == 404


@pytest.mark.asyncio
async def test_nothing_installed_a_missing_volume_and_an_unknown_series_say_so(
    work: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    empty = await _get("/branding")
    unknown = await _get("/branding/series/other")
    _install(work)
    monkeypatch.setattr(
        admin_api, "get_settings", lambda: Settings(video_work_dir=str(work / "absent"))
    )
    unmounted = await _get("/branding")
    for response in (empty, unknown, unmounted):
        assert response.status_code == 404
        assert response.json()["code"] == "video_branding_not_installed"


@pytest.mark.asyncio
async def test_a_package_switched_off_is_not_handed_out(work: Path) -> None:
    (work / "_branding").mkdir()
    (work / "_branding" / "current.json").write_text('{"enabled": false}')
    response = await _get("/branding")
    assert response.status_code == 404 and response.json()["code"] == "video_branding_disabled"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "changes",
    [
        {"schema_version": 2},
        {"hash": "short"},
        {"intro": {"file": "../../outside.mp4", "sha256": "d" * 64, "frames": 150}},
        {"intro": {"file": f"{PACKAGE_HASH}/intro.mp4", "sha256": "d" * 64, "frames": 0}},
        {"outro": {"file": f"{PACKAGE_HASH}/missing.mp4", "sha256": "d" * 64, "frames": 630}},
    ],
)
async def test_a_current_json_the_tool_would_refuse_is_reported_broken(
    work: Path, changes: dict[str, Any]
) -> None:
    _install(work)
    (work / "outside.mp4").write_bytes(b"outside")
    _rewrite(work, **changes)
    response = await _get("/branding")
    assert response.status_code == 503 and response.json()["code"] == "video_branding_broken"


@pytest.mark.asyncio
async def test_a_file_outside_the_branding_folder_is_never_served(work: Path) -> None:
    _install(work)
    secret = work / "secret.mp4"
    secret.write_bytes(b"not a bookend")
    intro = work / "_branding" / PACKAGE_HASH / "intro.mp4"
    intro.unlink()
    intro.symlink_to(secret)
    _rewrite(work, intro=_clip(f"{PACKAGE_HASH}/intro.mp4", b"not a bookend", 150))
    described = await _get("/branding")
    served = await _get(f"/branding/files/{_sha(b'not a bookend')}")
    assert described.status_code == 503 and described.json()["code"] == "video_branding_broken"
    assert served.status_code == 404
    (work / "_branding" / "current.json").write_text("{not json")
    assert (await _get("/branding")).json()["code"] == "video_branding_broken"
