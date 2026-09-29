---
id: 2026-09-29-video-acceptance-plan
title: Prepare story pilot and VPS private-upload acceptance plan
status: done
priority: P1
area: docs
owner: codex-p1-video-acceptance-plan
claimed_at: 2026-09-29T02:28:28Z
created_at: 2026-09-29T02:27:52Z
completed_at: 2026-09-29T02:34:24Z
branch: codex/p1-task-audit
depends_on: []
scope:
  - docs/work-status-2026-09-29-video-acceptance-plan.md
---

# Prepare story pilot and VPS private-upload acceptance plan

## Why

The owner asked to prepare the two-story pilot and VPS upload acceptance only after their dependencies are ready. Record current dependency evidence and a concrete private acceptance plan without production access, media generation or changes to the original execution tickets.

## Definition of done

- [x] The document distinguishes ready VPS code dependencies from the unmerged story worker; policy/languages merged during the audit and the snapshot was refreshed.
- [x] The VPS plan binds execution to a designated, owner-approved private test artifact, exact deployment version and owner Google login/channel confirmation.
- [x] Persistent metadata/assets, restart recovery, duplicate prevention and final receipt criteria are concrete; no live result is claimed.

## Steps

- [x] Read the original tasks, deployment/upload/story documentation and relevant skills.
- [x] Verify current GitHub PRs, checks and the stacked merge path into main using read-only calls.
- [x] Write the plan in the one-file scope; preserve original execution tickets for the coordinator.

## How to verify

Read-only gh pr view for #933, #938, #909, #893 and #890; gh api compare and git trees prove the parent squash integration and matching uploader blobs. Run npm run check:tasks. No production or media test is part of this document-only task.

## Notes

- Collision check: who-is-on-it found no active task or open PR touching the plan path. Reused codex/p1-task-audit under the coordinating agent; did not switch branches or commit.
- At the refreshed 02:33 UTC snapshot, #933 is OPEN/BLOCKED at its new head 345d8e99 (api/web/full-stack-smoke running). #938 merged at 02:29:18 UTC as 0cfcfdc1 with all four required checks successful. No story pilot started.
- #893 merged into its then-parent branch, then #890 squash-merged into main. #893 merge SHA is not a direct main ancestor, so readiness is supported by #890 ancestry and four matching file blobs, not by a misleading direct-ancestor claim.
- Existing approved-not-deployed/live-acceptance-pending boundary is preserved. This run did not refresh production state.
- Completed only the preparation task. Original story pilot and VPS deployment/live acceptance remain open.
- npm run check:tasks passed with exit 0; only existing stale/overlapping-claim warnings remain. The tasks done command left its known duplicate open copy; compared both complete task bodies and removed only that duplicate, preserving the done record.
