---
id: 2026-10-20-curio-s39-r3a-prompt-fix
title: Fix S39 R3a still prompts only
status: done
priority: P2
area: docs
owner: codex-s39-caesar
claimed_at: 2026-10-20T00:54:34Z
created_at: 2026-10-20T00:54:34Z
completed_at: 2026-10-20T00:56:03Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s39/video.json
  - docs/videos/curio-s39/verify-7.md
---

# Fix S39 R3a still prompts only

## Why

The R3 independent source and blind reviews passed, but 13 still prompts left some visible paper, book, scroll or tablet surface without an explicit blank requirement. The image model could invent legible historical text. This task is limited to those prompt strings.

## Definition of done

- [x] Only the 13 flagged `data.prompt` values change; all narration, claims, source, brief, music and other visual fields retain their R3 hashes/values.
- [x] Each flagged prompt tells the image model every visible document surface is blank or unmarked; lint remains 0 errors / 0 warnings.
- [x] Old independent audit receipt, new hash and independent focused recheck handoff are recorded before media.

## Steps

- [x] Read the R3 independent prompt findings and claim this narrow task.
- [x] Edit only the 13 specified prompts, regenerate `script.md` to confirm no narration drift, and lint.
- [x] Record `verify-7.md` and create the independent R3a prompt recheck task.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s39` leaves the script SHA unchanged; `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json` returns 0/0. Compare structured `video.json` against commit `0c234882` to prove exactly 13 `data.prompt` changes; all hashes in `docs/videos/curio-s39/verify-7.md`.

## Notes

Independent R3 narrative was 13/13 and source claims 89/89. Prompt review blocked 13/86 before image generation; author fixed the text but has not independently cleared it. New ticket: `2026-10-20-curio-s39-r3a-prompt-recheck`. No paid media.
