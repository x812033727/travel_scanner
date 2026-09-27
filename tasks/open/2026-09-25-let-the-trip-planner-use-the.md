---
id: 2026-09-25-let-the-trip-planner-use-the
title: Let the trip planner use the Claude subscription within a reader's wait
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-25T13:07:41Z
completed_at:
branch:
depends_on:
  - 2026-09-25-run-the-site-s-claude-features
scope:
  - apps/api/app/ai/itinerary.py
  - apps/api/app/ai/trip_parser.py
  - apps/api/app/admin/service.py
  - apps/api/tests/test_ai_itinerary.py
  - apps/api/tests/test_planner_budget.py
  - apps/web/app/api/travel/[...path]/route.ts
---

# Let the trip planner use the Claude subscription within a reader's wait

## Why

Since 2026-09-25, 「Claude 連線方式: 訂閱帳號」 moves the site's background Claude calls onto
the host's subscription accounts. The trip planner and the trip text parser still use only the
Anthropic key. A reader waits for both: the parser has a hard 12 s ceiling, the planner a
15 s per-vendor and 35 s total budget, and the web proxy cuts planner routes at 15 s. A Claude
Code run takes tens of seconds, and longer when the accounts are busy.

The owner asked for every Claude feature to use the subscription, and on 2026-09-25 approved
the plan in which a reader saving a trip may wait up to about two minutes for it. The parser
cannot fit a CLI run into 12 s, so it skips the subscription.

## Definition of done

- [ ] A subscription planner provider (schema in the prompt,
      `queue_seconds` 0), its own timeout (about 120 s), a total budget of about 150 s in
      subscription mode, and a longer web proxy timeout for the planning routes only.
- [ ] The trip parser skips the subscription and says so on the settings card.

## Steps

- [ ] Measure a real planner prompt through `/v1/runs` on the host first.

## How to verify

`tests/test_ai_itinerary.py` and `tests/test_planner_budget.py` cover the timeout and the
fallback in subscription mode, and a trip created on the site in subscription mode arrives.
