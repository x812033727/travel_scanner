# Batch040 Pair B: product SEO and zero-click translations

Both article packs now contain complete zh-TW, zh-CN, English, Japanese and Korean documents. This batch adds eight translations and 24 localized image assets (eight hero SVGs, eight 1600 × 900 JPG covers and eight diagram SVGs). Original zh-TW documents, article metadata, original images, source URLs, attribution and checked dates remain unchanged. Repository completion is separate from database import, publication and live browser acceptance.

## Source binding

The source is the #930 correction, now merged into main. #948 closed the source task and recorded live-source reconciliation. This branch incorporates main `e6155e0903cacf488d2c1299adaff5d8f5a56684`; installation verified each main source pack and every staged document/image against the frozen receipts before modifying either JSON pack. Historical CRLF/LF differences in SVG files were checked for exact newline equivalence; committed asset bytes were preserved.

The guarded read-only snapshot from 2026-09-28 recorded both articles as active/published article v2 with zh-TW draft/published v4, and no target-locale rows. It predates the live application of #930; it is not a current release preflight. The correction replaces three false AI-glossary links with unchanged plain text. Any eventual release must reconcile the live source through `2026-09-28-batch040-live-source-reconciliation` and preserve later edits and visibility changes.

| Installed pack | SHA-256 |
| --- | --- |
| `ecommerce-product-seo` | `3b02c4865a5534a01e36cf812091b16c845a976b9f9a19c3cc3f4e000f21edd9` |
| `zero-click-search-strategy` | `cfbdcbb0c8b67d98e23a59308a4d1a8269918b5c602939fcee81715e06592e91` |

## Editorial review

The coordinating agent independently read both originals and every title, description, heading, paragraph, list, callout, table, image description/alt/caption and source title in all eight translations. Each edition retains 33 ordered blocks, the five ecommerce or four zero-click source references, exact checked dates and seven remaining publication-aware ArticleInline targets. No further translation correction was needed. Link labels do not establish that a destination language is published.

The product article retains the original storage-box example, variant URLs, single-page versus multipage canonical choices, ProductGroup/Product relationships, merchant listings versus product snippets, actual price/stock/image consistency and the limits of structured-data testing. It does not invent product tests or a deployment. The zero-click article retains the illustrative 1,000 impressions, 50 clicks and 5% site CTR; these do not establish a market-wide 95% zero-click rate. Call-button clicks remain distinct from completed calls/jobs, with attribution and mixed Ads/organic limitations intact.

Strict editorial intake is **not fully passed**. Both source documents begin with a paragraph rather than a summary block; ecommerce has three source self-references and zero-click has two, against the limit of one. These inherited issues are separately tracked in `2026-09-28-review-batch040-pair-b-inherited-editorial`. They were not silently rewritten during translation. Internal article targets and SVG numeric checks passed.

## Images and local browser checks

All 16 localized SVGs passed the final Chromium geometry checks with zero clipping, card-margin or overlap issues. The coordinating agent inspected all eight final full-resolution diagrams and the final five-language desktop/mobile cover sheets; no missing glyphs, overlap or numeric mismatch was found.

The final standalone article preview loads the installed packs and assets, including the unchanged original locale, at desktop 1280 × 900 and mobile 390 × 844. All 20 cases passed: complete block/source counts, loaded 1600 × 900 covers, required image alt text, no horizontal overflow and no page errors. This HTML preview approximates article layout; it is **not** the actual Next.js route or production acceptance.

## Verification receipts

Raw receipts and screenshots remain outside the repository. The following portable identifiers bind the review to exact bytes:

| Receipt | SHA-256 |
| --- | --- |
| Frozen source | `dc2a772198bce10926b59e023bf23b046f1eb0c9a9b243caf1e8f7e500a85253` |
| Original staged content/asset audit | `2421f31f36971d1fcae810f3c2ba1de6b73eb5ff6f8d6063dd7e6b08a52e2bee` |
| Read-only inventory receipt | `676b67043693c188020e6adf9d5b16bd1e25a4b0a44f8660ed6034fb970dcd0d` |
| Final SVG layout report | `b1942ede56c4d84e50eb4f5e8af315eb363406656b793df2ab3cff9b9c2fde15` |
| Installed content/assets and independent review | `10090e34f05628d40c4cc9c12b57f0ce9844e32711c354819ce87e4bbcf38785` |
| Final 20-case article preview | `4b59cd826138eadc20eca1135eacf4261c27315807ced5c010bbc05b32424746` |

Scoped pack lint reported zero errors (English length advisories: 7,862 and 8,136 characters). Focused content-pack and guide-link tests passed: **15 passed, 11 database-dependent skipped**. Strict intake limitations are listed above. Current-head repository CI must pass before merge; task validation is run before push.

## Remaining release work

`2026-09-28-release-reviewed-batch040-product-seo-and` tracks the explicit two-slug/four-target-locale release. The same-image nonproduction Docker rehearsal environment remains unavailable, so production is NO-GO. No new database rows, deployment, import, publication or live acceptance is claimed. Release requires editorial acceptance, current source/version reconciliation, backup and write-control checks, exact-list dry run, idempotency/conflict checks, and five-language canonical/hreflang/link/image verification on real routes.
