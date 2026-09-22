---
id: 2026-09-22-localize-naver-map-and-kakao-t
title: Localize Naver Map and Kakao T guide in five languages batch013
status: review
priority: P1
area: docs
owner: codex-batch013-naver-kakao
claimed_at: 2026-09-22T03:19:43Z
created_at: 2026-09-22T03:19:24Z
completed_at:
branch: codex/article-localization-batch-013-naver-kakao-sparse
depends_on: []
scope:
  - apps/api/app/guides/content/korea-naver-map-kakao-t-guide.json
  - apps/web/public/guides/korea-naver-map-kakao-t-guide
---

# Localize Naver Map and Kakao T guide in five languages batch013

## Why

The published guide has only zh-TW. Add complete en, ja, ko, and zh-CN
documents and localized diagram text while preserving the published source,
reader audience, original photos and credits, metadata, and publication state.

## Definition of done

- [x] Four complete translations preserve all 51 blocks, 13 sources, numbers,
      conditions, source URLs and dates, image descriptions, and link labels.
- [x] Four localized SVG diagrams pass desktop and mobile render inspection.
- [x] Source/baseline and candidate hashes, focused checks, and review packet
      are ready for independent review before any PR or release.

## Steps

- [x] Claim exact article and asset scope; export fresh read-only live source.
- [x] Draft and check all four missing locales and diagrams.
- [x] Freeze candidate, run checks, and request independent review.

## How to verify

Run scoped `python -m app.guides.pack_cli --content-dir <this-worktree-content>
--public-dir <this-worktree-public> lint --slug korea-naver-map-kakao-t-guide`,
`npm run check:tasks`, and `git diff --check`. The external batch013 handoff
directory contains source-bound structure/numeric/link/asset audits and SVG
render scripts; rerun them with the existing shared Python/Playwright runtime.

## Notes

- Base at claim: `35299c153fd5d7dc8e6ae6b6fd48cfcc04fa27c3`.
- Fresh `REPEATABLE READ, READ ONLY` source snapshot at
  `2026-09-22T03:18:55.461950+00:00`: active published article v2, zh-TW
  locale/published v8, no expiration, and no other locale rows. Draft and
  published normalized SHA-256 are both
  `714a801228dc3b78bf10c7e0d0d6a3e1d5e490828e3f11008a25f781c2156db5`.
  The normalized repository zh-TW document matches that source exactly.
- Source, metadata, topic order, original source SVG, photos and credits are
  unchanged. The intended Taiwan departure/phone-number/currency audience is
  retained in all four translations, without inferring a reader's nationality.
- Source and candidate evidence lives in
  `C:/Users/x8120/.codex/article-localization-release/batch013/`.
  Source URL and `checked_on` values stay exact. Supplemental live topics
  export at `2026-09-22T03:35:58Z` confirms article v2 and topics
  `connectivity`, `transport`; repository topic ordering is preserved.
- Primary-source spot checks on 2026-09-22 confirmed current Naver/Kakao map
  interface languages, k.ride languages/registration/payment, Seoul fare
  increments, and Incheon night/out-of-area surcharges. No factual source
  correction was introduced. Historical source-publication dates are preserved.
- Four full translations have 51 blocks and 13 sources each. Source/default
  empty schema fields are normalized for comparisons. Numeric-token differences
  are English month names/date formatting and written Chinese numerals converted
  to Arabic numerals in Japanese/Korean; reviewers check the meanings.
- Scoped lint passes. Existing no-summary warnings remain across all locales;
  the complete English body is 9,019 characters, above the howto guideline.
  Nothing is shortened to satisfy that advisory.
- Existing content-import/link regression tests: 10 passed, 5 optional PostgreSQL
  tests skipped, 2 unrelated full-checkout asset/life tests deselected. A separate
  actual-candidate audit checks all 15 image references and 50 ArticleInline
  references, correct kinds, and same-language destination links. At that check,
  32 target locale references were not yet public and remain publication-aware
  ArticleInline values, never raw clickable article URLs.
- All 41 visible text labels in each new SVG are localized. Desktop and 390 px
  mobile horizontal-scroll previews pass text overlap, canvas/card boundaries,
  diamond-polygon bounds, and document-overflow checks. Source photos contain
  only photographed scene signage, with no designed text overlay to translate.
- Independent reviews PASS for en/zh-CN, ja, ko, and frozen SVG/render artifacts.
  Final Korean terminology and the explicit Kakao-account/verification yes
  branch were corrected before the final freeze. Only that latter correction
  changed SVG `<desc>`; all visible SVG bytes and 16 initial renders are exact.
- Additional image-element previews reproduce the actual ContentBlocks layout:
  diagram width 1180 px, mobile viewport 390 px, left padding 20 px. All four
  desktop and twelve mobile scroll-position images pass independent visual
  review; the document stays 390 px wide. This is offline image/layout QA,
  not live publication or browser verification of the article page.
- Final candidate pack SHA-256:
  `8a28c3ce063500fd2930fafa52b3b8b1f9f43015481363313287d09ebd0e7826`.
  `candidate-freeze-v2.json` SHA-256:
  `2e6c84f434a845402a1524ff84da151e8c473b4ce881055bd62fc2eea21c8a4f`.
  This frozen receipt binds all four final document hashes, seven assets,
  32 PNG renders, render geometry checks, and six audit/review receipts.
- Independent final review receipts under the batch013 evidence directory:
  `independent-en-zhcn-review.json`:
  `f74369f9625d8a7db3d8a6bf39a1539e76520a45989f7804850db322135b8fb6`;
  `ja-independent-review/receipt.json`:
  `ebb5c7aea6b6a266581875c530f9b2d1b4fd90028c29d2c4a535a329588dd6e4`;
  `ko-independent-review/receipt-pass.json`:
  `ff1c6edbb704f0d5a0d89abed167d3743324891646d52b976e27207cb6b54f14`;
  `svg-independent-review/receipt-final.json`:
  `4eb2d2993f12c3300c6731d3f6b14953158e0a8695e7aa5dfb6297106ff53547`.
- Draft PR review and CI are next. No production write, import, publication,
  or live article-page verification is claimed by this content task.
- P: reported ample capacity but actual file writes returned a device-malfunction
  error. Its incomplete registration is retained; this task uses a minimal C:
  sparse checkout and shared runtimes without installing dependencies.
