---
id: 2026-10-20-s39-six-line-listener-rewrite-after
title: S39 six-line listener rewrite after audio QA
status: done
priority: P2
area: docs
owner: codex-s39-caesar
claimed_at: 2026-10-20T01:22:44Z
created_at: 2026-10-20T01:22:41Z
completed_at: 2026-10-20T01:37:57Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s39/video.json
  - docs/videos/curio-s39/script.md
  - docs/videos/curio-s39/claims.md
  - docs/videos/curio-s39/verify-10.md
---

# S39 six-line listener rewrite after audio QA

## Why

The exact R3a script passed independent preflight, but two targeted TTS redo
rounds left six Jev audio flags. Some flagged words change the meaning; the
episode cannot enter image generation on that audio. Simplify only those six
lines, then subject the new exact script to fresh independent review.

## Definition of done

- [x] Six smallest source-preserving line rewrites in `video.json` and matching
  `claims.md`, two corrected loop payoff pointers, with a regenerated
  `script.md` and 0/0 lint.
- [x] New hashes, audio failure evidence, and invalidated approval status are
  recorded in `verify-10.md`.
- [x] Fresh independent exact-version blind 13/13 and source/visual check pass,
  followed by focused review of the two metadata loop corrections.
- [x] Only after review, renew exact-script approval and redo affected audio,
  with a current zero-flag `check-audio` before images.

## Steps

- [x] Preserve the third audio check and six IDs from R3a.
- [x] Edit only six spoken lines, six matching claim rows, and two loop payoff
  pointers; regenerate script.
- [x] Arrange fresh independent R4 blind and source/visual audit; address the
  two loop pointer findings with an exact R4a focused recheck.
- [x] Resume TTS and audio QA only after exact R4 review passes.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s39`

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json`

`git diff --unified=0 -- docs/videos/curio-s39/video.json docs/videos/curio-s39/claims.md docs/videos/curio-s39/script.md`

## Notes

R3a approvals and narrative verdict are hash-bound and no longer valid for
R4. New video/script/claims hashes are in `verify-10.md`. The last old-script
audio is 561.4 seconds and its story body is 502.77 seconds; its six audio
flags were `cs010,cs021,cs036,cs049,cs079,cs084`. No paid images or music.
A fresh reviewer first judged R4 script-only blind 13/13 and the official
`narrative` import passed. The reviewer then found two imprecise loop payoff
pointers, so R4a changed only those metadata fields. Their focused recheck
passed. The exact R4a script SHA is now locally approved under delegated owner
instructions with a note that the owner did not personally read it. Do not use
the old audio as evidence for R4a.
The new R4a TTS reused 81 of 87 clips and generated 6; one line needed a
single targeted redo. Its last audio check passed 89/89 with 0 flags. The
current exact audio/timeline SHA and 8:25 story-body measurement are in
`verify-10.md`. The site audio card remains pending; a local approval was
recorded under delegated instructions, with an explicit note that the owner
did not personally listen.
