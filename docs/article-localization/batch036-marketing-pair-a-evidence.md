# Batch036 marketing Pair A: five-language repository drafts

This change adds complete zh-CN, en, ja and ko documents for the already published `marketing-plan-small-business` and `paid-vs-organic-marketing` guides, plus language-specific original Mokaair hero and diagram assets. It does not import, publish or deploy target locales.

## Pinned source and document hashes

- `origin/main` at read-only inventory: `045afc1eb9ebf371cc54ef9b2dd10be82e7a7b01`.
- Inventory SHA-256: `f2919a2e4f3c9df9d656c8a9561131cbfa463886939233a23ad07e5f6519095f`.
- Both articles were public at article v2 / zh-TW published v4; four target locale rows per article were absent. Repository source matched the published zh-TW revision. Recheck versions and public state immediately before any import.
- Root metadata, full zh-TW documents and all original images remain unchanged.

| Article | Original pack SHA-256 | Current pack SHA-256 |
| --- | --- | --- |
| `marketing-plan-small-business` | `58f35e70c8fe86987f1dd8bd13980a958fc2793d093f88f90e70efa46683b1dd` | `c1fc45fc749a353e34cbea08f4cb4f7192fffbc9037a0ead1db90e7fa41cced2` |
| `paid-vs-organic-marketing` | `e3f9ce511bbbb568dea0de326b81c011d58c2271b3287e0576f383424e8582cc` | `d61970809da32cd7a59d83c154c715bed5a291f841da40dbd4b8140141dbbe7d` |

| Article | Locale | Blocks | Sources | Canonical document SHA-256 |
| --- | --- | ---: | ---: | --- |
| `marketing-plan-small-business` | `zh-CN` | 33 | 2 | `74ce5e33aa9164caba873fd335baf47970804baeea2581b93e3a7c193d19050f` |
| `marketing-plan-small-business` | `en` | 33 | 2 | `e6f10b78b5df8511017644ca98b8dd6c535ee8e96438d5d9c34d598c45e8013d` |
| `marketing-plan-small-business` | `ja` | 33 | 2 | `02f13f1894c6f70188ebfa1ab2264ba343c3ba4366a3d3a6b3fdeb4b4134c12c` |
| `marketing-plan-small-business` | `ko` | 33 | 2 | `967a336edb92f805b7d1df55636d0783056961e899a1ee00a1be055fc09a3efa` |
| `paid-vs-organic-marketing` | `zh-CN` | 33 | 3 | `7a1138e96ebee2e8fdd8d26a63c750eb7bdc47f0435ede6941419b5c56749a86` |
| `paid-vs-organic-marketing` | `en` | 33 | 3 | `6821b2686c8ad07f58bb6004d5218ef7c9494eb4d0c542ce8531908a2f3ee3b2` |
| `paid-vs-organic-marketing` | `ja` | 33 | 3 | `c9735d4b6fe5c8ebbb772a4f46c8e932d562ab7e4b31317721412e1f933c14aa` |
| `paid-vs-organic-marketing` | `ko` | 33 | 3 | `97330a233a9e278c46a211f52c30622fbe8affc150d7b151666ddc2c7957403a` |

## Localized image evidence

- Browser-rendered SVG receipt SHA-256: `bb114ec4027cce5c2d89638823d179a0718c5bf2be5c2634ddbf685b3fce3883` (16 SVGs, no canvas/card overflow or text overlap; eight 1600×900 JPG heroes).
- Content and asset audit SHA-256: `bf08fa65420a3b186db2ac163ce236c11ceffd05e01c26fd8859361dfa7c7e3e` (two articles, eight documents, 24 assets).
- All 16 hero and diagram previews were visually inspected for layout and missing glyphs. Source image credit, sizes, original assets and published zh-TW images remain intact.

