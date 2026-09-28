---
id: 2026-09-28-correct-wordpress-blog-build-source-inline
title: Correct WordPress blog-build source inline
status: review
priority: P2
area: docs
owner: codex-batch033
claimed_at: 2026-09-28T02:19:14Z
created_at: 2026-09-28T02:19:08Z
completed_at:
branch: codex/wordpress-blog-build-source-inline
depends_on: []
scope:
  - apps/api/app/guides/content/wordpress-blog-build.json
---

# Correct WordPress blog-build source inline

## Why

The public zh-TW v4 `wordpress-blog-build` article links the ordinary verb
`標記` in block 5, inline 1 to the AI glossary entry `ai-term-token`. It is
not a reference to tokens; clicking it sends readers to an unrelated article.
Batch033's four new locales already use plain text here, but their import is
blocked until the published source is corrected and their baseline rebound.

## Definition of done

- [x] This one inline is plain text with the same visible word, and no other
      pack content, metadata or locale changes.
- [x] Local lint and relevant link/content tests pass; the source-only diff is
      reviewable in its own PR. Publication and Batch033 rebind are separate.

## Steps

- [x] Claim the exact source pack path on a branch from latest main.
- [x] Replace the mistaken inline without changing the visible sentence.
- [x] Verify the minimal diff, new normalized source hash, lint and tests.
- [x] Open source-only draft PR and leave the task in review.

## How to verify

Run `uv run python -m app.guides.pack_cli lint --slug wordpress-blog-build`
from `apps/api`, `uv run pytest tests/test_guides_content_links.py
tests/test_guides_links.py`, `npm run check:tasks` and `git diff --check`.
Programmatically compare the original and corrected pack while normalizing
only block 5, inline 1 to prove that every other field is identical.

## Notes

Started from `origin/main` 2fa7bf1e. At task start the pack has only zh-TW;
its GuideDocument-normalized SHA-256 equals public v4
`e90738e066cae12a93dacf5d40ce4eb37993078b8eb61c12311cf8f786592189`.
Expected change:
`{"type":"article","text":"標記","kind":"life","slug":"ai-term-token"}`
to `{"type":"text","text":"標記"}` at
`locales.zh-TW.blocks[5].inlines[1]`. Batch033 draft PR #882 must not be
merged or imported until this correction is published and its source pin is
rebound. No production write is part of this task.

The corrected GuideDocument-normalized SHA-256 is
`7635cdee0e7c8cca6492be45d552ae88828f9899feea78a41e270ad4c5d176c8`.
A structural comparison against `origin/main` proved the changed inline is
the only JSON difference. Pack lint passed with the existing no-summary
advisory; content-link and guide-link tests passed (9 passed, 6 skipped).
`npm run check:tasks` and `git diff --check` passed.
Draft source-only PR: https://github.com/x812033727/travel_scanner/pull/883.
No merge, deployment or publication has occurred; move this task to done
only after the correction is merged.
