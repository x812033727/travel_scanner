---
id: 2026-10-04-news-ops-skill-says-a-spent
title: news-ops skill says a spent Jev budget holds candidates as uncertain duplicates
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-04T15:27:46Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/prod-host-ops/references/news-ops.md
  - .claude/skills/prod-host-ops/references/news-ops.md
---

# news-ops skill says a spent Jev budget holds candidates as uncertain duplicates

## Why

The host-operations skill's news troubleshooting list (`news-ops.md`, item 3 under the
symptoms, both copies) still says that when `jev_daily_call_budget` is spent the duplicate
check always answers "uncertain", so many candidates land in manual review. Since #829
(2026-09-27) the pipeline sends such a candidate back to `discovered` as `news_jev_quota_paused`
instead (`apps/api/app/news_automation/pipeline.py`, the `quota_unavailable` branch after
`jev_duplicate_check`), and it is queued again as soon as the budget has room
(`tasks/done/2026-09-27-resume-jev-paused-news-candidates-as.md`). The production budget was
raised from 200 to 5,000 that day. An operator who follows the skill looks for uncertain
duplicates that no longer appear and misses the paused ones. `docs/news-automation.md` was
corrected by `2026-10-03-jev-comments-drifted-from-vendor-docs`; the skill was outside that
ticket's scope.

## Definition of done

- [ ] Item 3 describes the paused state (`news_jev_quota_paused`, back in `discovered`, runs
      again after 00:00 UTC or as soon as a raised budget has room) and points to
      `docs/news-automation.md` §When Jev's daily budget is spent instead of repeating it.
- [ ] Both copies stay byte-identical.

## Steps

- [ ] Edit `.agents/skills/prod-host-ops/references/news-ops.md` and copy it to
      `.claude/skills/prod-host-ops/references/news-ops.md`.

## How to verify

```bash
node --test tools/skills.test.mjs
```

## Notes

- Found while closing `2026-10-03-jev-comments-drifted-from-vendor-docs` on 2026-10-04.
