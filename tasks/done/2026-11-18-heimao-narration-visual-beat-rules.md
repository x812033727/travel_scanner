---
id: 2026-11-18-heimao-narration-visual-beat-rules
title: Reinforce Heimao narration human-stakes and visual punch-in beat rules
status: done
priority: P2
area: tools
owner: antigravity-heimao-narration-beat
claimed_at: 2026-11-18T12:27:42Z
created_at: 2026-11-18T12:27:41Z
completed_at: 2026-11-18T12:40:06Z
branch: claude/heimao-narration-visual-beat-rules
depends_on: []
scope:
  - tools/video/automation/register.mjs
  - tools/video/automation/register.test.mjs
  - tools/video/automation/explainer-series.test.mjs
  - tools/video/automation/story-prompts.test.mjs
  - tools/video/core/narrative.mjs
  - tools/video/core/narrative.test.mjs
  - tools/video/core/curio.mjs
  - tools/video/core/curio.test.mjs
  - tools/video/assemble/drama.mjs
  - tools/video/assemble/drama.test.mjs
  - .agents/skills/brand-story/SKILL.md
  - .claude/skills/brand-story/SKILL.md
  - .agents/skills/youtube-video/references/script-writing.md
  - .agents/skills/producer/references/pace-targets.md
  - docs/videos/lessons/curio.md
  - docs/videos/lessons/sothatswhy.md
---

# Reinforce Heimao narration human-stakes and visual punch-in beat rules

## Why

Following the packaging/thumbnail improvements in PR `#2164` and the 6th-dimension demand-question gate already landed in `#2136`/`#2139`/`#2143` + `wave105`–`wave108`, two remaining content & assembly gaps separate our long-form illustrated series (`curio-*`, `sothatswhy-*`, `story-*`) from 黑猫研究院 (`@qiqiqushi0`):
1. **Spoken statutory/filing caveats & chronicle collation hurt retention (Item 3)**: Episodes such as `curio-w01` recite defensive disclaimers out loud 5 times (`照…的公開資料`、`年報寫`、`翻遍年報也找不到`、`沒有公布評審補助費`、`千萬別聽成…`), `sothatswhy-g05` cites `現行電業法規寫著`, and several historical mysteries pause to collate 3–4 chronicle editions line by line instead of advancing through human dilemmas, rivalries and moves while keeping legal/accounting footnotes in `claims.md` and `youtube.description`.
2. **Generic stand-in props & uniform full-shot zoompan glides flatten visual beats (Item 5)**: `curio-w01` (4 purses), `curio-w02` (7 purses), `curio-s13-v2` (9 plain books) and `curio-s26-v2` (10 plain books) lean on repeating generic stand-ins instead of topic-specific wordless physical objects/cross-sections; meanwhile `beat-motion-v4` glides across the entire 6 s still at one smoothstep speed (`slow_share: 0.580`, failing `pace-targets.md`'s `<= 0.30` target).

## Definition of done

- [x] Writer prompts (`STORY_SERIES_SCREEN_RULE`, `TOLD_TO_ONE_VIEWER`), narrative lint (`caveatRecitationProblems`), and the blind story-series panel (`STORY_SERIES_PANEL_QUESTIONS.no_detour`) steer narration away from statutory/annual-report caveats, `"查不到／沒有公布"` disclaimers, and multi-chronicle collation toward human dilemmas and moves.
- [x] `curio.mjs` (`genericPropWarnings`, wired into `pacingWarnings`) warns when `curio-`, `sothatswhy-`, or `story-` dramas use `purse`/`wallet` or `thick/plain-covered book` stand-ins in 3+ shots.
- [x] `drama.mjs` upgrades `still_motion: "beat"` to `beat-motion-v5` (`holdFrames: 24` ≈ 0.8 s hold + `punchFrames: 66` ≈ 2.2 s punch-in, `zoom: 0.22`, `panZoom: 1.2`) without altering unprofiled or `manga` motion expressions or keys.
- [x] Matching skills (`.agents/skills/**` + byte-identical `.claude/skills/**`), `pace-targets.md`, and `lessons/{curio,sothatswhy}.md` document the rules and measured benchmarks, with zero file overlap against PR `#2164` or `REVIEW_FILES`.

## Steps

- [x] Update `STORY_SERIES_SCREEN_RULE` and `TOLD_TO_ONE_VIEWER` in `tools/video/automation/register.mjs` and refresh `SERIES_TEXT_PINS` + tests (`register.test.mjs`, `story-prompts.test.mjs`, `explainer-series.test.mjs`).
- [x] Add `CAVEAT_RECITATION_MAX` / `caveatRecitationProblems` and `STORY_SERIES_PANEL_QUESTIONS.no_detour` in `tools/video/core/narrative.mjs` + `narrative.test.mjs`.
- [x] Add `GENERIC_PROP_MAX` / `genericPropWarnings` in `tools/video/core/curio.mjs` + `curio.test.mjs`.
- [x] Upgrade `MOTION_BEAT_VERSION` to `beat-motion-v5` with hold + punch-in in `tools/video/assemble/drama.mjs` + `drama.test.mjs`.
- [x] Update `brand-story/SKILL.md`, `youtube-video/references/script-writing.md`, `producer/references/pace-targets.md` (plus `.claude/skills` mirrors) and `docs/videos/lessons/{curio,sothatswhy}.md`.

## How to verify

```bash
npm run test:tools && npm run test:docs-videos && npm run check:tasks
```

## Notes

- Scoped deliberately to avoid any collision with open PR `#2164` (`tools/video/core/lint.mjs`, `.agents/skills/curio-episode/SKILL.md`, `docs/videos/lessons/explainer.md`, etc.) and `tools/video/long-form/review.mjs` `REVIEW_FILES`.
- Real `ffmpeg` + `reference_analysis.mjs` `motionStats` benchmark on 5 1080p illustrations (6 s each, 15-frame dissolves):
  - `beat-motion-v4`: `slow_share: 0.580`, `high_motion_share: 0.042`, `mean_difference: 5.84`
  - `beat-motion-v5` (`holdFrames: 24`, `punchFrames: 66`, `zoom: 0.22`, `panZoom: 1.2`): `slow_share: 0.059` (`<= 0.30`), `high_motion_share: 0.084` (Heimao `0.079–0.095`), `mean_difference: 5.78` (Heimao `5.0–5.9`).
