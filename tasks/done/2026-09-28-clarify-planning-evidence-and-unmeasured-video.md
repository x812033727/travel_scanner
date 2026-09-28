---
id: 2026-09-28-clarify-planning-evidence-and-unmeasured-video
title: Clarify planning evidence and unmeasured video timing
status: done
priority: P2
area: docs
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T06:46:45Z
created_at: 2026-09-28T06:46:24Z
completed_at: 2026-09-28T06:47:45Z
branch: codex/pr894-evidence-wording
depends_on: []
scope:
  - docs/videos/series-plans/claude-binge-five-20260928/README.md
  - docs/videos/series-plans/claude-binge-five-20260928/COMPARE.md
---

# Clarify planning evidence and unmeasured video timing

## Why

The planning overview claims that no one has used its story mechanism, without evidence.
The comparison also treats short hook text as proof of passing an eight-second production
threshold, although no narration or final media has been produced.

## Definition of done

- [x] Remove the unsupported universal originality claim.
- [x] Distinguish measured text length from pending audio/video timing and viewer retention.

## Steps

- [x] Inspect both descriptions and preserve the original story plans and metrics.
- [x] Correct the two claims without changing generated files or implying production approval.

## How to verify

Read the two changed paragraphs and run `git diff --check` and `node tools/tasks.mjs check`.
The exact original PR head 9e628c8 passed read-only `validate.mjs` for all five plans
(zero errors or warnings) and all ten `validate.test.mjs` cases before this prose-only edit.

## Notes

No active task covered these two paths; the original author's planning task is done,
the remote head was unchanged, and no local worktree holds its branch. Changes stay in
this watcher branch. No story source, generated manuscript, media or production state changes.
