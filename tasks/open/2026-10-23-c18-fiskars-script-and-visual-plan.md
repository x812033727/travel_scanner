---
id: 2026-10-23-c18-fiskars-script-and-visual-plan
title: C18 Fiskars script and visual plan
status: review
priority: P2
area: docs
owner: codex-c18-script
claimed_at: 2026-10-23T03:56:11Z
created_at: 2026-10-23T03:55:51Z
completed_at:
branch: codex/brand-story-fiskars-c18-script
depends_on: []
scope:
  - docs/videos/story-everyday-fiskars-c18/script.md
  - docs/videos/story-everyday-fiskars-c18/source-notes.md
  - docs/videos/story-everyday-fiskars-c18/visual-plan.md
  - docs/videos/story-everyday-fiskars-c18/visual-plan.json
  - docs/videos/story-everyday-fiskars-c18/reviews/author-preflight.md
---

# C18 Fiskars script and visual plan

## Why

The owner adopted the independently checked C18 treatment in draft PR #1702. The episode still needs a source-bound narration script and one-to-one unpaid shot directions before independent script review, two narration-only blind reads, and the separate owner script gate.

## Definition of done

- [ ] An independently source/visual-audited, two-reader narration-blind-checked C18 script is ready for the owner to review. This task currently delivers only the author's draft; the external checks are separate scope and PR work.

## Steps

- [x] Draft a six-chapter, chronological script against adopted M01–M12 with per-line source mapping.
- [x] Write a one-to-one original illustration/card plan, with Curio visual constraints and unpaid status explicit.
- [x] Document evidence boundaries and prepare author structural preflight.
- [ ] Obtain independent source/paired-visual audit and two genuine narrator-only blind reads on final script bytes.
- [ ] Present the reviewed script/shot direction to the owner for approval; separately price any local pilot later.

## How to verify

`npm run check:tasks`, `npm run test:docs-videos`, JSON parse plus script/shot ID and prohibited prompt-token checks, and `git diff --check`. These checks establish structure, not fact review or story quality. Independent agents must read the original sources and narration-only copy before owner review.

## Notes

Base is adopted C18 Treatment PR #1702 at c82b34811; independent Treatment source review #1706 PASS. Initial 85-line draft source/paired-visual review PR #1717 eventually passed the four initial factual fixes plus two removed historical table-position assertions. Two genuinely isolated narration-only readers on that prior draft filed HOLD in draft PRs #1722 and #1723: one-line story, no table of contents, no recap, and no detour all failed; reader 1 also marked chapter links NO. The author therefore rewrote the same draft PR #1711 around one continuous orange-grip problem. This version has 66 narration lines, 56 concept illustration shots, and 10 postproduction cards, with 1:1 IDs. MoMA's 1976 object is now a single chronological material-evidence beat; the end returns to the opening drawer without a date puzzle or repeated factual audit. The changed four input bytes require a **fresh full independent source/paired-visual audit and two new blind reads**; earlier PASS/HOLD receipts do not approve this revision. No TTS or images have been purchased. Finnish/US registration dates remain company-yearbook claims, Canadian CIPO scope remains particular handles' whole visible surface, and body duration/image screen-time share are unmeasured. Exact input hashes and check results are in `reviews/author-preflight.md`.
