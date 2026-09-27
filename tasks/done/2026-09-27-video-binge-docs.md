---
id: 2026-09-27-video-binge-docs
title: Video binge D7: BINGE.md, design docs and the skill's series route
status: done
priority: P2
area: docs
owner: claude-fable
claimed_at: 2026-09-27T12:18:08Z
created_at: 2026-09-27T11:43:47Z
completed_at: 2026-09-27T12:39:42Z
branch: claude/keen-hamilton-plu6kp
depends_on: []
scope:
  - .agents/skills/youtube-video
  - .claude/skills/youtube-video
  - docs/videos
---

# Video binge D7: BINGE.md, design docs and the skill's series route

## Why

The binge design (one button, hands-off gates, visual tiers, the compilation) was decided
with the owner on 2026-09-27 and implemented across seven tickets, but the long-form docs
under `docs/videos/` and the shared `youtube-video` skill still described a series as
something the owner approves document by document and episode by episode. The next agent
would have re-derived the workflow from the code.

## Definition of done

- [x] `docs/videos/BINGE.md`: the owner's decisions, the flow, the data model, the one-button
      form and quote, the server rules with their constants, the retention spec, the genre
      presets, the visual tiers, the compilation, the web and host changes, the cost table,
      the risks, what differs from the original plan, the tickets and the pilot plan.
- [x] `SERIES.md`, `AUTOMATION.md`, `HANDS-OFF.md`, `DRAMA.md` and `README.md` updated where
      the binge series changes them (new columns, the three extra worker duties, the
      document and script auto-approval rules, still shots and camera moves, the product's
      length spec).
- [x] The skill: `SKILL.md` route table gains 一鍵合集 (byte-identical copy under
      `.claude/skills/`), `references/series.md` and `drama.md` describe the binge mode,
      `prompts/series-chapter.md`, `writer-series.md` and `verifier-series.md` carry the
      retention fields, and the new `prompts/verifier-series-doc.md` and
      `prompts/planner-compilation.md` mirror the worker's new variants.

## Steps

- [x] BINGE.md.
- [x] The five existing docs.
- [x] Skill references, prompt mirrors, `cp` to `.claude/skills/`.
- [x] `npm run test:tools` (skill copies in step), `npm run check:tasks`.

## How to verify

```bash
node --test tools/skills.test.mjs
npm run test:tools && npm run check:tasks
diff .agents/skills/youtube-video/SKILL.md .claude/skills/youtube-video/SKILL.md
```

## Notes

- 2026-09-27: done on `claude/keen-hamilton-plu6kp`. BINGE.md's 「實作與原計畫不同的地方」
  section records where the code departed from the approved plan (the verdict vocabulary
  有／弱／無 instead of scores, the worker-side script fix loop before submission, the
  compilation step names), so the plan file is not the reference any more.
- The prompt mirrors are documentation of `tools/video/automation/prompts.mjs`, not a second
  source of truth; when the genre specs or retention rules change, change `prompts.mjs`
  first and the mirrors with it.
- The pilot ticket `2026-09-27-video-binge-pilot` stays open for the post-deploy trial run
  and the measured numbers.
