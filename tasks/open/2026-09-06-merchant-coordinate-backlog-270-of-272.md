---
id: 2026-09-06-merchant-coordinate-backlog-270-of-272
title: Merchant coordinate backlog: 270 of 272 merchants cannot be published
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-06T00:51:53Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/place_matching.py
  - apps/api/app/foods/coordinate_queue.py
---

# Merchant coordinate backlog: 270 of 272 merchants cannot be published

## Why

`publishable_merchant_filters()` needs a durable coordinate — latitude/longitude with a
`coordinate_source_type` in curated / wikidata / official_tourism / merchant_official /
admin_verified and an https `coordinate_source_url`. Production on 2026-09-06 holds 272
food merchants and **2 have one**, so the public merchant directory is empty of nearly
everything the catalogue describes.

Everything mechanical is already done. What is left needs a person, and this task exists to
say exactly how much and through which screen, so nobody rebuilds the tooling again.

Counts from production on 2026-09-06 (they move — other sessions keep adding merchants):

| country | merchants | with Place ID | with coordinates |
| --- | --- | --- | --- |
| JP | 85 | 31 | 1 |
| KR | 67 | 0 | 0 |
| TH | 39 | 24 | 0 |
| TW | 37 | 31 | 0 |
| VN | 26 | 26 | 0 |
| SG | 10 | 10 | 1 |
| HK | 8 | 8 | 0 |

142 merchants have **neither** a Place ID nor coordinates, so they cannot even enter the
coordinate review queue, which corroborates against a Google result.

## Definition of done

- [ ] Every non-KR merchant that can have a Place ID has one, so it can enter the queue.
- [ ] The coordinate review queue has been walked and the merchants a reviewer approved
      carry `admin_verified` coordinates.
- [ ] `GET /foods/merchants` returns a non-trivial list for the cities that were worked.
- [ ] The remaining backlog is written down here with a number, so the next reader knows
      whether this is nearly finished or barely started.

## Steps

- [ ] Re-run the Place ID matcher over the merchants added since 2026-09-05; ~112 non-KR
      merchants currently lack one. It skips KR by design and brakes at 90% of the Google
      SKU, so it is safe to run whole:
      `docker compose -f docker-compose.prod.yml exec -T api python -m app.cli match-food-merchant-places --apply`
- [ ] Check how many merchants the queue now offers: `GET /admin/foods/merchants/coordinate-queue`.
- [ ] Walk the queue. Each approval re-resolves the merchant server-side and writes
      `admin_verified` with the public Google Maps page as the source URL, so the reviewer's
      judgement is what is recorded, not a provider coordinate.
- [ ] For KR (67 merchants, no Place ID possible) decide separately: they need a
      `map.naver.com/p/entry/place/…` URL for exact map identity, and nothing in this
      repository produces one. Either an admin pastes them or KR stays unpublished.
- [ ] Update the numbers in this file as you go.

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T postgres sh -lc \
  'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select country_code, count(*), count(latitude) from food_merchants group by 1 order by 1"'
```

and open `/foods` for a city that was worked — merchants should appear rather than an empty
directory.

## Notes

**The automated coordinate path is exhausted; do not rebuild it.** `fill-food-merchant-coordinates`
(PRs #159, #162, #172) reads the merchant's own cited pages and extracts schema.org JSON-LD
or geo meta tags. Run against all 172 merchants on 2026-09-05 it produced:

```
no_source: 109   no_coordinates: 53   fetch_failed: 6   http_500: 1   not_html: 2   filled: 1
```

The single success was `singapore-328-katong-laksa`. 63 merchants had a first-party page,
every one was fetched, and **1 of 63 published a machine-readable coordinate**. A survey of
those 63 pages found: 21 carry JSON-LD without geo, 27 carry nothing, 4 carry a coordinate
in a plain (non-JSON-LD) JSON blob, 1 has only a Google map embed, 9 were unreadable.

Two paths were tried and deliberately rejected:

- **Reading the coordinate out of an embedded Google map** (`!3d..!4d..`, `/@lat,lng`).
  Implemented, then removed in #159 after review: those are Google's coordinates whatever
  page they are pasted into, and storing them as `merchant_official` launders the exact rule
  that bars Places coordinates from storage.
- **Reading a plain `"lat"/"lng"` JSON pair** as a fallback. Implemented on
  `feat/coordinate-json-data`, then deleted unmerged. It would unlock 3 merchants
  (`kamakura-chikaramochiya`, `taipei-lan-jia`, `taipei-chia-te`) but only by bypassing the
  `_is_geo_point` guard added in #162, and all three pages carry JSON-LD without geo, so the
  safe restriction "only when the page declares no structured data" would disable it. Three
  merchants did not justify weakening the rule protecting the other 169. The branch is gone;
  the diff is small enough to redo if someone disagrees.

`admin_verified` is in `DURABLE_COORDINATE_SOURCES` precisely so a human can settle this.
That is the designed path, not a workaround.

Related: `2026-09-06-missing-merchant-sources` is why `no_source` was 109.
