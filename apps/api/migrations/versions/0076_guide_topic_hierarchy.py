"""Two-level topics: a parent per sub-topic, a lead paragraph per topic hub.

Revision ID: 0076_guide_topic_hierarchy
Revises: 0075_finance_topic

``guide_topics`` gains ``parent_id`` (a nullable self reference, SET NULL on delete) and
``descriptions_json`` (one hub lead per locale). Both are plain nullable columns, so the
release before this one keeps running against them, and both are guarded the way 0074
guards ``section``: ``0001_initial`` builds from the current models, so a fresh database
already has them, while one upgrading from 0075 has neither.

The seed then follows 0072's contract twice over. Two new parents (``website``,
``marketing``) and twenty-three sub-topics are inserted only where the slug is absent, so
a re-run writes nothing and a label an administrator rewrote is never restored. The hub
lead is written only where ``descriptions_json`` is still NULL, for the same reason: an
editor's paragraph outranks the seed's.

The downgrade takes back exactly this revision's rows (their article links first, since
SQLite without ``PRAGMA foreign_keys`` does not cascade) and drops the two columns. It
never touches 0074's or 0075's vocabulary; a one-step rollback that deleted ``ai`` would
take the links of an entire published section with it.
"""

from collections.abc import Sequence
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from alembic import context, op
from sqlalchemy.engine import Connection

revision: str = "0076_guide_topic_hierarchy"
down_revision: str | None = "0075_finance_topic"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

LOCALES = ("en", "ja", "ko", "zh-TW", "zh-CN")
PARENT_FK = "fk_guide_topics_parent_id"
PARENT_INDEX = "ix_guide_topics_parent_id"

Labels = tuple[str, str, str, str, str]

# slug, display_order, (en, ja, ko, zh-TW, zh-CN); display_order continues after 0075's 270.
# Named as 0074 and 0075 name theirs so tests/test_guides_migration.py reads all three alike.
LIFE_SEED_TOPICS: tuple[tuple[str, int, Labels], ...] = (
    (
        "website",
        280,
        (
            "Websites & e-commerce",
            "サイト構築・EC",
            "웹사이트·이커머스",
            "架站與電商",
            "建站与电商",
        ),
    ),
    (
        "marketing",
        290,
        ("Marketing & SEO", "マーケティング・SEO", "마케팅·SEO", "行銷與 SEO", "营销与 SEO"),
    ),
)

# slug, parent slug, display_order, labels. Orders continue after the parents' 290 so the
# whole lifestyle vocabulary still sorts on one column.
LIFE_SEED_SUBTOPICS: tuple[tuple[str, str, int, Labels], ...] = (
    (
        "ai-terms",
        "ai",
        300,
        ("AI glossary", "AI用語解説", "AI 용어 해설", "AI 名詞解釋", "AI 名词解释"),
    ),
    ("ai-news", "ai", 310, ("AI news", "AIニュース", "AI 뉴스", "AI 新聞與趨勢", "AI 新闻与趋势")),
    (
        "ai-search",
        "ai",
        320,
        ("AI search & GEO", "AI検索とGEO", "AI 검색과 GEO", "AI 搜尋與 GEO", "AI 搜索与 GEO"),
    ),
    (
        "ai-chat",
        "ai",
        330,
        ("AI assistants", "AIアシスタント", "AI 어시스턴트", "對話助理", "对话助理"),
    ),
    ("claude-code", "ai", 340, ("Claude Code",) * 5),
    ("codex", "ai", 350, ("Codex",) * 5),
    (
        "gemini-dev",
        "ai",
        360,
        (
            "Gemini CLI & API",
            "Gemini CLI・API",
            "Gemini CLI·API",
            "Gemini CLI 與 API",
            "Gemini CLI 与 API",
        ),
    ),
    (
        "ai-coding",
        "ai",
        370,
        (
            "AI coding & local models",
            "AIコーディング・ローカルLLM",
            "AI 코딩·로컬 모델",
            "AI 寫程式與本機模型",
            "AI 编程与本地模型",
        ),
    ),
    (
        "ai-create",
        "ai",
        380,
        (
            "AI images, video & audio",
            "AI画像・動画・音声",
            "AI 이미지·영상·음성",
            "AI 圖片、影片與聲音",
            "AI 图片、视频与声音",
        ),
    ),
    (
        "ai-work",
        "ai",
        390,
        ("AI at work", "仕事でのAI活用", "업무용 AI", "AI 工作應用", "AI 工作应用"),
    ),
    (
        "ai-safety",
        "ai",
        400,
        (
            "AI safety & privacy",
            "AIの安全と法規",
            "AI 안전·개인정보",
            "AI 安全、隱私與法規",
            "AI 安全、隐私与法规",
        ),
    ),
    (
        "ai-plans",
        "ai",
        410,
        ("AI plans & pricing", "AIの料金プラン", "AI 요금제", "AI 方案與費用", "AI 方案与费用"),
    ),
    ("wordpress", "website", 420, ("WordPress",) * 5),
    ("woocommerce", "website", 430, ("WooCommerce",) * 5),
    (
        "web-basics",
        "website",
        440,
        (
            "Domains, hosting & front-end",
            "ドメイン・ホスティング・フロントエンド",
            "도메인·호스팅·프런트엔드",
            "網域、主機與前端",
            "域名、主机与前端",
        ),
    ),
    ("seo", "marketing", 450, ("SEO",) * 5),
    (
        "ads",
        "marketing",
        460,
        (
            "Ads & affiliates",
            "広告・アフィリエイト",
            "광고·제휴 마케팅",
            "廣告與聯盟行銷",
            "广告与联盟营销",
        ),
    ),
    (
        "content-marketing",
        "marketing",
        470,
        ("Content & brand", "コンテンツ・ブランド", "콘텐츠·브랜드", "內容與品牌", "内容与品牌"),
    ),
    (
        "finance-basics",
        "finance",
        480,
        ("Money basics", "お金の基本", "재테크 기초", "理財入門", "理财入门"),
    ),
    (
        "banking",
        "finance",
        490,
        ("Banking & payments", "銀行・決済", "은행·결제", "銀行與支付", "银行与支付"),
    ),
    (
        "credit",
        "finance",
        500,
        (
            "Credit cards & credit",
            "クレジットカード・信用",
            "신용카드·신용",
            "信用卡與信用",
            "信用卡与信用",
        ),
    ),
    (
        "tax-insurance",
        "finance",
        510,
        (
            "Tax, insurance & pensions",
            "税金・保険・年金",
            "세금·보험·연금",
            "稅務、保險與勞退",
            "税务、保险与劳退",
        ),
    ),
    (
        "investing",
        "finance",
        520,
        ("Investing basics", "投資の基本", "투자 입문", "投資入門", "投资入门"),
    ),
)

