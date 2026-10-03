---
id: 2026-09-28-review-batch040-pair-a-inherited-editorial
title: Review Batch040 Pair A inherited editorial intake failures
status: review
priority: P2
area: docs
owner: codex-batch040-editorial-20261003
claimed_at: 2026-10-03T10:21:11Z
created_at: 2026-09-28T17:25:09Z
completed_at:
branch: codex/unfinished-tickets-20261003
depends_on:
  - 2026-09-28-install-reviewed-batch040-affiliate-and-store
scope:
  - apps/api/app/guides/content/affiliate-marketing-basics.json
  - apps/api/app/guides/content/independent-store-marketplace.json
---

# Review Batch040 Pair A inherited editorial intake failures

## Why

Strict `intake_check.py --from-content` reports inherited source failures:
affiliate-marketing-basics starts with a paragraph instead of summary and has
three 本文/這篇 references (limit one); independent-store-marketplace starts with
a paragraph instead of summary. The localization preserves existing source text.

## Definition of done

- [ ] Review whether and how the existing published source should be corrected.
- [ ] Make any accepted correction as a distinct versioned change with review.
- [ ] Update all five editions consistently and rerun intake and source checks.
- [ ] Refresh release source/review bindings if documents change.

## How to verify

Run strict intake separately for both exact slugs and scoped pack lint; verify
source/locale hashes, complete paragraphs, attribution and unchanged facts.

## Notes

Unclaimed follow-up; do not overlap the localization claim. Internal article
targets and all SVG numeric checks passed. These failures are not hidden behind
the zero-error pack lint result. Do not silently modify the live source.


## 2026-10-03 local correction; release work remains open

Claimed normally as `codex-batch040-editorial-20261003` on
`codex/unfinished-tickets-20261003`, after the installation dependency was done.
PR #953 merged as `1dbb4ec15657892528f435e29c18903eaca042f6`; its original head
`ea66796f8d110ae74818e0dbce9c699887e9ecbd` had 9/9 successful checks. This local
baseline is main `21728c1d35123657ee2aae3a8b10e4389e6f1148`, including the later
#1104 zh-CN vocabulary correction, which is preserved.

The two source packs and this task's open/done paths were checked against the
three open PRs, 34 live remote heads and 28 registered worktrees. No current scope
changes or active claims collided. Historical local branches matched the already
merged #953/#954/#930/#498 scoped bytes. Collision evidence is in the private
`editorial-candidates-20261003` receipt set; no broad localization folder was edited.

Local implementation, independently reviewed below:

- All ten opening paragraphs became 2-4 `summary.items`, retaining every original
  sentence and punctuation with exact text rejoin. No first block had an inline.
- In affiliate zh-TW/zh-CN descriptions, removed the redundant 本文 prefix. At
  block9, changed the author-subject sentence to the equivalent explicit statement
  that unverified product prices or shipping fees are not listed; no limit or
  advice was removed. Japanese block9 omits only この記事では、 and retains the
  full statement about unconfirmed prices and shipping fees.
- The fictional desk-guide reference and every block16 disclosure example remain
  unchanged. Do not treat these quoted/example references as disposable prose.
- Every other JSON value, source/date/number, ArticleInline, whole paragraph,
  block count (33/32), and all 30 assets (20 SVGs) are unchanged. The five explicit
  self-reference text pointers are explicitly recorded; this is not a claim that
  the entire edited document is byte-identical.

Validation (Python3.13.15, frozen dependencies, no database services):

- Before strict intake: all ten editions failed missing first summary; affiliate
  zh-TW/zh-CN/ja additionally failed self-reference limits. Other pre-existing
  failures were retained in the baseline logs.
- After strict intake: both zh-TW sources pass. All ten summary failures and three
  excess-self-reference failures are resolved. The eight target editions still
  fail because `marketing-metrics-roi-roas` and `utm-link-conventions` (affiliate
  blocks30/32), or `woocommerce-store-launch` (store block30), lack their respective
  en/ja/ko/zh-CN documents. Store English additionally remains 7,362 characters,
  above the unchanged 1,500-6,000 band. Full text and ArticleInline nodes are kept;
  no check was disabled and no threshold was raised.
- Two-pack lint exits 0, with only the existing store English length warning.
  Locale checks exit 0 with one existing hint: store Korean block4 contains
  統一發票 while the source says 發票. That paragraph is unchanged and this work
  does not newly fact-verify its terminology.
