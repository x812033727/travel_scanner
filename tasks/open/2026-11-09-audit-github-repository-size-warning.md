---
id: 2026-11-09-audit-github-repository-size-warning
title: Audit GitHub repository size warning
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-11-09T09:24:06Z
completed_at:
branch:
depends_on: []
scope:
  - docs/ops/repository-storage-audit.md
---

# Audit GitHub repository size warning

## Why

GitHub accepted the November 9 push of the retrieval-graph localization branch,
but emitted `warning: Repository is approaching its size quota.` The message
does not establish the current storage size, limit or cause. Investigate with
read-only measurements and propose a concrete storage plan before future pushes
are blocked. No matching open task was found when this warning was recorded.

## Definition of done

- [ ] Establish current repository/storage measurements and the relevant limit.
- [ ] Identify the largest historical/current contributors without deleting data.
- [ ] Record a concrete mitigation proposal and its backup/review requirements.

## Steps

- [ ] Recheck current GitHub state and confirm the exact warning/limit.
- [ ] Compare history and current-tree sizes, preserving active work and media.
- [ ] Document viable options, expected savings and compatibility/restore risks.
- [ ] Obtain separate owner approval before history rewriting, moving tracked assets or deletion.

## How to verify

Use read-only Git/GitHub measurements with timestamps. The scoped document should
distinguish observed storage figures from estimates and explain how any proposed
cleanup would be verified and restored. This ticket authorizes investigation and
documentation only; it does not authorize cleanup or a force push.

## Notes

Observed during the successful push of content commit
`27dafa22fa427244be07fc4de52e8c961ba8ec28`, subsequently opened as PR #2053.
The localization push succeeded; this warning is not a content-test failure.
The ticket remains open and unclaimed. Do not expand the article content PR into
a repository-cleanup operation, and do not infer that this wave caused the warning.
