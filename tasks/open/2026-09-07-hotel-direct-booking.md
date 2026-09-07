---
id: 2026-09-07-hotel-direct-booking
title: Hotel booking without affiliate enrollment
status: in-progress
priority: P1
area: api
owner: codex-hotel-direct
claimed_at: 2026-09-07T10:45:13Z
created_at: 2026-09-07T10:45:12Z
completed_at:
branch: codex/hotel-direct-booking
depends_on: []
scope:
  - apps/api/app/travel_services
  - apps/api/tests/test_hotel_direct_booking.py
  - apps/api/tests/test_travel_services_integration.py
  - apps/web/components/travel-services
  - apps/web/messages
  - apps/web/e2e/travel-services.spec.ts
  - apps/web/app/api/travel
  - docs/travel-services.md
---

# Hotel booking without affiliate enrollment

## Why

The user approved ordinary hotel booking without affiliate enrollment. Hotels must
remain browseable/selectable and link to reviewed exact websites without waiting
for a Travelpayouts account or brand approval. Root dirty checkout is untouched.

## Definition of done

- [x] Ordinary links are reviewed separately from affiliate offers and require no token/project.
- [x] Hotel-only CSV can be committed without a network account; mixed affiliate imports stay gated.
- [x] Five-language visitor/admin UI labels ordinary links, preserves unknown prices and trip selection.
- [ ] API, type/lint, translation, unit, build and responsive Playwright checks pass.
- [ ] PR opened with release gates documented; do not merge/deploy without approval.

## Steps

- [x] Add typed, identity-evidenced hotel links in existing product facts; default-off switch.
- [x] Bounded DNS-pinned website validation, stale/pending/disabled guards, saved-ID clickout.
- [x] Admin editor and public new-tab forms; ordinary clicks never imply bookings or commissions.
- [ ] Validate and hand off.

## How to verify

`uv run pytest tests/test_hotel_direct_booking.py tests/test_travel_services.py`
and PostgreSQL `tests/test_travel_services_integration.py`; Ruff/mypy, five-language
check, Vitest catalog/admin/BFF tests, production build and travel-services Playwright
at 320/390/1280px in all locales. CI exercises the full existing migration chain.

## Notes

Base: origin/main 8853695. No migration, real hotel seeds, brand approval, production
config edits or deployment in this change. Website anti-bot/redirect failures stay
closed and require an alternative exact reviewed URL; the UI still allows selecting
the hotel. All test hotel pages are explicit fixtures, never real bookings.
Existing production Klook tpx.gr affiliate compatibility remains separate follow-up
work, not fixed or bypassed by ordinary hotel booking. Actual catalog is still empty;
hotel sourcing and manual verification remain necessary before public launch.

Local verification so far: 74 focused API tests, Ruff, mypy (234 source files),
typecheck, five-language keys and 24 catalog/admin/BFF Vitest tests passed. Disk
exhaustion interrupted the first lint/build attempt; available space subsequently
recovered and validation resumed. Full Windows pytest collection hits the pre-existing
deployment_agent UnixStreamServer limitation; Linux CI must cover that module.
