---
id: 2026-09-12-discovery-only-sees-100-articles-per-centre
title: Wikimedia discovery can only ever see the 100 nearest articles within 10 km of each city centre
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T08:43:12Z
created_at: 2026-09-12T14:00:00Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/hotspots/discovery.py
  - apps/api/app/hotspots/cities.py
  - apps/api/tests/test_hotspot_discovery.py
  - apps/api/app/hotspots/service.py
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

- [x] Discovery covers a city's configured radius rather than a 10 km ring. `geosearch` cannot
      do it in one call, so this means several search points per city (a ring or grid of
      sub-centres inside `radius_km`), or a different source such as a Wikidata SPARQL
      `wikibase:around` query, which has neither cap and is already used elsewhere in this
      repo's measurements.
- [x] The per-call 100-result cap no longer decides what a city can ever contain; state the new
      bound explicitly in a comment.
- [x] `HotspotCity.centers[].radius_km` either means what it says, or the field is renamed and
      documented so nobody configures 30 again and gets 10.
- [x] A test pins the behaviour for a city whose radius exceeds 10 km.

## How to verify

`uv run pytest apps/api/tests/test_hotspot_discovery.py`, plus a dry count of how many distinct
QIDs a single city yields before and after, and a check that at least the nine rows above fall
inside the new coverage.

## Notes

Cost control matters here: widening coverage widens the review queue, which is the thing
2026-09-12 spent a day draining. Pair any widening with the type denylist and, preferably, with
a cap on how many *new* pending rows a single pass may add.

### 2026-09-19 done in repo (claude-fable-5-1)

- Live `paraminfo` for `list=geosearch` (2026-09-19): `gsradius` max 10 000 m, `gslimit` max 500
  (5 000 for bots). Both constants are named in `discovery.py` with the reason.
- `search_points(center)`: a radius within 10 km is one call; a larger one is a hexagonal
  lattice of 10 km circles (spacing r·√3, lattice points kept up to R + r), which covers the
  whole configured disk. Tokyo's 30 km takes 19 calls, the 100 km centre about 150. Each call
  asks for 500 pages. Pages are deduplicated by pageid across calls and **dropped when they lie
  outside every centre's radius** (fringe circles see past R); the old `outside_city_radius`
  rule stays only as a rounding safety net, so the review queue is not flooded by the fringe.
- Candidates are ordered nearest-first and `discover_city(..., skip=...)` leaves out items the
  catalogue has already decided on; `discover_hotspots` passes the approved, rejected, disabled
  and curated QIDs. So the per-run limit (`hotspot_discovery_candidate_limit`, 100) now picks the
  nearest hundred *new or pending* items each week and the pass advances across the radius
  instead of returning the same hundred forever. Pending rows are still re-discovered
  (refreshed), which also keeps the queue from growing faster than it is read. The new bound is
  stated in the module comment: a city sees every page inside its configured radius.
- `DiscoveryCenter.radius_km` now means what it says (docstring in `cities.py`); no city was
  reconfigured. The two 8 km centres and the 10 km one now see exactly their radius instead of
  a 10 km ring.
- Tests: lattice geometry (one call under the cap; every sampled point of a 30 km disk within
  10 km of a lattice point; no point past R + r), a 30 km city reaching a page 25 km out while a
  page 45 km out is dropped, nearest-first order, the skip list, and the rewritten radius test
  (a page past the radius is not a candidate; a denied type inside it is rejected, not queued).
- Cost: roughly 800 geosearch calls plus pageprops batches per weekly pass instead of 68; the
  client keeps its identifying User-Agent and retry/backoff. After the next pass, compare
  `added` in the collector report and spot-check Kabuki-za (Q1132766) and Tokyo International
  Forum (Q1141234) under NRT.
