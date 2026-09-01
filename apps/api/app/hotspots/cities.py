from dataclasses import dataclass


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


def _center(latitude: float, longitude: float, radius_km: int) -> DiscoveryCenter:
    return DiscoveryCenter(latitude, longitude, radius_km)


HOTSPOT_CITIES: tuple[HotspotCity, ...] = (
    HotspotCity(
        "NRT", "東京", "JP", "日本", "ja.wikipedia.org", 16, (_center(35.6762, 139.6503, 30),)
    ),
    HotspotCity(
        "KIX",
        "大阪／京都",
        "JP",
        "日本",
        "ja.wikipedia.org",
        20,
        (_center(34.6937, 135.5023, 22), _center(35.0116, 135.7681, 22)),
    ),
    HotspotCity(
        "FUK", "福岡", "JP", "日本", "ja.wikipedia.org", 10, (_center(33.5904, 130.4017, 35),)
    ),
    HotspotCity(
        "CTS", "札幌", "JP", "日本", "ja.wikipedia.org", 10, (_center(43.0618, 141.3545, 45),)
    ),
    HotspotCity(
        "OKA", "沖繩", "JP", "日本", "ja.wikipedia.org", 10, (_center(26.3344, 127.8056, 100),)
    ),
    HotspotCity(
        "NGO", "名古屋", "JP", "日本", "ja.wikipedia.org", 10, (_center(35.1815, 136.9066, 35),)
    ),
    HotspotCity(
        "ICN", "首爾", "KR", "韓國", "ko.wikipedia.org", 16, (_center(37.5665, 126.9780, 30),)
    ),
    HotspotCity(
        "PUS", "釜山", "KR", "韓國", "ko.wikipedia.org", 10, (_center(35.1796, 129.0756, 35),)
    ),
    HotspotCity(
        "CJU", "濟州", "KR", "韓國", "ko.wikipedia.org", 10, (_center(33.3617, 126.5292, 65),)
    ),
    HotspotCity(
        "BKK", "曼谷", "TH", "泰國", "th.wikipedia.org", 16, (_center(13.7563, 100.5018, 35),)
    ),
    HotspotCity(
        "CNX", "清邁", "TH", "泰國", "th.wikipedia.org", 10, (_center(18.7883, 98.9853, 55),)
    ),
    HotspotCity(
        "HKT", "普吉", "TH", "泰國", "th.wikipedia.org", 10, (_center(7.9519, 98.3381, 55),)
    ),
    HotspotCity(
        "KBV", "喀比", "TH", "泰國", "th.wikipedia.org", 10, (_center(8.0863, 98.9063, 55),)
    ),
    HotspotCity(
        "TPE", "台北", "TW", "台灣", "zh.wikipedia.org", 10, (_center(25.0330, 121.5654, 35),)
    ),
    HotspotCity(
        "SIN", "新加坡", "SG", "新加坡", "en.wikipedia.org", 10, (_center(1.3521, 103.8198, 35),)
    ),
    HotspotCity(
        "HKG", "香港", "HK", "香港", "zh.wikipedia.org", 10, (_center(22.3193, 114.1694, 40),)
    ),
    HotspotCity(
        "HAN", "河內", "VN", "越南", "vi.wikipedia.org", 10, (_center(21.0278, 105.8342, 35),)
    ),
    HotspotCity(
        "SGN", "胡志明市", "VN", "越南", "vi.wikipedia.org", 10, (_center(10.8231, 106.6297, 40),)
    ),
    HotspotCity(
        "DAD", "峴港", "VN", "越南", "vi.wikipedia.org", 10, (_center(16.0544, 108.2022, 45),)
    ),
)

CITY_BY_CODE = {city.code: city for city in HOTSPOT_CITIES}
TARGET_PUBLIC_HOTSPOTS = sum(city.target_count for city in HOTSPOT_CITIES)
