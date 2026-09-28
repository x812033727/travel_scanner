# Batch037 Pair B: short video and influencer guide translations

This review-only branch adds complete zh-CN, English, Japanese, and Korean documents and localized hero/diagram artwork for `short-video-marketing` and `influencer-collaboration`. It does not change the published zh-TW documents or root article metadata. No import, publication, deployment, or production write is part of this PR.

## Source and scope

- Initial repository base: `5329ad8920300fec4fda06ded8bd006607a72d4f`; this branch was rebased onto `5b35df86` after unrelated Batch035 changes entered `origin/main`. The two source packs and six original images remain byte-identical to the pinned Batch037 inventory at `C:/Users/x8120/.codex/article-localization-release/batch037-social-content-readonly-inventory-20260928/candidate-inventory.json` (inventory SHA-256 `3bea364352f11e97fe1af688426c7f9c7c8e6c64b94a7dd6b8e55c1c60cac01c`).
- A fresh guarded, four-lock, repeatable-read **read-only** production capture completed at `2026-09-28T11:00:27.736024Z`: receipt at `C:/Users/x8120/.codex/article-localization-release/batch037-social-content-preflight-20260928/receipt-20260928T110024Z.json`, SHA-256 `575c4ec04629900421c106f6c58f81e3e6ce2ccd0a28f97b76515c59ad1ad669`; snapshot SHA-256 `63478e28b187cf3f7fc76ba7fbe92677086b1f496205d563fe095a72da7ee288`. Both articles were active/published, article v2 with published zh-TW v4, matching source draft and published hashes, and with no target-locale rows. The exporter and wrapper were SHA-pinned and the host state was unchanged before/after capture. This is a point-in-time receipt; any future import requires a new live preflight.

| Slug | Original pack SHA-256 | Published zh-TW normalized SHA-256 | Final pack SHA-256 |
| --- | --- | --- | --- |
| `short-video-marketing` | `7c6149b19b1d3d2f628831d0c5a43231d38b535d7c27ade8cc00ef87948f2578` | `d018c49cffb0452494b44e34f99f89dc1f29590a31bf7a25861ff68d7639a953` | `014810b153da93ae6de1cd5765d6a49b916bbad04f959368094d027a16f133c1` |
| `influencer-collaboration` | `32733b8cdbd96f4670b19f83790a800e4991679cdffa7af809409a4ab19ad666` | `15169e4ae9ae4ce8f95d45f0d7292aeb511f9703582cd6a0e628260be63390e8` | `9de7a68ab5e4b77bb57b6c79dcb758812b5c4908ea95bc0718455911c3cd5a85` |

## Editorial and structural review

All eight target documents have localized title, description, body, table, list, callout, image alt/caption/description, and source titles. Automated structural comparison confirms the 33-block order, heading levels, four sources and their exact URL/check dates, image credits, table dimensions, list lengths, and the three `ArticleInline` `(kind, slug)` targets per article. The source zh-TW document and article metadata equal the repository baseline. Inline links remain publication-aware: target text can display before a matching locale is published; this PR does not assert that those target locales already exist publicly.

The short-video example stays an illustrative ~30-second plan, not a platform optimum or limit. The 9:16 framing, music rights, and March 31, 2025 YouTube Shorts view-count change retain their qualifications. The influencer example makes no claims of real creator contact, verified quotations, or measured conversion. The legal copy attributes the advertising principles to **Taiwan's** Fair Trade Commission in each target locale and keeps deliverables separate from outcomes. The current official pages checked for those claims were [Taiwan FTC online advertising principles](https://law.ftc.gov.tw/law/LawContent.aspx?id=GL000222), [Taiwan FTC endorsement guidance](https://www.ftc.gov.tw/internet/main/doc/docDetail.aspx?docid=13021&mid=1789&uid=165), [YouTube Shorts creation guidance](https://blog.youtube/creator-and-artist-stories/your-guide-to-getting-started-with-youtube-shorts/), and [YouTube Shorts views guidance](https://support.google.com/youtube/answer/10059070?hl=en). Meta/Instagram source URLs and checked dates are preserved; direct retrieval redirected to login during this review.