| Asset | SHA-256 |
| --- | --- |
| `apps/web/public/guides/marketing-plan-small-business/hero-zh-cn.svg` | `c344e3c41e8faece873cf203c9dd771efd400a665b9bf0bb88fd47ab267bf16d` |
| `apps/web/public/guides/marketing-plan-small-business/hero-zh-cn.jpg` | `bfb7dbe830c4671a09d3dcdc04b83d1260e395b430e9198946033eb23a8a68f0` |
| `apps/web/public/guides/marketing-plan-small-business/diagram-1-zh-cn.svg` | `ac7f4db794e185af97998a21502f9a8286e3bdacb24ab83a137e684208338af4` |
| `apps/web/public/guides/marketing-plan-small-business/hero-en.svg` | `b503e0bf4c7bdd592b694b5cf3a187fec4fb607e9729e61b035da441535fc025` |
| `apps/web/public/guides/marketing-plan-small-business/hero-en.jpg` | `de3c7309f64c207f1773c56919f54385d64b05b5bb0cdf8bc99a3f148ca0a685` |
| `apps/web/public/guides/marketing-plan-small-business/diagram-1-en.svg` | `81be211a518347d3a943e6b560f81d2c916cfb8c673f34773e7869c578bab93b` |
| `apps/web/public/guides/marketing-plan-small-business/hero-ja.svg` | `82c5c5702476897fc1ddcbec40831dfce16d901a058931fa5e9a12bb4ab74384` |
| `apps/web/public/guides/marketing-plan-small-business/hero-ja.jpg` | `9879d5c8254f87f96038ce109dcf8189636fc0bbebb7f70a755ee0ca3e8059b2` |
| `apps/web/public/guides/marketing-plan-small-business/diagram-1-ja.svg` | `0cc50e92b10b207b1d6571f1bb20e3f9e10455fe771770f6092321dcf8541c6c` |
| `apps/web/public/guides/marketing-plan-small-business/hero-ko.svg` | `15b080a2c92eecabf67fb3850e785d757c6c58448267d2bcba0579b23ce35e63` |
| `apps/web/public/guides/marketing-plan-small-business/hero-ko.jpg` | `831f818af0e717d9b3e3fd40536a8d83a2c8b21a007a2ca9af980c0e2a5df614` |
| `apps/web/public/guides/marketing-plan-small-business/diagram-1-ko.svg` | `8a8a5e508131432f4ce876d8d34860d5258e2136cfa7262ed9c3407d60a2cb9b` |
| `apps/web/public/guides/paid-vs-organic-marketing/hero-zh-cn.svg` | `b0e9e0bff7949190b003887379e605ce60e7c1f80e36c2aa1e0515df5c3d9e0a` |
| `apps/web/public/guides/paid-vs-organic-marketing/hero-zh-cn.jpg` | `5ac585ec2912f63c9d2576a2571a77c6104883f4ded01bd5e6c29b7d3cd1f41f` |
| `apps/web/public/guides/paid-vs-organic-marketing/diagram-1-zh-cn.svg` | `e32ea5312b201410004ca1c6c462ddcd1d4d9d52f85d90cc26079b13642c8b5d` |
| `apps/web/public/guides/paid-vs-organic-marketing/hero-en.svg` | `f359725baf1e99f809bd4582938aa87aad4371dce718fae429d227bafbcea588` |
| `apps/web/public/guides/paid-vs-organic-marketing/hero-en.jpg` | `17f6283ed1e739533e90d26514f0c5abd2fbd89ac01727be11b1b3bcf3c2c3a3` |
| `apps/web/public/guides/paid-vs-organic-marketing/diagram-1-en.svg` | `1b572a3d802c0cd6eed17da6378e39295c76baecfe08587950f29ca0f3a3a0bc` |
| `apps/web/public/guides/paid-vs-organic-marketing/hero-ja.svg` | `a2e322e2de079c979e341d16da8552d8fe8b920e10333ba713226e3998b77819` |
| `apps/web/public/guides/paid-vs-organic-marketing/hero-ja.jpg` | `1f094b48562e21acd2c4e5b5e3e7beac2c7f120305103b70514e66aaabce640d` |
| `apps/web/public/guides/paid-vs-organic-marketing/diagram-1-ja.svg` | `d5c2ea5c062f2e1cbffc260237f38e482dc59a63a560537bd21e0a050831ee6e` |
| `apps/web/public/guides/paid-vs-organic-marketing/hero-ko.svg` | `5e8385a82b987c69b30d6ce635d55393cf485e8913bfee6ca97d235bfb466973` |
| `apps/web/public/guides/paid-vs-organic-marketing/hero-ko.jpg` | `dd28fee2b4978a8fdf3ba6498bb66823d918686d037a3b6269276d9fadae2c4b` |
| `apps/web/public/guides/paid-vs-organic-marketing/diagram-1-ko.svg` | `f05cca16b98a25d2af02ec06b0e7edbb51544d68491259156aab3c549cb65910` |