# Spelled out here rather than imported from ``app.guides.taxonomy`` for the reason 0074
# gives: a migration has to keep running after the application constant moves on. The
# vocabulary test holds the two to agree today.
TOPIC_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "ai": {
        "zh-TW": (
            "從名詞解釋、工具評比到寫程式與本機模型："
            "把 AI 用在工作與生活裡的每一步，都有一篇可以照著做的文章。"
        ),
        "en": (
            "From glossary entries and tool comparisons to coding agents and local models: "
            "every step of putting AI to work, written to be followed."
        ),
    },
    "website": {
        "zh-TW": "自己架站與開店：WordPress、WooCommerce、網域主機與前端基礎，從零開始到上線維運。",
        "en": (
            "Build and run your own site: WordPress, WooCommerce, domains, hosting and "
            "front-end basics, from zero to live."
        ),
    },
    "marketing": {
        "zh-TW": "讓內容被看見：SEO、廣告與聯盟行銷、內容與品牌經營的做法與取捨。",
        "en": (
            "Getting content seen: SEO, ads and affiliate programmes, and how to run content "
            "and a brand."
        ),
    },
    "finance": {
        "zh-TW": (
            "看懂錢的流向：記帳、銀行與信用卡、稅務保險、投資入門，只講制度與方法，不推薦商品。"
        ),
        "en": (
            "Understand where the money goes: budgeting, banking and cards, tax and insurance, "
            "investing basics. Methods and rules, never product picks."
        ),
    },
    "software": {
        "zh-TW": "軟體與 App 的設定、比較與替代方案。",
        "en": "Set-up, comparisons and alternatives for apps and software.",
    },
    "ai-terms": {"zh-TW": "一詞一篇：先講定義、再講為什麼重要、最後給一個看得懂的例子。"},
    "ai-news": {"zh-TW": "模型發布、價格變動與政策：只記錄查證過的事實與日期。"},
    "ai-search": {"zh-TW": "AI 搜尋怎麼挑內容、GEO 與 AEO 要做什麼、llms.txt 與結構化資料的實作。"},
    "ai-chat": {"zh-TW": "ChatGPT、Gemini、Claude 與其他對話助理的用法、方案與限制。"},
    "claude-code": {"zh-TW": "Claude Code 從入門到進階的系列教學，附可複製的指令與範例。"},
    "codex": {"zh-TW": "Codex 學習中心：五種語言的系列教學與練習。"},
    "gemini-dev": {"zh-TW": "Gemini CLI 與 API：安裝、認證、腳本化與整合。"},
    "ai-coding": {"zh-TW": "用 AI 寫程式的工具與工作流，以及在自己電腦上跑模型的做法。"},
    "ai-create": {"zh-TW": "圖片、影片與聲音的生成與編修工具，附授權與標示的注意事項。"},
    "ai-work": {"zh-TW": "會議、郵件、簡報、試算表與自動化流程裡的 AI 應用。"},
    "ai-safety": {"zh-TW": "帳號安全、隱私、提示注入、詐騙與各國法規。"},
    "ai-plans": {"zh-TW": "免費與付費方案、API 計價與用量控制。"},
    "wordpress": {"zh-TW": "WordPress 主題、外掛、主機與維運。"},
    "woocommerce": {"zh-TW": "WooCommerce 開店：金流、物流、稅務設定與商品 SEO。"},
    "web-basics": {"zh-TW": "網域、DNS、主機方案與前端基礎。"},
    "seo": {"zh-TW": "站內外 SEO、工具與資料來源。"},
    "ads": {"zh-TW": "Google Ads、AdSense 與聯盟行銷的設定與規範。"},
    "content-marketing": {"zh-TW": "內容行銷、品牌、電子報與社群經營。"},
    "finance-basics": {"zh-TW": "記帳、預算、緊急預備金與家庭財務的第一步。"},
    "banking": {"zh-TW": "銀行帳戶、數位銀行、行動支付與海外用卡。"},
    "credit": {"zh-TW": "信用卡怎麼選、聯徵信用分數與分期的取捨。"},
    "tax-insurance": {"zh-TW": "所得稅、勞健保、勞退與保險的制度說明。"},
    "investing": {"zh-TW": "投資的觀念、台股與海外投資的開戶與流程，不含任何買賣建議。"},
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


