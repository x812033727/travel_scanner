"""Let the event vocabulary live in Python, not in a database CHECK.

Revision ID: 0055_analytics_event_names
Revises: 0054_catalog_review

``analytics_events.event_name`` was pinned by ``ck_analytics_event_name``, a CHECK
listing the five names the browser could send. Every new event therefore needed a
migration before it could be recorded at all, which is why the backend has never sent
one. The names are now validated in ``app.analytics.service.EVENT_NAMES`` (and, for
what a browser may claim, ``app.analytics.schemas.EventName``), so the constraint only
adds a deploy-ordering trap: the API would start writing names the database rejects
before the migration reaches it.

Dropping a constraint is not the usual "add a column" shape, so both directions are
guarded by what the database actually has. ``0001_initial`` builds from the current
models, where the constraint is gone, so a fresh database has nothing to drop; a
database upgrading from 0054 does. The downgrade re-adds the constraint only when
every stored name is one the old CHECK allowed — re-adding it over rows written by
the new code would fail the whole downgrade, and silently deleting a member's history
to make a rollback fit is worse than leaving the constraint off.
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0055_analytics_event_names"
down_revision: str | None = "0054_catalog_review"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

TABLE = "analytics_events"
CONSTRAINT = "ck_analytics_event_name"
LEGACY_NAMES = (
    "page_view",
    "registration_completed",
    "search_completed",
    "trip_created",
    "outbound_click",
)


def _offline() -> bool:
    return bool(op.get_context().as_sql)


def _has_constraint() -> bool:
    if _offline():
        return True
    inspector = sa.inspect(op.get_bind())
    if TABLE not in inspector.get_table_names():
        return False
    return any(
        check["name"] == CONSTRAINT for check in inspector.get_check_constraints(TABLE)
    )


def upgrade() -> None:
    if _has_constraint():
        op.drop_constraint(CONSTRAINT, TABLE, type_="check")


def downgrade() -> None:
    if _offline():
        op.create_check_constraint(
            CONSTRAINT,
            TABLE,
            "event_name IN (" + ", ".join(f"'{name}'" for name in LEGACY_NAMES) + ")",
        )
        return
    if _has_constraint():
        return
    bind = op.get_bind()
    if TABLE not in sa.inspect(bind).get_table_names():
        return
    unsupported = bind.scalar(
        sa.text(
            f"SELECT count(*) FROM {TABLE} WHERE event_name <> ALL(:names)"  # noqa: S608
        ).bindparams(sa.bindparam("names", list(LEGACY_NAMES))),
    )
    if unsupported:
        return
    op.create_check_constraint(
        CONSTRAINT,
        TABLE,
        "event_name IN (" + ", ".join(f"'{name}'" for name in LEGACY_NAMES) + ")",
    )
