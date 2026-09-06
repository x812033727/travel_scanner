"""Themes end to end against PostgreSQL: seed, sync, filter, facets, and the sync rules.

Follows ``test_hotspot_seed_reconciliation.py``: real sessions and the catalog seeded
from scratch. The cases run in order against one seeded database — the first one seeds
it, the later ones build on what the earlier ones left — and the last one clears it.
"""

import os
from collections.abc import AsyncIterator
from datetime import date

import pytest
import pytest_asyncio
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionFactory, engine
from app.hotspots import themes as themes_module
from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.service import hotspot_facets, list_rankings, refresh_rankings, seed_catalog
from app.hotspots.theme_catalog import THEME_SEEDS
from app.hotspots.themes import (
    SEED_LINK_PAIRS,
    THEME_BOOTSTRAP,
    resolve_theme,
    sync_hotspot_themes,
)
from app.models import HotspotRanking, HotspotSignal, HotspotTheme, HotspotThemeLink, TravelHotspot
from app.problems import AppError

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="requires PostgreSQL",
)

OBSERVED_ON = date(2026, 9, 1)
SEEDS_BY_SLUG = {seed.slug: seed for seed in HOTSPOT_SEEDS}


@pytest_asyncio.fixture(scope="module", loop_scope="module", autouse=True)
async def dispose_engine_after_module() -> AsyncIterator[None]:
    await engine.dispose(close=False)
    yield
    await engine.dispose()


async def _reset(session: AsyncSession) -> None:
    for model in (HotspotThemeLink, HotspotRanking, HotspotSignal, TravelHotspot, HotspotTheme):
        await session.execute(delete(model))
    await session.commit()


async def _seed_and_rank(session: AsyncSession) -> dict[str, int]:
    await seed_catalog(session, OBSERVED_ON)
    report = await sync_hotspot_themes(session)
    await refresh_rankings(session, OBSERVED_ON)
    await session.commit()
    return report


def _seeded_slugs(theme_slug: str, destination_id: str | None = None) -> set[str]:
    return {
        hotspot_slug
        for hotspot_slug, theme in SEED_LINK_PAIRS
        if theme == theme_slug
        and (destination_id is None or SEEDS_BY_SLUG[hotspot_slug].destination_id == destination_id)
    }


async def _rankings(session: AsyncSession, **kwargs: object) -> dict[str, object]:
    return await list_rankings(session, limit=50, **kwargs)  # type: ignore[arg-type]


@pytest.mark.asyncio(loop_scope="module")
async def test_sync_seeds_every_theme_and_rankings_filter_by_theme() -> None:
    async with SessionFactory() as session:
        await _reset(session)
        report = await _seed_and_rank(session)
    assert report == {
        "themes": len(THEME_SEEDS),
        "links_created": len(SEED_LINK_PAIRS),
        "links_updated": 0,
        "links_removed": 0,
    }

    async with SessionFactory() as session:
        result = await _rankings(session, destination_id="tokyo", theme="sakura", locale="en")
        expected = _seeded_slugs("sakura", "tokyo")
        assert result["total"] == len(expected)
        items = result["items"]
        assert {item["slug"] for item in items} == expected
        for item in items:
            assert "sakura" in {theme["slug"] for theme in item["themes"]}, item["slug"]
        meguro = next(item for item in items if item["slug"] == "nrt-meguro-river-cherry-blossoms")
        assert meguro["themes"] == [
            {"slug": "sakura", "kind": "season", "name": "Cherry Blossoms", "months": [3, 4]}
        ]

        # The per-hotspot override wins: Sapporo blooms in May.
        sapporo = await _rankings(session, destination_id="sapporo", theme="sakura", locale="ja")
        moerenuma = next(item for item in sapporo["items"] if item["slug"] == "deep-cts-q1298335")
        assert moerenuma["themes"][0] == {
            "slug": "sakura",
            "kind": "season",
            "name": "桜",
            "months": [5],
        }

        # Both dimensions on one row, seasons first.
        lit = await _rankings(session, destination_id="tokyo", theme="illumination")
        naka_dori = next(
            item for item in lit["items"] if item["slug"] == "nrt-marunouchi-naka-dori"
        )
        assert [theme["kind"] for theme in naka_dori["themes"]] == ["season", "shop"]
        assert [theme["name"] for theme in naka_dori["themes"]] == ["燈飾", "商店街／市場"]

        # A theme this destination does not carry filters everything out rather than
        # erroring: skiing is a Hokkaido theme, and Tokyo has no mountain in the catalog.
        assert not _seeded_slugs("ski", "tokyo")
        assert (await _rankings(session, destination_id="tokyo", theme="ski"))["total"] == 0
        # The dedicated-store batch gave the shop types real rows: the outlet filter used
        # to return nothing anywhere, and now answers with the mall out at 南大沢.
        outlets = await _rankings(session, destination_id="tokyo", theme="outlet")
        assert {item["slug"] for item in outlets["items"]} == _seeded_slugs("outlet", "tokyo")
        assert outlets["total"] == 1
        with pytest.raises(AppError) as unknown:
            await resolve_theme(session, "bogus")
        assert unknown.value.status == 422
        assert unknown.value.code == "unsupported_theme"
        assert await resolve_theme(session, None) is None


