---
id: 2026-10-07-the-speech-and-shorts-clients-hold
title: The speech and Shorts clients hold the API's 503 rate_limit_unavailable as uncertain, though nothing ran
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-limiter-503
claimed_at: 2026-10-07T10:44:14Z
created_at: 2026-10-07T09:30:00Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - tools/video/shorts/site.mjs
  - tools/video/shorts/site.test.mjs
---

# The speech and Shorts clients hold the API's 503 rate_limit_unavailable as uncertain, though nothing ran

## Why

Every route a video tool token calls goes through `video_tool`
(`apps/api/app/video_speech/admin_api.py`). Its first check is the token's rate limit,
`enforce_named_rate_limit` in `app/infra.py`. When Redis cannot count the call, that answers 503
`rate_limit_unavailable` before any provider, Jev or model call.

`tools/video/tts/client.mjs` treats any paid 5xx it does not list as settled as
`SPEECH_UNCERTAIN`. So a narration line, a transcription or a Jev check that met this 503 is held
for the owner (exit 3), and the video is blocked until someone runs `speech-journal.mjs forget`.
`tools/video/shorts/site.mjs` does the same for a Short's policy judgement. The request never
reached a provider. A Redis restart during a deploy, while a worker round is running, is enough.

`tools/video/automation/client.mjs` settles this answer since
`2026-10-07-automation-client-settles-a-judge-route` (its `NEVER_RAN`).

## Definition of done

- [x] A paid speech, transcription, Jev or Shorts judgement request answered 503
  `rate_limit_unavailable` is asked again within the client's attempts, then told as the
  service's (exit 4). The same code with any other status still holds.

## Steps

- [x] Add `{ status: 503, code: "rate_limit_unavailable" }` beside each client's `NEVER_REACHED`,
  checked by its `settled()`, with a comment naming where the API answers it.
- [x] Tests: the 503 is sent again, and the code with another status is held.

## How to verify

`node --test tools/video/tts/client.test.mjs tools/video/shorts/site.test.mjs`.

## Notes

- Found by the review of `2026-10-07-automation-client-settles-a-judge-route` (2026-10-07).
- `rate_limit_unavailable` is answered only by `enforce_named_rate_limit`. On the video tool
  routes that runs in `video_tool` before every handler, and again as the first statement of
  the handlers that have their own limit.
- 2026-10-07 (claude-opus-5-5-limiter-503). `tts/client.mjs` and `shorts/site.mjs` replace
  `NEVER_REACHED` with `NEVER_RAN`, a list of answers that say nothing ran, each with its own
  status: the routes' 502 `upstream_unavailable` and the API's 503 `rate_limit_unavailable`.
  `settled()` checks both, as `automation/client.mjs` does. A settled 503 is retried within the
  attempts (any 5xx is retryable), then told as the service's. Through the speech journal, a
  settled error removes the entry, so the next run sends it.
- Tests: the settled tables of both clients gain the 503 (sent again, for all four paid speech
  calls and for the policy judgement), and their lost tables gain the code at a 500 (sent once,
  held). The settled rows fail on the old code. The lost rows pass on both, since they pin the
  side that stays. Accepting the code at any status fails a test in each client.
