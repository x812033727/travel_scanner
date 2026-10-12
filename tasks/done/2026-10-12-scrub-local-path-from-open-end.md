---
id: 2026-10-12-scrub-local-path-from-open-end
title: Scrub local path from open end-screen task
status: done
priority: P2
area: docs
owner: codex-curio-root-8bc3
claimed_at: 2026-10-12T17:48:53Z
created_at: 2026-10-12T17:48:43Z
completed_at: 2026-10-12T17:49:30Z
branch: codex/curio-five-recuts-20261012
depends_on: []
scope:
  - tasks/open/2026-10-12-correct-v4-youtube-end-screen-timing.md
---

# Scrub local path from open end-screen task

## Why

The open end-screen task includes one user's local Windows profile path in a
public repository ticket, which fails the repo hygiene check.

## Definition of done

- [x] The ticket identifies its evidence with a portable home placeholder.

## Steps

- [x] Find the one path in the existing open task.
- [x] Replace it without changing the task's status or end-screen scope.

## How to verify

Run `node --test tools/repo-hygiene.test.mjs` after the separate Curio docs
cleanup removes the remaining findings.

## Notes

The original task remains open for the shared v4 guidance change. This scrub
changes no media, owner decision or timing evidence.
