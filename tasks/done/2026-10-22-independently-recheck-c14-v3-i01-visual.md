---
id: 2026-10-22-independently-recheck-c14-v3-i01-visual
title: Independently recheck C14 v3 I01 visual card
status: done
priority: P2
area: docs
owner: codex-c14-v3-visual-recheck
claimed_at: 2026-10-22T17:54:02Z
created_at: 2026-10-22T17:53:57Z
completed_at: 2026-10-22T17:54:48Z
branch: codex/brand-story-camelbak-c14-treatment
depends_on: []
scope:
  - docs/videos/story-everyday-camelbak-c14/reviews/independent-v3-i01-visual-recheck.md
---

# Independently recheck C14 v3 I01 visual card

## Why

The v2 independent review held I01 because its founding-year card could contradict the adjacent attributed 1989 race card. The author changed only the I01 post-produced text and matching visual-plan explanation, so a separate reviewer must bind the repair verdict to the new visual hashes.

## Definition of done

- [x] A review-only receipt gives an independent PASS/HOLD on the v3 I01 repair, O10 pairing, and Curio card rules, tied to exact visual hashes and PR head.

## Steps

- [x] Compare author v3 visual diff with the v2 HOLD and verify script/notes bytes unchanged.
- [x] Parse current JSON for I01/O10, shot mapping, look, cards, durations, and prompt constraints.
- [x] Push only the receipt and task to PR #1695; update and read back its body.

## How to verify

`Get-FileHash` on six bound files; `git diff ba25e4aad 7caee78c8 -- visual-plan.md visual-plan.json`; parse `visual-plan.json` against script IDs; `npm run check:tasks`; `git diff --cached --check`; read back `gh pr view 1695 --json headRefOid,isDraft,labels,body`.

## Notes

Receipt: `docs/videos/story-everyday-camelbak-c14/reviews/independent-v3-i01-visual-recheck.md`. I01 is now a founding-year-only card, so it no longer denies O10's separately attributed brand recollection. Visual text PASS only; unchanged v2 source PASS still binds the old script/notes hashes. Do not promote this to blind narration, TTS, generated-image, owner, or paid-work approval. No blind-review content was read.
