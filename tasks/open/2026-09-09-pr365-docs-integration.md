---
id: 2026-09-09-pr365-docs-integration
title: Integrate PR 365 historical deployment and open verification notes
status: review
priority: P2
area: docs
owner: codex-pr365-docs
claimed_at: 2026-09-09T06:20:37Z
created_at: 2026-09-09T06:20:36Z
completed_at:
branch: codex/pr365-docs-ready-20260909
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
No further main merge was performed: integration remains pinned to a899437a
until the root agent supplies the final main SHA after the functional PRs.
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
