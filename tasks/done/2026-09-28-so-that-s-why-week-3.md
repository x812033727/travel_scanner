---
id: 2026-09-28-so-that-s-why-week-3
title: So That's Why: week 3 fact-checked episode packages
status: done
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-28T16:19:50Z
created_at: 2026-09-28T16:19:32Z
completed_at: 2026-09-28T16:27:24Z
branch:
depends_on: []
scope: []
---

# So That's Why: week 3 fact-checked episode packages

## Why

Weeks 1 and 2 (days 1–14) of `docs/videos/so-thats-why/schedule.csv` have fact-checked packages in
`week1/` and `week2/`. The owner needs at least 14 finished episodes before day 1 and a rolling
buffer after it (README §成本與產能), so days 15–21 need the same: B02, S04, T04, A03, B03, S05, T06.

## Definition of done

- [x] `week3/<id>.md` for all seven, in the week 2 format: claims table with URLs and the check
      date, corrections, paste-ready 故事前提 and 備註 for 「新的漫劇」, outline, two Shorts, what
      not to do.
- [x] `episodes.json`: the seven marked `fact-checked` with a `fact_check` path, and any title or
      answer the check changed.
- [x] `titles.json` follows any title change.

## Steps

- [x] Check each episode against primary or official sources.
- [x] Write the seven packages.
- [x] Update episodes.json and titles.json.

## How to verify

Every claim row has a source URL; `npm run check:tasks`; the JSON files parse.

## Notes
- 2026-09-28 claude-opus: seven packages written by one fact-check agent each, then checked mechanically (every claim row has a URL, 同上 or 查無出處; Shorts headlines ≤ 36, phrases ≤ 38, 25–55 s at about 4.2 characters a second).
- Titles changed by the check: B02 「日本人」→「日本公司」 (the 1991 buyer was IYG Holding, a company); T04 「不能」→「不要」 (etiquette, not law); T06 「歐洲上廁所」→「歐洲很多廁所」 (Network Rail stations free since 2019, Paris street toilets since 2006). Carried into titles.json (all locales for T06), schedule.csv, playlists.md and the previews in week2/A02.md, week3/S04.md and week3/S05.md, which is why those three paths joined the scope.
- Things the next check must not bring back: the banknote-stepping jail story (T04, no source); "Roman toilets charged entry" (T06, Vespasian taxed urine from urinals); "only two people know half the formula each" (B03); "cats test gravity" (S04); contagious yawning presented as proven empathy (S05).
