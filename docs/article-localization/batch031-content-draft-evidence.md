# Batch031 target-language content draft evidence

This is source-controlled content only. No database import, locale publication, deployment, or production write occurred. The fourth article (`wordpress-user-roles`) remains outside this task while its zh-TW source-correction scope is active.

Base commit after source PR #875: `4b6c5cd99fa9eab3b658d5b6cf639cb001f8fc3e`.

## Exact source and target checks

| Article | Pair commit | Pack blob SHA-256 | Source retained | Target locales |
|---|---|---|---|---|
| `wordpress-member-registration` | `b885927df5ee0bc6a13b1a1e93b9457eaa3dba3f` | `078a4200bb3f49e14ace039d02c2b31655e0638e301007935dda62967c13ad15` | byte-equivalent model to base | en, ja, ko, zh-CN |
| `wordpress-security-basics` | `b885927df5ee0bc6a13b1a1e93b9457eaa3dba3f` | `cdf7a2d7e585878448f1fdd9e1a902187d665d88972676ffbbfb49d208f62f28` | byte-equivalent model to base | en, ja, ko, zh-CN |
| `wordpress-social-login` | `e8fa87d9abb0969a5c9861e5b0b551757cd47ba6` | `fbc172c9f6e8e73ee01d42492c9c5739253fb527dcbdfa51563b5bb696e82656` | byte-equivalent model to base | en, ja, ko, zh-CN |

The three root metadata objects and three zh-TW documents match the post-#875 base exactly. The twelve target documents match their Pair commit models exactly. The fourth pack, `wordpress-user-roles`, is absent from this diff.

| Article | Locale | Canonical document SHA-256 |
|---|---|---|
| `wordpress-member-registration` | `en` | `3d40d77244ba6de0bda599edb93db5e7f352114bd466941f7dd70ff175ee40a5` |
| `wordpress-member-registration` | `ja` | `112b46631f28e1260a687c024ccdb99283ac5d9b8ec705445e1081a6efe7c909` |
| `wordpress-member-registration` | `ko` | `a64967b9b4e5ffdf776287bf0a69d0699f13a13c54cdd93da5a8537c7c27efd2` |
| `wordpress-member-registration` | `zh-CN` | `4022d23d303a26e37a9a9f8634b92961e8026566d57acad786baa0bffd413854` |
| `wordpress-security-basics` | `en` | `f8836772d748fa20e9555d9728d902ab73692377bbe55891a726f5587467f9fa` |
| `wordpress-security-basics` | `ja` | `6a2e9db872b2c1620c2b061e05e184437da549e2a6969ec0d006fd8c9a5447b0` |
| `wordpress-security-basics` | `ko` | `fbf003dee52a5b2f60801b7d3ef11b16edbd121ca14aca658e3650bf12385ed3` |
| `wordpress-security-basics` | `zh-CN` | `582613310b6658a5801df80c60336ceef282f0ec1d8a959346c7ade076677f92` |
| `wordpress-social-login` | `en` | `6f6d50b5c7dcffc78fa8bff8a6ec3f983a48b83da8c735d1b582031e192b4664` |
| `wordpress-social-login` | `ja` | `bb5e25c24994e8cc2dc7a8915fe532b76e245520dd10075dd4209f374c21cd27` |
| `wordpress-social-login` | `ko` | `f3485ac951806815cafe9524e363cbfb8eb1f7b9e8ea859e92d9d29fe44afc1d` |
| `wordpress-social-login` | `zh-CN` | `483f4c1d6732231fba34f962f01a73a54303468156313880e32a60f64874f8b8` |

## Exact localized assets

All 36 localized assets match their Pair commit Git blobs byte-for-byte. The three original-language asset sets are unchanged.

