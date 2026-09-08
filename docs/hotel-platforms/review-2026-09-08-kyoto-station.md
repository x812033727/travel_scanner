# 2026-09-08 — Kyoto station-area platform continuation

## Boundary and current result

PR #353 merged with the user's authorization after checking all eight CI jobs,
latest main, CLEAN/MERGEABLE and exact head `252a2d8bde8be0c6e3e62939378e23155a77be7a`.
SHA-guarded merge produced `6db0f51a127246beb82d30d3eef4a0624a649e50` at 04:05:33 UTC.
This isolated continuation starts there on `codex/hotel-content-review-kyoto-station`.
The original dirty checkout is untouched. No application deployment or migration here.

Still **60 hotel identities: 17 approved products / 43 pending**.
Of 360 independent platform options, **58 are approved / 302 pending**.
This batch adds **five Rakuten candidate URLs** to existing slots and **ten independent
official/Trip approvals**, all successful through normal server link verification.
No new hotel identity, product/location approval, city switch or quote/affiliate enablement.

| Existing hotel | Official | Trip | Rakuten |
| --- | --- | --- | --- |
| Hotel Granvia Kyoto | Approved | Approved | New candidate, pending |
| Hotel Vischio Kyoto by GRANVIA | Approved | Approved | New candidate, pending |
| Daiwa Roynet Hotel Kyoto Terrace Hachijo PREMIER | Approved | Approved | New candidate, pending |
| Miyako Hotel Kyoto Hachijo | Approved | Approved | New candidate, pending |
| Cross Hotel Kyoto | Approved | Approved | New candidate, pending |

Four hotels are in the Kyoto Station area; Cross is in Kawaramachi. All five products
stay pending: the licensed permit data has no coordinates, and exact map identities
still require review. Five-locale reads remain **Tokyo 10 / Osaka 2 / Kyoto 0**.
None of the six cities meets full official-plus-two-approved-OTAs acceptance yet.

## Identity evidence and exclusions

Official sources, minimal matched names/addresses and observed platform IDs are recorded
in `kyoto-station.review-2026-09-08.json`. Source facts, source credits and hotel/trip IDs
are unchanged. No prices, reviews, ratings, descriptions, photos or provider coordinates
were copied. Search index freshness is recorded honestly, not called live inventory.

- Granvia: official and Trip both identify JR Kyoto Station Central Entrance. The Kyoto
  licensed permit gives Higashi Shiokojicho 901; Trip does not print that street number.
  Do not claim the missing number was observed on Trip or synthesize a replacement address.
- Vischio: official and Trip agree on Higashikujo Kamitonoda-cho 44-1.
- Daiwa Terrace: official and Trip agree on Higashisanno-cho 14-1. The discovered
  [Booking Kyoto-Hachijoguchi page](https://www.booking.com/hotel/jp/daiwa-roynet-kyoto-hachijyoguchi.html)
  is a different branch at Kitakarasuma-cho 9-2, and is excluded. The existing
  `daiwa-roynet-kyoto-station.html` page yielded no readable identity; this is not proof
  it is wrong or delisted, so it is kept pending, not replaced by the wrong branch.
- Miyako: its current official website identifies the hotel; the
  [Kyoto official tourism directory](https://ja.kyoto.travel/tourism/single-hotel01.php?category_id=13&tourism_id=2265)
  corroborates Nishikujo Inmachi 17 and links back to that website. Trip agrees. Its saved
  URL has an `otokuni-district` path, but the actual property page identifies Kyoto and
  the matching street. Preserve the observed URL/ID; do not invent a canonical rewrite.
- Cross: official and Trip agree on Daikokucho 71-1.
- Rakuten: five distinct international property URLs/IDs were opened and their Kyoto
  property names observed. Full current street/landing identity is unresolved, so all
  five remain pending even where the index is recent. No Japanese/global ID conversion.
- Expedia's regional result contains a malformed Vischio hotel hyperlink with a space
  before `.h30990875`. Keep only that research lead; do not fabricate a corrected URL,
  import the regional page as a hotel link or treat its ID as independently verified.

The prior Hyatt Regency Kyoto future-closure hold and Westin official-link failure remain
unchanged. They were not re-reviewed or silently enabled in this batch.

## Browser recovery limit

Selecting the existing Intergate Chrome map tab failed with
`Timed out after 10000ms waiting for CDP command Emulation.setFocusEmulationEnabled.`
Fresh inventory succeeded; one reconnect failed with the same error. The computer-use
recovery rule stopped further browser operations. No new map observation, map coordinates,
Place ID lookup or browser-verified override is claimed. A tab title is not identity proof.

## Guarded production operations

Read-only verification first confirmed the previous batch's exact hotel/options/config
fingerprint and 14 audit records. Runtime remained
`travel-scanner-api:aaa33f008c82c56e5c541dede8205097102193e1`, schema
`0062_merchant_platform_links`, database/Redis ready. No runtime/settings reset performed.

Before writes, an exact-runtime-guarded PostgreSQL backup was created and its custom
archive directory verified with pg_restore:
`/root/travel_scanner_pre_hotel_candidates_20260908T041040Z.dump` (7,090,398 bytes).

Preflight fingerprint:
`adc6db5cc7270269a2b637a3a97029d9ca4222f8ff922b0b8bb1f180791b95c6`.
The existing authorized admin's normal edit/review functions used row/version guards.
Five option edits remain pending/version 2; ten reviews are approved/version 2/healthy.
All used `browser_verified=false`; no direct status override or safety bypass.

Independent read-only verification confirmed **15 audit records** (5 edits + 10 approvals)
and preserved all 60 product records, other 345 options and catalog config version 5:
`717290d01cd5cc81c66c11005e07c9ff5d7ec86da448bcb33ba75f59bf3b201c`.

No generated clickouts, test orders, provider API/price calls, API credentials, affiliate
qualification changes, new public-city switches, application deployment or migration.
Pending JSON files are research inputs, not live synchronization files: never replay them
over reviewed records. Content acceptance remains open; release the shared task at handoff.

## Validation and next work

139 related content/API/platform/offline-source tests, Ruff/format, mypy (257 sources),
five locales/25 namespaces and 27 tool tests passed. Independent database/audit/fingerprint
checks, internal reads and 15 actual HTTPS BFF reads passed for five locales across
Tokyo/Osaka/Kyoto. No clickouts generated. Post-merge main run 34185756687 passed all four
jobs on its first attempt at 6db0f51. The new head's complete CI is tracked in the PR.

Continue exact maps and reusable coordinates, independent Booking/Agoda/Expedia/Rakuten
identity/landing reviews, and dated Hyatt/Westin holds. City activation must still meet
the original acceptance criteria; five candidate URLs do not mean five public hotels.
