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


def test_city_words_split_a_destination_written_as_two_cities() -> None:
    assert localized.city_words("osaka-kyoto", "en", "大阪／京都") == ("Osaka", "Kyoto")
    assert localized.city_words("osaka-kyoto", "zh-TW", "大阪／京都") == ("大阪", "京都")
    assert localized.city_words("hanoi", "ja", "河內") == ("ハノイ",)
    assert localized.city_words(None, "en", "河內") == ("河內",)


def test_country_mentions_reads_the_place_names_of_every_locale() -> None:
    # The search result never says which language it is in, so all five spellings count.
    assert localized.country_mentions("Yushan National Park | Taiwan Tourism") == {
        "Taiwan": "Taiwan"
    }
    assert localized.country_mentions("서울 나들이 코스") == {"South Korea": "서울"}
    assert localized.country_mentions("東京ディズニーランドの回り方") == {"Japan": "東京"}
    # A country is named by its cities too, and 臺 is the same character as 台.
    assert localized.country_mentions("圓山自然景觀公園，台北散步景點") == {"Taiwan": "台北"}
    assert localized.country_mentions("位於南臺灣的中央山脈西側，臺灣南投縣水里鄉") == {
        "Taiwan": "台灣"
    }
    # A place the catalog never heard of names no country at all.
    assert localized.country_mentions("還劍湖旅遊指南｜熱門景點資訊、交通地圖") == {}


def test_country_mentions_keeps_a_latin_name_out_of_a_longer_word() -> None:
    assert localized.country_mentions("Japanese sandwiches") == {}
    assert localized.country_mentions("Japan in five days") == {"Japan": "Japan"}
    # Vietnam's Huế is written "Hue"; the ordinary English noun is not a place.
    assert localized.country_mentions("a warm hue at sunset") == {}


def test_mentions_country_accepts_the_regions_and_old_names_in_the_aliases() -> None:
    # 「北海道小樽手宮公園」 writes neither 札幌 nor 日本, and is still Japan.
    assert localized.mentions_country("北海道小樽手宮公園｜小樽賞櫻最佳景點", "Japan") is True
    assert localized.country_mentions("北海道小樽手宮公園｜小樽賞櫻最佳景點") == {}
    assert localized.mentions_country("西貢海鮮街", "Vietnam") is True
    assert localized.mentions_country("西門町一日遊", "Japan") is False


def test_mentions_place_reads_a_name_in_either_taiwan_spelling() -> None:
    assert localized.mentions_place("臺北101 觀景台怎麼去", "台北101") is True
    assert localized.mentions_place("台北101 觀景台怎麼去", "臺北101") is True
    assert localized.mentions_place("台北101 觀景台怎麼去", "") is False


def test_a_katakana_country_name_is_a_whole_word() -> None:
    # 「タイ」 names Thailand; it also opens タイム, スタイル and タイプ. NAVITIME's page for
    # a Shibuya shop was reported as Thailand over a 「タイムセール」 in its summary.
    assert localized.country_mentions("渋谷区のドンキホーテ タイムセール情報") == {}
    assert localized.country_mentions("スタイルとタイプで選ぶ") == {}
    assert localized.country_mentions("タイ旅行の準備") == {"Thailand": "タイ"}
    # The middle dot and a particle end a word; the catalog order still picks the word.
    assert localized.country_mentions("バンコク・タイの屋台") == {"Thailand": "タイ"}
    assert localized.mentions_country("タイ人観光客に人気", "Thailand") is True
    assert localized.country_mentions("ソウル旅行") == {"South Korea": "ソウル"}
    assert localized.mentions_country("ソウルフードの店", "South Korea") is False


def test_a_landmark_named_after_another_country_names_no_country() -> None:
    # 會安的日本橋 (來遠橋) is in Vietnam; the Hoiana article that listed it was reported
    # as Japan, twice.
    assert localized.country_mentions("會安古鎮：來遠橋（日本橋）、燈籠街與河畔咖啡") == {}
    assert localized.named_country("會安古鎮：來遠橋（日本橋）、燈籠街與河畔咖啡") is None
    assert localized.country_mentions("東京日本橋の老舗") == {"Japan": "東京"}
    # What points at this country is still read from the whole text.
    assert localized.mentions_country("日本橋三越本店", "Japan") is True


def test_named_country_is_the_one_the_text_names_most() -> None:
    # A Taiwanese blog index that lists 台南, 台北 and one 沖繩 trip is about Taiwan; the
    # first country in catalog order is Japan, and the rejection reason said 沖繩.
    blog = "旅遊景點美食親子景點介紹 @ 青青小熊＊旅遊札記 台南美食、沖繩親子行程、台北景點"
    assert localized.named_country(blog) == ("Taiwan", "台南")
    # ``country_mentions`` still answers in catalog order: 台北 is listed before 台南.
    assert localized.country_mentions(blog) == {"Japan": "沖繩", "Taiwan": "台北"}
    # 指南宮 in Taipei keeps a Buddha a Thai field marshal gave; the page is about Taiwan.
    temple = "指南宮位於台北市文山區，殿內供奉泰國巴博元帥致贈的金佛，台北捷運動物園站步行可達"
    assert localized.named_country(temple) == ("Taiwan", "台北")
    # A tie goes to the country named first: the title comes before the summary.
    assert localized.named_country("沖繩親子行程｜青青小熊 台南美食") == ("Japan", "沖繩")
    assert localized.named_country("還劍湖旅遊指南｜熱門景點資訊、交通地圖") is None
    # Either Taiwan spelling counts, and the catalog's spelling is the word reported.
    assert localized.named_country("南臺灣的中央山脈西側，臺灣南投縣") == ("Taiwan", "台灣")


def test_mentions_place_reads_through_a_directory_s_brackets_and_spaces() -> None:
    # NAVITIME writes 「MEGA(メガ)ドン・キホーテ 渋谷本店」 for MEGAドン・キホーテ渋谷本店.
    title = "MEGA(メガ)ドン・キホーテ 渋谷本店 | 渋谷区のドンキホーテ・アクセス・地図 - NAVITIME"
    assert localized.mentions_place(title, "MEGAドン・キホーテ渋谷本店") is True
    assert localized.mentions_place("會安古城（Hội An）一日遊", "Hội An") is True
    # Joining words never makes a longer word match a shorter one.
    assert localized.mentions_place("Hoiana Resort & Golf", "Hoi An") is False


def test_district_words_name_the_wards_of_a_city_in_every_locale() -> None:
    words = localized.district_words("NRT")
    assert {"澀谷", "原宿", "渋谷", "Shibuya", "Harajuku", "新宿"} <= set(words)
    assert len(words) == len(set(words))
    assert localized.district_words(None) == ()
    assert localized.district_words("XXX") == ()
