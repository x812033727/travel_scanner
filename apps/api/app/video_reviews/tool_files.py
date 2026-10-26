"""A video's review attachments, read back by the video tool (``review-files``).

The pipeline uploads a cut's previews, final, captions, descriptions, thumbnails and dub tracks
to the review store with its video tool token, and until 2026-10-26 only a signed-in owner could
read them back. A video made in a cloud container whose work directory is gone (the session
ended) could then not be rebuilt anywhere but on the owner's machine: on 2026-10-26 the approved
``ollama-phonon-local-speech-language-gap`` needed its channel bookends added and no producer
held its files.

Only files that a live review of the same video lists are served: a pending or approved one.
A rejected or superseded review's files, another video's, and anything the store holds that no
review names stay unreadable, as the owner's own file route already refuses anything outside
the video's reviews. The store checked each file's SHA-256 when its last part arrived; the
tool checks it again after the download (tools/video/review/files.mjs).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.problems import AppError
from app.video_reviews import admin_service as service
from app.video_reviews.storage import ReviewStore

SHA256 = re.compile(r"^[0-9a-f]{64}$")
# Which reviews still stand: what the owner can see and decide, or has decided for.
READABLE = frozenset({"pending", "approved"})


def _not_found() -> AppError:
    return AppError(
        404,
        "video_review_file_not_found",
        "這個檔案不在這支影片待審或已核准的審核裡（可能被退回、已被新版取代，或審核區已清掉）",
    )


async def file_for_tool(
    session: AsyncSession, store: ReviewStore, slug: str, sha256: str
) -> tuple[Path, str]:
    """The path and content type of a file a pending or approved review of ``slug`` lists."""
    if not SHA256.fullmatch(sha256):
        raise _not_found()
    project = await service._project(session, slug)  # noqa: SLF001 - the module's own lookup
    for review in await service._reviews(session, project):  # noqa: SLF001
        if review.status not in READABLE:
            continue
        for item in review.files or []:
            if isinstance(item, dict) and item.get("sha256") == sha256:
                path = store.path(slug, sha256)
                if path is None:
                    raise _not_found()
                return path, str(item.get("content_type") or "application/octet-stream")
    raise _not_found()


def listing(reviews: list[Any]) -> list[dict[str, Any]]:
    """Every file of every pending or approved review, newest review first (for tests and docs)."""
    out: list[dict[str, Any]] = []
    for review in reviews:
        if review.status not in READABLE:
            continue
        for item in review.files or []:
            if isinstance(item, dict) and SHA256.fullmatch(str(item.get("sha256", ""))):
                out.append({"gate": review.gate, "status": review.status, **item})
    return out
