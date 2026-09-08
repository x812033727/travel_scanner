# 2026-09-08 — Kyoto platform continuation and closure hold

## Merge and boundary

The user authorized merging #352 then continuing hotel additions/review. Main had advanced
to `aaa33f0` (#349 food reservation links), so the branch was synchronized and all eight
PR/push checks rerun at `5f1e661e861221851f61207e209313acc4644465`
(runs 34183706585 / 34183705002). SHA-guarded squash merge produced
`f65890ad76c7d6f3c47076e813e5e6cbebcec1e3` at 03:38:03 UTC.

Continued in isolated `codex/hotel-content-review-kyoto-links` from that merged main.
The original dirty worktree was not modified. This is a data/review batch, not a
runtime implementation, deployment, migration, provider enablement or completed city.

## Current checkpoint

Still **60 hotel identities: 17 product-approved / 43 pending**.
Platform options: **360 total, 48 approved / 312 pending**.

This batch adds **five Rakuten candidate URLs** to existing independent slots and
**seven platform approvals** after eight normal review attempts. Two existing Hyatt
official/Trip notes also gain a dated future-closure warning, staying pending.
There are no new hotel identities, map approvals, invented coordinates or city switches.

| Hotel | Official option | Trip option | Rakuten |
| --- | --- | --- | --- |
| The Royal Park Hotel Kyoto Sanjo | Approved | Approved | New candidate, pending |
| Mitsui Garden Hotel Kyoto Shijo | Approved | Approved | New candidate, pending |
| Hyatt Regency Kyoto | Pending, closure hold | Pending, closure hold | New candidate, pending |
| Hotel The Celestine Kyoto Gion | Approved | Approved | New candidate, pending |
| The Westin Miyako Kyoto | Pending, link verification failed | Approved | New candidate, pending |

All five products remain pending. Kyoto's licensed permit source supplies addresses,
not coordinates; exact map identity and reusable coordinates still need independent
review. Public five-language reads remain **Tokyo 10 / Osaka 2 / Kyoto 0**.
Zero cities meet the full official-plus-two-OTAs acceptance goal.

## Important factual review finding

[ORIX Real Estate's April 9, 2026 announcement](https://orix-realestate.co.jp/news/pdf/press_20260409.pdf)
states that Hyatt Regency Kyoto at Sanjusangendo-mawari 644-2 will end operations on
**May 9, 2027**. This is a future closing date, not a claim that it is already closed.

The catalog currently has no operating-date restriction. Keep this product and every
booking option pending until a reviewed date-aware guard or an agreed replacement hotel
resolves the issue. Do not approve it merely because a platform page or HTTP check works.
The official/Trip review notes and new Rakuten candidate carry the notice and source URL.
The permit evidence also retains the unresolved operating-date blocker. No existing
hotel/trip IDs or saved user itineraries were deleted or replaced.

## Source and platform review

Minimal name/street facts were cross-checked against official sources, with separate
platform ID and URL evidence in `kyoto-five.review-2026-09-08.json`. Rakuten international
IDs are copied only from observed URLs; the readable listings did not establish full
street/current landing identity, so none were approved. Historical indexed listings
(months old) are not claimed as newly refreshed inventory. No room prices, reviews,
ratings, descriptions, photographs or provider coordinates were copied.

Mitsui Kyoto Shijo (707-1 Myodenji-cho) is not Shinmachi Bettei. Rakuten ID
10123456795625 is excluded; Shijo's observed ID is 10123456863505.
Westin's full street identity is supplemented by the
[official Miyako contact page](https://www.miyakohotels.ne.jp/westinkyoto/contact/),
not inferred from a restaurant identity. The existing Marriott URL was preserved.
It failed normal server link verification, returning `service_link_unavailable`;
the transaction rolled back, leaving pending/version 1/unchecked. This is not evidence
that the hotel is closed. No browser override or alternate URL substitution was used.

Celestine's bare Trip URL could not be extracted, but its observed same-ID locale page
shows the correct Komatsucho 572 identity. It also contains conflicting postal codes.
The official 605-0933 is authoritative; no provider postal-code data was imported and
the stored URL was not rewritten. Its normal server link verification passed.

## Browser limit

Chrome creation for the saved Intergate Place ID returned `Debugger unattached`.
Fresh inventory succeeded, but reconnecting the actual returned tab timed out and
reset the JavaScript kernel. The computer-use recovery rule stopped further attempts.
**No new browser/map verification succeeded this turn.** Do not claim that seeing a
tab title established name/address/official-site identity.

## Guarded production work

The first backup guard stopped before writing because another work independently
deployed production from b3e49a3 to `aaa33f008c82c56e5c541dede8205097102193e1`.
Read-only readiness and the full prior hotel fingerprint still passed. Relevant
travel-service and authentication service files are unchanged between these runtimes.
No deployment, downgrade, restoration or settings reset was performed here.

A new exact-runtime-guarded backup succeeded:
`/root/travel_scanner_pre_hotel_candidates_20260908T034012Z.dump`,
7,084,300 bytes; pg_restore could read its custom-format directory.
Runtime readiness: `0062_merchant_platform_links`, database/Redis OK.

Preflight fingerprint:
`f7e0afecc0d6308adde4b8e198a13768528145ed7963959cb57a4f58d440ccdd`.
Normal versioned administrator edit/review functions used existing IDs and row guards.
All 60 product records, the other 345 option records, and config version 5 were
fingerprint-preserved:
`f8fadc76e81e6ff165aa6b8753eb72cf28a594db84ce454bb63b531049bda9fe`.
An independent read-only check confirmed 14 audit entries: seven edits and seven
approvals. The failed Westin review produced no approval or audit mutation.

No paid provider API calls, price queries, generated clickouts, test orders, affiliate
qualification changes, catalog enablement, application deployment or migration.
Do not replay pending import packages over already reviewed production records.

## Next review work

Finish the remaining Kyoto official/Trip pairs, investigate Westin link health without
bypassing safety, and verify independent Rakuten/Booking/Agoda/Expedia landing identities.
Continue exact maps and licensed coordinates when tools/sources are available. Resolve
Hyatt's dated closure hold before any public recommendation or choose a replacement
through the normal reviewed-identity workflow. The shared content task remains open.

## Validation

136 related content/API/platform/offline-source tests, Ruff/format, mypy (257 sources),
five locales/25 namespaces and 27 tool tests passed. Independent database/audit verification
and actual public HTTPS BFF reads passed for all five locales: Tokyo 10 / Osaka 2 / Kyoto 0,
only already approved official + Trip options visible. No clickouts were generated.
Full new-head API/web/container/Playwright/PostgreSQL/Redis smoke is tracked on the PR.
Post-merge main smoke is checked separately; unrelated failures are not silently repaired
or suppressed by this content-only batch.
