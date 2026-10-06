---
id: 2026-10-06-makedub-s-comment-still-says-a
title: makeDub's comment still says a down service or a STOP ends the run
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-06T23:28:30Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/flow.mjs
---

# makeDub's comment still says a down service or a STOP ends the run

## Why

The JSDoc of `makeDub` in `tools/video/automation/flow.mjs` (around lines 3344-3346, as of the
#1347 train) says that "a service that is down ends this run and the next one tries again, and a
STOP file that ends `dub`, a retake or the check (exit 6) ends it too". Since #1342 neither
ends the run:

- exit 4 defers the video (`defer`, with `everyone` for trouble that is everyone's);
- a STOP defers it for the rest of the run (`stopped()`, `backoffMs: 0`).

The lane goes on with the other videos. A reader who trusts the comment expects the lane to
halt. The first clause was already stale on main after #1342, and the train's STOP clause was
added to the same sentence. An independent reader found this while verifying the #1347 merge.

## Definition of done

- [ ] The comment says what the code does: exit 4 and a STOP defer only this video.

## Steps

- [ ] Reword the comment. No behaviour change.

## How to verify

Read the comment against `stopped()` and the exit-4 lines in `makeDub`.

## Notes

`flow.mjs` is bound in the duration review receipt, so even a comment change needs an
independent re-bind. Ride along with the next change to `flow.mjs` rather than spending a
re-bind on it alone.
