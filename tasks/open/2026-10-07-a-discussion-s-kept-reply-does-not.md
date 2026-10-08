---
id: 2026-10-07-a-discussion-s-kept-reply-does-not
title: A discussion's kept reply does not say its rewrite is still being repaired
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T15:20:00Z
completed_at:
branch:
depends_on:
  - 2026-10-06-a-discussion-whose-writer-answer-was
scope:
  - tools/video/automation/discuss.mjs
  - tools/video/automation/series.test.mjs
  - docs/videos/long-form/review.md
  - docs/videos/long-form/review.json
---

# A discussion's kept reply does not say its rewrite is still being repaired

## Why

`tools/video/automation/discuss.mjs` `answerHeld` keeps the writer's reply to the owner's line
before the rewrite's lint repairs (`saveAndLint`). When a repair is still running after the
client's wait, or fails and the video waits, the next unit posts that kept reply as it is: it reads
as if the change were done, though the rewrite is still being repaired and checked, and if the
video's own repair later fails the video is blocked with the rewrite on disk. Lint still gates the
script; only what the owner is told is off. Found by the duration re-bind of
`2026-10-06-a-discussion-whose-writer-answer-was` (2026-10-07).

## Definition of done

- [ ] A reply kept before the repairs says the new version is saved and still being checked; a
  visit that finishes the repairs posts the plain reply.

## Steps

- [ ] Keep the reply with a short zh-TW note before `saveAndLint`, and post the plain reply when
  the repairs finish in the same visit.
- [ ] Adjust the two lint-repair tests in `series.test.mjs`.

## How to verify

`node --test tools/video/automation/series.test.mjs`. `discuss.mjs` and `series.test.mjs` are bound
by the duration receipt and need the independent re-bind.

## Notes

- A process that dies between keeping the reply and `saveAndLint`'s first write would post the
  note for a rewrite that was never saved; the note's wording should not promise more than
  "saved".