@pytest.mark.asyncio(loop_scope="module")
async def test_facets_list_every_active_theme_in_catalog_order() -> None:
    async with SessionFactory() as session:
        facets = await hotspot_facets(session, "zh-CN")
    themes = facets["themes"]
    seasons = [seed.slug for seed in THEME_SEEDS if seed.kind == "season"]
    shops = [seed.slug for seed in THEME_SEEDS if seed.kind == "shop"]
    assert [theme["slug"] for theme in themes] == seasons + shops
    by_slug = {theme["slug"]: theme for theme in themes}
    assert by_slug["sakura"]["count"] == len(_seeded_slugs("sakura"))
    assert by_slug["sakura"]["name"] == "赏樱"
    assert by_slug["sakura"]["months"] == [3, 4]
    # A shop theme has no months, and its count is the whole catalog's, not one city's.
    assert by_slug["outlet"] == {
        "slug": "outlet",
        "kind": "shop",
        "name": "奥特莱斯",
        "months": [],
        "count": len(_seeded_slugs("outlet")),
    }
    # Every theme in the taxonomy leads somewhere; a chip that returns nothing anywhere
    # is a dead control, and outlet was one until the dedicated stores arrived.
    assert all(theme["count"] > 0 for theme in themes), [
        theme["slug"] for theme in themes if not theme["count"]
    ]
    assert sum(theme["count"] for theme in themes) == len(SEED_LINK_PAIRS)


