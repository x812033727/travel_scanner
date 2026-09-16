---
id: 2026-09-14-heading-anchors-for-h3
title: Level-3 headings have no id, so a citation can only ever point at an h2
status: review
priority: P3
area: web
owner: claude-fable-5-1
claimed_at: 2026-09-16T00:00:44Z
created_at: 2026-09-14T13:48:24Z
completed_at:
branch: claude/travel-article-structure-search-sr9jiq
depends_on: []
scope:
  - apps/web/components/content-blocks.tsx
  - apps/web/components/content-blocks.test.tsx
---

# Level-3 headings have no id, so a citation can only ever point at an h2

## Why

An answer engine cites a fragment URL when a page offers one, and that fragment is what turns a
citation into a click. `ContentBlocks` gives `section-N` ids to level-2 headings only; a level-3
heading renders with no id at all. Across the 106 how-to articles alone that is most of the
article's actual sub-answers left unaddressable.

## Definition of done

- [x] Level-3 headings carry a stable id.
- [x] Every existing `#section-N` anchor resolves to byte-identically the same heading.
- [x] The visible table of contents still lists level-2 headings only.

## Steps

- [x] In the heading branch of `ContentBlocks`, add a sub-counter that resets on each level-2,
      giving ids of the form `section-3-2`.
- [x] The sub-counter must hang off the existing global section number, not be a second
      independent sequence — `splitGuideBlocks` passes `headingStart` precisely because a
      renderer that restarted per slice would give two sections the same anchor.
- [x] Gate it on the same `headingStart === undefined` check, so legal pages keep id-free headings.
- [x] Leave `guideHeadings` alone: the contents list stays level-2 only, or it stops being the
      scroll-saver `CONTENTS_MIN_HEADINGS` exists to protect.

## How to verify

```bash
npm run lint:web && npm run typecheck:web && npm run test:web
```

Confirm an article's existing `#section-3` still lands on the same heading.

## Notes

Adds ids to h3 and moves no existing h2 id, so no inbound link breaks. Two sibling h3s with
identical text still get distinct ids because the sub-counter is positional, not slugified.

## Notes

2026-09-16（claude-fable-5-1，隨 `term-link-popover-related-grid-web` 同分支做掉）：`ContentBlocks` 渲染前一次算好 `headingIds`
（h2 `section-N` 沿用既有序列、h3 `section-N-M` 在每個 h2 下歸零；沒有 `headingStart` 時一律無 id）；`guideHeadings` 與目錄不動。
測試：`content-blocks.test.tsx`「numbers level-3 headings within their section」。