Pair A independently reviewed the English copy and diagrams, including FTC jurisdiction, example-only caveats, target slugs, and artwork. A detected English diagram label collision was corrected and rechecked. A second independent review inspected all 16 final localized hero/diagram browser previews without finding clipping, overlap, or missing glyphs.

## Validation

- `uv run python -m app.guides.pack_cli lint --kind life --slug short-video-marketing --slug influencer-collaboration`: **pass**, two entries; warnings only. The `no_summary` warning also applies to the unchanged zh-TW originals; the English body lengths exceed the generic life-guide character guideline while preserving the full source content and 33-block structure.
- `uv run pytest tests/test_guides_content_pack.py tests/test_guides_content_links.py tests/test_guides_pack_ingest.py`: **67 passed, 5 skipped**.
- `npm run typecheck:web`: **pass**.
- Targeted GuideArticle / article-page / GuideImage Vitest suites: **57 passed across two runs**. The first run passed the article-page and GuideImage suites (17 tests) but timed out starting the third Windows worker; a serial retry also hit worker-start timeouts. Running `article.test.tsx` alone with `--pool=threads --maxWorkers=1 --no-file-parallelism` passed all 40 tests. No test assertion failed. PR CI will run the combined web check again.
- `npm run check:tasks`: **pass**, 1,033 task files after the final rebase; existing queue overlap/stale-claim warnings are unrelated to these files.
- `git diff --check`: **pass**.
- Final content and asset audit at `C:/Users/x8120/.codex/article-localization-release/batch037-social-content-preflight-20260928/pair-b-final-content-asset-audit.json`, SHA-256 `f24cf5020929bcf08f75f6f69bf9aa443429f6361bb7223f8f28ba8f4bfea0c7`: 26 changed content/asset files, zero issues; original artwork hashes match inventory and all localized JPGs are 1600 × 900.
- Final SVG browser layout report at `C:/Users/x8120/.codex/article-localization-release/batch037-social-content-preflight-20260928/final-preview-pair-b/layout-report.json`, SHA-256 `5f9a384eb9ce5eddb8a97a95ebdaffe3deb899ed8b7cbc1474338e3bde82122c`: 16 hero/diagram cases, zero canvas/card-margin or text-overlap issues.
- Final article-content browser layout report at `C:/Users/x8120/.codex/article-localization-release/batch037-social-content-preflight-20260928/final-page-preview-pair-b/layout-report.json`, SHA-256 `5beb02723a2e83ca6620a79787dfe71cd46f20174659d6b3b5be6098456fccec`: 16 desktop/mobile renders across all eight target documents, zero horizontal overflow, all images loaded with alt text, and expected headings/table rows. These are standalone renders of the exact pack content/assets, because unpublished locales cannot be browsed on the live Next.js route; they are not live-site acceptance.

## Localized asset SHA-256

The original `hero.svg`, `hero.jpg`, and `diagram-1.svg` for each slug are unchanged. The 24 new locale assets are sealed here; the audit JSON above also records the two final pack hashes.