| Asset | SHA-256 |
|---|---|
| `apps/web/public/guides/wordpress-member-registration/diagram-1-en.svg` | `830ed1b05f7b8a415b87865ac6f319aeeaacd8592f5b5c58e921b55ca0f49eac` |
| `apps/web/public/guides/wordpress-member-registration/diagram-1-ja.svg` | `965673e859048c36f5da8c0e139af750249b47dc46f58c8c118506d35469a791` |
| `apps/web/public/guides/wordpress-member-registration/diagram-1-ko.svg` | `6967d60f2efa1958f92e9e04cf834beb5d761ab056761303f911a7c9df3eb60b` |
| `apps/web/public/guides/wordpress-member-registration/diagram-1-zh-cn.svg` | `7719d2c73e107d1db6d892bb9776da9259503ce550f62efd2ebe3c562326329d` |
| `apps/web/public/guides/wordpress-member-registration/hero-en.jpg` | `81f706ff1cfb7469c378f81afd665a7f4fd0a55bf215651ca34b5cbcb21750a2` |
| `apps/web/public/guides/wordpress-member-registration/hero-en.svg` | `cb380ebd87ab9c2cf02b00f0caea6a23b253da40102d43d2e8ed63e7efff24df` |
| `apps/web/public/guides/wordpress-member-registration/hero-ja.jpg` | `8b6630b4d68e99987898fbb737968c82a5b49dfc5f0b2ff948632f743b10facf` |
| `apps/web/public/guides/wordpress-member-registration/hero-ja.svg` | `40ad912be00718e619a8e5eae88ab2ea89931f3093ac55978951c4f10e8d814f` |
| `apps/web/public/guides/wordpress-member-registration/hero-ko.jpg` | `9ddf08c8acdd180f1bc133cf9972a4eaabf1ffd3e7df4dd9061a778d7e6b9acb` |
| `apps/web/public/guides/wordpress-member-registration/hero-ko.svg` | `9ec73adfe57a009631cf82b8c7fb2a00174c2a04951d5fe21b2fb4d386f3e84a` |
| `apps/web/public/guides/wordpress-member-registration/hero-zh-cn.jpg` | `b10870e0c3aec06646cff0b3c632951528280cfb52ec15479a9cf4f20d943d82` |
| `apps/web/public/guides/wordpress-member-registration/hero-zh-cn.svg` | `4c23d03eb9e5da1fd24589bcf60f1fe5dac3f8da70c7acc9eb6641bd6389bbca` |
| `apps/web/public/guides/wordpress-security-basics/diagram-1-en.svg` | `7843037781cf1ac84b792853c1103e3ee24037e843638dc474cb139c54d448aa` |
| `apps/web/public/guides/wordpress-security-basics/diagram-1-ja.svg` | `fad17c8fe7b081c19c7970fa2271111c29f82639ca52290feeafe56fb4259905` |
| `apps/web/public/guides/wordpress-security-basics/diagram-1-ko.svg` | `8282c0aaf020ecb6505314d11bd1f70f86c9ef74488e8045a1c008bebcaf8427` |
| `apps/web/public/guides/wordpress-security-basics/diagram-1-zh-cn.svg` | `905b124a9047adf72b22259f67ef41fd46b3940d2c81471a42d59d4a9afd3166` |
| `apps/web/public/guides/wordpress-security-basics/hero-en.jpg` | `65378532ff0198eee3ea095f75af10f54bda26ff4b820a6591733a2f16177326` |
| `apps/web/public/guides/wordpress-security-basics/hero-en.svg` | `fdde1208c667bb9d53e364cef24059b1fca61dafde92c6dfbf536a703a94d3eb` |
| `apps/web/public/guides/wordpress-security-basics/hero-ja.jpg` | `eeab7a74f8019aeea8bb8db02f108e40a01500f8dedb501314e5419746134194` |
| `apps/web/public/guides/wordpress-security-basics/hero-ja.svg` | `771821dc08df40772144c21d834df62b5fab1f329edaa270005b8a3f25831858` |
| `apps/web/public/guides/wordpress-security-basics/hero-ko.jpg` | `a2575042358107fba2624476a3d4f3b019a366f0fc3f627e5476258796387494` |
| `apps/web/public/guides/wordpress-security-basics/hero-ko.svg` | `dbe7978496f66b07a525f3b811aa50f55639cf52ed70f136b777575ad99e3c98` |
| `apps/web/public/guides/wordpress-security-basics/hero-zh-cn.jpg` | `0ed4740841339cc60ce9c79d316ffa2311cda3906ae1ceca9e8d64dc49fd1825` |
| `apps/web/public/guides/wordpress-security-basics/hero-zh-cn.svg` | `7ca222e821e05ddaa2bf4dcbbb46cf7a1d6182a8096261ddd9236f3f76cd401b` |
| `apps/web/public/guides/wordpress-social-login/diagram-1-en.svg` | `499a7700e4dc70819eecb6486e94a2c050dad82b2ed75e92b51862a787b27383` |
| `apps/web/public/guides/wordpress-social-login/diagram-1-ja.svg` | `c73624319729113d82ec4dfa0317db4e590a953b98211329606bdd81dcc04575` |
| `apps/web/public/guides/wordpress-social-login/diagram-1-ko.svg` | `11c1f0ed69aca4a231e8b1963cc6f54c1bc777463ac1795f15474d275eac9078` |
| `apps/web/public/guides/wordpress-social-login/diagram-1-zh-cn.svg` | `ed87d57de918c82930e447465083f5d202321b476e1cf7a565578f58c3d93aff` |
| `apps/web/public/guides/wordpress-social-login/hero-en.jpg` | `08685cff24f2a0a6cd48a358f5b42232455535be66fdd8658645fbe86ac71a4d` |
| `apps/web/public/guides/wordpress-social-login/hero-en.svg` | `e34c1de8cfad744bfdcc184d6e48faf849a07483390e2e95fd99bcd2818d1c90` |
| `apps/web/public/guides/wordpress-social-login/hero-ja.jpg` | `cea2a46b2edf6f649650b070b891108cb4baae22247912e46b46fb43c411e541` |
| `apps/web/public/guides/wordpress-social-login/hero-ja.svg` | `14a1994bfd9ca3ff14d26c1bcbf8a4dc6079e705001280466c5d42e213e679a3` |
| `apps/web/public/guides/wordpress-social-login/hero-ko.jpg` | `c21cc0054b5daf665bb6ce72648377c05beb630534c38b26fd57cfe6086c6b9c` |
| `apps/web/public/guides/wordpress-social-login/hero-ko.svg` | `83e1cef41321c97fc842818c28236632a4192608d4a17014dc6cc31a08bd9d97` |
| `apps/web/public/guides/wordpress-social-login/hero-zh-cn.jpg` | `66f3702665fda44deeaabec3b1894ee6a8d75851ced636bb26537ca2afcb5c87` |
| `apps/web/public/guides/wordpress-social-login/hero-zh-cn.svg` | `82c2ac2f6571e8f78e670b04423f80fecfad94aa0f4f5da0d15db2da8c4f2526` |

