# Batch043 Pair A: Google ranking history and Trends research

This repository candidate adds complete zh-CN, en, ja and ko documents to two published zh-TW life articles. It includes 24 localized assets: editable hero and diagram SVGs plus 1600×900 JPEG covers for each new locale. The existing zh-TW documents, root metadata, credits, source URLs, source check dates and three publication-aware article references per document remain unchanged. Nothing was imported or published to production.

## Source lock

The four-lock production read-only inventory `receipt-20260928T160437Z.json` has SHA-256 `003dde60b8e1849fac50dced292c1d74515e4c6b11a90abf286a3d21953a5c07`. It verified main `57eb97b9b6766d565f06aa50d55cdec2f995e309` against active, published article version 2 and zh-TW draft/published version 4, with no target locales present. Its transaction was read-only and it records no production writes. Both baseline pack hashes still match current origin/main at review.

| Article | Source pack SHA-256 | Reviewed five-locale pack SHA-256 |
| --- | --- | --- |
| `google-ranking-history` | `64f8e8845daa167877a507f64ce9562a9200091dd54c47bee3e34bb35b077f49` | `fa95257b8cac78c182541209fc541d0ea7cbaf85a0690b96eaace036306efb08` |
| `google-trends-research` | `0d13e794d19a3af52d7ee7d4d0feb0a34c429fc19b8d23c91456a46bba74cba7` | `fcf396b87434d039ac81b585255cb42baa5c962318c289502d98ec8c985189cb` |

## Content and independent review

All eight translations retain 33 blocks, including the complete headings, paragraphs, ordered steps, table, callout, captions, alt text, source titles and article labels. Ranking history preserves five source URLs; Trends preserves six. All retain the source check date 2026-09-14. ArticleInline kind/slug references remain unchanged and resolve only when the target language is published. Taiwan remains the Trends example market in every language; no local ranking, paid account trial or real measurement is claimed.

The coordinating Codex agent independently read each translated document against the source after the authoring subagent stopped at its quota. English, Japanese and Korean needed no correction. Simplified Chinese terminology conversion errors were found and corrected by the coordinating agent: core versus kernel, manual actions, restore data, queries, domain names and record terminology. The explicit before/after correction log covers 60 string fields (including SVG text), without changing source facts. The same coordinating agent applied and rechecked those corrections; this does not claim a separate second reviewer of that final edit set.

Current primary-source checks confirmed the historic Panda/Penguin dates, August 2013 Hummingbird context, the distinction between core updates and manual actions, and Google's recommendation to wait at least one full week after a completed core update for comparative analysis. Trends retains normalized 0–100 interest, low-volume/noise caveats, comparable query settings and the strictly greater than 5,000% Breakout threshold. References: [ranking systems](https://developers.google.com/search/docs/appearance/ranking-systems-guide?hl=en), [core updates](https://developers.google.com/search/docs/appearance/core-updates?hl=en), [manual actions](https://support.google.com/webmasters/answer/9044175?hl=zh-Hans), [Trends data](https://support.google.com/trends/answer/4365533?hl=en), [related searches](https://support.google.com/trends/answer/4355000?hl=en). These review checks do not replace the original source check dates in the translated documents.

