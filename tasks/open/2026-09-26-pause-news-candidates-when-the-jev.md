---
id: 2026-09-26-pause-news-candidates-when-the-jev
title: Pause news candidates when the Jev daily budget is spent, instead of holding them as uncertain duplicates
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5-news-backfill
claimed_at: 2026-09-26T22:03:56Z
created_at: 2026-09-26T22:03:21Z
completed_at:
branch: claude/news-jev-quota-pause
depends_on: []
scope:
  - apps/api/app/news_automation/pipeline.py
  - apps/api/app/news_automation/jobs.py
  - apps/api/app/news_automation/backfill_cli.py
  - apps/api/tests/test_news_pipeline.py
  - apps/api/tests/test_news_backfill_cli.py
  - apps/api/tests/test_news_jobs.py
  - docs/news-automation.md
---

# Pause news candidates when the Jev daily budget is spent, instead of holding them as uncertain duplicates

## Why

On 2026-09-26 a backfill reopened 127 news candidates and the hourly scan added about 124
from ten new sources. Jev's budget (200 calls per UTC day) ran out at 15:01Z, and from then on
every duplicate check returned `("manual", None, ["quota_unavailable"])`, which the pipeline
stored as `news_duplicate_uncertain`: 207 of 243 duplicate checks, 115 of the 127 reopened
candidates. Nothing was uncertain about those stories, and nothing would ever run them again.

## Definition of done

- [x] A spent budget at the duplicate check pauses the candidate (`news_jev_quota_paused`,
      status `discovered`) and records no assessment.
- [x] The orphan sweep leaves paused candidates until the UTC day ends, then runs them.
- [x] `backfill_cli --jev-quota-holds` reopens the existing holds, paused, without queueing.
- [ ] Merged and deployed; the 2026-09-26 holds reopened with `--jev-quota-holds --apply`.

## Steps

- [x] pipeline.py, jobs.py (comment), backfill_cli.py; tests; docs/news-automation.md.
- [ ] PR, CI, merge, deploy, reopen the holds.

## How to verify

`pytest tests/test_news_pipeline.py tests/test_news_backfill_cli.py -k "jev or orphan or backfill"`.
After the deploy, a dry run of `backfill_cli --since 2026-09-01 --jev-quota-holds` lists the holds.

## Notes

- `app/ai/jev.py` is untouched: `consume_jev_call` already returns False without calling Jev
  when the budget is spent, so the pause costs nothing, and the file is in the scope of the
  stale `2026-09-22-jev-review-advisory-tool` claim.
- Later Jev stages keep their holds (`news_jev_final_hold` is publishable by the owner).
