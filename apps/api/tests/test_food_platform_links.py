import runpy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
from alembic import context
from alembic.migration import MigrationContext
from alembic.operations import Operations
from sqlalchemy import inspect, select
from sqlalchemy.ext.asyncio import create_async_engine
from test_discovery_flow import block_detail_provider_clients, seed_reservation_merchant
from test_travel_discovery import harness as harness

from app.foods.admin_router import (
    MerchantPlatformLinkPayload,
    get_merchant_platform_links,
    update_merchant_platform_link,
)
from app.foods.merchant_catalog import MERCHANT_SEEDS
from app.foods.platform_link_catalog import PLATFORM_LINK_AUDIT_SEEDS
from app.foods.platform_links import (
    PLATFORMS_BY_COUNTRY,
    PLATFORMS_BY_PROVIDER,
    available_platforms,
    expected_platform,
    platform_url_identity,
    platform_url_language,
    serialize_reservation_link,
    validate_localized_platform_urls,
    validate_platform_url,
)
from app.models import (
    AdminAuditLog,
    FoodCategory,
    FoodMerchant,
    FoodMerchantCategory,
    FoodMerchantFood,
    FoodMerchantPlatformLink,
    FoodMerchantSource,
    User,
)
from app.problems import AppError


@pytest.mark.parametrize(
    ("country", "provider"),
    [
        ("JP", "tablecheck"),
        ("KR", "catchtable_global"),
        ("TW", "eztable"),
        ("SG", "chope"),
        ("HK", "openrice"),
        ("TH", "hungry_hub"),
        ("VN", "pasgo"),
    ],
)
def test_country_keeps_recommended_reservation_platform(country: str, provider: str) -> None:
    assert expected_platform(country).provider == provider


@pytest.mark.parametrize(
    ("provider", "url"),
    [
        ("tablecheck", "https://www.tablecheck.com/en/shops/sushi-sakai/reserve"),
        ("catchtable_global", "https://www.catchtable.net/shop/example"),
        ("eztable", "https://www.eztable.com/restaurant/example"),
        ("chope", "https://www.chope.co/singapore-restaurants/restaurant/song-fa"),
        ("openrice", "https://www.openrice.com/en/hongkong/p-yat-lok-p23206360"),
        ("hungry_hub", "https://web.hungryhub.com/en/restaurants/krua-apsorn/web"),
        ("pasgo", "https://pasgo.vn/nha-hang/example"),
        ("tablecheck", "https://www.tablecheck.com/shops/sushi-sakai/reserve"),
        ("tablecheck", "https://www.tablecheck.com/zh-TW/shin-yeh-main-restaurant/reserve/message"),
        ("tablecheck", "https://www.tablecheck.com/zh-TW/yuwaeru-honten/reserve/landing"),
        ("inline", "https://inline.app/booking/-Np4PbmnyNDdeWIZzRem:inline-live-3/"
         "-Np4PbzfZuNZ-afLExLd?language=zh-tw"),
        ("maifood", "https://reservation.maifood.com.tw/qingtian76/qingtian76_1"),
        ("sevenrooms", "https://www.sevenrooms.com/reservations/palmbeach"),
        ("sevenrooms", "https://www.sevenrooms.com/explore/candlenutsingapore/"
         "reservations/create/search"),
        ("ikyu", "https://restaurant.ikyu.com/107953"),
        ("myconcierge", "https://myconciergejapan.com/restaurants/ginza-kyubey"),
    ],
)
def test_exact_merchant_urls_are_accepted(provider: str, url: str) -> None:
    assert validate_platform_url(provider, url) == url


@pytest.mark.parametrize("identifier", ["yosukgung.kr", "normal.brunch", "Venue-1.a_b.c2"])
@pytest.mark.parametrize("route", ["shop", "restaurant", "restaurants"])
def test_catchtable_accepts_literal_dotted_venue_ids(identifier: str, route: str) -> None:
    url = f"https://www.catchtable.net/{route}/{identifier}"
    assert validate_platform_url("catchtable_global", url) == url
    assert platform_url_identity("catchtable_global", url) == identifier
    assert platform_url_language("catchtable_global", url) == ""


