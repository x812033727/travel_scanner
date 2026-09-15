---
id: 2026-09-14-planner-budget-admin-card
title: Planner budget cannot be lowered without a restart
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-14T13:50:02Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/admin/service.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/messages
---

# Planner budget cannot be lowered without a restart

## Why

`AI_PLANNER_USER_BUDGET` and `AI_PLANNER_IP_BUDGET` are what stand between the AI planner and
someone spending its provider bill (`2026-09-14-planner-spend-ceiling`). They are environment
variables, so lowering one during an attack means editing a file and restarting the API --
which needs shell access to the host at exactly the moment nobody wants to be at a terminal.

The AI planner already has a back office card. `ai_planner_mode`, `ai_planner_priority` and
`ai_planner_max_output_tokens` are all editable there through the `ProviderDefinition`
allowlist in `app/admin/service.py`, and `plan_within_budget` already reads its limits off the
runtime settings, so the values would be picked up with no change to the planner at all.

## Definition of done

- [ ] The owner can lower both budgets from the back office and have the next planning
      request honour the new number.
- [ ] The card explains what reaching the budget does, since it degrades to the catalogue plan
      rather than refusing (except on `/intents`, which answers 429 `planner_budget_reached`)
      and that is not what a reader expects a limit to do.

## Steps

- [ ] Add both fields to the `ai_planner` `ProviderDefinition` tuple in `app/admin/service.py`.
- [ ] Add them to the field type map in `apps/web/components/admin-settings-panel.tsx`.
- [ ] Label and describe them in all five `apps/web/messages/*/admin.json`.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_planner_budget.py tests/test_admin_provider_settings.py -q
npm run check:i18n && npm run test:web
```

Then set the budget to 1 in the back office and confirm the second planning request in the
window comes back with `planner_budget_reached` without restarting anything.

## Notes

Split out of `2026-09-14-planner-spend-ceiling` deliberately: the budget itself is API-only,
and pulling in the settings panel plus five locale files would have widened that change from
a spend fix into a back-office one. Nothing here blocks it -- env vars already work.
