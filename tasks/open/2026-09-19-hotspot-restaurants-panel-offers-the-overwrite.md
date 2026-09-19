---
id: 2026-09-19-hotspot-restaurants-panel-offers-the-overwrite
title: hotspot-restaurants-panel offers the overwrite step when a chosen meal answers meal_slot_occupied
status: open
priority: P3
area: web
owner:
claimed_at:
created_at: 2026-09-19T11:38:40Z
completed_at:
branch:
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

- [ ] When the selection fails with `code === "meal_slot_occupied"`, the panel explains the
      situation in the reader's language and offers one explicit overwrite action.
- [ ] The overwrite action resends the same body with `overwrite: true`; every other error keeps
      the current message.
- [ ] The panel sends `mode: "replace_meal", meal` instead of `meal_role` (both are accepted;
      the new shape is the documented one).
- [ ] Copy in five locales (`messages/*/restaurants.json`) and a test for the two-step flow.

## Steps

- [ ] Reuse the wording of `common.json` `cardActions.mealOccupied` / `cardActions.overwrite` or
      add restaurant-panel keys next to `tripSaved`.
- [ ] Test: first `trip-selections` answers 409 `meal_slot_occupied`, second (with `overwrite`)
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
