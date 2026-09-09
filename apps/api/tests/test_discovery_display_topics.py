"""Display-only labels share publication gates without changing search/ranking topics."""

from datetime import date
from uuid import uuid4

import pytest
from sqlalchemy import event, update
from test_discovery_flow import guide, merchant, seed_types
from test_travel_discovery import harness as harness
from test_travel_discovery import hotspot

from app.discovery.schemas import DiscoveryItem
from app.discovery.service import resolve_discovery_items
from app.discovery.sources import base_item, catalog_items
from app.foods.styles import STYLE_NAMES
from app.i18n import LOCALES
from app.models import (
    FoodMerchant,
    FoodMerchantSource,
    FoodMerchantStyle,
    HotspotGuide,
    HotspotTheme,
    HotspotThemeLink,
    TravelFood,
    TravelHotspot,
)

THEME_NAMES = {
    "en": "Cherry blossoms",
    "ja": "桜",
    "ko": "벚꽃",
    "zh-TW": "賞櫻",
    "zh-CN": "赏樱",
}
CULTURE_NAMES = dict(zip(LOCALES, ("Culture", "文化", "문화", "文化", "文化"), strict=True))


def style(merchant_id, name="artsy", status="approved"):
    return FoodMerchantStyle(
        merchant_id=merchant_id,
        style=name,
        status=status,
        evidence_url="https://example.com/review",
        evidence_title="Reviewed evidence",
        rationale="Only the approved editorial label is public",
        checked_on=date(2026, 9, 1),
    )


async def seed_topics(factory):
    place, dish, restaurant, hotel, article, video = await seed_types(factory)
    async with factory() as session:
        theme = HotspotTheme(slug="sakura", kind="season", names_json=THEME_NAMES, display_order=10)
        hidden = HotspotTheme(
            slug="hidden", kind="season", names_json={"en": "Hidden"}, is_active=False
        )
        removed = HotspotTheme(slug="removed", kind="season", names_json={"en": "Removed"})
        session.add_all([theme, hidden, removed])
        await session.flush()
        session.add_all(
            [
                HotspotThemeLink(hotspot_id=place.id, theme_id=theme.id),
                HotspotThemeLink(hotspot_id=place.id, theme_id=hidden.id),
                HotspotThemeLink(hotspot_id=place.id, theme_id=removed.id, is_active=False),
                style(restaurant.id),
                style(restaurant.id, "instagrammable", "pending"),
            ]
        )
        await session.execute(
            update(TravelFood)
            .where(TravelFood.id == dish.id)
            .values(ingredient_tags=["unknown_tag"])
        )
        await session.commit()
    return place, dish, restaurant, hotel, article, video, theme


@pytest.mark.asyncio
@pytest.mark.parametrize("locale", LOCALES)
async def test_localized_topics_are_public_in_search_detail_and_saved_resolution(harness, locale):
    client, factory, _, _, _ = harness
    place, _, restaurant, _, article, _, _ = await seed_topics(factory)
    headers = {"X-Travel-Locale": locale}
    response = await client.get("/api/v1/discovery/search", headers=headers)
    assert response.status_code == 200, response.text
    items = {item["kind"]: item for item in response.json()["items"]}
    expected = [
        {"id": "category:culture", "label": CULTURE_NAMES[locale]},
        {"id": "theme:sakura", "label": THEME_NAMES[locale]},
    ]
    for kind in ("hotspot", "article", "video"):
        assert items[kind]["display_topics"] == expected
        assert items[kind]["topics"] == ["culture"]
    # The guide's original language must not replace the requested display language.
    assert items["article"]["locale"] == "en"
    assert items["merchant"]["display_topics"][-1] == {
        "id": "style:artsy",
        "label": STYLE_NAMES["artsy"][locale],
    }
    assert items["merchant"]["topics"] == ["food"]
    assert [topic["id"] for topic in items["food"]["display_topics"]] == ["category:noodle_soup"]
    assert items["food"]["topics"] == ["food", "noodle_soup", "unknown_tag"]
    assert items["hotel"]["display_topics"] == []
    assert items["hotel"]["topics"] == ["hotel"]
    feed = await client.get("/api/v1/discovery/feed", headers=headers)
    assert feed.status_code == 200, feed.text
    assert {row["id"]: row["display_topics"] for row in feed.json()["items"]} == {
        row["id"]: row["display_topics"] for row in items.values()
    }
    for kind, target in (("hotspot", place), ("article", article), ("merchant", restaurant)):
        detail = await client.get(f"/api/v1/discovery/content/{kind}/{target.id}", headers=headers)
        assert detail.status_code == 200, detail.text
        assert detail.json()["display_topics"] == items[kind]["display_topics"]
    async with factory() as session:
        saved = await resolve_discovery_items(
            session, [f"hotspot:{place.id}", f"guide:{article.id}"], None, locale
        )
        assert [row.model_dump()["display_topics"] for row in saved] == [expected, expected]


def test_unknown_or_missing_labels_are_not_fabricated_and_defaults_are_independent():
    item = base_item("hotspot", uuid4(), "Place", "en", "tokyo", None, topics=["new_slug"])
    assert item.topics == ["new_slug"]
    assert item.display_topics == []
    legacy = item.model_dump(exclude={"display_topics"})
    assert DiscoveryItem.model_validate(legacy).display_topics == []
    known = base_item(
        "post", uuid4(), "Story", "ja", "tokyo", None, topics=["culture", "culture", "new_slug"]
    )
    assert known.model_dump()["display_topics"] == [{"id": "category:culture", "label": "文化"}]
    assert known.topics == ["culture", "culture", "new_slug"]
    assert item.display_topics == []


