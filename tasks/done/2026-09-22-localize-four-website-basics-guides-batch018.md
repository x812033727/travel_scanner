---
id: 2026-09-22-localize-four-website-basics-guides-batch018
title: Localize four website basics guides batch018
status: done
priority: P1
area: docs
owner: codex-batch018
claimed_at: 2026-09-22T09:41:01Z
created_at: 2026-09-22T09:40:59Z
completed_at: 2026-09-23T07:19:46Z
branch: codex/article-localization-batch018-web-basics
depends_on: []
scope:
  - apps/api/app/guides/content/domain-registration-guide.json
  - apps/api/app/guides/content/hosting-types-explained.json
  - apps/api/app/guides/content/website-cms-choice.json
  - apps/api/app/guides/content/website-maintenance-routine.json
  - apps/web/public/guides/domain-registration-guide
  - apps/web/public/guides/hosting-types-explained
  - apps/web/public/guides/website-cms-choice
  - apps/web/public/guides/website-maintenance-routine
---

# Localize four website basics guides batch018

## Why

Four original-626 website basics articles are publicly available only in zh-TW.
Add complete en, ja, ko and zh-CN documents and matching text-bearing hero and
inline diagrams, preserving source versions, metadata, code, URLs and credits.

## Definition of done

- [x] Read-only inventory identifies four public source articles and missing locales;
      source draft/latest/published documents match and repository source is equivalent.
- [x] Revalidate source/editorial concerns and preserve all existing zh-TW edits.
- [x] Independently review sixteen full translations, including all 26 blocks and
      three sources per document, applicability, numeric values and protected tokens.
- [x] Localize eight source SVGs into 32 SVGs and render sixteen localized hero JPGs;
      independently inspect all assets on desktop and mobile without text overflow.
- [x] Integrate only reviewed documents and locale-suffixed images; preserve four
      existing source documents, all metadata, original images and publication state.
- [x] Scoped article-pack checks, API content tests, task check and i18n pass.
- [x] Complete frontend checks and prepare the batch PR with exact evidence.
- [x] Track CI/merge and guarded publication/browser acceptance separately in
      `2026-09-23-release-localized-website-basics-batch018`; this content task does
      not claim production publication.

## Steps

- [x] Select domain-registration-guide, hosting-types-explained, website-cms-choice
      and website-maintenance-routine with no active-scope or open-PR overlap.
- [x] Create isolated worktree and normally claim the exact eight content/image paths.
- [x] Draft complete documents and assets outside Git; freeze and independently review.
- [x] Integrate and validate all reviewed content and image bytes for the batch PR.
- [x] Hand off canonical release and per-article acceptance to the explicit release task.

## How to verify

Use the isolated API runtime and run `python -m app.guides.pack_cli lint --slug`
for each exact slug, `npm run check:tasks` and `git diff --check`. Verify every
protected field and image reference against the pinned source; perform independent
full-body and actual rendered image review, then guarded canonical publisher tests
and production browser acceptance before marking this task done.

## Notes

Selection evidence is outside Git under
`C:/Users/x8120/.codex/article-localization-release/batch018-inventory/`.
`selection-receipt.json` SHA256
`f93e14a1df4bedeca4ae3bf30eeafb253ff959c21e7a0e30a18779fd2394afe8`.
Fresh live snapshot at 2026-09-22T09:14:33Z has SHA256
`96378db975386a6bb14de494167610446bf4fe0e01206f43f1e641b8baf87d76`.
All four articles are active and published at article v2, zh-TW locale v4, with
no expiry and no unpublished live draft difference. Worktree starts at
`9fafd4293506a264dfe54c3722cb2c2eac86b516`; the dimensions-tool merge changes none
of these sources. No publication or completed translation is claimed by this task.

## Reviewed offline candidate — 2026-09-23

All sixteen complete documents and forty-eight localized assets have independent
PASS receipts. Domain/hosting required twelve body-leaf corrections and eight
hero JPG size corrections; prior revisions remain preserved outside Git. All
sixteen hero JPGs are approved at 1600x900. The approved diagrams and hero
renders include desktop and mobile views. The unchanged field guard reports
exactly five independently reviewed Han-number-to-digit formatting rows in
Japanese: four in CMS and one in maintenance. Korean has no field-guard
warnings; no other warning is approved.

Independent review receipts (outside Git):

- `C:/Users/x8120/.codex/article-localization-release/batch018-web-basics/root-independent-cms-maintenance-en-cn-review.json`
  SHA256 `355fefefa9ae18d44d3da313d5b12dd505858bf6f302c22f7b974b7126ca5301`.
- `C:/Users/x8120/.codex/article-localization-release/batch018-web-basics/independent-cms-maintenance-ja-ko-review/receipt-index.json`
  SHA256 `f641cce471beac42dd1f22d350d1dcbf28b76d627696d54bcac5bf0695d46ef6`.
- `C:/Users/x8120/.codex/article-localization-release/batch018-web-basics/independent-cms-maintenance-assets/receipt-pass.json`
  SHA256 `bc725ddfde838a3bcd64e65a15c77e3b28a84c7ce53acef9af5a14c2e02fcb75`.
- `C:/Users/x8120/.codex/article-localization-release/batch018-web-basics/independent-domain-hosting-body-review-resumed-20260923/receipt-index.json`
  SHA256 `8bdafb8d831a5fe91c1d9f49c26b3125c90516649b9cede5d3f37a80b84fcbcd`.
- `C:/Users/x8120/.codex/article-localization-release/batch018-web-basics/independent-domain-hosting-assets-resumed-20260923/receipt-pass.json`
  SHA256 `fd5544e3fc9fa0aa77a077c7a03fd2180d0b10940d1642e7728470f98ba20c07`.

Four candidate ArticlePacks preserve the entire original source bytes by only
inserting the four missing locale entries. Removing those insertions exactly
restores each original pack. Original zh-TW documents, metadata, and all twelve
source images remain unchanged. This offline checkpoint does not claim that
integration, repository checks, CI, PR, deployment, import, publication or
public browser acceptance has happened at that offline checkpoint. A fresh live
baseline remains required before release.

## Integration and local validation — 2026-09-23

Applied the exact 53 reviewed candidate paths on `4547fac3f6c48b60eccfdbe6fab7be656f73ab80`
after confirming all source packs and original images still matched the approved
source. The only candidate correction was the task wording above: all five
number-format exceptions are Japanese, not Korean. Independent integration review
SHA256 `9d7280c9b537fb19216cd48c72ff9c3ca75f4296d3a6209733a91687789dafe4`;
applied-byte receipt SHA256
`ff104f0ce7099be81d32adcab83577ddfe45b4492ebaa095ffbd3dbd04f8d92f`.

Scoped lint completed for all four packs. It retains the source's missing-summary
advisory in all locales and English length advisories (6052, 6020 and 6231
characters); complete translations were preserved. API content/ingest tests:
64 passed, 5 skipped. Tool tests: 81 passed, 1 platform skip. Task check, i18n,
web lint, TypeScript and production build passed. Frontend unit tests passed:
293 files / 3205 tests using the bundled Node 24.19.0 runtime. The initial system
Node 24.13.0 run was stopped after it stalled; that runtime is below the installed
jsdom dependency's declared engine requirement. No application change was needed.
Final CI, merge and release state remain tracked by the separate release task.
