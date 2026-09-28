# Batch039 Pair B: PESTLE and SWOT/TOWS guide translations

This review-only branch adds complete zh-CN, English, Japanese, and Korean documents plus localized hero and diagram artwork for `pestle-business-scan` and `swot-tows-action-plan`. The published zh-TW documents, article metadata, and original images are unchanged. No import, publication, deployment, or production write is part of this PR.

## Source and scope

- The pinned Batch039 candidate inventory is `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-readonly-inventory-20260928/candidate-inventory.json`, SHA-256 `3ce92eeeb90f1793988308dacf1d93729b5a0ee61d8e0e98a9a769e68c7d666f`. Both source packs and all six original images match its byte hashes against `origin/main` after the later main update.
- A guarded four-lock, repeatable-read **read-only** production snapshot completed at `2026-09-28T11:51:28.934762Z`: receipt `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-readonly-inventory-20260928/receipt-20260928T115126Z.json`, SHA-256 `e156935e618b5233d63a5c8981db2dda0837f9cfceefded365fdd75d9485024f`; snapshot SHA-256 `64dc8d289a4ccaaf693f89478478ee25f37fe7cf4dba0ef1daa1cfe5b44f93cd`. Both articles were active/published, article v2 and published zh-TW v4, with source draft/published hashes matching the repository and no target-locale rows. The receipt records `production_writes: false` and unchanged host state. It is a point-in-time source check; any later import needs a new live preflight.

| Slug | Original pack SHA-256 | Published zh-TW normalized SHA-256 | Final pack SHA-256 |
| --- | --- | --- | --- |
| `pestle-business-scan` | `8ccf95744013eca3ed4221b37e4e308e33acab7e611d72a77c1cab9779a8ba5f` | `52bae6f00fca8e68812bbb8a2c8fd50313fc7e5f75a3153263fa3ed64cec4a37` | `1515730ab85e218e5cfef29bea1748914ff95f3e21975fe1255023f547a2d0de` |
| `swot-tows-action-plan` | `704381081a44535749cdcaa57e95017913045f2c417665b880eba7479db55fae` | `975c00a9defb6efd64ba26e9f8d761536602ffabd5fc62566dc913b7b94830c7` | `d3ac47ebb198c937d2b33536a1c92d24abd14614a1c5885ae5342672493d42a4` |

## Editorial and structural review

All eight target documents have translated title, description, body, headings, lists, callouts, table text and caption, image alt/caption/description, and source titles. The structural audit confirms all 33 block types and order, heading levels, list lengths, table dimensions, seven source URLs and exact checked dates, image credits, and six exact `ArticleInline` `(kind, slug)` targets. The links remain publication-aware: translation of link text does not assert that the linked locale is already public.

The PESTLE camping-rental shop and SWOT/TOWS print studio are explicitly original examples, not observed market events. PESTLE separates the six external factors, official announcements from assumptions, and Taiwan DGBAS CPI household-price scope from a shop's own costs. Taiwan CWA CODiS historical observations are not portrayed as a future weather forecast. SWOT separates internal strengths/weaknesses from external opportunities/threats and keeps SO, WO, ST, and WT options distinct; subjective scores are not treated as probabilities or guaranteed outcomes. In English, Japanese, and Korean, the first mention and source titles identify the Taiwanese agencies. The Weihrich 1982 source URL and checked date remain as published; DOI `10.1016/0024-6301(82)90120-0` is an additional durable identifier, not a replacement source.

