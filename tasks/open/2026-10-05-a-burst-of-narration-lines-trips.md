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
  - apps/api/app/infra.py
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

- [x] Confirm which calls burst: count requests per minute in one long `tts` run with a fake
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
- 2026-10-07 (claude-opus-5-5-speech-burst). What bursts, from three read-only investigations that
  ran the real CLIs against a fake fetch, a virtual clock and the API's fixed-window limiter:
  - Every speech command sends its requests one at a time; the only concurrency is the worker's
    two lanes on one token (`automation/cli.mjs` `Promise.all(lanes.map(drive))`).
  - One lane goes over 120 a minute only when each answer takes under about 0.5 s. With instant
    answers, a long slides tts (sothatswhy-t26, 169 requests) sends its 121st request at 3 s and
    fails with the production message. At a second or more per request, one lane runs at 60 a
    minute or less.
  - The window is not the speech routes' alone. `video_tool` guards about 56 routes in 8 modules
    (automation runs and their job polls, media, reviews, Shorts), all counted in
    `video_speech:<token id>`. So the production failure most likely needed both lanes and the
    other traffic, not one tts.
  - The client gave up because its five requests all went out within about 15 s of the first 429
    (+0, 1, 3, 7, 15), while a fixed window can stay spent for up to 60 s.
- The fix:
  - `app/infra.py` `enforce_named_rate_limit(..., retry_after=True)`: on a refusal it reads the
    window key's `PTTL` (only then, so an allowed hit costs nothing more) and sends
    `Retry-After`, rounded up so a caller is never early. A key already gone sends 1. A key
    without an expiry, or a read that fails, sends the whole window. The refusal stays the 429 it
    is; the 503 is still only for a count that could not be made.
  - It is opt-in. The token window in `video_tool`, transcribe's hourly window and align's
    hourly window use it; the other ~90 callers (login, password reset, public reads) answer
    exactly as before. Opting them in would change other clients: the automation client keeps a
    refusal's Retry-After and defers no sooner than it.
  - `tools/video/tts/client.mjs`:
    - Retry-After is honoured as sent, no longer cut to 60 s.
    - A 429 `rate_limit_exceeded` without the header (a host from before it) waits one whole
      window, 61 s, instead of 1, 2, 4, 8 s.
    - A wait over 90 s (the hourly limits, a provider's long quota) is told at once, as the
      service's (exit 4), instead of five refusals in a row.
    - Nothing sleeps after the last attempt (the old 16 s there was wasted).
    - Attempts stay at 5, so a window kept full by others still fails after at most 4 × 61 s.
- Tests:
  - `client.test.mjs`: every call (the four paid ones, status, align) waits Retry-After, a whole
    window without it, past the old 60 s cap, and on a date header. A limit that keeps refusing
    makes 5 calls with 4 window waits, as the service's and never SPEECH_UNCERTAIN. The 90 s
    boundary. Other backoffs. The speech journal: a refused narration is sent again, and one
    refused to the end leaves no entry to hold.
  - `test_video_speech.py`: the real `video_tool` limiter answers `Retry-After: 43` for 42.3 s
    left. Every PTTL answer (-2, -1, RedisError, past the window). The default stays header-less
    with no extra read. The three speech limits opt in.
  - The first four client tests fail on the old client.
- Left for later, not in this scope:
  - A tts or retake that exits 4 still blocks the video (`flow.mjs`), where check-audio, dub and
    media defer. That is `2026-10-06-tts-and-a-narration-retake-that`.
  - A worker restart during one of these waits leaves the journal entry `sent`, which the next
    run holds as SPEECH_UNCERTAIN although the 429 proved nothing ran. The waits are now up to
    61 s each instead of 1–16 s. Filed as `2026-10-07-a-speech-request-waiting-out-a`.
  - A STOP file is read between requests, so in a throttled run it now takes up to about four
    minutes to act.
