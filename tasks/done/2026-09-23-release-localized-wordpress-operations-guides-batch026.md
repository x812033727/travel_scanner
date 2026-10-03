---
id: 2026-09-23-release-localized-wordpress-operations-guides-batch026
title: Release localized WordPress operations guides batch026
status: done
priority: P2
area: ops
owner: codex-batch026-release
claimed_at: 2026-09-27T06:19:30Z
created_at: 2026-09-23T19:10:13Z
completed_at: 2026-09-27T08:10:35Z
branch:
depends_on:
  - 2026-09-23-localize-four-wordpress-operations-guides-batch026
scope:
  - docs/article-localization/releases/batch026
---

# Release localized WordPress operations guides batch026

## Why

The separate batch026 content adds English, Japanese, Korean and Simplified Chinese to four published Traditional Chinese WordPress guides. This task tracks the release record and remaining CI, merge, guarded deployment, import, publication and public acceptance. Content reviews and local checks alone do not establish production completion.

## Definition of done

- [x] Record the exact final content PR head and all required actual CI results, including PostgreSQL release-safety tests, then bind the actual merged target and full Git tree.
- [x] Refresh full live source rows, article/locale versions and visibility; stop or reconcile any source drift. Preserve hidden, withdrawn or expired states rather than republishing them.
- [x] Assemble and independently accept the canonical wrapper for the four exact articles, 16 missing-language documents, 48 localized assets and unchanged original full rows/assets; preserve hashes and freeze only approved inputs.
- [x] Verify a fresh restorable database backup, exclusive release ownership, deployed revision and service health through the existing `<saved-session>` flow.
- [x] Run a read-only preview limited to the intended 16 new documents and necessary image references; verify conflict protection, durable journal, idempotent reruns and no unrelated writes.
- [x] Create exactly 16 target-language drafts and publish exactly 16 article locales with zero hub publications, retaining all four original zh-TW rows and 12 original assets. Independently accept actual full models, revisions, actor, journal and operation history.
- [x] Verify all 20 public language pages, complete body/source details, visible credits, all 60 image asset bytes, canonical, reciprocal hreflang, same-language links and full paginated API/XML sitemap coverage. Independently view desktop/mobile screenshots and confirm drafts remain private.
- [x] Write the release record with per-article content/import/published/browser statuses and immutable evidence pins. Stage final acceptance, clear only the owned release hold after acceptance, and record fresh post-clear health.

## Steps

- [x] Re-export the four full sources and compare the actual baseline before release assembly.
- [x] Bind final CI, actual PostgreSQL execution, merged Git tree, independent document/image reviews and source-preservation evidence.
- [x] Independently review and freeze the canonical artifact; validate the exact transport and actual bound helpers before using them.
- [x] Backup, attest the already deployed target, preview, import target drafts, publish target locales and verify the final journal through the established locks and concurrency guards.
- [x] Run independent database/journal acceptance and serial public QA. Complete per-article visual review and all public asset hash checks.
- [x] Record final acceptance, owned hold clearance and post-clear health; complete this task only after these actual gates pass.

## How to verify

Use the existing ArticlePack/GuideDocument, publication service and guarded release protocol. Scope: four articles, 20 full final documents, 16 new target languages, 48 new assets and 12 preserved originals. Expected initial source state from the content baseline is article v2 and zh-TW draft/published v4; this must be freshly verified. New target locales should be created at v1 then published at v2 under the current service semantics. A changed runtime requires fresh applicability review rather than assuming historical behavior.

Check five languages (`zh-TW`, `en`, `ja`, `ko`, `zh-CN`) per article on desktop and mobile: 40 viewport cases, 80 top/diagram screenshots, and 20 full-body/detail cases. Headless responsive screenshots do not prove physical-device operation. Verify all 48 new assets, including editable hero SVGs not selected directly by the body manifest, plus 12 original files. Read all sitemap pages before declaring coverage complete; a truncated or failed page is not an acceptable result.

