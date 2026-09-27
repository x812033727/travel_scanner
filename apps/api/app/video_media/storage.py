"""The media store on disk: generated images, clips and music, named by their SHA-256.

The same layout and part upload as the review store (``app.video_reviews.storage``), in its
own directory (a volume in docker-compose.prod.yml), plus a streaming write for files the API
downloads from a vendor: the hash is computed as the bytes arrive, the type is read from the
first bytes rather than trusted from the vendor, and the caps are enforced before the file is
given its name. Files are a pipeline cache: ``prune`` deletes what no live job names.
"""

from __future__ import annotations

import hashlib
import os
import shutil
from collections.abc import AsyncIterator
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from app.video_reviews.storage import ReviewStore, StorageRefused, valid_sha256, valid_slug

CONTENT_TYPES = frozenset(
    {"image/png", "image/jpeg", "image/webp", "video/mp4", "audio/mpeg", "audio/wav"}
)
EXTENSIONS = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/webp": "webp",
    "video/mp4": "mp4",
    "audio/mpeg": "mp3",
    "audio/wav": "wav",
}


@dataclass(frozen=True)
class StoredFile:
    sha256: str
    size: int
    content_type: str


def sniff_type(head: bytes) -> str | None:
    """The media type the first bytes say a file is; None when it is none of ours."""
    if head.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png"
    if head.startswith(b"\xff\xd8\xff"):
        return "image/jpeg"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "image/webp"
    if head[:4] == b"RIFF" and head[8:12] == b"WAVE":
        return "audio/wav"
    if head[4:8] == b"ftyp":
        return "video/mp4"
    if head.startswith(b"ID3") or head[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"):
        return "audio/mpeg"
    return None


class MediaStore(ReviewStore):
    def writable(self) -> bool:
        try:
            self.root.mkdir(parents=True, exist_ok=True)
        except OSError:
            return False
        return os.access(self.root, os.W_OK)

    def slugs(self) -> list[str]:
        if not self.root.is_dir():
            return []
        return sorted(
            entry.name for entry in self.root.iterdir() if entry.is_dir() and valid_slug(entry.name)
        )

    def files(self, slug: str) -> dict[str, Path]:
        """The project's finished files by SHA-256."""
        folder = self._project(slug)
        if not folder.is_dir():
            return {}
        return {f.name: f for f in folder.iterdir() if f.is_file() and valid_sha256(f.name)}

    async def put_stream(self, slug: str, job_id: str, chunks: AsyncIterator[bytes]) -> StoredFile:
        """Write a vendor download as it arrives; the file is named only once it checks out."""
        folder = self._project(slug)
        incoming = folder / ".incoming"
        incoming.mkdir(parents=True, exist_ok=True)
        partial = incoming / job_id
        digest = hashlib.sha256()
        size = 0
        head = b""
        budget = self.max_total_bytes - self.used_bytes()
        try:
            with partial.open("wb") as out:
                async for chunk in chunks:
                    if not chunk:
                        continue
                    if len(head) < 16:
                        head = (head + chunk)[:16]
                    size += len(chunk)
                    if size > self.max_file_bytes:
                        raise StorageRefused(
                            413,
                            "video_media_file_too_large",
                            f"生成的檔案超過 {self.max_file_bytes} 位元組",
                        )
                    if size > budget:
                        raise StorageRefused(
                            507, "video_media_store_full", "媒體庫已滿：請清理或調高上限"
                        )
                    digest.update(chunk)
                    out.write(chunk)
            content_type = sniff_type(head)
            if size == 0 or content_type is None:
                raise StorageRefused(
                    415, "video_media_unsupported_type", "廠商回傳的不是圖片、mp4 或音檔"
                )
            sha256 = digest.hexdigest()
            target = folder / sha256
            if target.is_file():
                partial.unlink(missing_ok=True)
            else:
                os.replace(partial, target)
            return StoredFile(sha256=sha256, size=size, content_type=content_type)
        finally:
            partial.unlink(missing_ok=True)

    def content_type_of(self, path: Path) -> str:
        with path.open("rb") as handle:
            return sniff_type(handle.read(16)) or "application/octet-stream"

    def prune_files(self, slug: str, keep: set[str], older_than: datetime) -> list[tuple[str, int]]:
        """Delete the project's files not in ``keep`` and last written before ``older_than``."""
        removed: list[tuple[str, int]] = []
        for name, path in self.files(slug).items():
            if name in keep:
                continue
            stat = path.stat()
            if datetime.fromtimestamp(stat.st_mtime, tz=older_than.tzinfo) >= older_than:
                continue
            path.unlink(missing_ok=True)
            removed.append((name, stat.st_size))
        incoming = self._project(slug) / ".incoming"
        if incoming.is_dir():
            for stale in incoming.iterdir():
                if datetime.fromtimestamp(stale.stat().st_mtime, tz=older_than.tzinfo) < older_than:
                    stale.unlink(missing_ok=True)
        return sorted(removed)

    def delete_project(self, slug: str) -> None:
        shutil.rmtree(self._project(slug), ignore_errors=True)
