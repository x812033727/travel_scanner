"""The theme taxonomy and the seed assignments are data; check them without a database."""

from collections import Counter

import pytest

from app.hotspots.catalog import HOTSPOT_SEEDS
from app.hotspots.theme_catalog import (
    SEASON_THEME_COUNT,
    SEASON_THEME_SLUGS,
    SHOP_THEME_COUNT,
    SHOP_THEME_SLUGS,
    THEME_SEEDS,
    THEME_SEEDS_BY_SLUG,
    validate_months,
)
from app.hotspots.themes import (
    SEED_LINK_PAIRS,
    THEME_BOOTSTRAP,
    resolve_theme,
    theme_name,
    theme_ref,
)
from app.i18n import LOCALES
from app.models import HotspotTheme
from app.problems import AppError

SEEDS_BY_SLUG = {seed.slug: seed for seed in HOTSPOT_SEEDS}
# Shop types that only dedicated stores carry; the catalog has no outlet mall yet, so
# the theme exists (administrators can assign it) but the seed file cannot link it.
SHOP_THEMES_WITHOUT_SEEDS = {"outlet"}


def test_catalog_shape() -> None:
    assert len(THEME_SEEDS) == SEASON_THEME_COUNT + SHOP_THEME_COUNT == 14
    assert len(SEASON_THEME_SLUGS) == 6
    assert len(SHOP_THEME_SLUGS) == 8
    assert SEASON_THEME_SLUGS == {
        "sakura",
        "autumn-leaves",
        "ski",
        "fireworks",
        "illumination",
        "snow-scenery",
    }
    slugs = [seed.slug for seed in THEME_SEEDS]
    assert len(set(slugs)) == len(slugs)
    orders = [seed.display_order for seed in THEME_SEEDS]
    assert len(set(orders)) == len(orders)
    # Seasons sort before shop types everywhere (facets, cards, admin list).
    assert max(s.display_order for s in THEME_SEEDS if s.kind == "season") < min(
        s.display_order for s in THEME_SEEDS if s.kind == "shop"
    )
    for seed in THEME_SEEDS:
        assert set(seed.names) == set(LOCALES), seed.slug
        assert all(seed.names[locale].strip() for locale in LOCALES), seed.slug
        if seed.kind == "season":
            assert seed.months and all(1 <= month <= 12 for month in seed.months), seed.slug
        else:
            assert seed.months == (), seed.slug


@pytest.mark.parametrize("months", [(13,), (0,), (3, 3), (True,), ("4",)])
def test_validate_months_rejects_bad_values(months: tuple[object, ...]) -> None:
    with pytest.raises(RuntimeError):
        validate_months(months)  # type: ignore[arg-type]


def test_validate_months_accepts_wrapping_ranges() -> None:
    validate_months((11, 12, 1, 2))
    validate_months(())


def test_bootstrap_assignments_resolve_to_catalog_seeds() -> None:
    assert THEME_BOOTSTRAP
    hotspot_slugs = [assignment.hotspot_slug for assignment in THEME_BOOTSTRAP]
    assert len(set(hotspot_slugs)) == len(hotspot_slugs)
    for assignment in THEME_BOOTSTRAP:
        seed = SEEDS_BY_SLUG[assignment.hotspot_slug]
        assert assignment.themes
        for theme_slug in assignment.themes:
            theme = THEME_SEEDS_BY_SLUG[theme_slug]
            if theme.kind == "shop":
                assert seed.category == "shopping", (assignment.hotspot_slug, theme_slug)
        for theme_slug, months in assignment.months.items():
            assert theme_slug in assignment.themes
            assert theme_slug in SEASON_THEME_SLUGS, (assignment.hotspot_slug, theme_slug)
            assert months and all(1 <= month <= 12 for month in months)
    assert len(SEED_LINK_PAIRS) == sum(len(a.themes) for a in THEME_BOOTSTRAP)


