---
id: 2026-09-28-preserve-audio-batching-task-completion
title: Preserve audio batching task completion
status: done
priority: P2
area: meta
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T08:43:06Z
created_at: 2026-09-28T08:43:05Z
completed_at: 2026-09-28T08:48:34Z
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

- [x] The synchronized branch retains only the author's completed audio-batching ticket.
- [x] The author's implementation and completed-task contents are unchanged by this board cleanup.
- [x] Task validation and diff checks pass after main integration.

## Steps

- [x] Verify remote head, ownership and the duplicate produced by read-only merge-tree.
- [x] Merge main and remove only the reintroduced unclaimed open copy.
- [x] Validate preservation and close this maintenance task before the final push.

## How to verify

Compare tools/video/tts/check.mjs, check.test.mjs and the original done ticket
against author head 4d571c30.
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
- Main also brings the already-merged video-language/state work. Keep those main
  changes; preservation applies to the two audio-batching files and done ticket,
  not to reverting all tools/video files to the older author's tree.
- The three authored files were identical after integration. Task validation passed
  for 1,016 files, and diff checks passed. The integrated TTS suite then reported
  42 passes and one Windows EPERM rename failure; this is not a green local run.
  The root cause is tracked by existing task 2026-09-26-atomicwrite-fails-on-windows-when-the,
  which will own the separate runtime fix and recovery validation. Evidence:
  test-results/pr896-main-d8-tts.log and pr896-main-d8-tasks.log.
