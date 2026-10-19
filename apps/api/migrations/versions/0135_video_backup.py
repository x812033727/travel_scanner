"""Each uploaded video's copy in the owner's Google Drive (docs/videos/BACKUP.md).

Revision ID: 0135_video_backup
Revises: 0133_story_followon_budget

``video_projects.backup`` is what the video worker last reported about copying the video's files
to ``AI/備份/<series>/<episode>/``: {"state": "done", "folder": "奇聞檔案局/curio-h01",
"tier": "basic", "bytes": 535000000, "files": 14, "files_hash": "<sha256>", "at": "...",
"checked_at": "...", "attempts": 0, "error": null, "missing": [], "contents": {...}}. ``state``
is pending, done, failed, blocked_quota or partial; null means the worker never queued it.
app/video_backup/admin_status.py owns the transitions, and the worker's tidy keeps a video's files on
the host until it reads done.

The number skips 0134, which the story pilot's next migration has planned since 2026-10-19
(tasks/open/2026-09-28-video-story-pilot.md); this revision follows the head on main, 0133.

The column is json, not jsonb, like ``locales`` (0106), and nothing here applies an operator to
it. Additive and nullable, so the previous release keeps running against it and no row is
rewritten. 0001 builds a fresh database from the current models, so the column is added only
when missing. The downgrade drops the column and every backup record with it; the files in
Drive stay, each with its own backup.json.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0135_video_backup"
down_revision: str | None = "0133_story_followon_budget"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_projects"
COLUMN = "backup"


def _columns() -> set[str]:
    return (
        set()
        if op.get_context().as_sql
        else {column["name"] for column in sa.inspect(op.get_bind()).get_columns(TABLE)}
    )


def upgrade() -> None:
    if COLUMN not in _columns():
        op.add_column(TABLE, sa.Column(COLUMN, sa.JSON(), nullable=True))


def downgrade() -> None:
    if op.get_context().as_sql or COLUMN in _columns():
        op.drop_column(TABLE, COLUMN)
