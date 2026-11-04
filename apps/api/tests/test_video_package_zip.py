"""One zip of a manual upload package (app/video_reviews/admin_package_zip.py and its route)."""

from __future__ import annotations

import hashlib
import io
import zipfile
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

from app.config import Settings
from app.models import User
from app.problems import AppError
from app.video_reviews import admin_api, admin_service
from app.video_reviews import admin_package_zip as package_zip
from app.video_reviews.storage import ReviewStore
from tests.test_video_reviews import _app


def _stored(root: Path, slug: str, body: bytes) -> str:
    sha = hashlib.sha256(body).hexdigest()
    (root / slug).mkdir(parents=True, exist_ok=True)
    (root / slug / sha).write_bytes(body)
    return sha


def test_entries_are_sha_colon_name_each_name_once_and_never_a_path() -> None:
    good = package_zip.parse_entries([f"{'a' * 64}:final.mp4", f"{'b' * 64}:thumbnail.zh-TW.jpg"])
    assert good == [("a" * 64, "final.mp4"), ("b" * 64, "thumbnail.zh-TW.jpg")]
    for raw in (
        [],
        [f"{'a' * 64}:../final.mp4"],
        [f"{'a' * 64}:.hidden"],
        [f"{'a' * 64}:sub/final.mp4"],
        ["abc:final.mp4"],
        [f"{'a' * 64}:final.mp4", f"{'b' * 64}:FINAL.mp4"],
        [f"{'a' * 64}:x{index}" for index in range(65)],
    ):
        with pytest.raises(AppError) as refused:
            package_zip.parse_entries(raw)
        assert refused.value.status == 422


def test_only_files_a_review_shows_and_the_store_still_has_resolve(tmp_path: Path) -> None:
    store = ReviewStore(tmp_path, max_file_bytes=10_000, max_total_bytes=100_000)
    kept = _stored(tmp_path, "v", b"kept")
    gone = hashlib.sha256(b"gone").hexdigest()
    shown: list[list[Any]] = [[{"role": "final", "sha256": kept}, {"role": "x", "sha256": gone}]]
    assert package_zip.resolve_entries(store, "v", shown, [(kept, "final.mp4")]) == [
        ("final.mp4", tmp_path / "v" / kept)
    ]
    other = _stored(tmp_path, "v", b"not shown by any review")
    for sha in (gone, other):
        with pytest.raises(AppError) as refused:
            package_zip.resolve_entries(store, "v", shown, [(sha, "a.txt")])
        assert refused.value.status == 404


def test_the_archive_streams_stored_entries_that_unzip_byte_for_byte(tmp_path: Path) -> None:
    video = tmp_path / "final.mp4"
    video.write_bytes(bytes(range(256)) * 9000)  # a few chunks' worth
    text = tmp_path / "en.srt"
    text.write_bytes(b"1\n00:00:00,000 --> 00:00:01,000\nhi\n")
    chunks = list(package_zip.stream_zip([("final.mp4", video), ("en.srt", text)]))
    assert len(chunks) > 3 and all(len(chunk) <= 2 * package_zip.CHUNK for chunk in chunks)
    with zipfile.ZipFile(io.BytesIO(b"".join(chunks))) as archive:
        assert archive.testzip() is None
        assert [info.filename for info in archive.infolist()] == ["final.mp4", "en.srt"]
        assert all(info.compress_type == zipfile.ZIP_STORED for info in archive.infolist())
        assert archive.read("final.mp4") == video.read_bytes()
        assert archive.read("en.srt") == text.read_bytes()


@pytest.mark.asyncio
async def test_the_package_route_names_the_archive_and_never_caches_it(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    thumbnail = tmp_path / "t.png"
    thumbnail.write_bytes(b"PNG")
    resolve = AsyncMock(return_value=[("thumbnail.png", thumbnail)])
    monkeypatch.setattr(admin_service, "package_files_for_admin", resolve)

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    app = _app(owner)
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/api/v1/admin/videos/v/package.zip", params=[("file", f"{'a' * 64}:thumbnail.png")]
        )
        refused = await client.get("/api/v1/admin/videos/v/package.zip", params=[("file", "x:y")])
        empty = await client.get("/api/v1/admin/videos/v/package.zip")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/zip"
    assert response.headers["content-disposition"] == 'attachment; filename="v-upload.zip"'
    assert response.headers["cache-control"] == "private, no-store"
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        assert archive.read("thumbnail.png") == b"PNG"
    assert resolve.await_args is not None
    assert resolve.await_args.args[3] == [("a" * 64, "thumbnail.png")]
    assert refused.status_code == 422 and refused.json()["code"] == "video_package_entries_invalid"
    assert empty.status_code == 422


def test_the_check_names_each_file_the_archive_would_miss_and_why(tmp_path: Path) -> None:
    store = ReviewStore(tmp_path, max_file_bytes=10_000, max_total_bytes=100_000)
    kept = _stored(tmp_path, "v", b"kept")
    gone = hashlib.sha256(b"gone").hexdigest()
    stray = _stored(tmp_path, "v", b"not shown by any review")
    shown: list[list[Any]] = [[{"role": "final", "sha256": kept}, {"role": "x", "sha256": gone}]]
    assert package_zip.check_entries(store, "v", shown, [(kept, "final.mp4")]) == ([], 4)
    missing, size = package_zip.check_entries(
        store, "v", shown, [(kept, "final.mp4"), (gone, "dub.en.m4a"), (stray, "a.txt")]
    )
    assert missing == [
        {"name": "dub.en.m4a", "reason": "gone"},
        {"name": "a.txt", "reason": "not_shown"},
    ]
    assert size == 4


@pytest.mark.asyncio
async def test_the_check_route_answers_what_the_zip_would_miss_before_the_download(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    answer = {
        "ok": False,
        "missing": [{"name": "dub.en.m4a", "reason": "gone"}],
        "bytes": 3,
        "drive_folder": "ai-news/v",
    }
    check = AsyncMock(return_value=answer)
    monkeypatch.setattr(admin_service, "package_check_for_admin", check)

    async def settings(_: Any) -> Settings:
        return Settings(video_review_dir=str(tmp_path))

    monkeypatch.setattr(admin_api, "load_runtime_settings", settings)
    owner = User(id=uuid4(), email="owner@example.com", password_hash="unused")
    owner._admin_roles_cache = frozenset({"owner"})  # type: ignore[attr-defined]
    viewer = User(id=uuid4(), email="viewer@example.com", password_hash="unused")
    viewer._admin_roles_cache = frozenset({"viewer"})  # type: ignore[attr-defined]
    params = {"file": f"{'a' * 64}:dub.en.m4a"}
    async with AsyncClient(transport=ASGITransport(app=_app(owner)), base_url="http://test") as c:
        response = await c.get("/api/v1/admin/videos/v/package", params=params)
        refused = await c.get("/api/v1/admin/videos/v/package", params=[("file", "x:y")])
    async with AsyncClient(transport=ASGITransport(app=_app(viewer)), base_url="http://test") as c:
        forbidden = await c.get("/api/v1/admin/videos/v/package", params=params)
    assert response.status_code == 200 and response.json() == answer
    assert check.await_args is not None and check.await_args.args[3] == [("a" * 64, "dub.en.m4a")]
    assert refused.status_code == 422
    assert forbidden.status_code == 403
