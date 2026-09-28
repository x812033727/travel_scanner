# Batch043 Pair B: search-result CTR and Semrush research

This candidate adds `zh-CN`, `en`, `ja`, and `ko` to the existing `search-results-clickthrough` and `semrush-research-workflow` life packs. Their published `zh-TW` documents, root metadata, status, ordering and credit fields remain unchanged. It stages repository content only; no live import or publication occurred.

## Source lock and scope

The four-lock, read-only production receipt at `receipt-20260928T160437Z.json` has SHA-256 `003dde60b8e1849fac50dced292c1d74515e4c6b11a90abf286a3d21953a5c07`. It records both articles as active, published life articles, article version 2, `zh-TW` draft/published version 4, and no target locales. It verified the production source documents against repository main `57eb97b9b6766d565f06aa50d55cdec2f995e309` in a read-only DB transaction and made no production writes.

| Pack | Base pack SHA-256 | Current five-locale pack SHA-256 |
| --- | --- | --- |
| `search-results-clickthrough` | `dc87f91fa9a94921e2b413030e908af458c08bd11ca220179d3aaa506da7441e` | `bd65735eaf6d6c3769dfe52415e024d54692047c7a03595f486e0a5c3b1e34b1` |
| `semrush-research-workflow` | `9a040175eca486ec278c4ac21f8ef57d1782bc0a802e88e321382f7081e8a2f8` | `582dea87082a00ed1836ef3f654806f8b298d4954ad23e3b8580bcca96aeebba` |

The parsed root metadata and `zh-TW` document in each current pack equal their exact main baselines. The new eight documents each retain all 33 block positions, headings, lists, tables, callouts, image credits/dimensions, seven source URLs with original `2026-09-14` check dates, and the source article target kinds/slugs. The CTR example remains 1,000 impressions/100 clicks/10%, then 2,500/150/6%, a 4-percentage-point (40% relative) CTR decrease despite 50 more clicks. The Semrush definitions retain KD versus PKD, Missing/Untapped/Weak, estimated Traffic Cost, and the original Position Tracking caveats. No example is represented as a live account measurement.

The source uses `ArticleInline` rather than hard-coded locale URLs. The API resolves a target only when that specific language is published; until then the web renderer shows the label as plain text. This preserves the three internal targets in the Semrush document and four in the CTR document without exposing draft destinations.

## Source review and artwork

