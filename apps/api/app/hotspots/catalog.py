from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import quote

from app.hotspots.cities import CITY_BY_CODE


@dataclass(frozen=True)
class HotspotSeed:
    slug: str
    name: str
    aliases: tuple[str, ...]
    destination_id: str
    city_code: str
    city_name: str
    country_code: str
    country_name: str
    category: str
    latitude: float
    longitude: float
    wikipedia_project: str | None
    wikipedia_title: str | None
    wikidata_item_id: str | None
    editorial_relevance: int = 88
    is_deep_travel: bool = False
    depth_kind: str | None = None
    depth_score: float | None = None
    local_name: str | None = None
    depth_reason: str | None = None
    access_minutes: int | None = None
    recommended_duration_minutes: int | None = None
    depth_components: dict[str, int] | None = None
    source_urls: tuple[str, ...] = ()
    coordinate_source: str | None = None

    @property
    def wikipedia_url(self) -> str | None:
        if not self.wikipedia_project or not self.wikipedia_title:
            return None
        path = quote(self.wikipedia_title.replace(" ", "_"))
        return f"https://{self.wikipedia_project}/wiki/{path}"

    @property
    def wikidata_url(self) -> str | None:
        if not self.wikidata_item_id:
            return None
        return f"https://www.wikidata.org/wiki/{self.wikidata_item_id}"

    @property
    def search_text(self) -> str:
        return " ".join(
            (
                self.name,
                *self.aliases,
                self.destination_id,
                self.city_code,
                self.city_name,
                self.country_code,
                self.country_name,
                self.category,
            )
        ).casefold()


LEGACY_SLUGS = {
    "Sensō-ji": "sensoji",
    "Tokyo Skytree": "tokyo-skytree",
    "Dōtonbori": "dotonbori",
    "Fushimi Inari-taisha": "fushimi-inari",
    "Dazaifu Tenmangū": "dazaifu-tenmangu",
    "Ōhori Park": "ohori-park",
    "Sapporo Clock Tower": "sapporo-clock-tower",
    "Otaru Canal": "otaru-canal",
    "Shuri Castle": "shuri-castle",
    "Okinawa Churaumi Aquarium": "churaumi-aquarium",
    "Nagoya Castle": "nagoya-castle",
    "Atsuta Shrine": "atsuta-shrine",
    "Gyeongbokgung": "gyeongbokgung",
    "Namsan Seoul Tower": "n-seoul-tower",
    "Haeundae Beach": "haeundae-beach",
    "Gamcheon Culture Village": "gamcheon-culture-village",
    "Seongsan Ilchulbong": "seongsan-ilchulbong",
    "Hallasan": "hallasan",
    "Grand Palace": "grand-palace-bangkok",
    "Wat Arun": "wat-arun",
    "Wat Phra That Doi Suthep": "doi-suthep",
    "Tha Phae Gate": "tha-phae-gate",
    "Phuket Old Town": "phuket-old-town",
    "Patong": "patong-beach",
    "Railay Beach": "railay-beach",
    "Ao Nang": "ao-nang",
}

FOOD_AREA_NAMES = {
    "Ao Nang",
    "Chợ Cồn",
    "Đông Ba Market",
    "Hwangnidan-gil",
    "Okonomi-mura",
    "Phuket Old Town",
    "ตลาดวโรรส",
    "เกาะเกร็ด",
    "三鳳中街",
    "中峇鲁",
    "中華路夜市",
    "全州韓屋村",
    "円頓寺商店街",
    "國際通",
    "大叻市集",
    "小樽運河",
    "廣藏市場",
    "廟街夜市",
    "新街市",
    "東山東",
    "札嘎其市場",
    "神樂坂",
    "第二市場",
    "花園夜市",
    "西門市場",
    "道頓堀",
    "奧南海灘",
    "普吉老城",
    "鄭王廟周邊",  # Reserved for a future reviewed public food district.
    "錦市場",
    "順化東巴市場",
    "饒河街觀光夜市",
    "Ōmichō Market",
}

CATEGORY_CORRECTIONS = {
    "Apsan Park": "nature",
    "Bullodong Tumuli in Daegu": "culture",
    "National Debt Redemption Movement Memorial Park": "culture",
    "Sendai Literature Museum": "culture",
    "三鳳中街": "food",
    "原臺南地方法院": "culture",
    "台中大都會歌劇院": "culture",
    "大叻竹林禅院": "culture",
    "大稻埕慈聖宮": "food",
    "應陵": "culture",
    "慶基殿": "culture",
    "成巽閣": "culture",
    "柳川市": "culture",
    "疯狂屋": "culture",
    "石窟庵": "culture",
    "皇龍寺": "culture",
    "瑞鳳殿": "culture",
    "臺中刑務所演武場": "culture",
    "臺南孔子廟": "culture",
    "衛武營國家藝術文化中心": "culture",
    "西子灣風景區": "nature",
    "賴山陽史蹟資料館": "culture",
    "金澤城": "culture",
    "順化宮廷古物博物館": "culture",
    "順化皇城": "culture",
    "勾當臺公園": "nature",
    "龙苏町寺": "culture",
    "清盛": "culture",
    "莱东": "nature",
    "廣島市現代美術館": "culture",
    "廣島和平紀念資料館": "culture",
    "전주 남고산성": "culture",
    "전주역사박물관": "culture",
    "奇美博物館": "culture",
}


