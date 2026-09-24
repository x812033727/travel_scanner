---
id: 2026-09-24-recover-news-candidates-interrupted-by-a
title: Recover news candidates interrupted by a worker restart at once
status: done
priority: P1
area: api
owner: claude-opus-5.5
claimed_at: 2026-09-24T06:05:12Z
created_at: 2026-09-24T06:05:03Z
completed_at: 2026-09-24T06:06:41Z
branch: claude/news-worker-restart-recovery
depends_on: []
scope:
  - apps/api/app/news_automation/worker.py
  - apps/api/app/news_automation/pipeline.py
  - apps/api/tests/test_news_pipeline.py
  - docs/news-automation.md
---

# Recover news candidates interrupted by a worker restart at once

## Why

On 2026-09-24 four deploys (from several sessions) restarted the news worker within a few
hours. Each one cut off the candidate being processed and left it in an in-flight status
(RQ recorded the jobs as `AbandonedJobError`). The scheduler only recovers such
candidates after 70 minutes, because a job may legitimately run for up to 60. Two of them
then held both global concurrency slots, and for over half an hour the worker did nothing
but defer the other 48 discovered candidates once a minute, each deferral a three-second
job.

## Definition of done

- [x] A news worker that starts recovers every in-flight candidate at once (marked
      `failed`/`news_processing_stale`, a `stale-recovery` run recorded, re-queued within
      the existing limit of two automatic recoveries).
- [x] The scheduler's 70-minute rule stays as the fallback.
- [x] The runbook describes it.

## Steps

- [x] `recover_stalled_candidates(older_than=...)`.
- [x] `app.news_automation.worker.recover_interrupted()` runs before the worker loop and
      disposes the engine before RQ forks.
- [x] Test: a candidate cut off two minutes ago is recovered, a waiting one is untouched.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

On the host after deploying: no candidate stays in `drafting`/`verifying`/`locale_review`
/`jev_review` after the news worker restarts, and the worker log shows
"re-queued after a worker restart" for each one it found.

## Notes

- This relies on there being exactly one news worker (compose service `news-worker`).
  Scaling it to more than one would make a starting worker fail another worker's
  running candidates; use the scheduler's time rule alone in that case.
- The deploy of this change restarts the worker, which also frees the two candidates
  that were holding the slots on 2026-09-24.
