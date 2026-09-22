---
id: 2026-09-22-localize-four-website-basics-guides-batch018
title: Localize four website basics guides batch018
status: in-progress
priority: P1
area: docs
owner: codex-batch018
claimed_at: 2026-09-22T09:41:01Z
created_at: 2026-09-22T09:40:59Z
completed_at:
branch: codex/article-localization-batch018-web-basics
depends_on: []
scope:
  - apps/api/app/guides/content/domain-registration-guide.json
  - apps/api/app/guides/content/hosting-types-explained.json
  - apps/api/app/guides/content/website-cms-choice.json
  - apps/api/app/guides/content/website-maintenance-routine.json
  - apps/web/public/guides/domain-registration-guide
  - apps/web/public/guides/hosting-types-explained
  - apps/web/public/guides/website-cms-choice
  - apps/web/public/guides/website-maintenance-routine
---

# Localize four website basics guides batch018

## Why

Four original-626 website basics articles are publicly available only in zh-TW.
Add complete en, ja, ko and zh-CN documents and matching text-bearing hero and
inline diagrams, preserving source versions, metadata, code, URLs and credits.

## Definition of done

- [x] Read-only inventory identifies four public source articles and missing locales;
      source draft/latest/published documents match and repository source is equivalent.
- [ ] Revalidate source/editorial concerns and preserve all existing zh-TW edits.
- [ ] Independently review sixteen full translations, including all 26 blocks and
      three sources per document, applicability, numeric values and protected tokens.
- [ ] Localize eight source SVGs into 32 SVGs and render sixteen localized hero JPGs;
      independently inspect all assets on desktop and mobile without text overflow.
- [ ] Integrate only reviewed documents and locale-suffixed images; preserve four
      existing source documents, all metadata, original images and publication state.
- [ ] Scoped article-pack checks, relevant tests, task check and CI pass.
- [ ] Open a batch PR with exact content/asset/version evidence.
- [ ] After review and merge, guarded backup/deployment/dry-run/import/publication
      and five-language desktop/mobile/canonical/hreflang/link verification pass.

## Steps

- [x] Select domain-registration-guide, hosting-types-explained, website-cms-choice
      and website-maintenance-routine with no active-scope or open-PR overlap.
- [x] Create isolated worktree and normally claim the exact eight content/image paths.
- [ ] Draft complete documents and assets outside Git; freeze and independently review.
- [ ] Integrate, validate and open PR; bind final Git model and image bytes.
- [ ] Complete canonical missing-language-only release and record per-article acceptance.

## How to verify

Use the isolated API runtime and run `python -m app.guides.pack_cli lint --slug`
for each exact slug, `npm run check:tasks` and `git diff --check`. Verify every
protected field and image reference against the pinned source; perform independent
full-body and actual rendered image review, then guarded canonical publisher tests
and production browser acceptance before marking this task done.

## Notes

Selection evidence is outside Git under
`C:/Users/x8120/.codex/article-localization-release/batch018-inventory/`.
`selection-receipt.json` SHA256
`f93e14a1df4bedeca4ae3bf30eeafb253ff959c21e7a0e30a18779fd2394afe8`.
Fresh live snapshot at 2026-09-22T09:14:33Z has SHA256
`96378db975386a6bb14de494167610446bf4fe0e01206f43f1e641b8baf87d76`.
All four articles are active and published at article v2, zh-TW locale v4, with
no expiry and no unpublished live draft difference. Worktree starts at
`9fafd4293506a264dfe54c3722cb2c2eac86b516`; the dimensions-tool merge changes none
of these sources. No publication or completed translation is claimed by this task.