def test_catchtable_accepts_an_underscore_only_dot_segment() -> None:
    """Seoul 하니칼국수 is `hani._.noodle`; only the whole ID must start alphanumeric."""
    url = "https://www.catchtable.net/shop/hani._.noodle"
    assert validate_platform_url("catchtable_global", url) == url
    assert platform_url_identity("catchtable_global", url) == "hani._.noodle"


@pytest.mark.parametrize(
    ("provider", "url", "identity", "language"),
    [
        ("tabelog", "https://tabelog.com/osaka/A2701/A270202/27001289", "27001289", "ja"),
        ("tabelog", "https://tabelog.com/en/tokyo/A1301/A130101/13226719", "13226719", "en"),
        ("tabelog", "https://tabelog.com/tw/tokyo/A1301/A130101/13226719", "13226719", "zh-TW"),
        ("tabelog", "https://tabelog.com/cn/tokyo/A1301/A130101/13226719", "13226719", "zh-CN"),
        ("tabelog", "https://tabelog.com/kr/tokyo/A1301/A130101/13226719", "13226719", "ko"),
        ("tabelog", "https://tabelog.com/th/tokyo/A1301/A130101/13226719", "13226719", "th"),
        ("hotpepper", "https://www.hotpepper.jp/strJ003560255", "j003560255", "ja"),
        ("gurunavi", "https://r.gnavi.co.jp/k001100", "k001100", "ja"),
        ("gurunavi", "https://r.gnavi.co.jp/nmwubfx70000", "nmwubfx70000", "ja"),
        ("gurunavi", "https://gurunavi.com/en/k001100/rst", "k001100", "en"),
        ("gurunavi", "https://gurunavi.com/zh-hant/k001100/rst", "k001100", "zh-TW"),
        ("gurunavi", "https://gurunavi.com/zh-hans/k001100/rst", "k001100", "zh-CN"),
        (
            "autoreserve",
            "https://autoreserve.com/ja/restaurants/91FxEE6JLr2HE2owrKVL",
            "91FxEE6JLr2HE2owrKVL",
            "ja",
        ),
        (
            "autoreserve",
            "https://autoreserve.com/zh-tw/restaurants/91FxEE6JLr2HE2owrKVL",
            "91FxEE6JLr2HE2owrKVL",
            "zh-TW",
        ),
        ("naver_booking", "https://booking.naver.com/booking/13/bizes/210459", "210459", "ko"),
        ("naver_booking", "https://m.booking.naver.com/booking/13/bizes/210459", "210459", "ko"),
    ],
)
def test_japan_and_korea_shop_pages_are_accepted(
    provider: str, url: str, identity: str, language: str
) -> None:
    assert validate_platform_url(provider, url) == url
    assert validate_platform_url(provider, f"{url}/") == url
    assert platform_url_identity(provider, url) == identity
    assert platform_url_language(provider, url) == language


@pytest.mark.parametrize(
    ("provider", "url"),
    [
        # Area, ranking and review routes are not one shop.
        ("tabelog", "https://tabelog.com/osaka/A2701/A270202"),
        ("tabelog", "https://tabelog.com/tokyo/rstLst/RC0101"),
        ("tabelog", "https://tabelog.com/en/tokyo/A1301/A130101/13226719/dtlrvwlst"),
        ("tabelog", "https://tabelog.com/en/tokyo/A1301/A130101/1322671a"),
        # Tabelog has no Hong Kong directory; a site locale is not a Tabelog locale.
        ("tabelog", "https://tabelog.com/hk/tokyo/A1301/A130101/13226719"),
        ("tabelog", "https://tabelog.com/zh-tw/tokyo/A1301/A130101/13226719"),
        ("hotpepper", "https://www.hotpepper.jp/strJ00356025"),
        ("hotpepper", "https://www.hotpepper.jp/strJ003560255/yoyaku"),
        ("hotpepper", "https://www.hotpepper.jp/fukuoka"),
        ("gurunavi", "https://r.gnavi.co.jp/area"),
        ("gurunavi", "https://r.gnavi.co.jp/plan/r6pyrfvf0000/plan-reserve"),
        # Each Gurunavi route belongs to one host only.
        ("gurunavi", "https://r.gnavi.co.jp/en/k001100/rst"),
        ("gurunavi", "https://gurunavi.com/k001100/rst"),
        ("gurunavi", "https://gurunavi.com/en/k001100"),
        ("autoreserve", "https://autoreserve.com/ja/restaurants/91FxEE6JLr2HE2owrKV"),
        ("autoreserve", "https://autoreserve.com/restaurants/91FxEE6JLr2HE2owrKVL"),
        ("autoreserve", "https://autoreserve.com/ja/areas/osaka"),
        ("naver_booking", "https://booking.naver.com/booking/13/bizes"),
        ("naver_booking", "https://booking.naver.com/booking/13/bizes/210459/items/4567"),
        # Naver's map entry is a place page, not the reservation platform.
        ("naver_booking", "https://map.naver.com/p/entry/place/210459"),
    ],
)
def test_japan_and_korea_non_shop_pages_are_rejected(provider: str, url: str) -> None:
    with pytest.raises(ValueError):
        validate_platform_url(provider, url)


