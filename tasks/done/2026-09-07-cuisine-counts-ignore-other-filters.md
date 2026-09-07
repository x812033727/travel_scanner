---
id: 2026-09-07-cuisine-counts-ignore-other-filters
title: Cuisine chip counts ignore the area and keyword already chosen
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T08:02:49Z
created_at: 2026-09-07T02:06:16Z
completed_at: 2026-09-07T08:10:32Z
branch:
depends_on: []
scope:
  - apps/web/components/food-browser.tsx
  - apps/api/app/foods
---

# Cuisine chip counts ignore the area and keyword already chosen

## Why

Measured against production before the fix:

```
/foods/merchants?destination_id=tokyo                     -> sushi 1, seafood 1, ramen 1, dim-sum 1
/foods/merchants?destination_id=tokyo&area=tokyo-shibuya  -> sushi 1, seafood 1, ramen 1, dim-sum 1, total 1
```

Four cuisines each claiming a merchant above a list holding one. `_merchant_facets`
said so in its own docstring — "independent of the other active filters" — so this was
a decision, not an oversight, but it puts numbers on screen that contradict the list
underneath them.

## Definition of done

- [x] A cuisine count answers "how many would I get if I picked this one", under the
      area and keyword already applied.
- [x] An area count does the same, under the cuisine and keyword already applied.
- [x] A facet never narrows itself — picking a cuisine must not zero every other one.

## How to verify

`RUN_INTEGRATION_TESTS=1 uv run pytest tests/test_food_integration.py` — an empty area
and an unmatched keyword must both leave every category count at zero, while a chosen
category still counts itself.

## Notes

- The web side needed no change: `food-browser.tsx` already reads the counts from the
  merchant response's facets. It hides a chip whose count is zero, so the rows now also
  stop offering cuisines and areas that would return nothing.
- `list_merchants` built its category and text conditions inline. They are now
  `_category_filter` and `_search_filter`, used by both the list and the facets, so the
  two cannot drift apart again.
