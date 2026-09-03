from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.foods.area_catalog import AREA_SEEDS_BY_SLUG
from app.foods.catalog import FOOD_SEEDS
from app.foods.category_catalog import CATEGORY_SEEDS_BY_SLUG, categories_for_dishes

OFFICIAL_DESTINATION_FOOD_SOURCES = {
    "tokyo": "https://www.gotokyo.org/en/see-and-do/drinking-and-dining/index.html",
    "osaka-kyoto": "https://osaka-info.jp/en/gourmet/",
    "fukuoka": "https://www.gofukuoka.jp/en/articles/detail/d773d813-d160-4b3f-8092-8f7c2fe5d17d",
    "sapporo": "https://www.sapporo.travel/en/gourmet/",
    "kanazawa": "https://visitkanazawa.jp/en/restaurants/",
    "nagoya": "https://www.nagoya-info.jp/en/gourmet/",
    "sendai": "https://www.sentabi.jp/guidebook/attractions/",
    "hiroshima": "https://dive-hiroshima.com/en/feature/ichioshi/",
    "seoul": "https://english.visitseoul.net/restaurants",
    "busan": "https://www.visitbusan.net/en/index.do?menuCd=DOM_000000302002001000",
    "jeju": "https://www.visitjeju.net/en/themtour/list?menuId=DOM_000001832000000000",
    "daegu": "https://tour.daegu.go.kr/eng/index.do",
    "gyeongju": "https://www.gyeongju.go.kr/tour/eng/index.do",
    "jeonju": "https://tour.jeonju.go.kr/eng/index.jeonju",
    "bangkok": "https://www.tourismthailand.org/Destinations/Provinces/Bangkok/219",
    "chiang-mai": "https://www.tourismthailand.org/Destinations/Provinces/Chiang-Mai/101",
    "chiang-rai": "https://www.tourismthailand.org/Destinations/Provinces/Chiang-Rai/102",
    "phuket": "https://www.tourismthailand.org/Destinations/Provinces/Phuket/350",
    "krabi": "https://www.tourismthailand.org/Destinations/Provinces/Krabi/344",
    "taipei": "https://eng.taiwan.net.tw/m1.aspx?sNo=0002091",
    "taichung": "https://eng.taiwan.net.tw/m1.aspx?sNo=0002091",
    "kaohsiung": "https://eng.taiwan.net.tw/m1.aspx?sNo=0002091",
    "tainan": "https://eng.taiwan.net.tw/m1.aspx?sNo=0002091",
    "singapore": "https://www.visitsingapore.com/dining-drinks-singapore/local-dishes/",
    "hong-kong": "https://www.discoverhongkong.com/eng/explore/dining.html",
    "hanoi": "https://www.vietnam.travel/things-to-do/food",
    "ho-chi-minh-city": "https://www.vietnam.travel/things-to-do/food",
    "da-nang": "https://www.vietnam.travel/things-to-do/food",
    "hue": "https://www.vietnam.travel/things-to-do/food",
    "da-lat": "https://www.vietnam.travel/things-to-do/food",
}


@dataclass(frozen=True)
class MerchantSeed:
    slug: str
    destination_id: str
    country_code: str
    name: str
    local_name: str
    food_slugs: tuple[str, ...]
    display_order: int
    area_key: str | None = None
    extra_category_slugs: tuple[str, ...] = ()

    @property
    def area_slug(self) -> str | None:
        return f"{self.destination_id}-{self.area_key}" if self.area_key else None

    @property
    def category_slugs(self) -> tuple[str, ...]:
        """Dish-derived categories first (the first one is primary), curated extras last."""

        return categories_for_dishes(self.food_slugs, self.extra_category_slugs)

    @property
    def source_title(self) -> str:
        return "Official destination food guide (regional context only)"

    @property
    def source_url(self) -> str:
        return OFFICIAL_DESTINATION_FOOD_SOURCES[self.destination_id]


def _m(
    destination_id: str,
    country_code: str,
    slug: str,
    name: str,
    local_name: str,
    foods: tuple[str, ...],
    order: int,
) -> MerchantSeed:
    full_slug = f"{destination_id}-{slug}"
    return MerchantSeed(
        slug=full_slug,
        destination_id=destination_id,
        country_code=country_code,
        name=name,
        local_name=local_name,
        food_slugs=foods,
        display_order=order,
        area_key=MERCHANT_AREA_KEYS.get(full_slug),
        extra_category_slugs=MERCHANT_EXTRA_CATEGORIES.get(full_slug, ()),
    )


# Areas are assigned only where the branch name or the merchant's documented location
# makes the 商圈 unambiguous; everything else stays unassigned until an administrator
# confirms it. Keys are the ``AreaSeed.key`` values of the merchant's own destination.
MERCHANT_AREA_KEYS: dict[str, str] = {
    "tokyo-ichiran-shibuya": "shibuya",
    "tokyo-tsunahachi": "shinjuku",
    "osaka-kyoto-kinryu-ramen": "namba-shinsaibashi",
    "osaka-kyoto-mizuno": "namba-shinsaibashi",
    "osaka-kyoto-aizuya": "namba-shinsaibashi",
    "osaka-kyoto-tempura-makino": "shijo-kawaramachi",
    "fukuoka-shin-shin": "tenjin",
    "fukuoka-hachibei": "hakata-station",
    "sapporo-hanamaru": "sapporo-station",
    "kanazawa-mori-mori-sushi": "omicho",
    "nagoya-yabaton": "sakae",
    "nagoya-yamamotoya": "sakae",
    "seoul-namdaemun-hotteok": "myeongdong",
    "seoul-lees-gimbap": "gangnam",
    "busan-dari-jip": "nampo-dong",
    "busan-biff-ssiat-hotteok": "nampo-dong",
    "jeju-donsadon": "jeju-city",
    "jeju-kim-man-bok": "jeju-city",
    "daegu-jungang-tteokbokki": "dongseongno",
    "daegu-yakjeon-samgyetang": "banwoldang",
    "gyeongju-yosokkoong": "hwangnidan-gil",
    "gyeongju-gyodong-gimbap": "hwangnidan-gil",
    "jeonju-hankook-jib": "hanok-village",
    "jeonju-gyodong-hotteok": "hanok-village",
    "bangkok-som-tam-nua": "siam",
    "chiang-mai-huen-muan-jai": "nimman",
    "chiang-mai-som-tam-udon": "nimman",
    "chiang-mai-kiat-ocha": "old-city",
    "chiang-mai-mango-tango": "nimman",
    "chiang-mai-khao-soi-khun-yai": "old-city",
    "chiang-rai-clock-tower-pad-thai": "clock-tower",
    "chiang-rai-jetyod-chicken-rice": "night-bazaar",
    "chiang-rai-khao-soi-phor-jai": "night-bazaar",
    "phuket-one-chun": "old-town",
    "phuket-mae-somchit": "old-town",
    "krabi-kodam-kitchen": "krabi-town",
    "krabi-ruen-mai": "krabi-town",
    "krabi-family-thaifood": "ao-nang",
    "taipei-lin-dong-fang": "zhongshan",
    "taipei-din-tai-fung": "xinyi",
    "taipei-chun-shui-tang": "xinyi",
    "taichung-qin-yuan-chun": "central-district",
    "taichung-fu-din-wang": "central-district",
    "taichung-chun-shui-siwei": "west-district",
    "kaohsiung-gang-yuan": "yancheng",
    "tainan-lao-tang-beef-noodle": "west-central",
    "tainan-fu-sheng-hao": "west-central",
    "tainan-shi-jing-jiu": "west-central",
    "tainan-xiluo-dian": "west-central",
    "tainan-hanlin": "west-central",
    "tainan-a-song-gua-bao": "west-central",
    "tainan-du-xiao-yue": "west-central",
    "singapore-tian-tian": "chinatown",
    "singapore-song-fa": "chinatown",
    "singapore-ya-kun": "chinatown",
    "hong-kong-yat-lok": "central-sheung-wan",
    "hong-kong-maks-noodle": "central-sheung-wan",
    "hong-kong-tai-cheong": "central-sheung-wan",
    "hong-kong-kam-wah": "mong-kok",
    "hanoi-pho-bat-dan": "old-quarter",
    "hanoi-banh-mi-25": "old-quarter",
    "hanoi-cuon-n-roll": "old-quarter",
    "hanoi-cafe-giang": "old-quarter",
    "hanoi-che-ba-thin": "old-quarter",
    "ho-chi-minh-city-pho-hoa": "district-3",
    "ho-chi-minh-city-banh-mi-huynh-hoa": "district-1",
    "ho-chi-minh-city-wrap-roll": "district-1",
    "ho-chi-minh-city-banh-xeo-46a": "district-1",
    "da-nang-madame-lan": "han-river",
    "hue-banh-khoai-hong-mai": "imperial-city",
    "hue-che-hem": "perfume-river-south",
}

