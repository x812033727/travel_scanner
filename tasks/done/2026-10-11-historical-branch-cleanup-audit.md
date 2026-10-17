---
id: 2026-10-11-historical-branch-cleanup-audit
title: Audit and clean 197 historical branch candidates
status: done
priority: P2
area: meta
owner: codex-gpt6-historical-cleanup
claimed_at: 2026-10-11T13:01:33Z
created_at: 2026-10-11T13:00:09Z
completed_at: 2026-10-11T13:18:34Z
branch: codex/historical-branches-cleanup-20261011
depends_on: []
scope:
  - tasks/open/2026-10-11-historical-branch-cleanup-audit.md
  - tasks/done/2026-10-11-historical-branch-cleanup-audit.md
  - tasks/open/2026-10-11-retained-historical-branches.md
---

## Why

The owner requested verification of the 197 historical local branch candidates from the 2026-10-11 inventory, removal of completed clean branches, and a durable list of retained unfinished work.

## Done when

Every candidate has an evidence-backed decision. Deleted local refs have a verified independently restorable backup. Retained branches and their next actions are recorded without changing other agents' tasks or remote branches.

## Steps

- [x] Freeze the original 197-ref cohort and refresh both clones and all-state PR evidence.
- [x] Audit commit contents, squash merges, replacement PRs, task state, worktree changes and active ownership.
- [x] Review completion evidence and preserve unsupported or unfinished work.
- [x] Create and independently restore-test backup bundles before deletion.
- [x] Compare expected HEADs and remove only approved unused local refs; verify absence.
- [x] Record retained work in the follow-up task and prepare the task-only change for shared review.

## Verification

- Run the task checker on the isolated task-only checkout.
- Account for all 197 candidates in the audit and execution receipts.
- Recheck local refs, checked-out worktrees and open PRs immediately before deletion.

## Notes

- User authorization: delete completed branches with no uncommitted modifications; retain unfinished branches and organize follow-up tasks.
- Cohort and audit artifacts: C:/Users/x8120/.codex/scratch/historical-cleanup-20261011.
- Main evidence baseline: 0c93720e684b4c3995b16f7c2e859fe2bc06ec9f.
- No implementation work, production changes, remote branch deletion or task ownership transfers are included.

- Final accounting: all 197 candidates audited; 109 local refs removed (Codex 97, Claude 12), 88 retained (Codex 76, Claude 12). Retained: 64 unfinished and 24 uncertain.
- Four task-only bookkeeping refs were positively reclassified after root review: their associated tasks are done on main and every changed path is under tasks/.
- Backups independently restored and every expected HEAD checked: completed-codex.bundle (93), completed-codex-supplement-2.bundle (4), completed-claude.bundle (12). SHA-256 values and all deleted HEADs are in cleanup-receipt.json.
- Post-cleanup verification confirms all 109 deleted refs are absent and all 88 retained refs remain. The active Claude e001 branch advanced during the audit; its new HEAD was preserved and recorded.
- The first deletion succeeded but its initial missing-ref probe returned 128; recovery verified absence with show-ref --verify --quiet (return 1), recorded that action, and resumed from the checksum-verified backup. All subsequent actions persisted their absence checks.
- Reports: C:/Users/x8120/.codex/scratch/historical-cleanup-20261011/cleanup-report.html and cleanup-report.txt. Evidence: reviewed-audit.json, cleanup-receipt.json, post-cleanup-verification.json.
- Retained-work index: tasks/open/2026-10-11-retained-historical-branches.md. It links existing task IDs and preserves every original claim.
