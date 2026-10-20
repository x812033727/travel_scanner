---
id: 2026-10-20-curio-s37-verify-2
title: Independent S37 exact-hash narrative and source/visual verification
status: done
priority: P2
area: docs
owner: codex-s37-r1
claimed_at: 2026-10-20T00:04:47Z
created_at: 2026-10-20T00:04:44Z
completed_at: 2026-10-20T00:18:40Z
branch: codex/curio-s34-endurance-20261019
depends_on: []
scope:
  - docs/videos/curio-s37/verify-2.md
---

# Independent S37 exact-hash narrative and source/visual verification

## Why

S37's pinned preproduction script needs a genuinely independent blind narrative pass and a fresh full-text source and visual audit before any paid media. The existing S37 task is intentionally broader; this ticket claims only the new review note.

## Definition of done

- [x] Record a 13-question blind verdict, 13 comprehension answers, pinned source check, and 95-line/92-prompt audit in `docs/videos/curio-s37/verify-2.md` against exact input hashes.

## Steps

- [x] Seal script-only answers before opening research, claims, earlier reviews, or source text.
- [x] Reopen and hash the pinned LXV/LXVI text; compare all line IDs, claim rows, and prompts.
- [x] Write the independent verdict and remaining blockers to the scoped note.

## How to verify

`sha256sum docs/videos/curio-s37/script.md docs/videos/curio-s37/video.json`; `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs narrative --slug curio-s37 --answers /tmp/s37-narrative-answers.json --json`; `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s37 --json`; `npm run check:tasks`.

## Notes

Claim used `--force` because the older, blocked S37 parent ticket scopes the whole directory. This delegated task owns only `verify-2.md`; it does not change the parent's script, JSON, claims table, or paid media. The blind pass was sealed at `/tmp/s37-blind-verify-2.md` before other S37 files were opened (SHA-256 `0a4b8cfa1827c7b39c1449dab2b3fd84839757408eb17b0e0fcc8f26d779b30e`).

Review complete at the frozen script/JSON hashes. Formal narrative verdict has 4 required no answers and 1 advisory no; source/visual blockers are recorded in `verify-2.md`. Video lint returned 0 errors/0 warnings, `npm run check:tasks` exited 0 with existing unrelated warnings. The S37 production gate remains blocked pending owner-side revision and a new hash review; this narrow ticket is ready for review in the parent change.