# Categories beyond what the linked dishes imply (market stalls, tasting-menu houses).
MERCHANT_EXTRA_CATEGORIES: dict[str, tuple[str, ...]] = {
    "tokyo-torishiki": ("fine-dining",),
    "osaka-kyoto-endo-sushi": ("hawker-market",),
    "fukuoka-sushi-sakai": ("fine-dining",),
    "kanazawa-mori-mori-sushi": ("hawker-market",),
    "seoul-korea-house": ("fine-dining",),
    "gyeongju-yosokkoong": ("fine-dining",),
}


MERCHANT_SEEDS: tuple[MerchantSeed, ...] = (
    # Named candidates only. They stay pending until an exact provider identity and
    # independently sourced permanent coordinates are reviewed by an administrator.
    _m("tokyo", "JP", "sushi-dai", "Sushi Dai", "寿司大", ("jp-sushi",), 1),
    _m("tokyo", "JP", "ichiran-shibuya", "Ichiran Shibuya", "一蘭 渋谷店", ("jp-ramen",), 2),
    _m("tokyo", "JP", "tsunahachi", "Shinjuku Tsunahachi", "新宿つな八 総本店", ("jp-tempura",), 3),
    _m(
        "tokyo",
        "JP",
        "maisen-aoyama",
        "Maisen Aoyama",
        "とんかつ まい泉 青山本店",
        ("jp-tonkatsu",),
        4,
    ),
    _m("tokyo", "JP", "kanda-matsuya", "Kanda Matsuya", "神田まつや", ("jp-soba",), 5),
    _m("tokyo", "JP", "torishiki", "Torishiki", "鳥しき", ("jp-yakitori",), 6),
    _m("tokyo", "JP", "toraya-akasaka", "Toraya Akasaka", "とらや 赤坂店", ("jp-wagashi",), 7),
    _m("osaka-kyoto", "JP", "endo-sushi", "Endo Sushi", "ゑんどう寿司", ("jp-sushi",), 1),
    _m(
        "osaka-kyoto",
        "JP",
        "kinryu-ramen",
        "Kinryu Ramen Dotonbori",
        "金龍ラーメン 道頓堀店",
        ("jp-ramen",),
        2,
    ),
    _m(
        "osaka-kyoto",
        "JP",
        "tempura-makino",
        "Tempura Makino Teramachi",
        "天ぷら定食まきの 京都寺町店",
        ("jp-tempura",),
        3,
    ),
    _m("osaka-kyoto", "JP", "mizuno", "Mizuno", "美津の", ("jp-okonomiyaki",), 4),
    _m("osaka-kyoto", "JP", "aizuya", "Aizuya Namba", "会津屋 ナンバ店", ("jp-takoyaki",), 5),
    _m("osaka-kyoto", "JP", "omen", "Omen Ginkakuji", "おめん 銀閣寺本店", ("jp-udon",), 6),
    _m(
        "osaka-kyoto",
        "JP",
        "toraya-kyoto",
        "Toraya Kyoto Ichijo",
        "虎屋菓寮 京都一条店",
        ("jp-wagashi",),
        7,
    ),
    _m("fukuoka", "JP", "sushi-sakai", "Sushi Sakai", "鮨さかい", ("jp-sushi",), 1),
    _m(
        "fukuoka",
        "JP",
        "shin-shin",
        "Hakata Ramen ShinShin Tenjin",
        "博多らーめん ShinShin 天神本店",
        ("jp-ramen",),
        2,
    ),
    _m("fukuoka", "JP", "udon-taira", "Udon Taira", "うどん平", ("jp-udon",), 3),
    _m(
        "fukuoka",
        "JP",
        "hachibei",
        "Yakitori Hachibei Hakata",
        "焼とりの八兵衛 博多店",
        ("jp-yakitori",),
        4,
    ),
    _m(
        "sapporo",
        "JP",
        "hanamaru",
        "Nemuro Hanamaru Sapporo Stellar Place",
        "根室花まる 札幌ステラプレイス店",
        ("jp-sushi",),
        1,
    ),
    _m("sapporo", "JP", "sumire", "Sumire Sapporo", "すみれ 札幌本店", ("jp-ramen",), 2),
    _m(
        "kanazawa",
        "JP",
        "mori-mori-sushi",
        "Mori Mori Sushi Omicho",
        "もりもり寿し 近江町店",
        ("jp-sushi",),
        1,
    ),
    _m("kanazawa", "JP", "tempura-koizumi", "Tempura Koizumi", "天ぷら 小泉", ("jp-tempura",), 2),
    _m(
        "kanazawa",
        "JP",
        "tonkatsu-an-zukiyo",
        "Tonkatsu Anzu Kanazawa",
        "とんかつ あんず 金沢",
        ("jp-tonkatsu",),
        3,
    ),
    _m("kanazawa", "JP", "morihachi", "Morihachi Main Store", "森八 本店", ("jp-wagashi",), 4),
    _m("nagoya", "JP", "yabaton", "Yabaton Yabacho", "矢場とん 矢場町本店", ("jp-tonkatsu",), 1),
    _m("nagoya", "JP", "yamamotoya", "Yamamotoya Honten", "山本屋本店 栄本町通店", ("jp-udon",), 2),
    _m("nagoya", "JP", "ebisuya", "Sohonke Ebisuya", "総本家えびすや本店", ("jp-soba",), 3),
    _m("sendai", "JP", "ramen-kaichi", "Ramen Kaichi", "らーめん かいじ", ("jp-ramen",), 1),
    _m(
        "sendai",
        "JP",
        "sobadokoro-kanda",
        "Sobadokoro Kanda",
        "そばの神田 東一屋 本店",
        ("jp-soba",),
        2,
    ),
    _m("sendai", "JP", "aburiya-jujiro", "Aburiya Jujiro", "炙屋十兵衛", ("jp-yakitori",), 3),
    _m(
        "hiroshima", "JP", "hassei", "Okonomiyaki Hassei", "お好み焼き 八誠", ("jp-okonomiyaki",), 1
    ),
    # South Korea.
    _m("seoul", "KR", "korea-house", "Korea House", "한국의집", ("kr-kimchi", "kr-japchae"), 1),
    _m("seoul", "KR", "mokmyeoksanbang", "Mokmyeoksanbang", "목멱산방", ("kr-bibimbap",), 2),
    _m("seoul", "KR", "woo-lae-oak", "Woo Lae Oak", "우래옥", ("kr-bulgogi", "kr-naengmyeon"), 3),
    _m(
        "seoul",
        "KR",
        "maple-tree-house",
        "Maple Tree House Itaewon",
        "단풍나무집 이태원점",
        ("kr-samgyeopsal",),
        4,
    ),
    _m(
        "seoul",
        "KR",
        "mabongnim",
        "Mabongnim Halmeoni Tteokbokki",
        "마복림할머니떡볶이",
        ("kr-tteokbokki",),
        5,
    ),
    _m("seoul", "KR", "tosokchon", "Tosokchon Samgyetang", "토속촌삼계탕", ("kr-samgyetang",), 6),
    _m(
        "seoul",
        "KR",
        "namdaemun-hotteok",
        "Namdaemun Vegetable Hotteok",
        "남대문 야채호떡",
        ("kr-hotteok",),
        7,
    ),
    _m(
        "seoul",
        "KR",
        "lees-gimbap",
        "Lee's Gimbap Apgujeong",
        "리김밥 압구정본점",
        ("kr-gimbap",),
        8,
    ),
    _m(
        "busan",
        "KR",
        "anga",
        "Anga Busan",
        "안가 부산",
        ("kr-kimchi", "kr-bulgogi", "kr-samgyeopsal"),
        1,
    ),
    _m("busan", "KR", "dari-jip", "Dari Jip", "다리집", ("kr-tteokbokki", "kr-gimbap"), 2),
    _m(
        "busan",
        "KR",
        "gaya-milmyeon",
        "Wonjo Halmae Gaya Milmyeon",
        "원조할매가야밀면",
        ("kr-naengmyeon",),
        3,
    ),
    _m(
        "busan",
        "KR",
        "biff-ssiat-hotteok",
        "BIFF Square Ssiat Hotteok",
        "BIFF광장 씨앗호떡",
        ("kr-hotteok",),
        4,
    ),
    _m("jeju", "KR", "donsadon", "Donsadon", "돈사돈", ("kr-kimchi", "kr-samgyeopsal"), 1),
    _m("jeju", "KR", "kim-man-bok", "Jeju Kim Man-bok", "제주김만복", ("kr-gimbap",), 2),
    _m("daegu", "KR", "gogung", "Gogung Daegu", "고궁 대구", ("kr-kimchi", "kr-bibimbap"), 1),
    _m(
        "daegu",
        "KR",
        "palgong-samgyeopsal",
        "Palgong Samgyeopsal",
        "팔공삼겹살",
        ("kr-samgyeopsal",),
        2,
    ),
    _m(
        "daegu",
        "KR",
        "jungang-tteokbokki",
        "Jungang Tteokbokki",
        "중앙떡볶이",
        ("kr-tteokbokki",),
        3,
    ),
    _m(
        "daegu",
        "KR",
        "yakjeon-samgyetang",
        "Yakjeon Samgyetang",
        "약전삼계탕",
        ("kr-samgyetang",),
        4,
    ),
    _m("daegu", "KR", "busan-anmyeonok", "Busan Anmyeonok", "부산안면옥", ("kr-naengmyeon",), 5),
    _m("gyeongju", "KR", "yosokkoong", "Yosokkoong", "요석궁", ("kr-kimchi", "kr-japchae"), 1),
    _m("gyeongju", "KR", "gyodong-gimbap", "Gyodong Gimbap", "교동김밥", ("kr-gimbap",), 2),
    _m(
        "jeonju",
        "KR",
        "hankook-jib",
        "Hankook Jib",
        "한국집",
        ("kr-kimchi", "kr-bibimbap", "kr-bulgogi", "kr-japchae"),
        1,
    ),
    _m("jeonju", "KR", "gyodong-hotteok", "Gyodong Hotteok", "교동호떡", ("kr-hotteok",), 2),
    # Thailand.
    _m("bangkok", "TH", "thipsamai", "Thipsamai", "ทิพย์สมัย", ("th-pad-thai",), 1),
    _m(
        "bangkok",
        "TH",
        "pe-aor",
        "Pe Aor Tom Yum Kung Noodle",
        "พี่อ้อ ก๋วยเตี๋ยวต้มยำกุ้ง",
        ("th-tom-yum",),
        2,
    ),
    _m("bangkok", "TH", "krua-apsorn", "Krua Apsorn", "ครัวอัปษร", ("th-green-curry",), 3),
    _m("bangkok", "TH", "som-tam-nua", "Som Tam Nua", "ส้มตำนัว", ("th-som-tam",), 4),
    _m(
        "bangkok",
        "TH",
        "go-ang",
        "Go-Ang Pratunam Chicken Rice",
        "โกอ่างข้าวมันไก่ประตูน้ำ",
        ("th-khao-man-gai",),
        5,
    ),
    _m(
        "bangkok",
        "TH",
        "toy-kuay-teow-ruea",
        "Toy Kuay Teow Ruea",
        "ต้อย ก๋วยเตี๋ยวเรือ",
        ("th-boat-noodles",),
        6,
    ),
    _m("bangkok", "TH", "kor-panich", "Kor Panich", "ก.พานิช", ("th-mango-sticky-rice",), 7),
    _m(
        "bangkok",
        "TH",
        "muslim-restaurant",
        "Muslim Restaurant Bangkok",
        "มุสลิม เรสเตอรองท์",
        ("th-massaman-curry",),
        8,
    ),
    _m("bangkok", "TH", "hea-owan", "Hea Owan Moo Ping", "เฮียอ้วน หมูปิ้ง", ("th-moo-ping",), 9),
    _m(
        "chiang-mai",
        "TH",
        "pad-thai-mustache",
        "Pad Thai Mustache Style",
        "ผัดไทยหนวด",
        ("th-pad-thai",),
        1,
    ),
    _m("chiang-mai", "TH", "huen-muan-jai", "Huen Muan Jai", "เฮือนม่วนใจ๋", ("th-green-curry",), 2),
    _m(
        "chiang-mai",
        "TH",
        "som-tam-udon",
        "Som Tam Udon Chiang Mai",
        "ส้มตำอุดร เชียงใหม่",
        ("th-som-tam",),
        3,
    ),
    _m("chiang-mai", "TH", "kiat-ocha", "Kiat Ocha", "เกียรติโอชา", ("th-khao-man-gai",), 4),
    _m(
        "chiang-mai",
        "TH",
        "mango-tango",
        "Mango Tango Chiang Mai",
        "แมงโก้แทงโก้ เชียงใหม่",
        ("th-mango-sticky-rice",),
        5,
    ),
    _m(
        "chiang-mai",
        "TH",
        "khao-soi-khun-yai",
        "Khao Soi Khun Yai",
        "ข้าวซอยคุณยาย",
        ("th-khao-soi",),
        6,
    ),
    _m(
        "chiang-mai",
        "TH",
        "moo-ping-hea-owan",
        "Hea Owan Moo Ping Chiang Mai",
        "เฮียอ้วน หมูปิ้ง เชียงใหม่",
        ("th-moo-ping",),
        7,
    ),
    _m(
        "chiang-rai",
        "TH",
        "clock-tower-pad-thai",
        "Clock Tower Pad Thai",
        "ผัดไทยหอนาฬิกา",
        ("th-pad-thai",),
        1,
    ),
    _m(
        "chiang-rai", "TH", "barrab", "Barrab Chiang Rai", "บาราบ", ("th-som-tam", "th-moo-ping"), 2
    ),
    _m(
        "chiang-rai",
        "TH",
        "jetyod-chicken-rice",
        "Jetyod Chicken Rice",
        "ข้าวมันไก่เจ็ดยอด",
        ("th-khao-man-gai",),
        3,
    ),
    _m(
        "chiang-rai",
        "TH",
        "khao-soi-phor-jai",
        "Khao Soi Phor Jai",
        "ข้าวซอยพอใจ",
        ("th-khao-soi",),
        4,
    ),
    _m(
        "phuket",
        "TH",
        "one-chun",
        "One Chun Cafe and Restaurant",
        "วันจันทร์",
        ("th-pad-thai", "th-tom-yum", "th-green-curry", "th-massaman-curry"),
        1,
    ),
    _m(
        "phuket",
        "TH",
        "mae-somchit",
        "Mae Somchit Mango Sticky Rice",
        "แม่สมจิต ข้าวเหนียวมะม่วง",
        ("th-mango-sticky-rice",),
        2,
    ),
    _m("krabi", "TH", "kodam-kitchen", "Kodam Kitchen", "โกดำ คิทเช่น", ("th-pad-thai",), 1),
    _m(
        "krabi",
        "TH",
        "ruen-mai",
        "Ruen Mai Restaurant",
        "เรือนไม้",
        ("th-tom-yum", "th-massaman-curry"),
        2,
    ),
    _m(
        "krabi",
        "TH",
        "family-thaifood",
        "Family Thaifood and Seafood",
        "แฟมิลี่ ไทยฟู้ด",
        ("th-mango-sticky-rice",),
        3,
    ),
    # Taiwan.
    _m(
        "taipei",
        "TW",
        "lin-dong-fang",
        "Lin Dong Fang Beef Noodles",
        "林東芳牛肉麵",
        ("tw-beef-noodle-soup",),
        1,
    ),
    _m(
        "taipei",
        "TW",
        "din-tai-fung",
        "Din Tai Fung Xinyi",
        "鼎泰豐 信義店",
        ("tw-xiaolongbao",),
        2,
    ),
    _m(
        "taipei",
        "TW",
        "jin-feng",
        "Jin Feng Braised Pork Rice",
        "金峰魯肉飯",
        ("tw-lu-rou-fan",),
        3,
    ),
    _m(
        "taipei",
        "TW",
        "yuanhuan-oyster",
        "Ningxia Oyster Omelet",
        "圓環邊蚵仔煎",
        ("tw-oyster-omelet",),
        4,
    ),
    _m(
        "taipei",
        "TW",
        "dai-stinky-tofu",
        "Dai's House of Stinky Tofu",
        "戴記獨臭之家",
        ("tw-stinky-tofu",),
        5,
    ),
    _m(
        "taipei",
        "TW",
        "chun-shui-tang",
        "Chun Shui Tang Xinyi",
        "春水堂 信義店",
        ("tw-bubble-tea",),
        6,
    ),
    _m("taipei", "TW", "lan-jia", "Lan Jia Gua Bao", "藍家割包", ("tw-gua-bao",), 7),
    _m("taipei", "TW", "chia-te", "Chia Te Bakery", "佳德糕餅", ("tw-pineapple-cake",), 8),
    _m(
        "taipei",
        "TW",
        "tian-jin-pancake",
        "Tian Jin Scallion Pancake",
        "天津蔥抓餅",
        ("tw-scallion-pancake",),
        9,
    ),
    _m(
        "taichung",
        "TW",
        "lao-xiang",
        "Lao Xiang Beef Noodles",
        "老向的店",
        ("tw-beef-noodle-soup",),
        1,
    ),
    _m("taichung", "TW", "qin-yuan-chun", "Qin Yuan Chun", "沁園春", ("tw-xiaolongbao",), 2),
    _m("taichung", "TW", "fu-din-wang", "Fu Din Wang", "富鼎旺豬腳", ("tw-lu-rou-fan",), 3),
    _m(
        "taichung",
        "TW",
        "wang-gong-oyster",
        "Wang Gong Oyster Omelet",
        "王功蚵仔煎",
        ("tw-oyster-omelet",),
        4,
    ),
    _m(
        "taichung",
        "TW",
        "yizhong-stinky-tofu",
        "Yizhong Stinky Tofu",
        "一中臭豆腐",
        ("tw-stinky-tofu",),
        5,
    ),
    _m(
        "taichung",
        "TW",
        "chun-shui-siwei",
        "Chun Shui Tang Siwei",
        "春水堂 四維創始店",
        ("tw-bubble-tea",),
        6,
    ),
    _m("taichung", "TW", "wang-ji-gua-bao", "Wang Ji Gua Bao", "王記割包", ("tw-gua-bao",), 7),
    _m(
        "taichung",
        "TW",
        "sunnyhills",
        "SunnyHills Taichung",
        "微熱山丘 台中",
        ("tw-pineapple-cake",),
        8,
    ),
    _m(
        "taichung",
        "TW",
        "tian-jin-pancake",
        "Tian Jin Scallion Pancake Taichung",
        "天津蔥油餅 台中",
        ("tw-scallion-pancake",),
        9,
    ),
    _m(
        "kaohsiung",
        "TW",
        "gang-yuan",
        "Gang Yuan Beef Noodles",
        "港園牛肉麵",
        ("tw-beef-noodle-soup",),
        1,
    ),
    _m(
        "kaohsiung",
        "TW",
        "formosa-chang",
        "Formosa Chang Kaohsiung",
        "鬍鬚張 高雄",
        ("tw-lu-rou-fan",),
        2,
    ),
    _m(
        "kaohsiung",
        "TW",
        "old-zhou-oyster",
        "Old Zhou Oyster Omelet",
        "老周蚵仔煎",
        ("tw-oyster-omelet",),
        3,
    ),
    _m(
        "kaohsiung",
        "TW",
        "jiang-hao-ji",
        "Jiang Hao Ji Stinky Tofu",
        "江豪記臭豆腐王",
        ("tw-stinky-tofu",),
        4,
    ),
    _m(
        "kaohsiung",
        "TW",
        "chun-shui-tang",
        "Chun Shui Tang Kaohsiung",
        "春水堂 高雄",
        ("tw-bubble-tea",),
        5,
    ),
    _m("kaohsiung", "TW", "jiu-zhen-nan", "Jiu Zhen Nan", "舊振南餅店", ("tw-pineapple-cake",), 6),
    _m(
        "kaohsiung",
        "TW",
        "old-jiang-pancake",
        "Old Jiang Scallion Pancake",
        "老江蔥油餅",
        ("tw-scallion-pancake",),
        7,
    ),
    _m(
        "tainan",
        "TW",
        "lao-tang-beef-noodle",
        "Lao Tang Beef Noodles",
        "老唐牛肉麵",
        ("tw-beef-noodle-soup",),
        1,
    ),
    _m("tainan", "TW", "fu-sheng-hao", "Fu Sheng Hao", "福生小食店", ("tw-lu-rou-fan",), 2),
    _m(
        "tainan",
        "TW",
        "shi-jing-jiu",
        "Shi Jing Jiu Oyster Omelet",
        "石精臼蚵仔煎",
        ("tw-oyster-omelet",),
        3,
    ),
    _m(
        "tainan",
        "TW",
        "xiluo-dian",
        "Xiluo Dian Stinky Tofu",
        "西羅殿牛肉湯臭豆腐",
        ("tw-stinky-tofu",),
        4,
    ),
    _m("tainan", "TW", "hanlin", "Hanlin Tea Room", "翰林茶館", ("tw-bubble-tea",), 5),
    _m("tainan", "TW", "a-song-gua-bao", "A-Song Gua Bao", "阿松割包", ("tw-gua-bao",), 6),
    _m("tainan", "TW", "du-xiao-yue", "Du Hsiao Yueh", "度小月擔仔麵", ("tw-danzai-noodles",), 7),
    # Singapore and Hong Kong.
    _m(
        "singapore",
        "SG",
        "tian-tian",
        "Tian Tian Hainanese Chicken Rice",
        "Tian Tian Hainanese Chicken Rice",
        ("sg-chicken-rice",),
        1,
    ),
    _m(
        "singapore",
        "SG",
        "328-katong-laksa",
        "328 Katong Laksa",
        "328 Katong Laksa",
        ("sg-laksa",),
        2,
    ),
    _m(
        "singapore",
        "SG",
        "jumbo-riverside",
        "JUMBO Seafood Riverside Point",
        "JUMBO Seafood Riverside Point",
        ("sg-chilli-crab",),
        3,
    ),
    _m(
        "singapore",
        "SG",
        "hill-street-kway-teow",
        "Hill Street Fried Kway Teow",
        "Hill Street Fried Kway Teow",
        ("sg-char-kway-teow",),
        4,
    ),
    _m(
        "singapore",
        "SG",
        "song-fa",
        "Song Fa Bak Kut Teh New Bridge Road",
        "Song Fa Bak Kut Teh New Bridge Road",
        ("sg-bak-kut-teh",),
        5,
    ),
    _m(
        "singapore",
        "SG",
        "ya-kun",
        "Ya Kun Kaya Toast Far East Square",
        "Ya Kun Kaya Toast Far East Square",
        ("sg-kaya-toast",),
        6,
    ),
    _m("singapore", "SG", "haron-satay", "Haron Satay", "Haron Satay", ("sg-satay",), 7),
    _m(
        "singapore", "SG", "toa-payoh-rojak", "Toa Payoh Rojak", "Toa Payoh Rojak", ("sg-rojak",), 8
    ),
    _m(
        "singapore", "SG", "samys-curry", "Samy's Curry", "Samy's Curry", ("sg-fish-head-curry",), 9
    ),
    _m(
        "singapore",
        "SG",
        "jin-jin-dessert",
        "Jin Jin Hot Cold Dessert",
        "Jin Jin Hot Cold Dessert",
        ("sg-ice-kacang",),
        10,
    ),
    _m(
        "hong-kong",
        "HK",
        "tim-ho-wan",
        "Tim Ho Wan Sham Shui Po",
        "添好運 深水埗",
        ("hk-dim-sum",),
        1,
    ),
    _m(
        "hong-kong",
        "HK",
        "yat-lok",
        "Yat Lok Restaurant",
        "一樂燒鵝",
        ("hk-roast-goose", "hk-siu-mei"),
        2,
    ),
    _m(
        "hong-kong",
        "HK",
        "maks-noodle",
        "Mak's Noodle Central",
        "麥奀記忠記傳統雲吞麵家",
        ("hk-wonton-noodles",),
        3,
    ),
    _m(
        "hong-kong",
        "HK",
        "tai-cheong",
        "Tai Cheong Bakery Central",
        "泰昌餅家 中環",
        ("hk-egg-tart",),
        4,
    ),
    _m(
        "hong-kong",
        "HK",
        "kam-wah",
        "Kam Wah Cafe",
        "金華冰廳",
        ("hk-pineapple-bun", "hk-milk-tea"),
        5,
    ),
    _m(
        "hong-kong",
        "HK",
        "hing-kee",
        "Hing Kee Claypot Rice",
        "興記煲仔飯",
        ("hk-claypot-rice",),
        6,
    ),
    _m("hong-kong", "HK", "man-kee", "Man Kee Cart Noodle", "文記車仔麵", ("hk-cart-noodles",), 7),
    _m(
        "hong-kong",
        "HK",
        "trusty-congee",
        "Trusty Congee King",
        "靠得住粥麵小館",
        ("hk-congee",),
        8,
    ),
    # Vietnam.
    _m(
        "hanoi",
        "VN",
        "pho-bat-dan",
        "Pho Gia Truyen Bat Dan",
        "Phở Gia Truyền Bát Đàn",
        ("vn-pho",),
        1,
    ),
    _m("hanoi", "VN", "banh-mi-25", "Banh Mi 25", "Bánh Mì 25", ("vn-banh-mi",), 2),
    _m(
        "hanoi",
        "VN",
        "bun-cha-huong-lien",
        "Bun Cha Huong Lien",
        "Bún Chả Hương Liên",
        ("vn-bun-cha",),
        3,
    ),
    _m(
        "hanoi", "VN", "cuon-n-roll", "Cuon N Roll Hanoi", "Cuốn N Roll Hà Nội", ("vn-goi-cuon",), 4
    ),
    _m("hanoi", "VN", "cafe-giang", "Cafe Giang", "Cà Phê Giảng", ("vn-egg-coffee",), 5),
    _m("hanoi", "VN", "che-ba-thin", "Che Ba Thin", "Chè Bà Thìn", ("vn-che",), 6),
    _m("ho-chi-minh-city", "VN", "pho-hoa", "Pho Hoa Pasteur", "Phở Hòa Pasteur", ("vn-pho",), 1),
    _m(
        "ho-chi-minh-city",
        "VN",
        "banh-mi-huynh-hoa",
        "Banh Mi Huynh Hoa",
        "Bánh Mì Huỳnh Hoa",
        ("vn-banh-mi",),
        2,
    ),
    _m(
        "ho-chi-minh-city",
        "VN",
        "wrap-roll",
        "Wrap and Roll Hai Ba Trung",
        "Wrap & Roll Hai Bà Trưng",
        ("vn-goi-cuon",),
        3,
    ),
    _m(
        "ho-chi-minh-city",
        "VN",
        "banh-xeo-46a",
        "Banh Xeo 46A",
        "Bánh Xèo 46A",
        ("vn-banh-xeo",),
        4,
    ),
    _m(
        "ho-chi-minh-city",
        "VN",
        "com-tam-ba-ghien",
        "Com Tam Ba Ghien",
        "Cơm Tấm Ba Ghiền",
        ("vn-com-tam",),
        5,
    ),
    _m(
        "ho-chi-minh-city",
        "VN",
        "bun-bo-hue-dong-ba",
        "Bun Bo Hue Dong Ba",
        "Bún Bò Huế Đông Ba",
        ("vn-bun-bo-hue",),
        6,
    ),
    _m(
        "ho-chi-minh-city",
        "VN",
        "che-mam-khanh-vy",
        "Che Mam Khanh Vy",
        "Chè Mâm Khánh Vy",
        ("vn-che",),
        7,
    ),
    _m("da-nang", "VN", "pho-bac-hai", "Pho Bac Hai", "Phở Bắc Hải", ("vn-pho",), 1),
    _m("da-nang", "VN", "banh-mi-ba-lan", "Banh Mi Ba Lan", "Bánh Mì Bà Lan", ("vn-banh-mi",), 2),
    _m("da-nang", "VN", "madame-lan", "Madame Lan", "Madame Lân", ("vn-goi-cuon",), 3),
    _m(
        "da-nang",
        "VN",
        "banh-xeo-ba-duong",
        "Banh Xeo Ba Duong",
        "Bánh Xèo Bà Dưỡng",
        ("vn-banh-xeo",),
        4,
    ),
    _m("da-nang", "VN", "bep-cuon", "Bep Cuon Da Nang", "Bếp Cuốn Đà Nẵng", ("vn-cao-lau",), 5),
    _m(
        "da-nang",
        "VN",
        "bun-bo-ba-thuong",
        "Bun Bo Ba Thuong",
        "Bún Bò Bà Thương",
        ("vn-bun-bo-hue",),
        6,
    ),
    _m("da-nang", "VN", "che-lien", "Che Lien", "Chè Liên", ("vn-che",), 7),
    _m("hue", "VN", "pho-sai-gon", "Pho Sai Gon Hue", "Phở Sài Gòn Huế", ("vn-pho",), 1),
    _m(
        "hue",
        "VN",
        "banh-khoai-hong-mai",
        "Banh Khoai Hong Mai",
        "Bánh Khoái Hồng Mai",
        ("vn-banh-xeo",),
        2,
    ),
    _m(
        "hue",
        "VN",
        "bun-bo-my-tam",
        "Bun Bo Hue My Tam",
        "Bún Bò Huế Mỹ Tâm",
        ("vn-bun-bo-hue",),
        3,
    ),
    _m("hue", "VN", "che-hem", "Che Hem Hue", "Chè Hẻm Huế", ("vn-che",), 4),
    _m("da-lat", "VN", "pho-hieu", "Pho Hieu Da Lat", "Phở Hiếu Đà Lạt", ("vn-pho",), 1),
    _m(
        "da-lat",
        "VN",
        "banh-mi-hoang-dieu",
        "Banh Mi Xiu Mai Hoang Dieu",
        "Bánh Mì Xíu Mại Hoàng Diệu",
        ("vn-banh-mi",),
        2,
    ),
)


