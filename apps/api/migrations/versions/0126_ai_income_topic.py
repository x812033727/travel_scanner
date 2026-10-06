"""The lifestyle vocabulary gains ``ai-income`` under ``ai``: earning with AI.

Revision ID: 0126_ai_income_topic
Revises: 0125_news_review_judge

Seeding only, on 0080's contract: only a slug the database does not already hold is
inserted, so a re-run is a no-op and a label an administrator rewrote is never restored; the
hub lead is written only where ``descriptions_json`` is still NULL. A parent an administrator
removed seeds the sub-topic at the top level instead of skipping it, as 0076 and 0080 do.

The labels are spelled out rather than imported from ``app.guides.taxonomy`` for the reason
0074 through 0080 give, and
``tests/test_guides_migration.py::test_the_seeded_sub_topics_match_the_python_vocabulary``
holds the two to agreement. display_order 560 continues after 0080's 550.

The downgrade removes only this slug's seeded row and its article links, links first.
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.engine import Connection

revision: str = "0126_ai_income_topic"
down_revision: str | None = "0125_news_review_judge"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALES = ("en", "ja", "ko", "zh-TW", "zh-CN")

Labels = tuple[str, str, str, str, str]

# Named as 0076 and 0080 name theirs so tests/test_guides_migration.py reads them alike.
LIFE_SEED_TOPICS: tuple[tuple[str, int, Labels], ...] = ()

LIFE_SEED_SUBTOPICS: tuple[tuple[str, str, int, Labels], ...] = (
    (
        "ai-income",
        "ai",
        560,
        ("Earning with AI", "AIで稼ぐ", "AI로 수익 내기", "AI 賺錢與副業", "AI 赚钱与副业"),
    ),
)

TOPIC_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "ai-income": {
        "zh-TW": "用 AI 接案、賣數位商品與經營副業：平台規則、報價、責任與成本，不保證收入。"
    },
}

SLUGS = tuple(slug for slug, _, _, _ in LIFE_SEED_SUBTOPICS)
_SLUG_LIST = ", ".join(f"'{slug}'" for slug in SLUGS)
REMOVE_LINKS = (
    "DELETE FROM guide_article_topics WHERE topic_id IN "
    f"(SELECT id FROM guide_topics WHERE slug IN ({_SLUG_LIST}) AND source = 'seed')"
)
REMOVE_TOPICS = f"DELETE FROM guide_topics WHERE slug IN ({_SLUG_LIST}) AND source = 'seed'"

topics = sa.table(
    "guide_topics",
    sa.column("id", sa.Uuid()),
    sa.column("slug", sa.String()),
    sa.column("names_json", sa.JSON()),
    sa.column("display_order", sa.Integer()),
    sa.column("is_active", sa.Boolean()),
    sa.column("source", sa.String()),
    sa.column("section", sa.String()),
    sa.column("parent_id", sa.Uuid()),
    sa.column("descriptions_json", sa.JSON()),
    sa.column("created_at", sa.DateTime(timezone=True)),
    sa.column("updated_at", sa.DateTime(timezone=True)),
)


def _ids_by_slug(bind: Connection) -> dict[str, object]:
    return {row.slug: row.id for row in bind.execute(sa.select(topics.c.id, topics.c.slug))}


def upgrade() -> None:
    if context.is_offline_mode():
        return
    bind = op.get_bind()
    now = datetime.now(UTC)
    existing = _ids_by_slug(bind)
    children = [
        {
            "id": uuid4(),
            "slug": slug,
            "names_json": dict(zip(LOCALES, labels, strict=True)),
            "display_order": order,
            "is_active": True,
            "source": "seed",
            "section": "life",
            "parent_id": existing.get(parent),
            "created_at": now,
            "updated_at": now,
        }
        for slug, parent, order, labels in LIFE_SEED_SUBTOPICS
        if slug not in existing
    ]
    if children:
        op.bulk_insert(topics, children)
    for slug, descriptions in TOPIC_DESCRIPTIONS.items():
        bind.execute(
            sa.update(topics)
            .where(
                topics.c.slug == slug,
                sa.or_(
                    topics.c.descriptions_json.is_(None),
                    sa.cast(topics.c.descriptions_json, sa.Text) == "null",
                ),
            )
            .values(descriptions_json=descriptions)
        )


def downgrade() -> None:
    if context.is_offline_mode():
        op.execute(REMOVE_LINKS)
        op.execute(REMOVE_TOPICS)
        return
    bind = op.get_bind()
    tables = set(sa.inspect(bind).get_table_names())
    if "guide_topics" not in tables:
        return
    if "guide_article_topics" in tables:
        bind.execute(sa.text(REMOVE_LINKS))
    bind.execute(sa.text(REMOVE_TOPICS))
