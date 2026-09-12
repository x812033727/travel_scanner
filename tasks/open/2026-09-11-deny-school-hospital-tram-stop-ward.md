---
id: 2026-09-11-deny-school-hospital-tram-stop-ward
title: Deny school, hospital, tram stop, ward and military base types in hotspot discovery
status: in-progress
priority: P1
area: api
owner: claude-opus-5
claimed_at: 2026-09-11T16:53:59Z
created_at: 2026-09-11T16:53:58Z
completed_at:
branch: claude/attractions-review-progress-55bb39
depends_on: []
scope:
  - apps/api/app/hotspots/discovery.py
  - apps/api/tests/test_hotspot_discovery.py
---

# Deny school, hospital, tram stop, ward and military base types in hotspot discovery

## Why

On 2026-09-12 production held 1,237 pending hotspots, 1,167 of them from the
2026-09-08 Wikimedia discovery pass. A random sample was mostly kindergartens,
primary schools, hospitals, tram stops, Vietnamese wards and office buildings:
their Wikidata types are not in `DENIED_TYPES`, so `classify_types` files them as
`unknown_type` and they land in the human queue. The weekly discovery pass rewrites
every pending row, so rows left pending never go away, and each pass can add more.
Rejected rows are tombstones and are never reopened, so denying a type is durable.

Separately, `discover_city` overwrote a denied candidate's status with
`pending / outside_city_radius` whenever it sat past the city radius, so a denied
type could still reach the queue.

## Definition of done

- [x] Seven types that no approved attraction carries are denied: Q9842 primary school,
      Q56351315 Japanese high school, Q55521176 lower secondary school in Japan,
      Q16917 hospital, Q2175765 tram stop, Q687188 ward of Vietnam, Q245016 military base.
- [x] Types that also describe an approved attraction still reach a human
      (Q5358913 elementary school in Japan, Q285783 intersection; streets unchanged).
- [x] A denied candidate outside the city radius stays rejected.
- [x] Merged as PR #403 (`7867d5dd`) and deployed 2026-09-12 in `6925e3d1`, which was
      verified to contain that commit.
- [ ] After the next discovery pass the pending rows with these types are
      `rejected / denylisted_type`.

## Steps

- [x] Measure each candidate type against approved rows (stored `wikidata_types` for
      235 rows, live Wikidata P31 for the other 1,012 QIDs).
- [x] Extend `DENIED_TYPES` and fix the radius override.
- [x] Unit tests for both.
- [x] Merge and deploy.
- [ ] Check the next discovery pass (due after 2026-09-15 05:54 UTC, the first 6-hour
      collector cycle following it).

## How to verify

```bash
cd apps/api && uv run ruff check . && uv run mypy app && uv run pytest tests/test_hotspot_discovery.py
```

After deploy and the next discovery pass (the first 6-hour collector cycle after
`max(last_seen_at) + 7 days` for `origin='wikimedia_discovery'`), read-only:
`select review_reason, count(*) from travel_hotspots where review_status='rejected' group by 1;`
`denylisted_type` should rise by roughly the pending rows that carried these types.

## Notes

Impact measured 2026-09-12 (pending / approved / rejected rows carrying the type, from
stored `wikidata_types`): Q9842 13/0/54, Q16917 9/0/33, Q2175765 8/0/5, Q687188 6/0/77,
Q56351315 5/0/17, Q245016 5/0/0, Q55521176 4/0/26. About 50 pending rows in total.

Rejected as denylist candidates because they would hit an approved attraction:
Q5358913 (袋町小学校平和資料館), Q285783 (Shibuya scramble crossing, 銀座四丁目),
Q27686 hotel, Q35054 post office, Q1021645 office building, Q655686 commercial
building, Q5327369 chōchō (each had at least one approved row). A type is denied if
*any* of a candidate's P31 values matches, so one approved hit is enough to exclude it.

The 173 Gemini reject recommendations from catalog-review run `d943205e` are a
separate, time-limited operational step: the next discovery pass rewrites those rows,
which changes their snapshot fingerprint and makes the assessments unappliable.
