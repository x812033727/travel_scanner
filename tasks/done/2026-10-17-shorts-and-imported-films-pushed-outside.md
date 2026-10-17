---
id: 2026-10-17-shorts-and-imported-films-pushed-outside
title: Shorts and imported films pushed outside the worker are not marked hand-pushed
status: done
priority: P2
area: tools
owner: claude-opus-5-5-hand-pushed
claimed_at: 2026-10-17T13:54:27Z
created_at: 2026-10-17T11:39:43Z
completed_at: 2026-10-17T13:57:14Z
branch:
depends_on: []
scope:
  - tools/video/shorts/push.mjs
  - tools/video/shorts/cli.mjs
  - tools/video/shorts/bindings.test.mjs
  - tools/video/import/import.mjs
  - tools/video/import/import.test.mjs
  - docs/videos/HANDS-OFF.md
  - tasks/open/2026-10-17-shorts-and-imported-films-pushed-outside.md
---

# Shorts and imported films pushed outside the worker are not marked hand-pushed

## Why

Since `2026-10-11-hand-driven-film-approved-on-its` (owner, 2026-10-17: 「一律等站主」),
`review-push` marks a submission `hand_pushed: true` when the video's work directory has no
worker state file (`auto.json`), and `submit_review` approves none of those on arrival. Two other
submitters post reviews without going through `review-push`, so they are never marked (found by
the independent review `claude-pr-review-hand-pushed`):

- `tools/video/shorts/push.mjs`: a Short made outside the worker can still be approved on arrival
  by the Shorts checks.
- `tools/video/import/import.mjs`: an imported final carries no quality report, so it is not
  approved on arrival today, but nothing says so explicitly.

## Definition of done

- [x] Ask the owner whether 「一律等站主」 covers Shorts and imported films too. (Owner,
      2026-10-17: 「兩種都套用」.)
- [x] Both submitters add the same `hand_pushed` mark, with a test each; the server needs no
      change (`owner_decides` already reads it).

## Notes

- The Shorts rule is by command, not by `auto.json`: a Short's own directory never holds the
  long-form worker's state file, so that test would mark the worker's Shorts too. The worker
  calls `push()` from `lab.mjs` and `cut.mjs` without the flag; `shorts/cli.mjs push`, the only
  way a person or an agent sends one, passes `handPushed: true`, and both the final and publish
  reviews carry the mark.
- An import is always made outside the worker, so `finalReview` in `import.mjs` always marks it.
