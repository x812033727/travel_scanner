---
id: 2026-10-15-remove-machine-specific-paths-from-h09
title: Remove machine-specific paths from H09 localization tickets
status: done
priority: P2
area: meta
owner: codex-gpt6-h09-ci-hygiene
claimed_at: 2026-10-15T09:23:13Z
created_at: 2026-10-15T09:22:58Z
completed_at: 2026-10-15T09:25:44Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - tasks/open/2026-10-15-h09-en-localization.md
  - tasks/open/2026-10-15-h09-ja-localization.md
  - tasks/open/2026-10-15-h09-ko-localization.md
---

# Remove machine-specific paths from H09 localization tickets

## Why

CI's repo-hygiene test rejected three H09 localization tickets because their verification commands included a contributor's absolute media path. The commands should work from any checkout with its own video media directory.

## Definition of done

- [x] All three tickets describe `VIDEO_WORKDIR` without an absolute path, and the focused repo-hygiene test passes.

## Steps

- [x] Replace only the machine-specific path examples in the English, Japanese, and Korean tickets.
- [x] Run the focused test and diff whitespace check.

## How to verify

`node --test tools/repo-hygiene.test.mjs` and `git diff --check` both exit 0.

## Notes

The localization tickets retain their original owners, statuses, and i18n JSON scopes. The English and Japanese verification preambles now name the media root containing `curio-h09`; the Korean commands use the same preamble instead of repeating the local path. This ticket remains open until its changes are committed with the H09 draft PR.
