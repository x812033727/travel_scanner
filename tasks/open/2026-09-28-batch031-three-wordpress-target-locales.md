---
id: 2026-09-28-batch031-three-wordpress-target-locales
title: Batch031 three WordPress target language drafts
status: review
priority: P1
area: docs
owner: codex-batch031-content-draft
claimed_at: 2026-09-28T01:09:20Z
created_at: 2026-09-28T01:09:10Z
completed_at:
branch: codex/batch031-content-draft
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-member-registration.json
  - apps/api/app/guides/content/wordpress-security-basics.json
  - apps/api/app/guides/content/wordpress-social-login.json
  - apps/web/public/guides/wordpress-member-registration
  - apps/web/public/guides/wordpress-security-basics
  - apps/web/public/guides/wordpress-social-login
  - docs/article-localization/batch031-content-draft-evidence.md
  - tasks/open/2026-09-28-batch031-three-wordpress-target-locales.md
---

# Batch031 three WordPress target language drafts

## Why

These three public WordPress guides have a published zh-TW source, but their
en, ja, ko, and zh-CN documents and localized diagram/cover assets remain in
separate Batch031 Pair A/B commits. Integrate their reviewed content into a
draft code PR while preserving the existing zh-TW source and public state.

## Definition of done

- [x] Each of the three packs contains the existing zh-TW document unchanged
      plus four complete target-language documents.
- [x] Exactly 36 localized assets are added; original assets remain unchanged.
- [x] A draft PR records exact source and asset hashes, checks, and publication
      gates. No deployment, database import, or publication occurs.

## Steps

- [x] Claim the narrow three-pack and three-asset-directory scope.
- [x] Bring in Pair A/B content without cherry-picking their unrelated task files.
- [x] Recheck the 12 target documents and 36 assets against Pair commits and
      inspect native-size visual renders.
- [x] Run pack lint, focused API checks, task checks, and exact diff review.
- [x] Open draft PR #879 and keep the source-publication gate explicit.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --kind life --slug` for each
article in `apps/api`, focused guide tests, `npm run check:tasks`, and
`git diff --check`. Compare the four target-locale JSON documents and twelve
localized asset hashes per article to Pair A/B commit blobs.

## Notes

Pair A commit `b885927df5ee0bc6a13b1a1e93b9457eaa3dba3f` supplies
`wordpress-member-registration` and `wordpress-security-basics`; Pair B
commit `e8fa87d9abb0969a5c9861e5b0b551757cd47ba6` supplies
`wordpress-social-login`. `wordpress-user-roles` is excluded because the
active #875 source-correction task owns that pack until its source revision is
published and its task is released/done. This code PR must not imply any
target locale is live.

The three packs and 36 assets match Pair Git blobs exactly. Pack lint found
zero errors; 78 focused API tests passed with seven skips. All 24 SVGs parsed,
all 12 JPGs decoded at 1600×900, and twelve four-locale contact sheets were
visually checked. See `docs/article-localization/batch031-content-draft-evidence.md`
for the complete document and asset hashes. Rebased on merged #875 at
`4b6c5cd99fa9eab3b658d5b6cf639cb001f8fc3e`; repeated source, target,
asset, task, and diff checks against that exact base.
