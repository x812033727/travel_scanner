---
id: 2026-09-19-re-approve-tran-binh-dai
title: Re-approve 鎮平台 (Q8669747), tombstoned by the 2026-09-12 denylist
status: done
priority: P2
area: ops
owner: claude-opus-5
claimed_at: 2026-09-19T07:00:05Z
created_at: 2026-09-19T06:11:55Z
completed_at: 2026-09-19T07:01:09Z
branch: claude/tran-binh-dai-restore
depends_on: []
scope:
  - docs/catalog-content-reviews/2026-09-19-tran-binh-dai.md
---

# Re-approve 鎮平台 (Q8669747), tombstoned by the 2026-09-12 denylist

## Why

PR #403 (2026-09-11) put Q245016 (military base) into `DENIED_TYPES`. 鎮平台 (Trấn Bình đài,
Q8669747), the bastion inside the Huế citadel and part of a UNESCO site, carries that type, and
`classify_types` rejected it on 2026-09-12 17:01:31 UTC with `review_reason='denylisted_type'`.

`2026-09-12-denylist-tombstones-real-attractions` (PR #556, deployed 2026-09-19 05:57 UTC) released
the type again, so future rows of this kind reach the human queue. It does not touch rows that were
already rejected: `review_status='rejected'` is a tombstone that `discover_city` skips forever, so
the weekly pass will never bring this one back.

Read on production after that deploy (2026-09-19): of the four genuine sights that task named,
原花園尋常小學校本館 (Q10911386), 島醫院 (Q2410409) and 喜屋武城 (Q38278536) are `approved`
(human-reviewed on 2026-09-12). Only 鎮平台 is `rejected` (city `HUI`).

## Definition of done

- [x] 鎮平台 is `approved` under Huế with a verified map identity, durable coordinates and their
      source, and a review reason that records why it was restored.
- [ ] It appears in the public listing for the Huế destination.
- [x] The evidence and the action are written in `docs/catalog-content-reviews/2026-09-19-tran-binh-dai.md`.

## Steps

- [x] Find the Place ID the way `docs/hotspot-review-next-batch.md` describes ("Filling the
      map-identity gate" and the fourth batch): the site's Places Autocomplete first (Essentials
      tier, free), then `POST /admin/hotspots/map-candidates` as the second opinion, and compare the
      two IDs. Make sure the hit is the bastion, not the citadel as a whole; a local-language query
      such as `Trấn Bình Đài Huế` is the likeliest to land.
- [x] Approve it in the admin hotspot review (`POST /api/v1/admin/hotspots/review`, action `approve`,
      with the map fields and a reason). The endpoint has no "back to pending", and approval needs
      `map_match_status='verified'` or it fails with `map_verification_required`. Writing the Place ID
      and approving make no Google call.
- [x] Write the record.

## How to verify

Read-only, on the host in `/root/travel_scanner`:

```bash
docker compose -f docker-compose.prod.yml exec -T postgres psql -U travel -d travel_scanner -Atc "select wikidata_item_id, review_status, map_match_status, reviewed_at from travel_hotspots where wikidata_item_id = 'Q8669747'"
```

Public, once the next ranking refresh has run (the `hotspot-collector` rebuilds the day's
`HotspotRanking` snapshot every 6 hours; a Huế query needs `destination_id`, not `city_code`):

```bash
for page in '' '&after_rank=50'; do curl -s "https://mokaair.com/api/travel/hotspots/rankings?destination_id=hue&limit=50$page"; echo; done | grep -c 'Q8669747\|鎮平台\|Trấn Bình'
```

## Notes

- This changes production data; do it only with the owner's go-ahead.
- Same shape as `2026-09-12-re-add-the-seoul-national-folk`, a tombstoned Seoul museum.
- 2026-09-19 done (claude-opus-5, owner in the loop): approved at 06:57:40 UTC with Place ID
  `ChIJL5ESYAChQTERnr3JBGAuilk` (Autocomplete "Đồn Mang Cá", about 520 m from the row's point;
  `map-candidates` returned the whole Huế Citadel and was not used), coordinates kept and their
  source relabelled `admin_verified` → the Vietnamese Wikipedia article, because Wikidata has no
  P625 for this item. Full record: `docs/catalog-content-reviews/2026-09-19-tran-binh-dai.md`.
- Still open by design: the public listing item. The day's ranking snapshot was built before the
  approval, so `/api/travel/hotspots/rankings?destination_id=hue` still showed 53 rows without it;
  it appears after the next 6-hourly refresh.
