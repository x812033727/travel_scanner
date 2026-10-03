---
id: 2026-09-28-correct-wordpress-blog-build-source-inline
title: Correct WordPress blog-build source inline
status: done
priority: P2
area: docs
owner: codex-source-ticket-cleanup-20261003
claimed_at: 2026-10-03T09:18:49Z
created_at: 2026-09-28T02:19:08Z
completed_at: 2026-10-03T09:19:21Z
branch: codex/unfinished-tickets-20261003
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

### 2026-10-03 source-only task closure

- PR #883 merged on 2026-09-28T02:52:04Z as
  `4f9335b0b5f7f4f912aadf53e4565fd033c18acc`, an ancestor of checked main
  `5af4ffebfcea96fd23b387288901e513ed63d4f7`. The source-only acceptance
  conditions above are complete; the prior review status was not updated after merge.
- On that main, `/locales/zh-TW/blocks/5/inlines/1` is still exactly
  `{type: text, text: 標記}`. The complete zh-TW document matches the correction
  merge; only the four later translations make the full pack differ.
- Current Git pack SHA-256:
  `03bb0e4e8147a1b6ab05388f0657504f78a6f0dcd6b2b908020ddd50180d9032`.
  This is the raw Git pack hash, not a new normalized source hash or live hash.
- Fresh read-only checks found no open PR on this scope, no remote copy of the
  original branch and no registered worktree for it. The residual local branch
  retains the correction pack. Normal claim succeeded without `--force`.
- This closure changes task metadata only. No article, production data, approval,
  import or publication was changed or checked on the host. Publication and
  Batch033 source rebind remain separate work; their task states are unchanged.
  Historical hashes and validation results above remain historical evidence.
- Archival diagnostic: normal `done` wrote the completed record but returned
  exit 1 because the open copy remained. The coordinating agent then verified
  exact paths, IDs, statuses, owner, equal bodies and the completed-file SHA-256
  before removing only that stale open copy with native PowerShell. The completed
  bytes remained unchanged by that removal; this note was appended afterward.
