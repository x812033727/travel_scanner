# Batch038 source-link corrections before translation

Four public zh-TW guides used ordinary words as links to unrelated AI glossary
articles. The corrected packs retain those exact words as plain text. They are
the source candidates for the next five-language batch; this PR does not update
published database revisions.

Review: [draft PR #913](https://github.com/x812033727/travel_scanner/pull/913).

| Guide | zh-TW block | Word | Incorrect destination |
| --- | ---: | --- | --- |
| `customer-journey-funnel` | 7 | 標記 | `ai-term-token` |
| `customer-journey-funnel` | 19 | 參數 | `ai-term-model-parameters` |
| `ugc-word-of-mouth` | 0 | 標記 | `ai-term-token` |
| `marketing-copywriting` | 16 | 工具使用 | `ai-term-tool-calling` |
| `landing-page-cta` | 21 | 參數 | `ai-term-model-parameters` |

The guarded, four-lock, repeatable-read production snapshot was captured at
2026-09-28T11:23:03Z. It confirmed all four articles active/published at
article version 2, zh-TW published/draft version 4, no other locale rows, and
exact agreement with the repository source after `GuideDocument` normalization.
The read-only [snapshot receipt](C:/Users/x8120/.codex/article-localization-release/batch038-source-preflight-20260928/receipt-20260928T112259Z.json)
has SHA-256 `04a6c4082468109545f1d8fe054c18333db6aad9f14273f8ed1435da9a7739b3`.
The [exact JSON diff receipt](C:/Users/x8120/.codex/article-localization-release/batch038-source-preflight-20260928/diff-receipt.json)
has SHA-256 `f67d02e27eae9ed636d980d7367b9e1e86fbcc10213e7b8653d2252e0c4a5175`.
It asserts that the only changes are the five `article` inline nodes becoming
`text` nodes, with their displayed words unchanged; root metadata, all other
body content, images, credits, source URLs/dates, and intended article links
are identical.

| Guide | Published source document SHA-256 | Corrected document SHA-256 |
| --- | --- | --- |
| `customer-journey-funnel` | `2248c9e3878192970816dcc8def7951bff5aed0526cfb0188f1209b05ceabbc3` | `879d9ee8ebf60d7f6eb9f88ffe7cfcac5af563c9558aab848cc371963100cd33` |
| `ugc-word-of-mouth` | `6801bf41b6f6ba249622e3a5cb1ecc3365c3e974c45609c46ca823a9269facc2` | `5c13c8a48f2c2b7c63a0b12c0affd43df67a9af6464df3a6bf17752bf92be2bb` |
| `marketing-copywriting` | `8aa601c0f4896b26762777ba88c31b821c8630ba605a6285e518c49084963ecc` | `e00b538b56cb63eaf0a944ee62aa48ae516c3b189731d7f8953397c3e17d4bab` |
| `landing-page-cta` | `012df30273540e69a93014daa3e1f32bd9027f217041f6865a668066cce88ed3` | `7ddcb7251210ca6963b7882f9ed894bd11d142edc08d0cb266ab6e4bee2f845c` |

Before translation, publish a guarded new zh-TW revision with a fresh version
and hash check. If its published source differs, stop that article and review
the newer editor changes. Only then translate from the resulting published
revision. Import and browser validation remain separate release steps.

Validation: four focused pack lints passed with pre-existing `no_summary`
advisories; API content/link tests passed (12 passed, 5 environment skips);
`npm run check:tasks` and `git diff --check` passed. PR CI remains pending.
An independent read-only review compared parsed packs with the branch base and
confirmed exactly these five node changes, matching document and receipt hashes,
task scope, and snapshot pins. The snapshot is point-in-time evidence; a fresh
guarded version check is required before any published source revision.
