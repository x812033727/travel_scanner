---
id: 2026-11-01-let-the-daily-news-brief-run
title: Let the daily news brief run with the automatic drafts switched off
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-daily-brief
claimed_at: 2026-11-01T14:50:47Z
created_at: 2026-11-01T14:50:22Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/video_automation/daily_briefs.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/api/tests/test_video_daily_briefs.py
  - apps/api/tests/test_video_dub_retry.py
  - tools/video/automation/flow.mjs
  - tools/video/automation/cli.mjs
  - tools/video/automation/automation.test.mjs
  - apps/web/messages
  - docs/videos/AUTOMATION.md
---

# Let the daily news brief run with the automatic drafts switched off

## Why

The owner (2026-11-01) switched 「自動產生草稿」 (`enabled`) off and asked whether the daily AI
news brief still runs. It did not: `daily_briefs.next_request` returned nothing while `enabled`
was off, and the worker (`cli.mjs`, `flow.mjs stepUnit`) did nothing at all. The owner asked
for the brief to be independent of that switch.

## Definition of done

- [x] With `enabled` off and `daily_brief_enabled` on, the server files and hands out the day's
      brief, and the worker plans it and moves the `daily-ai-` videos through their stages and
      languages; every other video stays where it stands, and no draft, series, request or
      owner line is taken up.
- [x] With both off, nothing changes from before (Shorts and the Drive backup still run).
- [x] A daily brief's dub retry is allowed under the same rule (`_automation_enabled(session, slug)`).
- [x] The settings page's help text (five locales) and `docs/videos/AUTOMATION.md` say so.
- [ ] `.agents/skills/youtube-video/references/daily-brief.md` (and its `.claude` copy) say so too:
      left out of this task's scope because two in-progress tasks hold that directory.

## How to verify

```bash
cd apps/api && uv run pytest -q tests/test_video_daily_briefs.py tests/test_video_dub_retry.py
node --test tools/video/automation/automation.test.mjs tools/video/automation/cli.test.mjs
npm run check:i18n
```

## Notes

- Worker: `Automation.briefsOnly` and `scopedVideos()` in `flow.mjs`; bookkeeping (drops,
  retries, pasted addresses) is limited to the briefs while briefsOnly.
- The claim was forced: `flow.mjs`, `apps/web/messages` and `admin_service.py` are listed by many
  stale in-progress tasks, including `2026-10-29-daily-brief-on-the-host-worker`, whose
  feature has already landed.
