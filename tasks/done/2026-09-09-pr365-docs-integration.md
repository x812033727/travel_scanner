---
id: 2026-09-09-pr365-docs-integration
title: Integrate PR 365 historical deployment and open verification notes
status: done
priority: P2
area: docs
owner: codex-review-archive
claimed_at: 2026-09-09T07:37:00Z
created_at: 2026-09-09T06:20:36Z
completed_at: 2026-09-09T07:37:01Z
branch: codex/review-evidence-archive-20260909
depends_on: []
scope:
  - tasks/open/2026-09-08-community-ci-read-retry.md
  - tasks/open/2026-09-08-travelpayouts-live-destination-activation.md
---

# Integrate PR 365 historical deployment and open verification notes

## Why

PR #365 preserves deployment observations and unfinished Travelpayouts verification.
Its old base predates current CI and scope handoffs; reconcile the documentation
without presenting the historical deployment or approvals as the current live state.

## Definition of done

- [x] Preserve dated evidence and unfinished live verification obligations.
- [x] Describe the production-build CI improvement already present on the fixed main.
- [x] Integrate main normally, regenerate BOARD, and pass task/diff checks.
- [x] Prepare the local documentation commit for handoff without pushing, merging remotely or deploying.

## Steps

- [x] Verify the exact PR head and claim documentation-only integration scope.
- [x] Merge fixed main and reconcile only the task-documentation overlap.
- [x] Validate the local result for the root agent's review; remote CI/merge remain separate.

## How to verify

Run `npm run tasks:board`, `npm run check:tasks`, `npm run test:tools`, and
`git diff --check`. Inspect the net diff against the fixed main; it must contain
only the two original task documents, this integration task, and generated BOARD.
Read CI/configuration as source evidence only; do not run application, provider,
browser, deployment or operational commands.

## Notes

2026-09-09: The user accepted preparing functionality first, then organizing the
documentation/evidence. Start at PR #365 head
172da59278e1c269343f09869604b0765f4125a1 and integrate fixed main
a899437aaf2f60c7affe2e944d49d62216537c90, independently confirmed by GitHub's
`git/ref/heads/main` endpoint. The PR's `baseRefOid` is its historical base, not
proof of current main. This task does not claim the underlying CI test or live
affiliate operations scopes, change approval gates, or certify deployment state.

The normal merge had only a generated BOARD conflict, resolved with
`npm run tasks:board`. The net delta against fixed main is documentation only:
the two original open tasks, this integration task and BOARD. Preserve both
original operational tasks as open; this integration does not complete them.

Initial validation: `npm run check:tasks` passed for 204 task files; it reports the
existing discovery/planner overlap on trip-editor.test.tsx, which was not edited.
`node --test tools/tasks.test.mjs tools/json-duplicate-keys.test.mjs` passed all
24 relevant checks; `git diff --check` passed. The attempted broader
`npm run test:tools` passed those 24 checks but failed to import the unrelated
airline-crawler test because this fresh worktree initially had no installed
`@playwright/test`. No dependency installation, browser launch or crawler run
was attempted during that first check. This initial limitation is resolved by
the authorized follow-up below; it is retained here as historical validation evidence.

Authorized local dependency follow-up on 2026-09-09:
`npm ci --ignore-scripts --no-audit --no-fund` completed successfully (545 packages).
The locked package file is unchanged, SHA-256
8d579e5bec8b85c2e2c111f49aefb75e509664455292b6a587e9581b5f5f17a9.
Complete `npm run test:tools` now passes 27/27 tests with zero failures or skips.
The crawler-named unit tests only exercise argument parsing, query construction
and API-root validation; the crawler entry point and browsers were not invoked.
`npm run tasks:board`, `npm run check:tasks` (204 files), and `git diff --check`
also passed. Existing stale merchant-claim and discovery/planner-overlap warnings
are unchanged ownership issues outside this task; no other task was modified.
At that dependency checkpoint no further main merge was performed; integration
remained pinned to a899437a while awaiting the root's final functional-PR SHA.
The receiving agent must still run the updated PR's required CI before remote merge.

Documentation is suitable for normal PR review rather than being held draft
until affiliate activation or a separate network investigation is finished;
those unfinished obligations are explicitly retained. No remote draft-state
change, PR write, push, merge, deployment or live-provider call was performed.

2026-09-09 CI-evidence follow-up: documented the root's reviewed #343 merged-main
and #335 same-head push/PR observations in the owned community-read task, retaining
exact job IDs and the distinction between a transport reset, token assertions,
HTTP errors and reruns. Independently checked the job SHA/status/step metadata;
recorded the root's sanitized failure-output findings without copying credentials,
member IDs or request bodies. Added an open failure-artifact retention criterion,
with workflow scope coordination required before implementation. No workflow,
test, runtime or other task scope was changed, and no new main was integrated.

Final main integration on 2026-09-09: the root supplied
98f8067b3664a956e44d0b6e9f372b27a22775e6 after the guarded #335 merge, including
the already merged #343 safety changes. Normally merged that exact commit; the
only conflict was generated BOARD, regenerated with the task tool. The net delta
against this final main remains the same four documentation/task files, with no
runtime, CI, test, provider setting or operational change.

Independently rechecked #335's merged SHA/time and 12 successful final checks,
and #343 main CI run 34319338706's successful attempt 2. Added their historical
outcomes to the open investigation without calling the transport reset or lost
failure artifacts repaired. The #335 same-SHA push rerun is explicitly disclosed;
the PR jobs passed first attempt. No rerun was initiated by this documentation
task. Fresh PR CI, any draft-state change, remote push/merge and post-merge checks
remain the root agent's separate delivery steps; this task only supplies a clean
local handoff and does not perform them.

Final-base validation: complete tools tests 27/27 passed, task/BOARD validation
passed for 206 files, and whitespace/diff checks passed. The same unrelated
stale-claim/overlap warnings remain; no scope takeover or runtime fix is implied.

## Authorized merge and ownership handoff

On 2026-09-09 the user explicitly accepted merging #365 and #376 while leaving
#377 out of scope. Root rechecked live main, exact head, all 12 successful checks,
clean mergeability and the absence of unresolved review threads. #365 was
squash-merged with the exact-head guard at 2026-09-09T07:34:43Z as
3d88373caf5c6aab99399867112ed9944b30684c from
7054a1d9bcb779a836a18a2245fe0255640515ea. Both commits have tree
c8f3cdcdec245d2ff75a9216135777bbec949d10, and the remote main ref and ancestry
were independently verified.

Original owner codex-pr365-docs explicitly handed the completion-record/status
scope to root for inclusion in #376. Only this narrow documentation-integration
task is closed. The community CI investigation and live Travelpayouts verification
tasks remain open; no operational criterion is completed by this merge.

At this checkpoint, merged-main CI 34324567669, Planner 34324567728 and Discovery
34324567664 are running and are followed separately by root. No post-merge pass
is claimed before they finish. No deployment, provider activation, production
connection, review replay or quota change was performed.
