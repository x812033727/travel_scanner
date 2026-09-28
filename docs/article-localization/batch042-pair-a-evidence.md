# Batch042 Pair A: search intent and content quality

Scope: `seo-search-intent` and `seo-content-quality`, two published zh-TW SEO guides. The four missing locales are zh-CN, en, ja and ko. This branch stages localized artwork and records the repo-external article candidates. It does not change either article JSON while the source-link correction task owns those files.

## Baselines and candidates

- Read-only production inventory: `C:\Users\x8120\.codex\article-localization-release\batch042-readonly-inventory\receipt-20260928T150309Z.json`, SHA-256 `167d0a345864d1a3ca2117b585e8aaee91e5ef7dcd099954efd65f28e783f29f`.
- Repo inventory: `C:\Users\x8120\.codex\article-localization-release\batch042-readonly-inventory\candidate-inventory.json`, SHA-256 `2df6cd72344c96025188ab1407459a669d37d1c20d300a77897c4ec288fadfd5`.
- Source-link correction is [PR #942](https://github.com/x812033727/travel_scanner/pull/942). Its corrected zh-TW source is frozen outside the repository for translation. `seo-search-intent` SHA-256 `420e80f7c483ac21c1d3a5c9803e8daee846dd5e60c687e48354bb23d695f0ab`; `seo-content-quality` SHA-256 `aa8e6b95b373ec4f2fab13e9a99798173532541c760407cf07daf259b229880f`.
- Combined five-locale candidates are stored at `C:\Users\x8120\.codex\article-localization-release\batch042-pair-a\seo-search-intent.all-locales.candidate.json` (SHA-256 `66a73f28a0ab023ed9cc8eefbc08d9b47875483c270264edfa72000cf1153189`) and `seo-content-quality.all-locales.candidate.json` in the same folder (SHA-256 `44439b54099953e6c451e94855f010bc1512972488a92dca2d60ca5dc9e25a65`). The candidates are not imported or published.

## Content and link handling

Each of the eight new locale documents has all 32 source blocks, including the table, ordered checklist, callout, image alt/caption, related-reading labels and localized source titles. Root pack metadata and zh-TW document are unchanged. Source URLs, checked dates, image attribution, dimensions, block types, heading levels, callout tone and list ordering match the corrected source.

The two misleading zh-TW AI glossary links are replaced by text in PR #942. Related-reading links and the generative-AI glossary link remain plain translated text in new locales because there is no verified public destination for those locale routes. No target locale links to a non-public article.

## Artwork

Each guide has four localized versions of its original text-bearing hero SVG, 1600×900 JPEG cover and four-stage SVG diagram: 16 SVGs and 8 JPEGs in this branch. Original zh-TW assets remain unchanged; Mokaair credit is retained. Image text, title and accessible descriptions were translated. The diagrams retain the four source stages and their meaning.

The structural and asset audit at `C:\Users\x8120\.codex\article-localization-release\batch042-pair-a\structure-asset-audit.json` (SHA-256 `33099ef6f74b9c8dbc4e5524e1d05d87c637adae2e68e58f1e5911c8da0d0092`) passed for two packs, eight documents, 32 blocks each, exact source URLs/dates, every local image path, SVG parse, JPEG 1600×900 dimensions and 24 asset hashes. Microsoft Edge rendered all 16 localized SVGs and measured their text bounding boxes: no canvas or card overflow (`svg-browser-bbox.json`, SHA-256 `b28651a0cff6f9532ef3af1fd5f0ae735ad961f8be43ffaf0f050699f1993f34`). Independent language and desktop/mobile preview review remains in progress.

## Publication boundary

No live article, image, import, draft or release has been changed. After PR #942 merges and its task scope is released, recheck source hashes before installing these candidates into the article packs. Any intervening source change requires reconciliation first. Production publication still requires the guarded release gate and a suitable non-production rehearsal environment.
