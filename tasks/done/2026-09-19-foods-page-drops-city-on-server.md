---
id: 2026-09-19-foods-page-drops-city-on-server
title: Foods page drops ?city= on the server, so guide links render every city first
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-19T06:11:54Z
created_at: 2026-09-19T06:11:54Z
completed_at: 2026-09-19T06:16:59Z
branch: claude/foods-city-ssr
depends_on: []
scope:
  - apps/web/app/[locale]/foods/page.tsx
  - apps/web/app/[locale]/foods/page.test.tsx
---

# Foods page drops ?city= on the server, so guide links render every city first

## Why

`2026-09-14-food-links-city-param-ignored` (PR #556) taught `readFoodBrowserFilters` in
`apps/web/lib/foods.ts` to read `?city=` as a fallback for `destination_id`, because every travel
guide links its city's food list as `/foods?city=<destination_id>`. The server page never passes
it on: `app/[locale]/foods/page.tsx` copies only `destination_id`, `area`, `category`, `style` and
`q` into the search string it hands to `readFoodBrowserFilters`, so `city` is gone before the
parser sees it.

Measured on production right after the #556 deploy (2026-09-19, `3f5c8ad6`):

| URL | HTML bytes | "kanazawa" in the HTML |
|---|---|---|
| `/zh-TW/foods` | 420,726 | 3 |
| `/zh-TW/foods?city=kanazawa` | 420,786 | 6 |
| `/zh-TW/foods?destination_id=kanazawa` | 266,725 | 30 |

In the built-in browser the `?city=` page does end on Kanazawa: the city select reads
「金澤 (4)」 and the list shows Kanazawa shops, because `FoodBrowser` re-reads the full URL on
the client and fetches again. So a reader first gets every city and then watches the list swap,
crawlers and no-JS readers only ever get the unfiltered page, and the server's first merchants
request is wasted.

## Definition of done

- [x] The server render hands `?city=` to `getInitialFoods` and to the first-rendered controls,
      exactly as it does `?destination_id=`.
- [x] `destination_id` still wins when a URL carries both.
- [x] After the deploy, the production HTML of `/zh-TW/foods?city=kanazawa` is the filtered page.

## Steps

- [x] Add `city` to the keys `page.tsx` copies; precedence stays in `readFoodBrowserFilters`.
- [x] Extend `page.test.tsx` with both cases.
- [x] Deploy, then compare the three URLs again.

## How to verify

```bash
cd apps/web && npx vitest run "app/[locale]/foods/page.test.tsx"
for q in '' '?city=kanazawa' '?destination_id=kanazawa'; do curl -s "https://mokaair.com/zh-TW/foods$q" | wc -c; done
```

After the deploy the second size should drop to about the third (both filtered), well below the first.

## Notes

- The parser already owns precedence (`destination_id` first, then `city`), so the page copies
  `city` through unchanged instead of translating it; the browser keeps writing `destination_id`
  when a reader changes the filters, so `city` never becomes a second canonical form.
- 2026-09-19: `page.tsx` now copies `city` through. The new page test fails on the old code
  (`load` last called with an empty `destinationId`) and passes with the fix. `lint:web`,
  `check:i18n` and `typecheck:web` are clean, and the seven foods test files (44 tests) pass.
  The two unticked items are the post-merge deploy and the three-URL size comparison.

### 2026-09-19 主機執行（claude-opus-5，站主逐項同意；部署 `6a254971` 之後）

- 2026-09-19 after the 06:45 UTC deploy of #557: `/zh-TW/foods` 516,549 bytes (3 × kanazawa), `?city=kanazawa` 355,737 (30), `?destination_id=kanazawa` 355,777 (30) — the server HTML is now the filtered page.
