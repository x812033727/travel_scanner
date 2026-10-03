---
id: 2026-09-28-correct-unrelated-ai-term-links-in
title: Correct unrelated AI term links in two WordPress source guides
status: done
priority: P2
area: docs
owner: codex-source-ticket-cleanup-20261003
claimed_at: 2026-10-03T09:21:01Z
created_at: 2026-09-28T03:31:36Z
completed_at: 2026-10-03T09:21:25Z
branch: codex/unfinished-tickets-20261003
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-map-form-embeds.json
  - apps/api/app/guides/content/wordpress-multilingual-site.json
---

# Correct unrelated AI term links in two WordPress source guides

## Why

The map guide links its map marker (「地圖標記」) to the unrelated AI token glossary.
The multilingual-site guide does the same for an SEO markup tag (「標記」).
These links send readers away from the WordPress instructions and would also be
carried into the next four-language localization batch.

## Definition of done

- [x] Both visible 「標記」 terms remain in the Traditional Chinese source without
      the unrelated AI glossary link.
- [x] Every other source field, article identity, original image and locale stays unchanged.

## Steps

- [x] Change only `wordpress-map-form-embeds` block 3 inline 1.
- [x] Change only `wordpress-multilingual-site` block 16 inline 1.
- [x] Review the exact document-model diff and run scoped checks.
- [x] Open a draft PR; database publication is a separate guarded release.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --kind life --slug` for each
slug from `apps/api`, focused guide-pack tests, and `npm run check:tasks`.
Compare each edited `GuideDocument` with `origin/main`: exactly one inline
changes from `ArticleInline` to `text`, with the same visible word.

## Notes

Source baseline: GitHub main `ec383889f6d5ae582d07c350b5755899300aa4e7`.
The 2026-09-27 read-only production snapshot had article v2 / zh-TW v4 for
both guides, but current production revisions must be recaptured before any
publication. The Batch034 target-language documents must bind to the source
revision that is actually published, not only to this merged pack.

The exact parsed-pack comparison against `origin/main` passed for both files:
only the specified inline changed from `{type: article, kind: life,
slug: ai-term-token, text: 標記}` to `{type: text, text: 標記}`. The corrected
zh-TW `GuideDocument` model SHA-256 values are
`6cff3eb9594c0c72d8cd062d00120f680c2294c7366d15b0edeb75878711f97c`
for `wordpress-map-form-embeds` and
`6e2ee09c0eba9d01539a0d583ac27ddee47fc8cff5ee77febf9712f22f5de88f`
for `wordpress-multilingual-site`. Each scoped pack lint checked one entry
with only the existing `no_summary` advisory. Focused guide-pack/link tests:
12 passed, 5 skipped. `npm run check:tasks` passed with pre-existing stale
claim/overlap warnings; `git diff --check` passed.

Draft PR: https://github.com/x812033727/travel_scanner/pull/887 . It remains
in review; this task is not done until the source correction is merged.

### 2026-10-03 source-only task closure

- PR #887 merged on 2026-09-28T04:28:35Z as
  `dd1d51730c0c46698325fb357bb90ac0303d7b8c`, an ancestor of checked main
  `5af4ffebfcea96fd23b387288901e513ed63d4f7`. Both source-only acceptance
  conditions are complete; the review status was left behind after merge.
- Main still has `{type: text, text: 標記}` at map-form-embeds
  `/locales/zh-TW/blocks/3/inlines/1` and multilingual-site
  `/locales/zh-TW/blocks/16/inlines/1`. Both complete pack blobs are identical
  to the correction merge. Current raw Git pack SHA-256 values are:
  - `wordpress-map-form-embeds`:
    `03486c9cb2a460e7dcd0b512f11fad0d523dac48bed32c7521b5c4784edc1dc7`.
  - `wordpress-multilingual-site`:
    `0a8d905ace0f3a6d6c4877a470193740fd5eb7ee9dd23db0f3410caebd09d68a`.
  These are raw pack hashes, not fresh production or normalized source hashes.
- Fresh read-only checks found no open PR on these scopes, no remote original
  branch and no registered worktree for it; the residual local branch has the
  merged PR head. Normal claim succeeded without `--force`.
- Only this task metadata is being closed. No packs, host data, import, approval
  or publication were changed. Guarded source publication and Batch034 source
  rebind remain separate work; their task states are unchanged. Historical
  production captures and validation results above are not new live evidence.
- Archival diagnostic: normal `done` returned exit 1 because the open copy
  remained after writing the completed record. The coordinating agent checked
  exact path, ID, status, owner, equal bodies and the completed-file SHA-256,
  then removed only this stale open copy with its native PowerShell helper.
  The completed bytes were unchanged by removal; this note was appended later.
  This archival cleanup does not publish either source or rebind Batch034.
