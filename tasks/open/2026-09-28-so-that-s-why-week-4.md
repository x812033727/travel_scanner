---
id: 2026-09-28-so-that-s-why-week-4
title: So That's Why: week 4 fact-checked episode packages
status: in-progress
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-28T16:38:12Z
created_at: 2026-09-28T16:38:05Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/playlists.md
---

# So That's Why: week 4 fact-checked episode packages

## Why

Days 22–28 of `docs/videos/so-thats-why/schedule.csv` (A04, B04, S06, T07, A05, B05, S07) need
the same fact-checked packages as weeks 1–3, so the stock of ready episodes keeps ahead of the
daily schedule (README §成本與產能).

## Definition of done

- [ ] `week4/<id>.md` for all seven, in the week 3 format.
- [ ] `episodes.json` marks them `fact-checked` with a `fact_check` path and takes any title,
      hook, answer or Shorts angle the check changed; `titles.json`, `schedule.csv` and
      `playlists.md` follow any title change.

## Steps

- [ ] One fact-check per episode against primary or official sources.
- [ ] Mechanical check: every claim row has a URL (or 同上／查無出處), Shorts lengths.
- [ ] Update the JSON, CSV and playlists.

## How to verify

`npm run check:tasks`; both JSON files parse; the Shorts check in the week 3 notes.

## Notes
