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

- First automatic run (`daily-ai-20261029`, the news of 10-29). Times are Asia/Taipei, read on
  10-30 through the tool token's video list and reviews:
  - The brief was switched on 10-29 at about 20:15. The day already queued for 10-28 (episode 1,
    made by hand) was skipped by #1921.
  - At 09:02:58 Jev approved the outline automatically: plan A, stance 0.72, advice 0.02, demo
    not asked.
  - At 09:14 the project was at `fact-checked`.
  - At 12:00 it was not ready: stage `retrying` (last update 11:33), narration not yet
    synthesized, and the retry request acknowledged by the worker. The likely cause is the
    Gemini speech daily quota (429): the session dubbed episode 1 in eight languages through the
    night and morning before. This was inferred, and it was wrong: see the next bullet.
  - The real cause, found in the owner's host logs at 16:15: after the 11:33 retry, the
    storytelling panel said no and sent the script back. The rewrite is a durable writer job of
    about 2.5 minutes, which outlasts one round. Each next round read the panel again, the new
    note made a new writer request, and the finished rewrite before it was archived unread. The
    worker logged `writer is still running` every six minutes, and `video-ai-worker` finished a
    new job every six minutes. Fixed in `narrativeGate` (`tools/video/automation/flow.mjs`): the
    note is saved as `fix_note` in `review/narrative.json`, and while the script is still the one
    the panel read, the same note is sent again so the saved receipt is taken.
  - The storytelling-panel loop was fixed by #1935. After the owner's second retry the brief
    passed the panel (10-30 20:51) and reached its final cut, but in the dark default look with
    no key band: `DAILY_BRIEF_RULES` replaces the tutorial rules that carry the paper theme and
    `keys`. #1936 settles every brief on paper and redrew this one (final card 10-31 00:27).
  - The owner then saw a big card's second line cut off "under the white band": a card column
    squeezed by flex cut its last line while fitText let up to 0.4 em through. #1937 fixed the
    fit and redrew the brief (final card 02:24). The owner approved it at 03:05.
  - Upload package by 03:32. The eight locales then took until about 10:15 (one locale an hour),
    and the brief was ready to upload only after that, past the 12:00 publish the format plans.
  - Why the languages took seven hours: each locale is about five units, each translated and
    then reviewed, some 80 durable requests in a row. A request polls 25 s, a unit's job takes
    about a minute and a half, so every request waited for the next round (the 300 s sleep plus
    the recheck), about six minutes each. The worker now waits for its durable jobs in the same
    run, 45 s at a time and at most 15 minutes of sleep per run (`tools/video/automation/cli.mjs`
    `DURABLE_WAIT_MS`, `MAX_RUN_WAIT_MS`), which should bring the batch to two or three hours.
  - The 10-30 brief started at 09:00 while the 10-29 languages still ran on the same one-consumer
    `video-ai` queue; its verifier (not a durable stage) met a 504 at 09:51 and stopped as
    uncertain until the owner retried. Making the verifier durable is a separate question.
  - 10-31: both briefs were then deferred again and again as "Gemini busy" from about 09:00 to
    18:30. The real stall was the month's draft cap (60 of 60, `max_drafts_per_month` cannot go
    past 60): the server answered every daily request with `video_ai_budget_exhausted`, a
    run-ending code, so each run (`auto exited with 3` every five minutes) ended before any video
    already in progress was stepped. The owner set the draft interval to 720 hours as a stopgap;
    #1956 makes a spent cap pause new drafts until the next month while the rest goes on. Set the
    interval back after it is deployed.
  - The 10-29 dubs (all eight locales ticked at the final approval) finished and the brief was
    ready to upload on 10-31 at 20:25, about 35 hours after it started.
  - The 10-30 brief reached `frames rendered` at 20:27 and stopped: "render failed: 6 layout
    problems". #1937's check now refuses card text under the key band, but the worker blocked on
    any render failure, so a retry drew the same six cards. The worker now sends the refused
    cards back to the writer for their `data` alone (`fixLayout`, `withCardText`: the narration
    hash cannot change), at most `MAX_PROMPT_FIX_ROUNDS` rounds, then to the owner.
- Lesson: never run a hand dubbing batch on the morning of a brief. Gemini's daily speech quota
  resets around 15:00 Taipei, and the 09:00 brief needs it for its narration. Dub after 15:00, or
  finish the evening before.

- `next` answers `{"request": null}` when nothing is due (the slides queue's shape); the worker's
  `dailyNext` also accepts a bare request or 404.
- Dubs are ticked from `video_youtube/sync.py` `_finish` after a successful site send, not when
  the id first appears (mid-sync a changed language choice would fail the scheduling step). A
  brief whose URL is pasted by hand keeps captions only.
- No admin page lists the daily requests yet (API only: `GET /admin/video-automation/daily-briefs`).
