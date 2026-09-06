"""Site-locale text for the destination catalog.

``catalog.py`` carries each destination once, in Traditional Chinese, because that is
the language the catalog was written and reviewed in. The public endpoints render a
destination in the reader's locale from here: the city name, the country label and the
one-line reason. ``zh-TW`` is the catalog's own text and is never duplicated below.

Aliases and interest suggestions stay in the catalog's language on purpose: they are
search terms, and a translation nobody has checked against a map is worse than the
local script. Areas follow that rule too — they are just no longer stuck, because
``app.hotspots.areas`` already carries the same districts with names that were checked
against a map when their circles were drawn. ``area_labels`` reuses those and falls
back to the catalog's own text for anything the reviewed catalog has never heard of.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Final

from app.destinations.catalog import DESTINATIONS, DestinationProfile
from app.hotspots.areas import HOTSPOT_AREAS, HotspotArea, area_name
from app.i18n import LOCALES, Locale

DESTINATIONS_BY_ID: Final[Mapping[str, DestinationProfile]] = {
    profile.id: profile for profile in DESTINATIONS
}
# The rows outside the catalog carry an ISO code rather than the catalog's country name.
COUNTRY_BY_CODE: Final[Mapping[str, str]] = {
    "JP": "Japan",
    "KR": "South Korea",
    "TH": "Thailand",
    "TW": "Taiwan",
    "SG": "Singapore",
    "HK": "Hong Kong",
    "VN": "Vietnam",
}

TranslatedLocale = Locale  # every locale but zh-TW appears in the tables below
TRANSLATED: Final[tuple[Locale, ...]] = ("en", "ja", "ko", "zh-CN")

COUNTRY_LABELS: Final[Mapping[str, Mapping[str, str]]] = {
    "Japan": {"en": "Japan", "ja": "日本", "ko": "일본", "zh-CN": "日本"},
    "South Korea": {"en": "South Korea", "ja": "韓国", "ko": "한국", "zh-CN": "韩国"},
    "Thailand": {"en": "Thailand", "ja": "タイ", "ko": "태국", "zh-CN": "泰国"},
    "Taiwan": {"en": "Taiwan", "ja": "台湾", "ko": "대만", "zh-CN": "台湾"},
    "Singapore": {"en": "Singapore", "ja": "シンガポール", "ko": "싱가포르", "zh-CN": "新加坡"},
    "Hong Kong": {"en": "Hong Kong", "ja": "香港", "ko": "홍콩", "zh-CN": "香港"},
    "Vietnam": {"en": "Vietnam", "ja": "ベトナム", "ko": "베트남", "zh-CN": "越南"},
}

CITY_NAMES: Final[Mapping[str, Mapping[str, str]]] = {
    "tokyo": {"en": "Tokyo", "ja": "東京", "ko": "도쿄", "zh-CN": "东京"},
    "osaka-kyoto": {
        "en": "Osaka & Kyoto",
        "ja": "大阪／京都",
        "ko": "오사카／교토",
        "zh-CN": "大阪／京都",
    },
    "fukuoka": {"en": "Fukuoka", "ja": "福岡", "ko": "후쿠오카", "zh-CN": "福冈"},
    "sapporo": {"en": "Sapporo", "ja": "札幌", "ko": "삿포로", "zh-CN": "札幌"},
    "okinawa": {"en": "Okinawa", "ja": "沖縄", "ko": "오키나와", "zh-CN": "冲绳"},
    "nagoya": {"en": "Nagoya", "ja": "名古屋", "ko": "나고야", "zh-CN": "名古屋"},
    "seoul": {"en": "Seoul", "ja": "ソウル", "ko": "서울", "zh-CN": "首尔"},
    "busan": {"en": "Busan", "ja": "釜山", "ko": "부산", "zh-CN": "釜山"},
    "jeju": {"en": "Jeju", "ja": "済州", "ko": "제주", "zh-CN": "济州"},
    "bangkok": {"en": "Bangkok", "ja": "バンコク", "ko": "방콕", "zh-CN": "曼谷"},
    "chiang-mai": {"en": "Chiang Mai", "ja": "チェンマイ", "ko": "치앙마이", "zh-CN": "清迈"},
    "phuket": {"en": "Phuket", "ja": "プーケット", "ko": "푸껫", "zh-CN": "普吉"},
    "krabi": {"en": "Krabi", "ja": "クラビ", "ko": "끄라비", "zh-CN": "甲米"},
    "taipei": {"en": "Taipei", "ja": "台北", "ko": "타이베이", "zh-CN": "台北"},
    "singapore": {"en": "Singapore", "ja": "シンガポール", "ko": "싱가포르", "zh-CN": "新加坡"},
    "hong-kong": {"en": "Hong Kong", "ja": "香港", "ko": "홍콩", "zh-CN": "香港"},
    "hanoi": {"en": "Hanoi", "ja": "ハノイ", "ko": "하노이", "zh-CN": "河内"},
    "ho-chi-minh-city": {
        "en": "Ho Chi Minh City",
        "ja": "ホーチミン",
        "ko": "호찌민",
        "zh-CN": "胡志明市",
    },
    "da-nang": {"en": "Da Nang", "ja": "ダナン", "ko": "다낭", "zh-CN": "岘港"},
    "taichung": {"en": "Taichung", "ja": "台中", "ko": "타이중", "zh-CN": "台中"},
    "kaohsiung": {"en": "Kaohsiung", "ja": "高雄", "ko": "가오슝", "zh-CN": "高雄"},
    "sendai": {"en": "Sendai", "ja": "仙台", "ko": "센다이", "zh-CN": "仙台"},
    "kanazawa": {"en": "Kanazawa", "ja": "金沢", "ko": "가나자와", "zh-CN": "金泽"},
    "hiroshima": {"en": "Hiroshima", "ja": "広島", "ko": "히로시마", "zh-CN": "广岛"},
    "daegu": {"en": "Daegu", "ja": "大邱", "ko": "대구", "zh-CN": "大邱"},
    "chiang-rai": {"en": "Chiang Rai", "ja": "チェンライ", "ko": "치앙라이", "zh-CN": "清莱"},
    "da-lat": {"en": "Da Lat", "ja": "ダラット", "ko": "달랏", "zh-CN": "大叻"},
    "tainan": {"en": "Tainan", "ja": "台南", "ko": "타이난", "zh-CN": "台南"},
    "gyeongju": {"en": "Gyeongju", "ja": "慶州", "ko": "경주", "zh-CN": "庆州"},
    "jeonju": {"en": "Jeonju", "ja": "全州", "ko": "전주", "zh-CN": "全州"},
    "hue": {"en": "Hue", "ja": "フエ", "ko": "후에", "zh-CN": "顺化"},
    "yokohama": {"en": "Yokohama", "ja": "横浜", "ko": "요코하마", "zh-CN": "横滨"},
    "kamakura": {"en": "Kamakura", "ja": "鎌倉", "ko": "가마쿠라", "zh-CN": "镰仓"},
}

REASONS: Final[Mapping[str, Mapping[str, str]]] = {
    "tokyo": {
        "en": "The widest choice of flights, stays and cross-city transport",
        "ja": "航空便・宿泊・都市間交通の選択肢が最も豊富",
        "ko": "항공편·숙소·도시 간 교통 선택지가 가장 풍부합니다",
        "zh-CN": "航班、住宿与跨区交通选择最完整",
    },
    "osaka-kyoto": {
        "en": "Osaka's food and shopping with Kyoto's culture in one trip",
        "ja": "大阪のグルメ・買い物と京都の文化を一度の旅で",
        "ko": "오사카의 미식·쇼핑과 교토의 문화를 한 여행에",
        "zh-CN": "美食、购物与京都文化可在同一旅程搭配",
    },
    "fukuoka": {
        "en": "Airport minutes from downtown; a three-to-five-day food trip",
        "ja": "空港から市街地が近く、3〜5日のグルメ旅に最適",
        "ko": "공항이 도심과 가까워 3~5일 미식 여행에 적합합니다",
        "zh-CN": "机场离市区近，适合三至五日美食旅行",
    },
    "sapporo": {
        "en": "Four seasons of nature, hot springs and Hokkaido food",
        "ja": "四季の自然、温泉、北海道グルメがテーマ",
        "ko": "사계절 자연, 온천, 홋카이도 미식이 뚜렷한 테마",
        "zh-CN": "四季自然、温泉与北海道美食主题鲜明",
    },
    "okinawa": {
        "en": "Island beaches, family days and a slow self-drive pace",
        "ja": "離島・家族旅行・ドライブ向きのゆったりした旅",
        "ko": "섬 해변, 가족 여행, 렌터카 드라이브로 느긋하게",
        "zh-CN": "海岛、亲子与自驾路线适合放慢步调",
    },
    "nagoya": {
        "en": "A base for central Japan, theme parks and local food",
        "ja": "中部の都市、テーマパーク、ご当地グルメを結ぶ拠点",
        "ko": "주부 지역 도시, 테마파크, 현지 미식을 잇는 거점",
        "zh-CN": "适合串联中部城市、主题乐园与在地美食",
    },
    "seoul": {
        "en": "Dense with shopping, food, exhibitions and nightlife",
        "ja": "買い物・グルメ・展示・ナイトライフが密集",
        "ko": "쇼핑, 미식, 전시, 야간 활동이 밀집한 도시",
        "zh-CN": "购物、美食、展览与夜间活动密度高",
    },
    "busan": {
        "en": "Sea views, markets and easy transit for a four-to-five-day stay",
        "ja": "海の景色、市場、便利な交通で4〜5日ゆっくり",
        "ko": "바다 풍경, 시장, 편리한 교통으로 4~5일 여유롭게",
        "zh-CN": "海景、市场与城市交通适合四至五日慢游",
    },
    "jeju": {
        "en": "Coast, cafés and nature trails, best by car or private driver",
        "ja": "海岸、カフェ、自然の散策路をドライブや貸切車で",
        "ko": "해안, 카페, 자연 산책로를 렌터카나 전세 차량으로",
        "zh-CN": "海岸、咖啡与自然步道适合自驾或包车",
    },
    "bangkok": {
        "en": "Endless food, shopping, temples and massage",
        "ja": "グルメ、買い物、寺院、マッサージの選択肢が豊富",
        "ko": "미식, 쇼핑, 사원, 마사지 선택지가 풍부합니다",
        "zh-CN": "美食、购物、寺庙与按摩行程选择丰富",
    },
    "chiang-mai": {
        "en": "Old town, cafés, crafts and nearby nature for slow travel",
        "ja": "旧市街、カフェ、手仕事、郊外の自然でスローな旅",
        "ko": "옛 시가지, 카페, 수공예, 근교 자연으로 느린 여행",
        "zh-CN": "古城、咖啡、手作与近郊自然适合慢旅行",
    },
    "phuket": {
        "en": "Beaches, island hopping, resorts and nightlife, mixed as you like",
        "ja": "ビーチ、アイランドホッピング、リゾート、ナイトライフを自由に",
        "ko": "해변, 섬 투어, 리조트, 나이트라이프를 자유롭게 조합",
        "zh-CN": "海滩、跳岛、度假村与夜生活可自由组合",
    },
    "krabi": {
        "en": "Islands, limestone coast and an unhurried resort pace",
        "ja": "島々、石灰岩の海岸、のんびりしたリゾートのリズム",
        "ko": "섬, 석회암 해안, 여유로운 리조트 리듬",
        "zh-CN": "岛屿、石灰岩海岸与悠闲度假节奏鲜明",
    },
    "taipei": {
        "en": "Easy transit; food, culture and nearby nature for a short trip",
        "ja": "交通が便利で、グルメ・文化・近郊の自然が短い旅に最適",
        "ko": "교통이 편리하고 미식·문화·근교 자연이 짧은 여행에 적합",
        "zh-CN": "交通便利，美食、文化与近郊自然适合短天数旅行",
    },
    "singapore": {
        "en": "Compact and easy to get around: family, food and many cultures at once",
        "ja": "コンパクトで交通が簡単、家族・グルメ・多文化を一度に",
        "ko": "도시가 콤팩트하고 교통이 쉬워 가족·미식·다문화를 한 번에",
        "zh-CN": "城市紧凑、交通简单，亲子、美食与多元文化可一次体验",
    },
    "hong-kong": {
        "en": "Skyline, dim sum, shopping and outlying islands close together",
        "ja": "都市の景観、飲茶、買い物、離島ルートが密集",
        "ko": "도시 경관, 딤섬, 쇼핑, 섬 코스가 가까이 모여 있습니다",
        "zh-CN": "城市景观、饮茶、购物与离岛路线密度高",
    },
    "hanoi": {
        "en": "Old Quarter streets, coffee and history, best explored on foot",
        "ja": "旧市街、コーヒー、歴史文化を歩いてゆっくり",
        "ko": "구시가지 골목, 커피, 역사 문화를 천천히 걸으며",
        "zh-CN": "老城街区、咖啡与历史文化适合慢步探索",
    },
    "ho-chi-minh-city": {
        "en": "French architecture, markets, food and nightlife in one district",
        "ja": "フランス風建築、市場、グルメ、ナイトライフが集中",
        "ko": "프랑스식 건축, 시장, 미식, 나이트라이프가 집중",
        "zh-CN": "法式建筑、市场、美食与夜生活集中",
    },
    "da-nang": {
        "en": "Beaches, mountains and Hoi An's old town for a slow holiday",
        "ja": "ビーチ、山の景色、ホイアン旧市街でゆったりリゾート",
        "ko": "해변, 산 풍경, 호이안 옛 시가지로 느긋한 휴양",
        "zh-CN": "海滩、山景与会安古城适合度假慢游",
    },
    "taichung": {
        "en": "Old-town streets, cultural districts and nearby mountains and sea",
        "ja": "旧市街、文化エリア、山と海の近郊をゆっくり",
        "ko": "옛 시가지, 문화 지구, 산과 바다 근교를 느긋하게",
        "zh-CN": "老城街区、文化聚落与山海近郊适合慢游",
    },
    "kaohsiung": {
        "en": "Harbour views, old-town culture and southern Taiwan food",
        "ja": "港町の景観、旧市街の文化、南台湾グルメが集中",
        "ko": "항구 도시 경관, 옛 시가지 문화, 남부 대만 미식이 집중",
        "zh-CN": "港都景观、老城文化与南台湾美食集中",
    },
    "sendai": {
        "en": "Castle-town culture, Tohoku food and nearby Matsushima in any season",
        "ja": "城下町文化、東北グルメ、松島近郊で四季の旅",
        "ko": "성하마을 문화, 도호쿠 미식, 마쓰시마 근교로 사계절 일정",
        "zh-CN": "城下町文化、东北美食与松岛近郊可组成四季行程",
    },
    "kanazawa": {
        "en": "Crafts, teahouse streets and Hokuriku food for a cultural deep dive",
        "ja": "工芸、茶屋街、北陸の食で文化を深く味わう旅",
        "ko": "공예, 찻집 거리, 호쿠리쿠 음식으로 깊이 있는 문화 여행",
        "zh-CN": "工艺、茶屋街与北陆饮食适合文化深度旅行",
    },
    "hiroshima": {
        "en": "Peace memorials, Seto Inland Sea views and Miyajima: history and nature together",
        "ja": "平和の記憶、瀬戸内の景観、宮島で歴史と自然を",
        "ko": "평화의 기억, 세토내해 풍경, 미야지마로 역사와 자연을 함께",
        "zh-CN": "和平文化、濑户内景观与宫岛可兼顾历史及自然",
    },
    "daegu": {
        "en": "Markets, early-modern streets and hillside views with a local feel",
        "ja": "市場、近代の街並み、山あいの景観に地元の暮らしを感じる",
        "ko": "시장, 근대 거리, 산성 풍경에 현지 생활감이 있는 도시",
        "zh-CN": "市场、近代街区与山城景观兼具在地生活感",
    },
    "chiang-rai": {
        "en": "Lanna art, mountain nature and local markets at a slow pace",
        "ja": "ランナー芸術、山の自然、地元市場をゆっくり",
        "ko": "란나 예술, 산악 자연, 지역 시장을 느린 속도로",
        "zh-CN": "兰纳艺术、山区自然与地方市场适合慢节奏探索",
    },
    "da-lat": {
        "en": "Highland climate, French quarter, gardens and coffee farms for slow travel",
        "ja": "高原の気候、フランス風の街並み、庭園、コーヒー産地をゆっくり",
        "ko": "고원 기후, 프랑스풍 거리, 정원, 커피 산지를 깊이 있게",
        "zh-CN": "高原气候、法式街区、花园与咖啡产地适合深度慢游",
    },
    "tainan": {
        "en": "A day trip from Kaohsiung: old-capital heritage, lanes and food",
        "ja": "高雄から足を延ばす旧都の史跡、路地、食の日帰り",
        "ko": "가오슝에서 가는 옛 수도의 유적, 골목, 음식 당일 여행",
        "zh-CN": "由高雄延伸的府城古迹、巷弄与饮食一日行程",
    },
    "gyeongju": {
        "en": "A day trip from Busan to the old Silla capital",
        "ja": "釜山から足を延ばす新羅の古都への日帰り",
        "ko": "부산에서 가는 신라 천년 고도 당일 여행",
        "zh-CN": "由釜山延伸的新罗古都文化一日行程",
    },
    "jeonju": {
        "en": "A day trip from Seoul: hanok village, food and local crafts",
        "ja": "ソウルから足を延ばす韓屋、食、地元工芸の日帰り",
        "ko": "서울에서 가는 한옥, 음식, 지역 공예 당일 여행",
        "zh-CN": "由首尔延伸的韩屋、饮食与地方工艺一日行程",
    },
    "hue": {
        "en": "A day trip from Da Nang: the Nguyen capital, the Perfume River and local food",
        "ja": "ダナンから足を延ばす阮朝の古都、フォン川、地元料理の日帰り",
        "ko": "다낭에서 가는 응우옌 왕조 고도, 흐엉강, 지역 음식 당일 여행",
        "zh-CN": "由岘港延伸的阮朝古都、香江与地方饮食一日行程",
    },
    "yokohama": {
        "en": "A day trip from Tokyo: harbour lights, Chinatown and the Red Brick Warehouse",
        "ja": "東京から足を延ばす港の夜景、中華街、赤レンガ倉庫の日帰り",
        "ko": "도쿄에서 가는 항구 야경, 차이나타운, 붉은 벽돌 창고 당일 여행",
        "zh-CN": "由东京延伸的港湾夜景、中华街与红砖仓库一日行程",
    },
    "kamakura": {
        "en": "A day trip from Tokyo: old-capital temples, the Great Buddha and the Enoden coast",
        "ja": "東京から足を延ばす古都の寺社、大仏、江ノ電の海岸の日帰り",
        "ko": "도쿄에서 가는 옛 수도의 사찰, 대불, 에노덴 해안 당일 여행",
        "zh-CN": "由东京延伸的古都寺社、大佛与江之电海岸一日行程",
    },
}


def city_name(profile: DestinationProfile, locale: Locale) -> str:
    """The city as the reader would write it; the catalog's own text for zh-TW."""
    if locale == "zh-TW":
        return profile.city
    return CITY_NAMES.get(profile.id, {}).get(locale) or profile.english_name or profile.city


