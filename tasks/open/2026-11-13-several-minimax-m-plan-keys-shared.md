---
id: 2026-11-13-several-minimax-m-plan-keys-shared
title: Several MiniMax M Plan keys shared out by busy and quota
status: in-progress
priority: P2
area: api
owner: claude-opus-session-41c1d91a
claimed_at: 2026-11-13T07:01:42Z
created_at: 2026-11-13T07:01:25Z
completed_at:
branch: claude/minimax-key-pool
depends_on: []
scope:
  - apps/api/app/ai/minimax_pool.py
  - apps/api/app/config.py
  - apps/api/app/admin/service.py
  - apps/api/app/video_media/jobs.py
  - apps/api/app/video_speech/admin_api.py
  - apps/api/app/video_speech/schemas.py
  - apps/api/tests/test_minimax_pool.py
  - apps/api/tests/test_video_media_jobs.py
  - apps/web/components/admin-settings-panel.tsx
  - apps/web/messages/en/admin.json
  - apps/web/messages/ja/admin.json
  - apps/web/messages/ko/admin.json
  - apps/web/messages/zh-CN/admin.json
  - apps/web/messages/zh-TW/admin.json
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# Several MiniMax M Plan keys shared out by busy and quota

## Why

The owner (2026-11-13) has more than one MiniMax M Plan account and wants the site to spread
its MiniMax calls across them: when account A is busy the next call goes to B, the one with
more of its plan window left is preferred, and a used-up account rests until it resets. Both
the site's own text AI and the video tools' media and speech (through the video tool token)
should do this.

## Definition of done

- [x] Admin, AI 供應商與金鑰: a secret field `minimax_api_keys_extra` (comma separated) beside
      `minimax_api_key`. One key behaves exactly as before and never touches Redis.
- [x] `app/ai/minimax_pool.py` ranks keys by resting, used up, in-flight leases, plan left
      (bands of 20 points, `general` or `video` bucket of `GET /v1/token_plan/remains`, kept 5
      minutes) and least recently picked. Redis failures fall back to the first key.
- [x] Video media (images, music, clips) lease a key per job; a clip keeps the key's fingerprint
      in its request and polls on it; a refusal of kind `key` (plan or balance) or `busy`
      (not for pilot films) rests that key and tries the next.
- [x] MiniMax speech leases a key per call and moves on after a 429 or 402 refusal; the quota
      endpoint lists every key (`accounts`).
- [x] Text AI: `load_runtime_settings` puts the pool's pick in `minimax_api_key` when there are
      extra keys, so planner, parser, guide search/review, intros, news and video stages spread.
- [ ] Deployed, the owner adds the second key, and two parallel jobs are seen on two keys.

## How to verify

```bash
cd apps/api && uv run pytest -q tests/test_minimax_pool.py tests/test_video_media_jobs.py
npm run check:i18n
```

## Notes

- The remains answer (read through the video tool token 2026-11-13) has `model_remains[]` with
  `model_name` `general` (5-hour interval) and `video` (24-hour), each with
  `current_interval_remaining_percent`, `current_weekly_remaining_percent`, `end_time`,
  `weekly_end_time` (ms). No page publishes these names, so a missing field ranks as 50%.
- Text calls do not take leases (the providers are built synchronously), so they spread by plan
  left and turn-taking only; a key MiniMax refuses for a text call is not rested until the next
  quota read shows it used up.
- Extra keys need the first key set; a site with only extra keys reads as not configured.
- The five admin.json are bound by the duration review (docs/videos/long-form): an independent
  reviewer agent rebound them (PASS, DURATION_ONLY) after the new copy turned web-checks red.
- Whether MiniMax's terms allow one person several M Plan accounts was not checked.
