"""``python -m app.cli video-media-prune [--dry-run]``: the store's housekeeping, on demand.

The API runs the same pruning at most once an hour from a submission; this is for the host
when the disk is tight or before a redeploy, and for seeing what would go first.
"""

from __future__ import annotations

from typing import Any

from app.db import SessionFactory
from app.video_media.jobs import prune
from app.video_media.settings import get_media_settings
from app.video_media.storage import MediaStore


async def prune_video_media(*, dry_run: bool = False) -> dict[str, Any]:
    media = get_media_settings()
    store = MediaStore(
        media.video_media_dir,
        max_file_bytes=media.video_media_max_file_bytes,
        max_total_bytes=media.video_media_max_total_bytes,
    )
    async with SessionFactory() as session:
        result = await prune(session, store, media, dry_run=dry_run)
    return {"dry_run": dry_run, **result.model_dump(), "store_bytes": store.used_bytes()}
