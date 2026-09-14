---
id: 2026-09-14-food-links-city-param-ignored
title: Food directory links use ?city= but the directory only reads destination_id
status: open
priority: P2
area: web
owner:
claimed_at:
created_at: 2026-09-14T10:30:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/web/lib/foods.ts
  - apps/web/lib/foods.test.ts
---

# Food directory links use ?city= but the directory only reads destination_id

## Why

Every travel guide ends with a link to the city's food list, written as
`https://mokaair.com/zh-TW/foods?city=<destination_id>`. The food directory ignores it.

`readFoodBrowserFilters` in `apps/web/lib/foods.ts` reads only `destination_id`, `area`,
`category`, `style` and `q`, and `foodBrowserSearch` writes `destination_id`. A reader who taps
「札幌美食目錄」 lands on the unfiltered list of every city. On production (2026-09-14),
`/zh-TW/foods?city=kanazawa` returns the same generic page as `/zh-TW/foods`.

The `?city=` shape is not a one-off. It is the documented internal-link format for guides: the
brief of batches 1 to 5, `docs/travel-guides-batch-6/README.md`, and both batch check scripts
all use it. 60 content packs on main carry at least one such link.

## Definition of done

- [ ] `/zh-TW/foods?city=sapporo` opens the food list filtered to Sapporo, exactly as
      `?destination_id=sapporo` does.
- [ ] When both parameters are present, `destination_id` wins.
- [ ] Links the browser writes back keep using `destination_id`, so there is one canonical
      shape and the canonical URL is unchanged.

## Steps

- [ ] In `readFoodBrowserFilters`, fall back to `city` when `destination_id` is absent.
- [ ] Add a unit test in `apps/web/lib/foods.test.ts` for the alias and for the precedence.

## How to verify

```bash
cd apps/web && npx vitest run lib/foods.test.ts
```

Then open `/zh-TW/foods?city=seoul` locally and check the destination filter is selected.

## Notes

- Fixing the reader is one line. Rewriting 60 published packs would change every article's
  `modified_at` for no reader-visible gain.
- Found while planning batch 6. A reviewer flagged that `lib/foods.ts` only reads
  `destination_id`; the production page confirmed it.
