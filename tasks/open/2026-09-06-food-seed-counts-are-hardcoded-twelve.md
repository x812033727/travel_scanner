---
id: 2026-09-06-food-seed-counts-are-hardcoded-twelve
title: food seed counts are hardcoded twelve times and only CI can see them
status: in-progress
priority: P3
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T04:27:51Z
created_at: 2026-09-06T00:55:47Z
completed_at:
branch: claude/api-p2-data
depends_on: []
scope:
  - apps/api/tests/test_food_integration.py
---

# food seed counts are hardcoded twelve times and only CI can see them

## Why

`test_food_integration.py` asserts twelve hardcoded row counts against the seeded catalog —
dishes, localizations, merchants, food links, sources, areas, categories, category links,
and several filtered subsets. Every one of them has to be updated by hand whenever the seed
data grows.

The tests are gated behind `RUN_INTEGRATION_TESTS=1` and need PostgreSQL, so a local
`pytest` skips them silently. They can only fail in CI, and a red `api` on main blocks
nothing — so on 2026-09-05 main stayed red across two commits before anyone noticed, and
fixing it took four CI round-trips because each run only reveals the next stale assertion.

The counts are not worthless: they are a canary for "the seed changed in a way nobody
intended". But twelve of them, updated by hand, is a lot of friction for that signal.

## Definition of done

- [x] Growing the seed catalog does not require editing a list of unrelated numbers.
- [x] A seed change that is genuinely unintended still fails something.

## Steps

- [x] Split the assertions into two kinds: a few canaries that stay hardcoded (dish count,
      merchant count) and the derived totals (link counts, source counts, filtered subsets)
      that are pure functions of the seed modules.
- [x] Compute the derived ones from `MERCHANT_SEEDS` / `FOOD_SEEDS` /
      `MERCHANT_DIRECT_SOURCE_SEEDS` rather than restating them. That is not tautological
      for these: the test is checking that the seeder *wrote what the catalog describes*,
      which is a real property.
- [x] Leave a comment saying which numbers are canaries and why, so the next person does not
      re-hardcode the derived ones.

## How to verify

```bash
cd apps/api
RUN_INTEGRATION_TESTS=1 .venv/Scripts/python.exe -m pytest -q tests/test_food_integration.py
```

Needs PostgreSQL. There is no docker client on the current dev machine, which is exactly why
this is worth fixing — the person changing the seed usually cannot run the test that guards it.

## Notes

The expected values can be derived locally without a database. For the record, at the time
of writing:

```
FoodMerchant 173   FoodMerchantFood 192   FoodMerchantCategory 271 (+1 fixture = 272)
TravelFood 80      FoodLocalization 400   FoodMerchantSource 236
merchants with a resolvable area_slug 80
distinct merchants with merchant_listing/merchant_website evidence 63
merchants whose official_website_url is filled 28   (JP 16, TW 14, SG 6 by country)
```

`area_slug` is a derived property of `area_key` on the merchant seed — both give 80.

Related: `2026-09-06-ci-should-fail-a-branch-that` covers the other half of the same
structural problem, which is that a red `api` on main does not stop the next merge.

2026-09-06 claude-fable-5-1: two canaries stay hardcoded (`DISH_COUNT` = 80,
`MERCHANT_COUNT` = 173, each also asserted equal to the seed module's length so the
canary and the module cannot drift silently). Everything else is derived at module
level from `FOOD_SEEDS`, `MERCHANT_SEEDS`, `MERCHANT_DIRECT_SOURCE_SEEDS`,
`CATEGORY_SEEDS`, `ALL_AREA_SEEDS` and `DESTINATIONS`: localizations, merchant-dish
links, sources (one destination-context source per merchant plus every first-party
source), category links, merchants with a seed area, direct-evidence and
official-website merchants overall and per country, Seoul's Korean dishes, the
country and city facets. The comment above the constants says which are canaries and
why the rest must not be re-hardcoded. The area count had already been derived when
the trend districts landed (#190).
