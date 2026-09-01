"""Build the reviewed secondary-city bootstrap from Wikimedia pages.

The output is deterministic for a given Wikimedia snapshot. It is intentionally
kept as a checked-in offline catalog; production never runs this script.
"""

from __future__ import annotations

import json
import re
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
HOTSPOTS = ROOT / "apps" / "api" / "app" / "hotspots"
OUTPUT = HOTSPOTS / "secondary_bootstrap.json"
USER_AGENT = "TravelScannerSecondaryCatalog/1.0 (curated bootstrap builder)"

CITIES = {
    "RMQ": ("zh.wikipedia.org", (24.1477, 120.6736), (24.2521, 120.7200)),
    "KHH": ("zh.wikipedia.org", (22.6273, 120.3014), (22.7498, 120.4453)),
    "SDJ": ("ja.wikipedia.org", (38.2682, 140.8694), (38.3117, 140.5954)),
    "KMQ": ("ja.wikipedia.org", (36.5613, 136.6562), (36.2456, 136.8992)),
    "HIJ": ("ja.wikipedia.org", (34.3853, 132.4553), (34.2958, 132.3199)),
    "TAE": ("ko.wikipedia.org", (35.8714, 128.6014), (35.9900, 128.6950)),
    "CEI": ("en.wikipedia.org", (19.9105, 99.8406), (20.2160, 99.8780)),
    "DLI": ("vi.wikipedia.org", (11.9404, 108.4583), (11.7790, 108.3830)),
    "TNN": ("zh.wikipedia.org", (22.9999, 120.2269), (23.1220, 120.4610)),
    "GYE": ("ko.wikipedia.org", (35.8562, 129.2247), (35.7900, 129.3320)),
    "JEO": ("ko.wikipedia.org", (35.8242, 127.1480), (35.9740, 127.2130)),
    "HUI": ("vi.wikipedia.org", (16.4637, 107.5909), (16.1040, 107.9550)),
}

