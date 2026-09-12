---
id: 2026-09-12-discovery-only-sees-100-articles-per-centre
title: Wikimedia discovery can only ever see the 100 nearest articles within 10 km of each city centre
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-12T14:00:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/discovery.py
  - apps/api/app/hotspots/cities.py
  - apps/api/tests/test_hotspot_discovery.py
---

# Discovery can only ever see the 100 nearest articles within 10 km of each city centre

## Why

`WikimediaDiscoveryClient.discover_city` calls the MediaWiki `geosearch` list with

```python
"gsradius": str(min(center.radius_km * 1000, 10_000)),
"gslimit": str(min(limit, 100)),
```

`geosearch` caps `gsradius` at 10 km and `gslimit` at 100, and returns results **ordered by
distance**. So however large a city's configured `radius_km` is, discovery only ever sees the
100 Wikipedia articles nearest each centre, none of them more than 10 km out. Tokyo's centre
is configured with `radius_km=30`; that 30 is silently clamped to 10.

This is not theoretical. Of the 40 rows this batch gave a verified `wikidata_item_id` so that
discovery could adopt them, **9 sit outside the 10 km ring and could never be re-discovered**:

| row | city | km from centre |
|---|---|---|
| Huyện Sỹ Church | SGN | 24.7 |
| Tsuboya Pottery Museum | OKA | 17.6 |
| Ko Thap | KBV | 17.4 |
| Sōgen-ji | OKA | 17.1 |
| Klong Muang Beach | KBV | 16.8 |
| Asakusa Hanayashiki | NRT | 13.8 |
| Cape Maeda | OKA | 12.8 |
| Kabuki-za | NRT | 10.7 |
| Tokyo International Forum | NRT | 10.3 |

Kabuki-za and the Tokyo International Forum are not obscure. They were missing from the
catalogue because discovery structurally cannot reach them, and the same is true of the top-100
cut: in Tokyo the 100 nearest articles to Shibuya do not get anywhere near the interesting parts
of the city.

The 2026-09-12 batch worked around it by writing each row's Wikidata P625 coordinate directly
instead of waiting for adoption, so nothing is currently stuck — but the collector will keep
producing a queue drawn from the same narrow window.

## Definition of done

- [ ] Discovery covers a city's configured radius rather than a 10 km ring. `geosearch` cannot
      do it in one call, so this means several search points per city (a ring or grid of
      sub-centres inside `radius_km`), or a different source such as a Wikidata SPARQL
      `wikibase:around` query, which has neither cap and is already used elsewhere in this
      repo's measurements.
- [ ] The per-call 100-result cap no longer decides what a city can ever contain; state the new
      bound explicitly in a comment.
- [ ] `HotspotCity.centers[].radius_km` either means what it says, or the field is renamed and
      documented so nobody configures 30 again and gets 10.
- [ ] A test pins the behaviour for a city whose radius exceeds 10 km.

## How to verify

`uv run pytest apps/api/tests/test_hotspot_discovery.py`, plus a dry count of how many distinct
QIDs a single city yields before and after, and a check that at least the nine rows above fall
inside the new coverage.

## Notes

Cost control matters here: widening coverage widens the review queue, which is the thing
2026-09-12 spent a day draining. Pair any widening with the type denylist and, preferably, with
a cap on how many *new* pending rows a single pass may add.
