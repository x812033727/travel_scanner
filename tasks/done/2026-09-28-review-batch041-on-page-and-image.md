---
id: 2026-09-28-review-batch041-on-page-and-image
title: Review Batch041 on-page and image source summary blocks
status: done
priority: P2
area: docs
owner: codex-batch041-summary-20261003
claimed_at: 2026-10-03T09:53:30Z
created_at: 2026-09-28T17:34:18Z
completed_at: 2026-10-03T10:05:35Z
branch: codex/unfinished-tickets-20261003
depends_on:
  - 2026-09-28-install-reviewed-batch041-image-seo-language
  - 2026-09-28-localize-on-page-seo-workflow-article
scope:
  - apps/api/app/guides/content/on-page-seo-workflow.json
  - apps/api/app/guides/content/image-seo-workflow.json
---

# Review Batch041 on-page and image source summary blocks

## Why

Strict intake reports one inherited source failure in each of on-page-seo-workflow
and image-seo-workflow: first block is paragraph instead of summary. Localization
preserves existing source text and does not silently rewrite published content.

## Definition of done

- [x] Review any source correction as a distinct versioned change.
- [x] Keep all five editions consistent without dropping details or changing facts.
- [x] Re-run strict intake, locale checks and exact source/review hash binding.

## How to verify

Run intake_check.py --from-content separately for both slugs, then scoped pack lint.
Internal targets, self-reference counts and SVG numeric checks already pass.

## Notes

Leave unclaimed until localization scope is released. Source changes require
fresh review and guarded live reconciliation before production import.


## 2026-10-03 reviewed local summary correction

Claimed normally as `codex-batch041-summary-20261003` on
`codex/unfinished-tickets-20261003`, after both dependencies were done and
localization PR #941 had merged as `4dc3bd4812451762885c73ab96ce88a719069f0b`
(original head `ad7145abc9f60afe260426946d62a82132782dae`, 9/9 successful checks).
The source baseline is repository main `5af4ffebfcea96fd23b387288901e513ed63d4f7`.
The later #1104 zh-CN vocabulary edits are preserved. A targeted collision check
found no current open-PR, remote-head, worktree dirty-file or active claim overlap
for these two packs and this task. Three historical local branches match the
already-merged #941/#934/#498 content. No source assets or shared localization
folders were edited.

Each of the ten opening paragraphs already states the article's reader task or
its central image-explanation principle. Its exact 2-3 sentences are now
`summary.items`; the original words and punctuation rejoin exactly, and no inline
reference existed in these first blocks. All other JSON values, block counts
(32/33), metadata, source dates/URLs, links and all 30 assets (20 SVGs) are unchanged.
This is a structural source correction, not newly fact-checked prose.

Validation uses this checkout's frozen dependencies and Python 3.13.15:

- Before: strict intake failed all ten editions for the missing first summary;
  the two English editions additionally failed the pre-existing length band.
- After: both zh-TW sources and zh-CN/ja/ko pass (8/10). English still fails only
  `body_length=7020` / `6526`, outside the default `1500-6000` band. All ten
  summary failures are resolved. No reader-first check was disabled and no
  threshold was increased; complete English content is preserved.
- Both scoped pack lints exit 0. Existing English length and absent internal-link
  advisories remain; the prior localization review intentionally preserves
  text-only references until the targets are published.
- The two-pack locale script exits 0 with zero hits. Content-pack/content-link
  pytest reports 12 passed, 5 PostgreSQL integration skips. Scoped diff check passes.
- Separate independent review passed against both final pack hashes, all ten
  normalized document hashes and all 30 assets. It independently confirms that
  the original opening words and punctuation rejoin exactly, the summary content
  fits each article's reader purpose, and every other JSON value remains unchanged.
  The review also validates two ArticlePacks and all ten GuideDocuments.
- The two inherited English length failures are tracked separately in
  `2026-10-03-batch041-english-intake-length`; the owner was asked about the
  editorial choice, and the full text is preserved pending that answer.
  No whole strict-intake PASS or new browser acceptance is claimed.

