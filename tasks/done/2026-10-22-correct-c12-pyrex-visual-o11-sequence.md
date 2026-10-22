---
id: 2026-10-22-correct-c12-pyrex-visual-o11-sequence
title: Correct C12 Pyrex visual O11 sequence and N14 overlay
status: done
priority: P1
area: docs
owner: codex-c12-visual-author
claimed_at: 2026-10-22T15:14:15Z
created_at: 2026-10-22T15:13:55Z
completed_at: 2026-10-22T15:15:37Z
branch: codex/brand-story-pyrex-c12-script
depends_on: []
scope:
  - docs/videos/story-everyday-pyrex-c12-script/visual-plan.md
---

# Correct C12 Pyrex visual O11 sequence and N14 overlay

## Why

The independent C12 script delta review on PR #1692 held the O11 visual: it placed an intact ceramic dish at dinner before O12 showed its earlier oven shattering, reversing the museum account. N14's note also called an illustration overlay a separate postproduction card, leaving its card count ambiguous.

## Definition of done

- [x] O11 shows an anonymous dinner conversation without an intact ceramic baking dish, and O12 is explicitly cued as a memory of earlier breakage.
- [x] N14 clearly remains an illustration with only an optional later on-image text overlay; 80 IDs, 67 illustrations, 13 cards, and narration bytes stay unchanged.

## Steps

- [x] Compare O11/N14 against the independent SHA-bound review and Corning Museum source chronology.
- [x] Revise only O11 and N14 visual-plan rows.
- [x] Verify IDs/counts/hashes and push a draft PR update for a fresh independent delta review.

## How to verify

`git diff --check`; compare `Get-FileHash` of `script.md` with the prior `491AEE730835B0FFC6AC034E544AF25BB257C0CAD354BF0FC845DB8376411036`; parse the chapter tables for 80 matching IDs, 67 I/13 C and max two consecutive C; inspect `git diff -- visual-plan.md` for O11/N14 only; verify draft PR head after push.

## Notes

Corning Museum of Glass S1: https://blog.cmog.org/2015/beginning-pyrex. Its retrospective says the ceramic dish shattered in the oven before Bessie discussed it at dinner. The picture is an anonymous conceptual illustration, not a reconstruction. The reviewer-owned untracked task ghost with `independently-audit` in its name belongs to another agent and must not be deleted. No paid generation or owner script approval is part of this task.

Verification before commit: `git diff --check` passed; narration SHA-256 remains `491AEE730835B0FFC6AC034E544AF25BB257C0CAD354BF0FC845DB8376411036`; revised visual SHA-256 is `CB61FB065072CD9B3BA100CBBA087CBFB85D70386A1D86D432804CEF399FD122`; table parse found 80/80 identical unique IDs, 67 illustrations, 13 cards and max two consecutive cards. Reviewer must recheck the new visual bytes independently; this ticket does not grant script approval.
