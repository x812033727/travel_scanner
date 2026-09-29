---
id: 2026-09-28-review-batch043-inherited-editorial-intake-failures
title: Review Batch043 inherited editorial intake failures
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-28T17:12:04Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content/google-ranking-history.json
  - apps/api/app/guides/content/google-trends-research.json
  - apps/api/app/guides/content/search-results-clickthrough.json
  - apps/api/app/guides/content/semrush-research-workflow.json
---

# Review Batch043 inherited editorial intake failures

## Why

The four Batch043 published zh-TW sources each fail the stricter content-pipeline intake checker on two existing editorial rules: the first block is a paragraph instead of `summary`, and the combined description/body contains two self-references (`本文`/`這篇`) instead of at most one. This predates the translations: the source documents compare unchanged against the pinned production receipt and repository main. Pack lint treats the missing summary as an advisory, but intake returns exit 1.

## Definition of done

- [ ] Decide and document the editorial treatment for all four source articles; preserve full meaning and synchronized translations.
- [ ] Any source revision follows a separate version/hash-controlled source-correction workflow, with no silent production overwrite.

## Steps

- [ ] Wait for the Batch043 localization PRs and check their current source and target hashes before claiming these same paths.
- [ ] Review the paragraph-to-summary structure and repeated self-references without reducing content to meet an optional length hint.
- [ ] If revisions are needed, update and independently review all affected locales, reconcile source versions, and rerun intake, pack lint and content tests.

## How to verify

Run `.agents/skills/content-pipeline/scripts/intake_check.py --slug <slug> --from-content` for `google-ranking-history`, `google-trends-research`, `search-results-clickthrough`, and `semrush-research-workflow` using the API venv. Each currently reports the same two source-only failures; article references and diagram numbers pass. See Batch043 pair evidence for exact source locks and reviewed translations.

## Notes

Keep this ticket unclaimed while the localization scopes are active. The user explicitly required preserving the existing complete source bodies, so these inherited editorial issues were recorded rather than silently edited during translation. No source or production changes were made to address them. Translation schema tests passing is not a claim that this stricter editorial intake passed.
