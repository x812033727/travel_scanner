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

Validation: `npm run check:tasks` passed for 204 task files; it reports the
existing discovery/planner overlap on trip-editor.test.tsx, which was not edited.
`node --test tools/tasks.test.mjs tools/json-duplicate-keys.test.mjs` passed all
24 relevant checks; `git diff --check` passed. The attempted broader
`npm run test:tools` passed those 24 checks but failed to import the unrelated
airline-crawler test because this fresh worktree has no installed
`@playwright/test`. No dependency installation, browser launch or crawler run
was attempted, and no full-tools pass is claimed. The receiving agent must run
the updated PR's required CI before any remote merge.

Documentation is suitable for normal PR review rather than being held draft
until affiliate activation or a separate network investigation is finished;
those unfinished obligations are explicitly retained. No remote draft-state
change, PR write, push, merge, deployment or live-provider call was performed.
