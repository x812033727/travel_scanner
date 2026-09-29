# Batch043 Pair A: Google ranking history and Trends research

This repository candidate adds complete zh-CN, en, ja and ko documents to two published zh-TW life articles. It includes 24 localized assets: editable hero and diagram SVGs plus 1600×900 JPEG covers for each new locale. The existing zh-TW documents, root metadata, credits, source URLs, source check dates and three publication-aware article references per document remain unchanged. Nothing was imported or published to production.

## Source lock

The four-lock production read-only inventory `receipt-20260928T160437Z.json` has SHA-256 `003dde60b8e1849fac50dced292c1d74515e4c6b11a90abf286a3d21953a5c07`. It verified main `57eb97b9b6766d565f06aa50d55cdec2f995e309` against active, published article version 2 and zh-TW draft/published version 4, with no target locales present. Its transaction was read-only and it records no production writes. Both baseline pack hashes matched origin/main at that original review; after PR #952 merged, main contains the five-locale candidate hashes below. This historical inventory is not a fresh release preflight.

| Article | Source pack SHA-256 | Reviewed five-locale pack SHA-256 |
| --- | --- | --- |
| `google-ranking-history` | `64f8e8845daa167877a507f64ce9562a9200091dd54c47bee3e34bb35b077f49` | `fa95257b8cac78c182541209fc541d0ea7cbaf85a0690b96eaace036306efb08` |
| `google-trends-research` | `0d13e794d19a3af52d7ee7d4d0feb0a34c429fc19b8d23c91456a46bba74cba7` | `fcf396b87434d039ac81b585255cb42baa5c962318c289502d98ec8c985189cb` |

## Content and independent review

All eight translations retain 33 blocks, including the complete headings, paragraphs, ordered steps, table, callout, captions, alt text, source titles and article labels. Ranking history preserves five source URLs; Trends preserves six. All retain the source check date 2026-09-14. ArticleInline kind/slug references remain unchanged and resolve only when the target language is published. Taiwan remains the Trends example market in every language; no local ranking, paid account trial or real measurement is claimed.

The coordinating Codex agent independently read each translated document against the source after the authoring subagent stopped at its quota. English, Japanese and Korean needed no correction. Simplified Chinese terminology conversion errors were found and corrected by the coordinating agent: core versus kernel, manual actions, restore data, queries, domain names and record terminology. The explicit before/after correction log covers 60 entries: 56 document string fields and four complete SVG text revisions, without changing source facts. The same coordinating agent applied and rechecked those corrections; that original review did not have a separate second reviewer of the final edit set. The subsequent independent review is recorded below.

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

## Final independent review — 2026-09-29, after merge

**Accept the exact candidate's translation and editorial fidelity, with no new
corrections requested.** Two reviewers distinct from the original authors and
correcting coordinator each read one complete five-locale article. Together they
read all 330 blocks, titles, descriptions, source fields, captions, alt text,
article labels and text in all 20 source/localized SVGs. Ranking's 32 correction
entries and Trends' 28 entries were individually accepted; every current value
equals the corresponding recorded after value.

PR #952 merged as `8be1cf9bcaddd697df99e505e33f562b010cfbd0` at
2026-09-29 05:21:34 UTC, before this final review began. This record reviews the
merged bytes and cannot supply retroactive pre-merge review or approval. Both
pack hashes and all ten raw canonical document hashes remain exactly those in
the tables above.

| Independent receipt | SHA-256 | Result |
| --- | --- | --- |
| Ranking full-text review | `c03a70fe8ea6cdc5491999a2cfa58c3ca38c1a2fda8467349127560a0872d49f` | Five documents, 165 blocks, 32 corrections accepted |
| Trends full-text review | `e171ab07d15b41eb163140e3b21185640a0c91d100bb74037b046e7315a3b101` | Five documents, 165 blocks, 28 corrections accepted |
| Separate integrity verification | `3984145981568611f04680ada03e3cffe27c5d3ce1a1cd6430b82129b3fc7985` | Two packs, ten documents, 30 assets and 60 after values match |
| Coordinator's selected primary-source spot checks | `336c6d9c7a083fe33569f947f1a7beaea631a6200dd62793c359fa356234246f` | Selected historical/ranking and Trends qualifications checked |

The full receipts remain outside the repository. The integrity verifier checked
native `ArticlePack` schema, exact pack bytes against the merged commit and prior
PR content commit, all 24 localized assets against the earlier review receipt,
and all six original assets against the source baseline. Source zh-TW documents,
root metadata, credits, source URLs/dates and all reference identities remain
unchanged. Raw document hashes use sorted compact UTF-8 serialization of the
original locale JSON. The new review receipts also name schema-normalized
`GuideDocument` hashes separately; those include defaults and must not be
substituted for the original raw hashes.

Existing local visual evidence was retained by exact binding: ten stored HTML
bodies match rendering of the current documents, all 20 prior preview results
record two loaded images each, and all 16 prior SVG geometry records match the
current text/font inputs. No browser was rerun for this final review. The old
preview receipt's `documentSha256` field actually contains a whole-pack hash;
individual locale hashes were verified separately. Forty stored screenshot files
were hashed now; the old receipt did not contain those screenshot hashes. The
before values in the correction log are historical coordinator evidence, not
independently attested by an uncorrected translation commit.

The Trends reviewer opened all six official source pages on 2026-09-29. Separate
coordinator spot checks revisited the [ranking systems guide](https://developers.google.com/search/docs/appearance/ranking-systems-guide?hl=en),
[core-update guidance](https://developers.google.com/search/docs/appearance/core-updates?hl=en),
[manual-actions report](https://support.google.com/webmasters/answer/9044175?hl=en),
[Trends data FAQ](https://support.google.com/trends/answer/4365533?hl=en) and
[related-search definitions](https://support.google.com/trends/answer/4355000?hl=en).
These checks supported the selected qualifications already recorded above; they
do not change the documents' authored source-check date or constitute a complete
new factual review of the ranking article.

Fresh local pack lint exited 0 with ten inherited `no_summary` advisories and
the two already-recorded English length advisories. No article, source date or
asset changed. The earlier pytest and layout results remain historical results;
they are not represented as new runs in this documentation-only review.

### Remaining acceptance boundaries

- The paragraph-first and self-reference findings remain on
  `2026-09-28-review-batch043-inherited-editorial-intake-failures`. Strict editorial
  intake has not passed and this review does not close that task.
- Trends correctly preserves the `life/seo-content-cannibalization` reference,
  whose repository pack currently has only zh-TW. Four target-language link
  destinations are therefore not established by this review. Preserve its
  identity and verify publication-aware rendering during the existing release
  task; do not claim that every reference is an available localized hyperlink.
  The API selects published targets for the current locale and the frontend
  preserves unavailable references as plain text. Acceptance therefore checks
  the correct localized link or plain-text fallback; it does not require adding
  four translations. Repository absence alone does not establish database state.
- Same-image isolation, fresh approved live state, backup, deployment, import,
  publication and public five-language desktop/mobile acceptance remain on
  `2026-09-28-release-reviewed-batch043-google-ranking-and`. No production access
  or operation occurred during this final review. Any future document or image
  change invalidates this exact-byte acceptance and needs renewed review.
