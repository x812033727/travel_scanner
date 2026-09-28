# Batch041 Pair B: on-page and image SEO localization

This branch completes four additional language documents and matching artwork for `on-page-seo-workflow` and
`image-seo-workflow`. The read-only production baseline
`receipt-20260928T134834Z.json`
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
`batch041-pair-b-assets.py`.
It preserves the original SVG files, shapes and Mokaair credit while changing
the title, description and visible text into zh-CN, en, ja and ko. Output names
use locale suffixes. The Edge 154 renderer
`render-assets.cjs`
rendered 16 SVGs at 1600×900 and exported eight JPEG covers. Receipt
`asset-render-receipt.json`
has SHA-256 `fb7c933f2f66254f590c5a3549022e43c3b67b14d64d0f563f28ce4caa0e37a6`:
16/16 zero overflow, text overlap or card-boundary issues. Both four-locale
contact sheets were visually reviewed, with no missing glyphs or clipping.

## On-page document stage

The four missing on-page SEO documents were copied from the re-audited
external candidate
`on-page-seo-workflow.all-locales.candidate.json`
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

## Final installation and review binding

Source correction #934 and task closure #948 are merged. After refreshing main
to `e6155e0903cacf488d2c1299adaff5d8f5a56684` and claiming the image pack, the
independently reviewed external image candidate was installed with no wording
change. It has original review SHA-256
`4b6e1e3fc25c2ca2c5f0e796b5a999daae8e467f9bee7b1a1ecf28e207d54605`.
The corrected source pack matched
`b10f6e1f633cff9a13ef0470af157fdd4d0b5616b560141c6e17819fda7c0357`.
Both final packs preserve current main's zh-TW and root metadata exactly.

The final audit checks the original independent peer report SHA, original
reviewed pack bytes and all 24 image bytes. Where Git normalized CRLF to LF,
converting back reproduces the exact reviewed hash; no other difference is
accepted. The final receipt binds actual LF pack and asset bytes plus normalized
GuideDocument hashes. Original source images and credits remain unchanged.

All five locales now have standalone local desktop/mobile previews at 1365×900
and 375×812: 20 cases with all 32/33 blocks and six/four sources, both 1600×900
images loaded, zero browser errors and no page overflow. The coordinating agent
inspected all desktop/mobile first-screen sheets. Prior independent full-size
diagram review still applies to the unchanged reviewed assets. These previews
are local HTML, not Next.js or public canonical/hreflang acceptance.

## Checks and outstanding acceptance

- Two-pack lint: zero errors; inherited no-summary and deliberately non-clickable
  related-reading warnings remain. Complete English bodies are 7,020 and 6,526
  characters, above the advisory 6,000 guideline; no details were removed.
- Content-pack/link tests: **15 passed, 11 database-dependent skips** locally.
- Strict intake: **one inherited failure per source**, because its first block is
  paragraph instead of summary. Internal targets, self-reference counts and SVG
  numeric checks pass. The separate source-summary task records this unresolved
  editorial item; it is not counted as a pass.
- All nine CI checks passed the old partial PR head `0272a883`; adding the reviewed
  image documents and refreshing main requires new CI. The PR remains draft.
- Current live image SEO source in the historical receipt predates #934. Reconcile
  the source through the Batch041 live-source task and a fresh read-only preflight.
- No deploy, import, publication or public browser verification occurred. The
  separate unclaimed release task requires the currently unavailable same-image
  Docker rehearsal, version/hash and visibility protection, backup/health checks,
  scoped dry-run/import and unchanged rerun, then five-language public acceptance.

Final review receipt SHA-256: `bdc30cbe2ee0e51d5cc08504028ae13df8f26633e1c2753cff9a091a073f441e`.

Final preview receipt SHA-256: `a2ff36636e3ba3ab92beec0d9e85c36ddaf1bb177fb2d7acc26bc6b2e0a2fd01`.

| Pack | Locale | Reviewed normalized document SHA-256 |
| --- | --- | --- |
| `on-page-seo-workflow` | `zh-TW` | `4916a8cc37818e40960e39a28243f2bc8c62f5f07457745ea70f59505a924479` |
| `on-page-seo-workflow` | `zh-CN` | `531dfef338314b32f95ec078da92c0f5ec2ee3fafa39ab1d036269dfcdc3af2e` |
| `on-page-seo-workflow` | `en` | `fdedd7db594797846c46614ec1c570a6c0aa81f3ef0ed3e114afc858e015e912` |
| `on-page-seo-workflow` | `ja` | `93af5cae9e98710541935b067c0379677f5719d6665323493ca61ad0a2857049` |
| `on-page-seo-workflow` | `ko` | `e29c3c2e5789283a02ae9bc5ae3547854d77da406a666786223c6f7658419162` |
| `image-seo-workflow` | `zh-TW` | `e359a3d9f84fb59983424ec12a82369839d88c5570b1845e0c3c5af5345e433d` |
| `image-seo-workflow` | `zh-CN` | `f7c90be51532375c3ff018c55773b66365513d8383891b10c6c3f7438dc29bd7` |
| `image-seo-workflow` | `en` | `9254857df9bb2dc059e2762dafa5558831315d0599df753e388c32f98c20ad6e` |
| `image-seo-workflow` | `ja` | `89af3e12f925071f0b291e503f81e34f26c7768023aa0bc5f4229ccdf92d957a` |
| `image-seo-workflow` | `ko` | `9ed7ce44b430a7077e1102de5d6cc57e6d612291089afe521cba793468b5102c` |

Final pack hashes:

- `on-page-seo-workflow`: `f3c0bb3813c790509c8109222aba048378a45c23458c80c1a9a53a0ac7cc2f1b`.
- `image-seo-workflow`: `9b07710a4b4918cec10f22f141c6b8f85de2a6d8e765fec15d31a4eecbe98193`.
