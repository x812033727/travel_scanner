"""A video's files in the site's review store, laid out as its Drive backup folder.

Some videos are made outside the video worker (on the owner's PC, or by a session that pushes
each gate's files to the site), so the worker's ``video_work`` has no directory for them and only
the review store (``<video_review_dir>/<slug>/<sha256>``) holds their package. The worker mounts
that store read-only and copies these files when a video has no work directory
(docs/videos/BACKUP.md §沒有工作資料夾的影片).

The package is what the manual upload offers: the approved upload confirmation's files and the
approved languages batches'. For each role the newest approved review wins, whichever gate it came
from, so a languages batch approved before the confirmation still brings its dub tracks. On the
full tier a dub track or caption file that only a languages batch still waiting for the owner
holds goes to the same unpackaged folders as a work directory's (dubs/未進上傳包/,
captions/未進上傳包/), so the site never counts it as packaged.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import UTC, datetime

from app.models import VideoReview

UNPACKAGED_DUBS = "dubs/未進上傳包"
UNPACKAGED_CAPTIONS = "captions/未進上傳包"
LOCALE = r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})?"
_LOCALE_ROLE = re.compile(rf"^(captions|description|dub|thumbnail)_({LOCALE})$")
_THUMBNAIL_VARIANT = re.compile(r"^thumbnail-([a-z0-9]{1,8})$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
EPOCH = datetime(1970, 1, 1, tzinfo=UTC)


@dataclass(frozen=True)
class ReviewFile:
    path: str
    sha256: str
    size: int


def _image(content_type: str) -> str:
    return "png" if content_type == "image/png" else "jpg"


def _audio(content_type: str) -> str:
    return {"audio/mpeg": "mp3", "audio/wav": "wav", "audio/x-wav": "wav"}.get(content_type, "m4a")


def _caption(content_type: str) -> str:
    return "vtt" if content_type == "text/vtt" else "srt"


def package_path(role: str, content_type: str) -> str | None:
    """Where a review file goes in the backup folder, as the upload package names it; None for
    a file that is not part of the package (contact sheets, keyframes, the languages manifest)."""
    if role == "final":
        return "final.mp4"
    if role == "metadata":
        return "metadata.json"
    if role == "thumbnail":
        return f"thumbnail.{_image(content_type)}"
    if variant := _THUMBNAIL_VARIANT.match(role):
        return f"thumbnail-{variant[1]}.{_image(content_type)}"
    matched = _LOCALE_ROLE.match(role)
    if matched is None:
        return None
    kind, locale = matched[1], matched[2]
    if kind == "captions":
        return f"captions/{locale}.{_caption(content_type)}"
    if kind == "description":
        return f"descriptions/{locale}.txt"
    if kind == "dub":
        return f"dubs/{locale}.{_audio(content_type)}"
    return f"thumbnails/{locale}.{_image(content_type)}"


def _unpackaged(path: str) -> str | None:
    """Where a dub or caption file only a pending batch holds goes; None for anything else."""
    if path.startswith("dubs/"):
        return f"{UNPACKAGED_DUBS}/{path.removeprefix('dubs/')}"
    if path.startswith("captions/"):
        return f"{UNPACKAGED_CAPTIONS}/{path.removeprefix('captions/')}"
    if path.startswith("thumbnails/"):
        return path
    return None


def _entries(review: VideoReview) -> Iterable[tuple[str, str, int]]:
    for item in review.files or []:
        if not isinstance(item, dict):
            continue
        sha256 = str(item.get("sha256") or "")
        size = item.get("size")
        path = package_path(str(item.get("role") or ""), str(item.get("content_type") or ""))
        if path is None or not _SHA256.match(sha256) or type(size) is not int or size < 0:
            continue
        yield path, sha256, size


def _when(review: VideoReview) -> datetime:
    return review.decided_at or review.created_at or EPOCH


def backup_files(
    reviews: Iterable[VideoReview], *, full: bool, held: Callable[[str], bool]
) -> list[ReviewFile]:
    """The backup folder's files from one video's reviews. ``held(sha256)`` says whether the store
    still has that file (the mp4 goes PREVIEW_RETENTION after the upload); a file it lacks is left
    out, and the site counts it as missing as it would for a work directory."""
    rows = list(reviews)
    publish = [row for row in rows if row.gate == "publish" and row.status == "approved"]
    approved = sorted(
        [
            *([max(publish, key=_when)] if publish else []),
            *(row for row in rows if row.gate == "languages" and row.status == "approved"),
        ],
        key=_when,
    )
    chosen: dict[str, tuple[str, int]] = {}
    for review in approved:
        for path, sha256, size in _entries(review):
            chosen[path] = (sha256, size)
    if full:
        pending = sorted(
            (row for row in rows if row.gate == "languages" and row.status == "pending"), key=_when
        )
        for review in pending:
            for path, sha256, size in _entries(review):
                where = _unpackaged(path)
                if where is not None and path not in chosen:
                    chosen[where] = (sha256, size)
    return [
        ReviewFile(path=path, sha256=sha256, size=size)
        for path, (sha256, size) in sorted(chosen.items())
        if held(sha256)
    ]
