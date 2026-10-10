# Next web and life localization source audit

Status: bounded source investigation complete; this handoff grants no SOURCE, translation, merge, deployment or publication approval. The candidate set is 17 active published life articles with 68 missing language documents. Twelve require new translations; five contain existing local translations to review and reuse.

## Current production and preserved completed work

The official read-only export was captured on 2026-10-09 at 20:32 Asia/Taipei under all four existing deployment locks. It observed a clean stable current Git/API runtime at `c2a153ab406714bbc5c8fa00b10f38f8a9af38e9`. SSH exited 0; uncertainty and validation failure were absent. The exporter used a repeatable-read READ ONLY transaction and rollback. No article, setting, provider, job or publication write occurred.

Snapshot SHA-256: `ef3ef1cfeca66169cdb6f77499a2b3c4eec2230a805a46c08ab619203304c209`.
Root source-screen SHA-256: `713373d97a50b60c7bb71fc1b67e962dfe349483dad07364225fece99ac374db`.
Independent integrity/census/preservation review SHA-256: `3444ab3cc59e6ce2de16422fa12e3685a1bf8853ba04c2a6c8eee0af57bfa6f8`.

The current scope has 1,551 active published intel/howto/life articles. 805 articles still lack 3,220 documents: 805 each in en, ja, ko and zh-CN; no scoped zh-TW language is missing. All 17 candidate article/source-locale guards match the October 8 baseline. All previously completed 57 articles and 285 public documents match their original postpublication snapshots. The completed localization program has published 228 new language documents; this audit adds none.

The first read attempt was deliberately bound to the completed October 8 release and refused because the host checkout had changed. Its original refusal remains preserved. A separately reviewed current-runtime read-only exporter then made one successful attempt. Original release receipts and the completion ledger remain unchanged.

## Exact candidate source guards

| Article | Published zh-TW version | Normalized published source SHA-256 | Repository/source | Local locale count |
| --- | --- | --- | --- | --- |
| design-thinking-practice | 4 | `857a5be3f7a943afb443ccde509e08836aa2c1638a6de0329bdcf2a1fde9aa28` | equal | 1 |
| portfolio-case-study | 4 | `77b7e654e56aec4edb57501e589cb2eb8666debe8feb77838accef932a74d0a9` | equal | 1 |
| brand-identity-logo-brief | 4 | `81e4730d2f1025abc947462877573f3ef0195b252593225ae8a7a1aaf43219da` | equal | 1 |
| web-design-agency-brief | 4 | `9a2872dc2f80efaa0e74545107f15f49b9cc92a3ed73943125e9e03c71870ae4` | equal | 1 |
| website-404-recovery | 4 | `c7f8d1378d95db2b9c8f5df49499892e3a9464bb1b820208589efe9894a06373` | drift | 1 |
| website-www-subdomains | 4 | `cc521d0025b0a0c60cc709ba40581c29d2ce927e21a07f18647ff4240f81b949` | drift | 1 |
| ai-design-prompt-workflow | 4 | `4106a63b92268a6d8ee8e774a774d7283e6659e3b812db8b6cee3eb94bae1bbc` | equal | 1 |
| canva-design-workflow | 4 | `52f51c88a82a459398e6e599096a82c8ea9e704380465804c1149be6e1ef4383` | equal | 1 |
| customer-journey-funnel | 4 | `2248c9e3878192970816dcc8def7951bff5aed0526cfb0188f1209b05ceabbc3` | drift | 1 |
| marketing-copywriting | 4 | `8aa601c0f4896b26762777ba88c31b821c8630ba605a6285e518c49084963ecc` | drift | 1 |
| seo-domain-authority | 4 | `f2b1cbb9ddb7a108e66f1d7f41c4a726074948e38c260ab03ff4fdd2ebfb16a5` | equal | 1 |
| seo-trust-sensitive-topics | 4 | `37a2e06bc46baa91015ebc21b86f7d598419642811ac1c21ae42d186630d3919` | equal | 1 |
| paid-vs-organic-marketing | 4 | `5e1a8e1569da09bc78c46a3dfc8e465550ecebf9722b21be6756023e80ff8f16` | equal | 5 |
| wordpress-blog-build | 4 | `e90738e066cae12a93dacf5d40ce4eb37993078b8eb61c12311cf8f786592189` | drift | 5 |
| wordpress-comment-spam | 4 | `ef124872b2da725961846d3bb941f65a51b953f8a2c6ed9ac8f0df88467da98d` | drift | 5 |
| wordpress-performance-plugins | 4 | `b51710d0eaf7b53708f29399103471c22573264b6d68a5e997883b4188922f39` | drift | 5 |
| wordpress-reset-safely | 4 | `0e35950667a9c14985c34c0c9e30db67c93c100a8b48bb741f4ed5daa87ebfa6` | drift | 5 |

