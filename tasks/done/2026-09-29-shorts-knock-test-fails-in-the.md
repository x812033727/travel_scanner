---
id: 2026-09-29-shorts-knock-test-fails-in-the
title: Shorts knock test fails in the minutes before Pacific midnight
status: done
priority: P2
area: api
owner: claude-opus-merge-train
claimed_at: 2026-09-29T07:00:29Z
created_at: 2026-09-29T07:00:23Z
completed_at: 2026-09-29T07:00:38Z
branch: claude/brave-gauss-ra68mm
depends_on: []
scope:
  - apps/api/tests/test_video_shorts_publish.py
---

# Shorts knock test fails in the minutes before Pacific midnight

## Why

`test_a_knock_does_what_is_due_and_says_how_much` knocks at the real `now` and again five
minutes later, and expects the second knock not to run the daily check. The daily check is
keyed by the Pacific day (`VERIFIED_KEY` with `pacific_day`), so a CI run in the five minutes
before Pacific midnight put the two knocks on different days and the second one verified again:
`AssertionError: once a day` on #960's `api` job at 06:56 UTC (23:56 PDT), a tasks-only PR.

## Definition of done

- [x] The test passes whatever time of day it runs.

## Steps

- [x] Reproduce by pinning the `now` fixture to 23:57 Pacific: the test fails.
- [x] Move the test's `now` back ten minutes when the two knocks would straddle Pacific midnight.

## How to verify

`cd apps/api && uv run pytest -q tests/test_video_shorts_publish.py`, and once more with the
`now` fixture temporarily returning 23:57 America/Los_Angeles: 76 passed both times.

## Notes

Only this test compares two knocks across a day boundary; the rest of the file passed with the
pinned time too.
