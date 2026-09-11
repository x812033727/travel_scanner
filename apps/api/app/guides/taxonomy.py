"""Topic vocabulary for intel and guide articles.

The first nine slugs are the ones ``app.discovery.taxonomy`` already uses for hotspots and
dishes. Reusing those ids is what lets a guide and an attraction that share a subject find
each other later instead of living in two vocabularies that only look alike.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.guides.models import GuideTopic
from app.guides.schemas import TopicList, TopicOption
from app.i18n import DEFAULT_LOCALE, LOCALES, Locale

# slug -> (en, ja, ko, zh-TW, zh-CN), in the order of app.i18n.LOCALES.
SEED_TOPICS: tuple[tuple[str, tuple[str, str, str, str, str]], ...] = (
    ("transport", ("Transport", "交通", "교통", "交通", "交通")),
    ("entry", ("Entry rules", "入国手続き", "입국 규정", "簽證入境", "签证入境")),
    ("packing", ("Before you go", "出発前の準備", "출발 전 준비", "行前準備", "行前准备")),
    ("itinerary", ("Itineraries", "モデルコース", "추천 일정", "行程範例", "行程范例")),
    ("budget", ("Budget", "予算", "예산", "預算", "预算")),
    ("deal", ("Deals", "お得情報", "할인 정보", "優惠情報", "优惠情报")),
    ("season", ("Seasonal", "季節の催し", "계절 행사", "季節活動", "季节活动")),
    ("connectivity", ("Staying online", "通信・ネット", "통신・인터넷", "網路通訊", "网络通讯")),
    ("etiquette", ("Etiquette", "マナー", "에티켓", "禮儀文化", "礼仪文化")),
    ("safety", ("Safety", "安全・緊急時", "안전・비상", "安全應變", "安全应变")),
    ("food", ("Food", "グルメ", "음식", "美食", "美食")),
    ("shopping", ("Shopping", "ショッピング", "쇼핑", "購物", "购物")),
    ("hotel", ("Hotels", "ホテル", "호텔", "飯店", "酒店")),
    ("culture", ("Culture", "文化", "문화", "文化", "文化")),
    ("nature", ("Nature", "自然", "자연", "自然", "自然")),
    ("family", ("Family", "家族向け", "가족 여행", "親子", "亲子")),
    ("nightlife", ("Nightlife", "ナイトライフ", "야간 활동", "夜生活", "夜生活")),
    ("viewpoint", ("Viewpoints", "展望スポット", "전망 명소", "觀景", "观景")),
    ("beach", ("Beaches", "ビーチ", "해변", "海灘", "海滩")),
)


def seed_names(labels: tuple[str, str, str, str, str]) -> dict[str, str]:
    return dict(zip(LOCALES, labels, strict=True))


def topic_label(topic: GuideTopic, locale: Locale) -> str:
    """The reader's language if the topic has it, else the default locale, else the slug.

    A topic an administrator added may not carry all five labels yet. Showing the slug is
    honest about that; inventing a translation is not.
    """
    names = topic.names_json or {}
    return names.get(locale) or names.get(DEFAULT_LOCALE) or topic.slug


def topic_option(topic: GuideTopic, locale: Locale) -> TopicOption:
    return TopicOption(slug=topic.slug, label=topic_label(topic, locale))


async def list_topics(session: AsyncSession, locale: Locale) -> TopicList:
    rows = await session.scalars(
        select(GuideTopic)
        .where(GuideTopic.is_active.is_(True))
        .order_by(GuideTopic.display_order, GuideTopic.slug)
    )
    return TopicList(topics=[topic_option(row, locale) for row in rows])
