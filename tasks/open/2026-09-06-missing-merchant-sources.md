---
id: 2026-09-06-missing-merchant-sources
title: Most merchants have no first-party page, so nothing can locate them
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:52:13Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/merchant_catalog.py
---

# Most merchants have no first-party page, so nothing can locate them

## Why

Every seeded merchant carries a `destination_context` source — a city food guide. 272
merchants share about 23 of those, so such a page says a city has food, not where one
restaurant stands. Only a `merchant_website` (the shop's own site) or a `merchant_listing`
(a tourism board's page about that one merchant) is evidence about a specific place.

On 2026-09-05, 63 of 172 merchants had one. The coordinate fill reported `no_source` for the
other **109**, meaning it had nothing to even open. More merchants have been added since, so
the gap is now larger.

This is the upstream cause of `2026-09-06-merchant-coordinate-backlog-270-of-272`: a merchant
with no page of its own has no route to a durable coordinate except a human typing one.

## Definition of done

- [ ] Every merchant that can have a first-party page has one, or is explicitly recorded as
      having none available.
- [ ] `fill-food-merchant-coordinates` reports `no_source` for only the merchants where that
      is genuinely true.
- [ ] `tests/test_food_catalog.py` counts updated to match.

## Steps

- [ ] List the merchants with no usable source. `merchant_page_sources()` in
      `app/foods/coordinate_fill.py` is the exact rule: scope in (merchant_website,
      merchant_listing), `source_type` in `DURABLE_COORDINATE_SOURCES`, https.
- [ ] Work country by country. Government tourism sites with per-merchant pages already used
      here and known to work: `okinawastory.jp/gourmet/<id>` (OCVB),
      `trip-kamakura.com/stay-gurume/detail.php?id=<id>`, `kanagawa-kankou.or.jp/spot/<id>`,
      `travel.taipei/en/shop/details/<id>`, `english.visitseoul.net`, `khh.travel`.
- [ ] Fetch and read every page before citing it. Confirm three things: the page is about
      that merchant, the merchant is still operating, and the page mentions the dish the
      merchant is mapped to. #169 did this for 16 Japanese merchants and rejected several
      candidates on exactly those grounds.
- [ ] Use `_merchant_website` when the URL is the shop's own site (it also sets
      `official_website_url`) and `_official_listing` for a tourism page.
- [ ] Update the country balance and total assertions in
      `test_direct_sources_are_verified_and_country_balanced`.

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T api \
  python -m app.cli fill-food-merchant-coordinates --limit 40 | head -c 400
```

`no_source` should fall by the number of merchants given a page.

## Notes

Adding a page does not by itself produce a coordinate: of the 63 merchants that already had
one, 62 published nothing machine-readable, so expect the direct yield to be near zero. The
value is that a reviewer can open one page per merchant instead of searching, and that the
merchant becomes eligible for the coordinate review queue. Read the Notes of
`2026-09-06-merchant-coordinate-backlog-270-of-272` before assuming otherwise.

Japan had no entries in `MERCHANT_DIRECT_SOURCE_SEEDS` at all until #169 — a test asserted
that (`merchant_country[...] != "JP"`). That assertion is gone; the 16 Japanese entries added
there are the pattern to follow.

Scope overlaps `2026-09-06-broken-merchant-citations`: both edit
`apps/api/app/foods/merchant_catalog.py`. Doing both in one branch is reasonable.
