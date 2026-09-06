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
