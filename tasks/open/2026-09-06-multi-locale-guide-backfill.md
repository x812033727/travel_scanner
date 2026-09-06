---
id: 2026-09-06-multi-locale-guide-backfill
title: Guide backfill searches one locale, so four locales stay empty
status: in-progress
priority: P2
area: api
owner: claude-fable-5-1
claimed_at: 2026-09-06T04:27:51Z
created_at: 2026-09-06T00:52:15Z
completed_at:
branch: claude/api-p2-data
depends_on: []
scope:
  - apps/api/app/hotspots/guides.py
---

# Guide backfill searches one locale, so four locales stay empty

## Why

`backfill_guides_once()` searches exactly one locale — whatever
`hotspot_guide_backfill_locale` says, in practice `zh-TW`. The site serves five. A Japanese
or Korean visitor opening a hotspot that the backfill has already "done" still sees nothing
in their language, and nothing in the system records that the other four were never tried.

The single locale was a deliberate trade, and the docstring says why: Brave's daily budget is
the scarce one, and spending it on breadth would leave most hotspots with nothing at all
rather than giving each one a starting set. That reasoning holds while the backlog is large.
It stops holding once the backlog is worked through, and there is currently no mechanism that
notices the moment has arrived.

## Definition of done

- [ ] A hotspot that already has a guide in the default locale can receive guides in the
      others, without starving hotspots that still have none.
- [ ] The order is explicit: every hotspot gets one locale before any hotspot gets two.
- [ ] The daily provider budgets are still respected — this must not become a way to spend
      five times the quota by accident.

## Steps

- [ ] Extend `guideless_hotspots_statement()` (or add a sibling) to return hotspots missing a
      guide in a *given* locale, rather than missing guides entirely.
- [ ] Give the backfill a locale list rather than a single locale, and work it in passes:
      locale one across every hotspot, then locale two. `hotspot_guide_backfill_locale` is a
      single string today and is surfaced in the admin group added by #170.
- [ ] Keep the exhaustion break: `backfill_guides_once` stops when every configured provider
      reports `quota_exhausted`, which is what keeps one run from draining the day.
- [ ] Decide what happens for a locale where a hotspot genuinely has no coverage, so it is
      not retried every single run forever.

## How to verify

```sql
select locale, count(distinct hotspot_id) from hotspot_guides group by 1 order by 2 desc;
```

Today that is overwhelmingly one locale. After the change, a second locale should grow once
the first has broad coverage — and the first should not stall.

## Notes

State on 2026-09-05: 651 public hotspots, 81 with any guide, 1577 guide rows. It is moving —
41 hotspots had guides the day before — but the majority still have nothing, so this task
should probably wait until single-locale coverage is broad. Filed now so the decision is
visible rather than forgotten.

The rate is no longer an env edit: #170 put `hotspot_guide_backfill_enabled`,
`hotspot_guide_backfill_batch_size` and `hotspot_guide_backfill_locale` into the
`hotspot_guides` admin group. Batch size was set to 100 in production on 2026-09-06, which
makes one collector run drain the day's provider budget rather than stopping at ten hotspots
and leaving the rest unused.

Hard ceiling worth knowing: YouTube allows 100 search calls per day and that is Google's
limit, not a setting. Brave and Gemini daily budgets are admin-adjustable per provider card.
