---
id: 2026-10-19-independent-s31-frozen-script-source-and
title: Independent S31 frozen-script source and visual prompt gate
status: done
priority: P1
area: docs
owner: codex-s31-source-gate
claimed_at: 2026-10-19T23:54:20Z
created_at: 2026-10-19T23:54:16Z
completed_at: 2026-10-19T23:58:45Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s31/verify-2.md
---

# Independent S31 frozen-script source and visual prompt gate

## Why

The final S31 script passed an independent narrative read, but needs a separate check of its fixed primary texts, every narration/source mapping, and the ungenerated image prompts before media spending.

## Definition of done

- [x] Record a verdict tied to the frozen script hash and freshly downloaded full-text source hashes.
- [x] Check all 97 narration IDs across `script.md`, `claims.md`, and `video.json`, and all 96 image prompts.
- [x] Name any source or visual blockers for a later script/prompt revision without changing the frozen files or producing media.

## Steps

- [x] Reopen the four fixed full texts and inspect the seven anchored passages in their context.
- [x] Compare narration IDs and exact text, then review claim boundaries and prompts.
- [x] Write `docs/videos/curio-s31/verify-2.md` and run the structural lint.

## How to verify

`sha256sum docs/videos/curio-s31/script.md`; compare the four fresh-download hashes and cited lines in `docs/videos/curio-s31/verify-2.md`; `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`.

## Notes

Source gate is blocked by `ly006` merging Du Mu's horse with the later biography relay and `ly069` making Bai Juyi's fourth/fifth day sound additional to the first three. Further unsupported wording and pre-generation prompt fixes are itemized in `verify-2.md`. This ticket closes the **audit**; it does not clear S31 for audio or images. No script, media, or source notes were changed by this task.
