"""The owner's requests to make a skipped dub track again (docs/videos/DUBS.md §再做一次).

Revision ID: 0131_video_dub_retries
Revises: 0130_video_cute_presets

A dub the worker gave up on (a line that does not fit its window, a line Jev still hears wrong)
reads "skipped" on the language panel for good: its state comes from the languages batches, and
the worker passes over a locale it gave up. The owner can now ask for one again from the panel.
``video_projects.dub_retries`` holds that request, one record per locale and only the latest:
{"ja": {"id": "<uuid>", "status": "requested", "requested_at": "...", "requested_by": "...",
"replaced_reason": "...", "estimated_characters": 6120, "taken_at": null, "finished_at": null,
"reason": null}}. ``status`` is requested, taken, made, skipped or refused; "expired" is read
from ``requested_at`` and never stored. The worker reads the request on its list row and answers
in its report; app/video_reviews/dub_retry.py owns the transitions.

The column is json, not jsonb, like ``locales`` (0106), and nothing here applies an operator to
it. Additive, with a server default, so the previous release keeps running against it and no
row is rewritten. 0001 builds a fresh database from the current models, so the column is added
only when missing.

The downgrade drops the column, and with it every request: one still waiting or taken is lost,
and a dub the worker already cleared the skip for is then made and sent as any other dub.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0131_video_dub_retries"
down_revision: str | None = "0130_video_cute_presets"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "video_projects"
COLUMN = "dub_retries"


def _columns() -> set[str]:
    return (
        set()
        if op.get_context().as_sql
        else {column["name"] for column in sa.inspect(op.get_bind()).get_columns(TABLE)}
    )


def upgrade() -> None:
    if COLUMN not in _columns():
        op.add_column(
            TABLE,
            sa.Column(COLUMN, sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        )


def downgrade() -> None:
    if op.get_context().as_sql or COLUMN in _columns():
        op.drop_column(TABLE, COLUMN)
