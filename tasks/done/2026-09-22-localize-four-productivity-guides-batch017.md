---
id: 2026-09-22-localize-four-productivity-guides-batch017
title: Localize four productivity guides batch017
status: done
priority: P1
area: docs
owner: codex-batch017
claimed_at: 2026-09-23T07:31:02Z
created_at: 2026-09-22T08:32:08Z
completed_at: 2026-09-23T07:41:13Z
branch: codex/localization-007-017-release-evidence
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

## 2026-09-23 completed release checkpoint

The separately authorized release is complete. [Batch007/017 release record](../../docs/article-localization/releases/batch007-017/README.md)
lists every article and five public URLs; its compact evidence index pins the
external full receipts. Earlier HOLD and outstanding notes below are historical
checkpoints and do not override this completed release result.

- [x] PR #659 merged after all eight exact-head CI checks passed; final Git-bound
  release expectations and required preservation reviews were accepted.
- [x] All 16 missing en/ja/ko/zh-CN documents in Batch017 were imported and
  published on 2026-09-23; all four pre-existing zh-TW rows and article metadata
  remain unchanged.
- [x] All 20 public URLs in this batch passed five-language desktop/mobile
  browser, body/image, canonical/hreflang, link and expanded-description/source
  checks, with independent screenshot review.
- [x] A fresh verified backup preceded publication; the existing deployed
  `6b2339ec89eda90ad37c9e99009723dfca89ba4a` was adopted without redeployment or
  application restart. Final acceptance cleared the release hold; the subsequent
  read-only snapshot confirmed a clean same-revision host and three HTTP 200
  health responses.

Final evidence SHA256:
`8aaa3d308786e1d8486fed7940330f681ece154964d7d0522c0f48161e13d4ec`.
Final acceptance SHA256:
`933c778a81f70205f70927798283744c4eb7da1bdc42b253c9295c6a000fec56`.
Post-clear host evidence SHA256:
`1d607d92816b1d73c63a265c8aeb116c83b56c75a44da981fe2629874c3e3b51`.
The existing global search-placeholder icon issue remains tracked separately;
this completion does not cover the remaining site-wide localization backlog.

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
- [x] A reviewable draft pull request is opened with the exact Git bytes and
      evidence attached. Import and publication remain separate release work.

## Steps

- [x] Pin repo commit/tree, raw packs/assets, and the fresh live documents.
- [x] Draft and independently review all sixteen localized documents.
- [x] Author and render all sixteen localized SVGs outside the repository.
- [x] Receive independent asset/content/layout review and apply only approved
      files to this claimed scope.
- [x] Run scoped validation and freeze exact working-tree evidence.
- [x] Open draft PR #659 after the initial exact Git bytes were independently
      bound; later review identified and independently closed the AI disclosure
      translation gap before the required strict-main refresh.

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
- Root's first canonical-wrapper review correctly put the batch on HOLD because
  all 16 target documents retained two Traditional Chinese, reader-visible AI
  disclosure leaves. The HOLD receipt is
  `batch017-productivity/root-wrapper-review-HOLD-ai-disclosures-20260922.json`
  SHA-256 `5741bed4ef6181c40b20fc635d8f40b97780ae08f0b0945d583310e2c469d057`.
  The exact 32-leaf locale correction passed independent review in
  `batch017-productivity/independent-ai-disclosure-v2-review/receipt-pass.json`
  SHA-256 `859fae9d4f92a2cff778d4b1ceefdfc89751bfc3e052bbb306da097ba554098e`.
  It changes only `hero.credit.author` and `hero.credit.license` for en, ja, ko,
  and zh-CN, preserves Mokaair attribution and AI/non-photographic provenance,
  and removes the 32 copied-disclosure validation errors. Existing approved
  numeric-equivalence warnings remain explicit and are not called strict PASS.
- Do not import, publish, deploy, or write production in this task.
