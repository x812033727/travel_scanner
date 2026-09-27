---
id: 2026-09-27-record-batch029-five-language-wordpress-contact
title: Record Batch029 five-language WordPress contact publication
status: done
priority: P2
area: docs
owner: codex-batch029-release-record
claimed_at: 2026-09-27T21:34:40Z
created_at: 2026-09-27T21:34:34Z
completed_at: 2026-09-27T21:58:30Z
branch: codex/article-localization-029-release-record
depends_on: []
scope:
  - docs/article-localization/releases/batch029
  - tasks/open/2026-09-27-record-batch029-five-language-wordpress-contact.md
  - tasks/done/2026-09-27-record-batch029-five-language-wordpress-contact.md
---

# Record Batch029 five-language WordPress contact publication

## Why

Batch029's four WordPress contact guides were merged as source packs and then
published to production in 16 missing locale documents across four languages.
The publication, preserved originals, postpublication QA, and release hold
must have a durable record that reviewers can distinguish from source-code
merge status.

## Definition of done

- [x] A scoped Batch029 record lists each article's content, draft, publication,
      and public/browser QA status with pinned release evidence.
- [x] The owned production hold is independently cleared after final QA.
- [x] Repository task checks pass and the release record is merged through a PR.

## Steps

- [x] Claim a release-record-only scope.
- [x] Recheck production publisher and structural QA receipts.
- [x] Inspect all desktop/mobile and right-scroll visual captures.
- [x] Verify and clear the exact Batch029 owned hold.
- [x] Write and review the release record.
- [x] Open and merge the release-record PR after successful CI.

## How to verify

`npm run check:tasks` and `git diff --check`; read the final production
publisher, public QA, visual QA, and post-clear receipts at the hashes in the
release record. Confirm PR CI and merge state separately.

## Notes

Content PR #857 is merged. The guarded publisher dry-run selected exactly 16
`start_translation` and 16 `publish` operations, with no hubs. It published
those targets under a Batch029-owned hold after a verified 155,319,354-byte
PostgreSQL custom-format backup. Publisher verify receipt SHA-256:
`1a35906ad33f41a6670023cdfa7413be8161610a321cf8f1d60bb1f13c605c7c`.
Independent structural QA receipt SHA-256:
`c9a3e8907ea363e2dc8f9d5efcfda166ec799192410ca5e5016cf8b7b15d9d21`.
Independent visual receipt SHA-256:
`58b20cef1c1a78d411840c390473e5bab58f112f9d6251778d2f6f656e091ddb`.
The guarded four-lock helper cleared the owned hold once; hold-clear transport
receipt SHA-256 is `e75cd60a937d4535ee208ee370c3608e64358a1678e7a1f5f32f3fd053906fd6`.
Independent four-lock post-clear readback SHA-256
`97cf887da00999c9f337d11e27aca0213dc9934df3862f743640d4fbbf9c3b43`
confirmed both holds absent, 20 locale rows unchanged, clean host/main,
services/health, 2,240 sitemap entries, XML, and private drafts.