## Verification and release state

- Both scoped pack lints passed. Source `no_summary` and advisory long-English-body warnings remain; translations are full documents rather than summaries.
- Structure and all 33 block positions, list/table shapes, source URLs and checked dates, image credits/dimensions, and all three source ArticleInline kind/slug targets were preserved per locale. The resolver activates same-locale links only after their destinations are published.
- API content-pack/link tests: 12 passed, 5 skipped. Web content-block tests: 65 passed. `npm run check:tasks` and `git diff --check` passed.
- Independent read-only editorial review marked both articles GO for meaning, figures, applicability, source dates, images, and publication-aware navigation. The zh-CN `照著` typo found in review was corrected; the source/pack hashes above reflect that correction.
- Related-reading targets without a published same-locale document remain plain text as intended. A source-title mismatch for Google's "Do you need an SEO?" page and a Google Ads `hl=zh-Hant` URL inherited from zh-TW are recorded in the task for source-metadata follow-up; the linked pages support the claims.
- PR CI is pending. Guarded import, public publication and desktop/mobile live-page verification remain separate work.

## Current marketing-plan review, 2026-10-07

This follow-up reviews only `marketing-plan-small-business`. The retained
production capture from 2026-10-07T04:45:46.904711+00:00 has published zh-TW
v4 and no en/ja/ko/zh-CN rows. Its normalized source hash is
`1f556287a76e6352278f7a53601c6cb425201f2db1be6fe75d7f4f72943f6403`;
the source document and root metadata remain unchanged.

Independent reviewer `codex-current-independent-next-review` read the complete
source and four target documents, checked the current Australian government
and SBA supporting pages, and inspected eight fresh SVG renders plus four
actual hero JPGs. Root, as a distinct application party, applied eight terminal
related-reading labels equal to their published same-locale target titles and
one zh-CN hero-alt correction. The reviewer then independently confirmed all
nine exact leaves, normalized final documents, unchanged source/metadata and
all fifteen existing assets. No other content changed. Unpublished target
articles continue to resolve as plain text until their own locales are public.

Corrected pack SHA-256:
`06faef98b9310009ee7a32904f60474fd6da373c5a9305879334d9b9c2753582`.

| Locale | Final normalized document SHA-256 |
| --- | --- |
| en | `64e4957bfc6757936bbc086eb1bd6335bc5e29287fb0df3f7c898ccf3612c72d` |
| ja | `64a741891751d4e1e12a46e7e35b47c145bd693cbacfda5fb3fd8fb885c80ee7` |
| ko | `755f1f5319c72ff5dd904e169cf0a46568e08fc6c1a29ab75e2062d38d2778c2` |
| zh-CN | `efb180d5378fd8b65c5e20c859e57953b5e073b63d7385d85704e8c9ac637bc9` |