@pytest.mark.parametrize(
    ("locale", "directory"),
    [("ja", ""), ("en", "en/"), ("zh-TW", "tw/"), ("zh-CN", "cn/"), ("ko", "kr/")],
)
def test_tabelog_language_directories_map_onto_site_locales(
    locale: str, directory: str
) -> None:
    canonical = "https://tabelog.com/osaka/A2701/A270202/27001289"
    localized = f"https://tabelog.com/{directory}osaka/A2701/A270202/27001289"
    assert validate_localized_platform_urls("tabelog", canonical, {locale: localized}) == {
        locale: localized
    }


def test_tabelog_language_directory_must_match_its_locale() -> None:
    canonical = "https://tabelog.com/osaka/A2701/A270202/27001289"
    with pytest.raises(ValueError, match="language does not match"):
        validate_localized_platform_urls(
            "tabelog", canonical, {"ko": "https://tabelog.com/tw/osaka/A2701/A270202/27001289"}
        )
    with pytest.raises(ValueError, match="different merchant or branch"):
        validate_localized_platform_urls(
            "tabelog", canonical, {"en": "https://tabelog.com/en/osaka/A2701/A270202/27001290"}
        )


@pytest.mark.parametrize("locale", ["zh-TW", "zh-CN", "en", "ja", "ko"])
def test_catchtable_dotted_identity_matches_reviewed_locale_aliases(locale: str) -> None:
    canonical = "https://www.catchtable.net/shop/yosukgung.kr"
    localized = f"https://catchtable.net/{locale}/restaurants/yosukgung.kr"
    assert platform_url_identity("catchtable_global", canonical) == platform_url_identity(
        "catchtable_global", localized
    )
    assert validate_localized_platform_urls(
        "catchtable_global", canonical, {locale: localized}
    ) == {locale: localized}
    assert platform_url_language("catchtable_global", localized) == locale


@pytest.mark.parametrize("identifier", ["yosukgungkr", "yosukgung-kr", "yosukgung.kr2",
                                        "yosukgung.kr.branch", "Yosukgung.kr"])
def test_catchtable_dotted_ids_remain_distinct(identifier: str) -> None:
    canonical = "https://www.catchtable.net/shop/yosukgung.kr"
    other = f"https://www.catchtable.net/ja/shop/{identifier}"
    assert platform_url_identity("catchtable_global", canonical) != platform_url_identity(
        "catchtable_global", other
    )
    with pytest.raises(ValueError, match="different merchant or branch"):
        validate_localized_platform_urls("catchtable_global", canonical, {"ja": other})


