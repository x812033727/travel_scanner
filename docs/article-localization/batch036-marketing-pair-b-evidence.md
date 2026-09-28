# Batch036 marketing pair B: five-language draft

This change adds complete zh-CN, en, ja and ko documents for the already published `marketing-mix-models` and `brand-tone-vibe-marketing` life articles. It adds translated original Mokaair hero SVG/JPG and diagram SVG assets. It does not deploy, import or publish the new locales.

## Pinned baseline

- `origin/main` at inventory: `045afc1eb9ebf371cc54ef9b2dd10be82e7a7b01`.
- Read-only production and repository inventory SHA-256: `f2919a2e4f3c9df9d656c8a9561131cbfa463886939233a23ad07e5f6519095f`.
- Both articles were active/public, article v2 and zh-TW published v4; four target locale rows were absent at inventory. The repository zh-TW documents matched their published versions.
- Root metadata, full zh-TW source documents and original images are unchanged. Recheck source versions and public state before any import.

| Article | Original pack SHA-256 | Current pack SHA-256 |
| --- | --- | --- |
| `marketing-mix-models` | `76b10f97610c8f3e0ab402f99433a84a6188f9f7ec774bd50e8b88956eac4bc2` | `ff388b4168225355e69442ebeef528f1766669e40dd876dbb3aeffbe62e5168c` |
| `brand-tone-vibe-marketing` | `cd87a728e7c9760f73d7b6194bccf642e882e2733f7a1ce0fae06a0915a7116e` | `cadb408037f758da06a58aff957bba6cced2fe4014b5198640da28c1dd0883ff` |

## Target documents

Canonical hashes use UTF-8 JSON with sorted keys and compact separators.

| Article | Locale | Blocks | Sources | Canonical SHA-256 |
| --- | --- | ---: | ---: | --- |
| `marketing-mix-models` | `zh-CN` | 33 | 3 | `a0e9373fb740505fbd76c0d059b7b66aa0b37e88a602cb0e4123cbfc01376882` |
| `marketing-mix-models` | `en` | 33 | 3 | `0f9dfa32721aeff49138e17a821268f59077d771de4bca5e044e9cc0188b118c` |
| `marketing-mix-models` | `ja` | 33 | 3 | `672bab272525f84538631d7223de0d0342eba38a4add3a87b0ce9c3d1600c29c` |
| `marketing-mix-models` | `ko` | 33 | 3 | `69a1e8362409620cc165fc02d679804f2c7a04ef2d944891a5894e01d8189ae7` |
| `brand-tone-vibe-marketing` | `zh-CN` | 33 | 3 | `acd4b20a4bb091945bee89b58818a42fc2ce1568dff214ae1d5aa5dfbb4dd9cf` |
| `brand-tone-vibe-marketing` | `en` | 33 | 3 | `3f77bb0156961bcc8cde22dc9f5aa471b4ae2736f9f232365a42b622ef01ec42` |
| `brand-tone-vibe-marketing` | `ja` | 33 | 3 | `c66af982dbac77b0e9b8e1b42ea97a8982a92ae79b83a0cf037a5d5ae0a10b2c` |
| `brand-tone-vibe-marketing` | `ko` | 33 | 3 | `f0e0e985373cedfc3a34b3703f95fb99b2d065cf0eca9713d52720ed772424fe` |

## Localized images

Eight editable hero SVGs, eight 1600×900 raster hero JPGs and eight translated diagram SVGs were checked for canvas bounds, card overflow and text overlap. The original Mokaair credit, source image dimensions and all source assets remain intact.

- Render receipt SHA-256: `d95900d425380d479e850b0878e3973e2894567451cb00b54aea315e9a2168ee` (16 SVGs pass, eight raster JPGs).
- Content/asset audit SHA-256: `58d31990d54e930287146ef01e9c48a6a3cb9e231f9427fe821e37285b30c89c` (two articles, eight documents, 24 assets).

