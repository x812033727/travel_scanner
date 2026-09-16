"""Two news verticals join the lifestyle vocabulary: ``tech`` with ``tech-news``, and ``crypto``.

Revision ID: 0080_crypto_and_tech_topics
Revises: 0079_guide_news_date

Seeding only. 0076 built ``parent_id`` and ``descriptions_json`` and 0074 built ``section``
and both CHECK constraints, so this revision touches no schema at all -- which is why, like
0075, it needs none of 0076's ``inspector`` guards and adds no branch for
``tests/test_migration_dead_branches.py`` to account for.

``crypto`` hangs under ``finance`` rather than becoming a vertical of its own. It is the same
YMYL subject under the same review standard: one disclaimer rule (``pack_ingest``'s
``finance_no_disclaimer``), one hub lead that already promises 「只講制度與方法，不推薦商品」,
and the six crypto explainers ``docs/life-finance-series.md`` plans are filed under ``finance``
already. A second top-level crypto tree would need a duplicate of all of it.

``tech`` has to be a new parent, because there is nowhere to put it. ``gadgets`` is 3C devices
and ``software`` is apps; chips, telecoms and platform regulation are neither, and
``docs/article-architecture.md`` records the decision that those five stay single-level.

This started life as ``0079`` and was renumbered: ``0079_guide_news_date`` (PR #537) also
revised 0078, and two revisions off one parent give ``alembic upgrade head`` two heads.
#537 merged first, so this one re-chains onto it and takes the next number -- exactly what
that migration's own docstring says the second-merged branch must do. Nothing else changed;
this revision still touches no schema and seeds the same three slugs.

It keeps 0072's seeding contract: only a slug the database does not already hold is inserted,
so a re-run is a no-op and a label an administrator rewrote is never restored. The hub lead is
written only where ``descriptions_json`` is still NULL, for the same reason. The labels are
spelled out here rather than imported from ``app.guides.taxonomy`` for the reason 0074, 0075
and 0076 all give -- a migration has to keep running after the application constant moves on --
but the two must agree today, and
``tests/test_guides_migration.py::test_the_seeded_sub_topics_match_the_python_vocabulary``
holds them to it.

The downgrade is scoped to these three slugs, links first (SQLite without
``PRAGMA foreign_keys`` does not cascade). It never copies 0074's ``section = 'life'``
predicate: a one-step rollback that deleted ``ai`` would take the article links of an entire
published section with it.
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.engine import Connection

revision: str = "0080_crypto_and_tech_topics"
down_revision: str | None = "0079_guide_news_date"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALES = ("en", "ja", "ko", "zh-TW", "zh-CN")

Labels = tuple[str, str, str, str, str]

# slug, display_order, (en, ja, ko, zh-TW, zh-CN); display_order continues after 0076's 520.
# Named as 0074, 0075 and 0076 name theirs so tests/test_guides_migration.py reads them alike.
LIFE_SEED_TOPICS: tuple[tuple[str, int, Labels], ...] = (
    (
        "tech",
        530,
        ("Tech & industry", "テクノロジー・業界", "테크·산업", "科技與產業", "科技与产业"),
    ),
)

# slug, parent slug, display_order, labels.
LIFE_SEED_SUBTOPICS: tuple[tuple[str, str, int, Labels], ...] = (
    (
        "tech-news",
        "tech",
        540,
        ("Tech news", "テックニュース", "테크 뉴스", "科技新聞", "科技新闻"),
    ),
    (
        "crypto",
        "finance",
        550,
        (
            "Crypto & blockchain",
            "暗号資産・ブロックチェーン",
            "가상자산·블록체인",
            "加密貨幣與區塊鏈",
            "加密货币与区块链",
        ),
    ),
)

TOPIC_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "tech": {
        "zh-TW": "晶片、裝置、平台與電信的產業消息：只記錄查證過的事實與日期，不做推薦。",
        "en": (
            "Chips, devices, platforms and telecoms: verified facts and dates, "
            "never a recommendation."
        ),
    },
    "tech-news": {
        "zh-TW": "非 AI 的科技與產業消息：發布、法規、資安事件與服務變動，附官方來源與查核日。"
    },
    "crypto": {
        "zh-TW": (
            "加密貨幣與區塊鏈的法規、技術與產業動態。只講制度與運作方式，不寫價格、漲跌或買賣時機。"
        )
    },
}

SLUGS = tuple(slug for slug, _, _ in LIFE_SEED_TOPICS) + tuple(
    slug for slug, _, _, _ in LIFE_SEED_SUBTOPICS
)
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


def _row(
    slug: str, order: int, labels: Labels, parent_id: object | None, now: datetime
) -> dict[str, object]:
    return {
        "id": uuid4(),
        "slug": slug,
        "names_json": dict(zip(LOCALES, labels, strict=True)),
        "display_order": order,
        "is_active": True,
        "source": "seed",
        "section": "life",
        "parent_id": parent_id,
        # Absent rather than None where there is nothing to say: SQLAlchemy would store a
        # Python None as the JSON text ``null``, which ``IS NULL`` never matches.
        **({"descriptions_json": TOPIC_DESCRIPTIONS[slug]} if slug in TOPIC_DESCRIPTIONS else {}),
        "created_at": now,
        "updated_at": now,
    }


def _ids_by_slug(bind: Connection) -> dict[str, object]:
    return {row.slug: row.id for row in bind.execute(sa.select(topics.c.id, topics.c.slug))}


def upgrade() -> None:
    if context.is_offline_mode():
        return
    bind = op.get_bind()
    now = datetime.now(UTC)
    existing = _ids_by_slug(bind)
    parents = [
        _row(slug, order, labels, None, now)
        for slug, order, labels in LIFE_SEED_TOPICS
        if slug not in existing
    ]
    if parents:
        op.bulk_insert(topics, parents)
        existing = _ids_by_slug(bind)
    # A sub-topic whose parent an administrator removed is seeded at the top level rather
    # than skipped, exactly as 0076 does: the vocabulary is still complete, it is just flat
    # there. ``crypto``'s parent ``finance`` comes from 0075, ``tech-news``'s from above.
    children = [
        _row(slug, order, labels, existing.get(parent), now)
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
