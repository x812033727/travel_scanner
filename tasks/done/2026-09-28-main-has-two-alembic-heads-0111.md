---
id: 2026-09-28-main-has-two-alembic-heads-0111
title: Main has two alembic heads: 0111_video_story_series still revises 0108
status: done
priority: P0
area: api
owner: claude-opus-5-5
claimed_at: 2026-09-28T12:22:04Z
created_at: 2026-09-28T12:21:04Z
completed_at: 2026-09-28T12:22:52Z
branch: claude/fix-two-alembic-heads
depends_on: []
scope:
  - apps/api/migrations/versions/0111_video_story_series.py
---

# Main has two alembic heads: 0111_video_story_series still revises 0108

## Why

#912 merged `0109_video_shorts` (revises `0108_video_drama_messages`), then #910 merged
`0111_video_story_series`, which also revised `0108`. Its docstring said to set
`down_revision` to main's head when the PR left draft, and that step was missed. On main
`tests/test_schema.py` fails with "2 alembic heads", so the `api` check is red on every
pull request (seen on #917), and a deploy's `alembic upgrade head` would fail.

On 2026-09-28 production was at `0108_video_drama_messages (head)`, so neither migration had
been applied, and relinking is safe.

## Definition of done

- [x] `0111_video_story_series` revises `0109_video_shorts`, and the tree has one head.

## Steps

- [x] Change `down_revision` and the docstring's `Revises:` line.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_schema.py -q -p no:cacheprovider
```

## Notes

- The claim was forced. The migrations directory is in the scope of several open video
  tasks, and this one-line fix unblocks main for all of them.
- `#904` (`0109_video_flat_explainer`) now has to take 0112.
