---
id: 2026-09-14-preview-never-charged
title: Itinerary preview is limited but never charged
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-14T13:50:03Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/trips/router.py
  - apps/api/app/usage/service.py
  - apps/api/tests/test_trip_intents.py
  - apps/api/tests/test_usage_settings.py
  - apps/web/components/trip-editor.tsx
  - apps/web/components/trip-editor.test.tsx
  - apps/web/messages
---

# Itinerary preview is limited but never charged

## Why

`POST /trips/{id}/itinerary/preview` (`app/trips/router.py`) runs the full planner -- a real
provider call -- and the usage ledger never sees it. The charge lands on
`/itinerary/apply`, so a caller who previews and never applies pays nothing. The only bound
is the inline `ai-itinerary-preview-user` limiter at 12/hour, which means every account has
twelve free provider calls an hour, indefinitely, and registration grants `TRIAL_3` without
payment.

The account-wide ceiling from `2026-09-14-planner-spend-ceiling` now sits above this, so it
is no longer unbounded. What is left is a pricing question rather than an abuse one: preview
is the expensive half of the feature and it is the half that is free.

## Definition of done

- [ ] A decision, written down, on whether previewing costs a use.
- [ ] If it does: reserved on preview and released when the planner falls back to catalog,
      matching how `/itinerary/generate` already treats a result nobody asked to pay for.
- [ ] Whatever is decided, the remaining-uses copy tells the reader before they spend it --
      the point `2026-09-11-quota-and-limits-shown-too-late` already made about the trip cap.

## Steps

- [ ] Decide with whoever owns pricing; this is not a change to make unilaterally.
- [ ] If charging: `reserve_use` in `preview_trip_itinerary`, release on a catalog result.
- [ ] Update the preview UI copy so the cost is visible before the button, not after.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_trip_intents.py tests/test_usage_settings.py -q
```

## Notes

Found while closing the planner spend holes. Left out of that task on purpose: it changes
what the product charges for, which is a different kind of decision from stopping an
unbounded loop, and the ceiling shipped there already caps the worst case.
