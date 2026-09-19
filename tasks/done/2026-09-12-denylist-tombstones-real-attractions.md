---
id: 2026-09-12-denylist-tombstones-real-attractions
title: Military base, primary school and hospital deny types will tombstone real attractions on 2026-09-15
status: done
priority: P1
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-19T04:22:10Z
created_at: 2026-09-12T06:10:00Z
completed_at: 2026-09-19T04:46:51Z
branch: claude/travel-scanner-pr-552-rpq36m
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

- [x] Q245016, Q9842 and Q16917 no longer auto-reject; they reach the human queue like
      Q5358913 and Q285783 already do, with a comment recording the false-positive rate.
- [x] Q2175765 and Q56351315 stay denied — measured at zero false positives across eight rows.
- [x] A test covers "denied type on an item that is also an allowed type" and the three
      released types.
- [x] Check whether the same "count approved rows only" reasoning was used for any other
      entry in `DENIED_TYPES`, and say so either way.

## How to verify

`uv run pytest apps/api/tests/test_hotspot_discovery.py`, plus a dry read of production
pending rows carrying each released type to confirm they are queued rather than rejected.

## Notes

Deadline is the 2026-09-15 discovery pass — after it runs the four rows are unrecoverable
without re-seeding them by hand. Merged before that date this costs nine rows back in a queue
that is being drained anyway.

### 2026-09-19 done in code (claude-fable-5-1)

- `DENIED_TYPES` no longer carries Q245016, Q9842 or Q16917; the comment above the
  2026-09-12 block records the pending-row reading (2 of 3, 1 of 2, 1 of 4 genuine) and
  why a type alone cannot reject them. Q2175765 and Q56351315 stay (0 of 8 genuine).
  Q687188 and Q55521176 also stay, but only on the approved-rows measurement: they held no
  pending rows on 2026-09-12, so nobody has read a pending row of theirs yet.
- The "count approved rows only" reasoning was used for exactly that 2026-09-12 block of
  seven. Every earlier entry was measured both ways: observed as the bulk of the 2026-09
  queue (141 of 172 rows) and checked against the attractions kept, and each describes
  something no traveller visits (a person, a company, a station, an airport, a city, a
  country), so the pending-row question does not arise for them.
- Tests: `test_types_that_also_describe_real_sights_reach_the_human_queue` covers the three
  released types, a denied type beside an allowed one (denied still wins) and a released
  type beside an allowed one; the radius test now uses Q3914 (school) as its denied example.
- Still owed after deploy (owner): read the four rows' current `review_status` in
  production (Q38278536, Q8669747, Q10911386, Q2410409). The 2026-09-15 pass ran before
  this fix, so they may already be `rejected`; if so they need re-seeding by hand. Deploy
  before the next pass (about 2026-09-22) so no further rows are lost.
