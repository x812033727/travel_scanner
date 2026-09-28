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
has SHA-256 `621ef947fd8081a9e41a10f3bfdb311a6c0c12a383865a43bf08b3a1c97e03f8`
and contains each SVG/PNG/JPEG hash and text bounding box.

## Outstanding acceptance

- Complete and review the eight locale documents, including description,
  rich text, tables, warnings, source titles, alt text and captions.
- Keep the zh-TW documents and pack-level metadata byte-equivalent to source.
- Validate article links against each destination's actual locale publication
  state. Google Ads, Trends and Search Console interface/metrics claims need
  current official-source review before publication.
- Run focused pack/API/Web/i18n/task checks, CI, guarded import dry-run and
  later production/browser verification. This document does not count any of
  those pending steps as passed.
