---
id: 2026-10-07-a-paid-speech-request-the-limiter
title: A paid speech request the limiter refused (503 rate_limit_unavailable) is held as a lost answer
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T06:12:40Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
---

# A paid speech request the limiter refused (503 rate_limit_unavailable) is held as a lost answer

## Why

The API counts every video tool request on one token in the `video_tool` dependency
(`apps/api/app/video_speech/admin_api.py`, `enforce_named_rate_limit`), before any route body
runs. When Redis cannot count, `app/infra.py` refuses with 503 `rate_limit_unavailable`
("安全驗證服務暫時無法使用"): nothing reached a provider and nothing was charged.

`tools/video/tts/client.mjs` treats a paid POST's 5xx as uncertain unless its code is in
`SETTLED_CODES`, and `rate_limit_unavailable` is not there. So a `synthesize`, `synthesizeAligned`,
`transcribeClip`, `alignClip` or `judgeLines` that meets the limiter away throws `SPEECH_UNCERTAIN`
(exit 3): the narration's tts or a retake blocks for the owner, and the speech journal holds a
request that was never sent on. The worker's `everyones()` (`tools/video/automation/flow.mjs`)
already counts this sentence as everyone's trouble, but for tts only the status GET ever exits 4
with it. Found by the review of 2026-10-06-tts-and-a-narration-retake-that, with a probe through
the real client.

## Definition of done

- [ ] A paid speech POST answered 503 `rate_limit_unavailable` is retried like the 429 (it was
      refused before any provider call) and, when the retries run out, exits 4 with the API's
      sentence, so the worker defers the video as everyone's trouble.
- [ ] No other 503 changes: a 503 without that code is still uncertain on a paid POST.

## Steps

- [ ] Confirm in `apps/api/app/infra.py` and `apps/api/app/middleware.py` that every
      `rate_limit_unavailable` is raised before the route body; then add the code to the settled
      set (or handle it beside the 429), with a client test per paid call.

## How to verify

`node --test tools/video/tts/client.test.mjs`

## Notes

- Filed 2026-10-07 by claude-opus-5-5-tts-defer.
