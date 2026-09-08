# Gemini compatibility for this hotel review

Read-only code inspection on 2026-09-09. No keys, live quota values, provider calls,
production writes or application changes were made for this inspection.

## Finding

There is no existing Gemini hotel-review API or CLI. Do not disguise a hotel or a
booking option as a merchant/hotspot or use `scope=all` expecting hotel coverage.

- `apps/api/app/catalog_review/schemas.py:9`, `scope.py:8` and
  `repository.py:45` allow only `hotspot`, `food` and `merchant`.
- `catalog_review/service.py:39` defines start requests. `review_pending` snapshots
  every pending entity in that supported scope (`:411`); discovery counts are not
  an exact-ID review subset selector.
- `catalog_review/jobs.py:263` evaluates batches of eight from existing fetched
  source URLs. `provider.py:606` accepts at most 20 assessments; this path does not
  run a new Google Search. Missing source evidence remains unresolved.
- Grounded discovery searches then structures at most five new drafts per one
  destination round (`jobs.py:465`, `provider.py:796`). It normally needs two calls,
  plus a possible repair. It automatically imports new **pending** entities and
  snapshot items (`jobs.py:480`), so it is not a no-write hotel research preview.
- No background model assessment automatically approves. Explicit apply is gated
  by allowed actions, publication gaps, full snapshot hash, version, pending state
  and seven-day assessment freshness (`service.py:130`, `:499`).

## Budget and unsafe shortcuts

The supported catalog worker reserves every HTTP call, including repairs, before
sending it (`catalog_review/jobs.py:153`, `provider.py:557`). It shares
`hotspot_guide_gemini_daily_search_budget`: environment default 30, allowed 1–1000
(`config.py:372`), not a statement of today's effective production allowance.
Each run is additionally capped at 1–80 calls; start/resume are limited to six per
administrator per hour and only one catalog run may be active.

The Redis counter is `hotspot-guide-quota:gemini:<billing-date>`; its day is
America/Los_Angeles, not Taiwan midnight (`hotspots/guides.py:651`,
`providers/usage_meter.py:173`). Redis reservation failure blocks a call. The
read-only `/api/v1/admin/hotspots/guides/coverage` reports `quotas.gemini`; however,
the display helper maps Redis read failures to zero, so an uncertain status must
not be interpreted as unused allowance (`guides.py:667`). No live quota was read.

Do not substitute `generate-hotspot-candidates --dry-run`: it still makes an
ungrounded paid call and its raw structured provider does not reserve this shared
catalog budget (`hotspots/candidate_generation.py:211`, `ai/gemini.py:40`). Do not
run hotel maintenance as a review shortcut: it targets already-approved options
and can update health or disable them (`travel_services/jobs.py:244`).

## Safe path for the current request

Continue built-in-browser research only for the pinned pending subset with actual
new evidence; keep the prior 295 approved rows untouched. New platform identities
are separately checked, then applied through ordinary versioned hotel routes.
Grounding cannot certify a Google/Naver identity, durable coordinates, source
licensing or publication readiness. Existing discovery explicitly prohibits
invented map IDs/coordinates and ignores Maps/Naver/booking content
(`catalog_review/provider.py:74`, `evidence.py:1`).

A future hotel-specific Gemini research adapter would need an explicitly bounded
scope, mandatory shared budget reservation, actor/usage audit, grounding-chunk URL
provenance and no import/approval writes. That adapter is not part of this batch;
the current task instead uses the permitted built-in browser.
