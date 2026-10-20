---
id: 2026-10-20-curio-preprod-review-whitespace
title: Normalize copied review whitespace for clean Curio PR
status: done
priority: P2
area: docs
owner: codex-gpt6-root
claimed_at: 2026-10-20T21:08:37Z
created_at: 2026-10-20T21:08:34Z
completed_at: 2026-10-20T21:08:49Z
branch: codex/curio-preproduction-s46-s56-20261020
depends_on: []
scope:
  - docs/videos/curio-s51/review/r14-isolated-blind-a.md
  - docs/videos/curio-s53/review/r7-isolated-blind-b.md
  - docs/videos/curio-s53/review/r8-isolated-blind-a.md
  - docs/videos/curio-s53/review/r8-isolated-blind-b.md
  - docs/videos/curio-s53/review/r8-isolated-merge.md
---

# Normalize copied review whitespace for clean Curio PR

## Why

Five copied historical review reports contain Markdown hard-break trailing spaces that `git diff --check` rejects on the clean preproduction branch.

## Definition of done

- [x] All copied review lines preserve their wording, with no trailing spaces or tabs.

## Steps

- [x] Remove trailing blanks only from the five scoped review files.
- [x] Re-stage and run `git diff --cached --check`.

## How to verify

`git diff --cached --check` returns 0 after staging the five Markdown files.

## Notes

This is formatting only; no frozen episode script, claims, visuals or media changed.
