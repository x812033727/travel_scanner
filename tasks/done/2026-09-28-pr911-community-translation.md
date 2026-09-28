---
id: 2026-09-28-pr911-community-translation
title: Correct community meaning in social planning translation
status: done
priority: P2
area: docs
owner: codex-pr-merge-watch
claimed_at: 2026-09-28T11:38:15Z
created_at: 2026-09-28T11:37:23Z
completed_at: 2026-09-28T11:46:08Z
branch: codex/pr911-community-translation
depends_on: []
scope:
  - apps/api/app/guides/content/social-media-planning.json
  - docs/article-localization/batch037-pair-a-evidence.md
---

# Correct community meaning in social planning translation

## Why

Independent review of PR #911 found that the simplified Chinese social-planning
article changes an existing audience community into a social-media platform. It
also retains one traditional character in otherwise simplified Chinese prose.

## Definition of done

- [x] The two reviewed phrases preserve the source meaning and use simplified Chinese.
- [x] The source document, other locales, metadata, and all artwork remain unchanged.
- [x] Fresh document and pack hashes supplement the original review evidence.

## Steps

- [x] Apply only the two independent-review corrections.
- [x] Validate the exact structural diff, guide schema, and scoped pack lint; check the task board before committing.
- [x] Obtain a follow-up independent review of the changed document and hashes.

## How to verify

Run the focused content audit against PR head
`893ff4adaa862d634b74ea746209ad53f4b089c5`, then scoped
`python -m app.guides.pack_cli lint --kind life --slug social-media-planning`
and `node tools/tasks.mjs check`. The audit must permit only
`/locales/zh-CN/blocks/5/text` and `/locales/zh-CN/blocks/20/text` to change.

## Notes

The owner authorized fixing and merging all open PRs. This is a narrow review
repair in the watcher's isolated branch, not a second localization batch. Before
claiming, the PR author task was in review with every implementation checkbox
complete; its worktree was clean at the exact remote head above. The only scope
overlap is that completed implementation's review claim, so the new repair claim
uses `--force` without changing the author's task or worktree. Recheck the remote
head before a normal fast-forward push and stop if it has advanced.

Independent review read all eight target documents and checked all 24 assets.
Only the two prose corrections are accepted here; optional Korean graphic wording
is already understandable and does not need an unrelated asset change. No
production deployment, import, publication, or external acceptance is claimed.

The exact two-value structural audit and all five document schemas passed. Scoped
pack lint passed with only the existing no-summary and English-length advisories.
The independent follow-up review confirmed both corrected paragraphs and their
new pack/document hashes, with no remaining editorial blocker. Updated hashes
are recorded in the batch evidence supplement; unchanged artwork did not need
another render.
