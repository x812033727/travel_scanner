---
id: 2026-10-20-s57-r4-independent-source-and-written
title: S57 R4 independent source and written visual audit
status: done
priority: P2
area: docs
owner: codex-s57-source
claimed_at: 2026-10-20T23:21:38Z
created_at: 2026-10-20T23:21:36Z
completed_at: 2026-10-20T23:24:25Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s57/review/r4-source-independent.md
---

# S57 R4 independent source and written visual audit

## Why

R3 was held because its February narration placed the recovered cloth bale before the earlier aid and medicine. R4 needs an independent source and written-visual verdict tied to its exact five-file freeze before other gates can use it.

## Definition of done

- [x] `docs/videos/curio-s57/review/r4-source-independent.md` records an exact-version PASS/HOLD with fixed-source lines, visual boundaries, hashes, and checks.

## Steps

- [x] Read R3 source HOLD, R4 author receipt and diff, all five R4 files, and both pinned source texts.
- [x] Check February chronology, chapter link, river claim, opening and revised prompts, 183/183 alignment, and every fixed claim link.
- [x] Run lint, docs-video tests, and task check; preserve creative files and paid media state.

## How to verify

`sha256sum docs/videos/curio-s57/{research.md,brief.md,claims.md,video.json,script.md}`; `node tools/video/cli.mjs lint --slug curio-s57 --json`; `npm run test:docs-videos`; `npm run check:tasks`. The review note records the pinned source-text hashes and line checks.

## Notes

PASS for the frozen R4 source and written-visual scope. February events are ordered 18 February aid, 19 February medicine chest, 20 February recovered bale. The 183 unique JSON scene lines match 183 claim rows and 183 script lines exactly. All 215 claim links use the two fixed commits and valid line ranges. Lint: 0 errors, 0 warnings; docs-video tests: 236 pass; task check: exit 0 with unrelated stale/scope warnings. The claims introduction still labels the candidate R1, a nonblocking stale label; future edits need a new freeze and audit. Two fresh blind narrative readers and later policy/media gates remain separate.
