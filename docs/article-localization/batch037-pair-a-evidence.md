# Batch037 Pair A: STP personas and social-media planning

This draft localizes `stp-persona-research` and `social-media-planning` from their published `zh-TW` documents into `zh-CN`, `en`, `ja`, and `ko`. Each translation keeps the 33-block structure, examples and their limitations, source URLs and check dates, original credits, and the three `ArticleInline` targets. The root pack metadata and both `zh-TW` documents are unchanged. Each new language has its own text-bearing hero SVG, 1600×900 JPG cover, and diagram SVG; no translated document refers to the `zh-TW` artwork.

## Source and publication state

- Starting `origin/main`: `5329ad8920300fec4fda06ded8bd006607a72d4f`.
- Read-only inventory: `<home>/.codex/article-localization-release/batch037-social-content-readonly-inventory-20260928/candidate-inventory.json`, SHA-256 `3bea364352f11e97fe1af688426c7f9c7c8e6c64b94a7dd6b8e55c1c60cac01c`. Original pack SHA-256 values: `stp-persona-research` `009a350b2ae173b300ce51a419da35d604729f3ffd57ade55cbb567df0130a4a`; `social-media-planning` `3411f13b952cb6cff67e35a40074cb97474ddfdaa08553478135f6d218a3d6ca`.
- Fresh guarded production read, captured 2026-09-28 11:00:27 UTC: `<home>/.codex/article-localization-release/batch037-social-content-preflight-20260928/receipt-20260928T110024Z.json`, SHA-256 `575c4ec04629900421c106f6c58f81e3e6ce2ccd0a28f97b76515c59ad1ad669`. It ran with four locks in a `REPEATABLE READ, READ ONLY` transaction and made zero production writes. For both slugs, the source draft and published document match the pinned inventory, article version is 2, `zh-TW` published version is 4, the article is active and published, and all four target locale rows are absent. This is a preparation snapshot; repeat the preflight immediately before any future import.

## Content and link review

- `stp-persona-research` keeps its hypothetical home-organizing example separate from actual interviews and Taiwan market measurements. The translated text preserves the warning that a small qualitative interview set cannot establish market share or statistical confidence. Its persona table retains the distinction among evidence, interpretation, and assumptions.
- `social-media-planning` keeps the puzzle shop and its two-question, one-use-case, one-event weekly mix explicitly illustrative. It does not present that mix as a platform rule or traffic guarantee. It preserves the distinction between engagement, sales, understanding, and trust; the reply, privacy, and moderation boundaries; and the requirement to define comparable metrics.
- All six article references per locale remain structured `ArticleInline` entries with the original target kind and slug. The API resolves them using target-locale published documents (`apps/api/app/guides/series.py`), and the web renderer displays plain text when the target reference is absent (`apps/web/components/content-blocks.tsx`). A target that exists only as a draft in a language therefore does not become a broken clickable link.
- The `zh-CN` wording uses mainland terms such as `营销`, `信息`, `记录`, `字段`, `排期`, and `帖子`; `人物誌` is rendered consistently as `用户画像`. URLs, dates, codes, and credits remain unchanged.

## Asset and layout evidence

- Structural and SHA-256 audit: `<home>/.codex/article-localization-release/batch037-pair-a/audit-receipt.json`, SHA-256 `92bb0ad2d88cd0c0fa929130148785147eb17dbf6261faa21d227d9979b5e6f2`. It checks both original pack hashes, the unchanged source documents/root metadata, each target block shape, source URLs/dates, image geometry and credits, original asset hashes, and all 24 new assets. It records per-document and per-asset hashes. Generated JSON and SVG files were normalized to LF before staging; sampled staged and working-tree SHA-256 values match.
- Edge 154 browser render and text-boundary receipt: `<home>/.codex/article-localization-release/batch037-pair-a/render-receipt.json`, SHA-256 `28a64a208b715fd6d99330594bbf38840f36c8f2dfabe61c2ac03e60531063ac`. All 16 localized hero/diagram SVGs were rendered at 1600×900; the browser reported zero canvas or card overflow. Eight JPG covers were produced from those browser renders. The four contact sheets and individual previews are under `<home>/.codex/article-localization-release/batch037-pair-a/previews/`. The author and an independent reviewer visually inspected the contact sheets for clipped text, missing glyphs, and overlap; none was found.
- Independent Pair B read-only review: `<home>/.codex/article-localization-release/batch037-social-content-preflight-20260928/pair-a-independent-preview/layout-report.json`, SHA-256 `fe490af2f35d949c7ba0d41b4a0cba11553591f810ffac87bcba07fbc2ed6543`. It independently rendered all 16 SVGs with card-margin and text-overlap checks, found zero issues, and spot-checked document structure, article targets, source titles, caveats, and EN/JA/KO diagrams. No actionable findings.

