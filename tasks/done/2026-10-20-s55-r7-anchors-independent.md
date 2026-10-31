---
id: 2026-10-20-s55-r7-anchors-independent
title: S55 R7 three anchor independent recheck
status: done
priority: P2
area: docs
owner: codex-gpt6-s55-r7-anchor-review
claimed_at: 2026-10-20T21:06:36Z
created_at: 2026-10-20T21:06:34Z
completed_at: 2026-10-20T21:07:44Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s55/review/r7-anchors-independent.md
---

# S55 R7 three anchor independent recheck

## Why

The R6 source reviewer found three claims rows whose spoken facts were supported in fixed sources but whose links missed the exact lines. R7 added the links. Independently verify the three-cell diff and the source wording before removing the claims HOLD.

## Definition of done

- [x] Independent report records a PASS/HOLD verdict tied to exact five-file hashes.

## Steps

- [x] Redownload fixed F and M originals; verify hashes and read the three cited line spans.
- [x] Reverse only three new links to reproduce R6 claims SHA; verify unchanged other files, alignment and lint.

## How to verify

See `docs/videos/curio-s55/review/r7-anchors-independent.md` for SHA-256 and line spans. Run `VIDEO_WORKDIR=/tmp/curio-s55-r7-anchor-check NODE_USE_ENV_PROXY=1 NODE_NO_WARNINGS=1 node tools/video/cli.mjs lint --slug curio-s55 --json`, `git diff --check`, and `npm run check:tasks`.

## Notes

The narrow claims citation HOLD is lifted. Narration and visual prompts did not change. Fresh R6/R7 script blind readers remain necessary; no TTS or art was started by this task.
