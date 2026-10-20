---
id: 2026-10-20-curio-s39-r3-author-revision
title: Revise Curio S39 R3 after R2 audit
status: done
priority: P2
area: docs
owner: codex-s39-caesar
claimed_at: 2026-10-20T00:43:54Z
created_at: 2026-10-20T00:43:46Z
completed_at: 2026-10-20T00:48:48Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s39
---

# Revise Curio S39 R3 after R2 audit

## Why

S39 R2 independent blind reading passed 12/13 and failed `no_recap`: Greek-report qualification and Plutarch's missing quote were repeated. Source audit blocked Plutarch's statue scene being presented without its “Some say” caveat; prompt preflight found 21 stills with extra visible people, likely text, or insufficient action. The English-edition note was also described as at the “page bottom” although the pinned digital text collects its footnotes elsewhere.

## Definition of done

- [x] R3 has no repeated qualification or Plutarch summary, preserves “Some say”, and speaks precisely about the edition footnote.
- [x] All 21 R2 prompt issues receive R3 text revisions while retaining one-to-one claim/still mapping and at least eight minutes of estimated story body.
- [x] Final R3 hashes and the R2 review receipt are recorded, with a fresh independent review queued before media.

## Steps

- [x] Claim this narrow task; read both sealed R2 reports and re-open relevant pinned source lines.
- [x] Revise source-bounded script, still prompts, brief/research, and regenerate script/claims from R3 video JSON.
- [x] Run lint, docs tests, mapping checks; write `verify-5.md` and the R3 independent review task.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json` (0 errors / 0 warnings); `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s39`; `npm run test:docs-videos` (236/236); `npm run check:tasks`; SHA-256 values in `docs/videos/curio-s39/verify-5.md`.

## Notes

R2 reports are `/tmp/curio_s39_r2_fresh_blind_seal.md` and `/tmp/curio_s39_r2_source_visual_audit.md`. R3 is an author candidate only, with 89 spoken lines, 86 unique nonblank still prompts, 12 loops, and estimated 8:23 body. No paid media or owner approval was claimed. R3 fresh blind/source/still task is `2026-10-20-curio-s39-r3-independent-review`.
