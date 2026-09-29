---
id: 2026-09-29-so-that-s-why-fact-check
title: So That's Why: fact-check season 1 days 36-100
status: in-progress
priority: P2
area: docs
owner: claude-opus
claimed_at: 2026-09-29T02:36:45Z
created_at: 2026-09-29T02:36:37Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/so-thats-why/week6
  - docs/videos/so-thats-why/week7
  - docs/videos/so-thats-why/week8
  - docs/videos/so-thats-why/week9
  - docs/videos/so-thats-why/week10
  - docs/videos/so-thats-why/week11
  - docs/videos/so-thats-why/week12
  - docs/videos/so-thats-why/week13
  - docs/videos/so-thats-why/week14
  - docs/videos/so-thats-why/week15
  - docs/videos/so-thats-why/episodes.json
  - docs/videos/so-thats-why/titles.json
  - docs/videos/so-thats-why/schedule.csv
  - docs/videos/so-thats-why/playlists.md
---

# So That's Why: fact-check season 1 days 36-100

## Why

The owner asked to fact-check everything before production (2026-09-29, 「先全部審核」). Days 1–35
have packages in week1–week5; days 36–100 (65 episodes, weeks 6–15) still have only the plan in
episodes.json. Seasons 2 and 3 follow as their own tasks.

## Definition of done

- [ ] `week6/`…`week15/<id>.md` for all 65, in the week 5 format.
- [ ] episodes.json marks them fact-checked with the answers, hooks and Shorts angles the checks leave; titles.json (all locales), schedule.csv, playlists.md and the previews follow any title change.

## Steps

- [ ] One fact-check agent per episode, a week at a time, drafts written outside the repo.
- [ ] Mechanical check per week (claim URLs, Shorts lengths), then copy into the repo.
- [ ] JSON, CSV, playlists and previews.

## How to verify

`npm run check:tasks`; the JSON files parse; the Shorts check.

## Notes
