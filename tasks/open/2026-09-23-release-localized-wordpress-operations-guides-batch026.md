---
id: 2026-09-23-release-localized-wordpress-operations-guides-batch026
title: Release localized WordPress operations guides batch026
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-23T19:10:13Z
completed_at:
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

- [ ] Record the exact final content PR head and all required actual CI results, including PostgreSQL release-safety tests, then bind the actual merged target and full Git tree.
- [ ] Refresh full live source rows, article/locale versions and visibility; stop or reconcile any source drift. Preserve hidden, withdrawn or expired states rather than republishing them.
- [ ] Assemble and independently accept the canonical wrapper for the four exact articles, 16 missing-language documents, 48 localized assets and unchanged original full rows/assets; preserve hashes and freeze only approved inputs.
- [ ] Verify a fresh restorable database backup, exclusive release ownership, deployed revision and service health through the existing hostinger2 flow.
- [ ] Run a read-only preview limited to the intended 16 new documents and necessary image references; verify conflict protection, durable journal, idempotent reruns and no unrelated writes.
- [ ] Create exactly 16 target-language drafts and publish exactly 16 article locales with zero hub publications, retaining all four original zh-TW rows and 12 original assets. Independently accept actual full models, revisions, actor, journal and operation history.
- [ ] Verify all 20 public language pages, complete body/source details, visible credits, all 60 image asset bytes, canonical, reciprocal hreflang, same-language links and full paginated API/XML sitemap coverage. Independently view desktop/mobile screenshots and confirm drafts remain private.
- [ ] Write the release record with per-article content/import/published/browser statuses and immutable evidence pins. Stage final acceptance, clear only the owned release hold after acceptance, and record fresh post-clear health.

## Steps

- [ ] Re-export the four full sources and compare the actual baseline before release assembly.
- [ ] Bind final CI, actual PostgreSQL execution, merged Git tree, independent document/image reviews and source-preservation evidence.
- [ ] Independently review and freeze the canonical artifact; validate the exact transport and actual bound helpers before using them.
- [ ] Backup, deploy, verify, preview, import target drafts, publish target locales and verify final journal through the established locks and concurrency guards.
- [ ] Run independent database/journal acceptance and serial public QA. Complete per-article visual review and all public asset hash checks.
- [ ] Record final acceptance, owned hold clearance and post-clear health; complete this task only after these actual gates pass.

## How to verify

Use the existing ArticlePack/GuideDocument, publication service and guarded release protocol. Scope: four articles, 20 full final documents, 16 new target languages, 48 new assets and 12 preserved originals. Expected initial source state from the content baseline is article v2 and zh-TW draft/published v4; this must be freshly verified. New target locales should be created at v1 then published at v2 under the current service semantics. A changed runtime requires fresh applicability review rather than assuming historical behavior.

Check five languages (`zh-TW`, `en`, `ja`, `ko`, `zh-CN`) per article on desktop and mobile: 40 viewport cases, 80 top/diagram screenshots, and 20 full-body/detail cases. Headless responsive screenshots do not prove physical-device operation. Verify all 48 new assets, including editable hero SVGs not selected directly by the body manifest, plus 12 original files. Read all sitemap pages before declaring coverage complete; a truncated or failed page is not an acceptable result.

Preserve all 32 structured ArticleInline links. A link is clickable only when its target is currently published in the same language; unavailable targets must remain text. Keep original code, file paths, commands, URLs, dates, Mokaair credit and applicable conditions unchanged. Check source-body preservation and target-only image-description backfills separately.

## Notes

Exact article scope:

| Article | Source blocks | Source citations | Image block index |
| --- | ---: | ---: | ---: |
| `wordpress-admin-basics` | 30 | 4 | 25 |
| `wordpress-ftp-file-management` | 30 | 6 | 25 |
| `wordpress-local-development` | 29 | 4 | 24 |
| `wordpress-website-backup` | 29 | 7 | 24 |

Indexes are zero-based. Target languages are only `en`, `ja`, `ko`, `zh-CN`. There are no hubs, source corrections, numeric exceptions or route derivatives in this batch. All original source dates remain `2026-09-14`. Preserve roles/site-type exceptions, host-key checks, SFTP/FTPS and host-plan limits, Windows/MAMP port conditions, WXR versus full-backup distinctions, paid/free plugin limits, restore overwrite risks and external integration isolation.

Content task: `2026-09-23-localize-four-wordpress-operations-guides-batch026`. Content PR remains pending when this body is prepared; add only its verified reference at task creation. Actual task identity is `2026-09-23-release-localized-wordpress-operations-guides-batch026`, created through the task CLI as open/unclaimed with dependency on the content task and repository scope restricted to `docs/article-localization/releases/batch026`.

Content evidence archive: `C:/Users/x8120/.codex/article-localization-release/batch026-wordpress-operations/`. Integration manifest SHA256 `c294be54bdcfa1e4e954f153aa398624c1ce6132aa646b6fd00622bac6a6516f`; independent integration review `9bbed398ba2d7580d5a96bcc4a242de0e3dd232e3dd7ee2e6363359540d7c606`; actual application `c19fe2c4738b0d6aeb3a01c3f978ddaf46e93da607116288829273436fb32012`. The local summary at claim HEAD `d0299b21a95905dc8ac3651b25d32a0f6dbe88dc` is `c33f006afa69f0558ceea7abe79f17b021524b24df069d480d29206532f28b14`: seven groups / 16 commands passed, 64 PostgreSQL tests skipped for missing isolated integration services, 24 pack-lint advisories, no failed or incomplete attempts. No batch026 CI, merge, deployment, import, publication or public-browser acceptance is claimed by those records.

The 21 official references were read for editorial conditions. No provider/plugin account, installed WordPress/MAMP instance, paid plan, real backup/restore or physical device was tested by this translation work. Preserve actual failed attempts, skips and evidence history. Unrelated glossary-link, cable and URL/source corrections are excluded.
