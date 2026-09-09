---
id: 2026-09-09-add-privacy-scoped-stay22-script-backend
title: Add privacy scoped Stay22 script backend
status: in-progress
priority: P1
area: api
owner: codex-stay22-backend
claimed_at: 2026-09-09T13:26:11Z
created_at: 2026-09-09T13:26:02Z
completed_at:
branch: codex/stay22-modular-toggle
depends_on: []
scope:
  - apps/api/app/travel_services/schemas.py
  - apps/api/app/travel_services/hotel_admin.py
  - apps/api/app/travel_services/router.py
  - apps/api/app/travel_services/stay22_script.py
  - apps/api/tests/test_stay22_script.py
  - apps/api/tests/test_stay22_admin.py
  - apps/api/tests/test_stay22_clickout.py
---

# Add privacy scoped Stay22 script backend

## Why

An optional full Stay22 script needs a minimal, public-only data boundary without
exposing account/trip information or replacing private native clickouts.

## Definition of done

- [x] Script can be enabled with a validated public LMA ID; legacy Allez saves preserve it.
- [x] Public document gets only reviewed safe hotel links while inactive/privacy requests get none.

## Steps

- [x] Implement backward-compatible config and minimally scoped public endpoints.
- [x] Validate mode, privacy, catalog/review/URL gates and unchanged native flows.

## How to verify

From `apps/api`, using the existing Python 3.13 environment read-only with this
worktree's `apps/api` as `PYTHONPATH`:

```text
python -m ruff check app/travel_services/schemas.py app/travel_services/hotel_admin.py app/travel_services/router.py app/travel_services/stay22_script.py tests/test_stay22_script.py tests/test_stay22_admin.py tests/test_stay22_clickout.py
python -m mypy app/travel_services/schemas.py app/travel_services/hotel_admin.py app/travel_services/router.py app/travel_services/stay22_script.py
python -m pytest tests/test_stay22_script.py tests/test_stay22_admin.py tests/test_stay22_routes.py tests/test_stay22_clickout.py tests/test_stay22_context.py tests/test_hotel_options.py tests/test_admin_hotels.py tests/test_travel_services.py -q -rs
```

Ruff and mypy passed; **326 tests passed, 2 skipped** (PostgreSQL-only concurrent
hotel config tests; CI must run those on PostgreSQL). No external OTA requests,
script execution, affiliate attribution or bookings are verified by these tests.

## Notes

- Public script config exposes only effective `enabled`, mode and LMA ID; all off
  and DNT/GPC responses hide the ID. Existing public config still excludes Stay22.
- Script additionally requires ordinary hotel links to be enabled: original
  anchors are the fallback if the browser blocks the SDK, never a bypass of the
  direct-link policy. Private/native Allez can still work with direct links off.
- Public script options recheck publication, destination, option review freshness,
  exact identity, query-free URLs and DNS. Off/privacy/unpublished returns 404;
  independently unavailable options are omitted, leaving an honest empty list.
- No migration or change to the private/native clickout channel selection.
- Initial `uv` install failed updating Windows PE executable resources; reused
  `../stay22-hotel-clickout/apps/api/.venv/Scripts/python.exe` without modifying it.
- Parent owns PR, integration and deployment. This task is implemented and awaiting
  integration; do not mark merged based on the local tests alone.
