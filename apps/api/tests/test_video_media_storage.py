"""The media store: streamed writes named by their hash, type sniffing, caps and pruning."""

from __future__ import annotations

import hashlib
import os
import time
from collections.abc import AsyncIterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from app.video_media.storage import MediaStore, sniff_type
from app.video_reviews.storage import StorageRefused

PNG = b"\x89PNG\r\n\x1a\n" + b"\x00" * 40
JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 40
MP4 = b"\x00\x00\x00\x18ftypisom" + b"\x00" * 40
MP3 = b"ID3\x03" + b"\x00" * 40
WAV = b"RIFF\x00\x00\x00\x00WAVEfmt " + b"\x00" * 40
WEBP = b"RIFF\x00\x00\x00\x00WEBPVP8 " + b"\x00" * 40


def _store(root: Path, **limits: int) -> MediaStore:
    return MediaStore(
        root,
        max_file_bytes=limits.get("max_file_bytes", 10_000_000),
        max_total_bytes=limits.get("max_total_bytes", 50_000_000),
    )


async def _chunks(data: bytes, size: int = 7) -> AsyncIterator[bytes]:
    for start in range(0, len(data), size):
        yield data[start : start + size]


def test_the_first_bytes_say_what_a_file_is() -> None:
    assert sniff_type(PNG) == "image/png"
    assert sniff_type(JPEG) == "image/jpeg"
    assert sniff_type(MP4) == "video/mp4"
    assert sniff_type(MP3) == "audio/mpeg"
    assert sniff_type(b"\xff\xfb\x90\x00") == "audio/mpeg"
    assert sniff_type(WAV) == "audio/wav"
    assert sniff_type(WEBP) == "image/webp"
    assert sniff_type(b"<html>") is None
    assert sniff_type(b"") is None


@pytest.mark.asyncio
async def test_a_streamed_download_is_hashed_typed_and_named_only_once_it_is_whole(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path)
    stored = await store.put_stream("jingwei", "job-1", _chunks(MP4))
    assert stored.sha256 == hashlib.sha256(MP4).hexdigest()
    assert (stored.size, stored.content_type) == (len(MP4), "video/mp4")
    path = store.path("jingwei", stored.sha256)
    assert path is not None and path.read_bytes() == MP4
    assert store.content_type_of(path) == "video/mp4"
    assert not (tmp_path / "jingwei" / ".incoming" / "job-1").exists()
    again = await store.put_stream("jingwei", "job-2", _chunks(MP4))
    assert again.sha256 == stored.sha256, "the same bytes are one file"
    assert store.files("jingwei") == {stored.sha256: path}
    assert store.slugs() == ["jingwei"]
    assert store.writable()


@pytest.mark.asyncio
async def test_a_download_that_is_too_large_or_not_media_leaves_nothing_behind(
    tmp_path: Path,
) -> None:
    store = _store(tmp_path, max_file_bytes=30)
    with pytest.raises(StorageRefused) as too_big:
        await store.put_stream("v", "job-1", _chunks(PNG))
    assert too_big.value.code == "video_media_file_too_large"
    with pytest.raises(StorageRefused) as not_media:
        await _store(tmp_path).put_stream("v", "job-2", _chunks(b"<html>not a picture</html>"))
    assert not_media.value.code == "video_media_unsupported_type"
    with pytest.raises(StorageRefused) as empty:
        await _store(tmp_path).put_stream("v", "job-3", _chunks(b""))
    assert empty.value.code == "video_media_unsupported_type"
    assert store.files("v") == {}
    assert not any((tmp_path / "v" / ".incoming").iterdir())


@pytest.mark.asyncio
async def test_the_total_cap_counts_what_is_already_stored(tmp_path: Path) -> None:
    store = _store(tmp_path, max_total_bytes=len(MP4) + 10)
    await store.put_stream("v", "job-1", _chunks(MP4))
    with pytest.raises(StorageRefused) as full:
        await store.put_stream("v", "job-2", _chunks(PNG))
    assert full.value.code == "video_media_store_full" and full.value.status == 507


def test_pruning_keeps_named_files_and_recent_ones(tmp_path: Path) -> None:
    store = _store(tmp_path)
    old = tmp_path / "v" / hashlib.sha256(PNG).hexdigest()
    kept = tmp_path / "v" / hashlib.sha256(JPEG).hexdigest()
    fresh = tmp_path / "v" / hashlib.sha256(MP4).hexdigest()
    stale_part = tmp_path / "v" / ".incoming" / "job-9"
    stale_part.parent.mkdir(parents=True)
    for file, data in ((old, PNG), (kept, JPEG), (fresh, MP4), (stale_part, b"x")):
        file.write_bytes(data)
    week_ago = time.time() - 7 * 86400
    for file in (old, kept, stale_part):
        os.utime(file, (week_ago, week_ago))
    cutoff = datetime.now(UTC) - timedelta(days=1)
    removed = store.prune_files("v", {kept.name}, cutoff)
    assert removed == [(old.name, len(PNG))]
    assert kept.exists() and fresh.exists() and not old.exists()
    assert not stale_part.exists(), "an abandoned partial download goes too"
    assert store.prune_files("nobody", set(), cutoff) == []
