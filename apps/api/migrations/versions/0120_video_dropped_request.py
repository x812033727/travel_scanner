"""Cancel the drama requests still started for a video the owner dropped.

Revision ID: 0120_video_dropped_request
Revises: 0119_video_category_anime

Since ticket 2026-09-28-video-dropped-episode-request, dropping a video on /admin/videos moves
the request row it travelled as from ``started`` to ``cancelled`` (``_cancel_started_request``
in app.video_reviews.admin_service). Videos dropped before that shipped left their request
``started``, so the owner's request list still shows them in the making and the worker's active
list (``GET /video/automation/drama-requests``) still carries them. This backfill closes them
the way the drop does now: ``status = 'cancelled'``, ``cancelled_at`` the video's own
``dropped_at`` (when the owner actually stopped it) and ``updated_at`` the time of the change.

The request is matched to its video by slug, the join the request list itself uses. Only a
request still ``started`` whose video has a ``dropped_at`` is touched; queued, done and already
cancelled rows, and started rows whose video is still alive or has no row, stay as they are. The
statement matches nothing the second time, so running it again changes nothing, and it is the
same whether production holds zero such rows or many.

The downgrade does nothing: a row cancelled here cannot be told apart from one the drop
cancelled, and putting either back to ``started`` would only restore the bug.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0120_video_dropped_request"
down_revision: str | None = "0119_video_category_anime"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

REQUESTS = "video_drama_requests"
PROJECTS = "video_projects"
BACKFILL = (
    f"UPDATE {REQUESTS} AS r "
    "SET status = 'cancelled', cancelled_at = p.dropped_at, updated_at = now() "
    f"FROM {PROJECTS} AS p "
    "WHERE p.slug = r.slug AND r.status = 'started' AND p.dropped_at IS NOT NULL"
)


def upgrade() -> None:
    op.execute(sa.text(BACKFILL))


def downgrade() -> None:
    # Nothing to undo: a request cancelled here looks the same as one the drop cancelled.
    pass
