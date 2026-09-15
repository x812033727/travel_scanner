---
id: 2026-09-14-answer-first-howto-descriptions
title: AIO: 68 how-to descriptions enumerate topics instead of answering
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-14T13:48:24Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/guides/content
---

# AIO: 68 how-to descriptions enumerate topics instead of answering

## Why

`description` is what an AI answer engine quotes when it summarizes a page, and 68 of the
site's descriptions assert nothing it can lift.

Measured across all 498 localized documents: 72 descriptions are a single sentence containing
three or more `、` separators — a noun-phrase list with no predicate — and 60 of those are
`howto`, plus 8 `intel`. `seoul-subway-t-money-guide`'s 235-character description enumerates
「計費方式、30 分鐘免費轉乘規則、T-money 在哪裡買、怎麼儲值與退款」 and states no fact.

These are the fare-and-timetable pages where the site has its highest-value numbers and its
densest citations (howto carries a median of 19 sources), so they are exactly the pages losing
the extraction. The fix is cheap because the answer is already one block below: every document
opens with a paragraph, and the howto first paragraphs are already answer-first.

## Definition of done

- [ ] Each rewritten description opens with a one-sentence answer carrying the number, then the
      enumeration, then the provenance clause these descriptions already use.
- [ ] No fact is introduced that the article body does not already state and source.

## Steps

- [ ] Select the targets by the measured rule: splits into exactly one sentence on
      `/(?<=[。.])/` **and** contains at least three `、`. That is the 60 howto + 8 intel.
- [ ] Rewrite by hand, lifting the lead from the document's own first paragraph.
- [ ] Split the work by kind or destination so one task does not hold all of
      `apps/api/app/guides/content` — several models work the same queue.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_guides_content_pack.py
```

Spot-check that the new first sentence matches a number the body states and a source backs.

## Notes

**Do not automate the rewrite.** A generated first sentence that states a fare wrongly is the
one failure mode worse than a teaser: it is the sentence an answer engine caches and repeats.

Changing `description` changes both the meta description and the JSON-LD `description`, so this
is a live SEO change on 68 pages, not a silent one. The facts being promoted — fares, minutes —
are also the most perishable content on the site.
