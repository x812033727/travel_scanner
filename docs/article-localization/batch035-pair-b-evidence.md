# Batch035 pair B: Kit and content calendar five-language draft

This PR adds the missing zh-CN, en, ja and ko documents for two published life articles. It is source-controlled content only. It does not deploy, import, publish, or establish browser/device QA on the public site.

## Pinned baseline

- Base `origin/main`: `e36db07bbb1a511046def7c42cd6978f3888cc52`.
- Read-only production inventory: 2026-09-28; both articles active/public, article v2, zh-TW published v4, four target locale rows absent.
- Inventory SHA-256: `f6046853b9a53f979986763ac0a98fb23e966affd8732ac8b183ec00438a37a9`.
- The root metadata and complete zh-TW locale are structurally identical to the base for both packs. Original hero JPGs, SVGs, credits and licensing are unchanged.
- All target documents retain 33 block positions, original table/list shapes, source URLs and checked dates, and image dimensions. The translated ArticleInline nodes preserve source slug/kind. The API resolves them only for same-locale published destinations; unresolved nodes render as plain text. Recheck publication state before import.

| Article | Original pack SHA-256 | Current pack SHA-256 |
| --- | --- | --- |
| `kit-newsletter-setup` | `8bfc7cf36262d67b36e35bcaa7a8378e835833ac7fd000ca98c32f8e10679677` | `4b391258eb0aa34b847b454644c3fabc0a45e3cfb60eda056473a521ca36f2c1` |
| `content-marketing-calendar` | `30beb6bb2b3819a560e037d8a28f14b6ae42d18094001ef5a3b2f5004a261a18` | `ad43a52412b9d2dd2d050f108829a60cdcef0b7d6f0a34d0c1a059416f4119f3` |

## Target documents

Canonical document hashes use UTF-8 JSON with sorted keys and compact separators.

| Article | Locale | Blocks | Sources | SHA-256 |
| --- | --- | ---: | ---: | --- |
| `kit-newsletter-setup` | `zh-CN` | 33 | 8 | `28eda3ec90f4fa5311b1d8d6cb76c672aec69cacf4b9ca31df84529ddf258478` |
| `kit-newsletter-setup` | `en` | 33 | 8 | `d38438d3017ffe05d07a450197e6bbc898019c36040cb23e877fb4d1bedf8cc2` |
| `kit-newsletter-setup` | `ja` | 33 | 8 | `f52d741298d3ead2e949fbe61f43b2ef7e99120f4445f9fd9e06675f1f33a7b4` |
| `kit-newsletter-setup` | `ko` | 33 | 8 | `f1ec74eb515dbeb1ebf2d28f2206321dedc2d6a1d0b5e5c5179f7aad606b35ac` |
| `content-marketing-calendar` | `zh-CN` | 33 | 4 | `a6b4a6844b7669c050a810962804b03b205daa092dc7507e599b0bf2e3b3aa52` |
| `content-marketing-calendar` | `en` | 33 | 4 | `58058974bae6d568a729fa629a90cd5201506d2dde48c1f54259503509537caa` |
| `content-marketing-calendar` | `ja` | 33 | 4 | `914d70d3bf9a3645011a5c829efd104d97556b7fd81c8013f5362c8a45728ece` |
| `content-marketing-calendar` | `ko` | 33 | 4 | `51f0dca9a5e16b139e5d718976100908ae7b5cc06e21405601f0ea9bc6a26a96` |

## Localized artwork

The editable hero and diagram SVGs were translated from the original Mokaair vectors. Eight hero JPGs were rendered from those SVGs at 1600×900. All 16 SVGs passed automated canvas/card bounds and text-overlap checks; their contact sheet and full-size Japanese/Korean diagrams were visually inspected for glyphs, spacing and labels. The original art attribution is preserved. This is not physical-device or live-page QA.

- Image render receipt SHA-256: `026e0821ea5e70a5da5539593fc821c67d3a82b7781e17aa6735fd92219bfda1`.
- Content/asset audit receipt SHA-256: `cdeecb2a9441b7c662ae9ec83689fa47e48f4f6aaa3ea1ead95f3be423529947`.
- Contact sheet SHA-256: `d73e3107f0156781e2dff51889614c5212aef77e30ef74f5a06cab9977617a04`.
- Independent editorial review of `content-marketing-calendar`: GO_EDITORIAL, receipt SHA-256 `bfbdd8d99cb77e93a00be89e42a0e8ed78b1a418ba8f851f5b6350aec9ccb241`; its two English diagram labels were corrected before the final render.
- Independent editorial review of `kit-newsletter-setup`: GO after correcting the diagram's auto-confirm wording, separate email Published/Sequence Active states and import-trigger caveat; final receipt SHA-256 `65ed1e0d52e7f80e9c01ca2aaa3836f55e01090c040cd0c4ee113b8375bbf95f`.