def _load_seeds() -> tuple[HotspotSeed, ...]:
    base_rows = json.loads(Path(__file__).with_name("bootstrap.json").read_text(encoding="utf-8"))
    deep_rows = json.loads(
        Path(__file__).with_name("deep_bootstrap.json").read_text(encoding="utf-8")
    )
    secondary_rows = json.loads(
        Path(__file__).with_name("secondary_bootstrap.json").read_text(encoding="utf-8")
    )
    food_area_rows = json.loads(
        Path(__file__).with_name("food_area_bootstrap.json").read_text(encoding="utf-8")
    )
    rows = [*base_rows, *deep_rows, *secondary_rows, *food_area_rows]
    seeds: list[HotspotSeed] = []
    for row in rows:
        city = CITY_BY_CODE[row["city_code"]]
        title = row.get("wikipedia_title")
        name = row["name"]
        category = CATEGORY_CORRECTIONS.get(name, row["category"])
        if name in FOOD_AREA_NAMES:
            category = "food"
        seeds.append(
            HotspotSeed(
                slug=row.get(
                    "slug",
                    LEGACY_SLUGS.get(
                        title,
                        f"wikidata-{row['wikidata_item_id'].lower()}"
                        if row.get("wikidata_item_id")
                        else "",
                    ),
                ),
                name=name,
                aliases=tuple(value for value in (title, name, *row.get("aliases", ())) if value),
                destination_id=city.id,
                city_code=city.code,
                city_name=city.name,
                country_code=city.country_code,
                country_name=city.country_name,
                category=category,
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                wikipedia_project=row.get("wikipedia_project"),
                wikipedia_title=title,
                wikidata_item_id=row.get("wikidata_item_id"),
                is_deep_travel=bool(row.get("is_deep_travel", False)),
                depth_kind=row.get("depth_kind"),
                depth_score=row.get("depth_score"),
                local_name=row.get("local_name"),
                depth_reason=row.get("depth_reason"),
                access_minutes=row.get("access_minutes"),
                recommended_duration_minutes=row.get("recommended_duration_minutes"),
                depth_components=row.get("depth_components"),
                source_urls=tuple(row.get("source_urls", ())),
                coordinate_source=row.get("coordinate_source"),
            )
        )
    if (
        len(base_rows) != 170
        or len(deep_rows) != 95
        or len(secondary_rows) != 180
        or len(food_area_rows) != 5
        or len(seeds) != 450
    ):
        raise RuntimeError(
            "expected 170 standard + 95 deep + 180 secondary + 5 food-area hotspots, "
            f"found {len(base_rows)} + {len(deep_rows)} + "
            f"{len(secondary_rows)} + {len(food_area_rows)}"
        )
    qids = [seed.wikidata_item_id for seed in seeds if seed.wikidata_item_id]
    if len(set(qids)) != len(qids):
        raise RuntimeError("bootstrap hotspot Wikidata IDs must be unique")
    if len({seed.slug for seed in seeds}) != len(seeds):
        raise RuntimeError("bootstrap hotspot slugs must be unique")
    unmatched = sorted(LEGACY_SLUGS.keys() - {row.get("wikipedia_title") for row in rows})
    if unmatched:
        # A renamed wikipedia_title silently drops its curated slug: the attraction
        # re-seeds as wikidata-<id> and the old row is orphaned with no Wikidata id,
        # so it keeps collecting against the stale title. Fail the import instead.
        raise RuntimeError(f"LEGACY_SLUGS keys match no wikipedia_title: {unmatched}")
    deep = [seed for seed in seeds if seed.is_deep_travel]
    if len(deep) != 155 or any((seed.depth_score or 0) < 70 for seed in deep):
        raise RuntimeError("deep bootstrap must contain exactly 155 reviewed scores >= 70")
    food_destinations = {seed.destination_id for seed in seeds if seed.category == "food"}
    missing_food_destinations = sorted(
        set(CITY_BY_CODE) - {seed.city_code for seed in seeds if seed.category == "food"}
    )
    if missing_food_destinations or len(food_destinations) != 31:
        raise RuntimeError(
            f"every destination must have a reviewed food area; missing {missing_food_destinations}"
        )
    return tuple(seeds)


HOTSPOT_SEEDS = _load_seeds()