| Asset | SHA-256 |
| --- | --- |
| `apps/web/public/guides/marketing-mix-models/hero-zh-cn.svg` | `d359a49dcbf090c627a3be92fdfdd4ac61e54c1db74bbf6256713f31b7af34aa` |
| `apps/web/public/guides/marketing-mix-models/hero-zh-cn.jpg` | `6e0bb0a40350f710042dd6ade1aa0010f126a48c6e7df55b29323f0e5f9907ea` |
| `apps/web/public/guides/marketing-mix-models/diagram-1-zh-cn.svg` | `54642ea9e86d10300fd3d0a9279d2e3b9de0347ec4a22ea7ea468e627453045e` |
| `apps/web/public/guides/marketing-mix-models/hero-en.svg` | `b3d97b38ffdd00b45f52627f945733655d6f6455e71b833f27c4b7c695f646f8` |
| `apps/web/public/guides/marketing-mix-models/hero-en.jpg` | `c34c17c6aa266ec6d3bbe9a06f6c5ff5a8e0169b1a084d7ab5ae9d0d5a89e6b6` |
| `apps/web/public/guides/marketing-mix-models/diagram-1-en.svg` | `e1a10fee6437ccafa0037d106544af8cc95d37a8e6c17926943c1b70f152fcbe` |
| `apps/web/public/guides/marketing-mix-models/hero-ja.svg` | `f8221d5f85634def1d7719117d36ec7a18c928b27f655424929c5d6214e80f94` |
| `apps/web/public/guides/marketing-mix-models/hero-ja.jpg` | `3213249d4a1a0003bf0f65942d7313d814b3c6ff15f809f5e232b5563adc8a81` |
| `apps/web/public/guides/marketing-mix-models/diagram-1-ja.svg` | `d5ac0ecfdd7388a547ca043af7392fbf008ebc6226deb0a2e6f166718a4cec6e` |
| `apps/web/public/guides/marketing-mix-models/hero-ko.svg` | `fd584108408c3859322ea1f1c4d981e38a8c7fe96ba08309669fca9c8d43b0f5` |
| `apps/web/public/guides/marketing-mix-models/hero-ko.jpg` | `e198e3b2478d1d80ef702c68fd37eed568bafb90eb25af55e06639b6e42b217d` |
| `apps/web/public/guides/marketing-mix-models/diagram-1-ko.svg` | `d8fc648220d42f2f411955a736253272e03f5ee8773ba3efc303b48ce2145980` |
| `apps/web/public/guides/brand-tone-vibe-marketing/hero-zh-cn.svg` | `8cd4d6a5e574f76a53d80a09384348ac36eb8537b116dc06d3a7905dcb0b151a` |
| `apps/web/public/guides/brand-tone-vibe-marketing/hero-zh-cn.jpg` | `69f209c2eb5e81aabb4f616dff6475f09bab3d0dc9412cdb522c85e248ba1660` |
| `apps/web/public/guides/brand-tone-vibe-marketing/diagram-1-zh-cn.svg` | `50eb593790fb1ff69e3763f8e7a42d0210bd9db600c21a0ee2557abc2ef1c909` |
| `apps/web/public/guides/brand-tone-vibe-marketing/hero-en.svg` | `c4f3224036f2ab00e2a2b8397497cc39700b8970d35488c45efb2115a5bdf363` |
| `apps/web/public/guides/brand-tone-vibe-marketing/hero-en.jpg` | `5687ba2c49be5931ce98ba2b6380f916dc102da20b97578704b3f71e0a694a70` |
| `apps/web/public/guides/brand-tone-vibe-marketing/diagram-1-en.svg` | `97dab8725ff1509904b74c000e5c8c761fa1c4c02ff8ad54bd56208d078f576f` |
| `apps/web/public/guides/brand-tone-vibe-marketing/hero-ja.svg` | `d17d8328c53e39b649d330e1115334286ed4ceff439fde527c04703abe175e94` |
| `apps/web/public/guides/brand-tone-vibe-marketing/hero-ja.jpg` | `3b42320a642e324134b7abd31780d5f23594d235466e78e064f7350ec6f8dc0f` |
| `apps/web/public/guides/brand-tone-vibe-marketing/diagram-1-ja.svg` | `374e432b0730268158bd89e9d9bb6dde3ed108fb4b75a36bb07a48619711dcf5` |
| `apps/web/public/guides/brand-tone-vibe-marketing/hero-ko.svg` | `30bc76d6e4093ee4e2a8778830b8cf0451561584e6d6cadb584b03875e538c49` |
| `apps/web/public/guides/brand-tone-vibe-marketing/hero-ko.jpg` | `e69fdbc3333b805ed77f3a553a743f5bbd2bacbba4008580bd3000cf85c9bc6f` |
| `apps/web/public/guides/brand-tone-vibe-marketing/diagram-1-ko.svg` | `abdd99667d2a279c9897a7a8aa0837f6d8492bbfa18613d623d49ec331bd3cd2` |

## Verification

- Both scoped pack lints passed. Existing source `no_summary` and advisory English body-length warnings remain; the full translations were not reduced to summaries.
- Exact block types, 33 positions, list/table shapes, source URLs and checked dates, image credit/dimensions, and all three source ArticleInline slug/kind targets were preserved in each locale. The publication-aware resolver renders unpublished destinations as plain text and activates a same-locale path only when its target is published.
- No placeholder text or wholesale copied source blocks were detected. Digit differences were checked: English spells out September and one repeated 4C reference; the brand contrast value written in Chinese words appears as `4.5:1` in en/ja/ko.
- API content-pack/link tests: 12 passed, 5 skipped. Web content-block tests: 65 passed. `npm run check:tasks` and `git diff --check` passed; task checker warns about unrelated stale/overlapping tasks.
- Original and translated diagram sheets, all SVG measurements and hero previews were reviewed locally. Public-site desktop/mobile browser verification remains pending after publication.
- Independent read-only editorial review marked both articles GO for translation fidelity, figures, source dates, images and navigation safety. Related-reading targets without published same-locale revisions render as plain text until those destinations are released. PR CI and guarded publication remain pending.
