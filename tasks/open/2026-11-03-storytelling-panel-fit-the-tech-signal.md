---
id: 2026-11-03-storytelling-panel-fit-the-tech-signal
title: Storytelling panel: fit the Tech Signal podcast's segment chapters
status: open
priority: P2
area: tools
owner:
claimed_at:
created_at: 2026-11-03T02:40:20Z
completed_at:
branch:
depends_on: []
scope:
  - tools/video/core/narrative.mjs
---

# Storytelling panel: fit the Tech Signal podcast's segment chapters

## Why

The daily brief (`daily-ai-` slugs) became the two-host podcast Tech Signal on 2026-11-02 (`.agents/skills/youtube-video/references/daily-brief.md`): chapters are segments (Headlines with six stories, Money Signal with three, Try This right after the main story), and the main story is told at length with recurring key figures. The storytelling panel's daily-brief questions (`DAILY_BRIEF_PANEL_QUESTIONS` in `tools/video/core/narrative.mjs`) still assume one story per chapter. On `daily-ai-20261103` it took ten blind readers to pass: `chapters_are_events` failed on segment titles, and `no_recap` failed on a different set of repeats almost every time (the main story's key numbers, the deadline), so the verdict depended more on the reader than on the script.

## Definition of done

- [ ] `chapters_are_events` accepts a segment chapter titled 「段落名：該段的新聞」 that names its stories.
- [ ] `no_recap` judges repeats per story, lets the main story restate its one or two key figures once as a callback, and asks for exact line pairs.
- [ ] A Try This chapter that directly follows its story counts as part of that story for `one_line`.

## Steps

- [ ] Reword the daily-brief variants in `narrative.mjs` and keep their ids and required flags.
- [ ] Update `panelRulesSha256` expectations and the tests in `tools/video/core/narrative.test.mjs`.

## How to verify

`node --test tools/video/core/narrative.test.mjs`; then run the panel on `daily-ai-20261103` with two fresh readers and compare their answers.

## Notes

- Readers also sometimes wrap answer ids in brackets (`"[scene_first]"`), which the tool reads as no answer. Accepting a bracketed id would save a rerun.
