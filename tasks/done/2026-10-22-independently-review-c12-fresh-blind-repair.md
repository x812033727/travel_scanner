---
id: 2026-10-22-independently-review-c12-fresh-blind-repair
title: Independently review C12 fresh blind repair source visual delta
status: done
priority: P1
area: docs
owner: codex-c12-fresh-delta
claimed_at: 2026-10-22T16:37:50Z
created_at: 2026-10-22T16:36:54Z
completed_at: 2026-10-22T16:41:37Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v4.md
---

# Independently review C12 fresh blind repair source visual delta

## Why

The author revised 18 C12 Pyrex narration rows and nine matching visual rows after two fresh blind HOLD reviews. The new hashes require an independent source, causality, chronology, and visual consistency review before another gate.

## Definition of done

- [x] Save a new hash-bound PASS/HOLD verdict for every changed narration and visual ID.
- [x] Identify any newly introduced or newly exposed source conflict across adjacent rows.

## Steps

- [x] Confirm exact input hashes and compare all 80 row IDs against the prior reviewed head.
- [x] Reopen museum and Corning company sources, including sources about premarket home economists and Maltby's test kitchen.
- [x] Save receipt and run targeted mechanical checks.

## How to verify

`Get-FileHash` on both input files, per-ID Git row diff against `34d7753ed`, `git diff --check`, and `npm run check:tasks`.

## Notes

Direct museum source `Women and Pyrex` says Rorer and Maddocks received prototypes before market entry; the current E09→E10 narration places Corning's first turn to home economists after launch. Corning's own Maltby history says the test kitchen initially trained salesmen and only later tested products, whereas T11 immediately gives product evaluation as its task. Both the museum release and company history say the kitchen existed by 1931, not that its founding occurred precisely during 1931. A SHA-bound receipt will determine HOLD IDs. Preserve the two unrelated ghost tasks already in this checkout.

Receipt: `docs/videos/story-everyday-pyrex-c12-script/reviews/independent-source-visual-delta-v4.md`. E10, T09, T11 HOLD; 15 other changed narration IDs and nine changed visual prompts PASS. Input hashes match. `npm run check:tasks` remains red solely due the two pre-existing duplicate ghost IDs; their copies were preserved.