Private evidence set: `batch041-summary-20261003`, containing before packs,
proposal, exact pointer differences, all source/target/asset hashes, individual
before/after logs, and the local correction receipt. Receipt SHA-256:
`c753afebaf3f8ff5235dae2da7722aef8b6b014e02d141a45f0fef5767ca80a5`.
Independent review receipt SHA-256:
`16ccf353d2f16811e1bfd8e5bcb1a1cddc38939d07390518485d507700ce9502`.

These are GuideDocument-normalized hashes computed by
`document_hash(ArticlePack.locales[locale].model_dump(mode="json"))`, not live
published hashes or raw pack hashes:

| Slug | Locale | Repository before | Repository after |
| --- | --- | --- | --- |
| `on-page-seo-workflow` | `zh-TW` | `4916a8cc37818e40960e39a28243f2bc8c62f5f07457745ea70f59505a924479` | `4f7a862668f648b5e200998ab8152e94403dbd1970e14e7f08fa051f844c06eb` |
| `on-page-seo-workflow` | `zh-CN` | `b5ab2a19cca59b13c3cbbd88dc8f1a62a0808ef4298bb9f7b89863ef49e46858` | `1a68d2ce6db651e7d1dd6078fb134a51817a27f2d0544d3a0ee3138bc878a515` |
| `on-page-seo-workflow` | `en` | `fdedd7db594797846c46614ec1c570a6c0aa81f3ef0ed3e114afc858e015e912` | `e0b2f978a4ef5946e7e51141fe0aaaa522b4998111220f7f09ccf680682b2b31` |
| `on-page-seo-workflow` | `ja` | `93af5cae9e98710541935b067c0379677f5719d6665323493ca61ad0a2857049` | `19fedd53cb2b7635b8b49c85709e28b83ac94934348caced3e1af4aa7aabdcdf` |
| `on-page-seo-workflow` | `ko` | `e29c3c2e5789283a02ae9bc5ae3547854d77da406a666786223c6f7658419162` | `77734c949c45f2421b983c39f0acd4b828ddae3bca75861f449ac2f1333b499e` |
| `image-seo-workflow` | `zh-TW` | `e359a3d9f84fb59983424ec12a82369839d88c5570b1845e0c3c5af5345e433d` | `4e1eb6771f7cf14ef41a195eb6a69c291144a3ebec228328342802cab94bf6f5` |
| `image-seo-workflow` | `zh-CN` | `f7c90be51532375c3ff018c55773b66365513d8383891b10c6c3f7438dc29bd7` | `3c84c304f7787d147cc4492fcb1a87638c45c6ff834390e8e0a17b671ace82b3` |
| `image-seo-workflow` | `en` | `9254857df9bb2dc059e2762dafa5558831315d0599df753e388c32f98c20ad6e` | `87a21456ee66abfaf2ad9d55b46323fb33b57da9d96d7db287997ed2dda9657d` |
| `image-seo-workflow` | `ja` | `89af3e12f925071f0b291e503f81e34f26c7768023aa0bc5f4229ccdf92d957a` | `69c05eb16b95a701b46be4fe1ce9d6bcb6f3423ae75ef3d3fa27fa6e0d595b3a` |
| `image-seo-workflow` | `ko` | `9ed7ce44b430a7077e1102de5d6cc57e6d612291089afe521cba793468b5102c` | `cef9aa9e575f8cabd9233609fb938c96c7d5ef2e1f2d5332e6a8211297a07677` |

Final raw pack SHA-256: on-page `7219c405f799af8e0c52d751473aec92be68e05bd7ad02514a8a0e4010157df4`;
image `2811ab71370444a67d7cd1c40933cfe4d4b1e4ed5f96dde8c9345e73fa23815a`.

No fresh live `source_correction.py` receipt was created: no live draft/published
versions were read or invented. No production connection, import or publication
occurred. Guarded source reconciliation and newly bound source/translation release
evidence are still required before any future import. Older localization/release
receipts remain historical and cannot authorize these new hashes.
The reviewed source correction and its task record are a distinct commit in
draft PR #1175, separate from the already-merged localization change. Completion
here covers the summary-structure repair and its local review; the follow-up
length decision and guarded live import remain unfinished.