Preserve all 32 structured ArticleInline links. A link is clickable only when its target is currently published in the same language; unavailable targets must remain text. Keep original code, file paths, commands, URLs, dates, Mokaair credit and applicable conditions unchanged. Check source-body preservation and target-only image-description backfills separately.

## Notes

Post-merge checkpoint (2026-09-27 UTC): content PR #842 passed all nine CI checks on head `0f0e4c3ae1d3da20479c84a3f28c4c710311bfb8` and merged as `243b0f2f84359456ebf68c6f0b450d9ef19c344f`. Both commits have full Git tree `70077bef59efece203e236ad6bb58ac55d991aad`; their file diff is empty. Fresh read-only source export `live-source-full-20260927T062045Z.json` (SHA-256 `ad6bf19cdf295587c2682374bcb2f82d8565714a92a3799a9b5a173d5f38e1a5`) confirms all four full article rows, publication states and revisions equal the previous baseline. Fresh read-only host preflight `host-readonly-20260927T062114422928Z.json` (SHA-256 `ea75196b5b0a25ffd8e66472d861d77b1d4074591b84d1cdc17fdb19737b74c7`) found clean old host, no hold or pending release, and healthy endpoints. These are pre-release checkpoints, not evidence of deployment/import/publication; repeat before production writes.

Canonical checkpoint: independent root candidate review `a1a8128db43aa26ed921822f699bcd629f2baeeed68c63aa7c09a10b0af790fe` verified 733 wrapper files, 489 exact merged Git blobs, four live source models, 16 target documents, 60 assets and 16/16/0 selected operations. Frozen ZIP SHA-256 `d2c63d368372438f52e53de1903fe64cc40ba4569c2a6fcf2f103211db1220b6` passed a separate full member/CRC/byte review (`e3bd6f56f8abf63585240fcf741fac89293f1570987f22a9d1e9f89a981341c2`). A read-only schema capture found Alembic already at `0101_video_dub_locales`; migration review `39c217cc4872e2ea001084c6884fa70405471699f419bbe933401940d6321448` requires a revised no-upgrade transport. The earlier 0099-assuming transport is stale and must not run. No production write has occurred.

Exact article scope:

| Article | Source blocks | Source citations | Image block index |
| --- | ---: | ---: | ---: |
| `wordpress-admin-basics` | 30 | 4 | 25 |
| `wordpress-ftp-file-management` | 30 | 6 | 25 |
| `wordpress-local-development` | 29 | 4 | 24 |
| `wordpress-website-backup` | 29 | 7 | 24 |

Indexes are zero-based. Target languages are only `en`, `ja`, `ko`, `zh-CN`. There are no hubs, source corrections, numeric exceptions or route derivatives in this batch. All original source dates remain `2026-09-14`. Preserve roles/site-type exceptions, host-key checks, SFTP/FTPS and host-plan limits, Windows/MAMP port conditions, WXR versus full-backup distinctions, paid/free plugin limits, restore overwrite risks and external integration isolation.

Content task: `2026-09-23-localize-four-wordpress-operations-guides-batch026`. Content PR remains pending when this body is prepared; add only its verified reference at task creation. Actual task identity is `2026-09-23-release-localized-wordpress-operations-guides-batch026`, created through the task CLI as open/unclaimed with dependency on the content task and repository scope restricted to `docs/article-localization/releases/batch026`.

Content evidence archive: `<home>/.codex/article-localization-release/batch026-wordpress-operations/`. Integration manifest SHA256 `c294be54bdcfa1e4e954f153aa398624c1ce6132aa646b6fd00622bac6a6516f`; independent integration review `9bbed398ba2d7580d5a96bcc4a242de0e3dd232e3dd7ee2e6363359540d7c606`; actual application `c19fe2c4738b0d6aeb3a01c3f978ddaf46e93da607116288829273436fb32012`. The local summary at claim HEAD `d0299b21a95905dc8ac3651b25d32a0f6dbe88dc` is `c33f006afa69f0558ceea7abe79f17b021524b24df069d480d29206532f28b14`: seven groups / 16 commands passed, 64 PostgreSQL tests skipped for missing isolated integration services, 24 pack-lint advisories, no failed or incomplete attempts. No batch026 CI, merge, deployment, import, publication or public-browser acceptance is claimed by those records.

