---
id: 2026-09-28-batch042-pair-b-install-reviewed-locales
title: Install reviewed Batch042 technical SEO and roadmap locales
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T17:57:31Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/technical-seo-checklist.json
  - apps/api/app/guides/content/seo-learning-roadmap.json
---

# Install reviewed Batch042 technical SEO and roadmap locales

## Why

Eight independently reviewed translations exist outside the repository. Source PR #942 must merge and release its scopes before this task may claim or modify either article JSON.

## Definition of done

- [ ] Verify merged #942 source task is done and exact main hashes match the reviewed source.
- [ ] Claim only the two JSON paths, refuse intervening edits, and install four missing locales per pack.
- [ ] Preserve existing zh-TW and root metadata and prove rerun unchanged.
- [ ] Bind installed LF bytes to reviewed candidates/assets and pass scoped pack lint/API checks.
- [ ] Keep strict inherited editorial failures explicit, record follow-up and release tasks, and update the draft PR/evidence.

## How to verify

Compare both exact source/candidate hashes with docs/article-localization/batch042-pair-b-evidence.md; use the guarded reviewed installer and confirm current-head CI. Standalone local previews are not live acceptance.

## Notes

Leave unclaimed until #942 merges. Corrected source hashes are a5f692c99703c5b15e683fd4543d7438c6179d46042f8336f8abaee6cdcc5e08 and 5d4d982e675e03e7cf3b9840e5ce26488bf7dbc8f54a40f75c7113fdd7635dd5. No database import or publishing belongs to this task.