Current combined two-article external review bindings:
`findings.json` SHA-256
`e7f567907ebb7a4665a09d999fc5db2a54fca08617199cf9eeb61101ccd4da46`;
distinct-party application receipt SHA-256
`69968fd34f78247fd18a30fd4fbd432fed0b9c56e742fbf8e1bca052358f559d`;
`final-review-evidence.json` SHA-256
`28b83c1c26db0c0a2ee57795fbccc6e09a19262e7bdc9665c698c0b905d79c49`;
current `route-b-review-v1` receipt SHA-256
`6215361cac8abb391690d973feee8dc1b775400ab4477f8384b83fbd61e0bf72`.
The receipt has four PASS rows for this article and four for
`wordpress-security-basics`, with exact source, document and image hashes.

This content review does not claim a merged or deployed candidate, import or
publication. A candidate must separately freeze the exact committed Git blobs
before bundle preparation. The `paid-vs-organic-marketing` pack and all fifteen
assets are unchanged and remain held for the original source follow-up. Its
pack SHA-256 is
`d61970809da32cd7a59d83c154c715bed5a291f841da40dbd4b8140141dbbe7d`.
Optional zh-CN vocabulary and nonvisible SVG metadata changes are deferred to
the existing vocabulary follow-up and were not applied here.

## Final same-cohort review, 2026-10-07

The prospective first release cohort also contains `wordpress-business-site`.
Root's distinct executor `codex-root-distinct-cohort-label-executor` applied the
four reviewed marketing-plan terminal labels to that article's actual final
same-locale titles. Independent exact-leaf reconstruction accepts only those
four additional changes. The source, complete root metadata, all fifteen assets,
and the held `paid-vs-organic-marketing` content remain unchanged.

Latest marketing-plan pack SHA-256:
`c871fb1cbac44c7886755a64c501a4667d01493aa51aedc42e04ba03fa1152ed`.

| Article | Locale | Current normalized document SHA-256 |
| --- | --- | --- |
| marketing-plan-small-business | en | `0ce3cf1684645e633a37c8f584d1f274b37483acb090e08d86542759def2b4be` |
| marketing-plan-small-business | ja | `d6fb4a6e5384e8843ea2c68d7c726bfd5543763ff2b79f734f4985d51e0b60e3` |
| marketing-plan-small-business | ko | `831492c567dc143e53eceaf38f0d5d376e3a17adcf17eff9c1f77f4c6f6fa3cd` |
| marketing-plan-small-business | zh-CN | `5b7e3c88395a251da346482be707ca872e2cd1550eec12b8366674ebbf4a0358` |

Final cohort review at 2026-10-07T05:57:52.724199+00:00 by
`codex-current-independent-life-cohort-review:/root/localization_existing_work` binds the current documents and images to new review rows.
All 84 terminal ArticleInline links across the eight life articles were checked:
48 labels match currently published same-locale titles, 12 labels match the
actual final same-cohort target titles, and 24 retain plain-text behavior until
their target locale is published. The reviewer verified all 120 existing assets,
unchanged published source documents and complete root metadata. All eight
current scoped pack lints exited 0, with inherited source no-summary warnings
and advisory English length guidance only.

Current combined 32-row `route-b-review-v1` SHA-256:
`87986003cd9e266df5e569270ab3d2859f1573433d5c0f1d967c331e1969beaa`;
common final-review evidence SHA-256:
`d6e10b7546c48b0cdd76c0c03517c6d8ba0a2c0a84a99462ada3e6ed74e91527`;
this pair's current eight-row receipt SHA-256:
`04da1adaa0c6353acca365a27c456fe701f7a782afa6df9856219e5aaed3d851`.
The immutable current external receipt directory is
`reuse-t1/life-cohort-final-review-v2` in the retained 2026-10-07 release evidence.
Older receipts keep their original hash bindings and do not approve changed bytes.
The common review is for corrected workspace content; freezing exact committed
Git blobs, compilation, merge, deployment, import and publication remain
separate steps. No production write or model call was performed by this review.
