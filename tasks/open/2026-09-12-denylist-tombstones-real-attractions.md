---
id: 2026-09-12-denylist-tombstones-real-attractions
title: Military base, primary school and hospital deny types will tombstone real attractions on 2026-09-15
status: open
priority: P1
area: api
owner:
claimed_at:
created_at: 2026-09-12T06:10:00Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/discovery.py
  - apps/api/tests/test_hotspot_discovery.py
---

# Military base, primary school and hospital deny types will tombstone real attractions

## Why

PR #403 added seven types to `DENIED_TYPES`. The measurement behind it — "no approved
attraction carries this type" — was necessary but not sufficient: it never asked whether the
*pending* rows carrying the type were real attractions. On 2026-09-12 all 17 pending rows
carrying one of the seven were read against their Wikipedia extracts, and four of them are
genuine sights that `classify_types` will reject outright on the next discovery pass
(2026-09-15). `review_status='rejected'` is a tombstone: `discover_city` skips those rows
forever, so the loss is permanent.

| type | pending rows | genuine attractions among them |
|---|---|---|
| Q245016 military base | 3 | 2 — 喜屋武城 (Q38278536), a Ryukyu-era gusuku ruin in Uruma; 鎮平台 (Q8669747), the Trấn Bình đài bastion inside the Huế citadel, a UNESCO site |
| Q9842 primary school | 2 | 1 — 原花園尋常小學校本館 (Q10911386), gazetted a Tainan historic building in 2003 |
| Q16917 hospital | 4 | 1 — 島醫院 (Q2410409), the Hiroshima atomic-bomb hypocentre |
| Q2175765 tram stop | 6 | 0 |
| Q56351315 Japanese high school | 2 | 0 |
| Q687188 ward of Vietnam | 0 | — |
| Q55521176 lower secondary school in Japan | 0 | — |

The four are not badly modelled by accident: a gusuku *is* a fortification and an old school
building *is* a school, so Wikidata's P31 is correct and still useless as a rejection signal.
A heritage override does not rescue them either — none of the four carries P1435 (heritage
designation) or any other designation property, so there is nothing in the data to key on.
`classify_types` also tests `DENIED_TYPES` before `ALLOWED_TYPES`, so a denied type wins even
when an allowed one is present on the same item.

## Definition of done

- [ ] Q245016, Q9842 and Q16917 no longer auto-reject; they reach the human queue like
      Q5358913 and Q285783 already do, with a comment recording the false-positive rate.
- [ ] Q2175765 and Q56351315 stay denied — measured at zero false positives across eight rows.
- [ ] A test covers "denied type on an item that is also an allowed type" and the three
      released types.
- [ ] Check whether the same "count approved rows only" reasoning was used for any other
      entry in `DENIED_TYPES`, and say so either way.

## How to verify

`uv run pytest apps/api/tests/test_hotspot_discovery.py`, plus a dry read of production
pending rows carrying each released type to confirm they are queued rather than rejected.

## Notes

Deadline is the 2026-09-15 discovery pass — after it runs the four rows are unrecoverable
without re-seeding them by hand. Merged before that date this costs nine rows back in a queue
that is being drained anyway.
