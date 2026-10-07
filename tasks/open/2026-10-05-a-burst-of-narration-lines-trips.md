---
id: 2026-10-05-a-burst-of-narration-lines-trips
title: A burst of narration lines trips the speech route's 120-a-minute limit and blocks the video
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-speech-burst
claimed_at: 2026-10-07T05:14:10Z
created_at: 2026-10-05T23:43:19Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - apps/api/app/video_speech/admin_api.py
  - apps/api/tests/test_video_speech.py
---

# A burst of narration lines trips the speech route's 120-a-minute limit and blocks the video

## Why

On production, the illustrated-slides video `openai-agent-posted-53-user-images` has been
blocked since 2026-10-04 13:13Z with `tts failed: 請求過於頻繁，請稍後再試`. That text is
the API's own rate-limit answer (`enforce_named_rate_limit` in `apps/api/app/infra.py`,
429 `rate_limit_exceeded`). The video tool token is limited to `SPEECH_REQUESTS_PER_MINUTE = 120`
requests a minute (`apps/api/app/video_speech/admin_api.py`, the `video_tool` dependency), and
the worker runs two lanes on one token.

The speech client in `tools/video/tts/client.mjs` does retry a 429, but `retryDelayMs` waits
1, 2, 4, 8 and 16 seconds (no `Retry-After` comes back with this 429), about 31 seconds in all,
which is shorter than the 60-second window the limit counts. So a long narration that sends
more than 120 requests inside a minute fails after five tries, and the worker reports the
video as blocked, needing the owner to press retry. Nothing is lost or paid twice, but a
video stops for a reason that would clear by itself a minute later.

## Definition of done

- [ ] A narration (or check-audio) run that goes over the per-token limit waits for the
      window and carries on, instead of failing the stage after about 31 seconds.
- [ ] The 429 from the speech routes says how long to wait (`Retry-After`), or the client
      knows the window, and a test shows the client waiting it out.
- [ ] `openai-agent-posted-53-user-images` gets past "narration synthesized" after the fix is
      deployed (the owner presses retry once, or the worker retries it on its own), which also
      closes the last box of `2026-10-03-video-worker-narration-takes-made-stale`.

## Steps

- [ ] Confirm which calls burst: count requests per minute in one long `tts` run with a fake
      transport (lines, retakes, the second transcriber, judge calls on the same token) and the
      two-lane case.
- [ ] Choose the fix: `Retry-After` on the rate-limit 429 (the limiter knows the window), a
      client-side pace under 120 a minute, or both. Keep paid POSTs' journal rules: a 429 means
      the route refused before any provider call, so it is safe to send again.
- [ ] Tests for the client (fake fetch: 429 with and without `Retry-After`) and for the API
      header.

## How to verify

`node --test tools/video/tts/client.test.mjs`; `cd apps/api && PYTHONUTF8=1 uv run pytest
tests/test_video_speech.py -q`; after a deploy, `/admin/videos` shows the video past
"narration synthesized".

## Notes

- Found 2026-10-06 by a read-only query of `video_projects` on production while closing
  `2026-10-03-video-worker-narration-takes-made-stale`: the video's checklist has
  `narration_synthesized: false` and the blocked reason above; the six other slides videos
  from that retry passed narration.
- The limit is per token, not per lane, so `VIDEO_WORKER_LANES: "2"` in
  `docker-compose.prod.yml` doubles the burst.
