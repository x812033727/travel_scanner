---
id: 2026-09-28-resolve-narrator-story-merge-conflicts
title: Resolve narrator story merge conflicts
status: done
priority: P1
area: docs
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T08:37:53Z
created_at: 2026-09-28T08:37:53Z
completed_at: 2026-09-28T08:40:08Z
branch: codex/pr897-story-conflict
depends_on: []
scope:
  - docs/videos/STORY.md
  - tasks/open/2026-09-28-video-story-core-narrator-only.md
---

# Resolve narrator story merge conflicts

## Why

PR #897 adds narrator-only story rules to STORY.md. Its parent #888 landed through
squash merge, so Git sees both copies of that document as independently added and
reports an add/add conflict despite the feature document containing the full design.
Synchronizing the parent can also restore an open ticket already completed by #897.

## Definition of done

- [x] The merged document preserves the current main design and all authored story contracts.
- [x] The author's completed narrator-only ticket remains the sole copy of its ID.
- [x] Implementation/workflow files remain unchanged from the reviewed author head.

## Steps

- [x] Compare both document versions and check current head/worktree ownership.
- [x] Merge main, resolve only the documented differences and remove the duplicate open ticket.
- [x] Validate task structure, source preservation and diff integrity; require current-head CI.

## How to verify

Compare main's STORY.md with author head a687a51a: the only changes are the added
lint/tool-contract section and expanded scope row. Preserve that union. Verify all
tools/video and video-tooling workflow files equal a687a51a, then run task and diff
checks. Full latest-head CI remains required before merge.

## Notes

- Remote head a687a51a was rechecked before starting. No local worktree has its exact
  claude/video-story-core-narrator-only branch checked out. This correction uses the
  dedicated watcher checkout and preserves the author's history and done ticket.
- Read-only merge-tree against main d8d6363f reported only docs/videos/STORY.md.
  The feature document retains every main section and adds the series.json contract,
  STORY_RULES, narrator-only gate behavior and paginated contact-sheet explanation.
- The resolved document is identical to the reviewed feature document. Removing only
  its new contract section and reverting the expanded scope row reproduces main's
  document exactly. All tools/video files, the video-tooling workflow and the author's
  done ticket are unchanged. The reintroduced unclaimed open copy was removed.
- Task validation passed for 1,016 files; staged/working diff checks and unmerged-file
  checks passed. Evidence: test-results/pr897-document-union.json and pr897-tasks.log.
  No implementation tests were rerun for this document-only resolution; the author's
  existing test evidence remains applicable, and full new-head CI still gates merge.
