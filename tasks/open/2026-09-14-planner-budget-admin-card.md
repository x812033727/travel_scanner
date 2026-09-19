---
id: 2026-09-14-planner-budget-admin-card
title: Planner budget cannot be lowered without a restart
status: review
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T11:12:49Z
created_at: 2026-09-14T13:50:02Z
completed_at:
branch: claude/travel-scanner-pr-552-rpq36m
depends_on: []
scope:
  - apps/api/app/admin/service.py
  - apps/api/tests/test_admin_provider_settings.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/components/admin-settings-panel.test.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-TW/admin.json
  - apps/web/messages/zh-CN/admin.json
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

- [x] The owner can lower both budgets from the back office and have the next planning
      request honour the new number.
- [x] The card explains what reaching the budget does, since it degrades to the catalogue plan
      rather than refusing (except on `/intents`, which answers 429 `planner_budget_reached`)
      and that is not what a reader expects a limit to do.

## Steps

- [x] Add both fields to the `ai_planner` `ProviderDefinition` tuple in `app/admin/service.py`.
- [x] Add them to the field type map in `apps/web/components/admin-settings-panel.tsx`.
- [x] Label and describe them in all five `apps/web/messages/*/admin.json`.

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

### 2026-09-19 done in repo (claude-fable-5-1)

What changed:

- `apps/api/app/admin/service.py`: `ai_planner_user_budget` and `ai_planner_ip_budget` join the
  `ai_planner` `config_fields` tuple, right after `ai_planner_max_output_tokens`. That tuple is
  both the update allowlist (`_validate_provider_values`) and what `apply_runtime_overrides`
  copies onto `Settings`, so nothing else on the API had to move. Bounds stay the ones
  `config.py` already declares (1..1000 and 1..10000); the card gets the same 422
  `provider_setting_invalid` an env file would get for 0.
- No restart is needed because there is no cache to bust: every planning route calls
  `load_runtime_settings(session)` per request, which re-reads `provider_configs` and hands
  the merged `Settings` to `plan_within_budget`; `/intents` goes through the same
  `_build_ai_planning` path. `get_settings()` is the only `lru_cache`, and it holds the
  environment base only.
- `apps/api/tests/test_admin_provider_settings.py`: three tests -- the fields validate and
  clear back to the environment value, the bounds hold from the card, and a row storing 1 / 2
  is what `budget_spent` receives on the next call while the spent ceiling comes back as the
  catalogue plan with `planner_budget_reached` rather than a refusal.
- `apps/web/components/admin-settings-panel.tsx`: both fields in `fieldMeta` as
  `{ localized: true, type: "number" }`, the same shape as the timeout and token fields, so
  they save as integers (`Number(value)`) and render as spinbuttons.
- `apps/web/components/admin-settings-panel.test.tsx`: the planner snapshot carries both
  values; a test reads them, checks the help text says the ceiling degrades to the catalogue
  plan and that only `/intents` answers 429 `planner_budget_reached`, lowers the account
  budget to 1 and asserts the request body is `{ ai_planner_user_budget: 1 }` only.
- All five `apps/web/messages/*/admin.json`: `providerFields.ai_planner_user_budget` and
  `providerFields.ai_planner_ip_budget`, each with `label` + `help` (the panel reads `help`,
  not `description`, for every localized field). The help names the window variable, the
  default (40 / 120), the catalogue fallback, the `/intents` 429 and that a lower number
  applies to the next request. Inserted as new lines only, because the same files were being
  edited by another change on this branch; the claim was forced for that overlap and the
  scope narrowed from `apps/web/messages` to the five files.

Decisions and leftovers:

- `ai_planner_user_budget_window_seconds` stays environment-only: the ticket asks for the two
  ceilings, and a window edit changes the meaning of both numbers at once.
- The card's API-side description (Chinese, unlocalized) is unchanged; the explanation sits
  under each number, where whoever lowers it is reading.
- `docs/anti-scraping.md` and `.env.example` still describe the env vars only; both are
  outside this scope and still true (the env value is the base the card overrides).

Checks run: `uv run pytest tests/test_planner_budget.py tests/test_admin_provider_settings.py -q`
(116 passed), `uv run ruff check .` and `uv run mypy app` (clean, 338 files), `npm run check:i18n`
(5 locales, 25 namespaces), `npx vitest run components/admin-settings-panel.test.tsx` (53 passed),
`npm run lint:web` and `npm run typecheck:web` (clean).

Back-office check for the owner, once deployed: open AI 行程規劃, set 每個帳號的 AI 規劃次數上限 to
1, save. With one account, in one hour: the first planning request (trip creation, replan
preview or `/intents`) reaches a vendor; the second `/intents` answers 429
`planner_budget_reached`, and a second trip creation or preview answers the catalogue plan
with the `planner_budget_reached` warning. No restart anywhere. Clear the field afterwards
to fall back to `AI_PLANNER_USER_BUDGET`, or type the number you want.
