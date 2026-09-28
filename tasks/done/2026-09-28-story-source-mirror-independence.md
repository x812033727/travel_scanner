---
id: 2026-09-28-story-source-mirror-independence
title: Treat encyclopedia mirrors as one story source
status: done
priority: P2
area: tools
owner: codex-pr909-review
claimed_at: 2026-09-28T10:54:48Z
created_at: 2026-09-28T10:54:36Z
completed_at: 2026-09-28T10:56:37Z
branch: codex/pr909-source-independence
depends_on: []
scope:
  - tools/video/story-plans/plan.mjs
  - tools/video/story-plans/plan.test.mjs
---

# Treat encyclopedia mirrors as one story source

## Why

The story-plan validator counted Wikipedia and its mirrors as different source
families when their publisher labels differed. A claim could therefore pass the
two-independent-secondary-sources rule using only an encyclopedia and its copy.

## Definition of done

- [x] An encyclopedia, its language editions, mirrors and archived copies count
      as one source family; an unrelated newspaper remains independent.
- [x] Regression fails before the correction and passes afterward; all 100
      existing story plans and their generated files continue to validate.

## Steps

- [x] Confirm the exact PR #909 head and a free worktree, then claim only the
      source-family validator and its test file.
- [x] Add a regression and map the known mirror domains to one canonical family.
- [x] Run focused tests and plan validation, close this ticket and save a local
      commit for the merge monitor to review.

## How to verify

`node --test --test-concurrency=1 tools/video/story-plans/*.test.mjs`

`node tools/video/story-plans/validate.mjs`

`node tools/tasks.mjs check` and `git diff --check`.

## Notes

The author head was `9c3006044fa3a07c4da67c879aa3864a6309c07a` when work began.
The original backlog task is done on that head; no active task claims these two
files. The 100 story files contain no Wikiwand, Wikimili or Wikimedia URLs, so
this correction does not change their accepted sources, text, hashes or schedule.
The separate PR #906 repair remains saved on `codex/pr906-validator-guard` at
`aef6dcfb06949776edd57510f6486c3c7fc17079`.

The added regression failed before the fix (`wikiwand.com` was returned instead
of the shared family) and all 25 story-plan tests passed afterward. Validation
still reports 100 stories, 50 days and zero problems. The author's subsequent
`5c93f95e4360e9af2930ab44148141140f744826` only updates the separate admin task
and is preserved before committing this repair. No story, review, schedule,
production setting or publication changed.
