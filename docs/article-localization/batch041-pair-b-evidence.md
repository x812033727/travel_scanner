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

## On-page document stage

The four missing on-page SEO documents were copied from the re-audited
external candidate
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-b\onpage-draft\on-page-seo-workflow.all-locales.candidate.json`
(SHA-256 `7532179b8bcc2124bfdfb6f49ce4a480fc165dd1f8516b555a1f8e81567e496e`).
The current repository source file matched the pinned SHA before copying;
root metadata and zh-TW remain parsed-identical. Each new document retains
all 32 block types/order, six H2s, four list items, six table rows, six
original source URLs and checked dates. The two related-reading labels use
`rich_paragraph` blocks with translated text-only inlines: neither target
locale publication state is confirmed, so there is no premature public link.
The pack diff adds locale documents only. After installation, two zh-CN
wording fixes were made in the repository copy; the exact installed pack
SHA-256 reviewed by the peer is
`f3c0bb3813c790509c8109222aba048378a45c23458c80c1a9a53a0ac7cc2f1b`.
Independent editorial and desktop/mobile review passed for this document and
the corrected image SEO candidate. The final peer report SHA-256 is
`bf2c0098aca43ead8a04edb366d61e28415501e4e6c2384f98fd43d40933a70f`;
its eight-page gallery SHA-256 is
`336e763cdaa481cabea6ee7096539aeed9724bb3d1d39659bc94af3314d24eae`.
All 16 desktop/mobile renders passed without overflow, broken images or
receipt hash mismatches. This is standalone local preview, not public-site QA.

## Remaining

The corrected image SEO four-language candidate is staged outside the
repository at
`C:\Users\x8120\.codex\article-localization-release\batch041-pair-b\image-draft\image-seo-workflow.all-locales.candidate.json`
with SHA-256 `4b6e1e3fc25c2ca2c5f0e796b5a999daae8e467f9bee7b1a1ecf28e207d54605`.
The peer reviewed those exact bytes and verified the zh-CN diagram alt,
keyword/record wording, and Taiwan website-editor scope in en/ja/ko. Its
English length warning is advisory; the full source examples and cautions
remain translated. The image SEO documents must be installed after
#934 releases its source scope. The on-page source SHA-256 was
`2f27bcb83a1e327b29ed7584d2bbfa3208954251c72aaf0e13192f07f813b9a7`.
Image SEO source must use the corrected pack from #934, whose SHA-256 is
`b10f6e1f633cff9a13ef0470af157fdd4d0b5616b560141c6e17819fda7c0357`.
The current live zh-TW v4 predates that correction, so a guarded live source
revision is required before four-language publication. The source-shaped
no-summary and unpublished-link warnings are expected.
Local on-page pack lint passed with zero errors, content-link API tests passed
3/3, `npm run check:i18n` validated five locales across 25 namespaces,
`npm run check:tasks` validated 1,052 task files, and `git diff --check`
passed. The English body-length warning is advisory; retaining all source
examples and cautions takes priority over cutting content solely for the
length guideline. CI, dry-run import, release and public visual verification
are pending.