MerchantSourceType = Literal["merchant_official", "official_tourism"]
MerchantSourceScope = Literal["merchant_listing", "merchant_website"]
MerchantSourceClaim = Literal["display_name", "address", "official_website"]


@dataclass(frozen=True)
class MerchantDirectSourceSeed:
    merchant_slug: str
    source_type: MerchantSourceType
    source_scope: MerchantSourceScope
    source_title: str
    source_url: str
    claims: tuple[MerchantSourceClaim, ...]
    official_website_url: str | None = None


def _merchant_website(
    merchant_slug: str,
    source_title: str,
    source_url: str,
    *,
    includes_address: bool = False,
) -> MerchantDirectSourceSeed:
    claims: tuple[MerchantSourceClaim, ...] = (
        ("display_name", "address", "official_website")
        if includes_address
        else ("display_name", "official_website")
    )
    return MerchantDirectSourceSeed(
        merchant_slug=merchant_slug,
        source_type="merchant_official",
        source_scope="merchant_website",
        source_title=source_title,
        source_url=source_url,
        claims=claims,
        official_website_url=source_url,
    )


def _official_listing(
    merchant_slug: str,
    source_title: str,
    source_url: str,
    *,
    includes_address: bool = True,
) -> MerchantDirectSourceSeed:
    claims: tuple[MerchantSourceClaim, ...] = (
        ("display_name", "address") if includes_address else ("display_name",)
    )
    return MerchantDirectSourceSeed(
        merchant_slug=merchant_slug,
        source_type="official_tourism",
        source_scope="merchant_listing",
        source_title=source_title,
        source_url=source_url,
        claims=claims,
    )


