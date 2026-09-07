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


def test_the_committed_batch_overlaps_the_curated_catalog_by_exactly_one_tainan_shop() -> None:
    """One overlap, not two. The second was a slug collision between different shops.

    This test used to assert two, one matched by slug and one by name, and read them both as
    "the curated catalog already has this shop". Only the name match was that. The slug match
    was tainan-fu-sheng-hao, where the curated catalog means 福生小食店 and this file meant
    富盛號 — so the row was not a duplicate being skipped, it was a real shop that could never
    be imported. It now has its own slug, and parse_merchants refuses the situation outright.
    """
    merchants = load_trend_merchants(DEFAULT_FILE)
    catalog_slugs = {seed.slug for seed in MERCHANT_SEEDS}
    catalog_identity = {
        (seed.destination_id, seed.local_name.casefold()) for seed in MERCHANT_SEEDS
    }
    by_slug = sorted(m.slug for m in merchants if m.slug in catalog_slugs)
    by_name = sorted(
        m.slug for m in merchants if m.slug not in catalog_slugs and m.identity in catalog_identity
    )
    assert by_slug == [], by_slug
    assert by_name == ["tainan-a-song-ge-bao"], by_name


def test_a_slug_the_curated_catalog_uses_for_another_shop_is_refused() -> None:
    """Silence was the damage. 富盛號 sat unimportable behind a skipped_existing_slug count."""
    curated = next(seed for seed in MERCHANT_SEEDS if seed.slug == "tainan-fu-sheng-hao")
    assert curated.local_name == "福生小食店"

    with pytest.raises(TrendImportError) as error:
        parse_merchants(
            [
                _row(
                    destination="tainan",
                    district_key="zhengxing",
                    slug="tainan-fu-sheng-hao",
                    name_zh="富盛號",
                    local_name="富盛號",
                    category_slugs=["street-food"],
                    source_url="https://www.twtainan.net/zh-tw/shop/consume/8617/",
                    source_title="富盛號 - 台南旅遊網",
                )
            ]
        )
    assert "could never be imported" in str(error.value)
    assert "tainan-fu-sheng-hao" in str(error.value)


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


def test_a_withdrawn_english_name_strands_the_row_until_asked_to_reset() -> None:
    """Removing a name_en does nothing on its own: the importer never revisits a slug.

    Seven merchants were left holding a romanisation no source backed, because the data file
    stopped proposing it and nothing went back for the rows.
    """
    withdrawn = parse_merchant(_row(), row=1)  # the file no longer carries name_en
    stranded = _imported(withdrawn, name="Dandelion Chocolate")
    merchants = {withdrawn.slug: withdrawn}

    changed, left = plan_english_name_backfill([stranded], merchants)
    assert changed == []
    assert left == [
        {
            "slug": withdrawn.slug,
            "name": "Dandelion Chocolate",
            "reason": "renamed since import",
        }
    ]

    changed, left = plan_english_name_backfill([stranded], merchants, reset_drifted=True)
    assert changed == [
        {
            "slug": withdrawn.slug,
            "from": "Dandelion Chocolate",
            "to": "Dandelion Chocolate 藏前工廠咖啡館",
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
            "reason": "already matches the file",
        }
    ]


def test_a_row_with_no_english_name_in_the_file_is_never_touched() -> None:
    merchant = parse_merchant(_row(), row=1)
    changed, left = plan_english_name_backfill([_imported(merchant)], {merchant.slug: merchant})
    assert changed == []
    # Reported as matching rather than skipped silently: with the reset mode in the same
    # command, "nothing to say about this row" and "this row is already right" are different
    # answers, and only one of them means the operator can stop looking.
    assert left == [
        {
            "slug": merchant.slug,
            "name": "Dandelion Chocolate 藏前工廠咖啡館",
            "reason": "already matches the file",
        }
    ]


