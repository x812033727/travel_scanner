"""The trend-district merchant import: rules, dedupe and the committed batch, no database."""

import json
from typing import Any

import pytest

from app.foods.area_catalog import AREA_SEEDS_BY_SLUG, TREND_AREA_SEEDS_BY_SLUG
from app.foods.category_catalog import CATEGORY_SEEDS_BY_SLUG
from app.foods.merchant_catalog import MERCHANT_SEEDS
from app.foods.service import destination_country_code, merchant_names
from app.foods.trend_import import (
    DEFAULT_FILE,
    SOURCE_SCOPES,
    TrendImportError,
    load_trend_merchants,
    parse_merchant,
    parse_merchants,
    slug_for,
)
from app.i18n import LOCALES
from app.models import FoodMerchant


def _row(**overrides: Any) -> dict[str, Any]:
    row: dict[str, Any] = {
        "destination": "tokyo",
        "district_key": "kuramae",
        "name_zh": "Dandelion Chocolate 藏前工廠咖啡館",
        "local_name": "ダンデライオン・チョコレート ファクトリー＆カフェ蔵前",
        "address_local": "東京都台東区蔵前4-14-6",
        "category_slugs": ["desserts-sweets", "cafe-tea"],
        "source_url": "https://dandelionchocolate.jp/pages/factory-cafe-kuramae",
        "source_title": "ファクトリー&カフェ蔵前 – Dandelion Chocolate 公式サイト",
        "source_kind": "merchant_official",
        "note": "Bean-to-bar 巧克力工廠兼咖啡館",
        "confidence": "high",
        "slug": "tokyo-dandelion-chocolate",
    }
    row.update(overrides)
    return row


def test_a_valid_row_parses_into_the_shape_production_holds() -> None:
    merchant = parse_merchant(_row(), row=1)
    assert merchant.slug == "tokyo-dandelion-chocolate"
    assert merchant.area_slug == "tokyo-kuramae"
    assert merchant.source_scope == "merchant_website"
    assert merchant.category_slugs == ("desserts-sweets", "cafe-tea")
    assert merchant.identity == (
        "tokyo",
        "ダンデライオン・チョコレート ファクトリー＆カフェ蔵前".casefold(),
    )
    listing = parse_merchant(_row(source_kind="official_tourism"), row=1)
    assert listing.source_scope == "merchant_listing"
    assert SOURCE_SCOPES == {
        "merchant_official": "merchant_website",
        "official_tourism": "merchant_listing",
    }


@pytest.mark.parametrize(
    ("overrides", "message"),
    [
        ({"destination": "atlantis"}, "unknown destination"),
        ({"district_key": "Kuramae"}, "kebab-case"),
        ({"name_zh": "  "}, "name_zh is required"),
        ({"local_name": None}, "local_name is required"),
        ({"slug": "kuramae-dandelion"}, "start with 'tokyo-'"),
        ({"slug": "tokyo-Dandelion"}, "kebab-case"),
        ({"source_url": "http://dandelionchocolate.jp/"}, "must be https"),
        ({"source_kind": "tabelog"}, "source_kind must be one of"),
        ({"category_slugs": []}, "non-empty list"),
        ({"category_slugs": ["cafe-tea", "cafe-tea"]}, "repeats a category"),
        ({"category_slugs": ["cafe-tea", "sushi", "ramen", "curry"]}, "at most 3"),
        ({"category_slugs": ["bubble-tea-shop"]}, "unknown categories"),
        ({"source_title": ""}, "source_title is required"),
    ],
)
def test_broken_rows_are_refused_with_the_row_and_the_rule(
    overrides: dict[str, Any], message: str
) -> None:
    with pytest.raises(TrendImportError, match=message) as raised:
        parse_merchant(_row(**overrides), row=7)
    assert "row 7" in str(raised.value)


def test_a_missing_slug_is_derived_from_the_latin_brand_or_a_transliteration() -> None:
    assert slug_for("tokyo", "FUGLEN TOKYO 咖啡", "FUGLEN TOKYO") == "tokyo-fuglen-tokyo"
    assert slug_for("tokyo", "喫茶半月", "喫茶半月") == "tokyo-chi-cha-ban-yue"
    assert slug_for("seoul", "카페 어니언 성수", "카페 어니언 성수") == "seoul-kape-eonieon-seongsu"
    derived = parse_merchant(_row(slug=None), row=1)
    assert derived.slug == "tokyo-dandelion-chocolate"


def test_in_file_duplicates_are_refused_on_slug_and_on_identity() -> None:
    with pytest.raises(TrendImportError, match="duplicate slugs"):
        parse_merchants([_row(), _row(local_name="別家")])
    with pytest.raises(TrendImportError, match="same destination and local_name"):
        parse_merchants([_row(), _row(slug="tokyo-dandelion-two")])
    # Two different shops in two different cities never collide.
    assert (
        len(
            parse_merchants(
                [_row(), _row(destination="seoul", district_key="seongsu", slug="seoul-x")]
            )
        )
        == 2
    )


