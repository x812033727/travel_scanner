# Batch041 Pair A: SEO keyword and title guides

This record covers `seo-keyword-research` and `seo-title-writing`. Both are
already published life guides; this branch is preparing their four missing
languages and text-bearing artwork. It has not deployed, imported, or
published a locale.

## Pinned sources

The four-lock read-only production receipt is
`C:\Users\x8120\.codex\article-localization-release\batch041-seo-readonly-inventory-20260928\receipt-20260928T134834Z.json`
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
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-a\asset-render-receipt.json`
has SHA-256 `cd7fe39256484f6ae95d0e6676d53a85b41e8bdab111490bfb4825422794f363`
and contains each SVG/PNG/JPEG hash and text bounding box.

## Locale documents

All eight missing documents are staged in the two packs, with the original
root metadata and zh-TW document parsed-identical to their pinned sources.
The keyword candidate was prepared outside the repository at
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-a\keyword-draft\seo-keyword-research.all-locales.candidate.json`
(SHA-256 `1dd67c76d9b9f8de1960a1628c01317846d250abfba9d1b7a9a38a32131ece74`).
Its structural audit receipt has SHA-256
`fb708e39c978bafe216dca5090b22631c136b678a5728b3521cb6b93a2b68d58`:
32 blocks, five source URLs/dates, the ordered list and six-row comparison
table survive in each locale. External pack lint found zero errors.

The title candidate at
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-a\title-draft\seo-title-writing-draft.json`
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
receipt above reports zero layout issues. The desktop/mobile standalone article preview
receipt is being finalized; it is not public-site verification.

## Outstanding acceptance

- Finish independent editorial and desktop/mobile rendered-page review of all
  eight locale documents, including tables, warnings, alt text and captions.
- Recheck title-link, Discover and WordPress interface claims against current
  official sources before publication.
- Run focused pack/API/Web/i18n/task checks, CI, guarded import dry-run and
  later production/browser verification. This document does not count any of
  those pending steps as passed.
