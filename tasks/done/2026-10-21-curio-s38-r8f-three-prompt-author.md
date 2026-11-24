---
id: 2026-10-21-curio-s38-r8f-three-prompt-author
title: Adopt three independently reviewed S38 prompt candidates as R8f
status: done
priority: P2
area: docs
owner: codex-s38-art-continuation
claimed_at: 2026-10-21T00:07:00Z
created_at: 2026-10-21T00:07:00Z
completed_at: 2026-10-21T00:10:00Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s38/video.json
  - docs/videos/curio-s38/verify-15-r8f-author.md
  - docs/videos/curio-s38/verify-15-r8f-structured-diff.json
---

# Adopt three independently reviewed S38 prompt candidates as R8f

## Why

Native images of `pf004/005/006` failed historical and series visual checks. A separate paper review passed narrow replacements for those three shots.

## Definition of done

- [x] Adopt only the three reviewed `data.prompt` leaves into R8f.
- [x] Preserve the spoken script, claims, research, brief, look, existing media and STOP.
- [x] Freeze five SHA-256 values, visualHash, complete before/after JSON diff and next independent review boundary in [verify-15-r8f-author.md](../../docs/videos/curio-s38/verify-15-r8f-author.md).

## How to verify

Compare [structured diff](../../docs/videos/curio-s38/verify-15-r8f-structured-diff.json) to Git R8e, rerun `lint --slug curio-s38 --json`, and check `/workspace/.video-work/curio-s38/STOP` remains present. No paid media or site approvals were changed.

## Notes

The separate main S38 video task remains open. R8f is held for independent exact-delta source and visual review before any new native pilot.
