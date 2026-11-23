---
id: 2026-11-22-api-tests-red-on-windows
title: Two API tests fail on Windows: symlink privilege and a naive time read as local
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-11-22T03:26:25Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/tests/test_video_media_branding.py
  - apps/api/tests/test_video_youtube_reports.py
---

# Two API tests fail on Windows: symlink privilege and a naive time read as local

## Why

Found 2026-11-22 while running the whole API suite on Windows 11 (UTC+8). Both fail the same way
on origin/main at 25fbefed5; everything else passed (8137), so a local full run is never green.

1. `test_video_media_branding.py::test_a_file_outside_the_branding_folder_is_never_served` creates
   a symlink, which Windows refuses without the privilege (WinError 1314).
2. `test_video_youtube_reports.py::test_a_first_run_schedules_the_jobs_and_keeps_every_report_as_youtube_wrote_it`
   expects `createdAfter` 14:00Z and gets 06:00Z. Probably SQLite hands the stored time back
   naive and `rfc3339` (`moment.astimezone(UTC)`) reads it as local time; not confirmed.

## Definition of done

- [ ] Both tests pass, or skip with a reason, on Windows in UTC+8, and still run on CI's Linux.

## Steps

- [ ] Skip the symlink test where a link cannot be made.
- [ ] Confirm the cause of the eight hours; restore UTC on load in the test as the Shorts tests do.

## How to verify

`cd apps/api && uv run pytest tests/test_video_media_branding.py tests/test_video_youtube_reports.py`

## Notes

If production code turns out to need the fix, widen the scope first (PostgreSQL returns aware times).
