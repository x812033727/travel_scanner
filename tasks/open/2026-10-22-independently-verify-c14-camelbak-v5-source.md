---
id: 2026-10-22-independently-verify-c14-camelbak-v5-source
title: Independently verify C14 CamelBak v5 source and visuals
status: review
priority: P1
area: docs
owner: codex-c14-independent-v5
claimed_at: 2026-10-22T18:36:59Z
created_at: 2026-10-22T18:36:53Z
completed_at:
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/reviews/independent-v5-source-visual-review.md
---

# Independently verify C14 CamelBak v5 source and visuals

## Why

C14 CamelBak v5 author repair changed the narration and visual files after the exact-hash v4 HOLD. A different reviewer must reopen the cited originals and recheck all 74 narration/shot IDs against the new hashes before the story can advance.

## Definition of done

- [x] A new exact-hash independent v5 PASS/HOLD receipt is committed in the narrow review scope, with direct source links and actionable line/shot IDs.
- [x] Draft PR #1695 records the v5 result without merging or approving the author稿.

## Steps

- [x] Reopen CamelBak history, patents, 2003 report, 2006 trade-show report, 2007 release and 2014 10-K.
- [x] Recheck the v4 HOLDs, v5 adjacent claims, 74 shot IDs, visual prompts and duration arithmetic.
- [x] Record the single new O02 source HOLD and leave author files untouched.

## How to verify

Read `docs/videos/story-everyday-camelbak-c14/reviews/independent-v5-source-visual-review.md`; compare its six hashes with `Get-FileHash -Algorithm SHA256` on the named files. `git diff --check` verifies the receipt patch. Read back PR #1695 head, draft flag and `no-auto-merge` label after push.

## Notes

v5 repaired every enumerated v4 HOLD, including I10 fax orders and T05 filing/grant chronology. Fresh direct-source check found O02 claims a frame bottle remained on Eidson's particular ride; the brand history has no such detail, and O02 visual repeats it. Overall source/visual decision remains HOLD pending a narrow O02 narration and prompt repair. No paid media, merge, upload or self-approval. The old v4 task's two untracked copies remain in `tasks/open/` and `tasks/done/`; the exact deletion attempt was blocked by policy, so leave both untouched. Local `check:tasks` may fail on that unrelated duplicate task ID.
