from dataclasses import dataclass, field


@dataclass(frozen=True)
class DestinationProfile:
    code: str
    city: str
    country: str
    country_label: str
    timezone: str
    currency: str
    aliases: tuple[str, ...]
    areas: tuple[str, ...]
    estimated_flight_twd: int
    reason: str
    suggestions: dict[str, tuple[str, ...]] = field(default_factory=dict)


DESTINATIONS: tuple[DestinationProfile, ...] = (
    DestinationProfile(
        "NRT",
        "東京",
        "Japan",
        "日本",
        "Asia/Tokyo",
        "JPY",
        ("東京", "东京", "Tokyo", "NRT", "HND", "TYO"),
        ("新宿", "上野／淺草", "東京站／銀座", "澀谷"),
        9_400,
        "航班、住宿與跨區交通選擇最完整",
        {
            "food": ("築地場外市場早餐", "淺草老舖與甜點散步", "新宿居酒屋晚餐"),
            "shopping": ("銀座與有樂町選物", "澀谷原宿購物散步", "上野阿美橫町採買"),
            "culture": ("淺草寺與合羽橋散步", "上野博物館與公園", "神樂坂文化街區"),
            "nature": ("明治神宮與代代木公園", "濱離宮庭園", "高尾山近郊健行"),
            "family": ("台場親子體驗", "上野動物園與公園", "東京灣親子散步"),
            "nightlife": ("澀谷夜景與巷弄餐酒館", "新宿夜間街區", "東京車站夜景散步"),
        },
    ),
    DestinationProfile(
        "KIX",
        "大阪／京都",
        "Japan",
        "日本",
        "Asia/Tokyo",
        "JPY",
        ("大阪", "京都", "Osaka", "Kyoto", "KIX", "ITM", "OSA"),
        ("難波／心齋橋", "梅田", "京都站", "四條河原町"),
        8_600,
        "美食、購物與京都文化可在同一旅程搭配",
        {
            "food": ("黑門市場與難波美食", "道頓堀晚餐散步", "京都錦市場小吃"),
            "shopping": ("心齋橋與堀江選物", "梅田百貨與地下街", "京都河原町購物"),
            "culture": ("京都祇園與八坂神社", "大阪城與歷史街區", "伏見稻荷早晨散步"),
            "nature": ("嵐山竹林與河岸", "大阪中之島公園", "京都哲學之道"),
            "family": ("大阪灣親子景點", "天王寺公園與動物園", "京都鐵道博物館"),
            "nightlife": ("難波夜間美食巡禮", "梅田夜景", "京都先斗町晚餐"),
        },
    ),
    DestinationProfile(
        "FUK",
        "福岡",
        "Japan",
        "日本",
        "Asia/Tokyo",
        "JPY",
        ("福岡", "博多", "Fukuoka", "Hakata", "FUK"),
        ("博多站", "天神", "中洲", "大濠公園"),
        7_200,
        "機場離市區近，適合三至五日美食旅行",
        {
            "food": ("柳橋連合市場早餐", "博多拉麵與屋台晚餐", "天神在地咖啡巡禮"),
            "shopping": ("天神地下街與百貨", "博多站商場採買", "大名選物散步"),
            "culture": ("櫛田神社與博多町家", "太宰府文化一日遊", "福岡市博物館"),
            "nature": ("大濠公園與舞鶴公園", "海之中道近郊散步", "糸島海岸半日遊"),
            "family": ("海之中道親子一日", "福岡市科學館", "博多運河城親子時段"),
        },
    ),
    DestinationProfile(
        "CTS",
        "札幌",
        "Japan",
        "日本",
        "Asia/Tokyo",
        "JPY",
        ("札幌", "北海道", "Sapporo", "Hokkaido", "CTS"),
        ("札幌站", "大通", "薄野", "中島公園"),
        11_800,
        "四季自然、溫泉與北海道美食主題鮮明",
        {
            "food": ("二條市場海鮮早餐", "札幌拉麵與甜點", "薄野北海道晚餐"),
            "shopping": ("札幌站商場", "狸小路商店街", "大通地下街"),
            "culture": ("北海道廳舊本廳舍周邊", "札幌啤酒博物館", "北海道開拓村"),
            "nature": ("藻岩山與札幌夜景", "小樽運河近郊一日", "定山溪溫泉散步"),
            "spa": ("定山溪溫泉慢旅", "札幌市區湯屋", "登別溫泉近郊一日"),
        },
    ),
    DestinationProfile(
        "OKA",
        "沖繩",
        "Japan",
        "日本",
        "Asia/Tokyo",
        "JPY",
        ("沖繩", "那霸", "Okinawa", "Naha", "OKA"),
        ("國際通", "那霸新都心", "北谷", "恩納"),
        9_800,
        "海島、親子與自駕路線適合放慢步調",
        {
            "food": ("第一牧志公設市場", "沖繩麵與島料理", "北谷海景晚餐"),
            "shopping": ("國際通與壺屋通", "那霸新都心採買", "瀨長島選物"),
            "culture": ("首里城公園與城下町", "壺屋陶器街", "沖繩縣立博物館"),
            "nature": ("萬座毛海岸", "古宇利島環島", "沖繩北部森林散步"),
            "family": ("沖繩美麗海水族館", "名護親子景點", "瀨長島親子散步"),
            "beach": ("恩納海岸半日", "北谷日落海灘", "古宇利島海景路線"),
        },
    ),
    DestinationProfile(
        "NGO",
        "名古屋",
        "Japan",
        "日本",
        "Asia/Tokyo",
        "JPY",
        ("名古屋", "Nagoya", "NGO"),
        ("名古屋站", "榮", "伏見", "金山"),
        9_100,
        "適合串聯中部城市、主題樂園與在地美食",
        {
            "food": ("柳橋中央市場早餐", "名古屋飯與味噌料理", "榮地下街美食"),
            "shopping": ("名古屋站商場", "榮商圈", "大須商店街"),
            "culture": ("名古屋城與本丸御殿", "德川美術館", "有松老街"),
            "family": ("名古屋港親子一日", "鐵道館親子體驗", "近郊主題樂園"),
        },
    ),
    DestinationProfile(
        "ICN",
        "首爾",
        "South Korea",
        "韓國",
        "Asia/Seoul",
        "KRW",
        ("首爾", "首尔", "Seoul", "仁川", "Incheon", "ICN", "GMP", "SEL"),
        ("明洞", "弘大", "東大門", "江南"),
        7_800,
        "購物、美食、展覽與夜間活動密度高",
        {
            "food": ("廣藏市場早午餐", "望遠市場在地小吃", "乙支路烤肉晚餐"),
            "shopping": ("聖水洞選物與咖啡", "明洞與南大門採買", "弘大延南洞散步"),
            "culture": ("景福宮與北村韓屋", "國立中央博物館", "西村文化街區"),
            "nature": ("漢江公園散步", "首爾林", "北漢山輕健行"),
            "nightlife": ("乙支路巷弄夜生活", "弘大夜間散步", "漢江夜景"),
            "spa": ("韓式汗蒸幕體驗", "江南療癒半日", "市區美容與休息時段"),
        },
    ),
    DestinationProfile(
        "PUS",
        "釜山",
        "South Korea",
        "韓國",
        "Asia/Seoul",
        "KRW",
        ("釜山", "Busan", "PUS"),
        ("西面", "南浦洞", "海雲台", "廣安里"),
        8_200,
        "海景、市場與城市交通適合四至五日慢遊",
        {
            "food": ("札嘎其市場海鮮", "南浦洞在地小吃", "西面豬肉湯飯"),
            "shopping": ("西面地下街", "南浦洞商圈", "新世界百貨採買"),
            "culture": ("甘川文化村", "影島文化空間", "釜山近代歷史館"),
            "nature": ("太宗台海岸步道", "冬柏島散步", "松島海岸路線"),
            "beach": ("海雲台海岸半日", "廣安里日落與夜景", "松亭海灘慢遊"),
            "nightlife": ("廣安里夜景晚餐", "海雲台夜間散步", "西面餐酒館"),
        },
    ),
    DestinationProfile(
        "CJU",
        "濟州",
        "South Korea",
        "韓國",
        "Asia/Seoul",
        "KRW",
        ("濟州", "济州", "Jeju", "CJU"),
        ("濟州市", "涯月", "中文觀光區", "西歸浦"),
        9_600,
        "海岸、咖啡與自然步道適合自駕或包車",
        {
            "food": ("東門市場早午餐", "濟州黑豬肉晚餐", "海女海鮮料理"),
            "nature": ("城山日出峰", "漢拏山周邊步道", "偶來小路海岸散步"),
            "beach": ("涯月海岸咖啡路線", "咸德海水浴場", "中文海岸半日"),
            "family": ("濟州親子博物館", "西歸浦親子農場", "海岸親子慢遊"),
            "spa": ("濟州療癒森林", "海景休息與汗蒸", "西歸浦慢旅日"),
        },
    ),
    DestinationProfile(
        "BKK",
        "曼谷",
        "Thailand",
        "泰國",
        "Asia/Bangkok",
        "THB",
        ("曼谷", "Bangkok", "BKK", "DMK"),
        ("暹羅", "Asok／素坤逸", "Silom", "河濱"),
        8_500,
        "美食、購物、寺廟與按摩行程選擇豐富",
        {
            "food": ("早晨市場與泰式早餐", "唐人街晚餐巡禮", "在地餐廳與甜點"),
            "shopping": ("暹羅商圈", "恰圖恰週末市集", "河濱夜市"),
            "culture": ("大皇宮與臥佛寺", "昭披耶河文化路線", "曼谷藝術文化中心"),
            "nightlife": ("昭披耶河夜景", "通羅餐酒館", "曼谷夜市散步"),
            "spa": ("泰式按摩與療癒時段", "市區水療半日", "河濱放鬆行程"),
            "family": ("暹羅親子景點", "河濱親子半日", "曼谷城市公園"),
        },
    ),
    DestinationProfile(
        "CNX",
        "清邁",
        "Thailand",
        "泰國",
        "Asia/Bangkok",
        "THB",
        ("清邁", "Chiang Mai", "CNX"),
        ("古城", "尼曼區", "湄平河畔", "夜市周邊"),
        10_500,
        "古城、咖啡、手作與近郊自然適合慢旅行",
        {
            "food": ("清邁市場與北泰早餐", "尼曼咖啡散步", "夜市北泰料理"),
            "shopping": ("週末步行街", "瓦洛洛市場", "尼曼設計選物"),
            "culture": ("清邁古城寺廟散步", "素帖山雙龍寺", "蘭納文化館"),
            "nature": ("茵他儂山近郊一日", "湄林自然路線", "皇家公園散步"),
            "spa": ("蘭納按摩與水療", "古城療癒半日", "尼曼慢活時段"),
        },
    ),
    DestinationProfile(
        "HKT",
        "普吉",
        "Thailand",
        "泰國",
        "Asia/Bangkok",
        "THB",
        ("普吉", "普吉島", "Phuket", "HKT"),
        ("普吉老城", "芭東", "卡塔", "卡隆"),
        10_800,
        "海灘、跳島、度假村與夜生活可自由組合",
        {
            "food": ("普吉老城早午餐", "海鮮市場晚餐", "南洋風味料理"),
            "culture": ("普吉老城建築散步", "查龍寺", "在地文化館"),
            "nature": ("攀牙灣自然一日", "普吉南端觀景路線", "海岸森林散步"),
            "beach": ("卡塔海灘慢遊", "珊瑚島跳島", "芭東海灘日落"),
            "nightlife": ("芭東夜間街區", "海灘日落餐酒館", "普吉老城夜市"),
            "spa": ("度假村水療半日", "泰式按摩放鬆", "海景療癒時段"),
        },
    ),
    DestinationProfile(
        "KBV",
        "喀比",
        "Thailand",
        "泰國",
        "Asia/Bangkok",
        "THB",
        ("喀比", "甲米", "Krabi", "KBV"),
        ("奧南", "喀比鎮", "萊雷", "克隆芒"),
        11_200,
        "島嶼、石灰岩海岸與悠閒度假節奏鮮明",
        {
            "food": ("喀比鎮市場早餐", "奧南海鮮晚餐", "週末夜市小吃"),
            "nature": ("虎窟寺與自然景觀", "翡翠池近郊一日", "紅樹林生態路線"),
            "beach": ("四島跳島一日", "萊雷海灘半日", "奧南日落散步"),
            "spa": ("奧南水療半日", "溫泉瀑布療癒路線", "海景按摩時段"),
            "family": ("四島親子路線", "奧南海灘慢遊", "喀比鎮親子夜市"),
        },
    ),
)


_BY_CODE: dict[str, DestinationProfile] = {}
for _destination in DESTINATIONS:
    _BY_CODE[_destination.code] = _destination
    for _alias in _destination.aliases:
        if len(_alias) == 3 and _alias.isascii():
            _BY_CODE[_alias.upper()] = _destination


def destination_for_code(code: str | None) -> DestinationProfile | None:
    return _BY_CODE.get((code or "").upper())


def match_destination(text: str) -> DestinationProfile | None:
    folded = text.casefold()
    for destination in DESTINATIONS:
        if any(alias.casefold() in folded for alias in destination.aliases):
            return destination
    return None


def infer_destination_region(text: str) -> str | None:
    matched = match_destination(text)
    if matched:
        return matched.country
    region_aliases = {
        "Japan": ("日本", "japan"),
        "South Korea": ("韓國", "韩国", "南韓", "south korea", "korea"),
        "Thailand": ("泰國", "泰国", "thailand"),
    }
    folded = text.casefold()
    return next(
        (
            region
            for region, aliases in region_aliases.items()
            if any(alias in folded for alias in aliases)
        ),
        None,
    )
