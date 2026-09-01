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
    city_code: str
    city_name: str
    country_code: str
    country_name: str
    category: str
    latitude: float
    longitude: float
    wikipedia_project: str
    wikipedia_title: str
    wikidata_item_id: str
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
    def wikipedia_url(self) -> str:
        path = quote(self.wikipedia_title.replace(" ", "_"))
        return f"https://{self.wikipedia_project}/wiki/{path}"

    @property
    def wikidata_url(self) -> str:
        return f"https://www.wikidata.org/wiki/{self.wikidata_item_id}"

    @property
    def search_text(self) -> str:
        return " ".join(
            (
                self.name,
                *self.aliases,
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


def _load_seeds() -> tuple[HotspotSeed, ...]:
    base_rows = json.loads(Path(__file__).with_name("bootstrap.json").read_text(encoding="utf-8"))
    deep_rows = json.loads(
        Path(__file__).with_name("deep_bootstrap.json").read_text(encoding="utf-8")
    )
    rows = [*base_rows, *deep_rows]
    seeds: list[HotspotSeed] = []
    for row in rows:
        city = CITY_BY_CODE[row["city_code"]]
        title = row["wikipedia_title"]
        seeds.append(
            HotspotSeed(
                slug=row.get(
                    "slug", LEGACY_SLUGS.get(title, f"wikidata-{row['wikidata_item_id'].lower()}")
                ),
                name=row["name"],
                aliases=(title, row["name"]),
                city_code=city.code,
                city_name=city.name,
                country_code=city.country_code,
                country_name=city.country_name,
                category=row["category"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                wikipedia_project=row["wikipedia_project"],
                wikipedia_title=title,
                wikidata_item_id=row["wikidata_item_id"],
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
    if len(base_rows) != 170 or len(deep_rows) != 95 or len(seeds) != 265:
        raise RuntimeError(
            f"expected 170 standard + 95 deep hotspots, found {len(base_rows)} + {len(deep_rows)}"
        )
    if len({seed.wikidata_item_id for seed in seeds}) != len(seeds):
        raise RuntimeError("bootstrap hotspot Wikidata IDs must be unique")
    if len({seed.slug for seed in seeds}) != len(seeds):
        raise RuntimeError("bootstrap hotspot slugs must be unique")
    unmatched = sorted(LEGACY_SLUGS.keys() - {row["wikipedia_title"] for row in rows})
    if unmatched:
        # A renamed wikipedia_title silently drops its curated slug: the attraction
        # re-seeds as wikidata-<id> and the old row is orphaned with no Wikidata id,
        # so it keeps collecting against the stale title. Fail the import instead.
        raise RuntimeError(f"LEGACY_SLUGS keys match no wikipedia_title: {unmatched}")
    deep = [seed for seed in seeds if seed.is_deep_travel]
    if len(deep) != 95 or any((seed.depth_score or 0) < 70 for seed in deep):
        raise RuntimeError("deep bootstrap must contain exactly 95 reviewed scores >= 70")
    return tuple(seeds)


HOTSPOT_SEEDS = _load_seeds()