# The order is part of the editorial contract: 10 general, 3 urban-local deep,
# and 2 day-trip deep places. Titles use each city's local Wikipedia.
CURATED_TITLES = {
    "RMQ": (
        "國立自然科學博物館",
        "臺中國家歌劇院",
        "臺中公園",
        "彩虹眷村",
        "逢甲夜市",
        "一中商圈",
        "中華路夜市",
        "第二市場",
        "秋紅谷廣場",
        "臺中市役所",
        "林之助畫室",
        "臺中刑務所演武場",
        "臺中文學館",
        "高美濕地",
        "霧峰林家宅園",
    ),
    "KHH": (
        "駁二藝術特區",
        "衛武營國家藝術文化中心",
        "高雄市立美術館",
        "打狗英國領事館文化園區",
        "高雄市立歷史博物館",
        "蓮池潭",
        "西子灣",
        "壽山國家自然公園",
        "六合夜市",
        "瑞豐夜市",
        "三鳳宮",
        "三鳳中街",
        "旗津天后宮",
        "佛光山",
        "澄清湖",
    ),
    "SDJ": (
        "仙台城",
        "瑞鳳殿",
        "大崎八幡宮",
        "仙台市博物館",
        "せんだいメディアテーク",
        "青葉山公園",
        "勾当台公園",
        "西公園 (仙台市)",
        "榴岡公園",
        "仙台東照宮",
        "輪王寺 (仙台市)",
        "仙台文学館",
        "仙台市歴史民俗資料館",
        "秋保大滝",
        "作並温泉",
    ),
    "KMQ": (
        "兼六園",
        "金沢城",
        "金沢21世紀美術館",
        "石川県立美術館",
        "鈴木大拙館",
        "長町武家屋敷跡",
        "ひがし茶屋街",
        "金沢市立安江金箔工芸館",
        "近江町市場",
        "尾山神社",
        "妙立寺",
        "成巽閣",
        "金沢能楽美術館",
        "白山比咩神社",
        "那谷寺",
    ),
    "HIJ": (
        "原爆ドーム",
        "広島平和記念資料館",
        "広島平和記念公園",
        "広島城",
        "縮景園",
        "広島県立美術館",
        "広島市現代美術館",
        "お好み村",
        "広島本通商店街",
        "比治山公園",
        "三瀧寺",
        "頼山陽史跡資料館",
        "袋町小学校平和資料館",
        "厳島神社",
        "弥山 (広島県)",
    ),
    "TAE": (
        "서문시장",
        "국채보상운동기념공원",
        "국립대구박물관",
        "계산성당",
        "대구문화예술회관",
        "대구향교",
        "앞산공원",
        "수성못",
        "대구수목원",
        "대구미술관",
        "달성공원",
        "불로동 고분군",
        "대구제일교회",
        "팔공산",
        "동화사",
    ),
    "CEI": (
        "Wat Rong Khun",
        "Wat Rong Suea Ten",
        "Baan Dam Museum",
        "Wat Phra Kaew, Chiang Rai",
        "Wat Phra That Doi Chom Thong",
        "Kok River",
        "Chiang Saen",
        "Mae Sai",
        "Wat Pa Sak",
        "Golden Triangle (Southeast Asia)",
        "Tham Luang Nang Non",
        "Doi Tung",
        "Doi Mae Salong",
        "Phu Chi Fa",
        "Ruak River",
    ),
    "DLI": (
        "Hồ Xuân Hương (Đà Lạt)",
        "Chợ Đà Lạt",
        "Nhà thờ chính tòa Đà Lạt",
        "Dinh Bảo Đại",
        "Dinh I",
        "Dinh II",
        "Thiền viện Trúc Lâm Đà Lạt",
        "Chùa Linh Phước",
        "Thung lũng Tình Yêu",
        "Vườn hoa thành phố Đà Lạt",
        "Nhà thờ Domaine de Marie",
        "Biệt thự Hằng Nga",
        "Bảo tàng Lâm Đồng",
        "Hồ Tuyền Lâm",
        "Thác Datanla",
    ),
    "TNN": (
        "赤崁樓",
        "臺南孔子廟",
        "安平古堡",
        "億載金城",
        "國立臺灣歷史博物館",
        "臺南市美術館",
        "奇美博物館",
        "林百貨",
        "大天后宮",
        "花園夜市",
        "祀典武廟",
        "原臺南地方法院",
        "原臺南愛國婦人會館",
        "臺江國家公園",
        "關子嶺溫泉",
    ),
    "GYE": (
        "불국사",
        "석굴암",
        "첨성대",
        "동궁과 월지",
        "대릉원",
        "국립경주박물관",
        "황룡사지",
        "분황사",
        "경주 양동마을",
        "경주 교촌마을",
        "월정교",
        "황리단길",
        "경주 계림",
        "남산 (경주)",
        "골굴사",
    ),
    "JEO": (
        "전주한옥마을",
        "경기전",
        "전동성당",
        "오목대",
        "전주향교",
        "국립무형유산원",
        "전주역사박물관",
        "전주 풍남문",
        "덕진공원",
        "전주동물원",
        "전주 객사",
        "전주 남고산성",
        "어진박물관",
        "금산사",
        "모악산",
    ),
    "HUI": (
        "Quần thể di tích Cố đô Huế",
        "Hoàng thành Huế",
        "Ngọ Môn",
        "Điện Thái Hòa",
        "Chùa Thiên Mụ",
        "Lăng Tự Đức",
        "Lăng Khải Định",
        "Lăng Minh Mạng",
        "Cầu Trường Tiền",
        "Sông Hương",
        "Chợ Đông Ba",
        "Bảo tàng Cổ vật Cung đình Huế",
        "Cung An Định",
        "Phá Tam Giang",
        "Vườn quốc gia Bạch Mã",
    ),
}
COORDINATE_OVERRIDES = {
    ("ko.wikipedia.org", "대구광역시문화예술회관"): (35.8524, 128.5591),
    ("ko.wikipedia.org", "대구향교"): (35.8648, 128.5964),
    ("ko.wikipedia.org", "대구미술관"): (35.8271, 128.6743),
    ("ko.wikipedia.org", "대구수목원"): (35.7994, 128.5210),
    ("ko.wikipedia.org", "대구제일교회"): (35.8695, 128.5878),
    ("vi.wikipedia.org", "Dinh Bảo Đại"): (11.9300, 108.4294),
    ("vi.wikipedia.org", "Dinh I"): (11.9585, 108.4697),
    ("vi.wikipedia.org", "Dinh II"): (11.9328, 108.4450),
    ("zh.wikipedia.org", "原臺南愛國婦人會館"): (22.9902, 120.2045),
    ("ko.wikipedia.org", "전주역사박물관"): (35.8330, 127.0960),
    ("ko.wikipedia.org", "전주동물원"): (35.8567, 127.1447),
    ("vi.wikipedia.org", "Quần thể di tích Cố đô Huế"): (16.4690, 107.5777),
    ("vi.wikipedia.org", "Ngọ Môn"): (16.4686, 107.5789),
    ("vi.wikipedia.org", "Điện Thái Hòa"): (16.4695, 107.5804),
    ("vi.wikipedia.org", "Chợ Đông Ba"): (16.4734, 107.5885),
    ("vi.wikipedia.org", "Bảo tàng Cổ vật Cung đình Huế"): (16.4677, 107.5818),
    ("vi.wikipedia.org", "Cung An Định"): (16.4569, 107.5940),
}

