---
id: 2026-09-28-review-batch040-pair-b-inherited-editorial
title: Review Batch040 Pair B inherited editorial intake failures
status: review
priority: P2
area: docs
owner: codex-batch040-editorial-20261003
claimed_at: 2026-10-03T10:28:02Z
created_at: 2026-09-28T17:43:02Z
completed_at:
branch: codex/unfinished-tickets-20261003
depends_on:
  - 2026-09-28-install-batch040-product-seo-and-zero
scope:
  - apps/api/app/guides/content/ecommerce-product-seo.json
  - apps/api/app/guides/content/zero-click-search-strategy.json
---

# Review Batch040 Pair B inherited editorial intake failures

## Why

Strict intake reports four inherited source failures: both packs begin with a paragraph rather than summary, ecommerce-product-seo has three source self-references and zero-click-search-strategy has two (limit one). Localization preserved the published source structure and wording.

## Definition of done

- [ ] Review whether and how the existing source should be corrected.
- [ ] Make an accepted correction as a separate versioned and reviewed change.
- [ ] Keep all five editions consistent and rerun strict intake, scoped pack lint and source checks.
- [ ] Refresh release document hashes and source/review bindings after any change.

## How to verify

Run strict intake separately for the two exact slugs, preserve complete paragraphs/facts/attribution, and compare five-language document and image hashes.

## Notes

Local source correction claimed below; release follow-up remains open. Internal article targets and SVG numeric checks already passed. Zero-error pack lint does not conceal strict editorial failures. Do not silently change the live source.


## 2026-10-03 local correction; release work remains open

Claimed normally as `codex-batch040-editorial-20261003` on
`codex/unfinished-tickets-20261003`, after the installation dependency was done.
PR #954 merged as `49aa683a050df824204166c4f15656c603be2dab`; its original head
`b4bfad7f98dc6e0668c7ace07d8b1117e6ca883d` had 9/9 successful checks. This local
baseline is main `21728c1d35123657ee2aae3a8b10e4389e6f1148`.

The same four-pack gate used for Pair A covered both packs and this task's
open/done paths: three open PRs, 34 live remote heads and 28 registered worktrees,
with no current scope changes or active-claim collision. Four local historical
branches matched already merged scoped bytes. Evidence is in the private
`editorial-candidates-20261003/batch040-collision.json`; no broad localization
folder was edited. Claim succeeded without force.

Local changes, independently reviewed below:

- All ten opening paragraphs became three `summary.items`. Every original word
  and punctuation rejoins exactly; no first block had an inline.
- Removed only repeated author self-reference prefixes in six zh-TW/zh-CN/ja
  descriptions and the three ecommerce block1 first text inlines. The dated
  2026-09-14 Google attribution and the original-example/no-product-test,
  no-price-recommendation/no-store-deployment boundaries remain verbatim.
- Ecommerce block9 is wholly unchanged, retaining the explicit statement that
  the article does not set merchant transaction rules and that the responsible
  person should confirm them. Zero-click's original-scenario/no-real-data,
  no-market-wide-percentage and no-assumptions-as-observations boundaries remain.
- These 19 explicit pointers are the complete content diff. All other values,
  sources/URLs/dates/numbers, ArticleInline nodes, 33 blocks per edition and all
  30 assets (20 SVGs) are unchanged. English and Korean retain all original text.

Validation (Python3.13.15, frozen dependencies, no database services):

- Baseline strict intake failed missing summary in ten editions and excess
  self-reference in six editions. After the correction all 16 such failures are
  resolved; both zh-TW sources pass.
- Eight target-language documents retain their pre-existing missing-target
  failures: ecommerce blocks30/31/32 target `woocommerce-product-information`,
  `canonical-url-guide`, `knowledge-graph-entities`; zero-click blocks26/32 target
  `ai-term-artificial-intelligence`, `ai-search-tools-measurement`. These targets
  lack the relevant en/ja/ko/zh-CN editions. ArticleInline references were kept.
- English remains 7,862 / 8,136 characters, exceeding the unchanged 1,500-6,000
  band. No text was shortened, checks disabled or thresholds raised. Therefore
  strict intake is 2/10 PASS, not full localization or release acceptance.
- Two-pack lint exits 0 with only those existing English length warnings. Locale
  checks exit 0 with zero hints. Scoped content-pack/content-link pytest reports
  12 passed, 5 PostgreSQL integration fixture skips. Scoped diff check passes.

