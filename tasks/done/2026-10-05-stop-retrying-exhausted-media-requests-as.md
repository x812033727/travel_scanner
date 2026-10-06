---
id: 2026-10-05-stop-retrying-exhausted-media-requests-as
title: Stop retrying exhausted media requests as temporary service failures
status: done
priority: P1
area: tools
owner: codex-gpt-6-root
claimed_at: 2026-10-05T11:58:41Z
created_at: 2026-10-05T11:58:36Z
completed_at: 2026-10-05T12:08:54Z
branch: codex/video-exhausted-media-hold-20261005
depends_on: []
scope:
  - tools/video/media/client.mjs
  - tools/video/media/media.test.mjs
---

# Stop retrying exhausted media requests as temporary service failures

## Why

After the slides-format and policy-hold repair was deployed, the two oldest
eligible videos still occupied both worker lanes. Their keyframe submissions
returned HTTP 409 / `video_media_job_exhausted`: the server had already failed
the identical payload three times and required a source or seed change.

The media client classified this settled refusal as an external service error
(exit 4). Automation therefore kept the video active and retried it every
round, without accumulating stage failures or allowing younger videos to run.

## Definition of done

- [x] Exhausted media requests use the existing owner-action exit 3, preserving
      the exact server code and explanation. Automation blocks that project
      and can continue its other eligible work.
- [x] No blanket change to other HTTP 409s, provider retries or retake rules.
- [x] Preserve paid cache, jobs, ledgers, reviews, source and prompt-fix counts;
      do not reset attempts, truncate prompts or raise budgets.

## Steps

- [x] Recheck main, worktrees, remote branches and PR path collisions; this
      client's scope has no active claim or competing open PR.
- [x] Confirm the live refused requests, structured code and lane ordering.
- [x] Reproduce the faulty classification and verify the narrow repair.
- [x] Independently review the diff and focused suite; check task consistency.
- [ ] Complete full tools/CI and production verification before release.

## How to verify

`node --test tools/video/media/media.test.mjs` exercises actual image/clip
clients, exact code/message, one POST each with no retry sleep, CLI exit 3,
and an unrelated HTTP 409. Restore the old classification to prove the new
regression fails. Run Automation/media suites and `npm run test:tools`,
`npm run check:tasks`; production verification must use the deployed SHA.

## Notes

2026-10-05 11:58 UTC read-only production evidence: Skills had 25 and SEC 37
failed keyframe rows with attempts=3, all `video_media_upstream_invalid`:
the complete MiniMax prompt plus avoidance text exceeded 1,500 characters.
The latest sampled refusals had no submitted_at and zero estimated cost.
Their media journals had no pending/uncertain jobs; no rows or receipts were
cleared. The existing bounded-media producer owns source-quality recovery.
Changing a seed alone cannot shorten these prompts. This task fixes worker
isolation and reporting, without bypassing those source/quality decisions.

The actual client/CLI regression and independent media suite pass 11/11.
Removing the new code reproduces the original `service !== owner` failure.
An unrelated 409 keeps its existing service classification; exhausted codes
are excluded from automatic retakes. Independent diff/long-form checks pass;
task consistency passes (1,498 files). Full Windows tools is running at draft
creation; the remaining checkbox is a release gate, not a passing claim.
The production patch, prompt quality recovery, assembly, upload and publication
have not been declared complete by this code task.
