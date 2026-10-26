"""A video's review attachments, read back by the video tool (``review-files``).

The pipeline uploads a cut's previews, final, captions, descriptions, thumbnails and dub tracks
to the review store with its video tool token, and until 2026-10-26 only a signed-in owner could
read them back. A video made in a cloud container whose work directory is gone (the session
ended) could then not be rebuilt anywhere but on the owner's machine: on 2026-10-26 the approved
``ollama-phonon-local-speech-language-gap`` needed its channel bookends added and no producer
held its files.

Only files that a live review of the same video lists are served: a pending or approved one,
or a review that a live owner renewal of the final names in its ``retained_review_ids``. A
renewal supersedes the old final, publish and languages reviews but keeps their attachments,
because the publish package and the languages are rebuilt from exactly those files; the
renewed Ollama video needed its eight languages' dubs back the same day. Any other rejected or
superseded review's files, another video's, and anything the store holds that no review names
stay unreadable, as the owner's own file route already refuses anything outside the video's
reviews. The store checked each file's SHA-256 when its last part arrived; the
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
        "這個檔案不在這支影片待審、已核准或換版保留的審核裡（可能被退回、已被新版取代，或審核區已清掉）",
    )


def readable(reviews: list[Any]) -> list[Any]:
    """The live reviews, then the superseded ones a live owner renewal retains, newest first."""
    live = [review for review in reviews if review.status in READABLE]
    retained: set[str] = set()
    for review in live:
        renewal = (review.payload or {}).get(service.RENEWAL_KEY)
        ids = renewal.get("retained_review_ids") if isinstance(renewal, dict) else None
        if isinstance(ids, list):
            retained.update(item for item in ids if isinstance(item, str))
    kept = [r for r in reviews if r.status not in READABLE and str(r.id) in retained]
    return live + kept


async def file_for_tool(
    session: AsyncSession, store: ReviewStore, slug: str, sha256: str
) -> tuple[Path, str]:
    """The path and content type of a file a readable review of ``slug`` lists."""
    if not SHA256.fullmatch(sha256):
        raise _not_found()
    project = await service._project(session, slug)  # noqa: SLF001 - the module's own lookup
    for review in readable(await service._reviews(session, project)):  # noqa: SLF001
        for item in review.files or []:
            if isinstance(item, dict) and item.get("sha256") == sha256:
                path = store.path(slug, sha256)
                if path is None:
                    raise _not_found()
                return path, str(item.get("content_type") or "application/octet-stream")
    raise _not_found()


def listing(reviews: list[Any]) -> list[dict[str, Any]]:
    """Every file of every readable review (for tests and docs)."""
    out: list[dict[str, Any]] = []
    for review in readable(reviews):
        for item in review.files or []:
            if isinstance(item, dict) and SHA256.fullmatch(str(item.get("sha256", ""))):
                out.append({"gate": review.gate, "status": review.status, **item})
    return out
