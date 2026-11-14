---
id: 2026-10-21-curio-s38-r8g-pf004-narrow-author-repair
title: Narrowly repair S38 pf004 prompt after R8f native image rejection
status: done
priority: P2
area: docs
owner: codex-s38-r8g-author
claimed_at: 2026-10-21T00:19:00Z
created_at: 2026-10-21T00:19:00Z
completed_at: 2026-10-21T00:21:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/video.json
  - docs/videos/curio-s38/verify-17-r8g-author.md
  - docs/videos/curio-s38/verify-17-r8g-structured-diff.json
---

# Narrowly repair S38 pf004 prompt after R8f native image rejection

## Why

The first R8f pf004 take was a child-like medium portrait with nearby fire and modern-looking architecture. It failed the picture judge and direct native-image inspection.

## Definition of done

- [x] Replace only `pf004`'s prompt with a source-bound, full-figure adult in a wide 1666 London garden view and distant fire.
- [x] Freeze the exact five creative SHA-256 values, visual hash, and reversible one-leaf structured diff.
- [x] Preserve the STOP, media budget, existing media, and website review status without another paid call.
- [x] Record the R8g author handoff in [the receipt](../../docs/videos/curio-s38/verify-17-r8g-author.md).

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-s38 --json`; compare `video.json` with [the structured diff](../../docs/videos/curio-s38/verify-17-r8g-structured-diff.json) and reconstructed R8f SHA `084ff89c7df3dbfc0c150263eec6d96c3dabf85fc1baacd864a7e40f41416616`. The independent written-source and native-media gates remain separate.

## Notes

Paper author proposal only; one further pf004 native retry remains under the previously bounded pilot. No paid media or site approval occurred in this task.
