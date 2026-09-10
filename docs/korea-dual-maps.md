# Korean dual-map identities and navigation

Map display, structured route/time data, and external navigation are independent.

| Mode | Onsite map | Applicable time | External navigation |
| --- | --- | --- | --- |
| Transit | Google Maps | ODsay | Google default; NAVER also available |
| Walk | NAVER default; Google selectable | External/manual only | NAVER default; Google also available |
| Drive | NAVER Maps | NAVER Directions | NAVER Maps |

This change does not add a walking-time provider. An endpoint-only map is a
position reference, not a calculated route. External navigation does not make
its duration available to the trip. Google-derived geometry is never displayed
on NAVER, and NAVER driving geometry is not displayed on Google. ODsay stays
labelled as the time-data provider regardless of the Google basemap.

## Identity storage and review

One attraction, restaurant or hotel remains one canonical record. Existing
Google Place ID/NAVER URL fields remain authoritative. Shared `MapIdentity`
metadata stores independent provider ID/status/verification time; internal
reviewer/evidence fields are omitted from public projections. Attractions and
hotels reuse JSON; migration `0070_map_identity_metadata` adds an empty-default
JSON metadata column to restaurants. NAVER Local hashes are temporary lookup
keys, never exact NAVER place IDs.

The existing Korean NAVER publication gate is unchanged. Missing supplemental
Google data does not unpublish an approved place. Finding or confirming Google
candidates never changes names, main coordinates, NAVER review or publication.

The collapsed review panel is available in the attraction, restaurant and hotel
admin workspaces. Filter Korean city/type/missing review state, select at most
50 canonical records, then collect candidates. The existing `hotspot-places`
RQ queue, rate limits and Google usage guard are reused. Candidates remain
pending until the editor compares Korean name, exact branch and full address.
Distance is only supporting evidence, not an automatic approval rule.

Comparison-only Google names/addresses/coordinates expire from Redis after
15 minutes. Durable metadata/audit contains IDs and the site's own review
decisions, not a raw provider response. Batch progress expires after 7 days.
Confirmation checks row revision, canonical fingerprint and actor-bound
snapshot; duplicate IDs and stale/concurrent review requests are rejected.

## Trip and navigation APIs

- `GET /places/autocomplete?provider=google_places|naver_local`: optional explicit
  provider. Omission preserves NAVER-first Korean search.
- `POST /trips/{id}/items/{item_id}/map-identities`: current version,
  `provider=google_places`, exact `place_id`, `confirmed_same_place=true`, and
  `Idempotency-Key`. Verifies the candidate and only supplements this personal
  trip's identity; it does not approve the shared catalog. Main coordinates,
  title, sequence, times and manual/applied route segments are preserved.
- `GET /trips/{id}/routes/navigation`: adjacent `from_item_id`, `to_item_id`,
  `travel_mode`; builds safe server navigation URLs without provider queries,
  credits, routing jobs or version updates.
- Route previews and persisted trip route projections expose
  `external_navigations[]` and `map_capabilities`; singular legacy navigation
  remains compatible. `RouteSegment.provider` always identifies actual data.
- Google waypoints use only independently confirmed Google IDs; otherwise
  bounded canonical coordinates. NAVER temporary IDs are never sent to Google.

Open an existing Korean stop's editor to supplement its Google identity.
Save other edits first, select the same Google place, compare the branch and
address, then explicitly confirm. In-flight identity writes protect the parent
editor from unsaved-edit loss. Ordinary place replacement still invalidates
adjacent routes; map selection alone never does.

## Verification and rollout

### Local Chrome acceptance (2026-09-10)

- Installed Google Chrome `152.0.7977.83`, launched with Playwright's `chrome`
  channel in an isolated, extension-free headless profile: **2/2 scenarios passed**.
- Busan `412x915` and Seoul `1464x807`: real login form and Next BFF on loopback,
  backed by `tools/korea-map-preview.mjs`; no intercepted API/SDK responses.
  Browser map keys were disabled. Both scenarios made zero external requests
  and raised zero page errors.
- Each scenario completed transit preview, walking NAVER/Google selection,
  driving preview/apply, and reload. Exactly two preview POSTs and one apply
  POST occurred; selection itself made neither. Trip version moved `1 -> 2`
  only on apply and survived reload. All three map frames measured `240px`
  high, with no horizontal overflow at either viewport.
- Focused `trip-editor.test.tsx` and `route-map.test.tsx`: **82/82 passed**
  (67 editor + 15 map). Scoped ESLint passed. Regressions cover ordinary edits
  preserving identity and all actual replacement paths clearing old identity,
  including replacement catalog results that do or do not carry new identities.
- Root's CUA session timed out in its existing Chrome profile; that freeze was
  not reproduced in clean installed Chrome. These are synthetic-data browser
  checks, not live-provider coverage or production acceptance.

The installed-Chrome 2/2 result and root's visual inspection remain valid,
but its six screenshots were not retained: a later Playwright run cleared
`apps/web/test-results/`. An attempt to regenerate them against the production
build stopped when the execution policy rejected local Next startup. No
alternate startup was attempted, and the newly started fixture API was stopped.

Two screenshots from the later passing production-build Playwright suite are
preserved separately under
`C:/Users/x8120/.codex/visualizations/2026/09/10/korea-dual-maps/`:
`playwright-fixture-seoul-390.png` and `playwright-fixture-busan-1280.png`.
These use labelled API/SDK fixtures and are not substitutes for the deleted
installed-Chrome screenshots or evidence of live provider operation. They are
generated local artifacts, not committed production content.

### Release gates

General CI uses deterministic provider fixtures. The Korean UI acceptance uses
Seoul and Busan desktop/mobile data and asserts no extra route/write request
when switching basemaps, no horizontal overflow, and visible controls/disclaimer.
Unit/integration tests cover identity propagation, review/CAS, URL policy,
read-only navigation, manual-route preservation and idempotent supplement.

Local browser fixtures do not verify real ODsay/NAVER/Google credentials or
coverage. Before production enablement, manually validate a small licensed
Seoul and Busan route matrix. Do not bulk approve Google candidates. Apply the
compatible migration before the application update; no keys or production data
are changed by implementation/testing. Merge and deployment require explicit
authorization.

References: [NAVER driving API](https://api.ncloud-docs.com/docs/en/ai-naver-mapsdirections-driving),
[Google coverage](https://developers.google.com/maps/coverage),
[Places policy](https://developers.google.com/maps/documentation/places/web-service/policies),
[Routes display policy](https://developers.google.com/maps/documentation/routes/policies).
