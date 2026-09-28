---
id: 2026-09-28-batch042-pair-a-install-reviewed-locales
title: Install reviewed Batch042 search-intent and content-quality locales
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T18:01:55Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/seo-search-intent.json
  - apps/api/app/guides/content/seo-content-quality.json
---

# Install reviewed Batch042 search-intent and content-quality locales

## Why

Eight complete independently reviewed translations are external. Do not claim or edit either JSON until #942 merges and its source task releases the scope.

## Definition of done

- [ ] Verify #942 merge, task closure and exact main source hashes.
- [ ] Claim the two paths and install only the missing four locales, refusing intervening edits.
- [ ] Preserve original zh-TW and root metadata and prove rerun unchanged.
- [ ] Bind installed LF bytes/assets to the final independent review and local previews.
- [ ] Pass scoped lint/API/task checks; retain inherited strict-intake findings in follow-up tasks.
- [ ] Update PR #946 and separate guarded release tasks.

## How to verify

Use exact source/candidate hashes in docs/article-localization/batch042-pair-a-evidence.md and the guarded installer. Current-head CI must pass before ordinary merge; no local preview establishes live acceptance.

## Notes

Leave unclaimed until #942 merges. Corrected source hashes are 420e80f7c483ac21c1d3a5c9803e8daee846dd5e60c687e48354bb23d695f0ab and aa8e6b95b373ec4f2fab13e9a99798173532541c760407cf07daf259b229880f. Target-language related reading remains non-clickable until actual publication is verified. No database import/publication belongs to this task.
