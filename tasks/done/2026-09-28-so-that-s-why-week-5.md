---
id: 2026-09-28-so-that-s-why-week-5
title: So That's Why: week 5 fact-checked episode packages
status: done
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-28T23:04:26Z
created_at: 2026-09-28T23:04:24Z
completed_at: 2026-09-28T23:15:06Z
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

- [x] `week5/<id>.md` for all seven, in the week 4 format.
- [x] `episodes.json` marks them `fact-checked` with a `fact_check` path and takes any title, hook,
      answer or Shorts angle the check changed; `titles.json`, `schedule.csv`, `playlists.md` and
      the neighbouring 「下一集」 previews follow any title change.

## Steps

- [x] One fact-check per episode against primary or official sources.
- [x] Mechanical check (claim URLs, Shorts lengths).
- [x] Update the JSON, CSV, playlists and previews.

## How to verify

`npm run check:tasks`; both JSON files parse.

## Notes
- 2026-09-28 claude-opus: seven packages, one fact-check agent each; mechanical check passed (A06 has one row with no URL, a labelled wavelength calculation).
- Titles changed: T08 「都在」→「大多在」 (Taiwan, Narita and Incheon have arrival duty-free shops); B07 → 「星巴克的「中杯」為什麼叫 Tall？」 (Starbucks Taiwan still lists 小杯 for hot drinks, so Tall is the medium there); S08 「上癮」 in quotes (no clinical addiction); B09 → 「為什麼發明數位相機的柯達，後來還是聲請破產？」 (Kodak led US digital camera sales in 2005; Chapter 11 in 2012). All five locales in titles.json, schedule.csv, playlists.md and the previews in week4/S07, week5/A07 and week5/B07 follow.
- Recheck on the day: the JVMA count (T09; the JVMA site returned 503, figures came via pages quoting its table); the Sasson quote against the NYT 2008 original (B09); Ofcom's router advice page (A06, blocked to automated fetch); the Il Giornale page on about.starbucks.com (B07, 403); NVIDIA's market-cap ranking (A07, changes daily).
- Do not bring back: 2.4 GHz as water's resonant frequency (A06); endorphins as the proven reason people like spicy food, and "water doesn't help" (S08); Kodak "never did digital" (B09); "high labour costs, small land" as proven vending-machine reasons and "most per capita in the world" (T09); Taiwan arrival allowance 1 L / NT$20,000 (now 1.5 L / NT$35,000, T08).