| Asset | SHA-256 |
| --- | --- |
| `apps/web/public/guides/kit-newsletter-setup/hero-zh-cn.svg` | `053274b4eca14e95e5d51183336f7839a460e65eebfc30000dfad276820ddc3f` |
| `apps/web/public/guides/kit-newsletter-setup/hero-zh-cn.jpg` | `4f5b598faa9850c222451be050aa83ecd7f934684f03ac13d05eb513ced6fb40` |
| `apps/web/public/guides/kit-newsletter-setup/diagram-1-zh-cn.svg` | `7d22f956146565a5eca5d2bcdaa8b6de7e35306a5cc2be29991d17147840125a` |
| `apps/web/public/guides/kit-newsletter-setup/hero-en.svg` | `c719c6cb08d04e706d5a4bf010e3a52a3f6be8de74da17932e1e1e624bad4aed` |
| `apps/web/public/guides/kit-newsletter-setup/hero-en.jpg` | `cb29477c08d15f060be07363892c6fe1d2e839381e36323d11aafe13ed622349` |
| `apps/web/public/guides/kit-newsletter-setup/diagram-1-en.svg` | `e94fb0f5cc3d8f5f87cf63fdb9e0f8175789c63bb7f24eb434537dce3d7d3dc5` |
| `apps/web/public/guides/kit-newsletter-setup/hero-ja.svg` | `2d901333b396b72ffe5c1007ca281ed924a9eb5d1aca94ddf217a459db3cf487` |
| `apps/web/public/guides/kit-newsletter-setup/hero-ja.jpg` | `dbb9f08f04b0eb79fa97a054561b1bec255327be9c1a64189adf8a23e7fe35ca` |
| `apps/web/public/guides/kit-newsletter-setup/diagram-1-ja.svg` | `d47b26b60f77e52c7fe606c3ca01c990b2d365d40175a552b5725ae5ec72c69d` |
| `apps/web/public/guides/kit-newsletter-setup/hero-ko.svg` | `67143450b349591b6ac552c45cf59dcd4a91d95a85c4c8eff088583ea892c5cf` |
| `apps/web/public/guides/kit-newsletter-setup/hero-ko.jpg` | `b995a731f94ff32d693371cb8d0fee61a262a3c545179f7722adba32e14d29d1` |
| `apps/web/public/guides/kit-newsletter-setup/diagram-1-ko.svg` | `7c87760b7b34f828d3dc625f2b32b0ff3499507321faab5a4cabb88d8c3b9960` |
| `apps/web/public/guides/content-marketing-calendar/hero-zh-cn.svg` | `ea57728fcd5c445e524461b91b5c50391c6d974cab5635dd1f49d259cbef5b25` |
| `apps/web/public/guides/content-marketing-calendar/hero-zh-cn.jpg` | `d2bc958b6217ab79af7b33a39e3f448fa30c0db372e4931b26d4d43db0697cab` |
| `apps/web/public/guides/content-marketing-calendar/diagram-1-zh-cn.svg` | `72dc31034a6e8eb2933e415715d8afd8ef3c11be9125ca8732333362d8675fa6` |
| `apps/web/public/guides/content-marketing-calendar/hero-en.svg` | `0f5635d7032c2ad4321e5f69365fbfa0f390122dc36b4c6dd5e2088bd2e9118e` |
| `apps/web/public/guides/content-marketing-calendar/hero-en.jpg` | `fd25a9af6b045037c433b708f03d049399964be10b1cbdfd8671bc1d814550e7` |
| `apps/web/public/guides/content-marketing-calendar/diagram-1-en.svg` | `bed037c6962f16c5d47fc0e3e0cd1ee3d6534e7d2d96f839ef122ba76d64f0b3` |
| `apps/web/public/guides/content-marketing-calendar/hero-ja.svg` | `39a6247752a0f08df87ac870a8499b977255022761797dd8b95c0cc451f9f7da` |
| `apps/web/public/guides/content-marketing-calendar/hero-ja.jpg` | `1978bbbfcc4d91498ce6e9c0525c5122cfb8b419ca6f2151f4290e55bee3d046` |
| `apps/web/public/guides/content-marketing-calendar/diagram-1-ja.svg` | `cbd63bd5f61b07902640cf9079169464a9a6b9674b9cd479ba83f480148803fb` |
| `apps/web/public/guides/content-marketing-calendar/hero-ko.svg` | `36439751d0f8103ef152def09c4370e2d7f66cac6cc4b93c230ed68ce85d3631` |
| `apps/web/public/guides/content-marketing-calendar/hero-ko.jpg` | `31977813cb1a310311107df2453bda40089090c6db2ef369273dab800510f741` |
| `apps/web/public/guides/content-marketing-calendar/diagram-1-ko.svg` | `f369a28a86b30b8c47b8c222d7e204e94b132ff6eb6169dcc20172b4275a4974` |

## Verification

- `uv run python -m app.guides.pack_cli lint --slug kit-newsletter-setup`: exit 0.
- `uv run python -m app.guides.pack_cli lint --slug content-marketing-calendar`: exit 0.
- `uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py -q`: 12 passed, 5 skipped.
- `npm run test --workspace @travel-scanner/web -- components/content-blocks.test.tsx`: 65 passed; unresolved ArticleInline renders a span, while a published same-locale target gets its article path.
- `npm run check:tasks`: exit 0; existing unrelated stale/overlapping-task warnings remain.
- Both packs: source locale and metadata unchanged; four targets each, 33 blocks each, three same-slug/kind ArticleInline references per target, 24 expected language assets present. Image dimensions and source asset SHA-256 values match the inventory.
- Pack lint emits existing-source/target `no_summary` warnings. Full English translations exceed the advisory life-body length; they were not shortened into summaries. Unpublished destinations remain non-clickable through the publication-aware resolver.
