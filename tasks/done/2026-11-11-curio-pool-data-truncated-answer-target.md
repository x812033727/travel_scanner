---
id: 2026-11-11-curio-pool-data-truncated-answer-target
title: Curio pool data: truncated answer_target, placeholder scope, missing ids found by the material review
status: done
priority: P2
area: docs
owner: claude-opus-cloud-channel-review
claimed_at: 2026-11-11T02:16:53Z
created_at: 2026-11-11T02:15:11Z
completed_at: 2026-11-11T02:33:07Z
branch: claude/youthful-albattani-m1ih5z
depends_on: []
scope:
  - docs/videos/history-curiosity/pool
  - tools/video/curio/pool
---

# Curio pool data: truncated answer_target, placeholder scope, missing ids found by the material review

## Why

The 2026-11-11 material review (`docs/videos/history-curiosity/pool/reviews/material-20261111.md`, section 資料問題) found
data problems that made reviewers fall back on other files:

- About 30 candidates have `answer_target` cut off at exactly 800 characters (M10, M12, M14, L14, P09–P13, P16, U10, U15, and others). The full findings exist only in `topic-checks/*.md`.
- The same legacy-checked candidates still carry the old 「待查：…」 placeholder in `scope` instead of real limits.
- Notes cite ids that do not exist (N1224, P30, P03). P19 and P20 are said to be merged into P13, but none of their material is in P13. N191's suggested partner P25 is excluded.
- In the T88–T112 slice, every `source_refs` entry of a candidate shares one `locator` string, so no fact can be tied to its source.

## Definition of done

- [x] `answer_target` is no longer truncated (find where the 800-character cut happens in `tools/video/curio/pool/core.mjs` intake, or store the full text), and the export is rebuilt.
- [x] Legacy scopes are filled from their topic-checks, or marked plainly as not yet scoped.
- [x] The dangling ids are resolved or removed from notes. P19/P20 material is restored or the merge note is corrected.
- [x] `node tools/video/curio/pool/cli.mjs check` and `node --test tools/video/curio/pool/pool.test.mjs` pass.

## Notes

Filed by the channel review session (draft PR #2069).
- Done 2026-11-11:
  - The 800-character cut in `core.mjs` is removed, which affected 30 ids (the longest is now M14 at 1,588 characters).
  - Scope comes from the topic-checks' limit sections for 76 ids. The rest is marked `scope_status: not_yet_scoped`.
  - The dangling-id notes are corrected. No material was invented: P19 and P20 are cards only, so T24's empty 1919 chapter was cut.
  - `splitLocator` now gives each source its own locator.
  - selection revision `2026-11-11-curio-pool-761`. Counts are unchanged; `cli.mjs check` passes and pool.test passes 23/23.
- Left for a new task: other dangling ids (N194, N210) and the old revision stamps in topics.json.
