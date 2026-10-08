---
id: 2026-10-07-correct-japan-entry-customs-source-before
title: Correct Japan entry customs source before localization
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-07T08:30:15Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/japan-entry-2026-visit-japan-web.json
  - docs/article-localization/japan-entry-source-review-20261007.md
---


# Correct Japan entry customs source before localization

## Why

The actual published zh-TW source contains a clickable Machine Learning article
inside the unit760 ml, overgeneralizes medicines to two months, lists all guns
and swords as absolutely prohibited, and omits the form/purity scope of the1kg
gold declaration threshold. These errors must not be reproduced in four new
languages. The10,000yen duty-free exclusion also needs category-aggregate wording.

## Definition of done

- [ ] A distinct source writer proposes only the exact verified source changes;
      a genuine independent full-source review approves final document/assets.
- [ ] The760 ml unit is plain text, not an article link; other inlines stay exact.
- [ ] Medicines distinguish prescription/poisonous/powerful one-month and other
      medicine two-month self-use import-confirmation exemptions, plus applicable
      topical/cosmetic category limits; larger imports are not labelled impossible.
- [ ] Prohibited firearms and regulated gun/sword imports are distinguished.
- [ ] Gold declaration specifies bullion of at least90% purity exceeding1kg;
      duty-free10,000yen exclusion is aggregated per品目, not per individual object.
- [ ] Original database identities/versions, photos, valid_until and unrelated
      source/metadata remain pinned; source correction is independently verified.
- [ ] The four missing target languages resume only after genuine source approval;
      publication and public verification remain separate guarded release work.

## Steps

- [ ] Claim after verifying actual worktree/remote/PR ownership and fresh source.
- [ ] Preserve the original baseline and all failure/source evidence.
- [ ] Propose changes to blocks10/inlines1 and2, sources10/title and blocks4/rows4/2.
- [ ] Independently review, verify source_correction and precisely apply/install.
- [ ] Explicitly resolve existing repository-only description preservation before
      assembly; do not silently overwrite its accepted answer-first rewrite.

## How to verify

Read the full article, original and final SVG/photos, and primary Customs pages:
https://www.customs.go.jp/tetsuzuki/c-answer/imtsukan/1806_jr.htm
https://www.customs.go.jp/tetsuzuki/c-answer/imtsukan/1809_jr.html
https://www.customs.go.jp/mizugiwa/kinshi.htm
https://www.customs.go.jp/kaigairyoko/shiharaishudan.htm
https://www.customs.go.jp/kaigairyoko/menzei.htm
Use the unchanged official source-correction verifier, pack lint, source/media
preservation checks and exact independent review bindings. No target translation
may hide a different rule from an uncorrected original.

## Notes

The read-only independent source FAIL receipt SHA is
`0f987008c2ed1311f85f3ca285c20418288e4d3aa72be388628c6467474749b6`;
complete evidence SHA is
`f427eb7ca9ab40254860f5a0848c45915a90ff7aa165f813ffcb97aaff31b18c`.
Original published source SHA:
`b61bf8edee8f8ab40529399de2f6ef2c3f2419eeb69fb6958955c6c07793743e`.
Original repository pack SHA:
`ff77ccb926b9a218d2587ade952840e31e96bb439cc1d67a1ddfc0d135a75ab9`.

The separate /description drift is an existing repository answer-first rewrite,
not a new factual error by itself. The current default assembler would adopt the
baseline source, so repository-preservation admission needs explicit hash-bound
handling. No such approval or source-correction PASS was issued by the audit.
The original source cutoff is2026-09-13; all three source assets remain exact and
readable at15px. No SVG change is required for these body findings. The current
JESTA implementation wording remains dated and supported; do not invent launch
or fee availability. This open follow-up is outside the fixed wave3 content cohort.