@pytest.mark.parametrize("url", [
    "https://www.catchtable.net/shop/.yosukgung.kr",
    "https://www.catchtable.net/shop/_yosukgung.kr",
    "https://www.catchtable.net/shop/yosukgung.kr.",
    "https://www.catchtable.net/shop/yosukgung..kr",
    "https://www.catchtable.net/shop/yosukgung.-kr",
    "https://www.catchtable.net/shop/yosukgung%2ekr",
    "https://www.catchtable.net/shop/yosukgung%2Ekr",
    "https://www.catchtable.net/shop/yosukgung%252ekr",
    "https://www.catchtable.net/shop/yosukgung.kr%2fother",
    "https://www.catchtable.net/shop/yosukgung.kr%5cother",
    "https://www.catchtable.net/shop/yosukgung.kr%0a",
    "https://www.catchtable.net/shop/yosukgung.kr%C2%85",
    "https://www.catchtable.net/shop/yosukgung.kr\\other",
    "https://www.catchtable.net/shop/yosukgung.kr\n",
    "https://www.catchtable.net/shop/../yosukgung.kr",
    "https://www.catchtable.net/shop/yosukgung.kr/../other",
    "https://www.catchtable.net/shop/%2e%2e/yosukgung.kr",
    "https://www.catchtable.net/shop/yosukgung.\u212ar",
    "https://www.catchtable.net/shop/yosukgung.kr?redirect=https://evil.test",
    "https://www.catchtable.net/shop/yosukgung.kr?language=ja",
    "https://www.catchtable.net/shop/yosukgung.kr?",
    "https://www.catchtable.net/shop/yosukgung.kr#other",
    "http://www.catchtable.net/shop/yosukgung.kr",
    "https://www.catchtable.net.evil.test/shop/yosukgung.kr",
    "https://www.catchtable.net@evil.test/shop/yosukgung.kr",
    "https://user@www.catchtable.net/shop/yosukgung.kr",
    "https://www.catchtable.net:443/shop/yosukgung.kr",
    "https://www.catchtable.net./shop/yosukgung.kr",
    "https://127.0.0.1/shop/yosukgung.kr",
    "https://localhost/shop/yosukgung.kr",
])
def test_catchtable_dotted_ids_preserve_security_guards(url: str) -> None:
    with pytest.raises(ValueError):
        validate_platform_url("catchtable_global", url)


@pytest.mark.parametrize("provider,url", [
    ("tablecheck", "https://www.tablecheck.com/en/shops/normal.brunch/reserve"),
    ("eztable", "https://www.eztable.com/restaurant/normal.brunch"),
    ("chope", "https://www.chope.co/singapore-restaurants/restaurant/normal.brunch"),
    ("openrice", "https://www.openrice.com/en/hongkong/r-normal.brunch-r123"),
    ("hungry_hub", "https://web.hungryhub.com/en/restaurants/normal.brunch/web"),
    ("pasgo", "https://pasgo.vn/nha-hang/normal.brunch"),
    ("inline", "https://inline.app/booking/chain:inline-live-3/normal.brunch"),
    ("maifood", "https://reservation.maifood.com.tw/brand/normal.brunch"),
    ("sevenrooms", "https://www.sevenrooms.com/reservations/normal.brunch"),
    ("ikyu", "https://restaurant.ikyu.com/107.953"),
    ("myconcierge", "https://myconciergejapan.com/restaurants/normal.brunch"),
])
def test_dotted_catchtable_ids_do_not_widen_other_providers(provider: str, url: str) -> None:
    with pytest.raises(ValueError):
        validate_platform_url(provider, url)


@pytest.mark.parametrize(
    ("provider", "url"),
    [
        ("tablecheck", "https://www.tablecheck.com/en/japan"),
        ("catchtable_global", "https://www.catchtable.net/"),
        ("chope", "https://www.chope.co/singapore-restaurants/list_of_restaurants"),
        ("openrice", "https://www.openrice.com/en/hongkong/restaurants"),
        ("pasgo", "https://pasgo.vn/"),
    ],
)
def test_home_search_and_list_pages_are_rejected(provider: str, url: str) -> None:
    with pytest.raises(ValueError):
        validate_platform_url(provider, url)


