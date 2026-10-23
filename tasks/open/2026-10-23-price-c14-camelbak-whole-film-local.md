---
id: 2026-10-23-price-c14-camelbak-whole-film-local
title: Price C14 CamelBak whole-film local pilot
status: review
priority: P1
area: docs
owner: codex-root-c14-quote
claimed_at: 2026-10-23T04:41:58Z
created_at: 2026-10-23T04:41:16Z
completed_at:
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/production-quote.md
---

# Price C14 CamelBak whole-film local pilot

## Why

C14's script and visual direction are owner approved, but no whole-film quantity or dollar ceiling is approved. Quote the exact current bytes and check the timing denominator before asking for paid work.

## Definition of done

- [x] Count all 70 shots, distinct image upper bound, retry cap, cards, narration and music.
- [x] Reopen current official image, image-judge and music pricing; include unattributed TTS/ASR and other charges inside a whole-film hard stop.
- [x] Recompute the post-hook body duration and illustrated-time proxy from JSON rather than repeating a whole-voice figure as body.
- [ ] Push the nonpaid quote in the existing draft PR and read back draft/no-auto-merge.

## Steps

- [x] Bind approved script and visual hashes.
- [x] Document the 63-image/189-attempt estimate and US$25 proposal.
- [ ] Run checks, push, and update PR status text.

## How to verify

Recompute script/visual SHA-256 and parse `visual-plan.json`: 70 rows, 54 illustrations, 16 cards, 496.5 seconds all narration, 40.3 seconds H01–H05, 456.2 seconds post-hook body, 333.0 illustrated body seconds. Verify public [MiniMax pricing](https://platform.minimax.io/docs/pricing/overview) and [Google pricing](https://ai.google.dev/gemini-api/docs/pricing), run `npm run check:tasks` and `git diff --check`, then read back PR #1695 state.

## Notes

2026-10-23: The prior PR body and owner approval receipt called the 496.5-second whole spoken plan "body". Direct JSON arithmetic shows actual planned post-hook body is only 456.2 seconds; this is a paper estimate, not a TTS failure. The quote corrects the denominator without changing approved script or visuals. The code in this branch has no C14 per-episode budget slug; production ledger and prior charges remain unread, so no paid request may start.

2026-10-23 checks: `git diff --check` passed. `npm run check:tasks` exited 1 only because this worktree already contains an untracked `tasks/open/2026-10-22-independently-verify-c14-camelbak-v4-source.md` alongside its untracked `tasks/done/` copy; it is not part of this quote. The prior agent reported exact removal was policy-blocked. Both copies are left untouched and excluded from this PR. Existing queue overlap/stale-owner warnings are not this quote's changes.
