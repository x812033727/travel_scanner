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
    "N Seoul Tower": "n-seoul-tower",
    "Haeundae Beach": "haeundae-beach",
    "Gamcheon Culture Village": "gamcheon-culture-village",
    "Seongsan Ilchulbong": "seongsan-ilchulbong",
    "Hallasan": "hallasan",
    "Grand Palace": "grand-palace-bangkok",
    "Wat Arun": "wat-arun",
    "Wat Phra That Doi Suthep": "doi-suthep",
    "Tha Phae Gate": "tha-phae-gate",
    "Old Phuket Town": "phuket-old-town",
    "Patong Beach": "patong-beach",
    "Railay Beach": "railay-beach",
    "Ao Nang": "ao-nang",
}


def _load_seeds() -> tuple[HotspotSeed, ...]:
    rows = json.loads(Path(__file__).with_name("bootstrap.json").read_text(encoding="utf-8"))
    seeds: list[HotspotSeed] = []
    for row in rows:
        city = CITY_BY_CODE[row["city_code"]]
        title = row["wikipedia_title"]
        seeds.append(
            HotspotSeed(
                slug=LEGACY_SLUGS.get(title, f"wikidata-{row['wikidata_item_id'].lower()}"),
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
            )
        )
    if len(seeds) != 170:
        raise RuntimeError(f"expected 170 reviewed hotspots, found {len(seeds)}")
    if len({seed.wikidata_item_id for seed in seeds}) != len(seeds):
        raise RuntimeError("bootstrap hotspot Wikidata IDs must be unique")
    if len({seed.slug for seed in seeds}) != len(seeds):
        raise RuntimeError("bootstrap hotspot slugs must be unique")
    return tuple(seeds)


HOTSPOT_SEEDS = _load_seeds()
