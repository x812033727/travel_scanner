---
id: 2026-09-27-resume-jev-paused-news-candidates-as
title: Resume Jev-paused news candidates as soon as the daily budget has room
status: done
priority: P2
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-27T07:00:29Z
created_at: 2026-09-27T07:00:10Z
completed_at: 2026-09-27T07:04:11Z
branch:
depends_on: []
scope:
  - apps/api/app/news_automation/scheduler.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
  - docs/news-automation.md
---

# Resume Jev-paused news candidates as soon as the daily budget has room

## Why

On 2026-09-27 Jev's 200-call daily budget ran out at 02:57 UTC and 99 news candidates paused as
`news_jev_quota_paused`. The owner raised the budget to 5,000 in the admin at 06:56 UTC, but the
orphan sweep only lets paused candidates through after 00:00 UTC, so nothing would have run for
another 17 hours. They were resumed by hand that day (audit `news_candidate_reopened`).

## Definition of done

- [x] With room left in today's Jev budget, paused candidates are queued within a minute.
- [x] With the budget spent, or the counter unreadable, they still wait for 00:00 UTC.

## Steps

- [x] `pipeline.orphaned_candidates(jev_budget_left=...)` lets paused candidates through, without
      the two-hour orphan delay (no job waits for them).
- [x] `scheduler.jev_budget_left` reads the `jev-quota:<UTC day>` counter `consume_jev_call`
      spends and compares it with the runtime `jev_daily_call_budget`.
- [x] Tests and `docs/news-automation.md`.

## How to verify

`cd apps/api && uv run pytest tests/test_news_pipeline.py -k "budget or scheduler or paused"`.
On the host after deploy: raise the budget while candidates are paused and watch
`news-worker` pick them up in the next minute.

## Notes

`app/ai/jev.py` is in the scope of `2026-09-22-jev-review-advisory-tool` (still claimed although
#663 merged), so the key is read in the scheduler rather than exported from `jev.py`; a test
pins the two to the same key.
