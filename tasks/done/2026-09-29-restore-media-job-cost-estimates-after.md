---
id: 2026-09-29-restore-media-job-cost-estimates-after
title: Restore media job cost estimates after refunded retries
status: done
priority: P1
area: api
owner: codex-media-retry-pricing
claimed_at: 2026-09-29T03:49:32Z
created_at: 2026-09-29T03:47:34Z
completed_at: 2026-09-29T03:52:28Z
branch: codex/story-image-model-pricing
depends_on: []
scope:
  - apps/api/app/video_media/jobs.py
  - apps/api/tests/test_video_media_jobs.py
---

# Restore media job cost estimates after refunded retries

## Why

When a vendor refusal refunds a media generation, the API resets that job's cost
estimate to zero. Retrying the same request reuses the job ID and reserves the
budget again, but did not restore its estimate. A later successful image could
therefore be returned to the worker as free and understate the per-video ledger.

## Definition of done

- [x] A refunded image job that succeeds on retry reports the selected model's
      positive price, retaining its job ID and incrementing its attempt count.
- [x] Both the default Pro model and a series' Flash override retain their own
      prices; returning the ready job again adds no vendor call or reservation.
- [x] Focused API tests, Ruff and mypy pass without production or paid calls.

## Steps

- [x] Check active tasks, worktrees, remote branches and open PRs before claiming.
- [x] Demonstrate default Pro and series Flash refunded-retry failures in tests.
- [x] Restore the selected catalog estimate when a new retry is reserved.
- [x] Run focused API and static checks and record their exact results.

## How to verify

From `apps/api`, using this worktree's `.venv/Scripts/python.exe`:

```powershell
.venv/Scripts/python.exe -m pytest tests/test_video_media_jobs.py tests/test_video_story_policy.py tests/test_video_media_api.py tests/test_video_media_catalog.py -q
.venv/Scripts/python.exe -m ruff check app/video_media/jobs.py tests/test_video_media_jobs.py
.venv/Scripts/python.exe -m mypy app/video_media/jobs.py tests/test_video_media_jobs.py
```

## Notes

The owner authorized this related API correction with the story image pricing
work. No active task owns these paths. Draft merge-train PR #959 lists the already
merged #938; both target file blobs match this branch exactly, so it contains no
competing retry-pricing change. No other implementation is being replaced.

Only `jobs.py`, its existing test module and this task are in scope. Tests use the
existing fake vendor/session and fakeredis; no production, provider or paid calls.

Validation on 2026-09-29:

- Before the implementation change, the new parameterized test failed for both
  default Pro and the series Flash override: the ready job reported 0 instead of
  0.134 or 0.067 respectively. Focused red run: 2 failed / 9 deselected in 17.20s,
  exit 1.
- The retry now assigns `meter.usd_for(model, kind, seconds)` after its budget
  reservation succeeds, beside `attempts += 1`. This uses the same selected model
  and estimator as a new job. Failed reservation, ready-job dedupe and refund
  behavior retain their existing paths.
- All four listed API test modules: **34 passed**, no skipped tests, 13.67s,
  exit 0. The regression proves failure/refund, same-ID retry, positive ready-job
  API output, selected vendor model and repeat-ready dedupe/reservation behavior.
- Scoped Ruff: all checks passed, exit 0. Scoped mypy: no issues in 2 source files,
  exit 0.

These are local tests against controlled fixtures. Production deployment and
live provider billing are not claimed; repository-wide exact-head CI belongs
to the containing PR.
