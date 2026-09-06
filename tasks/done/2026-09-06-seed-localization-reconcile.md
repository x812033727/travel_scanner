---
id: 2026-09-06-seed-localization-reconcile
title: Re-seeding never corrects an existing dish name or summary
status: done
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T04:27:50Z
created_at: 2026-09-06T00:52:17Z
completed_at: 2026-09-06T09:06:57Z
branch: claude/api-p2-data
depends_on: []
scope:
  - apps/api/app/foods/service.py
  - apps/api/app/foods/admin_router.py
  - apps/api/app/models.py
  - apps/api/migrations/versions/0045_food_seed_ownership.py
  - apps/api/tests/test_food_integration.py
  - apps/api/tests/test_migration_dead_branches.py
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

- [x] Correcting a name or summary in `FOOD_SEEDS` and re-running `seed-foods` updates the
      row, unless a human changed that row.
- [x] A name an administrator edited is never overwritten.
- [x] A test proves both directions.

## Steps

- [x] Decide how a human edit is recognised. `FoodMerchant` solves the same problem with
      `area_source in ('seed', 'admin')`, set to `admin` as soon as an administrator touches
      the field — including when they clear it. `FoodLocalization` has no equivalent column,
      so this probably needs one plus a migration.
- [x] Update `seed_food_catalog` to reconcile seed-owned localizations and leave admin-owned
      ones alone.
- [x] Test: seed, edit one name as an admin, change two names in the seed, re-seed; the
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

2026-09-06 claude-fable-5-1: done with a `source` column (`seed` / `admin`) on both
`travel_foods` and `food_localizations` (migration `0045_food_seed_ownership`), the
same shape as `food_merchants.area_source`.

- Ownership flips in the admin router, and only when text actually changes: a
  localization becomes `admin` when its name or summary differs from what is stored;
  the dish row becomes `admin` when one of `SEED_OWNED_FOOD_FIELDS` changes, or when
  any localization changed (search_text is rebuilt from the admin's names, so a
  re-seed must not put the catalog's version back over it). Review status and
  activation are not ownership: approving a dish keeps it seed-owned.
- `seed_food_catalog` reconciles what it owns (the descriptive dish fields through
  `apply_seed_fields`, localization name and summary) and skips `admin` rows.
  Destination links stay additive exactly as #167 left them.
- The dish row was included, which answers the open question in the notes above:
  same column, same rule, decided in one pass.
- Backfill: every existing row is marked `seed`. That is measured, not assumed.
  Production on 2026-09-06 was compared against the catalog offline: 400 of 400
  localizations equal their seed text, 80 of 80 dish rows equal the seed except two
  stale `search_text` values (jp-ramen and jp-wagashi, whose city lists grew after
  the rows were written); the first re-seed after deploy corrects those two.
  `updated_at > created_at` was useless as a signal: 255 of 400 localization rows
  differ by one microsecond because the two timestamps are assigned separately on
  insert.
- Tests: `test_reseeding_corrects_seed_owned_text_and_leaves_admin_edits_alone`
  (seed correction lands, admin edit stays, the other locales of an admin-touched
  dish still follow the seed, re-seeding the original catalog restores seed-owned
  text) and `_exercise_0045` in `test_migration_dead_branches.py`.
- Shipped in PR #198 (ba96d74, merged 2026-09-06 05:41Z) and deployed; the `done` step was missed then and
  the file is archived on 2026-09-06 by claude-fable-5-1 without further changes.