def upgrade() -> None:
    _add_columns()
    # After the columns exist, never before: the seed writes parent_id.
    _seed()


def _add_columns() -> None:
    have_parent = have_descriptions = False
    if not context.is_offline_mode():
        columns = {
            column["name"] for column in sa.inspect(op.get_bind()).get_columns("guide_topics")
        }
        have_parent, have_descriptions = "parent_id" in columns, "descriptions_json" in columns
        if have_parent and have_descriptions:
            return
    with op.batch_alter_table("guide_topics") as batch:
        if not have_parent:
            batch.add_column(sa.Column("parent_id", sa.Uuid(), nullable=True))
            batch.create_foreign_key(
                PARENT_FK, "guide_topics", ["parent_id"], ["id"], ondelete="SET NULL"
            )
            batch.create_index(PARENT_INDEX, ["parent_id"])
        if not have_descriptions:
            batch.add_column(sa.Column("descriptions_json", sa.JSON(), nullable=True))


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
        # A lead is written at insert time for a new row; the UPDATE below is for the rows
        # 0074 and 0075 seeded, which have no lead yet. SQLAlchemy would store a Python None
        # as the JSON text ``null``, which ``IS NULL`` never matches, so the key is simply
        # absent when there is nothing to say.
        **({"descriptions_json": TOPIC_DESCRIPTIONS[slug]} if slug in TOPIC_DESCRIPTIONS else {}),
        "created_at": now,
        "updated_at": now,
    }


def _ids_by_slug(bind: Connection) -> dict[str, object]:
    return {row.slug: row.id for row in bind.execute(sa.select(topics.c.id, topics.c.slug))}


def _seed() -> None:
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
    # than skipped: the vocabulary is still complete, it is just flat there.
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
                # SQL NULL from the column add, or the JSON text ``null`` an ORM write of
                # ``None`` leaves behind: both mean "no lead yet".
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
        with op.batch_alter_table("guide_topics") as batch:
            batch.drop_index(PARENT_INDEX)
            batch.drop_column("parent_id")
            batch.drop_column("descriptions_json")
        return
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())
    if "guide_topics" not in tables:
        return
    if "guide_article_topics" in tables:
        bind.execute(sa.text(REMOVE_LINKS))
    bind.execute(sa.text(REMOVE_TOPICS))
    columns = {column["name"] for column in inspector.get_columns("guide_topics")}
    indexes = {index["name"] for index in inspector.get_indexes("guide_topics")}
    if not columns & {"parent_id", "descriptions_json"}:
        return
    with op.batch_alter_table("guide_topics") as batch:
        if "parent_id" in columns:
            # The index first, by name, so SQLite's rebuild is not asked to recreate an
            # index over a column the new table lacks. PostgreSQL would drop it with the
            # column, and the constraint with it, either way.
            if PARENT_INDEX in indexes:
                batch.drop_index(PARENT_INDEX)
            batch.drop_column("parent_id")
        if "descriptions_json" in columns:
            batch.drop_column("descriptions_json")
