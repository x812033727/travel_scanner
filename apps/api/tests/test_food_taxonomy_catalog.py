from collections import Counter

import pytest

from app.destinations.catalog import DESTINATIONS
from app.foods.area_catalog import AREA_SEEDS, AREA_SEEDS_BY_SLUG, AreaSeed, area_seed_for
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


def test_area_seed_slug_and_source_name_are_derived() -> None:
    seed = AreaSeed(
        destination_id="tokyo",
        key="shinjuku",
        names={"zh-TW": "新宿", "zh-CN": "新宿", "en": "Shinjuku", "ja": "新宿", "ko": "신주쿠"},
    )
    assert seed.slug == "tokyo-shinjuku"
    assert seed.source_name == "新宿"


def test_every_merchant_has_categories_and_curated_areas_stay_in_their_city() -> None:
    assert len(MERCHANT_SEEDS) == 155
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
    assert sum(1 for merchant in MERCHANT_SEEDS if merchant.area_slug) == 71
    assert sum(len(merchant.category_slugs) for merchant in MERCHANT_SEEDS) == 242
    by_slug = {merchant.slug: merchant for merchant in MERCHANT_SEEDS}
    assert by_slug["tokyo-ichiran-shibuya"].area_slug == "tokyo-shibuya"
    assert by_slug["tokyo-ichiran-shibuya"].category_slugs == ("ramen",)
    assert by_slug["fukuoka-sushi-sakai"].category_slugs == ("sushi", "seafood", "fine-dining")
    assert by_slug["tainan-du-xiao-yue"].area_slug == "tainan-west-central"
    assert by_slug["tokyo-sushi-dai"].area_slug is None
