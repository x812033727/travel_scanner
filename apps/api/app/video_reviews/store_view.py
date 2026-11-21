"""What GET /admin/videos/store answers: how full the preview store is (owner, 2026-11-19).

Kept apart from schemas.py, which the long-form duration review binds byte for byte.
"""

from __future__ import annotations

from pydantic import BaseModel


class ReviewStoreView(BaseModel):
    """What the store's files take, the cap the owner set (or the .env default), the largest
    file it takes, and the host disk under it, None when that cannot be read."""

    used_bytes: int
    max_total_bytes: int
    max_file_bytes: int
    disk_free_bytes: int | None = None
    disk_total_bytes: int | None = None