@pytest.mark.asyncio(loop_scope="module")
async def test_sync_leaves_admin_links_and_tombstones_alone(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async with SessionFactory() as session:
        assert await sync_hotspot_themes(session) == {
            "themes": len(THEME_SEEDS),
            "links_created": 0,
            "links_updated": 0,
            "links_removed": 0,
        }
        sakura = await session.scalar(select(HotspotTheme).where(HotspotTheme.slug == "sakura"))
        lights = await session.scalar(
            select(HotspotTheme).where(HotspotTheme.slug == "illumination")
        )
        sensoji = await session.scalar(select(TravelHotspot).where(TravelHotspot.slug == "sensoji"))
        meguro = await session.scalar(
            select(TravelHotspot).where(TravelHotspot.slug == "nrt-meguro-river-cherry-blossoms")
        )
        assert sakura and lights and sensoji and meguro
        # An administrator tags 淺草寺 with sakura, an AI pass adds lights, and the
        # administrator removes the seeded 目黑川 sakura link, leaving a tombstone.
        session.add(
            HotspotThemeLink(
                hotspot_id=sensoji.id, theme_id=sakura.id, months_json=[3], source="admin"
            )
        )
        session.add(HotspotThemeLink(hotspot_id=sensoji.id, theme_id=lights.id, source="ai"))
        tombstone = await session.scalar(
            select(HotspotThemeLink).where(
                HotspotThemeLink.hotspot_id == meguro.id, HotspotThemeLink.theme_id == sakura.id
            )
        )
        assert tombstone is not None and tombstone.source == "seed"
        tombstone.is_active = False
        tombstone.source = "admin"
        await session.commit()

    async with SessionFactory() as session:
        assert await sync_hotspot_themes(session) == {
            "themes": len(THEME_SEEDS),
            "links_created": 0,
            "links_updated": 0,
            "links_removed": 0,
        }
        await session.commit()
        links = {
            (link.hotspot_id, link.theme_id): link
            for link in (await session.scalars(select(HotspotThemeLink))).all()
        }
        sakura = await session.scalar(select(HotspotTheme).where(HotspotTheme.slug == "sakura"))
        lights = await session.scalar(
            select(HotspotTheme).where(HotspotTheme.slug == "illumination")
        )
        sensoji = await session.scalar(select(TravelHotspot).where(TravelHotspot.slug == "sensoji"))
        meguro = await session.scalar(
            select(TravelHotspot).where(TravelHotspot.slug == "nrt-meguro-river-cherry-blossoms")
        )
        assert sakura and lights and sensoji and meguro
        assert links[(sensoji.id, sakura.id)].source == "admin"
        assert links[(sensoji.id, sakura.id)].months_json == [3]
        assert links[(sensoji.id, lights.id)].source == "ai"
        kept = links[(meguro.id, sakura.id)]
        assert (kept.source, kept.is_active) == ("admin", False)

        result = await _rankings(session, destination_id="tokyo", theme="sakura")
        slugs = {item["slug"] for item in result["items"]}
        assert "sensoji" in slugs
        assert "nrt-meguro-river-cherry-blossoms" not in slugs

    # A pair that leaves the seed file is removed — but only when the seed owns it.
    dropped = next(item for item in THEME_BOOTSTRAP if item.hotspot_slug == "nrt-yoyogi-park")
    monkeypatch.setattr(
        themes_module,
        "THEME_BOOTSTRAP",
        tuple(item for item in THEME_BOOTSTRAP if item is not dropped),
    )
    async with SessionFactory() as session:
        report = await sync_hotspot_themes(session)
        await session.commit()
        assert report["links_removed"] == len(dropped.themes)
        assert report["links_created"] == 0
        yoyogi = await session.scalar(
            select(TravelHotspot).where(TravelHotspot.slug == "nrt-yoyogi-park")
        )
        assert yoyogi is not None
        remaining = (
            await session.scalars(
                select(HotspotThemeLink).where(HotspotThemeLink.hotspot_id == yoyogi.id)
            )
        ).all()
        assert remaining == []
        total = await session.scalar(select(HotspotThemeLink).limit(1))
        assert total is not None


@pytest.mark.asyncio(loop_scope="module")
async def test_deactivated_theme_disappears_from_filter_and_facets() -> None:
    async with SessionFactory() as session:
        sakura = await session.scalar(select(HotspotTheme).where(HotspotTheme.slug == "sakura"))
        assert sakura is not None
        sakura.is_active = False
        await session.commit()

    async with SessionFactory() as session:
        with pytest.raises(AppError):
            await resolve_theme(session, "sakura")
        facets = await hotspot_facets(session, "en")
        assert "sakura" not in {theme["slug"] for theme in facets["themes"]}
        result = await _rankings(session, destination_id="tokyo", theme="sakura")
        assert result["total"] == 0
        # The seed sync never reactivates a theme an administrator switched off.
        await sync_hotspot_themes(session)
        sakura = await session.scalar(select(HotspotTheme).where(HotspotTheme.slug == "sakura"))
        assert sakura is not None and sakura.is_active is False
        await _reset(session)