## Validation and release boundary

- `uv run python -m app.guides.pack_cli lint --kind life --slug stp-persona-research --slug social-media-planning`: passed, two packs. Existing `no_summary` advisories remain in all five languages because the source article has no summary block; the English body length advisories are 6,878 and 6,847 characters against the 6,000-character guide.
- Focused API tests: `tests/test_guides_content_pack.py`, `tests/test_guides_content_links.py`, `tests/test_guides_links.py`, and `tests/test_guide_rich_blocks.py`: 29 passed, 13 skipped.
- `npm run check:i18n`: passed, five locales and 25 namespaces. `npm run check:tasks`: passed with unrelated stale-claim/overlapping-task warnings.
- `npm run typecheck:web`: passed. Focused web component tests for `content-blocks`, `guide-image`, `article`, `article-page`, and `lib/guides`: four files and 123 tests passed in the first run; Vitest timed out while starting the `article.test.tsx` worker under concurrent repository test load. A separate run of that file passed all 40 tests. The combined focused coverage is 163 passing tests across two runs; the first command itself exited nonzero because of the worker startup timeout.

The branch is a review draft. It does not merge, deploy, import, publish, or change the production site. CI and a fresh source/version check remain gates before any later release action.

## Independent editorial correction on 2026-09-28

A further independent review of PR #911 at
`893ff4adaa862d634b74ea746209ad53f4b089c5` read all eight target documents and
checked the source, metadata, 24 localized assets, and their render receipts. It
identified a source-meaning error in the simplified Chinese social-planning
document: an existing audience community had become an existing social-media
platform. The sentence now says
`没有足够信息时，不把想象中的受众当成已经存在的社群。`
The same document's `放著不管` is corrected to `放着不管`.

The structural comparison permits exactly two changed text values:
`/locales/zh-CN/blocks/5/text` and `/locales/zh-CN/blocks/20/text`.
All five documents still validate against `GuideDocument`; the source document,
other locales, root metadata, STP pack, and every asset are unchanged. The prior
visual evidence therefore still applies. This supplement replaces only the old
social-planning pack and simplified Chinese document hashes; it preserves the
original audit as historical evidence.

| Artifact | Previous SHA-256 | Corrected SHA-256 |
| --- | --- | --- |
| `social-media-planning.json` (UTF-8 LF bytes) | `f416e8357f96e1311fb8f636a84eb34a51ecee1dd6e0af72cb21d42c52bc7db8` | `7450262ad063b15ac494b47a814f9436e19a5d159206e5d791aaf957193216fe` |
| `zh-CN` document (UTF-8 JSON, sorted keys, compact separators, unescaped Unicode) | `1f209d198fba6a16dd50d3e2c8dfb8e42d706b1ffaf6d51b2ba88dc6dbf5d7e6` | `7edc3d09013dd6f1ef155c3abea078f2bb9adacacadf3c509773b395d12ae494` |

An independent follow-up reviewer re-read both complete paragraphs against
`zh-TW`, recomputed the corrected hashes, verified the two-value-only diff and
all five document schemas, and found no remaining editorial blocker. The
unchanged asset and source evidence remains applicable.

Scoped `pack_cli lint --kind life --slug social-media-planning` passed after the
correction, retaining only the existing no-summary and English-length advisories.

This is a repository editorial correction. It does not perform or establish a
production deployment, content import, publication, or public-site acceptance.
