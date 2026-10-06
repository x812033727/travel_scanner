---
id: 2026-10-06-a-writer-job-that-stays-queued
title: A writer job that stays queued is looked up every round with no ceiling and never reaches a card
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-06T16:47:54Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
  - tools/video/automation/automation.test.mjs
---

# A writer job that stays queued is looked up every round with no ceiling and never reaches a card

## Why

`tools/video/automation/flow.mjs` `move()` rethrows `RUN_PENDING` for a writer job still queued
or running on the server, and `step()` turns it into a `pendingUntil` entry
(`PENDING_RECHECK_MS`, one worker round). Nothing counts these lookups. A job that stays queued
for ever, for example on a queue that never dispatches it, is looked up once a round with no
end. The video is named in the worker's idle line but never reaches a card, so the owner does
not see it. No money is at risk: the lookup sends nothing new. An independent reader found this
while verifying PR #1342, and it was left open there as a known low item.

## Definition of done

- [ ] A writer job that is still pending after a set time (or a set number of rounds) shows on
      the video's card with how long it has waited, and blocks or asks the owner after a
      ceiling. A job that is merely slow is never paid for twice.

## Steps

- [ ] Save when the video's writer job was first seen pending (auto.json), and clear it when the
      job settles.
- [ ] Past a ceiling (to be decided, e.g. 6 hours), report a `deferred`-style row on the card;
      past a second, block as `pending:<stage>` with an instruction for the owner's retry.
- [ ] Tests in `automation.test.mjs`.

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
```

`flow.mjs` and `automation.test.mjs` are bound in the duration review receipt, so the change
needs an independent re-bind.

## Notes

Left open in PR #1342 (`2026-10-06-a-failing-video-is-deferred`), which owns these files
until it merges.
