from dataclasses import dataclass, replace

from app.destinations.catalog import LEGACY_DESTINATION_IDS


@dataclass(frozen=True)
class DiscoveryCenter:
    latitude: float
    longitude: float
    radius_km: int


@dataclass(frozen=True)
class HotspotCity:
    code: str
    name: str
    country_code: str
    country_name: str
    local_wikipedia: str
    target_count: int
    centers: tuple[DiscoveryCenter, ...]
    destination_id: str | None = None
    role: str = "primary"
    parent_destination_id: str | None = None

    @property
    def id(self) -> str:
        return self.destination_id or LEGACY_DESTINATION_IDS[self.code]


def _center(latitude: float, longitude: float, radius_km: int) -> DiscoveryCenter:
    return DiscoveryCenter(latitude, longitude, radius_km)


HOTSPOT_CITIES: tuple[HotspotCity, ...] = (
    HotspotCity(
        "NRT", "東京", "JP", "日本", "ja.wikipedia.org", 105, (_center(35.6762, 139.6503, 30),)
    ),
    HotspotCity(
        "KIX",
        "大阪／京都",
        "JP",
        "日本",
        "ja.wikipedia.org",
        25,
        (_center(34.6937, 135.5023, 22), _center(35.0116, 135.7681, 22)),
    ),
    HotspotCity(
        "FUK", "福岡", "JP", "日本", "ja.wikipedia.org", 15, (_center(33.5904, 130.4017, 35),)
    ),
    HotspotCity(
        "CTS", "札幌", "JP", "日本", "ja.wikipedia.org", 15, (_center(43.0618, 141.3545, 45),)
    ),
    HotspotCity(
        "OKA", "沖繩", "JP", "日本", "ja.wikipedia.org", 15, (_center(26.3344, 127.8056, 100),)
    ),
    HotspotCity(
        "NGO", "名古屋", "JP", "日本", "ja.wikipedia.org", 15, (_center(35.1815, 136.9066, 35),)
    ),
    HotspotCity(
        "ICN", "首爾", "KR", "韓國", "ko.wikipedia.org", 21, (_center(37.5665, 126.9780, 30),)
    ),
    HotspotCity(
        "PUS", "釜山", "KR", "韓國", "ko.wikipedia.org", 15, (_center(35.1796, 129.0756, 35),)
    ),
    HotspotCity(
        "CJU", "濟州", "KR", "韓國", "ko.wikipedia.org", 15, (_center(33.3617, 126.5292, 65),)
    ),
    HotspotCity(
        "BKK", "曼谷", "TH", "泰國", "th.wikipedia.org", 21, (_center(13.7563, 100.5018, 35),)
    ),
    HotspotCity(
        "CNX", "清邁", "TH", "泰國", "th.wikipedia.org", 15, (_center(18.7883, 98.9853, 55),)
    ),
    HotspotCity(
        "HKT", "普吉", "TH", "泰國", "th.wikipedia.org", 15, (_center(7.9519, 98.3381, 55),)
    ),
    HotspotCity(
        "KBV", "喀比", "TH", "泰國", "th.wikipedia.org", 15, (_center(8.0863, 98.9063, 55),)
    ),
    HotspotCity(
        "TPE", "台北", "TW", "台灣", "zh.wikipedia.org", 15, (_center(25.0330, 121.5654, 35),)
    ),
    HotspotCity(
        "SIN", "新加坡", "SG", "新加坡", "en.wikipedia.org", 15, (_center(1.3521, 103.8198, 35),)
    ),
    HotspotCity(
        "HKG", "香港", "HK", "香港", "zh.wikipedia.org", 15, (_center(22.3193, 114.1694, 40),)
    ),
    HotspotCity(
        "HAN", "河內", "VN", "越南", "vi.wikipedia.org", 15, (_center(21.0278, 105.8342, 35),)
    ),
    HotspotCity(
        "SGN", "胡志明市", "VN", "越南", "vi.wikipedia.org", 15, (_center(10.8231, 106.6297, 40),)
    ),
    HotspotCity(
        "DAD", "峴港", "VN", "越南", "vi.wikipedia.org", 15, (_center(16.0544, 108.2022, 45),)
    ),
    HotspotCity(
        "RMQ",
        "台中",
        "TW",
        "台灣",
        "zh.wikipedia.org",
        18,
        (_center(24.1477, 120.6736, 28),),
        "taichung",
        "secondary",
    ),
    HotspotCity(
        "KHH",
        "高雄",
        "TW",
        "台灣",
        "zh.wikipedia.org",
        18,
        (_center(22.6273, 120.3014, 30),),
        "kaohsiung",
        "secondary",
    ),
    HotspotCity(
        "SDJ",
        "仙台",
        "JP",
        "日本",
        "ja.wikipedia.org",
        18,
        (_center(38.2682, 140.8694, 30),),
        "sendai",
        "secondary",
    ),
    HotspotCity(
        "KMQ",
        "金澤",
        "JP",
        "日本",
        "ja.wikipedia.org",
        18,
        (_center(36.5613, 136.6562, 28),),
        "kanazawa",
        "secondary",
    ),
    HotspotCity(
        "HIJ",
        "廣島",
        "JP",
        "日本",
        "ja.wikipedia.org",
        18,
        (_center(34.3853, 132.4553, 30),),
        "hiroshima",
        "secondary",
    ),
    HotspotCity(
        "TAE",
        "大邱",
        "KR",
        "韓國",
        "ko.wikipedia.org",
        18,
        (_center(35.8714, 128.6014, 30),),
        "daegu",
        "secondary",
    ),
    HotspotCity(
        "CEI",
        "清萊",
        "TH",
        "泰國",
        "th.wikipedia.org",
        18,
        (_center(19.9105, 99.8406, 35),),
        "chiang-rai",
        "secondary",
    ),
    HotspotCity(
        "DLI",
        "大叻",
        "VN",
        "越南",
        "vi.wikipedia.org",
        18,
        (_center(11.9404, 108.4583, 35),),
        "da-lat",
        "secondary",
    ),
    HotspotCity(
        "TNN",
        "台南",
        "TW",
        "台灣",
        "zh.wikipedia.org",
        18,
        (_center(22.9999, 120.2269, 28),),
        "tainan",
        "extension",
        "kaohsiung",
    ),
    HotspotCity(
        "GYE",
        "慶州",
        "KR",
        "韓國",
        "ko.wikipedia.org",
        18,
        (_center(35.8562, 129.2247, 32),),
        "gyeongju",
        "extension",
        "busan",
    ),
    HotspotCity(
        "JEO",
        "全州",
        "KR",
        "韓國",
        "ko.wikipedia.org",
        18,
        (_center(35.8242, 127.1480, 28),),
        "jeonju",
        "extension",
        "seoul",
    ),
    HotspotCity(
        "HUI",
        "順化",
        "VN",
        "越南",
        "vi.wikipedia.org",
        18,
        (_center(16.4637, 107.5909, 30),),
        "hue",
        "extension",
        "da-nang",
    ),
    HotspotCity(
        "YOK",
        "橫濱",
        "JP",
        "日本",
        "ja.wikipedia.org",
        18,
        (_center(35.4437, 139.6380, 12),),
        "yokohama",
        "extension",
        "tokyo",
    ),
    HotspotCity(
        "KMK",
        "鎌倉",
        "JP",
        "日本",
        "ja.wikipedia.org",
        18,
        (_center(35.3192, 139.5467, 8),),
        "kamakura",
        "extension",
        "tokyo",
    ),
)

