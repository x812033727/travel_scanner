---
id: 2026-10-02-oka-american-village-prod-check
title: Production check after the American Village seed fix: OKA row reconciled, Osaka row has Q4745722, stale Osaka guides and place profile cleared
status: open
priority: P3
area: ops
owner:
claimed_at:
created_at: 2026-10-02T19:45:33Z
completed_at:
branch:
depends_on:
  - 2026-09-06-oka-amerikamura-wrong-qid
scope:
  - docs/hotspot-review-next-batch.md
---

# Production check after the American Village seed fix: OKA row reconciled, Osaka row has Q4745722, stale Osaka guides and place profile cleared

## Why

Task `2026-09-06-oka-amerikamura-wrong-qid` corrected the repository seed only. The Okinawa
美國村 row keeps its public slug `wikidata-q4745722` (pinned in `bootstrap.json`) but now names
Q11609171, Mihama Town Resort American Village, at 26.316183, 127.756668 in 北谷町; the Osaka
shop row `kix-amerikamura` takes Q4745722 back.

Production only follows if `seed_catalog` (run by every `hotspot-collector` pass, at most six
hours apart) still owns the existing row: `_seed_can_reconcile_hotspot` in
`apps/api/app/hotspots/service.py` skips any row with a reviewer, a map verification, a Place
ID, a Naver URL or a coordinate source other than curated/wikidata, and the seeder also skips
it when another row already holds Q11609171 (for example a discovery row
`wikidata-q11609171`). When the Okinawa row is skipped, `kix-amerikamura` is skipped too,
because Q4745722 is still taken. `/admin` cannot repair that: the review endpoint refuses to
replace an existing QID (409 `hotspot_wikidata_identity_locked`).

The seed also never touches what was gathered for the row while it pointed at Osaka: guides,
AI intros and the Google place profile may all describe 大阪アメリカ村.

## Definition of done

- [ ] After the deploy and one collector pass, production `wikidata-q4745722` holds Q11609171,
      sits in Chatan (`area_code` `chatan`), and `kix-amerikamura` holds Q4745722.
- [ ] No approved guide, intro or place profile on `wikidata-q4745722` describes Osaka.
- [ ] The result is written down in `docs/hotspot-review-next-batch.md`.

## Steps

- [ ] Read-only, on the host (`<SSH>`/`<COMPOSE>` from skill `deploy`), in `psql`:
      `SELECT id, slug, city_code, wikidata_item_id, latitude, longitude, area_code, origin,
      review_status, map_match_status, google_place_id, reviewed_by_user_id,
      coordinate_source_type, wikipedia_title FROM travel_hotspots WHERE slug IN
      ('wikidata-q4745722', 'kix-amerikamura', 'wikidata-q11609171') OR wikidata_item_id IN
      ('Q4745722', 'Q11609171');`
- [ ] If the Okinawa row still holds Q4745722, name the column that made the seeder skip it
      and take the options to the owner (站主決定); do not write SQL by hand without that.
      A discovery row for Q11609171 is the same place: the owner decides which row survives.
- [ ] With the Okinawa row's `id`: list `hotspot_guides` (`locale`, `title`, `canonical_url`,
      `review_status`), `hotspot_intros` (`locale`, `review_status`, start of `body`) and
      `hotspot_place_profiles` (`candidate_name`, `candidate_address`, `formatted_address`,
      `google_maps_uri`). Anything about Osaka gets rejected or disabled through `/admin`
      (skill `hotspot-review`), and the Place ID is found again for Chatan
      (`references/place-ids.md`).
- [ ] Write the numbers and the decision into `docs/hotspot-review-next-batch.md`.

## How to verify

`GET https://mokaair.com/api/travel/hotspots/rankings?destination_id=okinawa&q=美國村` lists the
row with the Chatan area, and `destination_id=osaka-kyoto&q=アメリカ村` lists `kix-amerikamura`.

## Notes

- Evidence for the seed (2026-10-03): Wikidata Q11609171 P625 26.316183, 127.756668 (P131
  北谷町 Q1351759); the ja-wiki page 美浜タウンリゾート・アメリカンビレッジ links that item and
  carries the same coordinate; OpenStreetMap (Nominatim) has the bus stops
  美浜アメリカンビレッジ北口 and 南口 136 m and 216 m away, in 美浜, 北谷町.
- Nothing on the production host was read or changed while filing this.
