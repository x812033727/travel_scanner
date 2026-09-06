---
id: 2026-09-06-seed-localization-reconcile
title: Re-seeding never corrects an existing dish name or summary
status: open
priority: P2
area: api
owner:
claimed_at:
created_at: 2026-09-06T00:52:17Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/foods/service.py
---

# Re-seeding never corrects an existing dish name or summary

## Why

`seed_food_catalog()` creates a `FoodLocalization` only when none exists for that
(food, locale):

```python
localization = localizations.get((food.id, locale))
if localization is None:
    ...
    session.add(localization)
```

So correcting a dish's name in `FOOD_SEEDS` and running `seed-foods` reports success and
changes nothing in the database. The same shape was true of destination links until #167,
where it was the reason three cities could not be added at all; that half was fixed and this
half was left, deliberately but without a note explaining the asymmetry.

It matters because seed names do get corrected. #169 shipped two: `苦瓜炒什錦` → `苦瓜雜炒`
(什錦 leads a dish name in Taiwanese usage rather than trailing it) and `建長汁` →
`建長寺蔬菜湯` (汁 reads as juice in Mandarin, and the string gave a reader no clue it was a
soup). Those landed only because the rows did not exist yet. The next correction to an
already-seeded dish will silently do nothing.

The reason for the caution is real: an administrator may have edited a name through the admin
UI, and a seeder that overwrites would destroy that. So this is not "make it overwrite" — it
is "make it possible to correct a seed without destroying an edit".

## Definition of done

- [ ] Correcting a name or summary in `FOOD_SEEDS` and re-running `seed-foods` updates the
      row, unless a human changed that row.
- [ ] A name an administrator edited is never overwritten.
- [ ] A test proves both directions.

## Steps

- [ ] Decide how a human edit is recognised. `FoodMerchant` solves the same problem with
      `area_source in ('seed', 'admin')`, set to `admin` as soon as an administrator touches
      the field — including when they clear it. `FoodLocalization` has no equivalent column,
      so this probably needs one plus a migration.
- [ ] Update `seed_food_catalog` to reconcile seed-owned localizations and leave admin-owned
      ones alone.
- [ ] Test: seed, edit one name as an admin, change two names in the seed, re-seed; the
      seed-owned one moves and the admin-owned one does not.

## How to verify

`tests/test_food_integration.py` runs against real Postgres in CI with
`RUN_INTEGRATION_TESTS=1`. `test_reseeding_extends_an_existing_dish_to_a_newly_listed_city` is
the pattern to copy — it seeds, monkeypatches `FOOD_SEEDS`, re-seeds and asserts the
difference.

## Notes

Destination links were made additive in #167: missing links are added, links the seed no
longer lists are left alone because an administrator may have added them. Localizations were
left create-only in the same change. This task closes that gap.

Note the same create-only shape exists for the food row itself (name, description,
ingredient tags) — a corrected `description` in `FOOD_SEEDS` also never lands. Worth deciding
in the same pass, though the admin-edit risk there is higher.
