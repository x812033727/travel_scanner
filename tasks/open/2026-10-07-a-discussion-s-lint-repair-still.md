---
id: 2026-10-07-a-discussion-s-lint-repair-still
title: A discussion's lint repair still running on a durable route is taken by the video's own step, not the discussion
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-07T12:57:11Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/automation/discuss.mjs
  - tools/video/automation/flow.mjs
  - tools/video/automation/series.test.mjs
---

# A discussion's lint repair still running on a durable route is taken by the video's own step, not the discussion

## Why

A line the owner writes on a screenplay is answered by the writer (`discuss.mjs` `answerHeld`).
When the rewrite it answers with does not pass lint, `saveAndLint` sends the writer's lint
repair (variant `episode`, or the anime act repair) inside the same step. On the durable route
that repair is a job of its own. When it is still queued or running when the step's 25 seconds
are up, the client throws RUN_PENDING, and `answerHeld` rethrows it as before:

- the rejected rewrite stays in `video.json` and the owner's line stays unanswered;
- `step()` sets the video aside for a round (`pendingUntil`), and when the job finishes, the
  video's own unit takes the repair's answer (`write()`, "A draft exists and only fails lint"),
  not the discussion: the reply is never posted, and the next discussion step pays
  `writer:discuss` again for the same line on the repaired script.

Seen in a trial run while doing 2026-10-05-hold-lost-planner-and-jev-answers (the series test
of the lint repair's lost answer, durable variant, after the owner's retry): the video's own
unit took the repair's answer, blocked with "the answer has no video object", and the line got
the blocked reply. The test stops at the retry so it does not pin that behaviour. A lost
answer of the same repair (RUN_UNCERTAIN) is handled since that ticket: the script is put
back and the video blocks `uncertain:writer` with the line held.

## Definition of done

- [ ] A discussion's lint repair that is still running when the step ends is taken up by the
      discussion on a later round (its reply is posted, its rewrite kept), never by the
      video's own unit, and `writer:discuss` is not paid for again.
- [ ] The video's own stages wait while the repair runs, as they wait for a discussion's own
      writer job (`discussionOpen`, `untakenRuns`).

## Steps

- [ ] Decide between restoring the last good script and rethrowing RUN_PENDING (the next
      discussion attempt reuses the adopted discussion journal by its exact hash), or holding
      the line in the video's state until the repair's journal is taken.
- [ ] A test in `series.test.mjs` that owns the sequence: the owner's line, the discussion
      answered with a rewrite lint refuses, the repair job still running, the next rounds.
- [ ] Rebind the duration receipt independently (`discuss.mjs`, `flow.mjs` and
      `series.test.mjs` are bound).

## How to verify

`node --test tools/video/automation/series.test.mjs tools/video/automation/discuss.test.mjs`

## Notes

- Related: 2026-10-06-a-pending-discussion-job-and-the (a discussion's own pending writer job
  holds its video since PR #1342), 2026-10-07-a-discussion-s-refused-script-revision (lexicon
  terms a restored rewrite leaves behind, the same lines of `answerHeld`).
