"""One-shot retry requests for blocked videos.

Revision ID: 0104_video_retry_request
Revises: 0103_video_binge_series

The site records a request UUID and the UUID the worker last acknowledged. A retry is pending
only while they differ. Both are nullable so older projects and workers continue to work.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0104_video_retry_request"
down_revision: str | None = "0103_video_binge_series"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_projects"
COLUMNS = ("retry_request_id", "retry_acknowledged_id")


def _columns() -> set[str]:
    return (
        set()
        if op.get_context().as_sql
        else {column["name"] for column in sa.inspect(op.get_bind()).get_columns(TABLE)}
    )


def upgrade() -> None:
    existing = _columns()
    for name in COLUMNS:
        if name not in existing:
            op.add_column(TABLE, sa.Column(name, sa.Uuid(), nullable=True))


def downgrade() -> None:
    existing = _columns()
    for name in reversed(COLUMNS):
        if name in existing or op.get_context().as_sql:
            op.drop_column(TABLE, name)