Release attempt checkpoint (2026-09-27 07:15 UTC): target code `243b0f2f...` was already running on the clean host, while remote `main` advanced through unrelated commits. Root independently reviewed canonical ZIP and transport v4, then staged v4 under `/root/mokaair-localization-026-ahead-243b0f2f8435`. The host made a new 151,700,123-byte protected `pg_dump -Fc`, verified it with `pg_restore --list`, and attested the unchanged 13 running services and Alembic `0101_video_dub_locales`. The first publisher `dry-run` refused with `No active configured owner available`: the pinned actor was not the currently eligible owner. The publisher state contained only `.lock` and no journal; read-only full source rows remained exactly unchanged. After inspection under four locks, the attempted release wrote an abort receipt, retained its backup/evidence, withdrew only its own hold, and confirmed three healthy checks. No batch026 draft or article publication occurred. V4 must not be resumed; a new candidate must pin the eligible current owner. Relevant local evidence: `root-review-transport/transport-review-v4.json`, `host-phases-v4/dryrun-error-diagnostic.json`, `host-phases-v4/owner-readonly-20260927T071316Z.json`, and `host-phases-v4/withdrawal-v4-receipt.json` under the batch026 release archive.

The 21 official references were read for editorial conditions. No provider/plugin account, installed WordPress/MAMP instance, paid plan, real backup/restore or physical device was tested by this translation work. Preserve actual failed attempts, skips and evidence history. Unrelated glossary-link, cable and URL/source corrections are excluded.

Final v5 result (2026-09-27 08:08 UTC): the new owner-pinned transport SHA-256 `504b0de4ed948d8d9066ee62f87588b500389a68e44bab2a028bac00a9d12f20` passed independent transport and production preflight. Its new `pg_dump -Fc` backup was verified by `pg_restore --list` (backup receipt SHA-256 `bddc46bf953c478a233ee85abf8f87adffbe9d31e9824d11260491e3a554397d`). The host was already running clean target `243b0f2f...` and 13 pinned containers; no deployment restart or migration was needed. Dry-run selected only 16 drafts, 16 article publications and zero hubs. The protected release completed all 32 operations under the active configured owner; final journal SHA-256 `d16a4413f33380d52ad2dc71eb5bfc0c11d0c743a8896bb81abe982461935eb5`, with no pending intent and an idempotent final dry-run.

Independent full DB/journal receipt SHA-256 `b4716d8e62924ee1a0cf47b5924823879d0249abdd3ad4faf8d5e86f15c36cf2` passed 318 checks; actual-v5 public QA receipt SHA-256 `01b039af5260bb9da752e4bb5634f8621bf78d44e4c4a6fe526a4eff78ae2a6a` passed 20 pages, 60 exact image bytes, 32 links, three API sitemap pages (2,147 entries), five XML life sitemaps and unpublished-body privacy. Root visual receipt SHA-256 `4a88d750bcb3301b93d91b2311c7b860678e97b3f7f5ef51af2a52e30dbffb95` covers 40 desktop/mobile cases and 80 screenshots. Final host acceptance SHA-256 `61ff894903edad902acfa57e597e38128d6ed6ae2abedb11048bdf59de11d12c` bound six independently read-back evidence files. The guarded clear phase returned `cleared` (host receipt SHA-256 `cfb14e0e7827556efe84cb88d2ddf5f84eef436fda3ed6423de89dc77283e6ca`); post-clear read-only review SHA-256 `d65311660447389beef33f795fd9ddcf1639cec38c9db014fb440ebe8b2b3e50` confirmed absent hold, unchanged journal, target/runtime and three healthy service checks. Per-article matrix and limits are in `docs/article-localization/releases/batch026/README.md`.
