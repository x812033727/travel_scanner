---
id: 2026-09-21-taiwan-zh-tw-batch-004-taipei
title: Taiwan zh-TW batch 004: Taipei viewpoints and where to stay
status: review
priority: P1
area: docs
owner: codex-taiwan-zh-tw-batch004
claimed_at: 2026-09-21T15:17:57Z
created_at: 2026-09-21T15:17:51Z
completed_at:
branch: codex/taiwan-zh-tw-batch-004
depends_on: []
scope:
  - apps/api/app/guides/content/taipei-viewpoints-101-elephant-mountain.json
  - apps/api/app/guides/content/taipei-where-to-stay.json
  - apps/web/public/guides/taipei-viewpoints-101-elephant-mountain/diagram-1-zh-tw.svg
  - apps/web/public/guides/taipei-where-to-stay/diagram-1-zh-tw.svg
---

# Taiwan zh-TW batch 004: Taipei viewpoints and where to stay

## Why

Both guides are public in English, Japanese, Korean and Simplified Chinese, but the public
API returns `unpublished` for zh-TW. Add complete Taiwan Traditional Chinese documents and
language-specific diagrams without changing the existing locales or article taxonomy.

## Definition of done

- [x] Fresh public production API inventory proves both exact slugs are published in four
  locales at version 6 and have no zh-TW document.
- [x] Each pack contains one complete zh-TW `GuideDocument` with source/block parity against
  the current published source, language-correct internal routes and preserved image credits.
- [x] Time-sensitive prices, hours, closures, transport and entry/eligibility wording are
  checked against reader-visible official sources dated 2026-09-21.
- [x] Each text-bearing diagram has an explicit zh-TW SVG whose description matches the
  document and whose numbers occur in the article text.
- [x] Desktop and 390 px SVG renders have no clipping, overlap or missing glyphs.
- [x] Focused API/tool/task tests pass, apart from pre-existing non-target locale lint errors
  recorded below.
- [x] Independent fact/content review has no blocking finding.
- [x] Rebase onto the latest `origin/main`, prove content hashes unchanged, and open a
  non-draft pull request.

## Steps

- [x] Exclude batch 001 (`jiufen-shifen-yehliu-day-trip`,
  `taipei-night-markets-guide`), batch 002 (`taipei-metro-easycard-guide`,
  `taoyuan-airport-to-taipei`) and batch 003 (`kaohsiung-3-day-itinerary`,
  `tainan-2-day-itinerary`), then confirm no active exact-file scope conflicts.
- [x] Capture production public API responses and compare the four existing repository locales.
- [x] Author and review both zh-TW documents and SVGs.
- [x] Replace a retired Taipei Travel URL that redirected to `/404.html` with the current
  official 2026 Dadaocheng riverfront article.
- [x] Run target-only schema/editorial/SVG lint and structural/hash checks.
- [x] Run focused tests and visual checks.
- [x] Apply the independent fact review's 17 blocking corrections to eligibility, Skyline,
  construction, transport, lodging and disposable-amenity claims, including both diagrams.
- [x] Obtain the reviewer's final approval after applying the remaining five completeness
  corrections.
- [x] Freeze content hashes, rebase, prove the payload is unchanged, push and open PR #624.

## How to verify

```text
cd apps/api
uv run python -m app.guides.pack_cli lint   --slug taipei-viewpoints-101-elephant-mountain   --slug taipei-where-to-stay
uv run pytest tests/test_guides_content_pack.py   tests/test_guides_content_links.py tests/test_guides_pack_ingest.py -q
cd ../..
npm run test:tools
npm run check:tasks
git diff --check
```

A target-only script also loads each `ArticlePack`, runs `lint_document`, `check_svg` and
`missing_diagram_numbers` for zh-TW, and compares block/type/source/image metadata against the
captured production source. The external evidence directory is
`C:\Users\x8120\.codex\article-localization-release\taiwan-zh-tw-batch004`.

## Notes

- Public API snapshot captured 2026-09-21: both slugs expose en/ja/ko/zh-CN at version 6 and
  return `unpublished` with no document for zh-TW. No production write was performed.
- Production zh-CN source hashes: viewpoints
  `d1bb87ebb096007c9581dd6f2314b77b9b38b31727d06f7e73ea18a16bd405e4`;
  lodging `6730f02970852e5225d1b88109278c1d4b5094e704670de19d7800ca73776ed5`.
- Existing en/ja/ko/zh-CN payload hashes and every top-level pack field match the task base.
- The zh-TW copy does not infer nationality from language. Entry rules explicitly depend on
  the traveller's document, identity and residence; TWAC applicability points to the NIA.
- The independent review corrected 17 initial factual details and five final completeness
  findings. Among them, `1819` now has scheduled
  all-day departures with a longer night gap; `1840` and `1841/1842` state their distinct
  airport terminals; `1960` and taxis no longer promise unsupported fixed times or fares.
  The A1 check-in deadline, Airport MRT timetable validity, MRT transfer counts, Skyline
  eligibility, Xiangshan expected completion, B&B apartment exception, disposable amenities,
  Hong Kong/Macao eligibility and processing time, Mainland visitor categories, A1 airlines,
  Songshan routes and latest scheduled arrival, visa-waiver passport types and exact TWAC groups
  are explicit. The independent reviewer returned `APPROVE` after the corrections.
- All 40 current source URLs returned HTTP 200. The reachability check used an unverified TLS
  context only because Python 3.14 rejects several Taiwan government certificate chains; the
  one initial Yangmingshan handshake timeout returned 200 on an immediate curl retry.
- Target-only lint has no error; the inherited absence of a `summary` block is one warning per
  locale. Whole-pack lint still reports pre-existing diagram-number errors in `ko` and
  `zh-CN` for `taipei-where-to-stay`; zh-TW has no diagram-number error.
- Focused API tests: 43 passed, 5 skipped. Tool tests: 75 passed, 1 skipped. Task and diff
  checks pass; task check prints only repository-wide stale/overlap warnings outside this scope.
- Playwright renders at 1600x900 and 390x220 report 0 outside text, 0 overlaps and 0 missing
  glyphs for both diagrams after the review corrections; all four PNGs were inspected.
- Rebased onto `origin/main` at `2e952951f33a1d8db6f09d37c5068f883cf3b53f` before
  opening non-draft PR #624. Both canonical zh-TW document hashes and all four normalized Git
  blobs were identical before and after the rebase.
- This task must not merge, deploy, import or publish the documents.
