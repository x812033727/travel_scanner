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

Base is adopted C18 Treatment PR #1702 at c82b34811; independent Treatment source review #1706 PASS. Initial 85-line draft source/paired-visual review PR #1717 eventually passed four factual fixes plus removal of unsupported table-position assertions. Two genuinely isolated narration-only readers on that prior draft filed HOLD in #1722 and #1723, so the author rewrote PR #1711 around one continuous orange-grip problem. The 66-line rewrite received full independent source/visual PASS in #1727, but two new isolated narration-only readers #1730 and #1731 still filed HOLD: both found the MoMA/left-hand to U.S. factory to trademark bridge abrupt, and one found the Canadian legal phrasing difficult to hear. Its posthook body was only 1,414 nonblank characters, paper ~339 seconds at 0.24 seconds/character.

This same author PR now has 78 narration lines, 67 original concept illustration directions and 11 postproduction cards, with 1:1 IDs. The factory step now tracks the same orange-handled product: Fiskars 2011 annual report says it was first made in the village's old coppersmith's shop and later a new Billnäs factory; Fiskars 2005 corporate release says orange-handled scissors had been made in the U.S. since 1978, after the company's reported 1977 U.S. scissors factory. Both newly used company sources are identified as S13/S14, without inventing a Billnäs date or treating color as the cause of sales. Canada's CIPO goods, particular pictured handles, and whole visible surface are split into shorter spoken lines; Finnish/U.S. registration dates stay company-report claims, and the Canadian scope is not generalized to them. The 1976 MoMA object is only material evidence and is not described as orange or the 1967 prototype. No TTS or images have been purchased.

**Current gate: HOLD.** This 78-line revision has 1,803 posthook nonblank characters, paper ~433 seconds at the old 0.24 seconds/character estimate, so it does not plausibly prove the required 480-second body. Do not pad with unsupported facts or buy images. All four changed input files need a fresh independent full source/paired-visual review and two fresh genuinely narration-only blind readers; prior PASS/HOLD receipts do not approve these bytes. Actual TTS duration and illustration screen-time share remain unmeasured. Exact four SHA-256s and author check results are in `reviews/author-preflight.md`. Keep #1711 draft with the actual `no-auto-merge` GitHub label. Do not present this script as owner-approved.
