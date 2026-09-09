---
id: 2026-09-09-pr365-docs-integration
title: Integrate PR 365 historical deployment and open verification notes
status: in-progress
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

- [ ] Preserve dated evidence and unfinished live verification obligations.
- [ ] Describe the production-build CI improvement already present on the fixed main.
- [ ] Integrate main normally, regenerate BOARD, and pass task/diff checks.
- [ ] Hand off a clean local commit without pushing, merging remotely or deploying.

## Steps

- [x] Verify the exact PR head and claim documentation-only integration scope.
- [ ] Merge fixed main and reconcile only the task-documentation overlap.
- [ ] Validate and return the local result for the root agent's review.

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
