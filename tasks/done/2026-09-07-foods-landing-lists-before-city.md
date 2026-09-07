---
id: 2026-09-07-foods-landing-lists-before-city
title: The foods landing tells you to pick a city while already listing 110 merchants
status: done
priority: P2
area: web
owner: claude-opus-5
claimed_at: 2026-09-07T08:00:21Z
created_at: 2026-09-07T02:06:16Z
completed_at: 2026-09-07T08:10:31Z
branch:
depends_on: []
scope:
  - apps/web/components/food-browser.tsx
  - apps/web/components/food-city-grid.tsx
  - apps/web/messages/en/foods.json
  - apps/web/messages/ja/foods.json
  - apps/web/messages/ko/foods.json
  - apps/web/messages/zh-CN/foods.json
  - apps/web/messages/zh-TW/foods.json
---

# The foods landing tells you to pick a city while already listing 110 merchants

## Why

`/zh-TW/foods` opened with three statements that could not all be true at once:

- `<h1>` 先選城市，再依區域與分類找店家
- a section headed 先選一座城市
- immediately under it, a list headed 已驗證店家 holding every city's merchants

An instruction, and a contradiction of it, one above the other. A reader who follows
the instruction and one who ignores it both end up somewhere reasonable, which is
exactly why nobody notices the page is lying — but a first-time reader has to work out
which of the two the page means.

## Definition of done

- [x] Nothing on the page tells the reader to pick a city before they can see anything.
- [x] The heading over the list names what is in the list.
- [x] The city grid reads as the shortcut it is, and says the list is already there.

## How to verify

`npx vitest run components/food-browser.test.tsx` — the new case asserts the list
heading is 所有城市的店家 with no city and the city's own name once one is picked.

## Notes

Copy only; the list was never the problem. The city grid is genuinely useful as a
shortcut and keeping the full directory below it is the better page — what had to go
was the claim that one was required before the other.
