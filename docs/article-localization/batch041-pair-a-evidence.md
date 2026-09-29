# Batch041 Pair A: SEO keyword and title guides

This record covers `seo-keyword-research` and `seo-title-writing`. Both are
already published life guides; this branch is preparing their four missing
languages and text-bearing artwork. It has not deployed, imported, or
published a locale.

## Pinned sources

The four-lock read-only production receipt is
`receipt-20260928T134834Z.json`
(SHA-256 `01da33a9f151c5472997a449408593b2b8f4e789dcef06b7f0f9084f1760bb99`).
The full snapshot SHA-256 is
`3cbaeaea7c60d3139fa7cc9bbf2c475286c7652946a03412aa1fe0ddd92b15cd`.
It records a held host/main/clean/wrapper lock, a read-only repeatable-read
transaction, and `production_writes=false`. Both articles are active and
published at article v2. Each zh-TW draft and published document is v4 and
matches the repository source; zh-CN, en, ja, and ko have no rows.

| Guide | Pack SHA-256 | Normalized zh-TW SHA-256 | Blocks | Sources |
| --- | --- | --- | ---: | ---: |
| `seo-keyword-research` | `1384792649add24306aea80f76e274f2a837c9351661e846dba6f55c01e8f89d` | `4c59ec325c0e7cefe55a6cf62a58d9cba9860f2f0638f9bdfcfb5bb6bcd07929` | 32 | 5 |
| `seo-title-writing` | `88f444c85c32953cfe54e99166e234029f6400a537d12f009166136e0624ab4f` | `c35deec9315196507dcbaeb8b0e1e347a339e35ecba692a1c4a9baafc621e361` | 32 | 4 |

The source and asset inventory has SHA-256
`a1d44c2eb60092af75ce09fe1f85f52805c4e6f635ff79d475dda23b3a4bc7b1`.
Both pack hashes still match this branch's starting main `fa28079a`.

## Artwork stage

Each original text-bearing hero and four-card diagram SVG was translated into
zh-CN, en, ja, and ko while preserving its shapes, layout and original credit.
The 16 new SVGs were rendered in Edge 154 at 1600×900; the eight hero renders
were exported as language-suffixed JPEGs. The strict report found zero canvas
overflow, text overlap, or card-boundary issues across all 16 cases. Independent
contact-sheet review found no visible missing glyphs or clipping. The receipt
`asset-render-receipt.json`
has SHA-256 `cd7fe39256484f6ae95d0e6676d53a85b41e8bdab111490bfb4825422794f363`
and contains each SVG/PNG/JPEG hash and text bounding box.

## Locale documents

All eight missing documents are staged in the two packs, with the original
root metadata and zh-TW document parsed-identical to their pinned sources.
The keyword candidate was prepared outside the repository at
`seo-keyword-research.all-locales.candidate.json`
(SHA-256 `1dd67c76d9b9f8de1960a1628c01317846d250abfba9d1b7a9a38a32131ece74`).
Its structural audit receipt has SHA-256
`fb708e39c978bafe216dca5090b22631c136b678a5728b3521cb6b93a2b68d58`:
32 blocks, five source URLs/dates, the ordered list and six-row comparison
table survive in each locale. External pack lint found zero errors.

The title candidate at
`seo-title-writing-draft.json`
has SHA-256 `0696ef4e8c13f93e8b391dc6fb8b5f6a86470dfd7ee4f04ebe6375ba9dcb2450`.
Its external audit and GuideDocument schema check passed: 32 blocks and four
source URLs/dates per locale, no changed zh-TW or root metadata. Both candidates
were copied only after rechecking exact source file SHA-256 and parsed source
parity; the repository diffs contain locale insertions only.

Each source has two related-reading article links whose target-locale
publication is not established. The eight new documents translate the visible
labels but represent them as plain text inlines, so readers do not get clickable
links to an unavailable localized article. This explains the expected
`no_internal_link` lint warnings. The source format already lacks a summary
block, explaining `no_summary` warnings. These warnings are recorded rather
than replaced with a short abstract posing as the full translation.