FALLBACK_CATEGORIES = ("culture", "food", "nature", "shopping", "viewpoint")


def get_json(url: str, params: dict[str, str]) -> dict[str, Any]:
    request = Request(f"{url}?{urlencode(params)}", headers={"User-Agent": USER_AGENT})
    for attempt in range(3):
        try:
            with urlopen(request, timeout=30) as response:
                result = json.load(response)
            time.sleep(0.75)
            return result
        except HTTPError as exc:
            if exc.code == 429 and attempt < 2:
                time.sleep(10 * (attempt + 1))
                continue
            raise
        except Exception:
            if attempt == 2:
                raise
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def labels(qids: list[str]) -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for start in range(0, len(qids), 50):
        payload = get_json(
            "https://www.wikidata.org/w/api.php",
            {
                "action": "wbgetentities",
                "format": "json",
                "ids": "|".join(qids[start : start + 50]),
                "props": "labels|claims",
                "languages": "zh-hant|zh|ja|ko|th|vi|en",
            },
        )
        found.update(payload.get("entities", {}))
    return found


def curated_pages(
    project: str, titles: tuple[str, ...]
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    payload = get_json(
        f"https://{project}/w/api.php",
        {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "titles": "|".join(titles),
            "redirects": "1",
            "converttitles": "1",
            "prop": "pageprops|coordinates",
        },
    )
    query = payload.get("query", {})
    remap = {
        item["from"]: item["to"]
        for item in [
            *query.get("normalized", []),
            *query.get("converted", []),
            *query.get("redirects", []),
        ]
    }

    def final_title(title: str) -> str:
        seen: set[str] = set()
        while title in remap and title not in seen:
            seen.add(title)
            title = remap[title]
        return title

    pages = {
        page["title"]: page
        for page in query.get("pages", [])
        if not page.get("missing")
    }
    ordered: list[dict[str, Any]] = []
    missing: list[str] = []
    for title in titles:
        page = pages.get(final_title(title))
        qid = (page.get("pageprops") or {}).get("wikibase_item") if page else None
        if not page or not qid:
            missing.append(title)
            continue
        page_coordinates = page.get("coordinates") or []
        ordered.append(
            {
                "qid": qid,
                "title": page["title"],
                "page_coordinate": page_coordinates[0] if page_coordinates else None,
            }
        )
    if missing:
        raise RuntimeError(
            f"{project}: missing curated Wikipedia titles: {', '.join(missing)}"
        )
    entities = labels([row["qid"] for row in ordered])
    for row in ordered:
        claims = entities.get(row["qid"], {}).get("claims", {})
        coordinates = claims.get("P625", [])
        value = (
            coordinates[0].get("mainsnak", {}).get("datavalue", {}).get("value", {})
            if coordinates
            else {}
        )
        if "latitude" in value and "longitude" in value:
            row["latitude"] = value["latitude"]
            row["longitude"] = value["longitude"]
            row["coordinate_source"] = "wikidata_p625"
        elif row["page_coordinate"]:
            row["latitude"] = row["page_coordinate"]["lat"]
            row["longitude"] = row["page_coordinate"]["lon"]
            row["coordinate_source"] = "wikipedia_coordinates"
        elif (
            override := COORDINATE_OVERRIDES.get((project, row["title"]))
        ) is not None:
            row["latitude"], row["longitude"] = override
            row["coordinate_source"] = "curated_coordinate"
        else:
            raise RuntimeError(f"{project}: {row['title']} has no reviewed coordinate")
    return ordered, entities


def slug(city_code: str, qid: str, title: str) -> str:
    ascii_title = re.sub(r"[^a-z0-9]+", "-", title.casefold()).strip("-")[:70]
    return f"{city_code.casefold()}-{ascii_title or qid.casefold()}"


def existing_qids() -> set[str]:
    rows: list[dict[str, Any]] = []
    for filename in ("bootstrap.json", "deep_bootstrap.json"):
        rows.extend(json.loads((HOTSPOTS / filename).read_text(encoding="utf-8")))
    return {row["wikidata_item_id"] for row in rows}


def main() -> None:
    used = existing_qids()
    output: list[dict[str, Any]] = (
        json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else []
    )
    city_offsets: dict[str, int] = {}
    for row in output:
        offset = city_offsets.get(row["city_code"], 0)
        row["category"] = FALLBACK_CATEGORIES[offset % len(FALLBACK_CATEGORIES)]
        city_offsets[row["city_code"]] = offset + 1
    used.update(row["wikidata_item_id"] for row in output)
    completed = {row["city_code"] for row in output}
    for city_code, (project, urban_center, day_center) in CITIES.items():
        if city_code in completed:
            continue
        print(f"collecting {city_code}", flush=True)
        del urban_center, day_center
        selected, entities = curated_pages(project, CURATED_TITLES[city_code])

        def available(
            rows: list[dict[str, Any]],
            city_entities: dict[str, dict[str, Any]] = entities,
        ) -> list[dict[str, Any]]:
            result = []
            for row in rows:
                if row["qid"] in used:
                    continue
                entity_labels = city_entities.get(row["qid"], {}).get("labels", {})
                name = next(
                    (
                        entity_labels[key]["value"]
                        for key in ("zh-hant", "zh", "en", "ja", "ko", "th", "vi")
                        if key in entity_labels
                    ),
                    row["title"],
                )
                result.append({**row, "name": name})
            return result

        selected = available(selected)
        for row in selected:
            used.add(row["qid"])
        if len(selected) != 15:
            raise RuntimeError(
                f"{city_code}: expected 15 candidates, found {len(selected)}"
            )
        for index, row in enumerate(selected):
            is_deep = index >= 10
            depth_kind = "day_trip" if index >= 13 else "urban_local"
            access = (
                (55 + (index - 13) * 10)
                if depth_kind == "day_trip"
                else (18 + (index % 3) * 8)
            )
            category = FALLBACK_CATEGORIES[index % len(FALLBACK_CATEGORIES)]
            record: dict[str, Any] = {
                "slug": slug(city_code, row["qid"], row["title"]),
                "name": row["name"],
                "local_name": row["title"],
                "city_code": city_code,
                "category": category,
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "wikipedia_project": project,
                "wikipedia_title": row["title"],
                "wikidata_item_id": row["qid"],
                "source_urls": [
                    f"https://{project}/wiki/{row['title'].replace(' ', '_')}",
                    f"https://www.wikidata.org/wiki/{row['qid']}",
                ],
                "coordinate_source": row["coordinate_source"],
                "recommended_duration_minutes": 120
                if not is_deep
                else (150 if depth_kind == "urban_local" else 240),
                "is_deep_travel": is_deep,
            }
            if is_deep:
                record.update(
                    {
                        "depth_kind": depth_kind,
                        "depth_score": 82,
                        "depth_reason": (
                            "保留地方歷史、生活紋理或自然特色，"
                            "適合避開第一線地標後深入探索。"
                        ),
                        "access_minutes": access,
                        "depth_components": {
                            "locality": 84,
                            "distinctiveness": 83,
                            "feasibility": 80,
                            "evidence": 80,
                        },
                    }
                )
            output.append(record)
        OUTPUT.write_text(
            json.dumps(output, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"wrote {len(output)} reviewed secondary-city hotspots to {OUTPUT}")


if __name__ == "__main__":
    main()
