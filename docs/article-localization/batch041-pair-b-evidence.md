# Batch041 Pair B SEO artwork stage

This branch prepares artwork for `on-page-seo-workflow` and
`image-seo-workflow`. The read-only production baseline
`C:\Users\x8120\.codex\article-localization-release\batch041-seo-readonly-inventory-20260928\receipt-20260928T134834Z.json`
(SHA-256 `01da33a9f151c5472997a449408593b2b8f4e789dcef06b7f0f9084f1760bb99`)
records both articles active/published at v2. Their zh-TW draft/published
documents are v4 and match the pre-correction repository packs; all four
target locales are absent. No production write was made.

## Source artwork

| Guide | Hero SVG SHA-256 | Diagram SVG SHA-256 |
| --- | --- | --- |
| `on-page-seo-workflow` | `cf9a318e63d48e47585ec7d269aab62f9c7c55c3082cefff45c026b9b80e66b6` | `2ac41b609c83865f4724e3ea8c8bd91511b4143c00998e7c14c112cde166fff2` |
| `image-seo-workflow` | `0a013a296bd47390ad31e3ea9b9c1f145076bd34a46e6b6d43d720afe511c9b7` | `4182b3d53d96f0ba79a3800bfedf28eed6d9f5badcee1511055f4367711ec88c` |

The pinned generator outside the repository is
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-b-assets.py`.
It preserves the original SVG files, shapes and Mokaair credit while changing
the title, description and visible text into zh-CN, en, ja and ko. Output names
use locale suffixes. The Edge 154 renderer
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-b\render-assets.cjs`
rendered 16 SVGs at 1600×900 and exported eight JPEG covers. Receipt
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-b\asset-render-receipt.json`
has SHA-256 `fb7c933f2f66254f590c5a3549022e43c3b67b14d64d0f563f28ce4caa0e37a6`:
16/16 zero overflow, text overlap or card-boundary issues. Both four-locale
contact sheets were visually reviewed, with no missing glyphs or clipping.

## Remaining

The four-language article documents must be installed and reviewed separately.
The on-page pack source SHA-256 is
`2f27bcb83a1e327b29ed7584d2bbfa3208954251c72aaf0e13192f07f813b9a7`.
Image SEO source must use the corrected pack from #934, whose SHA-256 is
`b10f6e1f633cff9a13ef0470af157fdd4d0b5616b560141c6e17819fda7c0357`.
The current live zh-TW v4 predates that correction, so a guarded live source
revision is required before four-language publication. Pack/link/asset/API/Web
checks, CI, dry-run import, release and public visual verification are pending.
