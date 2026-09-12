---
id: 2026-09-12-re-add-the-seoul-national-folk
title: Re-add the Seoul National Folk Museum after its Wikidata QID was tombstoned
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-12T02:09:36Z
completed_at:
branch:
depends_on: []
scope:
  - docs/hotspot-review-next-batch.md
---

# Re-add the Seoul National Folk Museum after its Wikidata QID was tombstoned

## Why

Hotspot `557a6eb0-0592-4ab2-b2a9-707eabb0febb` (國立民俗博物館, QID **Q486449**) sat pending
under city `PUS` (Busan) even though the museum is in Seoul. On 2026-09-12 a Gemini
catalog-review recommendation from run `0a194879` rejected it — "目的地設為釜山，但該實體位於
首爾特別市，目的地歸屬與地理座標完全不符" — and that rejection was applied at 01:56 UTC.

The rejection of that row is defensible: the row really was wrong. The cost is that
`discover_hotspots` skips rows whose `review_status` is `rejected`/`disabled`, keyed by
Wikidata QID, so the weekly Wikimedia pass will never re-add this museum under Seoul.
The catalog now holds no row for it at all — a genuine Seoul attraction is missing.

## Definition of done

- [ ] The museum exists in the catalog under Seoul with an exact map identity (Naver for
      KR, per the publication gate), durable coordinates and their source, and is approved.
- [ ] It appears in the public rankings for the Seoul destination.
- [ ] The wrong Busan row stays rejected, or is corrected in place through a reviewed
      process — no blanket un-rejection of tombstones.

## Steps

- [ ] Pick the route: a curated seed entry, `import-hotspot-candidates --apply` with a
      manifest, or a reviewed correction of the existing row's destination.
- [ ] Get the identity the gate requires (KR rows need an exact Naver map URL, not a
      Google Place ID) and take coordinates from Wikidata P625 with its source URL.
- [ ] Apply through the normal admin review flow so the audit records a real actor.

## How to verify

Read-only first: `select id, name, city_code, review_status from travel_hotspots where
wikidata_item_id = 'Q486449';`

Then the public BFF: `/api/travel/hotspots/rankings?destination_id=<seoul destination id>`
must list it (the param is `destination_id` or `city_code` — `destination` is ignored, and
attractions have no standalone detail page, so a `/hotspots/<slug>` URL returns 404).

## Notes

Cross-run exclusion lists must be carried forward: this row had been deliberately excluded
from the 2026-09-12 morning sweep of run `d943205e`, but the afternoon sweep of run
`0a194879` only carried 新福宮 in its skip list, so this one went through.

新福宮 (Q10306724, a Taipei temple filed under Taichung) is the same shape of problem and is
still `pending` — keep it out of blanket rejections for the same reason.
