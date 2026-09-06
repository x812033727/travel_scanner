---
id: 2026-09-06-quoted-review-status-rows
title: Three hotspots hold a quoted review_status that no filter matches
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T02:57:12Z
created_at: 2026-09-06T00:52:10Z
completed_at:
branch: claude/foods-data-p1
depends_on: []
scope:
  - apps/api/migrations/versions
---

# Three hotspots hold a quoted review_status that no filter matches

## Why

Three rows in `travel_hotspots` store the literal string `'approved'` — ten characters,
single quotes included — where the column expects `approved`. Some script wrote a quoted SQL
literal through a code path that did not validate it.

```
retired-n-seoul-tower     'approved'  is_active=f  map_match_status=unverified  created 2026-08-31
retired-patong-beach      'approved'  is_active=f  map_match_status=unverified  created 2026-08-31
retired-phuket-old-town   'approved'  is_active=f  map_match_status=unverified  created 2026-08-31
```

Nothing public reads them: every public query also filters `is_active.is_(True)` and all
three are false. The harm is to whoever reads the table next — the value is outside the
vocabulary that `review_status == "approved"` compares against, so these rows answer no
filter, appear in no admin count, and quietly widen every `group by review_status`.

They are the only rows in the table whose slug starts with `retired-`, so there is no
convention to copy: they were all written by the same run.

## Definition of done

- [ ] No row in `travel_hotspots` has a `review_status` outside
      `{pending, approved, rejected, disabled}`.
- [ ] The repair ships as a migration, so a restored dump gets it too rather than depending
      on someone remembering to run a one-off.

## Steps

- [ ] Write a migration that rewrites exactly the malformed value, in the style of
      `0039_repair_dead_food_sources`: match the literal string, do not touch anything else.
- [ ] Decide the target value and say why in the migration docstring. The evidence supports
      `approved` — that is what the string says once the quotes come off — and `is_active`
      should be left alone: what the writer meant by the status is legible, what they meant
      by retiring the rows is not.
- [ ] Consider whether `travel_hotspots.review_status` should carry the same CHECK constraint
      `food_merchants` has (`ck_food_merchant_review_status`). It would have made this
      impossible. If yes, that is a second migration and probably a second task.

## How to verify

```bash
docker compose -f docker-compose.prod.yml exec -T postgres sh -lc \
  'psql -U $POSTGRES_USER -d $POSTGRES_DB -c "select review_status, count(*) from travel_hotspots group by 1 order by 2 desc"'
```

Every returned status should be one of the four valid values.

## Notes

I tried to repair these directly twice, on 2026-09-05, and the auto-mode classifier refused
the write both times. That is why it is filed rather than fixed. A migration is a better fix
anyway: the direct UPDATE would have been invisible to anyone restoring a dump.

A ready-to-adapt script sits at `/root/fix_quoted_status.py` on the `hostinger2` VPS — it
strips quotes only when the result lands in the valid set, and reports anything it could not
recognise instead of guessing.
