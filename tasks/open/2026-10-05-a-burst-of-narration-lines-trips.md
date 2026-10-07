---
id: 2026-10-05-a-burst-of-narration-lines-trips
title: A burst of narration lines trips the speech route's 120-a-minute limit and blocks the video
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-speech-burst
claimed_at: 2026-10-07T04:33:16Z
created_at: 2026-10-05T23:43:19Z
completed_at:
branch: claude/happy-carson-c1hy91
depends_on: []
scope:
  - apps/api/app/infra.py
  - tools/video/tts/client.mjs
  - tools/video/tts/client.test.mjs
  - apps/api/app/video_speech/admin_api.py
  - apps/api/tests/test_video_speech.py
  - apps/api/app/video_speech/align_api.py
  - apps/api/tests/test_video_speech_align.py
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

- [x] A narration (or check-audio) run that goes over the per-token limit waits for the
      window and carries on, instead of failing the stage after about 31 seconds.
- [x] The 429 from the speech routes says how long to wait (`Retry-After`), or the client
      knows the window, and a test shows the client waiting it out.
- [ ] `openai-agent-posted-53-user-images` gets past "narration synthesized" after the fix is
      deployed (the owner presses retry once, or the worker retries it on its own), which also
      closes the last box of `2026-10-03-video-worker-narration-takes-made-stale`.

## Steps

- [x] (in part) Confirm which calls burst: count requests per minute in one long `tts` run with a fake
      transport (lines, retakes, the second transcriber, judge calls on the same token) and the
      two-lane case.
- [x] Choose the fix: `Retry-After` on the rate-limit 429 (the limiter knows the window), a
      client-side pace under 120 a minute, or both. Keep paid POSTs' journal rules: a 429 means
      the route refused before any provider call, so it is safe to send again.
- [x] Tests for the client (fake fetch: 429 with and without `Retry-After`) and for the API
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

## 2026-10-07 (claude-opus-5-5-speech-burst)

- Both fixes. API: `enforce_named_rate_limit` (`app/infra.py`) takes `retry_after=False`; with it
  the 429 carries `Retry-After` = the seconds left in the caller's fixed window (see the review
  note below for how it is read). The `video_tool` dependency
  passes it; the ~110 other callers are unchanged (default off, tested). Scope widened to
  `app/infra.py` for that one keyword.
- Client (`tools/video/tts/client.mjs`): a `Retry-After` is honoured up to the 60 s window as
  before; a 429 `rate_limit_exceeded` without one (a host from before this change) now waits the
  whole window instead of 1–16 s. A 429 is refused before any provider call, so resending is safe.
- The per-token minute is shared by every route on the `VideoTool` dependency (speech, reviews,
  Shorts, media, automation). The header helps every client that reads it: `media/client.mjs`
  and `automation/client.mjs` do; `review/sync.mjs` and `shorts/site.mjs` do too but cap it at
  30 s (`Math.min(... , 30)`), so a long Retry-After there is shortened. Not changed here.
- Burst: not measured on a real `tts` run; a client test simulates it instead (a fixed-window
  fake API at 3 a minute, ten paid syntheses, the clock moving only when the client sleeps): all
  ten go through after waiting the windows out.
- Verified: `node --test tools/video/tts/client.test.mjs tools/video/tts/tts.test.mjs` (42);
  the new client rows fail against the old client; `apps/api`: ruff, both mypy runs, and every
  test file touching the limiter or `video_tool` (64 files, 1532 pass, 84 skipped for Postgres).
- Left open: the production check (DoD 3) after a deploy, for the owner or the worker's retry;
  it also closes the last box of 2026-10-03-video-worker-narration-takes-made-stale.

## 2026-10-07 review (claude-opus-5-5-speech-burst)

An independent multi-lens review, each finding checked by two skeptics against a real
redis-server 7.0.15, confirmed these, all fixed in a second commit:

- Redis `TTL` rounds to the nearest second, so a client that waits exactly `Retry-After` came
  back up to half a second early, was refused again, and under half a second the code read 0
  as "unknown" and sent the whole window: an extra minute and a spent attempt about half the
  time. `_window_left` now reads `PTTL` and rounds up (1..window); a key already gone (-2) is
  1, since the window has just reset; no expiry (-1) or a Redis error is the whole window.
  Tests pin exact values (1400 ms -> 2, 300 ms -> 1, 12 300 ms -> 13, gone -> 1, down -> 60);
  the old tests accepted any value from 1 to 60.
- The hourly limits on `speech/transcribe` and `speech/align` (1200 an hour a token) sent the
  same 429 with no header, so the new 60 s fallback held a lane five minutes per call for a
  limit that lasts the hour. Both now send `Retry-After` (scope widened to `align_api.py` and
  its test), and the client throws at once on a rate limit whose `Retry-After` is past the
  minute: no retry this call can afford clears it. A header-less rate limit now really means a
  host from before this change.
- The client slept after its last attempt, then threw; that sleep is gone (60 s on an exhausted
  rate limit, up to 16 s elsewhere).
- The burst simulation passed against the old client because its fake always sent the header.
  It now also runs against a header-less fake (a host from before the change), which the old
  1-16 s backoff fails; the new hourly and trailing-sleep tests fail against both earlier
  clients.
- Not changed: the other clients (`automation`, `media`, `review/sync`, `shorts/site`) also sleep
  after their last attempt; with `Retry-After` on the token's minute that can be up to 60 s (30 s
  for the last two) before a single-attempt caller throws. One skeptic of two found the cost
  overstated (it predates this change and a one-try caller retries next round anyway); left as is.