- Scoped content-pack/content-link pytest: 12 passed, 5 PostgreSQL fixture skips.
  Scoped diff check passes. No all-locale strict PASS or browser acceptance claimed.

Private `batch040-pair-a-editorial-20261003/local-correction.json` binds the full
before/after pointer diff, 10 documents, 30 assets, tools and per-locale logs.
Receipt SHA-256: `c4b6b6a2c2190a0df47758c2efd3473cc0c8db27af5be0675e1a012edc78dcba`.
The following hashes are `document_hash(ArticlePack.locales[locale].model_dump(mode="json"))`,
not raw pack hashes or live published hashes:

| Slug | Locale | Repository before | Repository after |
| --- | --- | --- | --- |
| `affiliate-marketing-basics` | `zh-TW` | `c893c8eafcb6b941454590103fbac8359c0db4d29d03e1597a788acac56fc0ce` | `def0b3e312560d9b78fc86dd12402dd2bb948e685461c480ee33cd7fe89acf6c` |
| `affiliate-marketing-basics` | `zh-CN` | `e641651be4ae027a4438fe0280e0143ca56ac2b2d0c661dbf3c0c90b8ab2a4ab` | `a544c7aadd7e200ff419a60a661daa7142c933575b2763fe88c2d79abdc652cf` |
| `affiliate-marketing-basics` | `en` | `59d903bf04ff70a43be15338b550d4acd07ae187cddd55a407f1c99edef32346` | `8d1ebec7acda5a2ebd837f7d388bb7a274b12090d5ec962126ff2321ac54a2cc` |
| `affiliate-marketing-basics` | `ja` | `81defe39a0b72d6c8713d4cbcee63f653156d081af487ecb880f25f4b2f41d26` | `8e3f2b719f0c04995bc3d1d635c0530bf980c47b453ca06a1bb0fbe10ff5f9b6` |
| `affiliate-marketing-basics` | `ko` | `2fde2eaabb5806bd943b0764a36964820e6593b798f5dda07a891890457a62ef` | `e500f680a9d7ac6f57ae4e1c706402514a905b92dac23d3c48add4ed0417809c` |
| `independent-store-marketplace` | `zh-TW` | `7cf113f88ce54b02f4e0b096584107bf7fb69093b8d5dd74829222a7d6d03985` | `2a4554751bb89ee847f442398ccccd84d52930d992dd524e0d48a0b5007f0f75` |
| `independent-store-marketplace` | `en` | `d5ff72f6812047ca05a76b0bd219524ead5b977a524d960bb163e0c5fa8cc39d` | `f2542ec428617c812b3f26698b93bbb4a0b23789a97e4b1969a4180f7ee8c325` |
| `independent-store-marketplace` | `zh-CN` | `1d8d659551cd1f322a886dc798cd62b481191fe52be6bb87ac74bbf6029e5102` | `aa4a7c0b7ed011f89e51edd152fdd7d56ed2b9896f3d7df9c9207a3c658dcbc8` |
| `independent-store-marketplace` | `ja` | `88abca048b9b07fb816ce88b627cc2c0004d25d30b52d30c0a75853fcc7084d5` | `93a3c71f166e01d6ad17df7f210c9eace7c03161369db9e210729ff5ae770eba` |
| `independent-store-marketplace` | `ko` | `2deecc52e3e944025ce4a50e5e68703805f80a88425f4c5e486cba78086b4687` | `c0b4681b608f255e38ff7944c0809397871ea4164c97a00c7cc0d47a1f55d85c` |

Raw final pack SHA-256: affiliate
`0370fc7d766a0af80b620b274ab0443bafcb54ec381ce7511d48cb003fde7212`;
store `29a6bdabecb195eae9693de0678c3bbe87a2a62d904805dd26d1f00f0bb964e3`.

Independent source review passed: private
`batch040-pair-a-editorial-20261003/independent-source-review.json`, SHA-256
`d9889e035ddf8c848deb6073e4cb048e70c27c6c85fe0daeb3813aa7b6dc7e6f`.
The independent reviewer confirmed all ten summaries, five self-reference edits,
schema/document hashes and unchanged assets. This is local editorial acceptance.

**This task is not complete.** The original
release source/review binding DoD remains unchecked. Local document hashes do
not update release bindings. No fresh live source_correction receipt, production
connection, source-version reconciliation, import, publication or new browser
acceptance occurred. Historical release receipts remain immutable; future release
work must capture fresh source versions and bind these reviewed files separately.
