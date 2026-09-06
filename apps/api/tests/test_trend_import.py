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
    plan_english_name_backfill,
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


def test_the_english_label_is_the_shops_own_not_the_chinese_rendering() -> None:
    """`FoodMerchant.name` is the English label, and the sweep only collected Chinese."""
    chinese_only = parse_merchant(_row(), row=1)
    assert chinese_only.english_name is None
    # No checked English name means the Chinese one stays: a machine transliteration of a
    # shop name is worse than something a reader can paste into a map.
    assert chinese_only.display_name == chinese_only.name

    thai = parse_merchant(
        _row(
            destination="bangkok",
            district_key="talat-noi",
            slug="bangkok-charmgang",
            name_zh="咖哩碗泰菜館",
            name_en="Charmgang",
            local_name="ชามแกง Charmgang",
            address_local="14 ซอยเจริญกรุง 35",
            source_url="https://www.instagram.com/charmgangcurryshop/",
            source_title="charmgangcurryshop | Instagram",
            category_slugs=["curry"],
        ),
        row=2,
    )
    assert thai.display_name == "Charmgang"
    # Thai has no site locale of its own, so the Chinese name would be lost without this.
    assert thai.stored_names("TH") == {"zh-TW": "咖哩碗泰菜館"}
    # Japan and Taiwan write in a script the site publishes, so merchant_names already
    # gives a Chinese reader the original and nothing needs storing.
    assert thai.stored_names("JP") is None
    assert thai.stored_names("TW") is None


def test_a_name_that_is_not_a_latin_label_is_refused() -> None:
    with pytest.raises(TrendImportError) as excinfo:
        parse_merchant(_row(name_en="咖哩碗泰菜館"), row=7)
    assert "row 7" in str(excinfo.value) and "name_en" in str(excinfo.value)
    # An accent is not a reason to refuse: oHacorté is the shop's own spelling.
    assert parse_merchant(_row(name_en="oHacorté Minatogawa"), row=8).english_name


def test_every_english_label_in_the_committed_batch_is_latin_and_not_the_chinese_one() -> None:
    rows = json.loads(DEFAULT_FILE.read_text(encoding="utf-8"))
    labelled = [row for row in rows if row.get("name_en")]
    assert labelled, "the batch has no English labels at all"
    for row in labelled:
        assert row["name_en"] != row["name_zh"], row["slug"]
    merchants = {merchant.slug: merchant for merchant in parse_merchants(rows)}
    assert merchants["bangkok-charmgang"].display_name == "Charmgang"
    assert merchants["tokyo-fuglen-tokyo"].display_name == "FUGLEN TOKYO"


def _imported(merchant: Any, name: str | None = None) -> FoodMerchant:
    """A row as the importer first wrote it, before name_en existed."""

    return FoodMerchant(
        slug=merchant.slug,
        destination_id=merchant.destination_id,
        country_code=destination_country_code(merchant.destination_id) or "",
        name=name if name is not None else merchant.name,
        local_name=merchant.local_name,
        names_json={},
    )


def test_the_backfill_reaches_rows_the_importer_will_not_touch() -> None:
    # The importer skips a slug it has seen and never merges into it, so adding name_en to
    # the file leaves the already-imported rows — the ones a reader sees — untouched.
    merchant = parse_merchant(_row(name_en="Dandelion Chocolate"), row=1)
    merchants = {merchant.slug: merchant}
    changed, left = plan_english_name_backfill([_imported(merchant)], merchants)
    assert changed == [
        {
            "slug": merchant.slug,
            "from": "Dandelion Chocolate 藏前工廠咖啡館",
            "to": "Dandelion Chocolate",
        }
    ]
    assert left == []


def test_the_backfill_leaves_a_row_an_administrator_renamed() -> None:
    merchant = parse_merchant(_row(name_en="Dandelion Chocolate"), row=1)
    merchants = {merchant.slug: merchant}
    row = _imported(merchant, name="Dandelion Chocolate Kuramae")
    changed, left = plan_english_name_backfill([row], merchants)
    assert changed == []
    assert left == [
        {
            "slug": merchant.slug,
            "name": "Dandelion Chocolate Kuramae",
            "reason": "renamed since import",
        }
    ]


def test_running_the_backfill_twice_changes_nothing_the_second_time() -> None:
    merchant = parse_merchant(_row(name_en="Dandelion Chocolate"), row=1)
    merchants = {merchant.slug: merchant}
    already = _imported(merchant, name=merchant.display_name)
    changed, left = plan_english_name_backfill([already], merchants)
    assert changed == []
    # And it says why, rather than calling it a rename an operator would go looking for.
    assert left == [
        {
            "slug": merchant.slug,
            "name": "Dandelion Chocolate",
            "reason": "already the English name",
        }
    ]


def test_a_row_with_no_english_name_in_the_file_is_never_touched() -> None:
    merchant = parse_merchant(_row(), row=1)
    changed, left = plan_english_name_backfill([_imported(merchant)], {merchant.slug: merchant})
    assert changed == []
    assert left == []
