---
id: 2026-09-28-so-that-s-why-week-5
title: So That's Why: week 5 fact-checked episode packages
status: in-progress
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-28T23:04:26Z
created_at: 2026-09-28T23:04:24Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/week5
  - docs/videos/so-thats-why/episodes.json
  - docs/videos/so-thats-why/titles.json
  - docs/videos/so-thats-why/schedule.csv
  - docs/videos/so-thats-why/playlists.md
---

# So That's Why: week 5 fact-checked episode packages

## Why

Days 29–35 of `docs/videos/so-thats-why/schedule.csv` (T08, A06, B07, S08, T09, A07, B09) need the
same fact-checked packages as weeks 1–4, to keep the stock of ready episodes ahead of the schedule.

## Definition of done

- [ ] `week5/<id>.md` for all seven, in the week 4 format.
- [ ] `episodes.json` marks them `fact-checked` with a `fact_check` path and takes any title, hook,
      answer or Shorts angle the check changed; `titles.json`, `schedule.csv`, `playlists.md` and
      the neighbouring 「下一集」 previews follow any title change.

## Steps

- [ ] One fact-check per episode against primary or official sources.
- [ ] Mechanical check (claim URLs, Shorts lengths).
- [ ] Update the JSON, CSV, playlists and previews.

## How to verify

`npm run check:tasks`; both JSON files parse.

## Notes