Private `batch040-pair-b-editorial-20261003/local-correction.json` binds exact
before/after pointers, ten documents, 30 assets, tools and per-locale logs.
Receipt SHA-256: `6ca3160a2382a59c2c2b8d3f1c94be9cc797c7ac756c79a4734f3e16027a6281`.
The following are normalized `document_hash(ArticlePack.locales[locale].model_dump(mode="json"))`
values from repository files, not raw pack or published/live hashes:

| Slug | Locale | Repository before | Repository after |
| --- | --- | --- | --- |
| `ecommerce-product-seo` | `zh-TW` | `25fe33ce82acaf264b19525ae192c3ca880891b8eebda6b28ef5435fffc9b2ee` | `6f0229058c271390e42def9dbafcc05554127d6dd29701b239729df1116dcec5` |
| `ecommerce-product-seo` | `zh-CN` | `0527e40fa3057a329d10c236a63c609e41f87c64595f678c74698dd6fc5e5b23` | `c92ad211d901dffe6620d9aa1e8d8d33f590334deeae661b5e93cc8ec3d715cc` |
| `ecommerce-product-seo` | `en` | `179dc082f7f70b3e1b4564294f9db0550622cd31fb8ca9528c12b62077bca67a` | `ec560691159cee2300d2826d6e8aa866385c4fd16ef5554ee1025af695ef941c` |
| `ecommerce-product-seo` | `ja` | `9a79b3ec62b053726580b079eab62212a56d4c5ee9776fca5b83c0ef01f1f0bc` | `469005ed1c06c7d11e96582cf7e4488812514e434349bfcd37df7f96e3dbe0c7` |
| `ecommerce-product-seo` | `ko` | `2a841f12c410eed7c1a8685ee3e20beb076c3b100c4dab123feb138a1f62326f` | `48fc75c38cb1c87bbfd8c043ccc9b97a445335109c59b4325ff4c48a126b7357` |
| `zero-click-search-strategy` | `zh-TW` | `2c0660c39def2c8b42aeac4ce1da4c0960d76eb99a48018298d7626a25307902` | `62ee13cdf40b8c226ef4a5905c1a446c0efc1c6d753239357460384404d4ae1c` |
| `zero-click-search-strategy` | `zh-CN` | `225e9c41e6042edfbf05a7a5e925d085b159348d0ea4fa21be0356d292a05d43` | `cd5d89f3c10fc8ab35dc0341225581aa7cebbff809a75ed62893487742f7aa9a` |
| `zero-click-search-strategy` | `en` | `dece135cba2abc5c915191270ca53c6d4e5a482f46e54ef3f3b61b5e91b2944a` | `b82ed8231ffc49a2d9da77198ac34c254d14c4f569a53b882b759bf6b6cad3e6` |
| `zero-click-search-strategy` | `ja` | `ecb208f3c894ae38f33a55b83f123d60c2ab1814e244eecd396b3846ff63dc71` | `bc813ca40c1fd3a54f30633cfdda473985434d52b59ad4460e71d26caa8b3724` |
| `zero-click-search-strategy` | `ko` | `666904c88ba0bad06c37019ae8bae120e8fcb35fd861645b016be2c0153d9d56` | `f9078e571fbf6322510c85bbd9bf886cb64d11275b834c2f4370fd31f64ff9ca` |

Raw frozen pack SHA-256: ecommerce
`76a0e0f6858e01e6fe639bd780f2e2b6743894d49e93352018ba4e8fa70e80e9`;
zero-click `84016de3c5b4687a02a25a6d7cfaa18219757722fcfd4f44f07c900df9f1258b`.

Independent source review passed: private
`batch040-pair-b-editorial-20261003/independent-source-review.json`, SHA-256
`6cb8d7bf44017053da21a943f3ef8782f754fcf0c55852a9298eb9cbbd1afe07`.
The independent reviewer confirmed all 19 pointers, ten summaries, source/fact
boundaries, schema/document hashes and unchanged assets. This is local editorial
acceptance; the separate source change is being reviewed in this PR.

**This task is not complete.** The original
release source/review binding DoD remains unchecked. Local hashes do not update
release bindings. No fresh live source_correction receipt, production connection,
source-version reconciliation, import, publication or new browser acceptance
occurred. Historical receipts remain immutable; future release work must capture
fresh source versions and bind these reviewed files separately.