def city_name_for(destination_id: str | None, locale: Locale, fallback: str) -> str:
    """The city as the reader would write it, addressed by destination id.

    The rows that carry place names outside the catalog — hotspots, merchants — know
    their ``destination_id`` but not the profile, and they store the catalog's own
    Traditional Chinese in ``city_name``. Passing that as ``fallback`` keeps a city the
    catalog has never heard of readable instead of turning it into an id.
    """
    if locale == "zh-TW" or not destination_id:
        return fallback
    profile = DESTINATIONS_BY_ID.get(destination_id)
    if profile is None:
        return CITY_NAMES.get(destination_id, {}).get(locale) or fallback
    return city_name(profile, locale)


def english_name(profile: DestinationProfile) -> str:
    """The destination's English name, for the field that claims to hold one.

    19 of the 33 catalog rows leave ``english_name`` unset, and every reader fell back
    to ``profile.city`` — the Traditional Chinese name — so a field called english_name
    returned Chinese. ``CITY_NAMES`` already carries a checked English name for all 33,
    so the fallback goes there first and only then to the catalog text.
    """
    return profile.english_name or CITY_NAMES.get(profile.id, {}).get("en") or profile.city


def country_label_for(country_code: str | None, locale: Locale, fallback: str) -> str:
    """The country as the reader would write it, addressed by ISO code."""
    if locale == "zh-TW" or not country_code:
        return fallback
    country = COUNTRY_BY_CODE.get(country_code.upper())
    if country is None:
        return fallback
    return COUNTRY_LABELS.get(country, {}).get(locale) or fallback