def test_every_curated_merchant_has_a_conservative_audit_result() -> None:
    assert len(MERCHANT_SEEDS) == 173
    assert len(PLATFORM_LINK_AUDIT_SEEDS) == len(MERCHANT_SEEDS)
    assert len({item.merchant_slug for item in PLATFORM_LINK_AUDIT_SEEDS}) == 173
    merchants = {item.slug: item for item in MERCHANT_SEEDS}
    for audit in PLATFORM_LINK_AUDIT_SEEDS:
        assert audit.status in {"verified", "not_found", "ambiguous", "disabled"}
        assert audit.provider == PLATFORMS_BY_COUNTRY[
            merchants[audit.merchant_slug].country_code
        ].provider
        if audit.status == "verified":
            assert audit.canonical_url
            validate_platform_url(audit.provider, audit.canonical_url)


def test_public_link_requires_verified_status_and_allows_cross_country_provider() -> None:
    row = FoodMerchantPlatformLink(
        provider="catchtable_global",
        canonical_url="https://www.catchtable.net/shop/example",
        localized_urls_json={},
        status="verified",
        checked_at=datetime(2026, 9, 8, tzinfo=UTC),
    )
    public = serialize_reservation_link(row, country_code="KR", locale="zh-TW")
    assert public == {
        "provider": "catchtable_global",
        "label": "Catchtable Global",
        "url": "https://www.catchtable.net/shop/example",
        "verified_at": "2026-09-08T00:00:00+00:00",
        "language_code": "",
    }
    row.status = "ambiguous"
    assert serialize_reservation_link(row, country_code="KR", locale="zh-TW") is None
    row.status = "verified"
    assert serialize_reservation_link(row, country_code="JP", locale="zh-TW") == public


def test_localized_url_is_selected_only_when_reviewed_on_the_same_row() -> None:
    row = FoodMerchantPlatformLink(
        provider="tablecheck",
        canonical_url="https://www.tablecheck.com/en/shops/sushi-sakai/reserve",
        localized_urls_json={
            "ja": "https://www.tablecheck.com/ja/shops/sushi-sakai/reserve"
        },
        status="verified",
        checked_at=datetime(2026, 9, 8, tzinfo=UTC),
    )
    public = serialize_reservation_link(row, country_code="JP", locale="ja")
    assert public is not None
    assert public["url"] == "https://www.tablecheck.com/ja/shops/sushi-sakai/reserve"
    assert public["language_code"] == "ja"


def test_every_reviewed_platform_is_available_independent_of_country() -> None:
    assert set(PLATFORMS_BY_PROVIDER) == {
        "tablecheck", "catchtable_global", "eztable", "chope", "openrice", "hungry_hub",
        "pasgo", "inline", "maifood", "sevenrooms", "ikyu", "myconcierge",
        "tabelog", "hotpepper", "gurunavi", "autoreserve", "naver_booking",
    }
    assert [item["provider"] for item in available_platforms()] == sorted(PLATFORMS_BY_PROVIDER)


@pytest.mark.parametrize("url", [
    "https://www.tablecheck.com.evil.test/en/shops/branch/reserve",
    "https://user:password@www.tablecheck.com/en/shops/branch/reserve",
    "https://www.tablecheck.com:443/en/shops/branch/reserve",
    "https://www.tablecheck.com:8443/en/shops/branch/reserve",
    "https://127.0.0.1/en/shops/branch/reserve",
    "https://localhost/en/shops/branch/reserve",
    "https://www.tablecheck.com/en/shops/branch/reserve?redirect=https://evil.test",
    "https://www.tablecheck.com/en/shops/branch/reserve?venue=other",
    "https://www.tablecheck.com/en/shops/branch/reserve#https://evil.test",
    "https://www.tablecheck.com/en/shops/branch/reserve/extra",
    "https://www.tablecheck.com/prefix/en/shops/branch/reserve",
    "https://www.tablecheck.com/en/shops/branch%2fother/reserve",
    "https://www.tablecheck.com/en/shops/branch%5cother/reserve",
    "https://www.tablecheck.com/en/shops/branch%252fother/reserve",
    "https://www.tablecheck.com/en/shops/branch%0aother/reserve",
    "https://www.tablecheck.com/en/shops/branch\\other/reserve",
    "https://www.tablecheck.com/en/shops/branch\n/reserve",
    "https://www.tablecheck.com/en/shops/../branch/reserve",
    "https://www.tablecheck.com/en/shops/%2e%2e/branch/reserve",
    "https://www.tablecheck.com/en//shops/branch/reserve",
    "https://www.tablecheck.com/en/shops/branch/reserve//",
    "https://www.tablecheck.com/en/shops/search/reserve",
])
def test_malicious_and_non_branch_urls_fail_closed(url: str) -> None:
    with pytest.raises(ValueError):
        validate_platform_url("tablecheck", url)


