---
id: 2026-10-12-scrub-local-path-from-completed-curio
title: Scrub local path from completed Curio handoff
status: done
priority: P2
area: docs
owner: codex-curio-root-8bc3
claimed_at: 2026-10-12T17:46:58Z
created_at: 2026-10-12T17:46:49Z
completed_at: 2026-10-12T17:47:43Z
branch: codex/curio-five-recuts-20261012
depends_on: []
scope:
  - tasks/done/2026-10-12-curio-five-recuts.md
---

# Scrub local path from completed Curio handoff

## Why

The earlier completed Curio handoff recorded a local Windows profile path in
the public repository. The repository hygiene check correctly rejects it.

## Definition of done

- [x] The completed handoff uses a portable home-directory placeholder and
      no longer exposes one person's Windows profile path.

## Steps

- [x] Locate the offending line in the completed Curio task.
- [x] Replace only that line with a portable placeholder.

## How to verify

Run `node --test tools/repo-hygiene.test.mjs` after the separate Curio docs
cleanup under its active upload task has removed its remaining path findings.

## Notes

The source files live outside Git. This change alters the public handoff text,
not a media path, source hash, or executable runner.
