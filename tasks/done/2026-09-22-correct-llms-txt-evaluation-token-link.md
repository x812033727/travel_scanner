---
id: 2026-09-22-correct-llms-txt-evaluation-token-link
title: Correct llms.txt evaluation token link semantics after localization draft
status: done
priority: P2
area: docs
owner: claude-opus-5-5
claimed_at: 2026-10-01T12:36:30Z
created_at: 2026-09-22T05:44:07Z
completed_at: 2026-10-01T12:37:11Z
branch: claude/llms-txt-token-link
depends_on:
  - 2026-09-22-localize-llms-txt-evaluation-draft-only
scope:
  - apps/api/app/guides/content/llms-txt-evaluation.json
---

# Correct llms.txt evaluation token link semantics after localization draft

## Why

In the repository-only zh-TW source for `llms-txt-evaluation`,
`/blocks/21/inlines/1` uses the ordinary verb `標記` while its
`ArticleInline` points to `ai-term-token`. The visible word means that
Lighthouse flags a server error; the linked article identity instead names a
token glossary entry. The localization draft must preserve the frozen source,
so this semantic source issue needs a separate editorial decision later.

## Definition of done

- [x] A future editor independently decides whether the inline should be plain
      text, use different linked text, or target another published article.
- [x] Any approved source correction updates zh-TW first and rebinds every
      affected locale and review artifact.
- [x] The duplicate-topic publication exclusion for `llms-txt-evaluation`
      remains in force unless separately reviewed and authorized.

## Steps

- [x] Claim a new narrow pack/editorial scope after the batch016 draft task is
      complete; do not extend this placeholder's task-file-only scope.
- [x] Review the surrounding Lighthouse sentence and the intended destination.
- [x] Apply the approved source-first correction and repeat localization review.

## How to verify

Compare the final zh-TW `ArticleInline` kind, slug and visible text against the
reviewed correction receipt, then verify all localized documents carry the
same identity and intended meaning.

## Notes

- This task is deliberately unclaimed and depends on
  `2026-09-22-localize-llms-txt-evaluation-draft-only`.
- Batch016 translations retain the source `kind: life`,
  `slug: ai-term-token` and translate only the visible verb in context.
- Do not modify the original zh-TW document inside the localization draft.
- 2026-10-01 (claude-opus-5-5): decision: plain text. The sentence says Lighthouse flags a
  server error; "標記" there is a verb, and no published article explains Lighthouse
  flags, so there is no better destination. `/blocks/21/inlines/1` is now a text inline
  with the same visible word in all five locales (標記 / flagged / 警告の対象 /
  문제로 표시 / 标记). A script restored the five original inlines and asserted equality
  with the original pack. Scope moved from this task file to the pack. `pack_cli lint`
  0 errors. The batch016 localization receipts are historical records of the frozen
  source and were not rewritten. Nothing was imported or published: the
  duplicate-topic publication exclusion for `llms-txt-evaluation` still stands.