def test_every_theme_has_seed_coverage() -> None:
    counts = Counter(theme_slug for _, theme_slug in SEED_LINK_PAIRS)
    for slug in SEASON_THEME_SLUGS:
        assert counts[slug] >= 2, slug
    for slug in SHOP_THEME_SLUGS - SHOP_THEMES_WITHOUT_SEEDS:
        assert counts[slug] >= 1, slug
    assert counts["sakura"] >= 25
    assert counts["autumn-leaves"] >= 20


def test_reviewed_spot_checks() -> None:
    by_slug = {assignment.hotspot_slug: assignment for assignment in THEME_BOOTSTRAP}
    assert by_slug["nrt-meguro-river-cherry-blossoms"].themes == ("sakura",)
    # Sapporo blooms in May; the Honshu default of March–April would mislead.
    assert by_slug["deep-cts-q1298335"].months["sakura"] == (5,)
    assert by_slug["kmq-q998239"].months["sakura"] == (4,)
    # Skiing only exists where the catalog has a mountain with a lift.
    assert {SEEDS_BY_SLUG[slug].city_code for slug, theme in SEED_LINK_PAIRS if theme == "ski"} == {
        "CTS"
    }
    # A hotspot may sit in both dimensions: 丸之內仲通 is a shopping street with lights.
    assert set(by_slug["nrt-marunouchi-naka-dori"].themes) == {"illumination", "market-street"}


def test_theme_name_falls_back_like_area_names() -> None:
    theme = HotspotTheme(
        slug="sakura",
        kind="season",
        names_json={"zh-TW": "賞櫻", "en": "Cherry Blossoms"},
        months_json=[3, 4],
    )
    assert theme_name(theme, "zh-TW") == "賞櫻"
    assert theme_name(theme, "zh-CN") == "賞櫻"
    assert theme_name(theme, "ja") == "Cherry Blossoms"
    assert theme_name(
        HotspotTheme(slug="ski", kind="season", names_json={}, months_json=[]), "ko"
    ) == ("ski")


def test_theme_ref_prefers_the_per_hotspot_months() -> None:
    theme = HotspotTheme(
        slug="sakura", kind="season", names_json={"zh-TW": "賞櫻"}, months_json=[3, 4]
    )
    assert theme_ref(theme, "zh-TW") == {
        "slug": "sakura",
        "kind": "season",
        "name": "賞櫻",
        "months": [3, 4],
    }
    assert theme_ref(theme, "zh-TW", [5])["months"] == [5]
    assert theme_ref(theme, "zh-TW", [])["months"] == []


class _OneLookupSession:
    """Just enough of AsyncSession for resolve_theme's single lookup."""

    def __init__(self, row: HotspotTheme | None = None) -> None:
        self.row = row
        self.lookups = 0

    async def scalar(self, statement: object) -> HotspotTheme | None:
        self.lookups += 1
        return self.row


@pytest.mark.asyncio
async def test_resolve_theme_refuses_a_slug_no_active_theme_carries() -> None:
    """The public filter's 422 path: worth a unit test because the integration
    suite that also covers it only runs where PostgreSQL is available."""
    session = _OneLookupSession()

    assert await resolve_theme(session, None) is None  # type: ignore[arg-type]
    assert await resolve_theme(session, "") is None  # type: ignore[arg-type]
    assert session.lookups == 0

    with pytest.raises(AppError) as refused:
        await resolve_theme(session, "bogus")  # type: ignore[arg-type]
    assert refused.value.status == 422
    assert refused.value.code == "unsupported_theme"


@pytest.mark.asyncio
async def test_resolve_theme_normalizes_before_looking_up() -> None:
    theme = HotspotTheme(slug="sakura", kind="season", names_json={}, months_json=[3, 4])
    session = _OneLookupSession(theme)

    assert await resolve_theme(session, "  SAKURA  ") is theme  # type: ignore[arg-type]
    assert session.lookups == 1
