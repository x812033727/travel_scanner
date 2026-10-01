---
id: 2026-09-30-long-form-drama-1-tide-after
title: Long-form drama 1: Tide After, 40 one-hour episodes plan and live-action budget
status: done
priority: P2
area: docs
owner: claude-fable-5-1
claimed_at: 2026-09-30T11:57:05Z
created_at: 2026-09-30T11:52:27Z
completed_at: 2026-09-30T13:32:36Z
branch: claude/nifty-heisenberg-0ldw0i-long-drama
depends_on: []
scope:
  - docs/videos/series-plans/tide-after-20260930
---

# Long-form drama 1: Tide After, 40 one-hour episodes plan and live-action budget

## Why

The owner is planning the channel's first long-form drama (影片分類 `long-drama`): 40 episodes of
about an hour, every episode with rising climaxes, a target of a million views an episode, one or
two dramas as structural references without copying them, and a live-action budget. Nothing in
`docs/videos/` covers a 60-minute episode: SERIES.md is the three-minute AI drama.

## Definition of done

- [x] `docs/videos/series-plans/tide-after-20260930/` holds README, setting, outline, four
      chapter files (40 episodes, each with cold open, 15/30/45-minute turns, climax, closing hook,
      rewards, tension curve, cast, places, planted and resolved mysteries, continuity), a
      40-row continuity table, packaging, a budget with three tiers and sources, and a review.
- [x] Every mystery id in setting.md is planted and resolved (or explicitly reserved) in the outline
      and chapters; closing-hook types never repeat on consecutive episodes.
- [x] References (《黑暗榮耀》, 《想見你》) are named with what is borrowed and what is not; the
      review checks the 40 episodes for resemblance to known dramas.
- [x] The budget gives per-episode and 40-episode totals for three tiers with linked sources, a
      schedule, and an honest revenue comparison against the million-views target.

## Steps

- [x] README, setting, outline (premise, cast, 40 one-liners, mystery and love-line schedules).
- [x] Four chapters written in parallel from the outline, then stitched.
- [x] Independent review of continuity, per-episode climaxes and resemblance; fixes applied.
- [x] continuity.md compiled from the chapters; budget.md and packaging.md.

## How to verify

Read README.md first, then outline.md, then any chapter. `npm run check:tasks` for the board.
Spot checks: every episode has a 冷開場, three timed turns and a typed closing hook; m01–m12 in
setting.md each appear in the chapter that outline.md schedules; budget.md numbers each carry a
source link or the word 假設.

## Notes

- This is a text plan for a live-action production, not an AI-pipeline pack: no SeriesIn JSON.
- Budget is a public-figure estimate (公視＋ Golden Bell analysis, Beauty321, TNL, CNA, SCMP,
  Wikipedia), not a quote; the honest finding is that YouTube ad revenue at a million views an
  episode covers about 0.4–1% of a mid-tier budget, so the plan names platform licensing,
  subsidies and placement as the revenue structure.
- The AI-drama pipeline could make the same runtime for about one hundredth of the cost; the plan
  suggests a 15-minute AI concept reel of episode 1 before committing to a live-action tier.
