from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from app.hotspots.cities import CITY_BY_CODE
from app.i18n import LOCALES
from app.localized_names import (
    build_localized_names,
    has_han_script,
    is_latin_script,
    original_locale_for,
)

# Wikipedia disambiguation suffixes ("Hongdae (area)") are not display names.
_DISAMBIGUATION = re.compile(r"\s*\([^)]*\)\s*$")


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
    # Who proposed the place ("gemini" for the AI-curated Kanto list, "editorial" for
    # rows added by hand to complete a destination); surfaced to admins only.
    provenance: str | None = None
    # Labels fetched from Wikidata by `python -m app.cli fill-hotspot-labels`, keyed by
    # site locale; they fill the locales the seed cannot derive from its curated text.
    names: dict[str, str] = field(default_factory=dict)

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
    def original_name(self) -> str | None:
        """The name in the script of the destination country (原文), when the seed knows it.

        Reviewed rows carry ``local_name``. Otherwise the Traditional Chinese
        catalog name already is the original for Taiwan and Hong Kong, and a
        Wikipedia title on the country's own wiki (``ja.wikipedia.org`` for
        Japan) is the original elsewhere. English-wiki titles are not.
        """

        if self.local_name:
            return self.local_name
        language = original_locale_for(self.country_code)
        if language == "zh-TW":
            return self.name
        if (
            language
            and self.wikipedia_project
            and self.wikipedia_title
            and self.wikipedia_project.split(".", 1)[0] == language
        ):
            return self.wikipedia_title
        return self.names.get(language) if language else None

    @property
    def english_name(self) -> str | None:
        """A romanized label: the first Latin-script alias or an English Wikipedia title."""

        for alias in self.aliases:
            if is_latin_script(alias):
                return _DISAMBIGUATION.sub("", alias).strip() or None
        if self.wikipedia_project == "en.wikipedia.org" and self.wikipedia_title:
            return _DISAMBIGUATION.sub("", self.wikipedia_title).strip() or None
        return None

    @property
    def localized_names(self) -> dict[str, str]:
        """Five site locales plus the original text, derived from the reviewed seed.

        The catalog name is Traditional Chinese; English comes from the seed's
        Latin-script alias or English Wikipedia title; the country's own
        language takes the original. Wikidata labels stored in ``names`` fill
        the other locales, and whatever is still missing falls back through
        :data:`app.localized_names.FALLBACK_LOCALES` so every hotspot always
        has a label in every language.
        """

        labels: dict[str, str] = {
            locale: value
            for locale, value in self.names.items()
            if locale in LOCALES and locale != "zh-TW" and value
        }
        if self.english_name:
            # A reviewed alias or title beats a fetched label.
            labels["en"] = self.english_name
        # The catalog name is the zh-TW label only when it is actually written in
        # Chinese. 22 seeds are curated under their Hangul or Thai name, and claiming
        # those as Traditional Chinese showed Korean script to Chinese readers; leaving
        # the slot empty lets the fallback chain reach the English label instead, and
        # ``fallback`` still catches the rows where nothing better exists.
        chinese = {"zh-TW": self.name} if has_han_script(self.name) else {}
        return build_localized_names(
            names={**chinese, **labels},
            original=self.original_name,
            country_code=self.country_code,
            fallback=self.name,
        )

    @property
    def search_text(self) -> str:
        return " ".join(
            (
                self.name,
                *self.aliases,
                *self.localized_names.values(),
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
    "Akiu Great Falls": "nature",
    "Apsan Park": "nature",
    "Bullodong Tumuli in Daegu": "culture",
    "DeokJin Park": "nature",
    "National Debt Redemption Movement Memorial Park": "culture",
    "Phu Chi Fa": "nature",
    "Sendai Literature Museum": "culture",
    "Tam Giang lagoon": "nature",
    "The Love Valley": "nature",
    "Tsutsujigaoka Park": "nature",
    "Tuyền Lâm Lake": "nature",
    "Wat Pa Sak": "culture",
    "Ōmichō Market": "food",
    "三鳳中街": "food",
    "二鯤鯓砲臺": "culture",
    "仙臺市博物館": "culture",
    "佛光山": "culture",
    "保大宮": "culture",
    "八公山": "nature",
    "六合夜市": "food",
    "勾當臺公園": "nature",
    "原臺南地方法院": "culture",
    "台中大都會歌劇院": "culture",
    "台江國家公園": "nature",
    "嚴島神社": "culture",
    "场钱桥": "culture",
    "大叻竹林禅院": "culture",
    "大天后宮": "culture",
    "大稻埕慈聖宮": "food",
    "奇美博物館": "culture",
    "廣島和平紀念資料館": "culture",
    "廣島城": "culture",
    "廣島市現代美術館": "culture",
    "彩虹眷村": "culture",
    "慶基殿": "culture",
    "慶州南山": "nature",
    "慶州東宮": "culture",
    "應陵": "culture",
    "成巽閣": "culture",
    "打狗英國領事館及領事官邸": "culture",
    "柳川市": "culture",
    "桂山聖堂": "culture",
    "梧木臺": "culture",
    "清盛": "culture",
    "玉佛寺": "culture",
    "瑞鳳殿": "culture",
    "疯狂屋": "culture",
    "白山比咩神社": "culture",
    "皇龍寺": "culture",
    "石川縣立美術館": "culture",
    "石窟庵": "culture",
    "秋紅谷生態公園": "nature",
    "臺中刑務所演武場": "culture",
    "臺南孔子廟": "culture",
    "良洞村": "culture",
    "莱东": "nature",
    "衛武營國家藝術文化中心": "culture",
    "西子灣風景區": "nature",
    "賴山陽史蹟資料館": "culture",
    "金山寺": "culture",
    "金澤城": "culture",
    "順化宮廷古物博物館": "culture",
    "順化皇城": "culture",
    "高美濕地": "nature",
    "龙苏町寺": "culture",
    "대구수목원": "nature",
    "전주 남고산성": "culture",
    "전주역사박물관": "culture",
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
    kanto_rows = json.loads(
        Path(__file__).with_name("kanto_expansion_bootstrap.json").read_text(encoding="utf-8")
    )
    rows = [*base_rows, *deep_rows, *secondary_rows, *food_area_rows, *kanto_rows]
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
                provenance=row.get("provenance"),
                names=dict(row.get("names") or {}),
            )
        )
    if (
        len(base_rows) != 170
        or len(deep_rows) != 95
        or len(secondary_rows) != 180
        or len(food_area_rows) != 5
        or len(kanto_rows) != 113
        or len(seeds) != 563
    ):
        raise RuntimeError(
            "expected 170 standard + 95 deep + 180 secondary + 5 food-area "
            "+ 113 Kanto-expansion hotspots, "
            f"found {len(base_rows)} + {len(deep_rows)} + {len(secondary_rows)} + "
            f"{len(food_area_rows)} + {len(kanto_rows)}"
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
    if len(deep) != 165 or any((seed.depth_score or 0) < 70 for seed in deep):
        raise RuntimeError("deep bootstrap must contain exactly 165 reviewed scores >= 70")
    food_destinations = {seed.destination_id for seed in seeds if seed.category == "food"}
    missing_food_destinations = sorted(
        set(CITY_BY_CODE) - {seed.city_code for seed in seeds if seed.category == "food"}
    )
    if missing_food_destinations or len(food_destinations) != 33:
        raise RuntimeError(
            f"every destination must have a reviewed food area; missing {missing_food_destinations}"
        )
    return tuple(seeds)


HOTSPOT_SEEDS = _load_seeds()
