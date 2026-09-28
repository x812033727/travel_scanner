---
id: 2026-09-28-preserve-audio-batching-task-completion
title: Preserve audio batching task completion
status: in-progress
priority: P2
area: meta
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T08:43:06Z
created_at: 2026-09-28T08:43:05Z
completed_at:
branch: codex/pr896-batch-verification
depends_on: []
scope:
  - tasks/open/2026-09-28-video-story-check-audio-batching.md
---

# Preserve audio batching task completion

## Why

PR #896 has already completed its audio-batching ticket. After parent #888 was
squash-merged, merging main creates both its original unclaimed open ticket and
the author's completed copy. That duplicate ID would fail task validation even
though Git reports no textual conflict.

## Definition of done

- [ ] The synchronized branch retains only the author's completed audio-batching ticket.
- [ ] The author's implementation and completed-task contents are unchanged.
- [ ] Task validation and diff checks pass after main integration.

## Steps

- [x] Verify remote head, ownership and the duplicate produced by read-only merge-tree.
- [ ] Merge main and remove only the reintroduced unclaimed open copy.
- [ ] Validate preservation and close this maintenance task before the final push.

## How to verify

Compare tools/video and the original done ticket against author head 4d571c30.
Confirm no duplicate open ID, run npm run check:tasks and git diff --check, and
require synchronized final-head CI before merging the PR.

## Notes

- Remote head 4d571c30 was unchanged, and no local worktree has the author's exact
  claude/video-story-check-audio-batching branch checked out. The implementation
  ticket is already done. This work uses the existing dedicated verification branch.
- Read-only merge-tree against main d8d6363f produced tree d59e6a74 with both open
  and done copies of the audio-batching ticket. The original done blob is 55e98d4f.
- This task changes board integration only. The separately recorded Windows EPERM
  issue and uncommitted recovery probe are not represented as newly fixed or passed.
