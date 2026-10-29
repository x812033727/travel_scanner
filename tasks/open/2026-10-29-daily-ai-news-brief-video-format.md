---
id: 2026-10-29-daily-ai-news-brief-video-format
title: Daily AI news brief video: format and one-week trial
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5
claimed_at: 2026-10-29T04:05:06Z
created_at: 2026-10-29T04:04:37Z
completed_at:
branch: claude/daily-news-brief
depends_on: []
scope:
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos/daily-ai
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Daily AI news brief video: format and one-week trial

## Why

The owner wants a daily video of about ten minutes that covers the previous day's AI and
technology news (2026-10-29), as fully automated slides, tried for one week (five episodes,
Monday to Friday) and made by an agent in a session before any host-worker work. The video
rules say one story per video, and the blind storytelling panel's required questions
(one_line, one_thread, no_toc, no_detour) fail a five-to-eight story roundup by design.

## Definition of done

- [x] A `daily-ai-` slug reads the storytelling panel in brief wording: same ids, same
      required flags (`DAILY_BRIEF_PANEL_QUESTIONS`, `isDailyBrief`), its own contract hash.
- [x] `references/daily-brief.md` and `scripts/daily_news_pick.mjs` written; SKILL.md
      (both copies) points to them and names the brief as rule 11's only exception.
- [ ] Episode 1 made and shown to the owner (lint 0 errors, qa passes, panel passes).
- [ ] Episodes 2-5 made; a week after upload, watch time, CTR and retention written here.

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs tools/video/long-form/review.test.mjs
node .agents/skills/youtube-video/scripts/daily_news_pick.mjs --date 2026-10-28
```

## Notes

- Editing SKILL.md makes the long-form duration receipt stale; a separate pass reviewed the
  two copies (DURATION_ONLY PASS, `docs/videos/long-form/review.md` "Daily AI brief
  increment").
- Production from a cloud session needs the owner to approve a `cli.mjs login` pairing link
  once; the channel intro/outro package is not in git, so episodes made here have none
  unless `branding --install` can fetch it. Hand-pushed videos wait for the owner at every
  gate.
- Run `npm ci` at the root before `npm run test:tools` or `cli.mjs login`: without it the
  tool tests fail by the dozen (missing `pinyin-pro` and others) and hide real failures.
- `tools/skills.test.mjs` refuses repository paths that do not exist yet and machine paths
  (`mokaair-work`): write `docs/videos/<slug>/` and `<VIDEO_WORKDIR>/<slug>/` in a skill.