# Reviewed near-suburban centers, all intended to remain within about 90 minutes
# of the destination's main accommodation area. Discovery candidates found here
# still require admin review before they can receive a deep-travel designation.
DAY_TRIP_CENTERS = {
    "NRT": (_center(35.6252, 139.2437, 16),),
    "KIX": (_center(34.8845, 135.7997, 16), _center(35.1220, 135.7680, 14)),
    "FUK": (_center(33.5898, 130.2013, 18),),
    "CTS": (_center(42.9650, 141.1668, 18),),
    "OKA": (_center(26.1735, 127.8266, 18),),
    "NGO": (_center(34.8860, 136.8324, 16),),
    "ICN": (_center(37.2850, 127.0100, 18),),
    "PUS": (_center(35.4880, 129.0640, 18),),
    "CJU": (_center(33.4350, 126.9220, 18),),
    "BKK": (_center(13.9120, 100.4980, 18),),
    "CNX": (_center(18.8650, 99.3500, 18),),
    "HKT": (_center(8.1080, 98.3060, 18),),
    "KBV": (_center(8.2140, 98.8360, 18),),
    "TPE": (_center(24.9340, 121.3690, 18),),
    "SIN": (_center(1.4040, 103.9600, 14),),
    "HKG": (_center(22.5100, 114.2400, 16),),
    "HAN": (_center(21.0810, 105.6540, 18),),
    "SGN": (_center(10.9900, 106.4900, 18),),
    "DAD": (_center(15.8800, 108.3200, 18),),
    "RMQ": (_center(24.2521, 120.7200, 15),),
    "KHH": (_center(22.7498, 120.4453, 16),),
    "SDJ": (_center(38.3117, 140.5954, 16),),
    "KMQ": (_center(36.2456, 136.8992, 16),),
    "HIJ": (_center(34.2958, 132.3199, 16),),
    "TAE": (_center(35.9900, 128.6950, 16),),
    "CEI": (_center(20.2160, 99.8780, 18),),
    "DLI": (_center(11.7790, 108.3830, 18),),
    "TNN": (_center(23.1220, 120.4610, 16),),
    "GYE": (_center(35.7900, 129.3320, 16),),
    "JEO": (_center(35.9740, 127.2130, 16),),
    "HUI": (_center(16.1040, 107.9550, 18),),
    "YOK": (_center(35.3370, 139.6440, 10),),
    "KMK": (_center(35.2990, 139.4800, 8),),
}
HOTSPOT_CITIES = tuple(
    replace(city, centers=city.centers + DAY_TRIP_CENTERS[city.code]) for city in HOTSPOT_CITIES
)

CITY_BY_CODE = {city.code: city for city in HOTSPOT_CITIES}
CITY_BY_DESTINATION_ID = {city.id: city for city in HOTSPOT_CITIES}
TARGET_PUBLIC_HOTSPOTS = sum(city.target_count for city in HOTSPOT_CITIES)
