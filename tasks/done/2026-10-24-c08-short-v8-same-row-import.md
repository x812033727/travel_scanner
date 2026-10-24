---
id: 2026-10-24-c08-short-v8-same-row-import
title: Preserve C08 episode identity during approved short-v8 import
status: done
priority: P2
area: api
owner: codex-c08-short-backend
claimed_at: 2026-10-24T05:27:30Z
created_at: 2026-10-24T05:15:06Z
completed_at: 2026-10-24T05:44:15Z
branch: codex/c08-kikkoman-canonical-preflight-20261024
depends_on: []
scope:
  - apps/api/app/video_automation/stories.py
  - apps/api/tests/test_video_story_import.py
---

# Preserve C08 episode identity during approved short-v8 import

## Why

The 20-row everyday story batch was imported with the historical C08 slug. The approved short-v8 video has a new top-level slug, but must update the existing paused/planned C08 episode row without adding episode 21, changing the other 19 rows, or deleting the historical project.

## Definition of done

- [x] A certified 20-row reimport reports `update=[C08]`, `create=[]`, and preserves the existing C08 row ID and original `VideoProject`.
- [x] The exception refuses a foreign old slug, an advanced row, and the importer retains its existing request and slug-conflict checks.
- [ ] Production dry-run and authorized import are separate later gates.

## Steps

- [x] Allow only the exact C08 old-to-short slug change on the existing review-only planned row.
- [x] Add in-memory DB dry-run/apply identity and refusal tests.

## How to verify

`cd apps/api; uv run pytest tests/test_video_story_import.py -q -p no:cacheprovider` (17 passed). The SQLite fixture is a local simulation, not a production DB dry-run.

## Notes

Precise stale-claim takeover: the overlapping `2026-10-18-story-thumbnail-brand` ticket was claimed on October 18, all steps were checked, its remote `claude/story-thumbnail-brand` branch no longer exists, and its PR #1568 merged October 18 at 13:43Z with these importer/test paths. The owner explicitly authorized `claim --force` for only `apps/api/app/video_automation/stories.py` and `apps/api/tests/test_video_story_import.py`; the old ticket and its other scope were not changed. The new C08 ticket now owns those two exact paths. No production connection or import was attempted.

The board also lists `2026-10-23-consolidate-x01-x20-brand-story-plans` on these two paths. Its source changes landed in merged PR #1799 at 2026-10-24 03:36Z, and `claude/pr-x-series-backend-deploy-9fe314` no longer exists remotely; the ticket stays open for its separate production import/readback. C08 adds only the exact C08 migration predicate and tests, does not change X-series behavior, and does not edit that ticket.

This ticket closes the locally tested importer implementation in PR #1811. The unchecked production dry-run and authorized import remain intentionally incomplete, with no production connection attempted. Before any future apply, read the live paused 20-row series and C08 planned row, run the current certified batch in dry-run, require `update=[C08]` and `create=[]`, then obtain the separate import authorization and verify the same row ID afterward.
