---
id: 2026-10-07-a-paid-media-judge-or-locate-call
title: A paid media judge or locate call whose answer was lost is asked again
status: done
priority: P3
area: tools
owner: claude-opus-5-5-media-judge
claimed_at: 2026-10-07T11:29:03Z
created_at: 2026-10-07T09:30:00Z
completed_at: 2026-10-07T11:46:02Z
branch:
depends_on: []
scope:
  - apps/web/app/api/video/media/[...path]/forward.ts
  - apps/web/app/api/video/media/[...path]/route.test.ts
  - tools/video/media/client.mjs
  - tools/video/media/media.test.mjs
  - docs/videos/DRAMA.md
---

# A paid media judge or locate call whose answer was lost is asked again

## Why

The media judge and locate routes take a Gemini call off the month's judge budget before they ask
Gemini. `apps/web/app/api/video/media/[...path]/forward.ts` answers 502 `upstream_unavailable`
both for an API it never reached and for a request it sent whose answer never came back: its
180 s abort, or a reset after the request went out. `tools/video/media/client.mjs` sends a 502
again. So a call that may already have been answered, and charged, is asked a second time. Its
first budget unit is also never released.

How likely this is depends on the settings. With the defaults, the 180 s abort comes after the
API's own Gemini timeout (`video_speech_gemini_timeout_seconds`, 150), so the API answers
`video_media_judge_failed` first. The realistic path is the API or the web container restarting
while a call is in flight. The cost is one extra judge unit and possibly one more ~US$0.01 call.

## Definition of done

- [x] Choose and record one of these:
  - A lost judge or locate answer is told apart from an API never reached, and is sent once.
  - The extra unit and call are accepted, and written down where the drama costs are.

## Steps

- [ ] Option (a): give the media forwarder a lost answer for judge and locate, as
  `apps/web/app/api/video/speech/forward.ts` does: a 504 with its own code after the request went
  out, keeping 502 `upstream_unavailable` for connect failures. Then the media client sends
  those calls once, and asks again only on the route's 502, `video_media_judge_failed` or
  `video_media_locate_failed`.
- [x] Option (b): record in `docs/videos/DRAMA.md` that a mid-call restart may cost one more
  judge unit. The media client already retries `video_media_judge_failed`, which accepts a
  second Gemini charge after an httpx timeout.

## How to verify

`node --test tools/video/media/*.test.mjs` and the web route tests for the media forwarder.

## Notes

- Found by the review of `2026-10-07-automation-client-settles-a-judge-route` (2026-10-07), as a
  nit outside that task's client.
- 2026-10-07 (claude-opus-5-5-media-judge). Chose option (b), and recorded it in
  `docs/videos/DRAMA.md` §先預留、後對帳 (the judge bullets) and in a comment by the media
  client's `RETRYABLE_CODES`. The reasons:
  - The event is rare. With the defaults the API's own Gemini timeout (150 s) answers
    `video_media_judge_failed` before the route's 180 s abort, so the real trigger is a restart
    mid-call. That holds while `video_speech_gemini_timeout_seconds` (allowed up to 280 s) stays
    under the route's fixed 180 s; above it, every slow call meets the route's abort first.
  - The cost of a restart is one more US$0.01-class Gemini call and one judge unit of the month
    for each call in flight.
  - The client already re-asks `video_media_judge_failed`, which may follow a call Gemini
    answered, so a second charge is accepted there already.
  - Option (a) would hold every lost answer for the owner: the stage would exit 3 and the video
    would be blocked as `media_owner`, for an event that costs about a cent.
  - Option (a) (a lost answer of its own in the media forwarder, and a paid path in the client)
    is not done. The task's scope keeps those files in case the owner prefers it.
- Review (2026-10-07, each finding verified), fixed in the docs and the comment:
  - The judge budget is monthly (`apps/api/app/video_media/meter.py`), not daily.
  - "At worst one more call" was wrong for a question that keeps failing. `call()` sends up to
    5 times a run, and each send may be charged. The stage exits 4, which is not everyone's
    trouble, so the worker defers it and blocks it after `DEFER_LIMIT` (6): 7 runs × 5 sends,
    about 35 calls (~US$0.35) for one stuck question. The calls that failed are not in the
    video's ledger (`Stage.judge` books a call once it answered), so the per-video cap does not
    see them.
  - A website restart reaches the tool as nginx's 502 or a dropped connection. `call()` asks
    again on every 5xx and network error whatever the code, so the comment now says a paid
    send-once needs its own path in `call()`; taking a code out of `RETRYABLE_CODES` would not
    do it.
