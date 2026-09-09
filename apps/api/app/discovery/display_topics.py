"""Batch-only display labels for already-public catalog items, not search signals."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.discovery.schemas import DiscoveryDisplayTopic, DiscoveryItem
from app.foods.styles import STYLE_NAMES
from app.hotspots.themes import load_hotspot_themes
from app.i18n import Locale
from app.models import FoodMerchantStyle


async def attach_catalog_display_topics(
    session: AsyncSession,
    items: list[DiscoveryItem],
    hotspot_refs: dict[str, UUID],
    locale: Locale,
) -> None:
    """Append active themes and approved styles without widening publication access."""
    themes = await load_hotspot_themes(session, list(dict.fromkeys(hotspot_refs.values())), locale)
    merchant_refs = {
        item.id: UUID(item.collection_ref["id"]) for item in items if item.kind == "merchant"
    }
    merchant_topics: dict[UUID, list[DiscoveryDisplayTopic]] = {}
    if merchant_refs:
        rows = (
            await session.execute(
                select(FoodMerchantStyle.merchant_id, FoodMerchantStyle.style)
                .where(
                    FoodMerchantStyle.merchant_id.in_(list(merchant_refs.values())),
                    FoodMerchantStyle.status == "approved",
                )
                .order_by(FoodMerchantStyle.style)
            )
        ).all()
        for merchant_id, style in rows:
            label = STYLE_NAMES.get(style, {}).get(locale)
            if label:
                merchant_topics.setdefault(merchant_id, []).append(
                    DiscoveryDisplayTopic(id=f"style:{style}", label=label)
                )
    for item in items:
        hotspot_id = hotspot_refs.get(item.id)
        if hotspot_id is not None:
            item.display_topics.extend(
                DiscoveryDisplayTopic(id=f"theme:{theme['slug']}", label=theme["name"])
                for theme in themes.get(hotspot_id, [])
                if theme.get("slug") and theme.get("name")
            )
        merchant_id = merchant_refs.get(item.id)
        if merchant_id is not None:
            item.display_topics.extend(merchant_topics.get(merchant_id, []))
