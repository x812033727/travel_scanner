---
id: 2026-10-08-a-storyboard-s-kept-shot-still
title: A storyboard's kept shot still carries the judge's verdict fields at the last size step
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-08T02:24:31Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/review/sync.mjs
  - tools/video/review/sync.test.mjs
---

# A storyboard's kept shot still carries the judge's verdict fields at the last size step

## Why

2026-10-06-a-storyboard-with-many-kept-pictures promised that keeping pictures never stops a
storyboard that would go up with nothing kept. On main (#1364) the last size step of
`review/sync.mjs` `fitPayload` drops only `payload.accepted`; each kept shot still carries
`accepted: true`, `needs_review: false` and `judge.problems: []`, about 18 bytes more than the
same shot passed by the judge. A board within that window of the site's 262,144 bytes with
nothing kept is refused with every shot kept (`keyframes --accept-best`), and the video blocks.
Main's task notes accept the window, and no real video is that large today (a brand story has
85 to 100 shots; the window is about 3.6 KB at 200 shots), so this is P3.

#1361 sent a kept shot without `needs_review` and `judge.problems` at that step, so a kept shot
cost less than a passed one; the server's `storyboard_check_passed` treats a missing
`needs_review` as false and skips the judge for accepted shots, the card reads
`shot.needs_review === true`, and flow.mjs filters on a truthy `needs_review`. That was dropped
when #1361 was rebased onto main (2026-10-08). Found by the overlap comparison of the two PRs.

## Definition of done

- [ ] A storyboard that goes up with nothing kept goes up with every shot kept, at any size.

## Steps

- [ ] `fitPayload`'s last step drops `needs_review` and `judge.problems` from each kept shot
      (accepted and not `needs_review: true`), with its comment and docstrings.
- [ ] sync.test.mjs: kept bytes <= plain bytes, and a near-limit board (about 261,000 bytes
      with nothing kept) that goes up with every shot kept.
- [ ] Rebind the duration receipt (sync.mjs and sync.test.mjs are bound) by an independent
      reviewer.

## How to verify

`node --test tools/video/review/sync.test.mjs`; `node tools/video/long-form/cli.mjs check`.

## Notes

#1361's version: commit 3cf44c41c (`withKeptRemarks`, the test "a storyboard that goes up with
nothing kept goes up with every shot kept").
