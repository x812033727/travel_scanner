---
id: 2026-09-28-so-that-s-why-week-4
title: So That's Why: week 4 fact-checked episode packages
status: done
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-28T16:38:12Z
created_at: 2026-09-28T16:38:05Z
completed_at: 2026-09-28T16:46:10Z
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/week4
  - docs/videos/so-thats-why/episodes.json
  - docs/videos/so-thats-why/titles.json
  - docs/videos/so-thats-why/schedule.csv
  - docs/videos/so-thats-why/playlists.md
---

# So That's Why: week 4 fact-checked episode packages

## Why

Days 22–28 of `docs/videos/so-thats-why/schedule.csv` (A04, B04, S06, T07, A05, B05, S07) need
the same fact-checked packages as weeks 1–3, so the stock of ready episodes keeps ahead of the
daily schedule (README §成本與產能).

## Definition of done

- [x] `week4/<id>.md` for all seven, in the week 3 format.
- [x] `episodes.json` marks them `fact-checked` with a `fact_check` path and takes any title,
      hook, answer or Shorts angle the check changed; `titles.json`, `schedule.csv` and
      `playlists.md` follow any title change.

## Steps

- [x] One fact-check per episode against primary or official sources.
- [x] Mechanical check: every claim row has a URL (or 同上／查無出處), Shorts lengths.
- [x] Update the JSON, CSV and playlists.

## How to verify

`npm run check:tasks`; both JSON files parse; the Shorts check in the week 3 notes.

## Notes
- 2026-09-28 claude-opus: seven packages, one fact-check agent each; mechanical check passed (claim rows have a URL or 同上／查無／未採用, Shorts within length).
- One title changed: T07 「是圓的」→「都是圓角」 (airliner windows are ovals or rounded rectangles; the point is no sharp corner). All five locales in titles.json follow, plus schedule.csv, playlists.md and the S06 preview.
- Do not bring back: "square cabin windows brought down the Comet" (the G-ALYP crack began at a bolt hole by the roof ADF window; the Cohen inquiry concluded pressure-cabin fatigue); "reCAPTCHA image clicks train self-driving AI" (Google never said so); Costco hot dog "since 1985" as fact (no Costco document) and the Pepsi switch "in 2018" (it was 2013); "ice is 9% less dense" (it is about 9% more volume, about 8% less dense); Apple "punished for planned obsolescence" (no regulator found that).
