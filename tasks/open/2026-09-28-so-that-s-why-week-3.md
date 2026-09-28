---
id: 2026-09-28-so-that-s-why-week-3
title: So That's Why: week 3 fact-checked episode packages
status: in-progress
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-28T16:19:50Z
created_at: 2026-09-28T16:19:32Z
completed_at:
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

- [ ] `week3/<id>.md` for all seven, in the week 2 format: claims table with URLs and the check
      date, corrections, paste-ready 故事前提 and 備註 for 「新的漫劇」, outline, two Shorts, what
      not to do.
- [ ] `episodes.json`: the seven marked `fact-checked` with a `fact_check` path, and any title or
      answer the check changed.
- [ ] `titles.json` follows any title change.

## Steps

- [ ] Check each episode against primary or official sources.
- [ ] Write the seven packages.
- [ ] Update episodes.json and titles.json.

## How to verify

Every claim row has a source URL; `npm run check:tasks`; the JSON files parse.

## Notes
