"""Generate the checked-in hotspot bootstrap artifact from reviewed Wikipedia titles."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "apps" / "api" / "app" / "hotspots" / "bootstrap.json"
USER_AGENT = "TravelScannerBot/0.1 (+https://github.com/x812033727/travel_scanner)"

# Each entry was selected as a genuine visitor attraction before its structured metadata is
# resolved. A small set of pages has no P625 value; their reviewed OpenStreetMap coordinates
# are kept here explicitly so the generated artifact never falls back to a city-centre point.
COORDINATE_OVERRIDES: dict[str, tuple[float, float]] = {
    "momochi seaside park": (33.5948717, 130.3507794),
    "uminonakamichi seaside park": (33.6626271, 130.3557112),
    "shiroi koibito park": (43.0886903, 141.2716802),
    "otaru canal": (43.2020231, 141.0006005),
    "kouri island": (26.6982327, 128.02055),
    "kokusai-dōri": (26.2171921, 127.69101),
    "chubu electric power mirai tower": (35.1722972, 136.9083338),
    "o'sulloc tea museum": (33.3059, 126.2895),
    "promthep cape": (7.7643212, 98.3053958),
    "elephant mountain (taipei)": (25.0265411, 121.575542),
    "longshan temple": (25.0352844, 121.4995813),
    "mỹ khê beach": (16.0756254, 108.2468784),
    "hội an": (15.8779509, 108.3239898),
    "百道濱海濱公園": (33.5948717, 130.3507794),
    "海之中道海濱公園": (33.6626271, 130.3557112),
    "白色戀人公園": (43.0886903, 141.2716802),
    "小樽運河": (43.2020231, 141.0006005),
    "古宇利島": (26.6982327, 128.02055),
    "國際通": (26.2171921, 127.69101),
    "中部電力 mirai tower": (35.1722972, 136.9083338),
    "雪綠茶博物館": (33.3059, 126.2895),
    "神仙半島": (7.7643212, 98.3053958),
    "象山": (25.0265411, 121.575542),
    "龍山寺": (25.0352844, 121.4995813),
    "美溪海灘": (16.0756254, 108.2468784),
    "會安古城": (15.8779509, 108.3239898),
    "沖繩縣立博物館・美術館": (26.2274, 127.6931),
}
QID_OVERRIDES = {
    "uminonakamichi seaside park": "Q11558610",
    "shiroi koibito park": "Q56963453",
    "otaru canal": "Q10959355",
    "kokusai-dōri": "Q4616917",
    "chubu electric power mirai tower": "Q283373",
    "promthep cape": "Q13026486",
}

SPECS: dict[str, list[tuple[str, str, str]]] = {
    "NRT": [
        ("Sensō-ji", "淺草寺", "culture"), ("Tokyo Skytree", "東京晴空塔", "viewpoint"),
        ("Meiji Shrine", "明治神宮", "culture"), ("Shibuya Crossing", "澀谷十字路口", "viewpoint"),
        ("Tokyo Tower", "東京鐵塔", "viewpoint"), ("Tokyo Imperial Palace", "東京皇居", "culture"),
        ("Ueno Park", "上野公園", "nature"), ("Odaiba", "台場", "family"),
        ("Shinjuku Gyo-en", "新宿御苑", "nature"), ("Akihabara", "秋葉原", "shopping"),
        ("Tsukiji fish market", "築地場外市場", "food"), ("Tokyo Disneyland", "東京迪士尼樂園", "family"),
    ],
    "KIX": [
        ("Dōtonbori", "道頓堀", "food"), ("Fushimi Inari-taisha", "伏見稻荷大社", "culture"),
        ("Kiyomizu-dera", "清水寺", "culture"), ("Kinkaku-ji", "金閣寺", "culture"),
        ("Arashiyama", "嵐山", "nature"), ("Osaka Castle", "大阪城", "culture"),
        ("Universal Studios Japan", "日本環球影城", "family"), ("Osaka Aquarium Kaiyukan", "大阪海遊館", "family"),
        ("Gion", "祇園", "culture"), ("Nijō Castle", "二條城", "culture"),
        ("Nishiki Market", "錦市場", "food"), ("Umeda Sky Building", "梅田藍天大廈", "viewpoint"),
        ("Shinsaibashi", "心齋橋", "shopping"), ("Nara Park", "奈良公園", "nature"),
    ],
    "FUK": [
        ("Dazaifu Tenmangū", "太宰府天滿宮", "culture"), ("Ōhori Park", "大濠公園", "nature"),
        ("Fukuoka Castle", "福岡城跡", "culture"), ("Canal City Hakata", "博多運河城", "shopping"),
        ("Kushida Shrine", "櫛田神社", "culture"), ("Fukuoka Tower", "福岡塔", "viewpoint"),
        ("Uminonakamichi Seaside Park", "海之中道海濱公園", "family"), ("Fukuoka City Museum", "福岡市博物館", "culture"),
    ],
    "CTS": [
        ("Sapporo Clock Tower", "札幌時計台", "culture"), ("Otaru Canal", "小樽運河", "viewpoint"),
        ("Odori Park", "大通公園", "nature"), ("Sapporo TV Tower", "札幌電視塔", "viewpoint"),
        ("Mount Moiwa", "藻岩山", "nature"), ("Sapporo Beer Museum", "札幌啤酒博物館", "culture"),
        ("Shiroi Koibito Park", "白色戀人公園", "family"), ("Historical Village of Hokkaido", "北海道開拓村", "culture"),
    ],
    "OKA": [
        ("Shuri Castle", "首里城", "culture"), ("Okinawa Churaumi Aquarium", "沖繩美麗海水族館", "family"),
        ("Kokusai-dōri", "國際通", "shopping"), ("Cape Manzamo", "萬座毛", "viewpoint"),
        ("Okinawa Prefectural Museum", "沖繩縣立博物館・美術館", "culture"), ("Nakagusuku Castle", "中城城跡", "culture"),
        ("Sefa-utaki", "齋場御嶽", "culture"), ("American Village", "美國村", "shopping"),
    ],
    "NGO": [
        ("Nagoya Castle", "名古屋城", "culture"), ("Atsuta Shrine", "熱田神宮", "culture"),
        ("Port of Nagoya Public Aquarium", "名古屋港水族館", "family"), ("SCMaglev and Railway Park", "磁浮鐵道館", "family"),
        ("Tokugawa Art Museum", "德川美術館", "culture"), ("Nagoya City Science Museum", "名古屋市科學館", "family"),
        ("Ōsu Kannon", "大須觀音", "culture"), ("Chubu Electric Power MIRAI TOWER", "中部電力 MIRAI TOWER", "viewpoint"),
    ],
    "ICN": [
        ("Gyeongbokgung", "景福宮", "culture"), ("N Seoul Tower", "南山首爾塔", "viewpoint"),
        ("Bukchon Hanok Village", "北村韓屋村", "culture"), ("Changdeokgung", "昌德宮", "culture"),
        ("Myeong-dong", "明洞", "shopping"), ("Dongdaemun Design Plaza", "東大門設計廣場", "shopping"),
        ("National Museum of Korea", "韓國國立中央博物館", "culture"), ("Lotte World", "樂天世界", "family"),
        ("Cheonggyecheon", "清溪川", "nature"), ("Gwangjang Market", "廣藏市場", "food"),
        ("Hongdae, Seoul", "弘大", "nightlife"), ("COEX Mall", "COEX 購物中心", "shopping"),
    ],
    "PUS": [
        ("Haeundae Beach", "海雲台海水浴場", "beach"), ("Gamcheon Culture Village", "甘川文化村", "culture"),
        ("Jagalchi Market", "札嘎其市場", "food"), ("Gwangalli Beach", "廣安里海水浴場", "beach"),
        ("Haedong Yonggungsa", "海東龍宮寺", "culture"), ("Taejongdae", "太宗臺", "nature"),
        ("Busan Tower", "釜山塔", "viewpoint"), ("Songdo Beach", "松島海水浴場", "beach"),
    ],
    "CJU": [
        ("Seongsan Ilchulbong", "城山日出峰", "nature"), ("Hallasan", "漢拏山", "nature"),
        ("Manjanggul", "萬丈窟", "nature"), ("Cheonjiyeon Waterfall", "天地淵瀑布", "nature"),
        ("Jeju Loveland", "濟州性愛主題公園", "culture"), ("Jeongbang Waterfall", "正房瀑布", "nature"),
        ("Udo (island)", "牛島", "nature"), ("O'Sulloc Tea Museum", "雪綠茶博物館", "culture"),
    ],
    "BKK": [
        ("Grand Palace", "曼谷大皇宮", "culture"), ("Wat Arun", "鄭王廟", "culture"),
        ("Wat Pho", "臥佛寺", "culture"), ("Chatuchak Weekend Market", "恰圖恰週末市集", "shopping"),
        ("Jim Thompson House", "湯普生博物館", "culture"), ("Lumphini Park", "倫披尼公園", "nature"),
        ("Wat Saket", "金山寺", "culture"), ("Khaosan Road", "考山路", "nightlife"),
        ("Siam Paragon", "暹羅百麗宮", "shopping"), ("Asiatique", "河濱碼頭夜市", "shopping"),
        ("Bangkok National Museum", "曼谷國立博物館", "culture"), ("Sea Life Bangkok Ocean World", "曼谷暹羅海洋世界", "family"),
    ],
    "CNX": [
        ("Wat Phra That Doi Suthep", "素帖山雙龍寺", "culture"), ("Tha Phae Gate", "塔佩門", "culture"),
        ("Wat Chedi Luang", "契迪龍寺", "culture"), ("Wat Phra Singh", "帕邢寺", "culture"),
        ("Chiang Mai Night Bazaar", "清邁夜市", "shopping"), ("Doi Inthanon National Park", "茵他儂山國家公園", "nature"),
        ("Wat Umong", "悟孟寺", "culture"), ("Royal Park Rajapruek", "皇家公園 Rajapruek", "nature"),
    ],
    "HKT": [
        ("Old Phuket Town", "普吉老城", "culture"), ("Patong Beach", "芭東海灘", "beach"),
        ("Karon Beach", "卡隆海灘", "beach"), ("Kata Beach", "卡塔海灘", "beach"),
        ("Wat Chalong", "查龍寺", "culture"), ("Phuket Big Buddha", "普吉大佛", "viewpoint"),
        ("Promthep Cape", "神仙半島", "viewpoint"), ("Sirinat National Park", "斯里納斯國家公園", "nature"),
    ],
    "KBV": [
        ("Railay Beach", "萊雷海灘", "beach"), ("Ao Nang", "奧南海灘", "beach"),
        ("Ko Phi Phi Le", "小皮皮島", "nature"), ("Ko Poda", "波達島", "beach"),
        ("Tiger Cave Temple", "虎窟寺", "culture"), ("Mu Ko Lanta National Park", "蘭塔群島國家公園", "nature"),
        ("Emerald Cave (Thailand)", "翡翠洞", "nature"), ("Khao Phanom Bencha National Park", "帕儂賓札國家公園", "nature"),
    ],
    "TPE": [
        ("Taipei 101", "台北 101", "viewpoint"), ("National Palace Museum", "國立故宮博物院", "culture"),
        ("Chiang Kai-shek Memorial Hall", "中正紀念堂", "culture"), ("Longshan Temple", "龍山寺", "culture"),
        ("Ximending", "西門町", "shopping"), ("Taipei Zoo", "臺北市立動物園", "family"),
        ("Dihua Street", "迪化街", "culture"), ("Raohe Street Night Market", "饒河街觀光夜市", "food"),
    ],
    "SIN": [
        ("Marina Bay Sands", "濱海灣金沙", "viewpoint"), ("Gardens by the Bay", "濱海灣花園", "nature"),
        ("Sentosa", "聖淘沙", "family"), ("Singapore Botanic Gardens", "新加坡植物園", "nature"),
        ("Singapore Zoo", "新加坡動物園", "family"), ("Merlion", "魚尾獅", "viewpoint"),
        ("Chinatown, Singapore", "牛車水", "culture"), ("National Gallery Singapore", "新加坡國家美術館", "culture"),
    ],
    "HKG": [
        ("Victoria Peak", "太平山", "viewpoint"), ("Tian Tan Buddha", "天壇大佛", "culture"),
        ("Hong Kong Disneyland", "香港迪士尼樂園", "family"), ("Avenue of Stars, Hong Kong", "星光大道", "viewpoint"),
        ("Temple Street Night Market", "廟街夜市", "nightlife"), ("Hong Kong Palace Museum", "香港故宮文化博物館", "culture"),
        ("Ocean Park Hong Kong", "香港海洋公園", "family"), ("Man Mo Temple", "文武廟", "culture"),
    ],
    "HAN": [
        ("Hoàn Kiếm Lake", "還劍湖", "nature"), ("Temple of Literature, Hanoi", "河內文廟", "culture"),
        ("Ho Chi Minh Mausoleum", "胡志明陵", "culture"), ("Imperial Citadel of Thăng Long", "昇龍皇城", "culture"),
        ("One Pillar Pagoda", "一柱寺", "culture"), ("Vietnam Museum of Ethnology", "越南民族學博物館", "culture"),
        ("Hanoi Opera House", "河內歌劇院", "culture"), ("St. Joseph's Cathedral, Hanoi", "河內聖若瑟主教座堂", "culture"),
    ],
    "SGN": [
        ("Independence Palace", "統一宮", "culture"), ("War Remnants Museum", "戰爭遺跡博物館", "culture"),
        ("Notre-Dame Cathedral Basilica of Saigon", "西貢聖母聖殿主教座堂", "culture"), ("Saigon Central Post Office", "西貢中央郵局", "culture"),
        ("Bến Thành Market", "濱城市場", "food"), ("Bitexco Financial Tower", "金融塔", "viewpoint"),
        ("Jade Emperor Pagoda", "玉皇殿", "culture"), ("Ho Chi Minh City Museum", "胡志明市博物館", "culture"),
    ],
    "DAD": [
        ("Marble Mountains (Vietnam)", "五行山", "nature"), ("Dragon Bridge (Da Nang)", "峴港龍橋", "viewpoint"),
        ("Mỹ Sơn", "美山聖地", "culture"), ("Museum of Cham Sculpture", "占婆雕刻博物館", "culture"),
        ("Bà Nà Hills", "巴拿山", "family"), ("Sơn Trà Mountain", "山茶山", "nature"),
        ("Hội An", "會安古城", "culture"), ("Golden Bridge (Vietnam)", "佛手金橋", "viewpoint"),
    ],
}


def get_json(base: str, params: dict[str, str]) -> dict[str, Any]:
    request = Request(f"{base}?{urlencode(params)}", headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=45) as response:  # noqa: S310 - fixed trusted hosts
                return json.load(response)
        except TimeoutError:
            if attempt == 2:
                raise
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def chunks(items: list[tuple[str, str, str]], size: int = 40):
    for index in range(0, len(items), size):
        yield items[index : index + size]


def main() -> None:
    generated: list[dict[str, Any]] = []
    failures: list[str] = []
    for city_code, specs in SPECS.items():
        for batch in chunks(specs):
            labels = {title.casefold(): (name, category) for title, name, category in batch}
            payload = get_json(
                "https://en.wikipedia.org/w/api.php",
                {
                    "action": "query", "format": "json", "formatversion": "2",
                    "redirects": "1", "prop": "coordinates|pageprops",
                    "titles": "|".join(title for title, _, _ in batch),
                },
            )
            normalized = {
                item["to"].casefold(): item["from"].casefold()
                for item in payload.get("query", {}).get("normalized", [])
            }
            redirects = {
                item["to"].casefold(): normalized.get(item["from"].casefold(), item["from"].casefold())
                for item in payload.get("query", {}).get("redirects", [])
            }
            page_rows: list[tuple[dict[str, Any], tuple[str, str]]] = []
            for page in payload.get("query", {}).get("pages", []):
                resolved = str(page.get("title", "")).casefold()
                source = redirects.get(resolved, normalized.get(resolved, resolved))
                name_category = labels.get(source) or labels.get(resolved)
                coordinates = page.get("coordinates") or []
                qid = (page.get("pageprops") or {}).get("wikibase_item") or QID_OVERRIDES.get(
                    source
                )
                if not name_category or not qid:
                    failures.append(f"{city_code}: {page.get('title', source)}")
                    continue
                page.setdefault("pageprops", {})["wikibase_item"] = qid
                page_rows.append((page, name_category))
            qids = [
                str((page.get("pageprops") or {})["wikibase_item"])
                for page, _ in page_rows
                if not page.get("coordinates")
            ]
            entities = (
                get_json(
                    "https://www.wikidata.org/w/api.php",
                    {
                        "action": "wbgetentities", "format": "json", "props": "claims",
                        "ids": "|".join(qids),
                    },
                ).get("entities", {})
                if qids
                else {}
            )
            for page, name_category in page_rows:
                coordinates = page.get("coordinates") or []
                qid = str((page.get("pageprops") or {})["wikibase_item"])
                if coordinates:
                    latitude = coordinates[0]["lat"]
                    longitude = coordinates[0]["lon"]
                else:
                    coordinate_claims = (entities.get(qid, {}).get("claims", {})).get("P625", [])
                    try:
                        point = coordinate_claims[0]["mainsnak"]["datavalue"]["value"]
                        latitude, longitude = point["latitude"], point["longitude"]
                    except (IndexError, KeyError, TypeError):
                        override = COORDINATE_OVERRIDES.get(
                            str(page.get("title", "")).casefold()
                        ) or COORDINATE_OVERRIDES.get(name_category[0].casefold())
                        if override is None:
                            failures.append(
                                f"{city_code}: {page.get('title', qid)} ({qid}; {name_category[0]!r})"
                            )
                            continue
                        latitude, longitude = override
                name, category = name_category
                generated.append(
                    {
                        "city_code": city_code,
                        "name": name,
                        "category": category,
                        "latitude": latitude,
                        "longitude": longitude,
                        "wikipedia_project": "en.wikipedia.org",
                        "wikipedia_title": page["title"],
                        "wikidata_item_id": qid,
                    }
                )
            time.sleep(0.1)
    if failures:
        print("Missing structured metadata:\n" + "\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    generated.sort(key=lambda item: (item["city_code"], item["name"]))
    OUTPUT.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {len(generated)} hotspots to {OUTPUT}")


if __name__ == "__main__":
    main()
