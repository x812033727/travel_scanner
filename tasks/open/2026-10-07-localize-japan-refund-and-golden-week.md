---
id: 2026-10-07-localize-japan-refund-and-golden-week
title: Localize Japan Golden Week travel information after refund source hold
status: in-progress
priority: P1
area: api
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:37:11Z
created_at: 2026-10-07T04:55:17Z
completed_at:
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/japan-golden-week-2027.json
  - apps/web/public/guides/japan-golden-week-2027
  - .codex/localization-staging/golden-week-20261007
  - docs/article-localization/installations/japan-golden-week-2027.json
  - docs/article-localization/installations/bundles/e4d3903b2197842a
  - docs/article-localization/installations/bundles/eb0ad09738c593b7
---

# Localize Japan refund and Golden Week travel information

## Why

The public Golden Week article has only zh-TW. Add en, ja, ko and zh-CN with
full text, source labels, captions and image text, preserving the current
published source and its original assets. The initial refund pilot is held
for a confirmed original-source error and moves to separate correction work.

## Definition of done

- [x] Complete four Golden Week target documents with original structure and facts.
- [x] Preserve zh-TW normalized document hashes and original image bytes.
- [x] Translate editable diagram text and independently inspect all raster photos.
- [x] Obtain independent hash-bound text, visual and glyph review for each locale.
- [ ] Pass content lint and applicable bundle/content CI checks; open a content PR.
- [x] Open a separate release ticket for guarded publication and public validation.

## Steps

- [x] Verify current production source, missing target rows and concurrent scopes.
- [x] Read fresh official tax/holiday sources before translating.
- [x] Prepare eight source/artifact-bound jobs outside the repository.
- [x] Finish Golden Week translation, materialization and first image rendering.
- [x] Independently review and apply corrections; assemble/install a reviewed bundle.
- [ ] Validate, open content PR and file release handoff.

## How to verify

Run `pack_cli lint` for Golden Week, source/target schema and localization checks,
and the applicable bundle integrity tests. Compare source hashes and original
assets before and after installation. Every review binds the final document
and artifact-manifest hashes. Publication and public browser validation belong
to the separate release ticket.

## Notes

- Fresh production snapshot: 2026-10-07T04:45:46.904711+00:00.
- `japan-tax-free-refund-2026` source hash:
  `6358cae7243f026ec6a2a27e9f26394e5805759ce42932ef92032a1367ff7c27`.
- `japan-golden-week-2027` source hash:
  `c906939f91e0ec733f537ea6f0972c354d81dcf6e11ef660499638488a62ead5`.
- Both repository sources match current published normalized documents; all
  four target database rows are absent. Neither overlaps an active content scope.
- Current MLIT tax page/FAQ and Cabinet Office 2027 holiday calendar were read.
  Preserve the Taiwan audience, the 2026-11-01 refund transition and explicitly
  unannounced 2027 JR dates; do not invent future announcements.
- Each article includes an editable SVG and a licensed raster hero/photo. A
  raster requires an explicit source-photo review, not an assumption of no text.
- Jobs and attempt logs are in the owner's persistent external work directory.
  Run uses ChatGPT-authenticated Codex, three workers, zero automatic retries.
- Quota/auth failures stop further jobs. Never clear their receipts or change
  the pinned baseline merely to restart an attempt.
- Full independent review found a real source error in the refund article:
  the Japan Tax-free Shop recognition logo is optional, while the article
  incorrectly makes display a requirement. Preserve the four attempted refund
  jobs; no review PASS or release for them until a guarded source correction.
- Refund pack/assets were removed from this ticket's active scope so separate
  correction work can claim them without conflicting with Golden Week.
- Golden Week en/ko required 21 numeric word-form corrections (no changed facts
  or dates); root applied the independent list and all four SVGs pass automated
  checks. Independent visual review additionally found an English legend
  collision and requests a compact equivalent label before final approval.
- All four final independent reviews pass with no open findings, including the
  compact English legend correction. The official fixed bundle manifest is
  `eb0ad09738c593b7a2a16fbb4e098aae531bcf5b49153c52cf0121e7fe9a6cec`.
- The first assembly exposed lost aliases and related-article metadata. Its
  exact installed bytes, inputs and completed journal were preserved externally,
  and the original pack was restored byte for byte before the corrected assembly.
  The obsolete per-article admission receipt was archived unchanged; its completed
  bundle journal remains for audit.
- The corrected official installation preserves every normalized root field,
  including two source aliases and four related articles. An independent review
  binds this comparison with receipt hash
  `cab59f541698e4bf5eead16b1ae6a1eec2634d92445e906f23783726a71eeb78`.
- Installed pack hash:
  `90d515b66ff127d7f42f6b61e9453ca1478f2b48e314d429f76452872bc04aa9`.
  Official admission receipt hash:
  `a77cea17de7d5aab4d480bcc79842b9f4171274fe4131e449799144aeb1f3597`.
  Completed installation journal hash:
  `70d4466062705438f8f4d382340e16606d1be586ea8f69a1bf04f28a487e8c76`.
- Immediate official replay changes no pack, receipt or journal bytes. The source
  document, original assets, immutable parent baseline and reviewed jobs are
  unchanged. This is local installation evidence; no production publication
  is authorized or performed here.
- Scoped final 13-pack lint EXIT0. Separate release ticket:
  2026-10-07-release-localized-travel-life-wave-20261007.
