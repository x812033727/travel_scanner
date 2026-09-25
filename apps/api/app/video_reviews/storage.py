"""The review files on disk: previews the owner watches, named by their SHA-256.

Production has no object storage (news images are kept in the database, capped at 5 MiB), and a
720p preview of a ten-minute video is about 100 MB, so the files live in a directory on the host
(a volume in docker-compose.prod.yml). nginx caps a request body at 6 MiB, so the pipeline sends
a file in parts of at most PART_BYTES; the last part assembles the file and checks its SHA-256
before it is used. Nothing here is served without an admin session.

Layout: ``<root>/<slug>/<sha256>`` for a finished file, ``<root>/<slug>/.parts/<sha256>/<n>``
while it arrives.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

PART_BYTES = 4 * 1024 * 1024
SLUG = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
CONTENT_TYPES = frozenset({"video/mp4", "audio/mp4", "image/png", "image/jpeg"})


class StorageRefused(Exception):
    """A request the store will not take; ``code`` is the error the API answers with."""

    def __init__(self, status: int, code: str, detail: str) -> None:
        super().__init__(detail)
        self.status = status
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class PartResult:
    received: list[int]
    complete: bool


def valid_slug(slug: str) -> bool:
    return bool(SLUG.fullmatch(slug))


def valid_sha256(value: str) -> bool:
    return bool(SHA256.fullmatch(value))


class ReviewStore:
    def __init__(self, root: str | Path, *, max_file_bytes: int, max_total_bytes: int) -> None:
        self.root = Path(root)
        self.max_file_bytes = max_file_bytes
        self.max_total_bytes = max_total_bytes

    def _project(self, slug: str) -> Path:
        if not valid_slug(slug):
            raise StorageRefused(
                422, "video_review_bad_slug", "slug must be lower-case a-z, 0-9, -"
            )
        return self.root / slug

    def _checked(self, slug: str, sha256: str) -> Path:
        if not valid_sha256(sha256):
            raise StorageRefused(422, "video_review_bad_hash", "file names are 64 hex characters")
        return self._project(slug) / sha256

    def path(self, slug: str, sha256: str) -> Path | None:
        """The finished file, or None when it has not arrived (or never will)."""
        target = self._checked(slug, sha256)
        return target if target.is_file() else None

    def used_bytes(self) -> int:
        if not self.root.exists():
            return 0
        return sum(file.stat().st_size for file in self.root.rglob("*") if file.is_file())

    def put_part(
        self, slug: str, sha256: str, *, index: int, count: int, size: int, data: bytes
    ) -> PartResult:
        """Store part ``index`` of ``count``; assemble and verify when the last one is in."""
        target = self._checked(slug, sha256)
        if target.is_file():
            return PartResult(received=list(range(count)), complete=True)
        if not 0 < size <= self.max_file_bytes:
            raise StorageRefused(
                413, "video_review_file_too_large", f"files are at most {self.max_file_bytes} bytes"
            )
        expected_count = -(-size // PART_BYTES)
        if count != expected_count or not 0 <= index < count:
            raise StorageRefused(
                422, "video_review_bad_part", f"a {size}-byte file has {expected_count} parts"
            )
        expected = PART_BYTES if index < count - 1 else size - PART_BYTES * (count - 1)
        if len(data) != expected:
            raise StorageRefused(
                422, "video_review_bad_part", f"part {index} must be {expected} bytes"
            )
        if self.used_bytes() + len(data) > self.max_total_bytes:
            raise StorageRefused(
                507, "video_review_store_full", "the review store is full; publish or delete videos"
            )
        parts = target.parent / ".parts" / sha256
        parts.mkdir(parents=True, exist_ok=True)
        partial = parts / f"{index}.tmp"
        partial.write_bytes(data)
        os.replace(partial, parts / str(index))
        received = sorted(int(name.name) for name in parts.iterdir() if name.name.isdigit())
        if received != list(range(count)):
            return PartResult(received=received, complete=False)
        self._assemble(parts, target, sha256, count, size)
        return PartResult(received=received, complete=True)

    def _assemble(self, parts: Path, target: Path, sha256: str, count: int, size: int) -> None:
        digest = hashlib.sha256()
        assembling = target.with_name(f".{sha256}.assembling")
        with assembling.open("wb") as out:
            for index in range(count):
                chunk = (parts / str(index)).read_bytes()
                digest.update(chunk)
                out.write(chunk)
        shutil.rmtree(parts, ignore_errors=True)
        if digest.hexdigest() != sha256 or assembling.stat().st_size != size:
            assembling.unlink(missing_ok=True)
            raise StorageRefused(
                422, "video_review_hash_mismatch", "the parts do not add up to that SHA-256"
            )
        os.replace(assembling, target)

    def keep_only(self, slug: str, keep: set[str]) -> list[str]:
        """Delete the project's finished files that no live review refers to; return their names."""
        folder = self._project(slug)
        if not folder.is_dir():
            return []
        removed = []
        for file in folder.iterdir():
            if file.is_file() and valid_sha256(file.name) and file.name not in keep:
                file.unlink(missing_ok=True)
                removed.append(file.name)
        return sorted(removed)

    def delete_project(self, slug: str) -> None:
        shutil.rmtree(self._project(slug), ignore_errors=True)
