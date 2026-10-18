# 2026-10-08 design and performance locales published

Twelve life articles now publish en, ja, ko and zh-CN. [PR #1378](https://github.com/x812033727/travel_scanner/pull/1378) merged and deployed as `bcba139a05e1ac6c3ce8a4e768086bf0d3b4a86f`. The owner authorized this exact 12-article cohort. The authoring task is `2026-10-07-localize-twelve-design-workflow-and-performance`; the release task is `2026-10-07-release-localized-design-web-life-wave5`.

The approved content head `2150d414168a681b3598bf56eb985d74dda2201a` was integrated with main as `f01faf630664e8bf1a6fac55511a3ef8ab8701e4`. All 162 approved changed files remained byte-identical, and all 21 checks passed on that exact integrated head. One normal deployment and the postdeploy checks completed without force or hold bypasses.

Fresh production source guards passed before writing. The full original snapshot was retained; a repository-backed baseline projection excluded 350 unrelated database-only news rows, with all 12 selected source rows unchanged. The reviewed payloads were rebound to this fresh baseline without new translation or editorial approval. Fresh bundle manifest: `7195c55422170f3eb76ce9856eeb3cad6d7082914a18190e821ba89ab94c80a0`.

All nine release phases completed: prepare, dry-run, backup, isolated rehearsal, drafts, publish-articles, publish-hubs, unchanged replay and complete. The consistent database backup covered 161 tables, its catalogue was readable, and the restored fixture passed source guards and all table counts. Publication wrote 48 new locales and four approved Traditional Chinese corrections, for 52 selected targets. Unchanged replay preserved publication data and write-phase journal bytes. Final acceptance verified 60 pages, 120 desktop/mobile originals, 180 distinct media files, document hashes, canonical/hreflang, rendered links and sitemap coverage. Only this release's owned hold was cleared.

The link index rebuild materialized 3,768 links and dropped none. All five global links-check commands exited 1; they are not recorded as a globally clean result. This cohort had no Traditional Chinese findings and 23 unpublished related-target findings in each added locale, with no other selected problems. Related target articles outside this cohort still await localization.

## Authoring and preserved failures

All 48 translations received independent complete-text, native image and glyph reviews bound to exact document and artifact hashes. Four sources had five irrelevant AI glossary links changed to plain text with the same visible words; eight other complete source documents, all original dates and 36 source media files stayed unchanged. Exact source corrections remain in `docs/article-localization/source-corrections/wave5-web-life-20261008.md`.

The original single CLI authoring run exited 1: 46 translated results and two rejected Korean results. Six targets were repaired from independent proposals, images were refined and fresh independent reviews passed; no provider retry occurred. The unchanged official assembler ran once with exit 0. An external post-check initially rejected topic order; an independent check confirmed the exact pinned-baseline permutation, the topics multiset and every other metadata field. The original failure was preserved and the assembler was not rerun.

The official installer and identical-argv replay both exited 0. All 164 journal operations, packs, 152 manifest assets, original backups and 12 installation receipts were byte-identical across replay; the shared Windows lock's incidental append was excluded from that identity claim. Independent installed-data auditing passed. Local checks passed: content-pack tests 9 passed/5 skipped, localization-tool tests 68 passed, zero lint errors, 60 no-summary warnings and 12 text-length warnings retained.

The GitHub CLI ready attempt failed a TLS handshake; the original wrapper exit 1 and unpersisted child exit were retained. Fresh inspection showed an unchanged draft before one reconciled normal ready/merge operation. After the successful deployment, a local verification formatter guard failed; only read-only verification was resumed, and deployment was not repeated. The independent postpublication audit also retained a failed date-format diagnostic before checking the repository's date-based expiry rule. Full original receipts remain outside Git; their exact hashes are retained in `evidence.json`.

## Published source guards

Every added locale's public version, complete document hash and URL, all media byte hashes and raw receipt hashes are in `evidence.json`.

| Article | zh-TW public version | Normalized public document SHA256 |
| --- | --- | --- |
| amp-website-decision | 6 | `7369c58003df56cc169d35efb05523c392cace876dddc1247daa5dfe250bbd40` |
| core-web-vitals-diagnosis | 4 | `79ea28908b8fc68573f202b0fdb0ade13029263a27073b88c9f672e01f925372` |
| figma-design-basics | 4 | `00bacd3467a6441febabc6372f10b96ce8a610784af66623d01684a467aee851` |
| lazy-loading-images | 6 | `2dda1061b6dd39fdfd06fe12b257d82ac92bfea46ded62ac0bddba6bb68bbde4` |
| lottie-web-animation | 4 | `56418ca1b26624eff12ed8efc540cf922391bba7d62e9b3ace31d959e3c85328` |
| open-graph-sharing | 6 | `8df97903caaae96f1792f04a3947d4a043991347ad5768051db0a110c5bc936f` |
| pagespeed-performance-review | 4 | `531a885101bc55e7c004988f19b64e818f219fbc9f2c2d7e1d843218b7666011` |
| rgb-cmyk-export | 4 | `f061761570269a8db0bf37b55c5eca0e809b4420f259032b72c359f5d8681ee4` |
| saas-paas-iaas-responsibility | 4 | `09bf76eb30950895f5c383381387442b5616522dee4d380d06cdb1f1ce35aaf2` |
| sass-scss-workflow | 4 | `37205fd94a9316f066553fb8b475a9577417a4372372d283fb1234edd4ff631f` |
| ui-ux-learning | 6 | `b01fb3630f90549698f89d9eac791dcc011b91e6b0e38069f0c9d8c1a6469411` |
| wireframe-prototype-testing | 4 | `74caa606d5c8265ef1d3494e690781b9db11ee3d442fc904c6ebc70c3d976b75` |

The prior 32 articles and their 160 documents remain identical to their original actual publication snapshot. The frozen 13-article PR #1374 cohort remains untouched, with all 52 target locale rows absent. A fresh observed census contains 1,409 public articles in intel/howto/life, of which 818 still lack 3,272 locale documents (818 each for en, ja, ko and zh-CN). The overall missing-language work remains unfinished.

Private snapshots, raw logs, screenshots, machine paths, database/actor identities and producer identifiers remain in the owner's external evidence storage. This repository keeps only this README and sanitized `evidence.json`.
