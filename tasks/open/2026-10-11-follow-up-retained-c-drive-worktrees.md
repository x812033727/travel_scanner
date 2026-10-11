---
id: 2026-10-11-follow-up-retained-c-drive-worktrees
title: Follow up retained Codex C drive worktrees when their work finishes
status: open
priority: P3
area: meta
owner:
claimed_at:
created_at: 2026-10-11T14:40:49Z
completed_at:
branch:
depends_on: []
scope:
  - tasks/open/2026-10-11-follow-up-retained-c-drive-worktrees.md
  - tasks/worktree-cleanup-20261011.md
---

# Follow up retained Codex C drive worktrees when their work finishes

## Why

The owner narrowed cleanup to Codex. The 36 Codex roots in the C: inventory remain protected by dirty changes, unfinished PRs or delivery work, ongoing use, or primary/audit/production ownership. The directory-specific reasons and next actions are in `tasks/worktree-cleanup-20261011.md`. This task tracks later cleanup eligibility; it does not claim the underlying product tasks or authorize discarding changes.

## Definition of done

- [ ] Recheck only Codex paths after their existing owners have completed their work; record any eligible removals with before/after evidence.
- [ ] Preserve unfinished work, non-regenerable ignored files, the primary repository, and the ongoing Ou de Jianghu handoff.

## Steps

- [ ] For the 22 dirty secondary checkouts, follow the owner-specific next action in the inventory; keep the original index and file contents until the owner reconciles them.
- [ ] Finish or review the six existing open PRs without treating a clean checkout as delivery completion.
- [ ] Resolve the four clean ongoing delivery/workflow entries: news-held recovery, Embedding, localization batch003, and batch005.
- [ ] Recheck the two active audit worktrees and the protected 1b93 visual handoff only after their work ends; never remove the primary clone as a historical worktree.
- [ ] Immediately before a later removal, verify current HEAD, main/PR completion, status including all untracked files, ignored artifacts, running processes and chat ownership; keep recovery evidence and verify removal.

## How to verify

Read `C:/Users/x8120/.codex/scratch/worktree59-cleanup-20261011/codex-worktree-report.html` and the JSON/verification receipts alongside it. Recompute the evidence live before future cleanup; this is a dated inventory. Run `node tools/tasks.mjs check` for metadata edits.

## Notes

This task is open and unclaimed. Claude and all other projects are outside the final scope. Existing task ownership, production leases, STOP markers, source media, and historical branch refs remain untouched.
