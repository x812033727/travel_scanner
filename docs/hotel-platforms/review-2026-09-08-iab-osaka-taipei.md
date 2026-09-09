# IAB Osaka / Taipei hotel review — 2026-09-08

## Delivered

PR [#364](https://github.com/x812033727/travel_scanner/pull/364) was SHA-guarded
squash-merged at head `3e08f993c26658410ea67c93b562c327c55d8674`, base
`434345419dc4a4117830f611197707fa11ed9b04`, after CLEAN/MERGEABLE and all eight checks.
The merged revision is `200e46ea922bdb0403f146b5db7ea4382af62c9a`; its
[main CI 34199564301](https://github.com/x812033727/travel_scanner/actions/runs/34199564301)
passed API, web, containers and full-stack smoke before deployment.

A clean Git archive was deployed to all eight application services. The API remains
at schema `0063_destination_offers`; this content batch adds no migration or UI code.
Existing PostgreSQL/Redis container IDs and volumes, runtime environment contents/mode,
community-off state, hotel settings, prior images and backups were preserved.
Application restarts were zero and three consecutive readiness checks passed.
Transient startup connection resets preceded the successful readiness checks.

Production had concurrently advanced from bdd01b6 to 4343454 while CI ran. The deploy
precondition and application rollback baseline were refreshed to the actually running
4343454 source. No newer application revision was silently replaced by an old baseline.

After deployment and independent verification of the previous Taipei checkpoint:

| Change | Result |
| --- | --- |
| Existing Osaka hotels newly location-approved | 3 |
| Existing platform links newly approved | 12 |
| New Expedia / Rakuten platform candidates | 6, all pending |
| Distinct hotels | 60, unchanged |
| Product status | 30 approved / 30 pending |
| Platform status | 100 approved / 260 pending |
| New audit records | 27 |
| Fully accepted cities | 0 |

Five-language public reads now show Tokyo 10 hotels / 20 options, Osaka **5 / 16**,
Kyoto 0, Seoul 5 / 7, Busan 0, and Taipei **10 / 30**. These are ordinary hotel links,
not affiliate activations, real-time prices, bookings or commissions.
There were no new duplicate hotel identities or city switch changes.

## Actual browser evidence

The user permitted the built-in browser or Gemini. The built-in browser worked;
**no Gemini or other paid provider API calls ran**. Each approved platform was
actually opened and its hotel name and complete street address inspected.
Search documents alone were not treated as browser evidence.

New Osaka map approvals:

- Hotel Intergate Osaka Umeda: official Umeda **2-5-2**.
  [Official facility page](https://www.intergatehotels.jp/osaka-umeda/facility/).
  The different 2-4-9 address on that page belongs to nearby parking, not the hotel.
- Hotel New Otani Osaka: official Shiromi **1-4-1**.
  [Official access page](https://www.newotani.co.jp/osaka/access/).
- Hotel Gracery Osaka Namba: official Motomachi **1-4-4**.
  [Official access page](https://gracery.com/namba/access/).

The saved Place IDs were opened in the browser and name/street/official-site identity
matched. Only IDs and review outcomes are retained from Google Maps. Existing Osaka
municipal CC BY 4.0 coordinates, source credits and documented coordinate-column
correction were not replaced with provider coordinates.

Each of those three Osaka hotels gained Booking and Agoda approvals, joining its
previously approved official and Trip links. In Taipei, WESTGATE, Solaria Nishitetsu
Ximen, W Taipei, Grand Hyatt Taipei and Humble House each gained Booking approval;
W Taipei also gained official-site approval.

Solaria's initial Chinese Booking page displayed only the district. The actual
language menu was used to choose English, and the hydrated page showed **No. 88,
Sec. 1, Zhonghua Rd.** The saved `solaria-nisitetsu-taipei-ximen` URL spelling was
preserved. W's official page initially loaded blank but later displayed its hotel
name and complete Zhongxiao East Road Section 5 **10** footer address.

Nine approved links truthfully retain server health **unconfirmed** (eight Booking,
W official); all have actual browser verification. The three Agoda links are healthy.
Normal DNS/HTTPS/redirect checks still ran; **unsafe or unavailable links cannot be
overridden**. Browser checks do not rewrite server health to healthy.

Grand Hyatt's saved official landing page remained blank after a fresh accessibility
observation and screenshot. It was not marked browser-verified, re-reviewed or disabled;
it remains pending/version 1. Booking approval does not substitute for official-link
verification. This is not a finding that the hotel has closed.

## New discoveries remain separate from approval

Six independently observed Expedia / Rakuten international URLs were added to existing
slots for the three Osaka hotels. Exact URLs, IDs, queries and freshness/identity limits
are in `iab-osaka-taipei.review-2026-09-08.json`.

Expedia's Intergate and Gracery documents showed full streets; New Otani's street
evidence came from its indexed document after a follow-up extraction error.
Rakuten documents identified name/city but did not establish full street addresses.
All six remain pending/version 2/unchecked, with no browser or server approval claimed.
No Japanese/international Rakuten ID conversion or guessed language URL was used.

Pending input files keep `map_verified=false` and contain no review status fields.
They are research/import packages, **not live synchronization truth**: never replay
them over independently reviewed production records. Historical checkpoints remain
immutable and describe their own earlier states.

## Backups and independent checks

Deployment archive SHA-256:
`2324833ac195ccd656e3e23f651cf900a7817ff5ee2543fbe413edacc884f7c4`.

Release source: `/root/mokaair-release-200e46e-W8swZzMT/source`.
Verified pre-deploy PostgreSQL archive:
`/root/travel_scanner_pre_deploy_200e46e_20260908T073833Z.dump` (10,221,944 bytes).
Separate verified pre-content archive:
`/root/travel_scanner_pre_iab_hotel_review_20260908T073933Z.dump` (10,225,071 bytes).

The default operator invocation was read-only. Apply required exact original row
data/status/version, authorized existing admin, a whole-catalog fingerprint and
per-row locks. Baseline:
`b5748df4994e24b2373b13c070c346aca769c588e2dbcb72b47d98fe8d151a73`.

Normal versioned admin services performed six candidate edits, three map-only product
edits, three location audit records, three product approvals and twelve option approvals.
No direct approval SQL or credential export was used.

An independent verifier enforced a PostgreSQL REPEATABLE READ, READ ONLY transaction.
It checked each changed record, metadata, version, source fact, review audit and public
option. The other **57 products, 342 options and config version 5** retain fingerprint:
`34b11bfb52a49a91109814c8dbb084f8da404e4e261414a12b4d3da362093cb6`.
It distinguished 27 new audits from three previous Agoda candidate-edit audits.

Thirty internal locale/city reads and ten real HTTPS Osaka/Taipei BFF reads passed.
Five public homepage reads also returned HTTP 200 after deployment. The IAB live
Osaka page showed `查看全部（5）`; Intergate's panel showed official / Booking / Trip /
Agoda, the no-live-price notice and ordinary-link disclosure. Escape closed the panel
and returned keyboard focus to its original opener. No clickouts or test orders ran.

## Validation and continuation

Local related API/content/offline-source tests: **194 passed, one integration skipped**.
Ruff/check-format, mypy (258 source files), five locales / 25 namespaces, 27 tooling
tests and task checks passed. No application dependency was added; the optional Seoul
projection checks used research-only pyproj==3.7.2. Full CI
on the new evidence PR supplies PostgreSQL/migration, web lint/typecheck/build,
responsive Playwright and unmocked full-stack validation; record its exact head there.
No claim is made that new UI code or paid price integration was implemented.

The original dirty workspace is untouched. Continue from the isolated worktree, release
the shared unfinished task at handoff, and keep the next evidence PR separate from the
already merged/deployed #364. The admin data above is live; the evidence/test PR does
not need another production deployment for those already committed records.

Remaining: more independent platform/map/source checks in the other cities, the blank
Taipei Hyatt official link, and full per-city acceptance. Preserve existing Kyoto Hyatt
future-closure and Westin holds. Do not manufacture content, quotes or completion counts.
