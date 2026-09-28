---
id: 2026-09-28-run-news-candidates-on-a-pool
title: Run news candidates on a pool of news workers instead of one at a time
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-28T12:05:00Z
created_at: 2026-09-28T12:04:00Z
completed_at:
branch: claude/news-second-worker
depends_on: []
scope:
  - apps/api/app/news_automation/worker.py
  - apps/api/app/news_automation/duplicates.py
  - apps/api/app/config.py
  - apps/api/tests/test_news_pipeline.py
  - .agents/skills/prod-host-ops/references/news-ops.md
  - docs/news-automation.md
---

# Run news candidates on a pool of news workers instead of one at a time

## Why

On 2026-09-28, after the extractor fix (#892) and the backfills, the news pipeline finally
had a queue of work. Production then showed the next limit: `news-worker` is a single RQ
worker process. It runs one candidate at a time, and a candidate is about 25 model calls
(draft, verification, Jev, four translations, locale reviews and five final edits), so about
3 to 5 candidates finish per hour. Source scans share that one process, so each hourly scan
waits behind whatever candidate is running.

The admin already has `global_concurrency` (2) and `per_vertical_concurrency` (1). They could
never take effect, because only one job ever ran.

## Definition of done

- [x] The one `news-worker` container runs a pool of RQ workers (`news_worker_processes`,
      default 3, env `NEWS_WORKER_PROCESSES`). The admin's concurrency settings still gate
      how many candidates run at once.
- [x] Restart recovery stays correct. It runs once in the container before the pool starts,
      so failing every in-flight candidate is still safe. A second news-worker container
      would break this, and the docs now say so.
- [x] Two workers cannot draft two outlets' versions of one story side by side:
      `duplicates.known_titles` includes in-flight candidates.
- [ ] After deploy: the container shows the pool's workers (`rq info` or logs), and more than
      one candidate runs at once when the settings allow.

## Steps

- [x] `worker.py`: `WorkerPool` when the size is above 1. Windows development stays on one
      `SimpleWorker`, because it cannot fork.
- [x] `config.py`: `news_worker_processes` (1 to 8).
- [x] `duplicates.KNOWN_STATUSES` includes the pipeline's active statuses, and a test keeps
      the two lists in step.
- [x] Tests: the pool starts after recovery, the pool size, and an in-flight story counts as
      a known title.
- [x] Docs: `news-ops.md`, `docs/news-automation.md`.
- [ ] Owner: raise `per_vertical_concurrency` from 1 to 2 in /admin/news. Most of the backlog
      is one vertical (tech), and with 1 the second worker only helps across verticals.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_news_pipeline.py -q
```

After deploy, on the host:

```bash
docker compose -f docker-compose.prod.yml exec -T news-worker rq info -u "$REDIS_URL" --only-workers
```

## Notes

- RQ 2.12 `WorkerPool` forks its workers, and each one runs `with_scheduler=True`. RQ's
  scheduler lock lets only one of them move scheduled jobs.
- The pool's parent handles SIGTERM, which sends SIGINT (a warm stop) to its workers. A
  deploy still interrupts the running candidates, and the next start recovers them as before.
- Candidates share the host's subscription accounts. With two candidates running, the
  five-hour windows fill faster, and `ai_subscription_fallback=wait` pauses a stage for 30
  minutes when every account is full.