On 2026-09-28, current official
[Google Ads Keyword Planner help](https://support.google.com/google-ads/answer/7337243?hl=en),
[Google Trends data FAQ](https://support.google.com/trends/answer/4365533?hl=en)
and [Search Console query-dimension documentation](https://support.google.com/webmasters/answer/17011259?hl=en)
were checked against the keyword guide's access, estimate, 0–100 relative
scale, privacy and row-limit caveats. These claims remain aligned. The source
citation `checked_on` dates remain unchanged from the pinned zh-TW document;
this editorial review did not silently rewrite their historic provenance.

Independent peer review corrected four keyword-guide strings. The en/ja
planning paragraph now says to record additions after the article is
complete, matching zh-TW rather than delaying until publication. The
zh-CN related-reading label uses `可执行`, and its diagram alt uses
`排期验收` instead of a misleading scheduling term. Root metadata and
zh-TW remain unchanged. The keyword diagram's en/ja/ko subtitle and footer
now preserve the source's idea that a group of related reader questions forms
one article topic. All 16 SVGs were rerendered after this change; the current
receipt above reports zero layout issues. Independent final peer QA passed
for both guides: the structural/asset audit SHA-256 is
`1c03de612b9e890770eb29d2c574d5f3f57c271be8e768ea77bcbafa684014f1`.
Its standalone Edge gallery is
`gallery.html`;
the preview receipt SHA-256 is
`3fe8ced2491249a07e484acaa8c8f828e42294342d665ae91fc05a665dfcd9a5`.
All eight documents rendered at desktop 1365px and mobile 375px, with both
images loaded and zero page overflow or browser errors. This remains local
draft preview, not public-site verification.

On 2026-09-28, current official
[Google title-link guidance](https://developers.google.com/search/docs/appearance/title-link),
[Discover guidance](https://developers.google.com/search/docs/appearance/google-discover)
and [WordPress heading-block documentation](https://wordpress.org/documentation/article/heading-block/)
were checked against the title guide's title-length, display, clickbait and
heading claims. They remain aligned. As above, the original source citation
dates are kept for provenance.

Local checks after the locale documents were installed: both pack lints
passed with the recorded warnings; `tests/test_guides_content_links.py`
passed 3/3; `npm run check:i18n` validated five locales across 25
namespaces; `npm run check:tasks`, `npm run lint:web`,
`npm run typecheck:web`, and `git diff --check` passed. The CI web job on
content commit `120377fbdece6254b3d474732b2c42d7df9ad0a0` also passed;
it runs Web tests, tools tests, build and isolated browser tests. A separate
local `npm run test:web` session was interrupted after more than 20 minutes
without output; it is not counted as a pass. All nine CI checks later passed at `6c8440f4dfd371236274ecaecc947716c7653230`. The final main refresh and evidence/task update require a fresh CI run.

## Outstanding acceptance

- Complete CI, guarded import dry-run and
  later production/browser verification. This document does not count any of
  those pending steps as passed.


## Final review binding and source acceptance

The previous independent peer review is preserved. Rechecking its exact bytes
found only Git's CRLF-to-LF normalization in the two pack files; converting the
current LF bytes back to CRLF reproduces both original review hashes exactly.
No translated wording was changed. Every localized image matches the reviewed
render bytes and its tracked Git blob. Root metadata and zh-TW remain identical
to current main. The final receipt below binds normalized GuideDocument values
and the actual LF pack bytes intended for Git.

The coordinating agent also extended local standalone previews to all five
locales: 20 desktop/mobile cases, all 32 blocks, five/four sources, both images,
zero browser errors and no page overflow. All first-screen sheets were inspected.
This does not replace Next.js or production page verification.

Strict editorial intake now records one inherited failure per source: the first
block is a paragraph rather than summary. Internal targets, self-reference count
and diagram numbers pass. The separate unclaimed summary-review task preserves
this unresolved acceptance item; zero-error pack lint is not an intake pass.
The draft PR still awaits current CI and editorial acceptance. Release has its
own unclaimed task and remains gated on the unavailable isolated Docker rehearsal.

- Final review receipt SHA-256: `91c3801224784c30fc93f2236e86cf2525358ea63ffa6e15a3292c81853f8adb`.
- Final preview receipt SHA-256: `dc92f5abc726895d1ab242fb220d5e5177840bc0f26a6eafef77fa6c3ca8659b`.

| Pack | Locale | Reviewed normalized document SHA-256 |
| --- | --- | --- |
| `seo-keyword-research` | `zh-TW` | `4c59ec325c0e7cefe55a6cf62a58d9cba9860f2f0638f9bdfcfb5bb6bcd07929` |
| `seo-keyword-research` | `zh-CN` | `a13df2f8839ecae45b1c70b1ba2612ff78968fc7801b71e77eebb614a582e400` |
| `seo-keyword-research` | `en` | `eedfae3dc174cf65ae7797d51ab510524e375d5da9126ad386b93a5ba870abe7` |
| `seo-keyword-research` | `ja` | `6b1e3ff00e4c2a0b9bdde951ee8f7d88852232aa59eebfd5dfecc6ea57df13b3` |
| `seo-keyword-research` | `ko` | `a8b76c00a289f20fa3d07197b4c3386e1c153c302c3e145981690e1351598ca9` |
| `seo-title-writing` | `zh-TW` | `c35deec9315196507dcbaeb8b0e1e347a339e35ecba692a1c4a9baafc621e361` |
| `seo-title-writing` | `zh-CN` | `c4804819e9c99ff10577900e8c149f85b1cbc7e86af4fe1988b1a65559663f94` |
| `seo-title-writing` | `en` | `49479ee491b2c8c72316b159d4639a631a41b073acdc2c71ec8ef5ab00a80387` |
| `seo-title-writing` | `ja` | `b73ef38377e499082fd6cb1eea5ba67c66b88b0c89ab0ede8dccb96d74644fb3` |
| `seo-title-writing` | `ko` | `82d41007b995431184f6d524da41a6bc75806d6c8a974d00b0fee306ee6d2776` |

Final LF pack hashes:

- `seo-keyword-research`: `5dff294b42067bb0cf5015d12d1d8264d436defee3fa7e4068b5736949264e6b`.
- `seo-title-writing`: `f35ee83ce3df05e8dc82743ba2832df8e73dedab56ad3a74c3b0a3914efdd447`.
