---
id: 2026-09-21-five-language-kansai-arrival-usj-batch
title: Five-language Kansai arrival and USJ batch 008
status: review
priority: P1
area: docs
owner: codex-kansai-batch008
claimed_at: 2026-09-21T19:30:37Z
created_at: 2026-09-21T19:30:27Z
completed_at:
branch: codex/article-localization-batch-008-kansai
depends_on: []
scope:
  - apps/api/app/guides/content/kansai-airport-to-osaka-kyoto.json
  - apps/api/app/guides/content/usj-guide.json
  - apps/web/public/guides/kansai-airport-to-osaka-kyoto
  - apps/web/public/guides/usj-guide
---

# Five-language Kansai arrival and USJ batch 008

## Why

The public Kansai airport-transfer and Universal Studios Japan guides each have
only a complete Traditional Chinese document. Add English, Japanese, Korean and
Simplified Chinese bodies and language-specific diagrams from the current
published source while preserving the existing locale, article metadata,
visibility, photo credits and licensing.

## Definition of done

- [x] Both public guides contain complete, native-quality documents in all five
  site languages, including every summary item, body block, table, link label,
  caption, alternative text, image description and source title.
- [x] Each text-bearing diagram has en, ja, ko and zh-CN variants that match the
  article facts and render without overflow, overlap or missing glyphs at
  1600x900 and 390px.
- [x] A current read-only production snapshot binds source versions and hashes;
  existing taxonomy, ordering, photo assets and credits are not replaced. The
  verified source corrections and live USJ editorial reconciliation are recorded.
- [x] Strict schema, token, source, link, pack, task and render checks pass, and
  an independent reviewer reports no unresolved blocker or major finding.

## Steps

- [x] Exclude all active task scopes and claim exactly the two pack and asset paths.
- [x] Capture a fresh production source snapshot and repository/source hashes.
- [x] Translate and materialize eight documents with eight localized SVGs.
- [x] Verify primary-source facts, numerical and eligibility parity, links and credits.
- [x] Complete focused tests, desktop/mobile renders and independent review.
- [x] Hold the branch without opening a PR until the preceding localization batch permits it.

## How to verify

Run the article-localization pipeline status and integrity checks for the exact
two slugs, scoped `pack_cli lint`, focused guide pack/link tests,
`npm run test:tools`, `npm run check:tasks`, and `git diff --check`. Render every
localized SVG at full and 390px widths and inspect the images.

## Notes

- Fresh read-only production snapshot at 2026-09-21T19:31:32Z: both articles
  are active and public at article version 2, with only zh-TW version 6
  published. Snapshot SHA-256:
  `ac6c214133bdcb906522b14ca0a3fd8b15ff16d4bd6ac4aace0a513dcd759fdc`.
- Worktree and task started from exact main
  `746004d046044a44a15f09e611a34a0e02c647f3`. The baseline SHA-256 is
  `8b36da18b08c117139ba6d11b07ff16e8a676d8cc2383f2f39dedaba2aa81b14`.
- `kansai-airport-to-osaka-kyoto` repository and live zh-TW document hashes
  match at `157f9a43bc306bca926560bd9aea1d674cdd8d80e1d1837ea6c673f88dc8c850`.
  `usj-guide` uses the current live zh-TW source hash
  `44ac22e35a3d179a41e0bd93fc4099bb6630a328387fa1d8988e04971647e217`;
  its repository source is older, so translations must retain the live edit.
- The published Kansai source used airport-bound taxi estimates in its airport-arrival
  guide. Corrected five inbound fares against the airport's *from-airport* tariff,
  including Kita 24,400 yen and Kyoto 43,150 yen, and corrected the four-person
  comparison to 6,100 yen versus HARUKA 1,800 yen. JR-WEST's online pickup
  requires reservation number, four-digit authentication number, payment card and
  passport; a ticket-machine pickup also needs an IC-chip passport. The exact
  source correction and four translated field changes are bound in external
  `source-correction-receipt.json` and `translation-correction-receipt.json`.
- The USJ zh-TW repository document retained three newer live editorial fields;
  its lunch time uses equivalent 11:00 formatting to match the diagram. Its
  reconciliation is recorded in `usj-live-edit-reconciliation.json`.
- Eight localized documents and eight SVGs passed schema, source/link/numeric,
  artifact binding, rendered 1600x900 layout and scoped pack lint. English length
  guidance is advisory because these are full translations. At 390px, the existing
  article renderer displays SVGs at 1180px in a horizontal scroller: Playwright
  measured 810px scroll range, keyboard ArrowRight motion and no page overflow
  for all eight; evidence is in external `mobile-scroller-check.json` and sixteen
  segment screenshots. It does not shrink the whole diagram to 390px.
- Localization and task tool tests: 45 passed; Python localization pipeline:
  32 passed. Focused API tests: 47 passed, 11 skipped, two unrelated whole-repo
  checks failed because this sparse checkout omits other guide assets. Full
  `npm run test:tools` likewise fails for sparse-omitted Claude Code ZIPs and a
  Gemini series module; the full log is external `test-tools-full.log`. Task
  validation and `git diff --check` pass.
- Independent final editorial and visual review checked official fares, JR ticket
  eligibility/pickup, USJ date/prices and ride names, all eight document/render
  audits and mobile scroller screenshots, with no remaining blocker. Do not merge,
  deploy or publish this batch until batch 007 has completed its production release.
- Independent review also corrected the official USJ Donkey Kong ride names in
  English (`Mine Cart Madness`) and Korean (`동키콩의 크레이지 트램카™`), in article and
  SVG accessible/visible text. Both localized assets were rendered again with no
  layout findings; the field and byte changes are in external
  `usj-ride-name-correction-receipt.json`. The existing `?city=osaka-kyoto` food
  links remain valid: the current `readFoodBrowserFilters` accepts `city` as an
  alias for `destination_id` and has a dedicated test.
- After rebasing onto `51e716da`, focused API pack/ingest/link tests passed:
  47 passed, 11 skipped, two whole-repository asset checks deselected because the
  isolated sparse checkout does not materialize unrelated guide assets. Full
  output is external `api-focused-after-rebase.log`.
- Review PR: https://github.com/x812033727/travel_scanner/pull/629. Merge and
  production release remain sequenced after the preceding localization batch.