@pytest.mark.asyncio
async def test_theme_order_namespace_and_immediate_reauthorization_keep_search_semantics(harness):
    client, factory, _, _, _ = harness
    place, _, restaurant, _, _, _, theme = await seed_topics(factory)
    async with factory() as session:
        first = HotspotTheme(
            slug="culture", kind="season", names_json={"en": "Festival"}, display_order=1
        )
        session.add(first)
        await session.flush()
        session.add(HotspotThemeLink(hotspot_id=place.id, theme_id=first.id))
        await session.commit()
    response = await client.get("/api/v1/discovery/search", params={"type": "hotspot"})
    assert response.json()["items"][0]["display_topics"] == [
        {"id": "category:culture", "label": "Culture"},
        {"id": "theme:culture", "label": "Festival"},
        {"id": "theme:sakura", "label": "Cherry blossoms"},
    ]
    # Display-only additions do not silently become search or recommendation inputs.
    response = await client.get("/api/v1/discovery/search", params={"topic": "sakura"})
    assert response.json()["items"] == []
    async with factory() as session:
        await session.execute(
            update(HotspotTheme).where(HotspotTheme.id == theme.id).values(is_active=False)
        )
        await session.execute(
            update(HotspotThemeLink)
            .where(HotspotThemeLink.theme_id == first.id)
            .values(is_active=False)
        )
        await session.execute(
            update(FoodMerchantStyle)
            .where(
                FoodMerchantStyle.merchant_id == restaurant.id,
                FoodMerchantStyle.style == "artsy",
            )
            .values(status="rejected")
        )
        await session.execute(
            update(FoodMerchantStyle)
            .where(
                FoodMerchantStyle.merchant_id == restaurant.id,
                FoodMerchantStyle.style == "instagrammable",
            )
            .values(status="approved")
        )
        await session.commit()
    response = await client.get("/api/v1/discovery/search")
    items = {item["kind"]: item for item in response.json()["items"]}
    for kind in ("hotspot", "article", "video"):
        assert items[kind]["display_topics"] == [{"id": "category:culture", "label": "Culture"}]
        assert items[kind]["topics"] == ["culture"]
    assert [topic["id"] for topic in items["merchant"]["display_topics"]] == [
        "category:food",
        "style:instagrammable",
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "change",
    [{"review_status": "pending"}, {"is_active": False}, {"map_match_status": "unverified"}],
)
async def test_approved_style_never_publishes_an_ineligible_merchant(harness, change):
    client, factory, _, _, _ = harness
    _, _, restaurant, _, _, _, _ = await seed_topics(factory)
    async with factory() as session:
        await session.execute(
            update(FoodMerchant).where(FoodMerchant.id == restaurant.id).values(**change)
        )
        await session.commit()
    response = await client.get("/api/v1/discovery/search", params={"type": "merchant"})
    assert response.status_code == 200, response.text
    assert response.json()["items"] == []
    detail = await client.get(f"/api/v1/discovery/content/merchant/{restaurant.id}")
    assert detail.status_code == 404


@pytest.mark.asyncio
async def test_active_themes_do_not_expose_pending_parent_or_pending_guide(harness):
    client, factory, _, _, _ = harness
    place, _, _, _, article, video, _ = await seed_topics(factory)
    async with factory() as session:
        await session.execute(
            update(HotspotGuide)
            .where(HotspotGuide.id == article.id)
            .values(review_status="pending")
        )
        await session.commit()
    response = await client.get("/api/v1/discovery/search", params={"type": "article"})
    assert response.json()["items"] == []
    assert (await client.get(f"/api/v1/discovery/content/article/{article.id}")).status_code == 404
    async with factory() as session:
        await session.execute(
            update(TravelHotspot)
            .where(TravelHotspot.id == place.id)
            .values(review_status="pending")
        )
        await session.commit()
    response = await client.get("/api/v1/discovery/search", params={"category": "hotspots"})
    assert response.json()["items"] == []
    assert (await client.get(f"/api/v1/discovery/content/video/{video.id}")).status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize("count", [1, 20])
async def test_label_enrichment_uses_one_theme_and_one_style_query_per_batch(harness, count):
    _, factory, _, _, _ = harness
    async with factory() as session:
        places = [hotspot(f"Place {index}") for index in range(count)]
        shops = [merchant(f"Shop {index}") for index in range(count)]
        theme = HotspotTheme(slug="sakura", kind="season", names_json=THEME_NAMES)
        session.add_all([*places, *shops, theme])
        await session.flush()
        for place, shop in zip(places, shops, strict=True):
            session.add_all(
                [
                    HotspotThemeLink(hotspot_id=place.id, theme_id=theme.id),
                    guide(place),
                    style(shop.id),
                    FoodMerchantSource(
                        merchant_id=shop.id,
                        source_url="https://example.com/source",
                        source_type="merchant_official",
                        source_title="Official",
                        is_current=True,
                    ),
                ]
            )
        await session.commit()
        engine = session.bind.sync_engine
        queries = []

        def record(_conn, _cursor, statement, _parameters, _context, _many):
            queries.append(statement)

        event.listen(engine, "before_cursor_execute", record)
        try:
            items = await catalog_items(session, "en", kinds={"hotspot", "article", "merchant"})
        finally:
            event.remove(engine, "before_cursor_execute", record)
    assert len(items) == count * 3
    assert sum("FROM hotspot_theme_links" in query for query in queries) == 1
    assert sum("FROM food_merchant_styles" in query for query in queries) == 1
    for item in items:
        assert len(item.display_topics) == 2