def test_the_committed_batch_is_valid_and_points_at_seeded_areas_and_categories() -> None:
    merchants = load_trend_merchants(DEFAULT_FILE)
    # 101 from the 2026-09-06 sweep plus the 45 second-sweep shops for the empty districts.
    assert len(merchants) == 146
    assert all(m.area_slug in TREND_AREA_SEEDS_BY_SLUG for m in merchants), [
        m.area_slug for m in merchants if m.area_slug not in TREND_AREA_SEEDS_BY_SLUG
    ]
    assert not any(m.area_slug in AREA_SEEDS_BY_SLUG for m in merchants)
    assert all(slug in CATEGORY_SEEDS_BY_SLUG for m in merchants for slug in m.category_slugs)
    assert all(m.source_url.startswith("https://") for m in merchants)
    assert {m.source_kind for m in merchants} == set(SOURCE_SCOPES)
    # The file is what ships in the wheel and what production imported: keep it tidy.
    raw = json.loads(DEFAULT_FILE.read_text(encoding="utf-8"))
    assert [row["slug"] for row in raw] == [m.slug for m in merchants]


def test_the_committed_batch_overlaps_the_curated_catalog_by_exactly_two_tainan_shops() -> None:
    """Why the importer dedupes on two keys: this is the overlap it met in production."""
    merchants = load_trend_merchants(DEFAULT_FILE)
    catalog_slugs = {seed.slug for seed in MERCHANT_SEEDS}
    catalog_identity = {
        (seed.destination_id, seed.local_name.casefold()) for seed in MERCHANT_SEEDS
    }
    by_slug = sorted(m.slug for m in merchants if m.slug in catalog_slugs)
    by_name = sorted(
        m.slug for m in merchants if m.slug not in catalog_slugs and m.identity in catalog_identity
    )
    assert len(by_slug) == 1 and len(by_name) == 1, (by_slug, by_name)
    assert all(slug.startswith("tainan-") for slug in by_slug + by_name)


def test_an_imported_merchant_reads_in_every_site_locale() -> None:
    merchant = parse_merchant(_row(), row=1)
    row = FoodMerchant(
        slug=merchant.slug,
        destination_id=merchant.destination_id,
        country_code=destination_country_code(merchant.destination_id) or "",
        name=merchant.name,
        local_name=merchant.local_name,
        names_json={},
    )
    names = merchant_names(row)
    assert set(LOCALES) <= set(names)
    assert all(names[locale].strip() for locale in LOCALES)
    assert names["original"] == merchant.local_name


def _localized(merchant: Any) -> dict[str, str]:
    return merchant_names(
        FoodMerchant(
            slug=merchant.slug,
            destination_id=merchant.destination_id,
            country_code=destination_country_code(merchant.destination_id) or "",
            name=merchant.display_name,
            local_name=merchant.local_name,
            names_json=merchant.chinese_label,
        )
    )


def test_english_readers_get_the_latin_sign_when_the_row_carries_one() -> None:
    # name_zh is what Chinese travel writing calls the place. Serving it as the English name
    # gave an English reader a string that is neither on the door nor findable in a map.
    merchant = parse_merchant(_row(name_en="Dandelion Chocolate"), row=1)
    assert merchant.display_name == "Dandelion Chocolate"
    assert _localized(merchant)["en"] == "Dandelion Chocolate"


def test_a_row_without_an_english_name_is_unchanged() -> None:
    merchant = parse_merchant(_row(), row=1)
    assert merchant.display_name == merchant.name
    assert merchant.chinese_label == {}


def test_a_chinese_reader_of_a_japanese_shop_still_sees_the_signboard() -> None:
    # merchant_names gives Chinese locales the original script for Japan, and a stored label
    # would override that. Writing one here would swap a Chinese reader from the signboard to
    # a Chinese rendering of it — a change this was never meant to make.
    merchant = parse_merchant(_row(name_en="Dandelion Chocolate"), row=1)
    assert merchant.chinese_label == {}
    assert _localized(merchant)["zh-TW"] == merchant.local_name


def test_a_chinese_reader_of_a_bangkok_shop_keeps_the_chinese_name() -> None:
    # Thailand has no such default, so without storing it the Chinese name would be lost the
    # moment `name` becomes Latin.
    merchant = parse_merchant(
        _row(
            destination="bangkok",
            district_key="talat-noi",
            slug="bangkok-charmgang",
            name_zh="咖哩碗泰菜館",
            name_en="Charmgang",
            local_name="ชามแกง Charmgang",
            category_slugs=["curry", "home-style"],
        ),
        row=1,
    )
    assert merchant.chinese_label == {"zh-TW": "咖哩碗泰菜館"}
    names = _localized(merchant)
    assert names["en"] == "Charmgang"
    assert names["zh-TW"] == "咖哩碗泰菜館"


def test_every_english_name_in_the_committed_batch_is_taken_from_the_row_itself() -> None:
    """No hand-written transliterations: the ticket forbids inventing romanisations."""

    for merchant in load_trend_merchants(DEFAULT_FILE):
        if not merchant.name_en:
            continue
        haystack = f"{merchant.name} {merchant.local_name}".casefold()
        assert merchant.name_en.casefold() in haystack, merchant.slug
