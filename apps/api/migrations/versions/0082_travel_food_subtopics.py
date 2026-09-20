"""The travel vocabulary gains its first sub-topics: one per dish under ``food``, and ``cafe``.

Revision ID: 0082_travel_food_subtopics
Revises: 0081_affiliate_click_article

Seeding only. 0076 built ``parent_id`` and ``descriptions_json`` and 0074 built ``section``
and both CHECK constraints, so this revision touches no schema at all -- which is why, like
0075 and 0080, it needs none of 0076's ``inspector`` guards and adds no branch for
``tests/test_migration_dead_branches.py`` to account for.

Until now the travel vocabulary was one level deep, because its second axis is the
destination. A food special is written one dish and one city at a time, and the destination
axis cannot gather the same dish across cities; a sub-topic per dish can. Every row here is
a child of ``food``, which 0072 seeded, and every row is ``section = 'travel'``: the two
lifestyle seeding revisions this one is modelled on write ``'life'``, and copying that would
file a dish where ``_resolve_topics`` refuses it on every travel article.

It keeps 0072's seeding contract: only a slug the database does not already hold is inserted,
so a re-run is a no-op and a label an administrator rewrote is never restored. The hub lead is
written only where ``descriptions_json`` is still NULL, for the same reason, and only for this
revision's own rows -- ``food`` itself is left exactly as it was, so the rollback is exact.
The labels are spelled out here rather than imported from ``app.guides.taxonomy`` for the
reason 0074, 0075, 0076 and 0080 all give -- a migration has to keep running after the
application constant moves on -- but the two must agree today, and
``tests/test_guides_migration.py::test_the_seeded_travel_sub_topics_match_the_python_vocabulary``
holds them to it.

If another revision takes 0082 first, this one re-chains onto it and takes the next number,
exactly as 0080 did; ``TRAVEL_SUBTOPIC_MIGRATIONS`` in that test file is the one name to change.

The downgrade is scoped to these slugs, links first (SQLite without ``PRAGMA foreign_keys``
does not cascade). An article that carried only a dish sub-topic is left with no topic by it,
which is what a rollback of the vocabulary means; re-importing the pack after an upgrade
restores the link.
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.engine import Connection

revision: str = "0082_travel_food_subtopics"
down_revision: str | None = "0081_affiliate_click_article"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALES = ("en", "ja", "ko", "zh-TW", "zh-CN")

Labels = tuple[str, str, str, str, str]

# slug, parent slug, display_order, labels. A band of its own, above the travel parents
# (10-190) and the lifestyle rows (200-550): one display_order column sorts every row.
TRAVEL_SEED_SUBTOPICS: tuple[tuple[str, str, int, Labels], ...] = (
    ("cafe", "food", 1000, ("Cafes", "カフェ", "카페", "咖啡店", "咖啡厅")),
    (
        "kr-dwaeji-gukbap",
        "food",
        1010,
        ("Dwaeji-gukbap", "テジクッパ", "돼지국밥", "豬肉湯飯", "猪肉汤饭"),
    ),
    ("kr-naengmyeon", "food", 1020, ("Naengmyeon", "韓国冷麺", "냉면", "韓式冷麵", "韩国冷面")),
    ("kr-samgyetang", "food", 1030, ("Samgyetang", "サムゲタン", "삼계탕", "蔘雞湯", "参鸡汤")),
    (
        "kr-beef-bone-soup",
        "food",
        1040,
        (
            "Seolleongtang & Gomtang",
            "ソルロンタン・コムタン",
            "설렁탕·곰탕",
            "雪濃湯・牛骨湯",
            "雪浓汤・牛骨汤",
        ),
    ),
    (
        "kr-dak-hanmari",
        "food",
        1050,
        ("Dak-hanmari", "タッカンマリ", "닭한마리", "一隻雞", "一只鸡"),
    ),
    ("kr-kalguksu", "food", 1060, ("Kalguksu", "カルグクス", "칼국수", "刀切麵", "刀切面")),
    ("kr-jokbal", "food", 1070, ("Jokbal", "チョッパル", "족발", "韓式豬腳", "韩式猪蹄")),
    ("kr-tteokbokki", "food", 1080, ("Tteokbokki", "トッポッキ", "떡볶이", "辣炒年糕", "辣炒年糕")),
    ("kr-heukdwaeji", "food", 1090, ("Jeju black pork", "済州黒豚", "흑돼지", "黑豬肉", "黑猪肉")),
    (
        "kr-gogi-guksu",
        "food",
        1100,
        ("Gogi-guksu", "コギグクス", "고기국수", "豬肉湯麵", "猪肉汤面"),
    ),
    ("kr-jjim-galbi", "food", 1110, ("Jjim-galbi", "チムカルビ", "찜갈비", "辣燉排骨", "辣炖排骨")),
    ("kr-makchang", "food", 1120, ("Makchang", "マクチャン", "막창", "烤腸", "烤肠")),
    (
        "kr-ganjang-gejang",
        "food",
        1130,
        ("Ganjang-gejang", "カンジャンケジャン", "간장게장", "醬蟹", "酱蟹"),
    ),
    ("kr-bibimbap", "food", 1140, ("Bibimbap", "ビビンバ", "비빔밥", "韓式拌飯", "韩式拌饭")),
)

TOPIC_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "cafe": {
        "zh-TW": (
            "一個街區寫一篇的咖啡店特輯：這一區怎麼逛、每家店是哪一種店，"
            "逐店附入選依據的官方來源與查核日期。"
        )
    },
    "kr-dwaeji-gukbap": {
        "zh-TW": (
            "釜山的日常湯飯，首爾也吃得到：依城市分篇，寫菜單怎麼看、桌上的佐料怎麼加，"
            "以及有官方來源點名的店家。"
        )
    },
    "kr-naengmyeon": {
        "zh-TW": (
            "首爾的平壤冷麵與咸興冷麵、釜山的小麥冷麵（밀면）：依城市分篇，"
            "寫各自的吃法與有官方來源點名的店家。"
        )
    },
    "kr-samgyetang": {
        "zh-TW": ("一人一鍋的蔘雞湯（삼계탕）：怎麼點、怎麼吃，以及各城市有官方來源點名的店家。")
    },
    "kr-beef-bone-soup": {
        "zh-TW": (
            "雪濃湯（설렁탕）與牛骨湯（곰탕）：兩種牛湯的差別、在桌上自己調味的吃法，"
            "以及各城市有官方來源點名的店家。"
        )
    },
    "kr-dak-hanmari": {
        "zh-TW": (
            "整隻雞下鍋的一隻雞（닭한마리）：怎麼點、怎麼吃，以及各城市有官方來源點名的店家。"
        )
    },
    "kr-kalguksu": {
        "zh-TW": (
            "現切麵條的韓式湯麵刀切麵（칼국수）：怎麼點、配什麼，以及各城市有官方來源點名的店家。"
        )
    },
    "kr-jokbal": {
        "zh-TW": ("韓式豬腳（족발）：份量怎麼選、怎麼包著吃，依城市分篇，附有官方來源點名的店家。")
    },
    "kr-tteokbokki": {
        "zh-TW": (
            "辣炒年糕（떡볶이）：從市場小攤到桌邊現煮的年糕鍋，依城市分篇，附有官方來源點名的店家。"
        )
    },
    "kr-heukdwaeji": {
        "zh-TW": ("濟州的黑豬肉（흑돼지）燒烤：部位怎麼選、怎麼吃，以及有官方來源點名的店家。")
    },
    "kr-gogi-guksu": {
        "zh-TW": ("濟州的豬肉湯麵（고기국수）：怎麼點、怎麼吃，以及有官方來源點名的店家。")
    },
    "kr-jjim-galbi": {
        "zh-TW": ("大邱東仁洞的辣燉排骨（찜갈비）：怎麼點、怎麼吃，以及有官方來源點名的店家。")
    },
    "kr-makchang": {"zh-TW": "大邱的烤腸（막창）：怎麼點、怎麼吃，以及有官方來源點名的店家。"},
    "kr-ganjang-gejang": {
        "zh-TW": ("醬油醃生蟹的醬蟹（간장게장）：怎麼點、怎麼吃，以及各城市有官方來源點名的店家。")
    },
    "kr-bibimbap": {
        "zh-TW": (
            "韓式拌飯（비빔밥）：全州拌飯與各城市的版本，怎麼點、怎麼拌，附有官方來源點名的店家。"
        )
    },
}

SLUGS = tuple(slug for slug, _, _, _ in TRAVEL_SEED_SUBTOPICS)
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
        "section": "travel",
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
    # A sub-topic whose parent an administrator removed is seeded at the top level rather
    # than skipped, exactly as 0076 and 0080 do: the vocabulary is still complete, it is
    # just flat there.
    children = [
        _row(slug, order, labels, existing.get(parent), now)
        for slug, parent, order, labels in TRAVEL_SEED_SUBTOPICS
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
