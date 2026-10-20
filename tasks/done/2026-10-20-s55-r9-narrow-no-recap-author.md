---
id: 2026-10-20-s55-r9-narrow-no-recap-author
title: S55 R9 narrow no recap author repair
status: done
priority: P2
area: docs
owner: codex-s55-r9-author
claimed_at: 2026-10-20T21:22:16Z
created_at: 2026-10-20T21:22:14Z
completed_at: 2026-10-20T21:27:17Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/video.json
  - docs/videos/curio-s55/claims.md
  - docs/videos/curio-s55/script.md
  - docs/videos/curio-s55/brief.md
  - docs/videos/curio-s55/research.md
  - docs/videos/curio-s55/review/r9-author-fix.md
---

# S55 R9 narrow no recap author repair

## Why

R8 passed independent source and written visual review, but two isolated readers both found repeated facts and the official narrative gate failed `no_recap`. A narrow rewrite must preserve the sourced story and eight-minute body.

## Definition of done

- [x] Freeze an R9 draft that removes the shared repeated facts, stays above eight minutes at the fastest text estimate, and has zero lint errors or warnings.

## Steps

- [x] Remove the two redundant scenes and rewrite the cited callbacks/transitions in `video.json` and `claims.md`.
- [x] Regenerate `script.md`, update the brief status, and record five exact hashes in the author receipt.

## How to verify

Run `node tools/video/cli.mjs script --slug curio-s55` and `VIDEO_WORKDIR=/tmp/curio-s55-r9-author node tools/video/cli.mjs lint --slug curio-s55 --json`; check 138/138 claim texts, 2625 body Han characters, and `npm run check:tasks`.

## Notes

R9 author freeze is `docs/videos/curio-s55/review/r9-author-fix.md`. Research is unchanged. Lint 0/0; fastest body 8.08 min. The remaining 25-character margin is thin, so further cuts need sourced new action/detail. Independent source/visual and two fresh isolated narrative readers are the next gates. No TTS, imagery, music, or film made.
