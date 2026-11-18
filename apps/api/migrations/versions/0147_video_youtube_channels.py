"""More than one linked YouTube channel (video_youtube_connections.key, video_projects).

Revision ID: 0147_video_youtube_channels
Revises: 0146_deployment_host_status

docs/videos/YOUTUBE-REPORTS.md §頻道. The site linked exactly one channel: the connection and
the report state were single rows (CHECK id = 1). The owner now runs two channels, so:

- video_youtube_connections loses its single-row check and gains ``key`` (unique; row 1 becomes
  ``default``) and ``label``. Row 1 keeps the OAuth client every channel signs in with.
- video_projects gains ``youtube_channel_key``: which channel a video goes to. Null is the
  default channel, so no video needs a backfill.
- video_youtube_report_state loses its single-row check and gains ``channel_id`` (unique), one
  row per channel; row 1 is stamped with the channel linked today.

Everything is additive: the code from before reads id = 1 and never sees the new rows.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0147_video_youtube_channels"
down_revision: str | None = "0146_deployment_host_status"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

CONNECTIONS = "video_youtube_connections"
PROJECTS = "video_projects"
STATE = "video_youtube_report_state"
CONNECTION_CHECK = "ck_video_youtube_connection_single"
STATE_CHECK = "ck_video_youtube_report_state_single"
KEY_UNIQUE = "uq_video_youtube_connections_key"
STATE_CHANNEL_UNIQUE = "uq_video_youtube_report_state_channel_id"


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _columns(inspector: sa.Inspector, table: str) -> set[str]:
    return {column["name"] for column in inspector.get_columns(table)}


def _checks(inspector: sa.Inspector, table: str) -> set[str]:
    return {str(check["name"]) for check in inspector.get_check_constraints(table)}


def _uniques(inspector: sa.Inspector, table: str) -> set[str]:
    return {str(unique["name"]) for unique in inspector.get_unique_constraints(table)}


def _key_column() -> sa.Column[str]:
    return sa.Column("key", sa.String(32), nullable=False, server_default=sa.text("'default'"))


def _bump_sequence(table: str) -> None:
    """Rows were written with an explicit id = 1, so a serial sequence behind the id was never
    advanced; move it past the rows so a new row gets a free id."""
    op.execute(
        sa.text(
            f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
            f"COALESCE((SELECT MAX(id) FROM {table}), 1)) "
            f"WHERE pg_get_serial_sequence('{table}', 'id') IS NOT NULL"
        )
    )


def _stamp_state_channel() -> None:
    op.execute(
        sa.text(
            f"UPDATE {STATE} SET channel_id = ("
            f"SELECT channel_id FROM {CONNECTIONS} WHERE id = 1) "
            f"WHERE id = 1 AND channel_id IS NULL"
        )
    )


def upgrade() -> None:
    if _offline():
        op.drop_constraint(CONNECTION_CHECK, CONNECTIONS, type_="check")
        op.add_column(CONNECTIONS, _key_column())
        op.add_column(CONNECTIONS, sa.Column("label", sa.String(80), nullable=True))
        op.create_unique_constraint(KEY_UNIQUE, CONNECTIONS, ["key"])
        op.add_column(PROJECTS, sa.Column("youtube_channel_key", sa.String(32), nullable=True))
        op.drop_constraint(STATE_CHECK, STATE, type_="check")
        op.add_column(STATE, sa.Column("channel_id", sa.String(64), nullable=True))
        op.create_unique_constraint(STATE_CHANNEL_UNIQUE, STATE, ["channel_id"])
        _stamp_state_channel()
        _bump_sequence(CONNECTIONS)
        _bump_sequence(STATE)
        return
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if CONNECTION_CHECK in _checks(inspector, CONNECTIONS):
        op.drop_constraint(CONNECTION_CHECK, CONNECTIONS, type_="check")
    connection_columns = _columns(inspector, CONNECTIONS)
    if "key" not in connection_columns:
        op.add_column(CONNECTIONS, _key_column())
    if "label" not in connection_columns:
        op.add_column(CONNECTIONS, sa.Column("label", sa.String(80), nullable=True))
    if KEY_UNIQUE not in _uniques(sa.inspect(bind), CONNECTIONS):
        op.create_unique_constraint(KEY_UNIQUE, CONNECTIONS, ["key"])
    if "youtube_channel_key" not in _columns(inspector, PROJECTS):
        op.add_column(PROJECTS, sa.Column("youtube_channel_key", sa.String(32), nullable=True))
    if inspector.has_table(STATE):
        if STATE_CHECK in _checks(inspector, STATE):
            op.drop_constraint(STATE_CHECK, STATE, type_="check")
        if "channel_id" not in _columns(inspector, STATE):
            op.add_column(STATE, sa.Column("channel_id", sa.String(64), nullable=True))
        if STATE_CHANNEL_UNIQUE not in _uniques(sa.inspect(bind), STATE):
            op.create_unique_constraint(STATE_CHANNEL_UNIQUE, STATE, ["channel_id"])
        _stamp_state_channel()
    if bind.dialect.name == "postgresql":
        _bump_sequence(CONNECTIONS)
        if inspector.has_table(STATE):
            _bump_sequence(STATE)


def downgrade() -> None:
    """Back to one channel: every row but the default one goes, with the grants it held."""
    if _offline():
        op.drop_constraint(STATE_CHANNEL_UNIQUE, STATE, type_="unique")
        op.drop_column(STATE, "channel_id")
        op.execute(sa.text(f"DELETE FROM {STATE} WHERE id <> 1"))
        op.create_check_constraint(STATE_CHECK, STATE, "id = 1")
        op.drop_column(PROJECTS, "youtube_channel_key")
        op.drop_constraint(KEY_UNIQUE, CONNECTIONS, type_="unique")
        op.drop_column(CONNECTIONS, "label")
        op.drop_column(CONNECTIONS, "key")
        op.execute(sa.text(f"DELETE FROM {CONNECTIONS} WHERE id <> 1"))
        op.create_check_constraint(CONNECTION_CHECK, CONNECTIONS, "id = 1")
        return
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if inspector.has_table(STATE):
        if STATE_CHANNEL_UNIQUE in _uniques(inspector, STATE):
            op.drop_constraint(STATE_CHANNEL_UNIQUE, STATE, type_="unique")
        if "channel_id" in _columns(inspector, STATE):
            op.drop_column(STATE, "channel_id")
        op.execute(sa.text(f"DELETE FROM {STATE} WHERE id <> 1"))
        if STATE_CHECK not in _checks(sa.inspect(bind), STATE):
            op.create_check_constraint(STATE_CHECK, STATE, "id = 1")
    if "youtube_channel_key" in _columns(inspector, PROJECTS):
        op.drop_column(PROJECTS, "youtube_channel_key")
    if KEY_UNIQUE in _uniques(inspector, CONNECTIONS):
        op.drop_constraint(KEY_UNIQUE, CONNECTIONS, type_="unique")
    connection_columns = _columns(inspector, CONNECTIONS)
    if "label" in connection_columns:
        op.drop_column(CONNECTIONS, "label")
    if "key" in connection_columns:
        op.drop_column(CONNECTIONS, "key")
    op.execute(sa.text(f"DELETE FROM {CONNECTIONS} WHERE id <> 1"))
    if CONNECTION_CHECK not in _checks(sa.inspect(bind), CONNECTIONS):
        op.create_check_constraint(CONNECTION_CHECK, CONNECTIONS, "id = 1")
