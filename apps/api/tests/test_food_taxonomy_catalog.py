from collections import Counter

import pytest

from app.destinations.catalog import DESTINATIONS
from app.destinations.catalog import destination_for_id
from app.foods.area_catalog import (
    ALL_AREA_SEEDS,
    AREA_SEEDS,
    AREA_SEEDS_BY_SLUG,
    TREND_AREA_SEEDS,
    TREND_AREA_SEEDS_BY_SLUG,
    AreaSeed,
    area_seed_for,
)
from app.foods.catalog import FOOD_SEEDS
from app.foods.category_catalog import (
    CATEGORY_SEEDS,
    CATEGORY_SEEDS_BY_SLUG,
    DISH_CATEGORIES,
    categories_for_dishes,
    validate_names,
)
from app.foods.merchant_catalog import (
    MERCHANT_AREA_KEYS,
    MERCHANT_EXTRA_CATEGORIES,
    MERCHANT_SEEDS,
)
from app.i18n import LOCALES


def test_categories_are_site_wide_localized_and_cover_every_dish() -> None:
    assert len(CATEGORY_SEEDS) == 18
    assert len({seed.slug for seed in CATEGORY_SEEDS}) == 18
    assert [seed.display_order for seed in CATEGORY_SEEDS] == list(range(1, 19))
    for seed in CATEGORY_SEEDS:
        assert set(seed.names) == set(LOCALES)
        assert all(seed.names[locale].strip() for locale in LOCALES)
    assert set(DISH_CATEGORIES) == {seed.slug for seed in FOOD_SEEDS}
    used = {slug for slugs in DISH_CATEGORIES.values() for slug in slugs}
    assert used <= set(CATEGORY_SEEDS_BY_SLUG)
    assert "fine-dining" not in used  # curated extra only
    assert categories_for_dishes(("jp-sushi", "jp-ramen"), ("fine-dining", "sushi")) == (
        "sushi",
        "seafood",
        "ramen",
        "fine-dining",
    )


def test_validate_names_requires_every_site_locale() -> None:
    with pytest.raises(RuntimeError):
        validate_names({"zh-TW": "壽司"})
    with pytest.raises(RuntimeError):
        validate_names({locale: " " for locale in LOCALES})


def test_areas_mirror_destination_profiles_with_five_locales() -> None:
    assert len(AREA_SEEDS) == 132
    assert Counter(seed.destination_id for seed in AREA_SEEDS) == {
        profile.id: 4 for profile in DESTINATIONS
    }
    for profile in DESTINATIONS:
        for source_name in profile.areas:
            seed = area_seed_for(profile.id, source_name)
            assert seed is not None, (profile.id, source_name)
            assert seed.slug.startswith(f"{profile.id}-")
            assert set(seed.names) == set(LOCALES)
            assert seed.names["zh-TW"] == source_name
    combined = [seed for seed in AREA_SEEDS if "／" in seed.source_name]
    assert len(combined) == 8
    assert all(" / " in seed.names["en"] for seed in combined)
    assert AREA_SEEDS_BY_SLUG["osaka-kyoto-namba-shinsaibashi"].names["ja"] == "難波・心斎橋"
    assert AREA_SEEDS_BY_SLUG["tokyo-shibuya"].names["zh-CN"] == "涩谷"
    assert all(seed.center is None for seed in AREA_SEEDS)


def test_trend_districts_are_a_separate_list_with_centres_and_reviewed_names() -> None:
    assert len(TREND_AREA_SEEDS) == 57
    assert len(ALL_AREA_SEEDS) == 132 + 57
    assert not set(TREND_AREA_SEEDS_BY_SLUG) & set(AREA_SEEDS_BY_SLUG)
    for seed in TREND_AREA_SEEDS:
        assert set(seed.names) == set(LOCALES)
        assert all(seed.names[locale].strip() for locale in LOCALES)
        assert seed.center is not None
        assert seed.display_order > 200
        assert seed.match_terms
        assert destination_for_id(seed.destination_id) is not None
    for destination_id in {seed.destination_id for seed in ALL_AREA_SEEDS}:
        orders = [s.display_order for s in ALL_AREA_SEEDS if s.destination_id == destination_id]
        assert len(set(orders)) == len(orders), destination_id
    # Reviewer-verified spellings; a well-meaning re-translation must fail here.
    assert TREND_AREA_SEEDS_BY_SLUG["taichung-shenji"].names["ko"] == "심계신촌"
    assert TREND_AREA_SEEDS_BY_SLUG["singapore-jalan-besar"].names["ja"] == "ジャラン・ベサール"
    assert TREND_AREA_SEEDS_BY_SLUG["daegu-bukseongro"].names["ja"] == "北城路（プクソンノ）"
    assert TREND_AREA_SEEDS_BY_SLUG["okinawa-minatogawa"].center == (26.2627, 127.7152)
    assert TREND_AREA_SEEDS_BY_SLUG["osaka-kyoto-kawaramachi-gojo"].center == (34.9943, 135.7656)


def test_area_seed_slug_and_source_name_are_derived() -> None:
    seed = AreaSeed(
        destination_id="tokyo",
        key="shinjuku",
        names={"zh-TW": "新宿", "zh-CN": "新宿", "en": "Shinjuku", "ja": "新宿", "ko": "신주쿠"},
    )
    assert seed.slug == "tokyo-shinjuku"
    assert seed.source_name == "新宿"


def test_every_merchant_has_categories_and_curated_areas_stay_in_their_city() -> None:
    assert len(MERCHANT_SEEDS) == 173
    for merchant in MERCHANT_SEEDS:
        assert 1 <= len(merchant.category_slugs) <= 6, merchant.slug
        assert len(set(merchant.category_slugs)) == len(merchant.category_slugs)
        assert set(merchant.category_slugs) <= set(CATEGORY_SEEDS_BY_SLUG)
        if merchant.area_slug:
            area = AREA_SEEDS_BY_SLUG[merchant.area_slug]
            assert area.destination_id == merchant.destination_id, merchant.slug
    merchant_slugs = {merchant.slug for merchant in MERCHANT_SEEDS}
    assert set(MERCHANT_AREA_KEYS) <= merchant_slugs
    assert set(MERCHANT_EXTRA_CATEGORIES) <= merchant_slugs
    assert sum(1 for merchant in MERCHANT_SEEDS if merchant.area_slug) == 80
    assert sum(len(merchant.category_slugs) for merchant in MERCHANT_SEEDS) == 271
    by_slug = {merchant.slug: merchant for merchant in MERCHANT_SEEDS}
    assert by_slug["tokyo-ichiran-shibuya"].area_slug == "tokyo-shibuya"
    assert by_slug["tokyo-ichiran-shibuya"].category_slugs == ("ramen",)
    assert by_slug["fukuoka-sushi-sakai"].category_slugs == ("sushi", "seafood", "fine-dining")
    assert by_slug["tainan-du-xiao-yue"].area_slug == "tainan-west-central"
    assert by_slug["tokyo-sushi-dai"].area_slug is None
    # The three cities that had no food at all until now.
    assert by_slug["okinawa-kijimuna-onna"].area_slug == "okinawa-onna"
    assert by_slug["yokohama-manchinro-honten"].area_slug == "yokohama-chinatown-motomachi"
    assert by_slug["kamakura-tenshin-an"].area_slug == "kamakura-kita-kamakura"
    assert by_slug["okinawa-inaka-kosetsu-ichiba"].category_slugs == ("noodles",)
    assert by_slug["yokohama-hotel-new-grand"].category_slugs == (
        "noodles",
        "home-style",
        "rice-dishes",
    )
