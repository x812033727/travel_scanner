"""One zip of a manual upload package: every file the guide on /admin/videos lists, under the
names that page gives them (final.mp4, thumbnail.en.jpg, ja.vtt, description.en.txt ...), so the
owner downloads one archive instead of a dozen files.

The page names the entries (``<sha256>:<name>``), because it is the page that decides which
review's files make up the package and what each one is called; the API only lets through files
some review of the video actually shows. The archive is stored, not compressed: an MP4 does not
shrink, and storing streams the gigabyte straight from the review store without buffering it.
"""

from __future__ import annotations

import re
import zipfile
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import IO, Any, cast

from app.problems import AppError
from app.video_reviews.storage import ReviewStore, valid_sha256

ENTRY_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
MAX_ENTRIES = 64
CHUNK = 1 << 20


def parse_entries(raw: list[str]) -> list[tuple[str, str]]:
    """``<sha256>:<name>`` items into (sha256, name) pairs; a bad or repeated name is refused."""
    if not raw or len(raw) > MAX_ENTRIES:
        raise AppError(422, "video_package_entries_invalid", "壓縮檔要有 1 到 64 個檔案")
    entries: list[tuple[str, str]] = []
    names: set[str] = set()
    for item in raw:
        sha256, _, name = item.partition(":")
        if not valid_sha256(sha256) or not ENTRY_NAME.fullmatch(name) or ".." in name:
            raise AppError(422, "video_package_entries_invalid", f"檔名不合法：{item[:120]}")
        if name.lower() in names:
            raise AppError(422, "video_package_entries_invalid", f"檔名重複：{name}")
        names.add(name.lower())
        entries.append((sha256, name))
    return entries


def resolve_entries(
    store: ReviewStore, slug: str, shown: list[list[Any]], entries: list[tuple[str, str]]
) -> list[tuple[str, Path]]:
    """Each wanted file's path, when a review of the video shows it and the store still has it."""
    known = {
        str(item["sha256"])
        for files in shown
        for item in files
        if isinstance(item, dict) and "sha256" in item
    }
    resolved: list[tuple[str, Path]] = []
    for sha256, name in entries:
        path = store.path(slug, sha256) if sha256 in known else None
        if path is None:
            raise AppError(404, "video_review_file_not_found", f"這個檔案已經不在審核區：{name}")
        resolved.append((name, path))
    return resolved


class _Sink:
    """What zipfile writes into: unseekable, so it writes data descriptors and never looks back."""

    def __init__(self) -> None:
        self.chunks: list[bytes] = []
        self.position = 0

    def write(self, data: bytes) -> int:
        self.chunks.append(bytes(data))
        self.position += len(data)
        return len(data)

    def tell(self) -> int:
        return self.position

    def flush(self) -> None:
        return None

    def drain(self) -> bytes:
        out = b"".join(self.chunks)
        self.chunks = []
        return out


def stream_zip(files: list[tuple[str, Path]]) -> Iterator[bytes]:
    """The archive's bytes, a megabyte or so at a time, stored (not deflated) and zip64 when a
    file needs it."""
    sink = _Sink()
    stamp = datetime.now(UTC).timetuple()[:6]
    target = cast(IO[bytes], sink)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_STORED, allowZip64=True) as archive:
        for name, path in files:
            size = path.stat().st_size
            info = zipfile.ZipInfo(name, date_time=stamp)
            info.compress_type = zipfile.ZIP_STORED
            info.file_size = size
            entry = archive.open(info, "w", force_zip64=size >= 1 << 31)
            with entry, path.open("rb") as source:
                while chunk := source.read(CHUNK):
                    entry.write(chunk)
                    yield sink.drain()
            yield sink.drain()
    yield sink.drain()
