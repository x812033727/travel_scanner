---
id: 2026-09-08-prevent-google-coordinates-being-labelled-durable
title: Prevent Google coordinates being labelled durable by merchant review
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T04:22:10Z
created_at: 2026-09-08T08:53:20Z
completed_at: 2026-09-19T04:46:51Z
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/foods/coordinate_queue.py
  - apps/api/tests/test_food_coordinate_queue.py
---

# Prevent Google coordinates being labelled durable by merchant review

## Why

Production coordinate_queue.apply_approval copies Google match.latitude/longitude to
catalog rows, labels them admin_verified and uses a Google Maps URL as permanent
provenance. This contradicts coordinate_fill's explicit rule excluding embedded
Google data and allows incomplete candidates to pass durable-coordinate gates.

## Definition of done

- [x] Accepting a Google identity candidate never turns provider coordinates into durable catalog data.
- [x] Preserve separately verified permanent coordinates and require independent provenance for publication.
- [x] Add regression tests for missing coordinates, preserved genuine coordinates and Korean exact-map behavior.
- [x] Define a separately authorized review of affected historical data; no blanket relabel or deletion.

## Steps

- [x] Confirm current main and normal map approval flows before selecting the smallest fix.
- [x] Fix and test queue approval without bypassing existing publication guards.

## How to verify

Run apps/api/tests/test_food_coordinate_queue.py and affected integration tests,
Ruff and mypy; verify new Google candidates remain non-public until independent
durable coordinate evidence exists.

## Notes

Confirmed in the running API container 2026-09-08 08:54 UTC: coordinate_queue.py
around lines 298-305 assigns Google match coordinates, admin_verified, Google URL
and fresh verification timestamp. No app code was changed by the editorial task.
Only its own prior four approvals were withdrawn with full audits; five pending
source repairs also cleared unsupported stamps. See
docs/catalog-review-followup-2026-09-08.md for exact operational scope.
Other administrators' previously published rows were not silently changed.

### 2026-09-19 補註

claude-opus-5 應站主「整理目前所有工作狀態」處理，盤點見 `docs/work-status-2026-09-19.md`。

在 main `161687ad` 重新確認問題仍在：`apps/api/app/foods/coordinate_queue.py` 的 `apply_approval`（第 298–303 行）把 Google 候選的 `latitude`／`longitude` 寫進店家、標成 `admin_verified`，來源寫 Google Maps 網址。每核准一筆就多一筆。

### 2026-09-19 done in code (claude-fable-5-1)

- `coordinate_queue.apply_approval` now writes the Google identity only: `google_place_id`,
  and `map_match_status`/`verified_at`/`verified_by_user_id` where the country's exact-map
  rule allows it. It no longer touches `latitude`, `longitude`, `coordinate_source_type`,
  `coordinate_source_url` or `coordinate_verified_at`, so a Google pair can never become
  `admin_verified`, and a Wikidata pair (with or without its URL) is left exactly as found.
  The `already_durable` short-circuit is gone with it (a durable row may still want its
  identity recorded), and the KR outcome is `identity_saved` instead of `coordinates_saved`.
- `coordinate_queue_statement` also requires `google_place_id IS NULL`: since approval no
  longer changes a row's coordinates, a merchant with a recorded identity would otherwise
  return to the queue after every approval. Durable coordinates now come only from
  `coordinate_fill` (Wikidata, official tourism, merchant pages) or an admin entering them
  with a citable https source; `merchant_is_publishable` is unchanged and keeps demanding
  them.
- Outside the ticket's two files, the rename touched what shows the outcome: the approve
  endpoint's success list and audit action (`food_merchant_google_identity_approved`), the
  admin panel's outcome list, and `merchantCoordinateQueue` copy in the five locales
  (description, Korea note, empty state, written counts, outcome labels). `check:i18n` green.
- Tests: missing coordinates, an existing untrusted pair preserved, Google's Maps URL never
  written, KR identity_saved, a Wikidata pair preserved, a Wikidata pair without URL not
  "repaired" with a Google link, and the queue filter on `google_place_id`.
- Historical data -- to be authorised separately, never in bulk: rows written by the old
  path are `coordinate_source_type = 'admin_verified'` with a `coordinate_source_url`
  starting `https://www.google.com/maps/place/?q=place_id:` or `https://maps.google.com/`
  (the two shapes the old code wrote). Proposed review: list them
  (`SELECT id, slug, destination_id, coordinate_source_url, coordinate_verified_at FROM
  food_merchants WHERE coordinate_source_type = 'admin_verified' AND (coordinate_source_url
  LIKE 'https://www.google.com/maps/place/%' OR coordinate_source_url LIKE
  'https://maps.google.com/%')`), then per row either replace the pair with one from
  `coordinate_fill`'s sources or, where none exists, relabel it `google_places` with a
  written note so the merchant leaves publication until a citable source is found. The
  2026-09-08 follow-up already withdrew the four approvals of that day's editor; the rest
  belong to other administrators and are not to be changed silently.
