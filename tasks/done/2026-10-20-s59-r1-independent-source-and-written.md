---
id: 2026-10-20-s59-r1-independent-source-and-written
title: S59 R1 independent source and written visual audit
status: done
priority: P2
area: docs
owner: codex-s59-source-review
claimed_at: 2026-10-20T23:40:56Z
created_at: 2026-10-20T23:40:54Z
completed_at: 2026-10-20T23:42:12Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s59/review/r1-source-independent.md
---

# S59 R1 independent source and written visual audit

## Why

The frozen S59 R1 preproduction needs a reviewer independent of its author before its historical claims or written visuals can be treated as source verified. Its 1910 biography contains both Edison’s quoted retrospective and separate editor narration, so a link to the same book does not automatically establish the right witness tier.

## Definition of done

- [x] An exact five-hash PASS/HOLD receipt records primary text checks, claim/visual exceptions, reproducible source lines, and safe repair boundaries without changing creative files.

## Steps

- [x] Reopen the fixed 1878 French and 1910 English texts, verify raw SHA-256 values, and inspect the cited passages against all 110 scenes and their claims.
- [x] Recheck lint and scene count; write `docs/videos/curio-s59/review/r1-source-independent.md` with the R1 HOLD and exact narrow fixes.

## How to verify

`sha256sum docs/videos/curio-s59/{research.md,brief.md,claims.md,video.json,script.md}`; `sha256sum /tmp/s59_du_moncel_1878.txt /tmp/s59_edison_1910.txt` after refetching the fixed commits; `VIDEO_WORKDIR=/workspace/.video-work NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s59 --json` (0 errors, 0 warnings). Read the linked original lines and the written report, then `npm run check:tasks`.

## Notes

R1 HOLD: s59018 attributes the rapid paper strip’s audible note to Edison’s quoted E5195–5221, though it is in the biographers’ E5175–5184 narrative; s59019 mixes the same editorial contact lever with the quoted disk; s59057 makes an unsupported claim about survival of the original recording; s59069 invents Du Moncel’s standing position. The s59019 hand/fingertip picture also risks evoking the finger-prick myth expressly rejected at E5165–5173. Other event and machine claims are broadly supported with proper tiers. No paid media, creative edits, local approval or site mutation.
