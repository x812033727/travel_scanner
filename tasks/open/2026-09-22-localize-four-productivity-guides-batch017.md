---
id: 2026-09-22-localize-four-productivity-guides-batch017
title: Localize four productivity guides batch017
status: review
priority: P1
area: docs
owner: codex-batch017
claimed_at: 2026-09-22T08:32:10Z
created_at: 2026-09-22T08:32:08Z
completed_at:
branch: codex/article-localization-batch017-productivity
depends_on: []
scope:
  - apps/api/app/guides/content/email-triage-three-actions.json
  - apps/api/app/guides/content/meeting-notes-action-template.json
  - apps/api/app/guides/content/notification-focus-boundaries.json
  - apps/api/app/guides/content/weekly-review-reset-routine.json
  - apps/web/public/guides/email-triage-three-actions
  - apps/web/public/guides/meeting-notes-action-template
  - apps/web/public/guides/notification-focus-boundaries
  - apps/web/public/guides/weekly-review-reset-routine
---

# Localize four productivity guides batch017

## Why

These four original-626 productivity guides are published only in zh-TW. Add
complete English, Japanese, Korean, and Simplified Chinese documents and one
localized diagram per new locale while keeping the published zh-TW document,
metadata, sources, and existing image bytes unchanged.

## Definition of done

- [x] Fresh read-only production evidence proves each published zh-TW document
      equals the repository source and each article is missing exactly en, ja,
      ko, and zh-CN.
- [x] Sixteen complete GuideDocuments pass independent editorial review.
- [x] Sixteen localized diagrams preserve all 19 source text nodes, bind their
      accessible title and description to the reviewed document, and pass
      independent desktop and actual mobile-pan visual review.
- [x] The four packs contain exactly five locales, retain the original zh-TW and
      pack metadata byte-for-model, and reference only their locale-suffixed
      diagrams.
- [x] Scoped pack lint, structural/protected-field/numeric/link audits,
      repository task checks, and a final diff review pass.
- [ ] A reviewable draft pull request is opened with the exact Git bytes and
      evidence attached. Import and publication remain separate release work.

## Steps

- [x] Pin repo commit/tree, raw packs/assets, and the fresh live documents.
- [x] Draft and independently review all sixteen localized documents.
- [x] Author and render all sixteen localized SVGs outside the repository.
- [x] Receive independent asset/content/layout review and apply only approved
      files to this claimed scope.
- [x] Run scoped validation and freeze exact working-tree evidence.
- [ ] Open a draft PR after the exact Git bytes are independently bound.

## How to verify

```powershell
$env:PYTHONPATH = "$PWD\apps\api"
& C:\Users\x8120\.codex\article-localization-release\runtime-api-20260922\Scripts\python.exe `
  -m app.guides.pack_cli lint --slug email-triage-three-actions
# Repeat pack_cli lint for the other three slugs.
npm run check:tasks
git diff --check
```

The batch audit also verifies all 15 blocks and one source per locale, exact
protected fields, source URLs/dates/credits, ArticleInline identities, diagram
paths, 19 visible SVG labels, and the 01–04 step numbers.

## Notes

- Source pin: repository commit `d5f03e679bef2102e843426c42f045aef4ae08c0`,
  tree `f230962b0db506c9b0e223ebe966ce1bafe0e8fa`; fresh read-only live
  snapshot `batch017-inventory/selected-live-source.json` SHA-256
  `77c7ec140ea803eef2e2435b2c3fef62c4c7e9dccd6846a5c41281c3bf99bd34`.
- Selection/source receipt: `batch017-inventory/selection-receipt.json`
  SHA-256 `7557e99511ce131f3486b1314cce9d1d2f0d879365d92d7778e5d5b9b5cbc1ab`.
- Independent body review index:
  `batch017-productivity/independent-body-review/receipt-index.json` SHA-256
  `95957f4d3b3316d2ec3f7df4b807ee72ec1231eeec54a7574c93e64e3f771b2f`.
- Final uncommitted integration validation:
  `batch017-productivity/final-worktree-validation.json` SHA-256
  `a521fce78f511636e8457ed133e6aa744e60000bd0737eb5a97f8513fee9da77`.
  Independent integration review PASS:
  `batch017-productivity/root-integration-review-pass.json` SHA-256
  `cd77f0127bf5d8f85547795e781952cd2bcf742ade612787b0c06feeadb09a62`.
- The first asset freeze remains preserved as WITHHOLD evidence. The corrected
  author freeze is `batch017-productivity/author-freeze-v2-pending-focused-review.json`
  SHA-256 `0b3a6636684265e23c5c4f62d3bb9ec6c7d21d07f7aebf5de781073fdfb274d3`.
  Independent asset review PASS is
  `batch017-productivity/independent-asset-review/receipt-pass-v3.json`
  SHA-256 `898f331099ebb310c5d2b61a1b6db133c039091c6666d3ce8a5e7a3f34a219e1`.
- A second read-only production snapshot captured at 2026-09-22T09:04:05Z
  confirmed all four articles remain article v1, zh-TW locale v6, published and
  active, with draft/latest/published documents equal and no additional locale.
- The 16 independently approved numeral renderings are translation-format
  equivalences. Do not claim the strict ASCII numeric-token guard passed those
  rows; preserve their explicit independent review evidence.
- Existing non-text hero JPGs are reusable. Keep the original zh-TW SVG and all
  four original hero JPG files unchanged.
- Do not import, publish, deploy, or write production in this task.