def country_label(profile: DestinationProfile, locale: Locale) -> str:
    if locale == "zh-TW":
        return profile.country_label
    return COUNTRY_LABELS.get(profile.country, {}).get(locale) or profile.country


def reason(profile: DestinationProfile, locale: Locale) -> str:
    if locale == "zh-TW":
        return profile.reason
    return REASONS.get(profile.id, {}).get(locale) or profile.reason


# Both catalogs write a two-part district the same way but with their own connector:
# 「上野／淺草」, 「上野・浅草」, 「명동·남산」, "Ueno & Asakusa". Splitting on all of them lets
# one side's 「澀谷」 find its half of the other side's 「澀谷／原宿」. A name that explains
# itself in brackets — "Osaka Bay (Tempozan & USJ)" — is never split: the bracket, not
# the connector inside it, is what the reader is reading.
AREA_SEGMENT: Final[re.Pattern[str]] = re.compile(r"\s*(?:[／/・·&,、]|\band\b)\s*")
AREA_JOIN: Final[Mapping[str, str]] = {"en": " & ", "ja": "・", "ko": "·", "zh-CN": "／"}

# The 15 lodging areas with no entry in the coordinate-reviewed catalog, keyed by the
# destination and the catalog's own text. Only ``en`` is required: ja and ko fall back
# to it exactly as ``app.hotspots.areas.area_name`` does, and zh-CN is listed only where
# the Simplified spelling differs from the Traditional one, so this table stays a list
# of the differences a reader can check rather than 60 restatements.
#
# Checked one by one: Wikipedia's own interlanguage links for 濟州市 (Jeju City / 済州市 /
# 제주시 / 济州市), Silom (是隆路 / シーロム通り), 中西區 (West Central District / 中西区)
# and 韓屋村 (전주한옥마을); ko.wikipedia's 완산동 article for 완산공원; ja.wikipedia for
# 青葉通り. The rest are the standard romanisations of names that are already Latin or
# already Japanese (Nimman, Klong Muang, Night Bazaar, Riverside, Old Town, 国分町,
# 紙屋町, West District, Hai'an Road).
AREA_NAMES: Final[Mapping[tuple[str, str], Mapping[str, str]]] = {
    ("jeju", "濟州市"): {"en": "Jeju City", "ja": "済州市", "ko": "제주시", "zh-CN": "济州市"},
    ("bangkok", "Silom"): {"en": "Silom", "ja": "シーロム", "zh-CN": "是隆"},
    ("chiang-mai", "尼曼區"): {"en": "Nimman", "zh-CN": "尼曼区"},
    ("chiang-mai", "夜市周邊"): {"en": "Night Bazaar", "zh-CN": "夜市周边"},
    ("krabi", "克隆芒"): {"en": "Klong Muang"},
    ("taichung", "西區"): {"en": "West District", "zh-CN": "西区"},
    ("sendai", "國分町"): {"en": "Kokubuncho", "ja": "国分町", "zh-CN": "国分町"},
    ("sendai", "青葉通"): {"en": "Aoba-dori", "ja": "青葉通り", "zh-CN": "青叶通"},
    ("hiroshima", "紙屋町"): {"en": "Kamiyacho", "ja": "紙屋町", "zh-CN": "纸屋町"},
    ("chiang-rai", "河畔"): {"en": "Riverside"},
    ("chiang-rai", "舊城"): {"en": "Old Town", "zh-CN": "旧城"},
    ("tainan", "中西區"): {"en": "West Central District", "ja": "中西区", "zh-CN": "中西区"},
    ("tainan", "海安路"): {"en": "Hai'an Road"},
    ("jeonju", "韓屋村"): {
        "en": "Hanok Village",
        "ja": "韓屋村",
        "ko": "한옥마을",
        "zh-CN": "韩屋村",
    },
    ("jeonju", "完山公園"): {
        "en": "Wansan Park",
        "ja": "完山公園",
        "ko": "완산공원",
        "zh-CN": "完山公园",
    },
}