@pytest.mark.parametrize("provider,url", [
    ("inline", "https://inline.app/booking/chain:inline-live-3/branch?redirect=https://evil.test"),
    ("inline", "https://inline.app/booking/chain:inline-live-3/branch?language=ja&language=en"),
    ("inline", "https://inline.app/booking/chain:inline-live-3/branch?LANGUAGE=en"),
    ("inline", "https://inline.app/booking/chain:inline-live-3"),
    ("maifood", "https://reservation.maifood.com.tw/qingtian76/branches"),
    ("sevenrooms", "https://www.sevenrooms.com/explore/branch/reservations/create"),
    ("ikyu", "https://restaurant.ikyu.com/search"),
    ("myconcierge", "https://myconciergejapan.com/restaurants"),
])
def test_new_platforms_reject_search_and_unsafe_parameters(provider: str, url: str) -> None:
    with pytest.raises(ValueError):
        validate_platform_url(provider, url)


@pytest.mark.parametrize("provider,canonical,localized", [
    ("tablecheck", "https://www.tablecheck.com/en/shops/branch/reserve",
     {"ja": "https://www.tablecheck.com/ja/shops/other-branch/reserve"}),
    ("tablecheck", "https://www.tablecheck.com/en/shops/branch/reserve",
     {"ja": "https://www.tablecheck.com/zh-TW/branch/reserve/message"}),
    ("tablecheck", "https://www.tablecheck.com/en/shops/branch/reserve",
     {"zh-TW": "https://www.tablecheck.com/%6aa/shops/branch/reserve"}),
    ("inline", "https://inline.app/booking/chain:inline-live-3/branch?language=en",
     {"ja": "https://inline.app/booking/chain:inline-live-3/other?language=ja"}),
    ("inline", "https://inline.app/booking/chain:inline-live-3/branch?language=en",
     {"ja": "https://inline.app/booking/chain:inline-live-3/branch?language=zh-tw"}),
])
def test_payload_rejects_localized_branch_and_language_mismatch(
    provider: str, canonical: str, localized: dict[str, str]
) -> None:
    with pytest.raises(ValueError):
        MerchantPlatformLinkPayload(
            provider=provider, status="verified", canonical_url=canonical,
            localized_urls=localized,
        )


@pytest.mark.parametrize("provider,first,second", [
    ("tablecheck", "https://www.tablecheck.com/en/shops/branch/reserve",
     "https://tablecheck.com/zh-TW/branch/reserve/message"),
    ("sevenrooms", "https://sevenrooms.com/reservations/branch",
     "https://www.sevenrooms.com/explore/branch/reservations/create/search"),
    ("openrice", "https://www.openrice.com/en/hongkong/r-name-r123",
     "https://openrice.com/zh-HK/hongkong/r-餐廳-r123"),
])
def test_identity_matches_route_host_and_locale_aliases(
    provider: str, first: str, second: str
) -> None:
    assert platform_url_identity(provider, first) == platform_url_identity(provider, second)


@pytest.mark.parametrize("provider,url,language", [
    ("tablecheck", "https://www.tablecheck.com/zh-TW/branch/reserve/message", "zh-TW"),
    ("tablecheck", "https://www.tablecheck.com/shops/branch/reserve", ""),
    ("tablecheck", "https://www.tablecheck.com/%6aa/shops/branch/reserve", "ja"),
    ("inline", "https://inline.app/booking/chain:inline-live-3/branch?language=zh-tw", "zh-TW"),
    ("inline", "https://inline.app/booking/chain:inline-live-3/branch", ""),
    ("ikyu", "https://restaurant.ikyu.com/107953", ""),
])
def test_only_explicit_url_language_is_reported(provider: str, url: str, language: str) -> None:
    assert platform_url_language(provider, url) == language


