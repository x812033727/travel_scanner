---
id: 2026-10-20-s52-r16-source-independent
title: S52 R16 independent source and visual diff review
status: done
priority: P2
area: docs
owner: codex-gpt6-root
claimed_at: 2026-10-20T21:01:32Z
created_at: 2026-10-20T21:01:30Z
completed_at: 2026-10-20T21:02:59Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s52/review/r16-source-independent.md
---

# S52 R16 independent source and visual diff review

## Why

R16 changed 18 flagged lines to clearer spoken Chinese. R15 source approval is hash-bound; independently recheck those changes against the fixed Cook, Kippis, and 1771 Royal Society texts and verify visuals did not change.

## Definition of done

- [x] Exact R16 source/claim/visual differential review saved in `docs/videos/curio-s52/review/r16-source-independent.md` with a clear gate result.

## Steps

- [x] Verify five current hashes, fixed source hashes, and reconstruct R15 video/claims hashes from 18 old lines.
- [x] Recheck changed factual wording and line/claims alignment; run video lint.

## How to verify

`sha256sum docs/videos/curio-s52/{brief.md,research.md,claims.md,video.json,script.md}`; `VIDEO_WORKDIR=/workspace/.video-work NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s52 --json`; `git diff --check`.

## Notes

R16 source, claims, and unchanged written visuals PASS. R16 narrative blind reads and new TTS remain separate HOLD gates. R15 audio cannot be reused.