# Merchant-level evidence verified against first-party merchant sites or government /
# official-tourism listings. Missing merchants intentionally remain pending instead of
# inheriting the destination-level context source as proof that the merchant is listed.
MERCHANT_DIRECT_SOURCE_SEEDS: tuple[MerchantDirectSourceSeed, ...] = (
    # South Korea
    _merchant_website(
        "seoul-korea-house",
        "Korea House official website",
        "https://www.kh.or.kr/kh/eng",
        includes_address=True,
    ),
    _official_listing(
        "seoul-mokmyeoksanbang",
        "Visit Seoul listing for Mokmyeoksanbang",
        "https://english.visitseoul.net/hallyu/NCT-Hot-Young-Seoul-Trip/27243",
    ),
    _official_listing(
        "seoul-woo-lae-oak",
        "Visit Seoul listing for Wooraeok",
        "https://english.visitseoul.net/eat/Wooraeok/ENP003207",
    ),
    _official_listing(
        "seoul-maple-tree-house",
        "Visit Seoul listing for Maple Tree House Itaewon",
        "https://english.visitseoul.net/area/DanpungnamujipItaewon-branch-EN/ENP006582",
    ),
    _official_listing(
        "seoul-mabongnim",
        "Visit Seoul listing for Mabongnim Halmeonijip",
        "https://english.visitseoul.net/attractions/MabongnimHalmeonijip/ENP8wjib6",
    ),
    _official_listing(
        "seoul-tosokchon",
        "Visit Seoul listing for Tosokchon Samgyetang",
        "https://english.visitseoul.net/PalaceArea/TosokchonSamgyetang/ENPywjsmm",
    ),
    # Taiwan
    _merchant_website(
        "taipei-din-tai-fung",
        "Din Tai Fung Taiwan locations",
        "https://www.dintaifung.com.tw/eng/store.php",
        includes_address=True,
    ),
    _merchant_website(
        "taipei-chun-shui-tang",
        "Chun Shui Tang Taiwan locations",
        "https://www.chunshuitang.com.tw/en/",
    ),
    _official_listing(
        "taipei-lan-jia",
        "Taipei City listing for Lan's Taiwanese Sandwich Shop",
        "https://travel.taipei/en/shop/details/619",
    ),
    _official_listing(
        "taipei-chia-te",
        "Taipei City listing for Chia Te Bakery",
        "https://travel.taipei/en/shop/details/549",
    ),
    _official_listing(
        "taichung-qin-yuan-chun",
        "Taichung City listing for Qin Yuan Chun",
        "https://travel.taichung.gov.tw/zh-tw/shop/consume/5448",
    ),
    _merchant_website(
        "taichung-chun-shui-siwei",
        "Chun Shui Tang original store",
        "https://www.chunshuitang.com.tw/location-detail/original_store/",
        includes_address=True,
    ),
    _official_listing(
        "kaohsiung-gang-yuan",
        "Kaohsiung City listing for Gang Yuan Beef Noodles",
        "https://khh.travel/zh-tw/shop/gourmet/810/",
    ),
    _merchant_website(
        "kaohsiung-chun-shui-tang",
        "Chun Shui Tang Kaohsiung locations",
        "https://www.chunshuitang.com.tw/location/taiwan/southern_taiwan/kaohsiung_city/",
    ),
    _merchant_website(
        "kaohsiung-jiu-zhen-nan",
        "Jiu Zhen Nan Taiwan locations",
        "https://www.jzn.com.tw/location",
    ),
    _official_listing(
        "tainan-fu-sheng-hao",
        "Tainan City listing for Fu Sheng Hao",
        "https://www.twtainan.net/zh-tw/shop/consume/2199/",
    ),
    _official_listing(
        "tainan-shi-jing-jiu",
        "Tainan City listing for Shi Jing Jiu Oyster Omelet",
        "https://www.twtainan.net/zh-tw/shop/consume/2075/",
    ),
    _merchant_website(
        "tainan-hanlin",
        "Hanlin Tea Room official website",
        "https://www.hanlin-tea.com.tw/",
    ),
    _official_listing(
        "tainan-a-song-gua-bao",
        "Tainan City listing for A-Song Gua Bao",
        "https://www.twtainan.net/zh-tw/shop/consume/1741/",
    ),
    _merchant_website(
        "tainan-du-xiao-yue",
        "Du Hsiao Yueh Tainan original store",
        "https://noodle1895.com/en/branch-2/tainan-original-store/",
        includes_address=True,
    ),
    # Singapore
    _merchant_website(
        "singapore-tian-tian",
        "Tian Tian Hainanese Chicken Rice official website",
        "https://www.tiantianchickenrice.com.sg/",
    ),
    _merchant_website(
        "singapore-328-katong-laksa",
        "328 Katong Laksa official website",
        "https://www.328katonglaksa.sg/",
        includes_address=True,
    ),
    _merchant_website(
        "singapore-jumbo-riverside",
        "JUMBO Seafood Riverside Point",
        "https://www.jumboseafood.com.sg/en/riverside-point",
        includes_address=True,
    ),
    _official_listing(
        "singapore-hill-street-kway-teow",
        "Singapore Tourism Board food guide listing",
        "https://www.visitsingapore.com/content/dam/desktop/global/deals/hk/Singapore_Food_Guide_PDF.pdf",
    ),
    _merchant_website(
        "singapore-song-fa",
        "Song Fa Bak Kut Teh official locations",
        "https://songfa.com.sg/",
        includes_address=True,
    ),
    _merchant_website(
        "singapore-ya-kun",
        "Ya Kun official store locator",
        "https://app.yakun.com/find-us",
        includes_address=True,
    ),
    _merchant_website(
        "singapore-samys-curry",
        "Samy's Curry official contact page",
        "https://www.samyscurry.com/contact-us/",
        includes_address=True,
    ),
    # Hong Kong
    _merchant_website(
        "hong-kong-tim-ho-wan",
        "Tim Ho Wan Hong Kong official website",
        "https://www.timhowan.com.hk/",
        includes_address=True,
    ),
    _official_listing(
        "hong-kong-yat-lok",
        "Hong Kong Tourism Board listing for Yat Lok Restaurant",
        "https://www.discoverhongkong.com/eng/place-to-go/travel.guide-yat-lok-restaurant.html",
    ),
    _merchant_website(
        "hong-kong-tai-cheong",
        "Tai Cheong Bakery official website",
        "https://www.taicheongbakery.com.hk/en/brands/tai_cheong/index.html",
    ),
    _official_listing(
        "hong-kong-kam-wah",
        "Hong Kong Tourism Board listing for Kam Wah Cafe",
        "https://www.discoverhongkong.com/eng/place-to-go/travel.guide-kam-wah-cafe.html",
    ),
    _official_listing(
        "hong-kong-hing-kee",
        "Hong Kong Tourism Board Temple Street dining guide",
        "https://www.discoverhongkong.com/eng/food-and-drink/local-cuisine-to-try-on-temple-street.html",
    ),
    _official_listing(
        "hong-kong-man-kee",
        "Hong Kong Tourism Board listing for Man Kee Cart Noodle",
        "https://www.discoverhongkong.com/eng/place-to-go/travel.guide-man-kee-cart-noodles.html",
    ),
    _official_listing(
        "hong-kong-trusty-congee",
        "Hong Kong Tourism Board listing for Trusty Congee King",
        "https://www.discoverhongkong.com/eng/travel-guide/qts/restaurants-results/restaurants-details.id18984.congee-king.html",
    ),
    # Thailand
    _merchant_website(
        "bangkok-thipsamai",
        "Thipsamai official locations",
        "https://thipsamai.com/contact-us/",
        includes_address=True,
    ),
    _merchant_website(
        "bangkok-krua-apsorn",
        "Krua Apsorn official website",
        "https://www.krua-apsorn.com/",
        includes_address=True,
    ),
    _official_listing(
        "bangkok-go-ang",
        "Tourism Authority of Thailand listing for Go-Ang Pratunam",
        "https://www.thailandtravel.or.jp/go-ang-kaomunkai-pratunam/",
    ),
    _official_listing(
        "bangkok-kor-panich",
        "Tourism Authority of Thailand listing for K. Panich",
        "https://www.thailandtravel.or.jp/kpanich/",
    ),
    _official_listing(
        "chiang-mai-huen-muan-jai",
        "Tourism Authority of Thailand listing for Huen Muan Jai",
        "https://www.thailandtravel.or.jp/huen-muan-jai/",
    ),
    _official_listing(
        "krabi-ruen-mai",
        "Tourism Authority of Thailand Krabi restaurant guide",
        "https://www.thailandtravel.or.jp/common/pdf/Krabi_trang2019.pdf",
    ),
    # Vietnam
    _merchant_website(
        "hanoi-banh-mi-25",
        "Banh Mi 25 official website",
        "https://banhmi25.net/",
        includes_address=True,
    ),
    _merchant_website(
        "hanoi-cafe-giang",
        "Cafe Giang official website",
        "https://cafegiang.vn/",
        includes_address=True,
    ),
    _merchant_website(
        "da-nang-madame-lan",
        "Madame Lan official website",
        "https://www.madamelan.vn/",
        includes_address=True,
    ),
    _official_listing(
        "da-nang-banh-xeo-ba-duong",
        "Da Nang official food portal listing for Ba Duong Pancake",
        "https://www.foodtourdanang.vn/en/banh-xeo-ba-duong?food=56",
    ),
    _official_listing(
        "da-nang-bep-cuon",
        "Da Nang official food portal 2025 restaurant list",
        "https://foodtourdanang.vn/en/michelin-guide-2025-goi-ten-am-thuc-da-nang-nhung-quan-an-nho-ma-co-vo-chinh-thuc-ghi-danh-tren-ban-do-am-thuc-the-gioi",
    ),
    _official_listing(
        "da-nang-bun-bo-ba-thuong",
        "Da Nang official food portal 2025 restaurant list",
        "https://foodtourdanang.vn/en/michelin-guide-2025-goi-ten-am-thuc-da-nang-nhung-quan-an-nho-ma-co-vo-chinh-thuc-ghi-danh-tren-ban-do-am-thuc-the-gioi",
    ),
    _official_listing(
        "da-nang-che-lien",
        "Da Nang official food portal listing for Che Lien",
        "https://www.foodtourdanang.vn/en/che-lien-da-nang-dien-bien-phu-2?food=106",
    ),
)


