---
id: 2026-10-04-news-ops-skill-says-a-spent
title: news-ops skill says a spent Jev budget holds candidates as uncertain duplicates
status: done
priority: P3
area: docs
owner: claude-opus-5-5-incomplete-tickets
claimed_at: 2026-10-04T17:43:06Z
created_at: 2026-10-04T15:27:46Z
completed_at: 2026-10-04T17:43:08Z
branch: claude/news-ops-jev-paused
depends_on: []
scope:
  - .agents/skills/prod-host-ops/references/news-ops.md
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

- [x] Item 3 describes the paused state (`news_jev_quota_paused`, back in `discovered`, runs
      again after 00:00 UTC or as soon as a raised budget has room) and points to
      `docs/news-automation.md` §When Jev's daily budget is spent instead of repeating it.
- [x] Both copies stay byte-identical (there is only one: see Notes).

## Steps

- [x] Edit `.agents/skills/prod-host-ops/references/news-ops.md` and copy it to
      `.claude/skills/prod-host-ops/references/news-ops.md`.

## How to verify

```bash
node --test tools/skills.test.mjs
```

## Notes

- Found while closing `2026-10-03-jev-comments-drifted-from-vendor-docs` on 2026-10-04.
- 2026-10-04 (claude-opus-5-5-incomplete-tickets): item 3 now names `news_jev_quota_paused`, says the
  candidate is back in `discovered` and is queued again after 00:00 UTC or at once when a raised
  budget has room, points at `docs/news-automation.md` "When Jev's daily budget is spent", and
  says what a real `news_duplicate_uncertain` is (Jev answered between 0.25 and 0.85,
  `news_automation/ai.py`).
- There is no `.claude/skills/prod-host-ops/references/news-ops.md`: only SKILL.md is mirrored
  under `.claude/skills` (`tools/skills.test.mjs`; PR #1222 makes that a test), so that scope
  line was dropped.
- Claimed with `--force` over `2026-10-04-resume-held-news-drafts-from-their`
  (claude-opus-5-5-news-resume, review): its file changes landed as #1212 and what is left
  there is the deploy and the production pilot; this change is one line in item 3, outside the
  resume section it added.