def _area_segments(text: str) -> list[str]:
    return [part for part in AREA_SEGMENT.split(text) if part]


def _build_area_index() -> dict[str, dict[str, tuple[HotspotArea, int, int]]]:
    """Every reviewed area, addressable by any one of its Traditional segments.

    The position and the segment count travel with it so a one-part lodging area can
    take the matching one part of a two-part district name — 「澀谷」 becomes "Shibuya",
    not "Shibuya & Harajuku" — and fall back to the whole name when the reader's locale
    splits it differently (Korean writes several of these as one word).
    """
    index: dict[str, dict[str, tuple[HotspotArea, int, int]]] = {}
    for city_code, areas in HOTSPOT_AREAS.items():
        table: dict[str, tuple[HotspotArea, int, int]] = {}
        for area in areas:
            parts = _area_segments(area.names["zh-TW"])
            for position, part in enumerate(parts):
                # First writer wins: catalog order is the reviewed order.
                table.setdefault(part, (area, position, len(parts)))
        index[city_code] = table
    return index


AREA_INDEX: Final[Mapping[str, Mapping[str, tuple[HotspotArea, int, int]]]] = _build_area_index()


def _listed_area_name(destination_id: str, label: str, locale: Locale) -> str | None:
    """The hand-checked name for an area the reviewed catalog does not carry."""
    names = AREA_NAMES.get((destination_id, label))
    if names is None:
        return None
    if locale == "zh-CN":
        return names.get("zh-CN") or label
    return names.get(locale) or names.get("en") or label


