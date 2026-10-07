---
id: 2026-10-07-a-paid-media-judge-or-locate-call
title: A paid media judge or locate call whose answer was lost is asked again
status: in-progress
priority: P3
area: tools
owner: claude-opus-5-5-media-judge
claimed_at: 2026-10-07T11:29:03Z
created_at: 2026-10-07T09:30:00Z
completed_at:
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

The media judge and locate routes take a Gemini call off the day's judge budget before they ask
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
    mid-call.
  - The cost is at most one more US$0.01-class Gemini call and one judge unit of the day.
  - The client already re-asks `video_media_judge_failed`, which may follow a call Gemini
    answered, so a second charge is accepted there already.
  - Option (a) would hold the call and stop the stage, and the worker would still ask again next
    round, so it would save little.
  - Option (a) (a lost answer of its own in the media forwarder, and a paid path in the client)
    is not done. The task's scope keeps those files in case the owner prefers it.