Sorted asset path/hash list SHA-256: `4a6545c33a277f696cb64962b04286c5782d9234602941cfea8a2cfb655f5cf5`.

## Local validation

- Pack lint: three entries checked, zero errors. Existing `no_summary` advisories and English length advisories remain; there were no lint errors.
- Focused API tests (`test_guides_content_pack.py`, `test_guides_content_links.py`, `test_guide_rich_blocks.py`, `test_guides_pack_ingest.py`): 78 passed, 7 skipped.
- `npm run check:tasks`: 946 task files validated after rebase; unrelated stale-claim and overlap warnings only.
- `git diff --check`: passed.
- All 24 localized SVGs parsed successfully with a 1600×900 viewBox; all 12
  localized JPGs decoded successfully at 1600×900.
- Each of the 12 target documents has 31 blocks, a localized title and
  description, a locale-specific hero and diagram, nonempty image alt text,
  Mokaair credit, and existing asset files. No TODO/placeholder marker or
  unrelated `ai-term-token`/`ai-term-model-parameters` ArticleInline remains.
- Independently viewed twelve four-locale contact sheets: diagrams, SVG covers, and JPG covers for each of the four Batch031 articles, including the deferred `wordpress-user-roles`; no clipping, overlap, or missing glyph was observed.

## Publication gate

This draft PR only stages repository content. The target locales remain unpublished until a separately reviewed and backed-up release runs the existing publication service. For `wordpress-user-roles`, PR #875 is merged, but its zh-TW source correction must be published and its task released before a separate content task can claim that pack; merge only the Pair B target locales into the corrected source pack. Recheck current production source versions, hashes, visibility, drafts, deployed assets, and sibling links before any later import or publication.