The official source set was independently checked before translation, including the [CIPD PESTLE factsheet](https://www.cipd.org/uk/knowledge/factsheets/pestle-analysis-factsheet/), [Taiwan DGBAS CPI explanation](https://www.stat.gov.tw/News_Content.aspx?n=2668&s=207893), [Taiwan CWA CODiS](https://codis.cwa.gov.tw/), [Business Queensland SWOT guide](https://www.business.qld.gov.au/running-business/planning/swot-analysis), [Australian government SWOT guide](https://business.gov.au/planning/business-plans/do-a-swot-analysis), and the [university-hosted Weihrich TOWS PDF](https://elearning15.unibg.it/pluginfile.php/644921/mod_folder/content/0/STR%20T06%20Weihrich_1982_LRP.pdf). The current branch keeps every original source URL and `checked_on` date unchanged. An independent reviewer checked key paragraphs and all 16 final artwork previews.

## Validation

- `uv run python -m app.guides.pack_cli lint --kind life --slug pestle-business-scan --slug swot-tows-action-plan`: **pass**, two entries. The generic `no_summary` warning also applies to unchanged zh-TW originals; the full English translations exceed the generic life-guide character guideline while preserving the original 33-block coverage.
- `uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py tests/test_guides_pack_ingest.py`: **67 passed, 5 skipped**.
- `npm run typecheck:web`: **pass**.
- Targeted `article.test.tsx`, `article-page.test.tsx`, and `guide-image.test.tsx` Vitest invocation: **not run to assertions** because all three Windows `vitest-pool` thread workers timed out during startup. There was no test assertion failure. PR CI must validate these suites; the same local startup failure was not repeatedly retried.
- `npm run check:tasks`: **pass**, 1,045 task files; existing stale-claim and overlapping-scope warnings are unrelated to this task. `git diff --check`: **pass**.
- Content/asset audit: `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-pair-b/pair-b-final-content-asset-audit.json`, SHA-256 `57efeba38978cf2d212b76b6451c1e463e5929ec8d74283074b7e293f11173db`: 26 content/asset files, zero issues. All 16 localized SVGs parse, and all eight localized JPGs are 1600 × 900.
- Final Chromium SVG report: `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-pair-b/final-svg-preview-pair-b/layout-report.json`, SHA-256 `475625961fce6cf7affc3d3710cea5b4079ec46a7f8c406e735a150101a2a830`: 16 hero/diagram cases, zero canvas, card-margin, or text-overlap issues. A strict check found several English PESTLE labels crossing card boundaries; their final wording was shortened and all cases rerendered. Minimum final card text inset in pixels is PESTLE zh-CN/en/ja/ko `28/21.28/14/24.48` and SWOT/TOWS `28/7.94/17/9.83`.
- Final standalone article browser report: `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-pair-b/final-page-preview-pair-b/layout-report.json`, SHA-256 `266f3b2558bef0dab4c15945c974859bd1a9d29b28651ba3088e071010a45bae`: 16 desktop/mobile renders of exact localized pack content and assets, zero horizontal overflow, all hero and diagram images loaded with alt text, and expected headings/table rows. This is a preview of unpublished locales, not live Next.js or production acceptance.
- Independently inspected final contact sheets: `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-pair-b/final-preview/pestle-business-scan-all-locales-final.png` and `C:/Users/x8120/.codex/article-localization-release/batch039-strategy-pair-b/final-preview/swot-tows-action-plan-all-locales-final.png`.

## Localized asset SHA-256

The original `hero.svg`, `hero.jpg`, and `diagram-1.svg` for each slug are unchanged. The 24 localized assets are sealed below. Source page/content changes require regenerating this audit before any later release.

| Slug | Locale | Asset | SHA-256 |
| --- | --- | --- | --- |
| `pestle-business-scan` | `zh-CN` | `hero-zh-cn.svg` | `9887db6f4778742beda38a0043bdb10e25dda8c328525d828b8288d2ce3f5261` |
| `pestle-business-scan` | `zh-CN` | `hero-zh-cn.jpg` | `23ab67cce493539c018c5ff0f9b9b78eaa41c0a78004aedc5365dcfc3fccf4bf` |
| `pestle-business-scan` | `zh-CN` | `diagram-1-zh-cn.svg` | `0fac2eeb08cf7db807c097cafa4f0609212dc8daa98ae7b7c7efd238434abd59` |
| `pestle-business-scan` | `en` | `hero-en.svg` | `f129db2f1f35d47958ee61329f2e7978b7eddef19395fd630027a18ec84b838b` |
| `pestle-business-scan` | `en` | `hero-en.jpg` | `7118217092c94d455ed2592987bce938dcee18288fca4c9d0af934eb886a2841` |
| `pestle-business-scan` | `en` | `diagram-1-en.svg` | `b1bf599c05235c94efd01b6c7cd100bc571716bda1ba6ee006aef506e9ec1e39` |
| `pestle-business-scan` | `ja` | `hero-ja.svg` | `7524e3f23f12a10cd8653c5d115655acdad78aaaaa92e15a3465ebc965984a62` |
| `pestle-business-scan` | `ja` | `hero-ja.jpg` | `1d5eacd9ae9a716e7df5800798f4d1cb284bef3ac4b29d9c31ec72b2d28ccfce` |
| `pestle-business-scan` | `ja` | `diagram-1-ja.svg` | `8ce30e6c82a1ac3004199efc8800c7d4f8df48283c1b071a3018a5b2b6eb5de0` |
| `pestle-business-scan` | `ko` | `hero-ko.svg` | `c241aada6fd05427b03ba5a25801121b4401726a08703eac3f7aa838c4a66760` |
| `pestle-business-scan` | `ko` | `hero-ko.jpg` | `10120926c60e990ffa7e24ed887fd82025910ec8a00aae6128710372a60ca7a2` |
| `pestle-business-scan` | `ko` | `diagram-1-ko.svg` | `e18e3a3b95e28f4a398974fff5800f28d92eb307c61b7ca23b4b32b3f7ffbffe` |
| `swot-tows-action-plan` | `zh-CN` | `hero-zh-cn.svg` | `f8e55724a8ab229e10d93dbb5544bc3b76695568eeba797ab7f3181ec38aef1f` |
| `swot-tows-action-plan` | `zh-CN` | `hero-zh-cn.jpg` | `291c4b3f03bb9cb50017d5d4ec273364a0407f2a6253defe88eca6305fca8bec` |
| `swot-tows-action-plan` | `zh-CN` | `diagram-1-zh-cn.svg` | `e4c800dc9593b10198a39ce3f5bb795e6f556c3c08433e78c11fa3ff83d12e2e` |
| `swot-tows-action-plan` | `en` | `hero-en.svg` | `c1ac0365fed9ce3b6a994d51247d2d93853e885a66bd91d29d039b6895e9c1ae` |
| `swot-tows-action-plan` | `en` | `hero-en.jpg` | `35c5102797e31614d146463101bd0b447b2be1911f7db856f88b2f2bdff732c3` |
| `swot-tows-action-plan` | `en` | `diagram-1-en.svg` | `55c8a0cdd72f1f4c4c08a9059e0f84e4f10e91fe80011e57f6ac9b67e10c18c4` |
| `swot-tows-action-plan` | `ja` | `hero-ja.svg` | `597df1ee10be43ebb125d3e6fb9fe8116f49fda615f7208921f1194a013d684e` |
| `swot-tows-action-plan` | `ja` | `hero-ja.jpg` | `788e0cd117dd356ea9dcc6f776af828982f600b0094f43bacfc670843a7d05b6` |
| `swot-tows-action-plan` | `ja` | `diagram-1-ja.svg` | `82af7914736985419ca20038cccbae94525957c29785779a5f5244801d5baf4a` |
| `swot-tows-action-plan` | `ko` | `hero-ko.svg` | `d9c8153405be0a0a94af95ec462a7542ef25d5e49007467aaa3663134582e6a7` |
| `swot-tows-action-plan` | `ko` | `hero-ko.jpg` | `cf7bfd72de931bcefaf9e869e4b08e3708bb1b445022f20722452ed990cdf5de` |
| `swot-tows-action-plan` | `ko` | `diagram-1-ko.svg` | `327dfc69cba311d4ce1ce3d8b376d9deda972eec5197445994067313eb168fe8` |

## Review and release gate

The branch starts at `c54594e488f48e3655566cc8a86d45e9dc2e004e` and is updated to current `origin/main` before the draft PR. That main includes the joined Alembic migration chain from #918; local content validation does not establish full PR CI status. Review, green CI, a fresh live source/version preflight, and separate authorization are required before import, publication, or deployment.
