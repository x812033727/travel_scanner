---
id: 2026-10-28-release-localized-two-ai-concept-life
title: Release localized two AI concept life guides
status: open
priority: P1
area: docs
owner:
claimed_at:
created_at: 2026-10-28T13:52:03Z
completed_at:
branch:
depends_on:
  - 2026-10-28-localize-two-ai-concept-life-guides
scope:
  - docs/article-localization/releases/2026-10-28-ai-concepts
---

# Release localized two AI concept life guides

## Why

The dependent content task adds eight reviewed en/ja/ko/zh-CN translations for
the public foundation-model and tokenization life articles. It also corrects
tokenization's two inaccurate source alt strings and matching SVG descriptions
through an independently approved native source-correction receipt. Repository
installation and green CI do not publish these documents. This task owns the
separate guarded deployment, source correction and translation publication.

## Definition of done

- [ ] The exact reviewed content commit is merged after applicable checks pass, with the full pending deploy range and migration scope inspected.
- [ ] Fresh production source/draft/published/target guards match the admitted bundle; concrete owner authorization and a verified fresh full backup precede writes.
- [ ] New-image isolated rehearsal, native publisher phases, durable journal readback and idempotent replay pass for exactly the authorized locales/source correction.
- [ ] All ten public documents (two articles times five locales), public assets, link resolution, sitemap/canonical/hreflang and actual desktop/mobile views pass independent acceptance.
- [ ] Sanitized release evidence is recorded, only the release driver's own hold is cleared and final host verification passes.

## Steps

- [ ] Verify merged content and exact final source-correction/job/artifact reviews; preserve the original source bindings and failed attempts.
- [ ] Take fresh source/version/visibility/target snapshots, validate source-correction old/new hashes, and dry-run the exact native plan.
- [ ] Present the full release scope for approval, verify backup restore, deploy under owned hold and rehearse using the actual new runtime.
- [ ] Execute the native phases with one durable state directory, rebuild/check links and replay without further writes.
- [ ] Complete paced public capture with settled navigation/geometry, independent visual review and native progress accounting.
- [ ] Write README.md/evidence.json, close this task and clear only its own hold after final acceptance.

## How to verify

Follow the article-localization/deploy skills, source_correction.verify_review,
the native publisher's source-drift guards and ops/release/README.md. The exact
publication count must come from the final manifest and fresh runtime dry-run;
it includes the approved source correction as well as new target documents.
The native progress report is historical journal accounting, not a live query.
Retain actual database, backup/restore, browser/network and screenshot receipts
outside Git; release docs contain only sanitized hashes/counts/public paths.

## Notes

- Selected slugs: ai-term-foundation-model, ai-term-tokenization. Eight new
  translations are the intended scope; tokenization zh-TW also has two alt
  corrections. Its SVG desc metadata changes preserve all original visible
  pixels/text/geometry and the JPEG. Foundation-model's source stays unchanged.
- The old tokenization source is clean public v10. Native independent correction
  review SHA256:
  `9653389d926c83b7015bff4827c6084ef95f3c147fc4a177e4b22f8905dad980`.
  Corrected source canonical SHA256:
  `e7f4742aaacaba918503108e6b07cfbfd1dc24536f3a3dca6f2f7eeb7fc20364`.
- Source correction authoring baseline retains original database pins; never
  replace them with corrected content pretending it was already public. The
  editable hero SVG companion has separately bound old/new hashes and pixel
  proof; public diagram SVG and unchanged source JPEG are in the native review.
- This is separate from the completed 48-translation release recorded in
  PR #1913, and from the earlier two business-analysis articles. None of their
  backup, deployment, publication approval or finalization receipts authorize
  this new cohort. No production write for these articles is claimed here.
- Final authoring manifest SHA256:
  `26e5a4626ea069118ea232383e15c20d149ff09246ce1ce7839caf4d45eeeffe`.
  It selects four locales for foundation-model and five for tokenization:
  eight new translations plus the reviewed tokenization zh-TW correction.
  The bundle has two packs and twenty-six assets (twenty-four new localized
  assets, the corrected original diagram and the unchanged source JPEG).
- Corrected authoring baseline SHA256:
  `2a77df5832dbbd833495faeb101073e434865736051d60fc15876b80bd5835df`.
  Native local install and replay passed; production dry-run, backup, deployment,
  publisher journal and public acceptance have not been performed for this cohort.
