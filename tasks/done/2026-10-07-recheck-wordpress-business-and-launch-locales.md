---
id: 2026-10-07-recheck-wordpress-business-and-launch-locales
title: Recheck WordPress business and launch locales
status: done
priority: P2
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:39:03Z
created_at: 2026-10-07T05:38:43Z
completed_at: 2026-10-07T06:11:06Z
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-business-site.json
  - apps/api/app/guides/content/wordpress-local-to-live.json
  - apps/web/public/guides/wordpress-business-site
  - apps/web/public/guides/wordpress-local-to-live
  - docs/article-localization/wordpress-business-launch-review-20261007.md
---

# Recheck WordPress business and launch locales

## Why

Two source-valid published life articles already have four unpublished translations from batch033. Reuse those documents instead of paying for duplicate translation, but independently recheck their current content and images before preparing a publication bundle.

## Definition of done

- [x] Both articles have current independent review receipts for en, ja, ko and zh-CN after a distinct executor applies the exact mandatory corrections.
- [x] The published zh-TW source, complete root metadata and all existing assets remain unchanged.
- [ ] The reviewed content, evidence and task are frozen for a prospective PR; publication remains a separate release task.

## Steps

- [x] Audit current source equality, absent target rows, publication holds and overlapping work before claiming the narrow scope.
- [x] Read both source documents and all eight translations, verify official sources and actual published related-article titles.
- [x] Render and inspect all sixteen target SVGs and eight actual target JPGs, checking text layout, glyphs and content.
- [x] Record 22 exact mandatory corrections with before/after JSON pointers and evidence outside the repository.
- [x] A distinct executor applies the pinned correction script; the independent reviewer rechecks the final bytes and emits current route-b receipts.
- [x] Record sanitized review evidence in the scoped document and hand the exact content hashes to the release owner.

## How to verify

Use the pinned external review inputs and correction script in the current release evidence directory. After application, compare every changed leaf, reconstruct the unchanged original document, verify source and assets against their reviewed hashes, validate ArticlePack/GuideDocument schemas, and run the two scoped pack lints plus `npm run check:tasks` and `git diff --check`.

## Notes

Current production snapshot captured 2026-10-07T04:45:46.904711Z: both zh-TW sources are published version 4 and match the repository; all four target locale rows are absent, with no hold or alias. Previous authored translation task is `2026-09-28-localize-four-wordpress-growth-and-launch`, owner `codex-batch033`; it is done. No overlapping active task, worktree or open-PR scope was found for these two packs/assets.

The current review requires 20 terminal related-reading labels to match the actual published same-locale titles, one English business-guide caveat to faithfully state that client cases and conversion-rate figures are not invented, and one zh-CN launch-guide technical term (`HTTPS 证书`). Source facts, external links, body structure and all assets pass. The launch guide's HTTPS related target is unpublished in those locales; its ArticleInline may resolve as plain text until that target is public.

The independent reviewer does not apply content corrections. Findings SHA256: `cf06c8ef7cb09aacd85a28d5834c7bb8259412f1497a221012261773cae24b7c`; original review-evidence SHA256: `ac986d8d94c4089b8d083795bacefc37d0a47e6be4bc76569f0b29ca57bbf8da`. The original documents are `CORRECTIONS_REQUIRED`, not PASS. Exact retained local paths are in the external handoff receipt; they are intentionally not treated as Git-bound or deployed artifacts.

Root applied the 22 exact changes as a distinct actor; application receipt SHA256 `1ed51c2f119a7d3b4069d80fb4df993e61fa1222db5aaef3b7ac2e7d64e7b696`. Independent final recheck at 2026-10-07T05:44:37.415737Z passed all eight target documents, exact leaf reconstruction, all source/root metadata values and thirty asset hashes. Current route-b receipt SHA256 `36533099bf9766229d0a1a80c20dd3c0db16095719e4a1a07cbe8f284c1b9a33`; evidence SHA256 `004975b672e9178a5b7a2fc6c579eb75bfeaaf9fbf1a8f4f880fdb98703822fd`. Sanitized evidence and all eight target document hashes are in the scoped review document. No publication or merge is asserted.

Both scoped pack lints exited 0 with only inherited no-summary and English length guidance (6,961 and 6,334 characters). Task validation passed for 1,612 files with existing unrelated stale-claim warnings; scoped `git diff --check` passed.

## Final cohort review, 2026-10-07

Current independent final review at 2026-10-07T05:57:52.724199+00:00 verifies this task's
exact current content, unchanged source/root metadata/assets and all same-cohort
terminal link labels. Combined 32-row route-b receipt SHA-256
`87986003cd9e266df5e569270ab3d2859f1573433d5c0f1d967c331e1969beaa`; common evidence SHA-256
`d6e10b7546c48b0cdd76c0c03517c6d8ba0a2c0a84a99462ada3e6ed74e91527`.
Use only the immutable external `reuse-t1/life-cohort-final-review-v2` receipts.
All current eight life-pack lints exited 0; no production publication is claimed.
The prospective content PR must freeze exact committed blobs separately.

### Content PR handoff

PR: https://github.com/x812033727/travel_scanner/pull/1365.
Authoring, exact independent review, local validation and local installation/replay
are complete for this ticket's selected scope. Required GitHub checks and merge
remain enforced PR gates; marking this authoring ticket done does not claim those
checks are green. The PR remains draft pending owner approval.
Production deployment, publication and public desktop/mobile verification remain
open in 2026-10-07-release-localized-travel-life-wave-20261007.
Any unchecked CI/merge/publication lines above are handed to those explicit gates,
not waived or reported as completed.
