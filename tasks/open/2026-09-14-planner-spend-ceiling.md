---
id: 2026-09-14-planner-spend-ceiling
title: AI itinerary planning has no spend ceiling
status: review
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-14T13:15:06Z
created_at: 2026-09-14T13:15:02Z
completed_at:
branch: claude/festive-tesla-qtibnk
depends_on: []
scope:
  - apps/api/app/infra.py
  - apps/api/app/ai/itinerary.py
  - apps/api/app/config.py
  - apps/api/app/trips/router.py
  - apps/api/tests/conftest.py
  - apps/api/tests/test_planner_budget.py
  - apps/web/components/trip-editor.tsx
  - apps/web/messages
  - .env.example
  - docs/anti-scraping.md
  - architecture.md
---

# AI itinerary planning has no spend ceiling

## Why

`POST /trips` plans with the LLM and counts nothing. `save_trip` (`app/trips/router.py`)
calls `AIItineraryPlanner.generate` whenever `source` is `blank` and `planning_mode` is not
`manual_blank` -- and `ai_draft` is that field's default, so a request that simply omits it
spends provider money. There is no rate limit on the path and no usage charge; planning at
creation is free by design (`architecture.md`).

The only ceiling is the 20 saved trips cap, and `DELETE /trips/{trip_id}` makes that cap
mean nothing: create, delete, create is an unbounded loop, and each turn of it is not one
call but up to four, because the planner fails over across the whole roster and Gemini
retries itself once on a validation failure. `AI_PLANNER_MAX_OUTPUT_TOKENS` is 12000.

Two smaller versions of the same hole sit beside it. The deprecated
`POST /trips/{id}/itinerary/generate` reaches the planner with no limit either. And both it
and the trip-intent path *refund* the slot they counted whenever the planner falls back to
catalog -- correct for a traveller who lost a real outage, and a lever for anyone who can
provoke one: the calls are attempted, the budget is handed back, repeat.

## Definition of done

- [x] An account cannot spend provider calls on itinerary planning without bound, however
      many trips it creates and deletes.
- [x] Reaching the ceiling still produces a usable itinerary from the reviewed catalogue --
      it never refuses, and it says which of the two happened rather than borrowing the
      copy for a provider outage.
- [x] A genuine full-provider outage still costs the traveller nothing, exactly as today.
- [x] The ceiling can be lowered on a running deployment without a rebuild.
- [x] Redis being unreachable stops the spend instead of opening it.

## Steps

- [x] `budget_spent` in `app/infra.py`: the fail-closed counterpart to
      `over_named_rate_limit`, for a budget that costs money rather than load.
- [x] `app/ai/itinerary.py`: lift the catalog tail of `generate` into `catalog_result`,
      add `planner_budget_reached`, and add `plan_within_budget` as the one entry point
      that spends the roster.
- [x] Skip the roster entirely when no candidate could survive `normalize_draft`.
- [x] `ai_planner_user_budget` + `ai_planner_user_budget_window_seconds` in `config.py`,
      and the matching block in `.env.example`.
- [x] Route all three user-facing planner call sites in `app/trips/router.py` through
      `plan_within_budget`; leave the refunds alone.
- [x] Neutralise the new default in `tests/conftest.py`.
- [x] `planner_budget_reached` copy in the five `apps/web/messages` locales, the code list
      in `trip-editor.tsx`, and a headline that does not claim an outage.
