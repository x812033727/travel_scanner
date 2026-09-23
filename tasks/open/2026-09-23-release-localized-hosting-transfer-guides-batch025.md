---
id: 2026-09-23-release-localized-hosting-transfer-guides-batch025
title: Release localized hosting transfer guides batch025
status: open
priority: P2
area: ops
owner:
claimed_at:
created_at: 2026-09-23T17:43:35Z
completed_at:
branch:
depends_on:
  - 2026-09-23-localize-four-hosting-transfer-guides-batch025
scope:
  - docs/article-localization/releases/batch025
---

# Release localized hosting transfer guides batch025

## Why

The separately reviewed batch025 content adds English, Japanese, Korean and Simplified Chinese to four published Traditional Chinese guides. This task owns the release record and remaining CI, merge, deployment, import, publication and public acceptance. Content/local checks do not establish production completion.

## Definition of done

- [ ] The exact final content PR head has all required CI checks, including actual PostgreSQL release-safety evidence, and its merge/tree identity is recorded.
- [ ] A canonical wrapper binds the exact four articles, 16 missing-language documents, 48 localized assets, source full rows and original versions; independent review and portable artifact hashes are recorded.
- [ ] The guarded hostinger2 flow verifies a fresh restorable database backup, exclusive release ownership, deployed revision and service health before publication.
- [ ] A read-only import preview limits changes to the 16 target documents and necessary image references; publication is idempotent and preserves source bodies, metadata, revisions and any changed visibility.
- [ ] All 16 intended missing-language documents are published; all four original zh-TW documents and 12 original image files are unchanged. Actual database full-row/revision/journal acceptance is independently checked.
- [ ] Five-language public body, images, canonical, hreflang, structured links and sitemap checks pass; actual desktop/mobile screenshots are independently viewed. Drafts remain private.
- [ ] The final release record contains exact inputs, operations, acceptance, explicit limitations, successful hold clearance and fresh post-clear health evidence.

## Steps

- [ ] Re-export the exact live sources and compare source versions/full rows before preparing the release.
- [ ] Bind final CI, merged Git tree, reviewed models/images, canonical jobs and wrapper provenance; freeze only after independent acceptance.
- [ ] Backup, deploy, verify health, preview, import target drafts, publish target languages and verify final journals using the established locks and conflict guards.
- [ ] Perform independent database acceptance and serial production QA, including same-language link publication conditions.
- [ ] Write the batch025 release record, clear only the owned hold after acceptance, and record post-clear health.

## How to verify

Use the existing ArticlePack/GuideDocument assembly and publisher contracts. Check exactly four articles, 20 final documents, 16 new target-language revisions, 48 new assets and 12 preserved originals. Do not infer production success from a merged PR, HTTP 200, a local fixture or an import preview. Preserve actual failed attempts and all evidence pins.

Verify five languages (`zh-TW`, `en`, `ja`, `ko`, `zh-CN`) for each article, on desktop and mobile: 40 viewport cases and 80 top/diagram screenshots. Inspect full body/source details and the complete paginated sitemap. Structured ArticleInline targets may link only when the same-language target is actually published; unavailable DNS translations remain nonclickable.

## Notes

Exact article scope: `domain-registrar-transfer`, `fastcomet-wordpress-setup`, `hostgator-wordpress-setup`, `siteground-wordpress-setup`. Target languages are `en`, `ja`, `ko`, `zh-CN` only; no source correction or unrelated publication is authorized by this task.

The initial sources were published article v2 with zh-TW draft/published/latest v4. Reconfirm these identities at release time; do not use this historical snapshot as a current-state override. Preserve all original source URLs and `checked_on: 2026-09-14`. The content includes ICANN gTLD versus ccTLD boundaries, conditional transfer locks, backup/restore restrictions and plan-dependent facilities. HostGator primary pages returned 403 during editorial review; this is not a fresh account, payment, performance or physical-device acceptance.

Content evidence lives outside the repository at `C:/Users/x8120/.codex/article-localization-release/batch025-hosting-transfer`. The initial integration receipt is `87d73e6aa82c1b7a4cb5b0a8a0b212b84cd17fc18bcd587344af206e5f67e811`; local summary at source worktree HEAD `1b01c6075886e49294832dc25dbf948f58c1aa08` is `e2dd24527777c04fdeb83b44fe2b9b8c2fb252539cbfaef0e285107a9492c3de`. Those records cover content and local checks only. No deployment, import or publication has occurred under this task when it is created.

Content PR: https://github.com/x812033727/travel_scanner/pull/700. The content task is archived within that PR after actual content/local acceptance; this release task remains open/unclaimed and all release gates above are still pending.
