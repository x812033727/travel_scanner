---
id: 2026-10-21-curio-s38-r8k-pf007-author
title: Repair S38 pf007 composition after one native image rejection
status: done
priority: P2
area: docs
owner: codex-root
claimed_at: 2026-10-21T00:41:00Z
created_at: 2026-10-21T00:41:00Z
completed_at: 2026-10-21T00:43:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/video.json
  - docs/videos/curio-s38/verify-26-r8j-pf007-native-stop.md
  - docs/videos/curio-s38/verify-27-r8k-pf007-author.md
  - docs/videos/curio-s38/verify-27-r8k-structured-diff.json
---

# Repair S38 pf007 composition after one native image rejection

## Why

The bounded R8j pf007 image scored 9.71 but failed the frame question for dark bands. It cannot enter the approved storyboard. A prompt-only composition revision needs an exact diff and independent review before another paid attempt.

## Definition of done

- [x] Preserve STOP and record the native image, judge result, ledger and old pf003 reservation.
- [x] Change only pf007's prompt, with D2a event and Curio style preserved.
- [x] Reconstruct R8j SHA exactly, write structured diff, freeze R8k hash and lint.

## How to verify

Read [the native stop](../../docs/videos/curio-s38/verify-26-r8j-pf007-native-stop.md) and [author receipt](../../docs/videos/curio-s38/verify-27-r8k-pf007-author.md); run `node tools/video/cli.mjs lint --slug curio-s38 --json` and `npm run check:tasks`. No R8k media generation was performed by this task.
