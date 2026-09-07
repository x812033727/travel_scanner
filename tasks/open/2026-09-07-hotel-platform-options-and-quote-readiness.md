---
id: 2026-09-07-hotel-platform-options-and-quote-readiness
title: Hotel platform options and quote readiness
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-07T12:32:44Z
completed_at:
branch: codex/hotel-content-review-kyoto
depends_on: []
scope:
  - apps/api/app/travel_services
  - apps/api/app/models.py
  - apps/api/migrations/versions
  - apps/api/tests
  - apps/web/components/travel-services
  - apps/web/messages
  - apps/web/e2e
  - apps/web/app/api/travel
  - docs/hotel-platforms
---

# Hotel platform options and quote readiness

## 2026-09-08 live content checkpoint

Continuation claimed on `codex/hotel-content-review-kyoto` from latest main
`7f21d7eb2af223a561bc04519ce67021198b1068`, preserving the original dirty workspace.
PR #342 had already merged and production later advanced to this main revision; observed
readiness is schema `0060_community_places`. This turn did not redeploy or migrate.

Added ten Kyoto pending research inputs and municipal CC BY 4.0 permit evidence, three
areas and 40 official/Booking/Trip/Agoda candidate links. Expedia/Rakuten remain unconfirmed.
The July 2026 permit spreadsheet has no coordinates; none were guessed, geocoded or copied
from providers, and no paid Places lookup ran. Kyoto still lacks coordinates/Place IDs.
Selected names/addresses/category/permit dates only are saved; do not re-download the whole
spreadsheet to recover these facts. Busan's ten hotels remain outstanding.

Chrome recovered long enough to verify primary Naver names, street numbers and official
sites for L7 Myeongdong, Four Points Josun Myeongdong, Mercure Hongdae and L7 Hongdae.
These are four new identity checks, plus RYSE's earlier one. Parnas navigation was interrupted;
debugger/fresh-tab recovery failed. Five Naver identities now have primary evidence, not ten.

With user authorization to add/review hotels, a verified database backup was taken and the
normal CSV/admin import service was run over the existing SSH session. The serializable,
exact-new-key guarded import skipped all six existing Tokyo products/options, added 44
pending hotels and 264 pending options, and recorded preview/commit audits. Run ID:
`31379d38-7180-4ceb-b2af-75ba5b6238ad`. Four newly browser-verified Seoul product locations
then passed version-checked admin edit/review; all their platform options remain pending.
No browser auth tokens were forged or exported, and no affiliate/API/public switches changed.

Verified live: 50 total hotels, 10 product-approved (six original Tokyo plus four Seoul
locations), 40 pending. Zero cities meet rollout acceptance. Original Tokyo/config/options
fingerprint stayed identical. See `docs/hotel-platforms/review-2026-09-08.md` for counts and
backup evidence. Pending JSON remains research input, not sync truth: never blindly replay
it over reviewed production rows or reset original hotels to pending.

117 related tests passed; Ruff, formatting, five-language catalogs (25 namespaces), and
task checks passed. Content/test/docs-only change; no new UI behavior or full-60 acceptance
claimed. Remaining: Busan, Kyoto durable locations, five remaining Seoul Naver checks,
independent platform landing checks/approvals, existing six Tokyo source-credit update,
and per-city rollout gates. Keep task open and release at handoff.

## Why

Keep one hotel identity while independently reviewing each platform, enabling commission links only after qualification, and preparing honest on-demand quotes without activating paid APIs.

## Definition of done

- [x] Ordinary and qualified affiliate links share one independently reviewed platform option; legacy clients remain compatible.
- [x] Migration preserves product/trip IDs and removes dual authority in facts.hotel_links.
- [x] No unlicensed live API, fake price, guessed platform identity, or automatic booking.
- [ ] Six cities each have ten verified hotels, three areas, official and two OTA links, checks for all five OTAs, and public source attribution.
- [x] API, migration, i18n, typecheck, lint, production build, five-language responsive E2E pass.
- [ ] City rollout only after factual review and actual link checks. No unverified affiliate enablement.

## Steps

- [x] Isolated worktree from verified main 54009ba; original dirty worktree preserved.
- [x] Independent options, compatibility import, safe clickout, quote contract and policy gates.
- [x] Five-language public/admin panels and source attribution.
- [x] Extended regression tests and full validation.
- [ ] Verified 60-hotel research/import package and city release gates.

## How to verify

Run uv pytest for travel services and hotel platforms; fresh Alembic migration on a disposable PostgreSQL database; web i18n/typecheck/lint/build/Vitest and travel-services Playwright on 320/390/1280px.

## Notes

Full web regression completed: 126 test files / 729 tests passed. All three pending city packages validate (four content tests), including the licensed Osaka coordinate-column correction. Taipei CSV preview has ten rows; i18n and Ruff rerun passed.

