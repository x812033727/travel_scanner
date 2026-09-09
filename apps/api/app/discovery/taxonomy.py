"""Labels for actual published catalog topic IDs, not invented recommendations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.service import effective_site_visibility
from app.discovery.schemas import DiscoveryDisplayTopic, Kind
from app.i18n import LOCALES, Locale
from app.models import TravelFood, TravelHotspot
from app.travel_services.service import catalog_config

LABELS = {
    "culture": ("Culture", "文化", "문화", "文化", "文化"),
    "nature": ("Nature", "自然", "자연", "自然", "自然"),
    "beach": ("Beaches", "ビーチ", "해변", "海灘", "海滩"),
    "family": ("Family", "家族向け", "가족 여행", "親子", "亲子"),
    "nightlife": ("Nightlife", "ナイトライフ", "야간 활동", "夜生活", "夜生活"),
    "viewpoint": ("Viewpoints", "展望スポット", "전망 명소", "觀景", "观景"),
    "food": ("Food", "グルメ", "음식", "美食", "美食"),
    "shopping": ("Shopping", "ショッピング", "쇼핑", "購物", "购物"),
    "hotel": ("Hotels", "ホテル", "호텔", "飯店", "酒店"),
    "main": ("Main dishes", "主菜", "주요리", "主食", "主食"),
    "noodle_soup": ("Noodles and soups", "麺・スープ", "면과 국물", "麵食與湯品", "面食与汤品"),
    "street_food": ("Street food", "屋台料理", "길거리 음식", "街頭小吃", "街头小吃"),
    "dessert": ("Desserts", "デザート", "디저트", "甜點", "甜点"),
    "drink": ("Drinks", "ドリンク", "음료", "飲品", "饮品"),
}


def display_category_topics(
    kind: Kind, topics: list[str], locale: Locale
) -> list[DiscoveryDisplayTopic]:
    """Display known translations only; ranking/filter topic IDs remain untouched."""
    index = LOCALES.index(locale)
    return [
        DiscoveryDisplayTopic(id=f"category:{topic}", label=LABELS[topic][index])
        for topic in dict.fromkeys(topics)
        if topic in LABELS and not (topic == kind and kind in {"food", "hotel"})
    ]


async def topic_options(session: AsyncSession, locale: Locale) -> list[dict[str, str]]:
    topics: set[str] = set()
    if (await effective_site_visibility(session)).hotspots_enabled:
        topics.update(
            await session.scalars(
                select(TravelHotspot.category)
                .where(
                    TravelHotspot.is_active.is_(True),
                    TravelHotspot.review_status.in_(("approved", "auto_approved")),
                )
                .distinct()
                .order_by(TravelHotspot.category)
                .limit(50)
            )
        )
    foods = list(
        await session.scalars(
            select(TravelFood.food_kind)
            .where(TravelFood.is_active.is_(True), TravelFood.review_status == "approved")
            .distinct()
            .order_by(TravelFood.food_kind)
            .limit(10)
        )
    )
    if foods:
        topics.update(["food", *foods])
    config, _ = await catalog_config(session)
    if config.public_enabled and "hotel" in config.enabled_kinds:
        topics.add("hotel")
    index = LOCALES.index(locale)
    return [
        {"id": topic, "label": LABELS[topic][index] if topic in LABELS else topic.replace("_", " ")}
        for topic in sorted(topics)
        if topic
    ]