def validate_merchant_catalog() -> None:
    slugs = [item.slug for item in MERCHANT_SEEDS]
    if len(slugs) != len(set(slugs)):
        raise RuntimeError("merchant bootstrap slugs must be unique")
    expected_pairs = {
        (destination_id, food.slug)
        for food in FOOD_SEEDS
        for destination_id in food.destination_ids
    }
    actual_pairs = {
        (merchant.destination_id, food_slug)
        for merchant in MERCHANT_SEEDS
        for food_slug in merchant.food_slugs
    }
    if actual_pairs != expected_pairs:
        missing = sorted(expected_pairs - actual_pairs)
        extra = sorted(actual_pairs - expected_pairs)
        raise RuntimeError(f"merchant coverage mismatch; missing={missing}, extra={extra}")
    if len(actual_pairs) != 173:
        raise RuntimeError(f"merchant bootstrap must cover 173 pairs, found {len(actual_pairs)}")
    if any(
        not item.name
        or not item.local_name
        or not item.source_url.startswith("https://")
        or item.destination_id not in OFFICIAL_DESTINATION_FOOD_SOURCES
        for item in MERCHANT_SEEDS
    ):
        raise RuntimeError("merchant bootstrap names and official sources are required")
    merchant_slugs = set(slugs)
    direct_source_keys = [
        (item.merchant_slug, item.source_url) for item in MERCHANT_DIRECT_SOURCE_SEEDS
    ]
    if len(direct_source_keys) != len(set(direct_source_keys)):
        raise RuntimeError("merchant direct-source keys must be unique")
    if any(
        item.merchant_slug not in merchant_slugs
        or not item.source_url.startswith("https://")
        or not item.claims
        or (
            item.official_website_url is not None
            and (
                item.source_scope != "merchant_website"
                or "official_website" not in item.claims
                or not item.official_website_url.startswith("https://")
            )
        )
        for item in MERCHANT_DIRECT_SOURCE_SEEDS
    ):
        raise RuntimeError("merchant direct sources must be scoped, claimed, and HTTPS")