| Article | Locale | Reviewed document SHA-256 (sorted compact UTF-8 JSON) |
| --- | --- | --- |
| `google-ranking-history` | `zh-TW` | `214873bb713abd01291cf804a7de820301c6aa3769c3b831f4f130621ab68272` |
| `google-ranking-history` | `zh-CN` | `d69fb6df95df78c7db0b8f8fec3a7b0fc215d096c2bf771b1a5a8cf1509c16c0` |
| `google-ranking-history` | `en` | `88d1c7ac191532f2f0b95c589200e3ce006277cb08c85689cc4bba586fb5ce00` |
| `google-ranking-history` | `ja` | `36a64b7f6d836e30213d1cc63f5980e8336371f11d6293074565e4e098c8dd50` |
| `google-ranking-history` | `ko` | `fc89d51cb759a1f38c7bab526400ae9be5080f42707897a506d16bff88ac868e` |
| `google-trends-research` | `zh-TW` | `742aa3eddb782574afd534a480773ed2aac6db4d7d999ed0b191f72825a2d4fe` |
| `google-trends-research` | `zh-CN` | `5e0fb574c155d0cc418ef492b88b6eb159907de116aa9435e99054f602073007` |
| `google-trends-research` | `en` | `9a7b5ecd25b8cc9033055f1c49ee035a8dae4ef69b093db169bfedbc65002205` |
| `google-trends-research` | `ja` | `727a9dcb7e588c0b5c537fef5ab0a48812e2e6456c8668c179b0f2b139e1dc5e` |
| `google-trends-research` | `ko` | `63ee885d9afcf9b11548bd1896564a2d621bc8be8420f6aa3fd3defc89f8a8c6` |

The external `review-hashes.json` binds all candidate bytes, document hashes and the 24 localized image files: SHA-256 `6c41f52a2b2510eaeabcd305643ccfc00728ed2f8d42f5dc362e641a186ce6de`. Terminology correction log SHA-256 `3ad036ae546cad1f768a67409a80b4ebfb4418ad0718ed2b5b7c47a285ede4a5`.

## Visual and local validation

All 16 SVGs were rendered in Edge and measured against their text containers, with zero measured overflow. The reviewer inspected all eight full-resolution diagrams and all four-locale cover sheets. Original artwork credits remain Mokaair. Simplified Chinese asset filenames use `zh-cn`. JPEG covers were regenerated from the localized SVG masters; original assets are unchanged. Temporary diagram previews remain outside the commit.

All five languages were captured for both articles at 1365×900 and 375×812: 20 local standalone page renderings, 33 blocks per page, both images loaded, no console/page errors and no page-level horizontal overflow. Desktop/mobile heading and cover sheets were reviewed. Large diagrams and tables use their own scroll containers on mobile. These are standalone draft HTML previews, not Next.js or production canonical/hreflang/browser acceptance.

`render-report.json` SHA-256 `372d3af968ee3a1ddc97717c1ef3226e2f2d7fe5c02497c292ee253fc9a59cd0`; `preview-receipt.json` SHA-256 `a2f6c8de1f5e25cfdffccf9ca183f457784b6e802c69983072a54555c853d5ca`.

- Pack structural audit: source/root equality, five locales, eight complete 33-block documents, preserved source URLs/dates, 3 article references per document and localized asset dimensions pass.
- `pack_cli lint --kind life --slug google-ranking-history --slug google-trends-research`: exit 0. Inherited no-summary advisories and optional English body-length advisories (6,557 / 6,625 characters) are retained; content was not shortened to satisfy a length hint.
- `pytest tests/test_guides_content_links.py tests/test_guides_content_pack.py -q`: 12 passed, 5 database-dependent tests skipped locally. CI must cover database integration.
- Strict `intake_check.py --from-content`: exit 1 for each unchanged source, reporting a paragraph instead of a first `summary` block and two self-references instead of at most one. Article references and diagram numbers pass. These inherited findings are recorded in task `2026-09-28-review-batch043-inherited-editorial-intake-failures` in PR #951; strict editorial intake is not reported as passing.

## Release state

| Article | Four target documents | Local images/previews | Draft import | Public publication | Public browser verification |
| --- | --- | --- | --- | --- | --- |
| Google ranking history | Complete, reviewed with noted corrections | Passed | Not performed | Not performed | Not performed |
| Google Trends research | Complete, reviewed with noted corrections | Passed | Not performed | Not performed | Not performed |

Before a separate release, require merged green CI, the same-image isolated rehearsal, deployed assets, current live source/target-draft/version/visibility checks, verified backup and guarded explicit article/locale manifest. The owner currently has no available nonproduction Docker environment. Do not infer production acceptance from local previews or CI smoke.
