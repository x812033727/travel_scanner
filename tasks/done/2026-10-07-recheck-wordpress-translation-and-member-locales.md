---
id: 2026-10-07-recheck-wordpress-translation-and-member-locales
title: Recheck WordPress translation and member locales
status: done
priority: P2
area: docs
owner: codex-article-localization-4e16
claimed_at: 2026-10-07T05:49:09Z
created_at: 2026-10-07T05:49:08Z
completed_at: 2026-10-07T06:11:07Z
branch: codex/article-missing-locales-20261007
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-plugin-theme-translation.json
  - apps/api/app/guides/content/wordpress-member-registration.json
  - apps/web/public/guides/wordpress-plugin-theme-translation
  - apps/web/public/guides/wordpress-member-registration
  - docs/article-localization/wordpress-translation-member-review-20261007.md
---

# Recheck WordPress translation and member locales

## Why

Two source-valid published life articles already have complete unpublished four-language translations and localized images. Independently review their present content before reuse, preserving published source facts and avoiding duplicate translation calls.

## Definition of done

- [x] Both articles have current independent en/ja/ko/zh-CN review receipts, with the exact plugin-guide and same-cohort member-link corrections applied by distinct executors.
- [x] Both published zh-TW sources, complete root metadata and all thirty assets remain unchanged; only approved target leaves changed.
- [x] Scoped evidence and task notes are ready for a prospective content PR; production release remains separate.

## Steps

- [x] Verify retained production source/target state and absence of holds, aliases or overlapping task/worktree/open-PR scope.
- [x] Read all ten full documents and twelve current cited primary-source pages; verify ArticleInline target kinds, publication state and public title labels.
- [x] Render and inspect sixteen target SVGs and eight actual target hero JPGs, checking text fit, glyphs and visual meaning.
- [x] Record eight exact mandatory corrections and prepare a pinned distinct-executor script outside the repository.
- [x] Root applies the eight exact plugin-guide leaves and four prospective cohort member-security labels; independently reconstruct both final packs and emit current route-b receipts.
- [x] Run scoped lints, task and whitespace checks, then hand off the sanitized evidence and content hashes.

## How to verify

Use the external pinned review inputs and correction script, then independently compare every reviewed leaf, both source documents, complete root metadata and all existing asset hashes. Validate ArticlePack/GuideDocument schemas; run `python -m app.guides.pack_cli lint --slug` for both slugs, `npm run check:tasks` and scoped `git diff --check`.

## Notes

Retained production capture: 2026-10-07T04:45:46.904711Z. Both zh-TW v4 sources match the repository and the four target locale rows are absent. Shared-scope audit found no overlapping current claim, open PR or active translation worktree. Prior authored/integrated translation work is complete: Batch034 #889 for the plugin-theme guide and Pair A `b885927df5ee0bc6a13b1a1e93b9457eaa3dba3f` / Batch031 #879 for the member guide. Original authorship evidence is retained separately from this new independent review.

The plugin guide requires four published website-backup title labels and four final sentences at `/locales/{locale}/blocks/24/text` to be corrected. The source's compound `搜尋取代` means search-and-replace; old translations mistakenly treat broad search as a substitute for direct code edits and omit replacement, reversing the practical warning. Correct only the last sentence to explicitly avoid bulk search-and-replace directly altering code. The member guide has no mandatory text findings. Twelve related target locales remain unpublished and keep legitimate plain-text resolver behavior; recheck their title labels if those targets become public before release.

Findings SHA256 `c65be20e6b521bc9db3fc8c75f33d036cb9357bf2ccf9d9f925521d107f24326`; original current-review evidence SHA256 `5404df343369d4cecac5069dd1ca3753b4831db39f8e95e3e1a74e3d6d60fccf`. The original plugin documents are `CORRECTIONS_REQUIRED`, not PASS. Reviewer will not apply content edits; root is the distinct executor.

## Final cohort review, 2026-10-07

Current independent final review at 2026-10-07T05:57:52.724199+00:00 verifies this task's
exact current content, unchanged source/root metadata/assets and all same-cohort
terminal link labels. Combined 32-row route-b receipt SHA-256
`87986003cd9e266df5e569270ab3d2859f1573433d5c0f1d967c331e1969beaa`; common evidence SHA-256
`d6e10b7546c48b0cdd76c0c03517c6d8ba0a2c0a84a99462ada3e6ed74e91527`.
Use only the immutable external `reuse-t1/life-cohort-final-review-v2` receipts.
All current eight life-pack lints exited 0; no production publication is claimed.
The prospective content PR must freeze exact committed blobs separately.

The earlier statement that the member guide needed no edit referred to full body review before the first cohort was selected. The final cohort includes WordPress security: four member terminal labels now equal its reviewed final locale titles. Application receipts: plugin eight leaves `e953b51bb9fba74e489c64b2fe24b8e288b766503a06c219d488ab8576a354ce`; cohort twelve labels `187056b45c3f53f556f5e2f74ddeb48af94c5ddb9d935d1f3493dbcea523a42d`. The independent reviewer applied no content correction.

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