# An English name that is not already somewhere in its own row came from outside the file, so
# it needs a source a reader can check. These were each confirmed on the page the row itself
# cites, on 2026-09-07. Seven others were removed in the same pass because their cited source
# carried no Latin script at all — 金得春捲's official Tainan page, 東區粉圓's own site and
# 蠔爽's Kaohsiung village page name the shop only in Chinese, so the romanisation had no
# origin anyone could confirm.
SOURCED_ENGLISH_NAMES = {
    # "Copyright © SHIROGANE SABO All Rights Reserved." on s-sabo.com
    "fukuoka-bai-jin-cha-fang": "Shirogane Sabo",
    # "川本屋" romanised as Kawamotoya on kawamotoya.com, which is also the domain
    "yokohama-chuan-ben-wu-cha-pu": "Kawamotoya",
    # "Tsuruya Yoshinobu CO., LTD." in the footer of tsuruyayoshinobu.jp
    "osaka-kyoto-he-wu-ji-xin-ben-dian": "Tsuruya Yoshinobu Main Store",
    # The brand is in the row already; only the branch is romanised, and it is a place name.
    "tokyo-hattifnatt": "HATTIFNATT Koenji",
    "fukuoka-manu-coffee": "manu coffee Daimyo",
    "okinawa-ohacort": "oHacorté Minatogawa",
    "okinawa-houkiboshi": "Houkiboshi Minatogawa",
    # faidama.com writes the shop as "faidama"; shokudou_faidama is its own Instagram handle.
    "okinawa-faidama": "Shokudo faidama",
    # --- added 2026-09-07 from a two-lens research pass, an adversarial verify pass and a
    # curl of every cited page; each comment names where the Latin form is printed ---
    # printed on an English listing:
    # https://www.eatingthaifood.com/restaurants/thai-beef-noodles-wattana-panich-ekkamai/
    "bangkok-wathnaaphaanich-enuue-tun": "Wattana Panich",
    # Visit Busan's English listing prints it (uc_seq=2158&lang_cd=en); local_name 모모스 로스터리 &
    # 커피바 is the same words
    "busan-momos": "Momos Roastery & Coffee Bar",
    # printed on an English listing:
    # https://world.nol.com/en/content/pois/c39cac50-504c-4924-a89e-8739bcc281a5
    "busan-mumyeongilgi": "Cotton Diary",
    # printed on an English listing:
    # https://www.timeout.com/chiang-mai/restaurants/kanomwan-chang-moi
    "chiang-mai-khnmhwaanchaangm-y": "Kanomwan Chang Moi",
    # printed on the shop's own page: https://www.kitipanit.com
    "chiang-mai-kitiphaanich": "Kiti Panit",
    # printed on an English listing:
    # https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=86381
    "daegu-bongsanjjimgalbi": "Bongsan Jjimgalbi",
    # printed on an English listing: https://creatrip.com/en/blog/9055
    "daegu-nagyeongjjimgalbi": "Nakyoung Jjimgalbi",
    # printed on an English listing: https://en.edaily.co.kr/news/eda202606275710/
    "daegu-nogyang": "Nokyang",
    # printed on an English listing:
    # https://www.daegufood.go.kr/kor/food/food.asp?idx=1790&gotoPage=1&snm=9&ta=5
    "daegu-nosekondo": "Nosecondo",
    # printed on an English listing:
    # https://english.visitkorea.or.kr/svc/contents/contentsView.do?vcontsId=183910
    "daegu-sanhojjimgalbisigdang": "Sanho Jjimgalbi",
    # printed on the shop's own page: https://www.manucoffee.com/shoplist/
    "fukuoka-manucoffee-roasters": "manucoffee roasters KUJIRA",
    # printed on the shop's own page: https://www.sehwamaeulcoop.com/our/cafe477
    "jeju-kape477": "CAFE477+",
    # printed on an English listing:
    # https://www.visitjeju.net/en/detail/view?contentsid=CNTS_000000000018312
    "jeju-kapegongjagso": "Cafe Gongjakso",
    # printed on an English listing:
    # https://www.visitjeju.net/en/detail/view?contentsid=CNTS_000000000021519
    "jeju-sehwaminsogoilsijang": "Sehwa Haenyeo Traditional 5-Day Market",
    # Instagram @a_norange, captions signed ANORANGE; case normalised like Shirogane Sabo
    "jeonju-eonorenji": "Anorange",
    # printed on an English listing:
    # https://www.google.com/maps/place/Geumeum/data=!4m6!3m5!1s0x3570254e521a8579:0xc2f0eecf98de54a8!8m2!3d35.8063178!4d127.150582!16s%2Fg%2F11v0396q8h?hl=en
    "jeonju-geumeum": "Geumeum",
    # printed on an English listing:
    # https://www.google.com/maps/place/Eat+Anything+with+vegan,+71+Seohak+3-gil,+Wansan-gu,+Jeonju-si,+Jeonbuk+State,+South+Korea/data=!4m6!3m5!1s0x357025b76951fd63:0xcfcaaddba0d08a68!8m2!3d35.8087076!4d127.1519068!16s%2Fg%2F11k3xgf4ry?hl=en
    "jeonju-isaenidding": "Eat Anything",
    # Instagram @kinoandco_official bio 「KINO & Co. Masion de Cafe & Spirits」
    "jeonju-kinoaenko": "Kino & Co.",
    # Instagram @cafe_ordonne display name 「전주카페 오르도네 Ordonné」, bio 「Ordonné [오르도네]」
    "jeonju-oreudone": "Ordonné",
    # Naver blog PostView 224269018154 prints 「PAUZE COFFEE」 with the row's address; the shop is
    # @pauze_jeonju
    "jeonju-paujaekeopi": "Pauze Coffee",
    # printed on an English listing:
    # https://tour.jeonju.go.kr/eng/board/view.jeonju?boardId=BBS_0000025&menuCd=DOM_000000209001000000&paging=ok&startPage=1&dataSid=10436
    "jeonju-seohagateuseupeiseu": "Seohak Art Space",
    # printed on an English listing: https://tabelog.com/en/ishikawa/A1701/A170101/17000399/
    "kanazawa-ye-tian-wu-cha-dian": "Nodaya Chaten",
    # printed on an English listing: https://www.nagoya-info.jp/en/gourmet/detail/25/
    "nagoya-mei-hua-tang": "Baikado",
    # printed on an English listing:
    # https://www.okinawastory.jp/feature/favorite_time/discover_coffee
    "okinawa-beans-store": "OKINAWA CERRADO COFFEE Beans Store",
    # printed on an English listing: https://untappd.com/v/ukishima-brewing-tap-room/8064988
    "okinawa-taproom": "Ukishima Brewing Tap Room",
    # printed on the shop's own page: https://bonobakery.jp/
    "osaka-kyoto-bono-bakery": "bonobakery",
    # printed on the shop's own page: https://taiyounotou.com/shops/honten/
    "osaka-kyoto-cafe-taiyounotou-honten": "cafe Taiyou no Tou Honten",
    # printed on the shop's own page: https://www.pancante.com/
    "osaka-kyoto-cante-grande": "Cante Grande Bakery",
    # printed on an English listing: https://tabelog.com/en/matome/26803/
    "osaka-kyoto-gokkei-ichijoji": "Menya Gokkei Ichijoji Honten",
    # printed on an English listing: https://tabelog.com/en/kyoto/A2601/A260303/26000491/
    "osaka-kyoto-ichijoji-nakatani": "Ichijoji Nakatani",
    # printed on an English listing: https://tabelog.com/en/osaka/A2701/A270101/27116582/
    "osaka-kyoto-kyuri-kissaten": "Kyuri Kissa Ten",
    # printed on an English listing: https://tabelog.com/en/kyoto/A2601/A260303/26001199/
    "osaka-kyoto-takayasu": "Chuka Soba Takayasu",
    # printed on the shop's own page: https://moonsunbrewing.jp/concept/
    "sapporo-brewing": "Moon and Sun BREWING",
    # printed on the shop's own page: https://donburi.jp/en/
    "sapporo-donburicha-wu-satsuporoer-tiao-shi-chang-dian": "Sapporo Nijyo-Ichiba DONBURI-CHAYA",
    # t-sushi.net/en, Tabelog EN 1079655 and japan-food.guide all print it; the site's own copyright
    # line says TATSUYOSHI THE SECOND Co.,ltd
    "sapporo-er-dai-mu-chen-yoshi": "Nidaime Tatsuyoshi",
    # printed on an English listing: https://tabelog.com/en/hokkaido/A0101/A010102/1082918/
    "sapporo-garaku": "Soup curry GARAKU Sapporo honten",
    # printed on an English listing: https://tabelog.com/en/hokkaido/A0101/A010103/1004766/
    "sapporo-zingisukan-higenoushi-ben-dian": "Jingisukan Higenoushi Honten",
    # printed on an English listing: https://en.wikipedia.org/wiki/Andongjang
    "seoul-andongjang": "Andongjang",
    # brand is in name_zh; en.coffeelibre.kr lists the branch as YeonNam (shopinfo no=2470), a place
    # name
    "seoul-coffee-libre-yeonnam": "Coffee Libre Yeonnam",
    # printed on an English listing:
    # https://english.visitkorea.or.kr/svc/whereToGo/locIntrdn/rgnContentsView.do?vcontsId=112805
    "seoul-daerimcanggo": "Daelim Changgo Gallery",
    # printed on an English listing:
    # https://ployslittleatlas.com/en/food-en/hani-kalguksu-an-unmissable-dish-in-seouls-sindang-dong/
    "seoul-hanikalgugsu": "Hani Kalguksu",
    # printed on an English listing:
    # https://english.visitseoul.net/restaurants/Joseonok-EN/ENP006970
    "seoul-joseonog": "Joseonok",
    # printed on an English listing:
    # https://english.visitseoul.net/restaurants/coffeehanyakbang/ENPyiaqhs
    "seoul-keopihanyagbang": "Coffee Hanyakbang",
    # printed on an English listing:
    # https://english.visitseoul.net/attractions/MabongnimHalmeonijip/ENP8wjib6
    "seoul-mabogrimhalmeonijib": "Mabongnim Halmeonijip",
    # printed on the shop's own page: https://mongtan.co.kr/
    "seoul-mongtan": "Mongtan",
    # printed on an English listing:
    # https://www.mytravelnotes.co.kr/en/sindang-mokpo-seafood-grilled-squid-fried-fish
    "seoul-oggyeongine-geonsaengseon": "Okgyeongine Geonsaengseon",
    # printed on an English listing:
    # https://www.tastekoreanfood.com/eatout/sansugapsan-seoul-authentic-korean-sundae
    "seoul-sansugabsan": "Sansugapsan",
    # printed on an English listing: https://letseoul.com/en/places/somunnan-seongsu-gamjatang
    "seoul-somunnanseongsugamjatang": "Somunnan Seongsu Gamjatang",
    # printed on an English listing:
    # https://edition.cnn.com/travel/article/tainan-street-food/index.html
    "tainan-fu-sheng-hao-wan-gui": "Fu Sheng Hao",
    # Tripadvisor d6143638, h1 「Tai Cheng Fruit Shop」, checked in a browser 2026-09-07; the shop's
    # own Facebook handle is Tai.cheng.fruit.shop
    "tainan-tai-cheng-shui-guo-bing-dian": "Tai Cheng Fruit Shop",
    # printed on an English listing:
    # https://tw.openrice.com/en/tainan/r-%E4%BF%AE%E5%AE%89%E6%89%81%E6%93%94%E8%B1%86%E8%8A%B1-xiuan-douhua-west-central-district-taiwanese-vegetarian-r94324/
    "tainan-xiu-an-bian-dan-dou-hua": "Xiu'an Douhua",
    # printed on an English listing: https://wanderlog.com/place/details/8323720/akamaru
    "taipei-dango-akamaru": "Akamaru",
    # Tripadvisor d1633072, h1 「Dongqu Fenyuan Bingdian (Eastern Ice Store)」, checked in a browser
    # 2026-09-07
    "taipei-dong-qu-fen-yuan": "Dongqu Fenyuan Bingdian",
    # printed on the shop's own page: https://www.fujintreeshop.com/en/pages/shopinfo
    "taipei-fujin-tree-cafe": "Fujin Tree Café – Fujin Store",
    # Instagram @ikenone_tw display name 「池音 鶏白湯拉麵 CHIYIN」
    "taipei-ikenone-ramen": "CHIYIN",
    # printed on an English listing: https://www.friendlystore.taipei/store/en/pg1/4/company/8482
    "taipei-waha-cafe-chengde": "Waha Café Chengde Branch",
    # printed on an English listing: https://tabelog.com/en/tokyo/A1311/A131103/13281905/
    "tokyo-chi-cha-ban-yue": "Kissa Hangetsu",
    # printed on the shop's own page: https://dandelionchocolate.jp/pages/shop-list
    "tokyo-dandelion-chocolate": "Dandelion Chocolate Factory & Cafe Kuramae",
    # printed on an English listing: https://tabelog.com/en/tokyo/A1311/A131103/13227380/
    "tokyo-guo-zi-wu-shinonome": "Kashiya Shinonome",
    # printed on the shop's own page: https://trianon.co.jp/
    "tokyo-torianonyang-guo-zi-dian": "TRIANON",
    # printed on an English listing: https://trulytokyo.com/gyozaro/
    "tokyo-yuan-su-jiao-zi-lou": "Harajuku Gyozaro",
    # printed on an English listing: https://tabelog.com/en/tokyo/A1311/A131103/13102272/
    "tokyo-yuwaeru": "Yuwaeru Honten",
    # printed on an English listing: https://tabelog.com/en/kanagawa/A1401/A140306/14001122/
    "yokohama-bang-zhi-man": "Hamajiman",
    # printed on an English listing: https://tabelog.com/en/kanagawa/A1401/A140306/14053590/
    "yokohama-yuan-zu-kare-tantanmian-zheng-hu-zong-ben-dian": (
        "Ganso Curry Tantanmen Masatora Souhonten"
    ),
    # Daegu's English city-tourism blog prints 「Neoguri (너구리)」 with the Hyangchon-dong address:
    # https://visitdaegu2011.blogspot.com/2011/09/famous-restaurants-in-daegu.html
    "daegu-neoguri": "Neoguri",
}