def validate_merchant_taxonomy() -> None:
    merchant_slugs = {item.slug for item in MERCHANT_SEEDS}
    for mapping_name, mapping in (
        ("MERCHANT_AREA_KEYS", MERCHANT_AREA_KEYS),
        ("MERCHANT_EXTRA_CATEGORIES", MERCHANT_EXTRA_CATEGORIES),
    ):
        unknown = sorted(set(mapping) - merchant_slugs)
        if unknown:
            raise RuntimeError(f"{mapping_name} references unknown merchants {unknown}")
    with_area = 0
    for item in MERCHANT_SEEDS:
        categories = item.category_slugs
        if not categories or len(categories) > 6:
            raise RuntimeError(f"merchant {item.slug} must have between one and six categories")
        unknown_categories = [slug for slug in categories if slug not in CATEGORY_SEEDS_BY_SLUG]
        if unknown_categories:
            raise RuntimeError(f"merchant {item.slug} references unknown categories")
        if item.area_slug is None:
            continue
        area = AREA_SEEDS_BY_SLUG.get(item.area_slug)
        if area is None or area.destination_id != item.destination_id:
            raise RuntimeError(f"merchant {item.slug} points at an area outside its destination")
        with_area += 1
    if with_area < 50:
        raise RuntimeError(f"expected at least 50 merchants with a curated area, found {with_area}")


validate_merchant_catalog()
validate_merchant_taxonomy()