def area_label(profile: DestinationProfile, label: str, locale: Locale) -> str:
    """One lodging area as the reader would write it; the catalog's own text for zh-TW."""
    if locale == "zh-TW":
        return label
    listed = _listed_area_name(profile.id, label, locale)
    if listed is not None:
        return listed
    table = AREA_INDEX.get((profile.code or "").upper(), {})
    pieces: list[str] = []
    for part in _area_segments(label):
        found = table.get(part)
        if found is None:
            # Nothing reviewed covers this one. The local script beats a guess.
            return label
        area, position, count = found
        whole = area_name(area, locale)
        segments = [] if "(" in whole or ")" in whole else _area_segments(whole)
        piece = segments[position] if len(segments) == count else whole
        if piece not in pieces:
            pieces.append(piece)
    return AREA_JOIN.get(locale, "／").join(pieces)


def area_labels(profile: DestinationProfile, locale: Locale) -> list[str]:
    """The lodging areas in the reader's locale, in catalog order and without repeats."""
    if locale == "zh-TW":
        return list(profile.areas)
    labels: list[str] = []
    for label in profile.areas:
        value = area_label(profile, label, locale)
        if value not in labels:
            labels.append(value)
    return labels


def validate_localized_catalog() -> list[str]:
    """Every destination and country has every locale; run by the tests."""
    problems: list[str] = []
    for profile in DESTINATIONS:
        for table, name in ((CITY_NAMES, "city name"), (REASONS, "reason")):
            entries = table.get(profile.id, {})
            missing = [locale for locale in TRANSLATED if not entries.get(locale)]
            if missing:
                problems.append(f"{profile.id}: {name} missing {', '.join(missing)}")
        if profile.country not in COUNTRY_LABELS:
            problems.append(f"{profile.id}: country {profile.country!r} has no labels")
    for country, labels in COUNTRY_LABELS.items():
        missing = [locale for locale in TRANSLATED if not labels.get(locale)]
        if missing:
            problems.append(f"{country}: label missing {', '.join(missing)}")
    unknown = set(CITY_NAMES) | set(REASONS)
    unknown -= {profile.id for profile in DESTINATIONS}
    problems.extend(f"{extra}: not in the catalog" for extra in sorted(unknown))
    if set(TRANSLATED) | {"zh-TW"} != set(LOCALES):
        problems.append("TRANSLATED does not cover the site locales")
    problems.extend(_area_problems())
    return problems


def _area_problems() -> list[str]:
    """Every lodging area resolves, either through the reviewed catalog or by name.

    This is the guard that keeps AREA_NAMES honest: adding an area to the destination
    catalog that neither matches a reviewed district nor appears below leaves a label
    that stays Traditional in all four other locales, and the tests say so instead of
    the reader finding out.
    """
    problems: list[str] = []
    listed = set(AREA_NAMES)
    for profile in DESTINATIONS:
        table = AREA_INDEX.get((profile.code or "").upper(), {})
        for label in profile.areas:
            listed.discard((profile.id, label))
            if (profile.id, label) in AREA_NAMES:
                if not AREA_NAMES[(profile.id, label)].get("en"):
                    problems.append(f"{profile.id}: area {label!r} has no English name")
                continue
            unknown = [part for part in _area_segments(label) if part not in table]
            if unknown:
                problems.append(
                    f"{profile.id}: area {label!r} is not in the reviewed catalog "
                    f"({', '.join(unknown)}) and has no entry in AREA_NAMES"
                )
    problems.extend(
        f"{destination_id}: AREA_NAMES has {label!r}, which is not one of its areas"
        for destination_id, label in sorted(listed)
    )
    return problems
