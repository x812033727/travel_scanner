---
id: 2026-09-19-hotspot-restaurants-panel-offers-the-overwrite
title: hotspot-restaurants-panel offers the overwrite step when a chosen meal answers meal_slot_occupied
status: in-progress
priority: P3
area: web
owner: codex-b10e-web
claimed_at: 2026-09-30T10:57:16Z
created_at: 2026-09-19T11:38:40Z
completed_at:
branch: codex/remaining-tickets-20260930
depends_on: []
scope:
  - apps/web/components/hotspot-restaurants-panel.tsx
  - apps/web/components/hotspot-restaurants-panel.test.tsx
---

# hotspot-restaurants-panel offers the overwrite step when a chosen meal answers meal_slot_occupied

## Why

Since `2026-09-07-add-a-meal-to-a-day`, every `trip-selections` endpoint shares one
placement (`apps/api/app/trips/selections.py`): a lunch or dinner card the traveller already
chose a place for (`data.meal_selection_source == "user"`) answers `409 meal_slot_occupied`
until the request carries `overwrite: true`. `travel-card-actions` shows that as a readable
message with a second "換成這個" button. `hotspot-restaurants-panel` still posts the legacy
`meal_role` body to `POST /restaurants/{place_id}/trip-selections` (which keeps working: it
means `mode: replace_meal`), but on a 409 it only shows the API's localized `detail` in its
error line, with no way to say "yes, replace it". Placeholder and planner-suggested meals are
filled without asking, so this only bites when the reader re-picks a restaurant for a meal
they already chose.

## Definition of done

- [x] When the selection fails with `code === "meal_slot_occupied"`, the panel explains the
      situation in the reader's language and offers one explicit overwrite action.
- [x] The overwrite action resends the same body with `overwrite: true`; every other error keeps
      the current message.
- [x] The panel sends `mode: "replace_meal", meal` instead of `meal_role` (both are accepted;
      the new shape is the documented one).
- [x] Copy in five locales (reused existing `common.cardActions` keys) and a test for the two-step flow.

## Steps

- [x] Reuse the wording of `common.json` `cardActions.mealOccupied` / `cardActions.overwrite` or
      add restaurant-panel keys next to `tripSaved`.
- [x] Test: first `trip-selections` answers 409 `meal_slot_occupied`, second (with `overwrite`)
      answers 200.

## How to verify

```bash
cd apps/web && npx vitest run components/hotspot-restaurants-panel.test.tsx
npm run check:i18n && npm run typecheck:web && npm run lint:web
```

## Notes

- Contract and the occupied-slot decision: `apps/api/app/trips/selections.py` module docstring
  and `tasks/open/2026-09-07-add-a-meal-to-a-day.md` (2026-09-19 note). The reference UI is the
  `occupied` state in `apps/web/components/travel-card-actions.tsx`.

### 2026-09-30 local implementation (codex-b10e-web)

- Normal claim after checking main `422b3f68`, all files of 25 open PRs,
  remote/local branches and other worktrees. Historical #71/#74 changes match
  their merged scope contents; no current implementation collision was found.
- Only `ApiError` with status 409 and code `meal_slot_occupied` offers the explicit
  overwrite action. It resends the original restaurant URL, trip/version/date/meal
  snapshot with `overwrite: true`. All normal writes use `mode: replace_meal` and
  `meal`; existing five-locale `common.cardActions` copy avoids duplicate messages.
- Changing trip, date, meal or restaurant, canceling, or Escape invalidates the
  pending confirmation and any late response. Returning to the same choices does
  not restore an earlier confirmation. Other errors retain their original message.
- Added 15 regressions. Old component: 12 failed / 6 passed; corrected component:
  18 passed. Coverage includes the exact overwrite request, unrelated errors,
  six changes of context and delayed responses after cancellation/reselection.
  Independent code review passed. The isolated lint run was stopped to avoid
  duplicating root's full web lint; it is not recorded as a pass.
- This is local code and synthetic API testing only; no real trip was changed.