Branch CI 34131439819: web, containers and unmocked full-stack smoke passed. Full Linux API ran 1,721 tests; two new assertions incorrectly assumed empty shared audit tables. Fixed them to assert exact before/after deltas (ordinary adds zero affiliates, one affiliate plus one fallback adds exactly one). Related integration rerun: 19 passed. Added independent option recheck reminders and hotel affiliate/fallback counters, and preserved saved evidence in the admin editor; three admin component tests passed. A new full CI run is required for the fix.

Corrected branch CI 34132295317: Linux API 1,722 passed / one existing skip; containers and full-stack smoke passed. Final hardening refreshes/locks legacy omitted options before disabling, preventing a stale identity-map version from overwriting an independent review; three related integration tests passed. A final push reruns CI for that change. Chrome separately opened the saved Tokyo Station Hotel Place ID and confirmed name/address against the official identity; no Google price/rating/review/coordinate fields were copied. This is one spot check, not blanket approval of the 30 candidates.

Previous handoff: the architecture was isolated on codex/hotel-platforms, with content acceptance open. The user subsequently authorized merging that architecture milestone, not declaring a finished 60-hotel release; see the follow-up below. Do not re-request already saved Place IDs, copy OTA/Google content, or mark pending rows approved merely because schema tests pass. Finish source/platform/map reviews before staged admin import. No new paid APIs, affiliate activation, production migration, content writes or deployment were performed.

0057 migration succeeded on empty PostgreSQL. Related migration/API regression batch: 113 passed; row-lock hardening rerun: 40 passed. Ruff and full mypy (236 source files) passed. Five-language i18n, typecheck, lint and production build passed. Related Vitest: 32 passed; Playwright desktop 50 and mobile 53 passed. Actual Redis/RQ daily worker smoke passed on isolated PostgreSQL/Redis. Tools: 27 passed. Full Python collection on Windows hits the existing deployment agent UnixStreamServer import; Linux CI must verify the full suite.

Original content checkpoint: thirty pending research inputs (Tokyo, Osaka and Taipei each ten), preserving the original Tokyo six source keys. Twenty-four metered IDs-only lookups have already run; saved IDs must not be re-requested unnecessarily. Production settings, secrets and hotel rows are unchanged. Do not mark this task done or enable cities from the pending-input count.

## 2026-09-07 content follow-up

PR #341 merged the architecture milestone at f2c3b2af431d093bfb2169fefab7deb41cc90427 with explicit user authorization; post-merge CI 34135118181 passed all jobs. No deployment was requested/performed by that merge. The continuation uses codex/hotel-catalog-followup from that latest verified main in C:\Users\x8120\hotel-platforms; the original dirty worktree remains untouched.

Added ten Seoul pending inputs: four Myeongdong, three Hongdae, three Gangnam. Forty research inputs now exist, but **zero cities have completed rollout acceptance**. Each Seoul hotel has an official source plus cross-checked Booking, Trip, Agoda and Expedia property pages (50 discovered links including official). All five target OTAs were independently searched. Rakuten remains unconfirmed: Japanese-site leads are outside the current international-only host policy; L7 Gangnam's international listing needs street/address and live landing confirmation. Do not mix Rakuten Japan/global IDs or broaden affiliate rights to fill a content gap.

Resolved Seoul public licensed coordinates: OA-16044's Sheet CSV form works with serviceKind=1 despite the empty file tab. CP949, EPSG:5174 explicitly documented by Seoul, not older mirrors' EPSG:2097. Selected active permit IDs/raw X/Y and transformed WGS84 are in seoul.evidence.json, with KOGL Type 1 attribution also in public source_credits. No complete CSV or unrelated/personal fields retained. The optional pyproj==3.7.2 inspector can verify all saved transforms offline; no dependency was added to the application. Do not fetch again just to recover the saved facts.

Chrome inspected RYSE's official direct Naver link 1578505636; heading/address/homepage matched 130 Yanghwa-ro. All new map_verified flags remain false until independent admin review. Five other Naver IDs are third-party leads only in evidence; four are still missing. Further Chrome attempts failed with Debugger unattached, and in-app fallback also failed to attach. Do not claim those map checks happened. Known hotel-restaurant Naver IDs and wrong same-brand properties are explicitly excluded in evidence. Solaria's old host failed DNS; new official NNR site is used. Parnas standalone sites failed TLS; no certificate checks bypassed, official IHG SEOHA used instead.

Validation: 114 related tests passed (API content/platform/direct-link/travel-service tests plus 13 optional offline research-tool checks). Verified all ten stored projections without network, UTF-8 admin CSV transfer, closed/missing/duplicate permit rejection, and pending candidates never publicly usable. Five-language catalog and task integrity checks passed. No runtime/UI/migration changes in this follow-up; full CI will still run on the PR. Remaining: Kyoto/Busan, Rakuten usable entries, remaining map/landing reviews, separate product/option approvals and staged city release. Content task stays open; no new merge authorization or production writes/enablement/deployment assumed.
