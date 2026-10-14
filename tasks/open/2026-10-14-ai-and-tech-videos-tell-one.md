---
id: 2026-10-14-ai-and-tech-videos-tell-one
title: AI and tech videos tell one story with one protagonist
status: in-progress
priority: P2
area: tools
owner: claude-opus-5-5-ai-storytelling
claimed_at: 2026-10-14T16:46:12Z
created_at: 2026-10-14T16:45:24Z
completed_at:
branch: claude/ai-video-storytelling
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/prompts.mjs
  - tools/video/automation/prompts.test.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/automation/series.test.mjs
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - .agents/skills/youtube-video/references/script-writing.md
---

# AI and tech videos tell one story with one protagonist

## Why

The owner (2026-10-15) says the AI and tech YouTube videos should be lively and told like a
story so viewers keep watching; today they jump around and are hard to follow. The storytelling
rules of 2026-10-13 (`NARRATIVE_RULES`, `CONDENSATION_RULE`, the blind panel `NARRATIVE_PANEL`,
script-writing.md §故事主線與鉤子) were written around the history series (years, places,
records, lab results) and give a tech video no concrete shape. A blind reader read three recent
AI videos (Anthropic network-cut evaluations, Cloudflare Auto Router, Google SynthID) and found
the same failure in all three: no single protagonist or example carried from start to end;
scenes and metaphors switching constantly (one video used eight: chef, coins, scale, post office,
motorbike, shoebox, bridge, tasting); detours away from the viewer's question (a third of the
SynthID video on text watermarks while the story was about mom's image); comparisons before the
things compared were introduced; lists read out (product roll calls, four scores in four seconds,
who-said-what tables); 「以官網為準」 instead of numbers. The one stretch with a single thread
(mom's image) was the most followable part.

## Definition of done

- [x] `NARRATIVE_RULES` has a compact "One protagonist, one story shape" subsection: four shapes
      (事件型、實測型、疑問型、抉擇型), one protagonist from opening to close, at most one metaphor,
      detours cut, introduce before comparing, no read-out lists, numbers not 「以官網為準」.
- [x] The slides planner's outline format carries 「故事線：<事件／實測／疑問／抉擇（選一）>」 and
      「主角：…」 before 主線／轉折.
- [x] `NARRATIVE_PANEL` has two more required questions, `one_thread` and `no_detour`; tests
      count with `NARRATIVE_PANEL.length` (or the required count), never a fixed number.
- [x] script-writing.md §故事主線與鉤子 has 「AI 與科技片：一個主角、一種故事線」 and the panel
      section lists thirteen questions.
- [ ] The owner has read a proof rewrite of the Anthropic network-cut video written to these rules
      and accepted it, before the branch is merged or deployed.
- [ ] Deployed with no unfinished episode on the host at a stage whose prompt moved (see Notes).

## Steps

- [x] Rules, outline lines, panel questions, docs, tests (branch `claude/ai-video-storytelling`).
- [ ] Proof rewrite of the Anthropic network-cut script under the new rules, blind panel run on
      it (13 questions), shown to the owner.
- [ ] Duration receipt: `tools/video/automation/prompts.mjs` is bound by
      `docs/videos/long-form/review.json`, so `node tools/video/long-form/cli.mjs check` fails
      with "stale duration review binding" until an independent agent records a DURATION_ONLY
      increment. Do not edit review.json/review.md by hand.
- [ ] Merge, then deploy when the host has no unfinished episode at a moved stage.

## How to verify

```bash
node --test tools/video/core/narrative.test.mjs tools/video/automation/prompts.test.mjs tools/video/automation/explainer-series.test.mjs
node --test tools/skills.test.mjs
npm run check:tasks
node tools/video/long-form/cli.mjs check   # red until the receipt increment above
```

## Notes

- The owner wants a proof rewrite of the Anthropic network-cut video before merge or deploy:
  the rules are a guess until one real script written to them reads as one story.
- Deploying changed prompts re-runs and re-charges unfinished work: the instructions are part of
  each stage's durable key, so any episode on the host still sitting at a stage whose prompt
  moved is asked, and paid for, again (or stops with video_ai_receipt_input_changed). Moved by
  this change: every slides planner, writer and listener (REGISTER_RULES embeds NARRATIVE_RULES),
  the brand-story writer (story-prompts.mjs embeds NARRATIVE_RULES), `writer:explainer`, and the four
  series writers `writer:explainer-cartoon`, `writer:discuss-cartoon`, `writer:explainer-mystery`,
  `writer:discuss-mystery`. Re-pinned: prompts.test.mjs (`writer:explainer`),
  explainer-series.test.mjs (group 1: the explainer writer composed with a row and with a stance;
  SERIES_TEXT_PINS: the four writers above), series.test.mjs (EXPLAINER_STAGE_PINS: the writer
  instructions digest). Planners and verifiers of the explainer routes did
  not move. The blind panel's payload gains two questions, so a narrative review in flight is
  asked again.
- The two skill SKILL.md lines that count the panel are now stale and were left alone because
  their files are inside the scope of the still-open
  2026-10-14-curio-episodes-keep-the-series-look task: `.agents/skills/youtube-video/SKILL.md`
  row 4.5 says 「十一題」 (now thirteen), `.agents/skills/curio-episode/SKILL.md` step 1 says
  「11 題全過」. Fix both (with their `.claude/skills` mirrors) once that task is done.
- REGISTER_RULES still says every chapter has "one concrete scene or comparison"; the new
  subsection says the scene is the protagonist's own, not a new comparison, which keeps the two
  consistent without rewording the register.
