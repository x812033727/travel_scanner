---
id: 2026-09-06-measure-the-flood-before-widening-allowed
title: Measure the flood before widening ALLOWED_TYPES with temple, shrine and museum types
status: open
priority: P3
area: api
owner:
claimed_at:
created_at: 2026-09-06T06:32:48Z
completed_at:
branch:
depends_on: []
scope:
  - apps/api/app/hotspots/discovery.py
  - apps/api/tests/test_hotspot_discovery.py
---

# Measure the flood before widening ALLOWED_TYPES with temple, shrine and museum types
## Why

Clearing the 482-row review queue on 2026-09-06 showed what the queue is made of: every
P31 type that recurred was a place a traveller visits — Buddhist temple (Q5393308, 49
rows), Shinto shrine (Q845945, 32), art museum (Q207694, 15), history museum (Q16735822,
12), wat (Q427287, 10), botanical garden (Q167346, 7), urban park (Q22746, 7), national
museum (Q17431399, 8). None of them is in `ALLOWED_TYPES`, so every one queues for a human.

Two things stop this from being a one-line change. `collect_hotspots` now turns every
auto-approved discovery into `pending / map_identity_required`, so for the weekly
discovery the whitelist only decides the category; but `import-hotspot-candidates`
still publishes a whitelisted type straight through its `confirmed` lane, and that is
where Q2680845 (Chinese temple) would have published 94 neighbourhood shrines in Taipei.
Buddhist temples and Shinto shrines are the same risk in Kyoto and Kamakura.

## Definition of done

- [ ] For each candidate type, a measured count of Wikidata items with that P31 inside
      each of the 33 cities' discovery radius (SPARQL `wikibase:around`), written down.
- [ ] Types whose flood is tens, not hundreds, added to `ALLOWED_TYPES` with the
      measurement in the comment; the rest recorded as deliberately absent, like Q2680845.
- [ ] `tests/test_hotspot_discovery.py` pins the absences.

## Steps

- [ ] Take the city centres and radii from the discovery city table.
- [ ] One SPARQL query per (type, city); Buddhist temple in Kyoto is the number that
      decides whether the type can go in at all.
- [ ] Widen, re-run `import-hotspot-candidates` for one city, confirm the confirmed lane
      only picked up what was expected.

## How to verify

```bash
cd apps/api && uv run pytest tests/test_hotspot_discovery.py -q
```

## Notes

Filed by claude-fable-5-1 from `2026-09-06-hotspot-review-backlog`, where the type
distribution of the queue was measured but the whitelist deliberately left alone.
