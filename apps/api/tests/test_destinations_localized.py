"""The destination catalog answers in the reader's locale."""

import httpx
import pytest

from app.destinations import localized
from app.destinations.catalog import DESTINATIONS, destination_for_id
from app.main import app


def test_every_destination_and_country_is_translated() -> None:
    assert localized.validate_localized_catalog() == []


def test_helpers_keep_the_catalog_text_for_zh_tw() -> None:
    tokyo = destination_for_id("tokyo")
    assert tokyo is not None
    assert localized.city_name(tokyo, "zh-TW") == "東京"
    assert localized.city_name(tokyo, "en") == "Tokyo"
    assert localized.city_name(tokyo, "ko") == "도쿄"
    assert localized.country_label(tokyo, "zh-TW") == "日本"
    assert localized.country_label(tokyo, "ja") == "日本"
    assert localized.country_label(tokyo, "en") == "Japan"
    assert localized.reason(tokyo, "zh-CN") == "航班、住宿与跨区交通选择最完整"
    kamakura = destination_for_id("kamakura")
    assert kamakura is not None
    assert localized.city_name(kamakura, "en") == "Kamakura"
    assert localized.city_name(kamakura, "zh-TW") == "鎌倉"


@pytest.mark.asyncio
async def test_catalog_endpoint_uses_the_request_locale() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        english = await client.get("/api/v1/destinations", headers={"X-Travel-Locale": "en"})
        korean = await client.get("/api/v1/destinations", headers={"X-Travel-Locale": "ko"})
        default = await client.get("/api/v1/destinations")
    assert english.status_code == korean.status_code == default.status_code == 200
    by_id = {item["id"]: item for item in english.json()["items"]}
    assert (by_id["tokyo"]["city"], by_id["tokyo"]["country"]) == ("Tokyo", "Japan")
    assert by_id["tokyo"]["reason"].startswith("The widest choice")
    # local_name and english_name keep their own meaning whatever the reader's locale.
    assert by_id["kanazawa"]["local_name"] == "金沢"
    assert by_id["kanazawa"]["english_name"] == "Kanazawa"
    assert {item["id"]: item["city"] for item in korean.json()["items"]}["seoul"] == "서울"
    zh = {item["id"]: item for item in default.json()["items"]}
    assert (zh["tokyo"]["city"], zh["tokyo"]["country"]) == ("東京", "日本")
    assert len(by_id) == len(zh) == len(DESTINATIONS)


def test_english_name_is_english_for_every_destination() -> None:
    """The field claimed to hold an English name returned Chinese for 19 of 33 rows."""
    from app.destinations.localized import english_name

    for profile in DESTINATIONS:
        assert english_name(profile) != profile.city or profile.city.isascii(), profile.id
    tokyo = destination_for_id("tokyo")
    assert tokyo is not None and english_name(tokyo) == "Tokyo"
    osaka = destination_for_id("osaka-kyoto")
    assert osaka is not None and english_name(osaka) == "Osaka & Kyoto"


def test_place_names_localize_by_id_and_by_country_code() -> None:
    """Hotspot and merchant rows know an id and an ISO code, never the profile."""
    from app.destinations.localized import city_name_for, country_label_for

    assert city_name_for("tokyo", "en", "東京") == "Tokyo"
    assert city_name_for("tokyo", "ko", "東京") == "도쿄"
    assert city_name_for("tokyo", "zh-CN", "東京") == "东京"
    assert country_label_for("JP", "en", "日本") == "Japan"
    assert country_label_for("KR", "zh-CN", "韓國") == "韩国"

    # zh-TW is the catalog's own text, so the stored value is returned untouched.
    assert city_name_for("tokyo", "zh-TW", "東京") == "東京"
    assert country_label_for("JP", "zh-TW", "日本") == "日本"


def test_an_unknown_place_keeps_its_stored_name_rather_than_becoming_an_id() -> None:
    from app.destinations.localized import city_name_for, country_label_for

    assert city_name_for("atlantis", "en", "亞特蘭提斯") == "亞特蘭提斯"
    assert country_label_for("ZZ", "en", "未知國") == "未知國"
    assert city_name_for(None, "en", "東京") == "東京"
    assert country_label_for(None, "en", "日本") == "日本"


def test_lodging_areas_answer_in_the_readers_locale() -> None:
    """`areas[]` stayed Traditional in every locale while `city` next to it did not."""
    tokyo = destination_for_id("tokyo")
    assert tokyo is not None
    assert localized.area_labels(tokyo, "zh-TW") == list(tokyo.areas)
    assert localized.area_labels(tokyo, "en") == [
        "Shinjuku",
        "Ueno & Asakusa",
        "Tokyo Station & Ginza",
        "Shibuya",
    ]
    assert localized.area_labels(tokyo, "ja") == ["新宿", "上野・浅草", "東京駅・銀座", "渋谷"]
    assert localized.area_labels(tokyo, "zh-CN") == ["新宿", "上野／浅草", "东京站／银座", "涩谷"]

    # 「澀谷」 takes its own half of the reviewed 「澀谷／原宿」 rather than widening.
    assert localized.area_label(tokyo, "澀谷", "en") == "Shibuya"

    # Korean writes several of these as one district, so the whole reviewed name is
    # used when it does not split the same way — the fallback ``area_name`` already has.
    seoul = destination_for_id("seoul")
    assert seoul is not None
    assert localized.area_labels(seoul, "ko") == ["명동", "홍대", "동대문", "강남"]
    assert localized.area_labels(seoul, "ja") == ["Myeongdong", "Hongdae", "Dongdaemun", "Gangnam"]


def test_areas_the_reviewed_catalog_never_heard_of_are_named_by_hand() -> None:
    tainan = destination_for_id("tainan")
    assert tainan is not None
    assert localized.area_label(tainan, "中西區", "en") == "West Central District"
    assert localized.area_label(tainan, "中西區", "ja") == "中西区"
    # No Korean name was checked, so it falls back to English, never to Traditional.
    assert localized.area_label(tainan, "中西區", "ko") == "West Central District"
    assert localized.area_label(tainan, "海安路", "zh-CN") == "海安路"
    jeonju = destination_for_id("jeonju")
    assert jeonju is not None
    assert localized.area_label(jeonju, "完山公園", "ko") == "완산공원"


def test_an_area_nobody_has_checked_keeps_the_catalogs_own_text() -> None:
    tokyo = destination_for_id("tokyo")
    assert tokyo is not None
    assert localized.area_label(tokyo, "沒有人審過的地方", "en") == "沒有人審過的地方"
    assert localized.area_label(tokyo, "沒有人審過的地方", "zh-TW") == "沒有人審過的地方"


@pytest.mark.asyncio
async def test_catalog_endpoint_localizes_areas() -> None:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        english = await client.get("/api/v1/destinations", headers={"X-Travel-Locale": "en"})
        default = await client.get("/api/v1/destinations")
    by_id = {item["id"]: item for item in english.json()["items"]}
    assert by_id["tokyo"]["areas"][0] == "Shinjuku"
    assert all(
        not any("\u4e00" <= character <= "\u9fff" for character in area)
        for item in by_id.values()
        for area in item["areas"]
    )
    zh = {item["id"]: item for item in default.json()["items"]}
    assert zh["tokyo"]["areas"] == ["新宿", "上野／淺草", "東京站／銀座", "澀谷"]
