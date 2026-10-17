---
id: 2026-10-17-shorts-and-imported-films-pushed-outside
title: Shorts and imported films pushed outside the worker are not marked hand-pushed
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-10-17T11:39:43Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/shorts/push.mjs
  - tools/video/import/import.mjs
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

- [ ] Ask the owner whether 「一律等站主」 covers Shorts and imported films too.
- [ ] If so, both submitters add the same `hand_pushed` mark under the same rule (no worker state
      file), with a test each; the server needs no change (`owner_decides` already reads it).
