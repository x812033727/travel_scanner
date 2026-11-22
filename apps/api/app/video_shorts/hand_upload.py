"""Which Shorts the owner uploads by hand (docs/videos/SHORTS.md §手動上架).

The site keeps such a Short off its calendar and never uploads it or sends it under the standing
consent (owner, 2026-11-21). A Short is uploaded by hand when:

- it was pushed by hand: its final cut or upload package, waiting or approved, says
  ``hand_pushed`` (tools/video/shorts/push.mjs); or
- the YouTube video it has was linked while no upload package was approved. The site's own route
  always has one, so that upload was the owner's. The link's audit entry says when it was made
  and the publish reviews say what was approved then; a link corrected later keeps the moment of
  the first, until the owner unlinks.

Nothing is stored for this: it is read where it is asked, so a link counts from its commit.
Only the models are imported: the calendar and the YouTube sync both read this module.
"""

from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import AdminAuditLog, VideoProject, VideoReview

# What ``admin_service.link_youtube`` and ``unlink_youtube`` write to the audit log.
LINKED = "video_youtube_linked"
UNLINKED = "video_youtube_unlinked"
NOT_SENT = "這支是手動上架：網站不會自動排程，也不會替你上傳"


async def hand_uploaded(session: AsyncSession, projects: Iterable[VideoProject]) -> frozenset[str]:
    """The slugs of these projects that are Shorts the owner uploads by hand."""
    shorts = {project.id: project for project in projects if project.shorts_line is not None}
    if not shorts:
        return frozenset()
    found: set[str] = set()
    # When each Short's packages stood approved: from the decision until one was superseded.
    approvals: dict[UUID, list[tuple[datetime, datetime | None]]] = {}
    for project_id, gate, status, payload, decided_at, updated_at in await session.execute(
        select(
            VideoReview.project_id,
            VideoReview.gate,
            VideoReview.status,
            VideoReview.payload,
            VideoReview.decided_at,
            VideoReview.updated_at,
        ).where(
            VideoReview.project_id.in_(list(shorts)),
            VideoReview.gate.in_(("final", "publish")),
            VideoReview.status.in_(("pending", "approved", "superseded")),
        )
    ):
        # Read in Python: JSON's true is "true" in PostgreSQL and 1 in SQLite; only true counts.
        pushed = isinstance(payload, dict) and payload.get("hand_pushed") is True
        if pushed and status != "superseded":
            found.add(shorts[project_id].slug)
        if gate == "publish" and status != "pending" and decided_at is not None:
            until = updated_at if status == "superseded" else None
            approvals.setdefault(project_id, []).append((decided_at, until))
    linked = {
        f"video_project:{project.slug}": project
        for project in shorts.values()
        if project.youtube_video_id is not None and project.slug not in found
    }
    if not linked:
        return frozenset(found)
    # For each Short, when it was first linked since it was last unlinked, and the newest id.
    links: dict[str, tuple[datetime, str]] = {}
    for target, action, recorded, at in await session.execute(
        select(
            AdminAuditLog.target,
            AdminAuditLog.action,
            AdminAuditLog.metadata_json,
            AdminAuditLog.created_at,
        )
        .where(
            AdminAuditLog.action.in_((LINKED, UNLINKED)),
            AdminAuditLog.target.in_(list(linked)),
        )
        .order_by(AdminAuditLog.created_at)
    ):
        if action == UNLINKED:
            links.pop(target, None)
        elif isinstance(recorded, dict):
            first = links[target][0] if target in links else at
            links[target] = (first, str(recorded.get("youtube_video_id")))
    for target, (first, video_id) in links.items():
        project = linked[target]
        approved = any(
            start <= first and (end is None or first < end)
            for start, end in approvals.get(project.id, [])
        )
        if video_id == project.youtube_video_id and not approved:
            found.add(project.slug)
    return frozenset(found)


async def is_hand_uploaded(session: AsyncSession, project: VideoProject) -> bool:
    return project.slug in await hand_uploaded(session, [project])
