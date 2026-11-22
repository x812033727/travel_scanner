"""Which Shorts the owner uploads by hand (docs/videos/SHORTS.md §手動上架).

The site keeps such a Short off its calendar and never uploads it or sends it under the standing
consent (owner, 2026-11-21). A Short is uploaded by hand when:

- it was pushed by hand: its final cut or upload package, waiting or approved, says
  ``hand_pushed`` (tools/video/shorts/push.mjs); or
- the YouTube video it has was linked before any upload package was approved. The site's own
  route always has one, so that upload was the owner's. ``link_youtube`` marks the audit entry.

Only the models are imported: the review store and the YouTube sync read this module too.
"""

from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, VideoProject, VideoReview

LINKED_ACTION = "video_youtube_linked"
LINKED_MARK = "by_hand"
NOT_SENT = "這支是手動上架：網站不會自動排程，也不會替你上傳"


async def hand_uploaded(session: AsyncSession, projects: Iterable[VideoProject]) -> frozenset[str]:
    """The slugs of these projects that are Shorts the owner uploads by hand."""
    shorts = {project.id: project for project in projects if project.shorts_line is not None}
    if not shorts:
        return frozenset()
    found: set[str] = set()
    # Read in Python: JSON's true is "true" in PostgreSQL and 1 in SQLite, and only true counts.
    for project_id, payload in await session.execute(
        select(VideoReview.project_id, VideoReview.payload).where(
            VideoReview.project_id.in_(list(shorts)),
            VideoReview.gate.in_(("final", "publish")),
            VideoReview.status.in_(("pending", "approved")),
        )
    ):
        if isinstance(payload, dict) and payload.get("hand_pushed") is True:
            found.add(shorts[project_id].slug)
    linked = {
        f"video_project:{project.slug}": project
        for project in shorts.values()
        if project.youtube_video_id is not None and project.slug not in found
    }
    if linked:
        for target, recorded in await session.execute(
            select(AdminAuditLog.target, AdminAuditLog.metadata_json).where(
                AdminAuditLog.action == LINKED_ACTION,
                AdminAuditLog.target.in_(list(linked)),
            )
        ):
            project = linked[target]
            if (
                isinstance(recorded, dict)
                and recorded.get(LINKED_MARK) is True
                and recorded.get("youtube_video_id") == project.youtube_video_id
            ):
                found.add(project.slug)
    return frozenset(found)


async def is_hand_uploaded(session: AsyncSession, project: VideoProject) -> bool:
    return project.slug in await hand_uploaded(session, [project])
