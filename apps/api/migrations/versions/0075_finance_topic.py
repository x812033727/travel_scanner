"""The lifestyle vocabulary gains ``finance``.

Revision ID: 0075_finance_topic
Revises: 0074_lifestyle_guides

One row in ``guide_topics``, nothing else. 0074 already built the ``section`` column and
both CHECK constraints, so this revision touches no schema at all -- which is why it needs
none of 0074's ``inspector`` guards and adds no branch for
``tests/test_migration_dead_branches.py`` to account for.

It keeps 0072's seeding contract: only a slug the database does not already hold is
inserted, so a re-run is a no-op and a label an administrator rewrote is never restored.
The labels are spelled out here rather than imported from ``app.guides.taxonomy`` for the
reason 0074 gives -- a migration has to keep running after the application constant moves
on -- but the two must agree today, and
``tests/test_guides_migration.py::test_the_seeded_life_topics_match_the_python_vocabulary``
holds them to it by concatenating this list onto 0074's.

The downgrade is scoped to this one slug. 0074's removes every ``section = 'life'`` seed;
copying that predicate here would make a single-step rollback delete the seven topics 0074
owns, and with them the article links of an entire section that is still published.
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import context, op

revision: str = "0075_finance_topic"
down_revision: str | None = "0074_lifestyle_guides"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALES = ("en", "ja", "ko", "zh-TW", "zh-CN")

# slug, display_order, (en, ja, ko, zh-TW, zh-CN); display_order continues after 0074's 260.
# Named as 0074 names its own list so the vocabulary test can read both the same way.
LIFE_SEED_TOPICS: tuple[tuple[str, int, tuple[str, str, str, str, str]], ...] = (
    (
        "finance",
        270,
        ("Money & finance", "お金・家計", "돈・재테크", "理財與金錢", "理财与金钱"),
    ),
)
SLUGS = tuple(slug for slug, _, _ in LIFE_SEED_TOPICS)
_SLUG_LIST = ", ".join(f"'{slug}'" for slug in SLUGS)
REMOVE_LINKS = (
    "DELETE FROM guide_article_topics WHERE topic_id IN "
    f"(SELECT id FROM guide_topics WHERE slug IN ({_SLUG_LIST}) AND source = 'seed')"
)
REMOVE_TOPICS = f"DELETE FROM guide_topics WHERE slug IN ({_SLUG_LIST}) AND source = 'seed'"


def upgrade() -> None:
    if context.is_offline_mode():
        return
    existing = set(op.get_bind().execute(sa.text("SELECT slug FROM guide_topics")).scalars())
    missing = [entry for entry in LIFE_SEED_TOPICS if entry[0] not in existing]
    if not missing:
        return
    now = datetime.now(UTC)
    op.bulk_insert(
        sa.table(
            "guide_topics",
            sa.column("id", sa.Uuid()),
            sa.column("slug", sa.String()),
            sa.column("names_json", sa.JSON()),
            sa.column("display_order", sa.Integer()),
            sa.column("is_active", sa.Boolean()),
            sa.column("source", sa.String()),
            sa.column("section", sa.String()),
            sa.column("created_at", sa.DateTime(timezone=True)),
            sa.column("updated_at", sa.DateTime(timezone=True)),
        ),
        [
            {
                "id": uuid4(),
                "slug": slug,
                "names_json": dict(zip(LOCALES, labels, strict=True)),
                "display_order": order,
                "is_active": True,
                "source": "seed",
                "section": "life",
                "created_at": now,
                "updated_at": now,
            }
            for slug, order, labels in missing
        ],
    )


def downgrade() -> None:
    # The links first: SQLite without ``PRAGMA foreign_keys=ON`` does not cascade, and a
    # topic row removed from under its links leaves rows pointing at nothing.
    if context.is_offline_mode():
        op.execute(REMOVE_LINKS)
        op.execute(REMOVE_TOPICS)
        return
    tables = set(sa.inspect(op.get_bind()).get_table_names())
    if "guide_topics" not in tables:
        return
    if "guide_article_topics" in tables:
        op.execute(REMOVE_LINKS)
    op.execute(REMOVE_TOPICS)