def test_an_english_name_not_in_its_row_has_a_recorded_source() -> None:
    """A romanisation nobody can trace is what this rule exists to keep out.

    An English reader who cannot find the shop by the name we show them is worse off than
    one who was given the Chinese name and could at least paste it into a map.
    """
    for merchant in load_trend_merchants(DEFAULT_FILE):
        if not merchant.english_name:
            continue
        haystack = f"{merchant.name} {merchant.local_name}".casefold()
        if merchant.english_name.casefold() in haystack:
            continue
        assert SOURCED_ENGLISH_NAMES.get(merchant.slug) == merchant.english_name, (
            f"{merchant.slug}: {merchant.english_name!r} is not in the row and is not on the "
            "checked list; add it with the source it came from, or drop it"
        )


def test_the_checked_list_has_no_entries_the_file_dropped() -> None:
    """A stale allowlist quietly stops guarding anything."""

    slugs = {m.slug for m in load_trend_merchants(DEFAULT_FILE) if m.english_name}
    assert set(SOURCED_ENGLISH_NAMES) <= slugs


def test_the_reset_refuses_a_slug_the_curated_catalog_owns() -> None:
    """The two files disagree about which shop this slug names.

    tainan-fu-sheng-hao is 福生小食店 in merchant_catalog.py and 富盛號 in the trend file.
    The importer kept the curated shop, so resetting that row toward the trend file would
    rename a restaurant into a different one. A production dry run reported it alongside the
    seven rows that really were stranded, which is what the printed list is for.
    """
    # The file no longer proposes this slug, but a production row still carries it, so the
    # backfill must keep refusing it whatever the file says today.
    curated = next(m for m in load_trend_merchants(DEFAULT_FILE) if m.slug.startswith("tainan-fu-"))
    assert "tainan-fu-sheng-hao" in {seed.slug for seed in MERCHANT_SEEDS}

    row = FoodMerchant(
        slug="tainan-fu-sheng-hao",
        destination_id=curated.destination_id,
        country_code=destination_country_code(curated.destination_id) or "",
        # What production holds: the curated shop, under its own English name.
        name="Fu Sheng Hao",
        local_name="福生小食店",
        names_json={},
    )
    changed, left = plan_english_name_backfill(
        [row], {"tainan-fu-sheng-hao": curated}, reset_drifted=True
    )
    assert changed == []
    assert left == [
        {
            "slug": "tainan-fu-sheng-hao",
            "name": "Fu Sheng Hao",
            "reason": "the curated catalog owns this slug",
        }
    ]
