# 2026-09-08 — Seoul independent booking-option review

## Result and scope

PR #355 was SHA-guarded at `a8a750cebef66e415a748d00f1fe8e4cfe25eb8e` after all
eight checks and CLEAN/MERGEABLE verification. It merged to
`9ca88c22435759d4d6edbd6b34e7a0186318280d` at 05:06:35 UTC. Post-merge main run
34189379559 passed all four jobs. Continued from that main in isolated branch
`codex/hotel-content-review-seoul-links`; original dirty checkout untouched.

Still **60 hotel identities: 17 approved products / 43 pending**. This is completion
of existing hotels' platform coverage, not an increase in distinct hotel identities.
Platform options are now **64 approved / 296 pending** out of 360.

| Existing Seoul hotel | New approvals | Other result |
| --- | --- | --- |
| L7 Myeongdong | Trip | Lotte bot page remains pending |
| Four Points Josun Myeongdong | Trip | Official and Expedia review did not pass |
| RYSE, Autograph Collection | Trip | New Rakuten candidate pending; prior official approval preserved |
| Mercure Ambassador Hongdae | Official, Trip | New Rakuten candidate pending |
| L7 Hongdae | Trip | Expedia review did not pass; Lotte bot page remains pending |

Nine review attempts yielded six approvals and three `service_link_unavailable`
outcomes. Failed reviews rolled back and remain version 1/pending/unchecked; the code
does not establish delisting or distinguish the underlying HTTP/DNS/redirect cause.
No manual browser override, URL safety bypass, guessed ID or alternate destination.

Five-locale public Seoul results remain five hotels, but usable platform options
increase **from one to seven**. All seven are ordinary official/Trip links with
`quote_status=not_configured`. No city yet meets ten hotels with official plus two
approved OTAs; this is not a completed city release.

## Evidence boundaries

Primary document URLs, minimal names/addresses and exact observed option IDs are in
`seoul-links.review-2026-09-08.json`. No prices, review text, photos, ratings, inventory
or provider coordinates were copied. Existing licensed Seoul permit coordinates and
prior dated Naver reviews are unchanged; no new map/browser observation this turn.

- Trip street numbers match the official/permit identities: L7 Myeongdong 137
  Toegye-ro; Four Points 36 Samil-daero 10-gil; RYSE 130 Yanghwa-ro; Mercure 144
  Yanghwa-ro; L7 Hongdae 141 Yanghwa-ro. Hongdae's 130/141/144 are different hotels.
- Current Marriott, RYSE and Accor documents corroborate their identities. The saved
  Lotte pages return `Pardon Our Interruption`; Korea Tourism Organization's current
  L7 entries corroborate addresses, but do not turn those bot pages into approved links.
- Five saved Booking pages expose no readable identity in this check. They remain
  pending; absence of readable content is not absence of the hotel.
- Expedia Four Points and L7 Hongdae documents show matching street addresses, but
  normal server review fails. The other three Expedia titles were observed; subsequent
  full-address extraction returned Internal Error, so they were not freshly reviewed.
- RYSE Rakuten international ID `34123457159873` comes from an observed property
  document indexed last year. Mercure ID `34123457217428` comes from a seven-month-old
  primary search result; direct opening failed. Both remain pending for complete
  current landing/address identity. Preserve Mercure's observed `/hkg/zh-hk/` path;
  no invented `/usa/en-us/` equivalent or Japanese/global ID conversion.

`seoul.pending.json` remains a research/import input. Never replay it over reviewed
production products or options. It intentionally carries no approval and leaves
`map_verified=false`. The dated checkpoint records the separate real admin outcomes.

## Guarded production writes and independent verification

The previous Kyoto station verifier passed before writes. Runtime is still
`travel-scanner-api:aaa33f008c82c56e5c541dede8205097102193e1`, schema
`0062_merchant_platform_links`. Database and Redis were ready. No deployment/migration.

Before writes, the exact-runtime-guarded PostgreSQL custom archive was created and
its directory validated by pg_restore:
`/root/travel_scanner_pre_hotel_candidates_20260908T051250Z.dump` (7,095,043 bytes).

Preflight whole-catalog fingerprint:
`6a70a44e0190a0591021100f6046c2d336ae6346ca3d4a94868f73b5e8207c90`.

The existing authorized administrator's normal versioned edit/review functions
performed two candidate edits and six successful approvals: **eight audit records**.
Three rejected reviews made no audited state change. All use `browser_verified=false`.
Per-row locks and before-state checks guard the one-time execution.

An independent read-only script verifies outcome/version/health, exact original URLs,
candidate payloads, audit metadata, public options and the unchanged fingerprint of
all 60 products, the other 349 options and config version 5:
`8da6cf45fe63270b3bc46855503fb5c7faf84f5eda085e1ac355f3e1eba836e7`.

Internal five-locale reads across all six cities and five actual HTTPS BFF Seoul
reads passed: Tokyo 10 / Osaka 2 / Kyoto 0 / Seoul 5 / Busan 0 / Taipei 0. Pending
Rakuten/Expedia/Booking options do not appear. No clickouts, affiliate enablement,
quote calls, test orders, paid API requests or configuration changes were made.

## Validation and remaining work

Content/schema/API/offline-coordinate tests cover exact Korean identity, separate
option approvals, two candidate-only international URLs, failed/unreadable pages,
UTF-8 import counts and no implicit approval. Full CI is tracked on the continuation PR.
Release the shared task at handoff; city acceptance remains unfinished.

Next: browser-assisted review of blocked landing pages when available, remaining exact
map identities, a second approved OTA per hotel, and source-complete per-city acceptance.
Do not relax checks or copy unlicensed data simply to fill the remaining counts.