- [x] `docs/anti-scraping.md` Known gaps, and the planning paragraph in `architecture.md`.

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest
npm run lint:web && npm run check:i18n && npm run typecheck:web && npm run test:web
npm run test:tools && npm run check:tasks
```

End to end, against the original attack: start the API with `AI_PLANNER_USER_BUDGET=2`,
then `POST /trips` three times on one account with `planning_mode: "ai_draft"`. The first
two responses carry a real provider in `data.planning.provider`; from the third it is
`catalog` with `status: "fallback"` and `planner_budget_reached` in the warnings, and the
status code is still 201. Then run create-delete-create and confirm deleting a trip does
not give the budget back.

## Notes

**Claimed with `--force`.** `2026-09-12-trip-partner-offer-availability` holds
`apps/api/app/trips/router.py` in its scope, but its claim has been open since
2026-09-12T13:27:21Z -- past the 24 hour staleness rule in `tasks/README.md`. Same
convention as `tasks/done/2026-09-12-edge-rate-limit-and-header-hygiene.md`. The overlap is
three call-site lines in a 6000 line file, nowhere near that task's partner-offer work.

**Why degrade instead of 429.** Refusing to create a trip is the harshest outcome available
and the UI already renders the alternative: `trip-editor.tsx` shows the fallback badge, and
the copy exists in all five locales. `app/ai/trip_parser.py` sets the precedent -- its rate
gate returns `MockAITripParser` rather than raising. So the ceiling costs an abuser money
and costs a heavy traveller nothing but a less clever itinerary.

**Why a new warning code rather than `planner_fallback_used`.** That string reads "the
providers could not do it". Showing it to someone who actually hit their own ceiling is the
kind of dishonesty `intents.py` already argues against in its fallback comment.

**Why the refunds did not need changing.** The new counter is never refunded and sits
inside the shared entry point, so it bounds the attempts themselves. The existing
refundable limiters keep doing their own, different job, and a traveller who loses a real
outage still gets their slot back.

**Not in this task**, deliberately: moving the budget onto the back office AI planner card
(`app/admin/service.py` `ProviderDefinition`) would let the owner lower it without even a
restart, but it pulls in `admin-settings-panel.tsx` and five `admin.json` files. Metering
`POST /{id}/itinerary/preview`, which is limited to 12/hour but never charged, is a pricing
decision rather than an abuse fix. Both are worth their own tasks.

## 本次驗證（claude-opus-5, 2026-09-14）

Full suite green: `ruff`, `mypy app`, 3740 pytest passed / 277 skipped; web lint, typecheck,
`check:i18n`, 2809 vitest passed; `test:tools` 48 passed; `check:tasks` validated.

End to end against a real Redis with the real Lua counter, `AI_PLANNER_USER_BUDGET=2` and
`AI_PLANNER_IP_BUDGET=3`:

- Five create-delete-create attempts asked the roster **twice**. Attempts 3-5 returned the
  catalogue plan carrying `planner_budget_reached` alone, while the two real provider
  failures carried `planner_provider_failed` + `planner_fallback_used` -- the distinction
  the trip editor now renders as two different headlines.
- Three **fresh accounts** on the same address were stopped by the address ceiling after one
  more call, so minting accounts does not reset the budget.
- A request with no candidates never reached a provider and was not counted, because nothing
  was spent.
- `abuse:ai-planner-llm-user:<date>` and `abuse:ai-planner-llm-ip:<date>` both populated with
  hashed sources, so the numbers can be judged against real traffic.

## Notes from doing it

**`Request | None = None` does not work in FastAPI.** It looks like the polite way to add the
caller's address without disturbing the signature, and it raises `FastAPIError: Invalid args
for response field` at import: `analyze_param` uses `lenient_issubclass`, so a union falls
through the "is this a Starlette type" check and is treated as a Pydantic body field. It has
to be a bare `request: Request`, which then has to precede the defaulted `idempotency_key`,
which is why `tests/test_trip_create_replay.py` grew a positional argument.

**The per-address budget was not in the original plan and is why it is there now.** Per
account alone looked sufficient until `/auth/register` turned out to return a token
immediately with no email verification, which makes `AUTH_REGISTER_IP_LIMIT` (30/h) a
multiplier on any per-account number. The residual gap -- someone with many addresses -- is
written down in `docs/anti-scraping.md` Known gaps rather than left implied.

**The no-candidate guard removes more waste than the budget does, for the cheapest attack.**
`normalize_draft` keeps only items naming a `candidate_key` the request supplied, and
`_load_ai_planner_candidates` returns `[]` on a `match_destination` miss, so a destination
name the catalogue does not know spent the whole roster and could not produce one usable
item. It costs a caller nothing to type and cost us four vendors. Found while checking the
budget design, fixed in the same door.
