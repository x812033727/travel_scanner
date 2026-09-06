---
id: 2026-09-06-broken-merchant-citations
title: Nine merchant citations are dead, unreachable or not HTML
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:52:12Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/merchant_catalog.py
---

# Nine merchant citations are dead, unreachable or not HTML

## Why

A merchant's cited page is its evidence: it is what an administrator opens to confirm the
place is real and where it is, and it is what `fill-food-merchant-coordinates` reads. Nine of
the 63 first-party citations in `MERCHANT_DIRECT_SOURCE_SEEDS` cannot be opened at all, so
those merchants carry evidence that proves nothing.

Found by running the coordinate fill over every merchant on 2026-09-05:

```
fetch_failed: 6    http_500: 1    not_html: 2
```

Two are identified: `www.taicheongbakery.com.hk` serves a certificate that does not cover its
own hostname, and `https://www.krua-apsorn.com/` answers 500. The other seven are in the run
report and need naming before they can be fixed.

This is the same class of rot as the two country-level sources repaired in #165, where the JP
food page had been a hard 404 for every one of the ten Japanese dishes and the TW one had
silently become a New Taipei City page. Nobody notices a citation going bad, because nothing
reads it until someone does.

## Definition of done

- [ ] Every URL in `MERCHANT_DIRECT_SOURCE_SEEDS` returns a real page about that merchant.
- [ ] Any that cannot be repaired are removed rather than left broken — a merchant with no
      first-party source is honest, one with a dead link is not.
- [ ] Existing rows are repaired too, not only the seed constants: `FoodMerchantSource.source_url`
      is written at creation, so changing the constant alone leaves production untouched.

## Steps

- [ ] Get the nine slugs: `/root/coordfill_all.json` on the `hostinger2` VPS holds the full
      run, one row per merchant with its outcome.
- [ ] Re-check each by hand. A 403 is not proof of rot — tourismthailand.org and
      discoverhongkong.com both answer 403 to a bot and are fine in a browser; that was
      checked in #165 and they were deliberately left alone.
- [ ] Replace or remove. If replacing, fetch and read the new page first; #165 has the
      pattern, including a `_official_listing` vs `_merchant_website` choice that must match
      what the page actually is.
- [ ] Add a migration rewriting the old strings in `food_merchant_sources.source_url`, in the
      style of `0039_repair_dead_food_sources`.
- [ ] Update the count assertions in `tests/test_food_catalog.py` if the seed count changes.

## How to verify

Re-run the coordinate fill and confirm the unreadable outcomes are gone:

```bash
docker compose -f docker-compose.prod.yml exec -T api \
  python -m app.cli fill-food-merchant-coordinates | head -c 400
```

`fetch_failed`, `http_500` and `not_html` should all be absent from `outcomes`.

## Notes

The failure reasons are individually named because of #162 — before that every unreadable
page collapsed into one `fetch_failed`, which said only that something went wrong somewhere.
That change is what makes this task actionable.

Scope overlaps `2026-09-06-missing-merchant-sources`: both edit
`apps/api/app/foods/merchant_catalog.py`. They are separate problems (repair the broken
versus supply the absent) but cannot be worked in parallel. Whoever claims one should look at
the other first — doing both in one branch is reasonable.