| Slug | Locale | Asset | SHA-256 |
| --- | --- | --- | --- |
| `short-video-marketing` | `zh-CN` | `hero-zh-cn.svg` | `83bebcfc70ba665f07a613ac14461981fefa361f0ff4977a2c06908dce7af4f5` |
| `short-video-marketing` | `zh-CN` | `hero-zh-cn.jpg` | `06120d6da7aef4b55880790b3ebcb534e66ed34a421c72f449e25541ce768ca0` |
| `short-video-marketing` | `zh-CN` | `diagram-1-zh-cn.svg` | `9bccf0ca25a811815fe76e022a2cf007d577fc478162705f7c560716cdd18be3` |
| `short-video-marketing` | `en` | `hero-en.svg` | `2e58e7832080f453574c49c08c9da0570c94b250d88180820281da9d008442db` |
| `short-video-marketing` | `en` | `hero-en.jpg` | `2014aea5fdc3cd96cf9aef99f8cb7fb4aa261d3bf0aa0871df54acead7bef4eb` |
| `short-video-marketing` | `en` | `diagram-1-en.svg` | `23ae4ddeb329b52f55735b383b8809694c62160890e88655e0ee817cd8e20ccf` |
| `short-video-marketing` | `ja` | `hero-ja.svg` | `c8f48f47b4d211cce23b5c705af6a394d97b7653cc0113ff858579a6bf4fb10a` |
| `short-video-marketing` | `ja` | `hero-ja.jpg` | `1e57caf43e6c106ebef53b418198c89c67a2d9c89c486d868e9ac9d25f8e6a15` |
| `short-video-marketing` | `ja` | `diagram-1-ja.svg` | `58ce5ff4ce157ac4d71760cfb7a117107f38d450de363a1c4cf238825518becf` |
| `short-video-marketing` | `ko` | `hero-ko.svg` | `b98c37701cbe6391945f35cc74e1f55670bc0dbf7c8519883bd915089664466a` |
| `short-video-marketing` | `ko` | `hero-ko.jpg` | `317399370651bc2635a2a661080c2102858f654e796cdf1536fc3b91eb77cb20` |
| `short-video-marketing` | `ko` | `diagram-1-ko.svg` | `9652f692bb09d64806f053e21c9a5a6f24a783e3d2bb1c2739f81bf88ccda422` |
| `influencer-collaboration` | `zh-CN` | `hero-zh-cn.svg` | `166138b0528e9bb33f0fc0ead334a9f2b0aae5afb5103c002cbf2eebf5ba66e9` |
| `influencer-collaboration` | `zh-CN` | `hero-zh-cn.jpg` | `c9cd16e4c6f012588af36455c0c5dda45b37343ed2181d7d7937fb1ed82a4140` |
| `influencer-collaboration` | `zh-CN` | `diagram-1-zh-cn.svg` | `bd58db116ec8951561df52c1a61f325bdfbdc688d5d791c3039d9664010daac1` |
| `influencer-collaboration` | `en` | `hero-en.svg` | `6f2caf6b8c3b715de1609b8ac6e42c4ecc293108dcf8b99e43827957d405ae8f` |
| `influencer-collaboration` | `en` | `hero-en.jpg` | `093de667476cf6af04adfbc019fbd00952b7525fcc007e7f2ec787a5bd58f1c1` |
| `influencer-collaboration` | `en` | `diagram-1-en.svg` | `d77033cd90ffee5c78e8031fc2fbdccf546b767aeea138df02bcd5f5f8dca880` |
| `influencer-collaboration` | `ja` | `hero-ja.svg` | `6c7d8ae6443b046d524cc7c6acaf799075433da1a54eda2199956097fbc90ff3` |
| `influencer-collaboration` | `ja` | `hero-ja.jpg` | `5eaf215a0d29fbf1daf103273337f0e91ab438cfe616b5bde576fd4fae3b2e90` |
| `influencer-collaboration` | `ja` | `diagram-1-ja.svg` | `1c7aaf0dbb49d4e89cbe4c820778b8d71763550cf9598775c5724f29c3f4e29d` |
| `influencer-collaboration` | `ko` | `hero-ko.svg` | `9c68ee31ff53a750dfa1471bbfacb68e88763fa057f00989f40de2ab591aa224` |
| `influencer-collaboration` | `ko` | `hero-ko.jpg` | `89b801f498016913953fbfad375314cfebf937d9d27c44e67687bb8cdfb6c8f4` |
| `influencer-collaboration` | `ko` | `diagram-1-ko.svg` | `ad98cecafa77d86ce46b57164e1c6501b44bf0fb8485cf02e331b1dd160e2bb7` |
