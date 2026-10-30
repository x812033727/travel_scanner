---
id: 2026-10-29-daily-brief-on-the-host-worker
title: Daily brief on the host worker: daily request, Jev gates, eight-language captions and dubs
status: in-progress
priority: P1
area: api
owner: claude-opus-5-5
claimed_at: 2026-10-29T09:42:05Z
created_at: 2026-10-29T09:41:55Z
completed_at:
branch: claude/daily-news-brief
depends_on: []
scope:
  - apps/api/app/video_automation
  - apps/api/migrations/versions/0143_video_daily_brief_requests.py
  - apps/api/tests/test_video_daily_briefs.py
  - apps/api/tests/test_migration_0143_video_daily_brief_requests.py
  - apps/api/app/video_reviews/admin_service.py
  - apps/web/app/api/video/automation/daily-briefs
  - tools/video/automation
  - .agents/skills/youtube-video/references/daily-brief.md
  - docs/videos/AUTOMATION.md
  - docs/videos/HANDS-OFF.md
  - docs/videos/LANGUAGES.md
  - apps/api/app/video_youtube/sync.py
  - apps/web/components/admin-video-settings.tsx
  - apps/web/components/admin-video-settings-tutorial.tsx
  - apps/web/components/admin-video-settings.test.tsx
  - apps/web/messages
  - tools/video/review/sync.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Daily brief on the host worker: daily request, Jev gates, eight-language captions and dubs

## Why

The owner wants the daily AI/tech brief fully hands-off (2026-10-29): the host worker starts at
09:00 Taipei from the previous day's published ai-news and tech-news articles, Jev decides the
outline and every gate, narration, eight-language titles/captions and dubs follow, and it goes up
at 12:00. A video pushed by hand from a session waits for the owner at every gate (owner rule
2026-10-17), so the brief has to be made by the worker. Owner decisions: if Gemini's voice quota
is out in the morning, publish later; click "upload" once a day to schedule noon; upload the
eight dub tracks in Studio in the afternoon (YouTube's API has no audio-track upload).

## Definition of done

- [x] Server: `video_daily_brief_requests` (migration 0143), settings `daily_brief_*`, worker
      endpoints `daily-briefs/next|start|done`, admin list, settings panel (five locales).
- [x] Outline auto-pick does not ask a `daily-ai-` slug for a demonstration.
- [x] Languages: titles/captions in eight languages decided at final approval (no dub, so the
      batch auto-approves); dubs ticked once the site's YouTube send has finished.
- [x] Worker: daily branch ahead of other new work (not gated by `room()`, no draft-cap count),
      `daily` prompt variants, fixed slug, no `source_guide`, `dailyDone` on upload confirm.
- [x] Gemini busy (429) waits without counting toward a video's block.
- [ ] Deployed; Gemini monthly limit checked: production already has 10,000,000 on the admin card 「Azure 語音（影片旁白）」 (`video_speech_gemini_monthly_character_limit`, 5.65M used on 2026-10-29), so it stays; lowering it to 1,500,000 would stop all narration;
      `daily_brief_enabled` on; first run watched and its timings written here.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_video_daily_briefs.py tests/test_migration_0143_video_daily_brief_requests.py -q
node --test tools/video/automation/*.test.mjs
```

## Notes

- `next` answers `{"request": null}` when nothing is due (the slides queue's shape); the worker's
  `dailyNext` also accepts a bare request or 404.
- Dubs are ticked from `video_youtube/sync.py` `_finish` after a successful site send, not when
  the id first appears (mid-sync a changed language choice would fail the scheduling step). A
  brief whose URL is pasted by hand keeps captions only.
- No admin page lists the daily requests yet (API only: `GET /admin/video-automation/daily-briefs`).