def test_invalid_legacy_localized_metadata_falls_back_to_reviewed_canonical() -> None:
    canonical = "https://www.tablecheck.com/zh-TW/branch/reserve/message"
    row = FoodMerchantPlatformLink(
        provider="tablecheck", canonical_url=canonical, status="verified",
        localized_urls_json={"ja": "https://www.tablecheck.com/ja/other/reserve/message"},
        checked_at=datetime(2026, 9, 8, tzinfo=UTC),
    )
    public = serialize_reservation_link(row, country_code="TW", locale="ja")
    assert public is not None
    assert public["url"] == canonical and public["language_code"] == "zh-TW"


@pytest.mark.asyncio
@pytest.mark.parametrize("provider,url", [
    ("inline", "https://inline.app/booking/chain:inline-live-3/branch?language=zh-tw"),
    ("catchtable_global", "https://www.catchtable.net/zh-TW/shop/yosukgung.kr"),
])
async def test_platform_save_preserves_merchant_relations_and_other_platform(
    harness: Any, provider: str, url: str,
) -> None:
    _, factory, users, _, _ = harness
    _, merchant = await seed_reservation_merchant(factory)
    async with factory() as session:
        admin = await session.get(User, users[0])
        assert admin is not None
        row = await session.scalar(select(FoodMerchantPlatformLink))
        assert row is not None
        category = FoodCategory(slug="preserve-category", names_json={"en": "Preserve"})
        session.add(category)
        await session.flush()
        session.add(FoodMerchantCategory(
            merchant_id=merchant.id, category_id=category.id, is_primary=True,
        ))
        await session.commit()
        existing_platform = dict((await session.execute(
            select(FoodMerchantPlatformLink.__table__)
        )).mappings().one())
        models = (FoodMerchant, FoodMerchantFood, FoodMerchantSource, FoodMerchantCategory)
        before = [
            [dict(item) for item in (await session.execute(select(model.__table__))).mappings()]
            for model in models
        ]
        created = await update_merchant_platform_link(
            merchant.id,
            MerchantPlatformLinkPayload(
                provider=provider, status="verified", expected_checked_at=None,
                canonical_url=url,
                review_note="Only this platform changed",
            ), admin, session,
        )
        assert [item["provider"] for item in created["platform_links"]] == [provider, "tablecheck"]
        assert created["platform_links"][0]["canonical_url"] == url
        assert created["platform_link"]["provider"] == "tablecheck"
        assert created["platform_links"][0]["country_mismatch"] is False
        assert before == [
            [dict(item) for item in (await session.execute(select(model.__table__))).mappings()]
            for model in models
        ]
        assert existing_platform == dict((await session.execute(
            select(FoodMerchantPlatformLink.__table__).where(
                FoodMerchantPlatformLink.provider == "tablecheck"
            )
        )).mappings().one())
        audit = (await session.scalars(select(AdminAuditLog))).one()
        assert audit.actor_user_id == admin.id
        assert audit.metadata_json["provider"] == provider
        refreshed = await get_merchant_platform_links(merchant.id, admin, session)
        assert refreshed["platform_links"] == created["platform_links"]
        assert len(refreshed["available_platforms"]) == len(PLATFORMS_BY_PROVIDER)


@pytest.mark.asyncio
@pytest.mark.parametrize("status", ["verified", "ambiguous", "disabled", "not_found"])
async def test_dotted_catchtable_public_detail_requires_review_without_network(
    harness: Any, monkeypatch: pytest.MonkeyPatch, status: str,
) -> None:
    client, factory, _, _, _ = harness
    url = "https://www.catchtable.net/zh-TW/shop/yosukgung.kr"
    _, merchant = await seed_reservation_merchant(
        factory, country="KR", city="seoul", provider="catchtable_global",
        canonical_url=url, status=status,
    )
    block_detail_provider_clients(monkeypatch)
    for locale in ("zh-TW", "zh-CN", "en", "ja", "ko"):
        response = await client.get(
            f"/api/v1/discovery/content/merchant/{merchant.id}",
            headers={"X-Travel-Locale": locale},
        )
        assert response.status_code == 200, response.text
        links = response.json()["detail"]["merchants"][0]["reservation_links"]
        if status == "verified":
            assert len(links) == 1
            assert links[0]["url"] == url  # No invented locale alternate.
            assert links[0]["language_code"] == "zh-TW"
        else:
            assert links == []
        assert "Private branch audit note" not in response.text


