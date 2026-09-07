---
id: 2026-09-07-hotel-platform-options-and-quote-readiness
title: Hotel platform options and quote readiness
status: in-progress
priority: P1
area: api
owner: codex-hotel-platforms
claimed_at: 2026-09-07T12:33:33Z
created_at: 2026-09-07T12:32:44Z
completed_at:
branch: codex/hotel-platforms
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

## Why

Keep one hotel identity while independently reviewing each platform, enabling commission links only after qualification, and preparing honest on-demand quotes without activating paid APIs.

## Definition of done

- [x] Ordinary and qualified affiliate links share one independently reviewed platform option; legacy clients remain compatible.
- [x] Migration preserves product/trip IDs and removes dual authority in facts.hotel_links.
- [x] No unlicensed live API, fake price, guessed platform identity, or automatic booking.
- [ ] Six cities each have ten verified hotels, three areas, official and two OTA links, checks for all five OTAs, and public source attribution.
- [ ] API, migration, i18n, typecheck, lint, production build, five-language responsive E2E pass.
- [ ] City rollout only after factual review and actual link checks. No unverified affiliate enablement.

## Steps

- [x] Isolated worktree from verified main 54009ba; original dirty worktree preserved.
- [x] Independent options, compatibility import, safe clickout, quote contract and policy gates.
- [x] Five-language public/admin panels and source attribution.
- [ ] Extended regression tests and full validation.
- [ ] Verified 60-hotel research/import package and city release gates.

## How to verify

Run uv pytest for travel services and hotel platforms; fresh Alembic migration on a disposable PostgreSQL database; web i18n/typecheck/lint/build/Vitest and travel-services Playwright on 320/390/1280px.

## Notes

Full web regression completed: 126 test files / 729 tests passed. All three pending city packages validate (four content tests), including the licensed Osaka coordinate-column correction. Taipei CSV preview has ten rows; i18n and Ruff rerun passed.

Branch CI 34131439819: web, containers and unmocked full-stack smoke passed. Full Linux API ran 1,721 tests; two new assertions incorrectly assumed empty shared audit tables. Fixed them to assert exact before/after deltas (ordinary adds zero affiliates, one affiliate plus one fallback adds exactly one). Related integration rerun: 19 passed. Added independent option recheck reminders and hotel affiliate/fallback counters, and preserved saved evidence in the admin editor; three admin component tests passed. A new full CI run is required for the fix.

0057 migration succeeded on empty PostgreSQL. Related migration/API regression batch: 113 passed; row-lock hardening rerun: 40 passed. Ruff and full mypy (236 source files) passed. Five-language i18n, typecheck, lint and production build passed. Related Vitest: 32 passed; Playwright desktop 50 and mobile 53 passed. Actual Redis/RQ daily worker smoke passed on isolated PostgreSQL/Redis. Tools: 27 passed. Full Python collection on Windows hits the existing deployment agent UnixStreamServer import; Linux CI must verify the full suite.

Thirty pending research inputs exist: Tokyo, Osaka and Taipei each ten, preserving the original Tokyo six source keys. Kyoto, Seoul and Busan are NOT complete; no city has completed independent approvals/all platform checks. See docs/hotel-platforms/README.md for precise gaps. Twenty-four metered IDs-only lookups have already run; saved IDs must not be re-requested unnecessarily. Production settings, secrets and hotel rows are unchanged. Do not mark this task done or enable cities from the pending-input count.
