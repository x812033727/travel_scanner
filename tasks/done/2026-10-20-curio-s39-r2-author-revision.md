---
id: 2026-10-20-curio-s39-r2-author-revision
title: Revise S39 Caesar R2 after independent review
status: done
priority: P2
area: docs
owner: codex-s39-caesar
claimed_at: 2026-10-20T00:28:51Z
created_at: 2026-10-20T00:28:48Z
completed_at: 2026-10-20T00:36:45Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s39
---

# Revise S39 Caesar R2 after independent review

## Why

R1's independent blind and source review blocked S39. It gave away the answer in the opening, wandered into unrelated aftermath, and misstated the scope of Suetonius's groan, Shakespeare's English final line, and the later translator's footnote. The still audit also found ambiguous Brutus identities and Cimber's action.

## Definition of done

- [x] R2 has a source-bounded, one-thread script of at least eight minutes of story body, with corrected ancient and stage language layers.
- [x] Claims, prompts, script and source memo correspond to the final R2 `video.json`; lint gives 0 errors and 0 warnings.
- [x] R2 is explicitly handed to a fresh independent narrative/source/still review before any media generation.

## Steps

- [x] Read R1 sealed blind and source/still audits; revise story line and visual prompts.
- [x] Reopen fixed source excerpts needed for revisions, correct `research.md` and `brief.md`, regenerate claims and script.
- [x] Record final hashes, estimates, tests, and production gate in `verify-3.md`; file R2 review task.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s39 --json` (0/0); `VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs script --slug curio-s39`; `npm run test:docs-videos` (236/236); `npm run check:tasks` (exit 0). The final SHA-256 values are recorded in `verify-3.md`.

## Notes

R2: 89 spoken lines; 86 unique nonblank still prompts; estimated story body 8:21, full 9:18. No paid media. Live `keyframes --dry-run` site quote failed because `https://mokaair.com` was unreachable; image/music cost in `verify-3.md` is a proportionate estimate from R1, not a quote. The unclaimed R2 review task is `2026-10-20-curio-s39-r2-independent-review`.
