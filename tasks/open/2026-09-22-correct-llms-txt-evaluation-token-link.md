---
id: 2026-09-22-correct-llms-txt-evaluation-token-link
title: Correct llms.txt evaluation token link semantics after localization draft
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-09-22T05:44:07Z
completed_at:
branch:
depends_on:
  - 2026-09-22-localize-llms-txt-evaluation-draft-only
scope:
  - tasks/open/2026-09-22-correct-llms-txt-evaluation-token-link.md
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

- [ ] A future editor independently decides whether the inline should be plain
      text, use different linked text, or target another published article.
- [ ] Any approved source correction updates zh-TW first and rebinds every
      affected locale and review artifact.
- [ ] The duplicate-topic publication exclusion for `llms-txt-evaluation`
      remains in force unless separately reviewed and authorized.

## Steps

- [ ] Claim a new narrow pack/editorial scope after the batch016 draft task is
      complete; do not extend this placeholder's task-file-only scope.
- [ ] Review the surrounding Lighthouse sentence and the intended destination.
- [ ] Apply the approved source-first correction and repeat localization review.

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
