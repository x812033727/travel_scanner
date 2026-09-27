---
id: 2026-09-27-video-binge-worker
title: Video binge T2: worker judges series documents, drafts the compilation, genre specs and retention prompts
status: done
priority: P1
area: tools
owner: claude-fable
claimed_at: 2026-09-27T12:04:32Z
created_at: 2026-09-27T11:43:45Z
completed_at: 2026-09-27T12:29:25Z
branch: claude/keen-hamilton-plu6kp
depends_on:
  - 2026-09-27-video-binge-api
scope:
  - tools/video/automation
---

# Video binge T2: worker judges series documents, drafts the compilation, genre specs and retention prompts

## Why

On a hands-off binge series (docs/videos/BINGE.md) nobody reads the setting, the outline, the
chapter outlines or the screenplays before they are used, so the worker has to be the reader:
it asks the checker for a verdict on every series document and submits the verdict with the
document, holds a retention genre's outlines and scripts to the retention rules before the
server sees them, and, once the series is finished, produces the compilation video (title,
description, tags, thumbnail, five locales, the cut, the upload package) without a person. The
prompts also only knew the owner's xianxia setting; a binge series needs genre presets with
their conflict engines, satisfaction beats and title formulas.

## Definition of done

- [x] `planDocument` on a hands-off series asks the checker (`verifier`, variant `series-doc`)
      for `{verdicts, problems, similar_works, notes}` and submits it with the document; a
      retention genre's chapter outline is held to `hook_type`, `lead_arc`, two satisfaction
      beats, alternating hooks and a payoff every four episodes (`retentionProblem`) before
      it is submitted; when the verdict cannot be had, the document goes up without one and
      waits for the owner.
- [x] The script gate on a hands-off series runs the checker's fix loop (`fixScript`) on
      the retention numbers and coverage before `review-push --gate script`, so the server's
      `script_check_passed` decides on a payload the worker already made pass where it could.
- [x] `draftEpisode` writes the series' genre, lead, visual tier and compilation flag into
      `series.json` and `auto.json`, so lint caps the clip share and the writer knows the
      episode has no title card in a compilation.
- [x] A `compilation` job (`api.compilationStart`) writes `docs/videos/<series>-full/video.json`
      and walks `COMPILATION_STEPS`: the planner's metadata (`planner:compilation`, held by
      `metadataProblem`, the thumbnail on one of `thumbnailCandidates`), cards, `compile`,
      translations for every non-narration locale (`translator:compilation`,
      `translationProblem`), the final gate, the package, publish, then `api.compilationDone`.
- [x] `GENRE_SPECS` for `xianxia-bonds` (today's text), `rebirth-revenge`, `system-game`,
      `urban-return`, `empress-rise` and `custom`; `SATISFACTION_TYPES`, `HOOK_TYPES`,
      `LEAD_ARCS`, `RETENTION_RULES` and `VISUAL_TIER_RULES` are appended to the planner,
      writer and verifier instructions from the series' genre.

## Steps

- [x] `series.mjs`: verdict shapes, retention checks, `judgeDocument`, compilation job.
- [x] `flow.mjs`: hands-off script pre-check, binge fields in `settle`/`draftEpisode`,
      `advanceCompilation`, publish tells the series.
- [x] `compilation.mjs`: `startCompilation`, `planMetadata`, `translateMetadata`,
      `thumbnailCandidates`, `descriptionBudget`.
- [x] `prompts.mjs`: genre specs, retention and visual-tier rules, the three new variants.
- [x] `client.mjs`: `compilationStart`, `compilationDone`.
- [x] Tests: `series.test.mjs` (judge, retention, compilation job), `compilation.test.mjs`
      (an end-to-end compilation against a fake site).

## How to verify

```bash
node --test tools/video/automation/*.test.mjs
npm run test:tools
```
The end-to-end case in `compilation.test.mjs` takes a placeholder compilation document through
metadata, cards, compile, four translations, final, package and publish, and asserts the site's
`compilation/done` call.

## Notes

- 2026-09-27: done on `claude/keen-hamilton-plu6kp` with the other binge tickets. The
  verdict vocabulary is 有／弱／無 (`verdictPasses`: no 無, at most one 弱), the same as the
  server's `series_doc_passed`, so both sides agree on what passes.
- The compilation's description body budget (`descriptionBudget`) reserves 64 bytes per
  chapter line and 400 for the tool's own lines; with 40 episodes the planner gets about
  2,000 bytes, and the compile step falls back to bare 「第 N 集」 chapters if the titled
  description would still pass 5,000 bytes.
- `translateMetadata` iterates every non-narration locale in `LOCALES`, not
  `settings.caption_locales`, because `metadata translated` requires all four.
- The prompt mirrors under `.agents/skills/youtube-video/references/prompts/` are the docs
  ticket's; keep them in step with `prompts.mjs` when the genre specs change.