Official primary documentation checked during this translation: [Google impression/position/click definitions](https://support.google.com/webmasters/answer/7042828?hl=en), [Search Console Performance data](https://support.google.com/webmasters/answer/17011364?hl=en), [Google title links](https://developers.google.com/search/docs/appearance/title-link), [Google snippets](https://developers.google.com/search/docs/appearance/snippet), [Semrush Keyword Magic Tool](https://www.semrush.com/kb/617-keyword-magic-tool-manual), [PKD](https://www.semrush.com/kb/1434-how-is-personal-keyword-difficulty-calculated), [Keyword Gap](https://www.semrush.com/kb/28-keyword-gap), [Keyword Magic Tool dates](https://www.semrush.com/kb/1138-date-range-in-kmt), [Organic Rankings](https://www.semrush.com/kb/890-Organic-Rankings-Overview), and [Position Tracking](https://www.semrush.com/kb/548-configuring-position-tracking). These confirm the key definitions and limitations above. Existing source URLs and check dates were preserved; this review does not imply a logged-in Semrush trial.

Both Mokaair original covers and diagrams were adapted from their SVG masters, with local text and accessibility metadata in all four new languages. Every language has a `hero-<locale>.svg`, 1600×900 `hero-<locale>.jpg`, and `diagram-1-<locale>.svg`; simplified Chinese filenames use the repository convention `zh-cn`. The original four SVG SHA-256 values are, respectively, CTR hero `84f134bdb5999bb073810a73b8bcdc24535a08fd227070dca6b5fad875866a52`, CTR diagram `309edbabb493a2c26ff12d1b1075aefab981ccf929f351efac1d6c67795b3e31`, Semrush hero `98a75ed7df09f86d1057ac2430d04b0f5bb9de6f5c5bd847ebd8a31ee992648f`, and Semrush diagram `7c305791c8e8cfc560ff08fa7c9af9bbf281df50b4c8d21fd9c84353004f8de5`.

The local asset contact sheet (`contact-sheet.png`, SHA-256 `ee41a25dc0a58f15fb5e39c78be02d77f0c2eb6e14a654c256dd955d058c82d2`) shows the 16 SVGs at half resolution. Each JPEG reports 1600×900; XML parses and all text nodes are nonempty. A font-measured audit checked 168 SVG text nodes against their containers and found zero overflow (`svg-text-bounds.json`, SHA-256 `945da59826023a1be986b6e2d91057163b7fa8c7cf4ce6aea1b3e266398aed25`). Structural audit (`structural-audit.json`, SHA-256 `1a172aa6a91a1cd25dba452bc96a90ff0abbbe68178de7a43c8d8c9c2d2bda6f`) checks source parity, document shape, links, URLs/dates and all 24 asset paths. Independent full-resolution review by the coordinating Codex agent passed on 2026-09-29 (Asia/Taipei). The reviewer is distinct from the authoring subagent. All eight target documents were read against the source; all eight diagrams were inspected individually at full resolution, and all localized covers were checked in the asset sheet and page previews. No content correction was required. Final text assets use LF line endings.

## Checks and release boundary

- `uv run python -m app.guides.pack_cli lint --kind life --slug search-results-clickthrough --slug semrush-research-workflow`: exit 0, two packs. The inherited no-summary advisory applies to the unchanged source and all targets. Complete English translations trigger the optional life-guide length advisory (6,259 and 6,956 characters); content was not cut to satisfy a length hint.
- `npm run check:tasks`: exit 0, 1,067 task files; repository-wide stale/overlapping-task warnings are unrelated to these narrow scopes.
- `git diff --check`: exit 0.
- `uv run pytest tests/test_guides_content_links.py tests/test_guides_content_pack.py -q`: exit 0, 12 passed and 5 database-dependent tests skipped locally. CI must cover the database tests.
- Additional `intake_check.py --from-content` returns exit 1 for each pack: the unchanged zh-TW first block is not `summary`, and the source description/body has two self-references instead of at most one. Source hashes and parsed equality demonstrate these are inherited editorial findings. Article targets and image-number checks pass. Follow-up: `2026-09-28-review-batch043-inherited-editorial-intake-failures`. This stricter intake is not reported as passing.

Before any separate release, recheck the exact repository source, live versions/hashes/visibility, target-locale drafts, image deployment, publication-aware article links, CI and the guarded batch manifest. This candidate does not claim public availability or browser-verified publication.

## Independent review binding

The final `review-hashes.json` has SHA-256 `c14856077452313f69bde39e3bdeab5f5d8400d99d9b7e79800f134f2c65f074`. It binds the candidate pack bytes, canonical document hashes (UTF-8, sorted keys, compact JSON), and all 24 localized image files. Original and target documents were compared block by block, including numeric examples, caveats, applicable readers, link targets, captions and source titles.

| Pack | Locale | Reviewed document SHA-256 |
| --- | --- | --- |
| `search-results-clickthrough` | `zh-TW` | `044084730f228bcef446f084aca1da9618459f79128066b912a452d2db5fda35` |
| `search-results-clickthrough` | `zh-CN` | `58cde11d58239bc1a81fc79d7743bbeae78e29988c0ed6f5fff71e5aab5bde58` |
| `search-results-clickthrough` | `en` | `162e570c577bef16028354f1ca2a688883518801cd72cbfdf0adbab2ef60de8e` |
| `search-results-clickthrough` | `ja` | `3692cf27bfe8823291f64f780f49b6866f6917540eda5f57fc4e0a5c95fcf38b` |
| `search-results-clickthrough` | `ko` | `c3110d5cc35c0d91f7c1155921d63d7a75b744d56f875dee333b3d74fcc6ed97` |
| `semrush-research-workflow` | `zh-TW` | `74ccf69e1ae02db5b585e49a24a18ce3685a36ada140d03493fa2e76313d237c` |
| `semrush-research-workflow` | `zh-CN` | `46b19b0d6013ecdfe4564f0c125a8a8eb23be3fa35b3aab4779d8861645e86ea` |
| `semrush-research-workflow` | `en` | `5db396d977e9bb1fd6caac78d026c32b8492308268ac2565fdcc26210f4bad45` |
| `semrush-research-workflow` | `ja` | `140178c3b848b6b5a94fc9af85b9ada69625c9656f7394f9e5af6086ccf6bffe` |
| `semrush-research-workflow` | `ko` | `49de4a7d9cdb42d89357e0ffccb759f144f45ba31318e05e0e43caad607ac3d7` |

Local standalone HTML previews were captured in Microsoft Edge for both articles in all five locales at 1365×900 and 375×812: 20 renderings, all 33 blocks present, both images loaded, no console/page errors and no page-level horizontal overflow. The reviewer checked the desktop/mobile cover and heading sheets; the large diagrams scroll within their own containers on mobile. `preview-receipt.json` SHA-256 `67af115217f3aacaa8c2b80b3eea7017a3bc6c8f7ff16f1e763b65113dba9350`. These previews are local layout checks, not the Next.js application and not production canonical/hreflang or publication acceptance.
