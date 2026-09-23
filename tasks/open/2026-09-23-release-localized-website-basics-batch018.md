---
id: 2026-09-23-release-localized-website-basics-batch018
title: Release localized website basics batch018
status: open
priority: P1
area: ops
owner:
claimed_at:
created_at: 2026-09-23T07:02:24Z
completed_at:
branch:
depends_on:
  - 2026-09-22-localize-four-website-basics-guides-batch018
scope:
  - docs/article-localization/releases/batch018
---

# Release localized website basics batch018

## Why

The four website-basics packs have sixteen reviewed translations and forty-eight
localized images. A merged content PR alone does not publish those languages.
Keep the remaining CI, deployment, import and public acceptance gates explicit.

## Definition of done

- [ ] Exact content PR head passes required CI and is reviewed and merged.
- [ ] Fresh live source/visibility/version inventory still permits missing-language
      publication for exactly the four slugs below; retain any concurrent edits.
- [ ] Freeze reviewed canonical bundle, original/version hashes and image evidence.
- [ ] Verify fresh database backup and deployment health under the existing owned
      hold/locking protocol; deploy only the reviewed necessary code and images.
- [ ] Dry-run and idempotent import/publish change only en, ja, ko and zh-CN.
- [ ] All twenty five-language pages pass full-body/image/canonical/hreflang/link
      checks and desktop/mobile visual review; unrelated drafts remain private.
- [ ] Record per-article content/import/publication/browser evidence and release
      only this task's owned hold after acceptance.

## Steps

- [ ] Review final Git export and CI for the content PR.
- [ ] Refresh source snapshot and assemble/review the exact release bundle.
- [ ] Deploy, import and publish through the reviewed explicit-list publisher.
- [ ] Complete database and public-browser acceptance and delivery receipt.

## How to verify

Use `docs/article-localization/publish_bundle.py` and the existing guarded release
workflow, with explicit slugs and target locales. Bind the full normalized
documents, deployed image bytes, original rows, final journals and screenshots.
Follow `.agents/skills/deploy/SKILL.md` and the content-pipeline publish runbook.

## Notes

Exact scope: `domain-registration-guide`, `hosting-types-explained`,
`website-cms-choice`, `website-maintenance-routine`. Source inventory on
2026-09-22 showed active published article v2 / zh-TW locale v4 with no draft
divergence. Recheck those facts before release; this task does not assert they
remain current.

Reviewed work and receipt pins are in the dependent content task and the persistent
outside-Git directory `C:/Users/x8120/.codex/article-localization-release/batch018-web-basics/`.
All sixteen documents and forty-eight images passed independent review. Five
Japanese number-format equivalences were explicitly reviewed; the strict field
guard is not a zero-warning result. Existing source documents, metadata and twelve
source images are preserved. No production work for this batch has been claimed
as complete by this task.