All four target locale publications are absent for every candidate. A local locale count of five establishes existing content only; it establishes no independent translation or public acceptance result.

Eight source documents differ from their repository packs: website-404-recovery, website-www-subdomains, customer-journey-funnel, marketing-copywriting, wordpress-blog-build, wordpress-comment-spam, wordpress-performance-plugins and wordpress-reset-safely. Independent exact-pointer review explains their ten removed ordinary-word hyperlinks. Five further source packs still contain five such hyperlinks. The proposal removes only unrelated AI-glossary links while preserving their visible words: 15 unique inline edges across 13 articles, corresponding to 45 normalized changed leaves. Published source documents remain authoritative; no correction has yet been admitted or applied by this audit.

Independent editorial audit SHA-256: `2d128ca5a3dee8a403751e76d5f03cba41dcb839688d9bc51349fc1491245b0b`.
Exact finding/proposal SHA-256: `ca957c510635e2c38d3b9e24996bb1a83b54b2f9dc3344e5d34adf012571735d`.
Fresh full-source rebinding SHA-256: `ce9c9567a919a9f06930515e1393416b734d7ffdad9b6bb84cb4607dda6b6fb3`.

The independent reviewer read all 17 sources, 555 content blocks and 84 citation entries, and personally inspected 34 original source images. The reviewer and its child read substantive current primary content at 59 distinct URLs; this is not a claim that all 84 citation destinations received complete current body or HTTP verification. Original NIH tool-retrieval failures remain preserved. Root separately read substantive official indexed NIH text about information ownership, evidence, authorship, dates and privacy; that supplement establishes neither a fresh HTTP 200 nor equivalence of alternate ODS routes. No article source dates or URLs were changed and no SOURCE PASS was issued.

## Ownership and next gates

The current main queue at `12f8a8413d7c1126071e0848606520a812838cd5` records four historical candidate content tickets as done. The paid-vs-organic paired ticket is open with no owner and has an explicit owner-approved stale-claim release. Current independent primary reading found no concrete defect in its descriptive Google SEO citation title or retained exact Google Ads `hl=zh-Hant` URL; a narrow follow-up must record withdrawal of those historical questions, without inventing a metadata correction. Older worktree copies still contain five historical claim groups. Their observations remain preserved, but their stale status alone is not treated as release: the current done/release records provide the evidence. Root's subsequent live open-PR inventory found 20 open PRs, with no new candidate content branch; recheck current scopes immediately before any narrow authoring claim.

This task owns only this audit handoff. Existing content, image bytes and dated source metadata remain unchanged. Source proposals must use an independent proposer, a separate applicator and a separate final reviewer. No final review is inferred before an actual correction and its exact bytes are shown. Preserve original source dates unless an exact reviewed correction explicitly includes one.

Independent proposal reconstruction and full handoff review exited 0 with no blockers. Review SHA-256: `e759638b4601759e88a30f355b9f136c7f8f11061de2a792d14635feec3514f5`. It binds 17 actual original pack copies, twenty existing target documents and 111 candidate media files, and reconstructs all 45 proposed source leaves through the unchanged official schema.

The bounded source investigation and handoff review are complete. Narrow follow-up task `2026-10-09-localize-reviewed-web-design-wave6` records the actual application, source admission and language work. The independent source auditor proposes; a separate operator applies only the exact claimed corrections; a distinct final source reviewer reads the actual final source bytes. These are assigned roles, not future PASS receipts. Source admission requires those real final reviews before baseline preparation or authoring. Existing twenty target documents require current independent language and image review; twelve new sources need 48 authored documents. Publication requires its own concrete reviewed cohort decision after content work and CI.

All raw snapshots, source pairs, native images, primary-source receipts, worktree/PR inventories and failed attempts remain in private external evidence storage.
