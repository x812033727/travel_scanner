---
id: 2026-10-07-the-media-automation-review-and-shorts
title: The media, automation, review and Shorts clients sleep after their last attempt, now as long as the server's Retry-After
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T07:11:49Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/media/client.mjs
  - tools/video/automation/client.mjs
  - tools/video/review/sync.mjs
  - tools/video/shorts/site.mjs
---

# The media, automation, review and Shorts clients sleep after their last attempt, now as long as the server's Retry-After

## Why

Every route a video tool token calls answers its rate limit (`apps/api/app/video_speech/admin_api.py`
`video_tool`, 120 a minute per token) with `Retry-After`, the seconds until the window opens again,
since `2026-10-05-a-burst-of-narration-lines-trips`. `tools/video/tts/client.mjs` stopped sleeping
after its last attempt in that ticket. The other clients still sleep once more after the final
refusal before they throw:

- `tools/video/media/client.mjs` `call()`: up to 60 s, where the old backoff wasted 16 s;
- `tools/video/automation/client.mjs` `request()`: up to 60 s (it caps the header at 120), where it
  wasted 40 s;
- `tools/video/review/sync.mjs` and `tools/video/shorts/site.mjs`: up to 30 s, where they wasted 8 s.

Nothing is sent or paid twice. The cost is up to a minute per exhausted call before the caller
learns the outcome, and a STOP file that waits as long.

## Definition of done

- [ ] None of the four clients sleeps after its last attempt; each throws the last error at once.

## Steps

- [ ] Add `if (attempt === attempts - 1) throw last;` (or `break`) before each retry sleep,
  network errors included.
- [ ] Update any test that counts the sleeps, so it pins one sleep fewer.

## How to verify

`node --test tools/video/media/*.test.mjs tools/video/automation/client.test.mjs tools/video/review/sync.test.mjs tools/video/shorts/site.test.mjs`.

## Notes

- Found by the review of `2026-10-05-a-burst-of-narration-lines-trips` (2026-10-07). The reviewer ran
  the media client against five 429s with `Retry-After: 60`: it slept 60 s five times, the last one
  after the final refusal.