@pytest.mark.asyncio
async def test_platform_checked_at_guard_rejects_stale_update_and_create(harness: Any) -> None:
    _, factory, users, _, _ = harness
    _, merchant = await seed_reservation_merchant(factory)
    async with factory() as session:
        admin = await session.get(User, users[0])
        assert admin is not None
        row = await session.scalar(select(FoodMerchantPlatformLink))
        assert row is not None
        checked_at = row.checked_at.replace(tzinfo=UTC)
        payload = MerchantPlatformLinkPayload(
            provider="tablecheck", status="disabled", expected_checked_at=checked_at,
            review_note="Independent review",
        )
        result = await update_merchant_platform_link(merchant.id, payload, admin, session)
        checked_after = result["platform_link"]["checked_at"]
        for expected in (checked_at, None):
            with pytest.raises(AppError) as conflict:
                await update_merchant_platform_link(
                    merchant.id,
                    MerchantPlatformLinkPayload(
                        provider="tablecheck", status="not_found", expected_checked_at=expected,
                    ), admin, session,
                )
            assert conflict.value.status == 409
            assert conflict.value.code == "reservation_platform_version_conflict"
        await session.refresh(row)
        assert row.status == "disabled"
        assert row.checked_at.replace(tzinfo=UTC) == checked_after.replace(tzinfo=UTC)
        assert len((await session.scalars(select(AdminAuditLog))).all()) == 1
        # Omitted guard remains compatible with older clients.
        legacy = await update_merchant_platform_link(
            merchant.id, MerchantPlatformLinkPayload(provider="tablecheck", status="not_found"),
            admin, session,
        )
        assert legacy["platform_link"]["status"] == "not_found"


@pytest.mark.asyncio
async def test_platform_identity_alias_cannot_be_assigned_to_another_merchant(harness: Any) -> None:
    _, factory, users, _, _ = harness
    _, first = await seed_reservation_merchant(factory)
    _, second = await seed_reservation_merchant(
        factory, canonical_url="https://www.tablecheck.com/en/shops/second-fixture/reserve"
    )
    assert first.id != second.id
    async with factory() as session:
        admin = await session.get(User, users[0])
        assert admin is not None
        with pytest.raises(AppError) as conflict:
            await update_merchant_platform_link(
                second.id, MerchantPlatformLinkPayload(
                    provider="tablecheck", status="verified",
                    canonical_url="https://tablecheck.com/ja/mokaair-fixture/reserve/message",
                ), admin, session,
            )
        assert conflict.value.status == 409
        assert conflict.value.code == "reservation_platform_url_conflict"
        assert not (await session.scalars(select(AdminAuditLog))).all()


@pytest.mark.asyncio
async def test_migration_is_idempotent_and_round_trips() -> None:
    migration = runpy.run_path(
        str(Path("migrations/versions/0062_food_merchant_platform_links.py"))
    )
    engine = create_async_engine("sqlite+aiosqlite://")

    def run(connection: Any) -> None:
        with (
            Operations.context(MigrationContext.configure(connection)),
            pytest.MonkeyPatch.context() as patch,
        ):
            patch.setattr(context, "is_offline_mode", lambda: False)
            migration["upgrade"]()
            migration["upgrade"]()
            columns = {
                item["name"]
                for item in inspect(connection).get_columns("food_merchant_platform_links")
            }
            assert columns == {
                column.name for column in FoodMerchantPlatformLink.__table__.columns
            }
            migration["downgrade"]()
            assert "food_merchant_platform_links" not in inspect(connection).get_table_names()

    async with engine.begin() as connection:
        await connection.run_sync(run)
    await engine.dispose()
