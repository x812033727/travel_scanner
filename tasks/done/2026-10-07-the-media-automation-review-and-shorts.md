---
id: 2026-10-07-the-media-automation-review-and-shorts
title: The media, automation, review and Shorts clients sleep after their last attempt, now as long as the server's Retry-After
status: done
priority: P3
area: tools
owner: claude-opus-5-5-last-sleep
claimed_at: 2026-10-07T09:21:02Z
created_at: 2026-10-07T07:11:49Z
completed_at: 2026-10-07T10:24:44Z
branch:
depends_on: []
scope:
  - tools/video/media/client.mjs
  - tools/video/media/media.test.mjs
  - tools/video/automation/client.mjs
  - tools/video/automation/client.test.mjs
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
  - tools/video/shorts/site.mjs
  - tools/video/shorts/site.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
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

- [x] None of the four clients sleeps after its last attempt; each throws the last error at once.

## Steps

- [x] Add `if (attempt === attempts - 1) throw last;` (or `break`) before each retry sleep,
  network errors included.
- [x] Update any test that counts the sleeps, so it pins one sleep fewer.

## How to verify

`node --test tools/video/media/*.test.mjs tools/video/automation/client.test.mjs tools/video/review/sync.test.mjs tools/video/shorts/site.test.mjs`.

## Notes

- Found by the review of `2026-10-05-a-burst-of-narration-lines-trips` (2026-10-07). The reviewer ran
  the media client against five 429s with `Retry-After: 60`: it slept 60 s five times, the last one
  after the final refusal.
- 2026-10-07 (claude-opus-5-5-last-sleep). Each of the four loops checks for its last attempt
  before the sleep, in the network branch as well as after a refusal: the media client's
  `call()`, the automation client's `request()`, the review client in `sync.mjs` (its four
  attempts are now `ATTEMPTS`) and the Shorts `siteClient`. Each throws the last error at once.
- Scope: the four clients' tests. `review/sync.mjs` and `sync.test.mjs` are bound by the
  duration-review receipt, so `docs/videos/long-form/review.*` takes the independent re-bind.
- Tests, each failing on the old code:
  - automation: the generic-failure and Retry-After tests pin one sleep fewer, and a new test
    covers a site that stays unreachable (network branch);
  - media: a new test, five refusals (a 429 with `Retry-After: 60`) and five refused
    connections, each giving four waits;
  - Shorts: the same with four attempts;
  - review: the push-failure table now counts waits as attempts minus one, network included.
  - Removing the automation network guard fails its new test.
- Review (2026-10-07, two lenses, each finding verified): no defects. It replayed 31 answer
  sequences against every client and route shape, at one to five attempts: 1,674 cases. Old and
  new send the same requests and throw the same error (class, message, status, code, `who`,
  `retry_after`, `submission`). The only difference is the final sleep. It traced every caller
  with fewer attempts (the Shorts lab's `subjectApi`, `renewal.mjs`, `judgeOutline`): none relied
  on the trailing wait. Removing any one of the eight guards fails a test. Taken as optional
  hardening: the media network case and the review table assert the exact waits, so a guard
  moved to skip the first wait instead of the last is caught too.
- Duration re-bind (2026-10-07, claude-pr-review-last-sleep, independent): PASS, DURATION_ONLY.
  The only difference in `review/sync.mjs` is the final wait. No length gate reads elapsed time,
  and no changed line names a duration term. `review/sync.mjs` and `sync.test.mjs` are rebound in
  `docs/videos/long-form/review.json`, and the CLI check passes.
