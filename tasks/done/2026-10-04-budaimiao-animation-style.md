---
id: 2026-10-04-budaimiao-animation-style
title: Add optional Budaimiao animation style and browser production route
status: done
priority: P2
area: docs
owner: codex-budaimiao-style
claimed_at: 2026-10-04T03:45:06Z
created_at: 2026-10-04T03:45:05Z
completed_at: 2026-10-04T04:11:54Z
branch: codex/budaimiao-animation-style
depends_on: []
scope:
  - .agents/skills/animation-camera/SKILL.md
  - .claude/skills/animation-camera/SKILL.md
  - .agents/skills/animation-camera/references/budaimiao-style.md
  - .agents/skills/animation-camera/references/budaimiao-example.json
  - .agents/skills/animation-production/SKILL.md
  - .claude/skills/animation-production/SKILL.md
  - .agents/skills/animation-production/references/browser-production.md
  - .agents/skills/animation-production/references/providers-and-plans.md
  - .agents/skills/animation-production/references/stage-preconditions.md
  - tasks/open/2026-10-04-shot-reading-offscreen-target-false-positive.md
  - tasks/open/2026-10-04-anime-silent-action-guidance.md
---

# Add optional Budaimiao animation style and browser production route

## Why

The owner wants the camera, visual finish, character performance and editing feel of
真一隻布袋喵 available as an optional animation style. Existing skills explain the
pipeline fields but do not contain this reference; some provider guidance also treats
an earlier Kling CLI choice and a Claude browser upload limitation as current defaults.

## Definition of done

- [x] Explicitly selecting 「布袋喵參考風格」 loads a dated reference with observed timecodes, portable style guidance and an original eight-shot example.
- [x] The same shots have Hailuo and Kling browser prompt adaptations using existing fields.
- [x] User-selected browser routes take priority, with session-specific capability checks and the current production-profile import rejection preserved.
- [x] Both skill entrypoint mirrors match; example checks, skill checks and independent forward-use review pass or have documented editorial exceptions.

## Steps

- [x] Refresh main and inspect active claims, worktrees, remote branches and PR scopes; create and claim this narrow task.
- [x] Write the camera reference, original example and optional-style routing.
- [x] Update browser production instructions and historical provider notes.
- [x] Validate examples, run checks and independent forward-use review.
- [x] Record results and close with the implementation for draft-PR delivery.

## How to verify

Use Node 24.19 with its directory in PATH:

```bash
node tools/video/cli.mjs lint --file .agents/skills/animation-camera/references/budaimiao-example.json
node .agents/skills/youtube-video/scripts/drama_craft_check.mjs .agents/skills/animation-camera/references/budaimiao-example.json
node .agents/skills/animation-camera/scripts/shot_reading.mjs .agents/skills/animation-camera/references/budaimiao-example.json
node --test tools/skills.test.mjs tools/animation-camera.test.mjs tools/animation-production.test.mjs
npm run test:tools
npm run check:tasks
git diff --check
```

Run skill-creator `quick_validate.py` for both animation skills. The eight-shot
single-scene example is not a complete episode: record whole-episode requirements
and intentional performance holds separately from shot-level errors. Have an
independent agent use the skills for a fresh original browser-production request.

## Notes

- Owner chose an optional style, covering both visual design/performance and camera/editing; retain Mokaair branding, voices and CC. No paid generation is part of this task.
- The root browser inspected three reference videos on 2026-10-04; the reference will list sampled frame times and keep unmeasured movement, cuts and sound distinct.
- Refreshed to origin/main ea33aba72 before branching. No active task or open PR touched either animation skill. Existing untracked `.codex/environments/` belongs to the workspace and is not part of this change.
- Keep youtube-video/SKILL.md and its mirror unchanged: the long-form review receipt binds their hashes.
- `tools/video/media/clips.mjs` rejects every project containing `series.production.profile` before import; editing provider values does not enable external clips.
- System Node 24.13 crashes on this Unicode worktree. Bundled Node 24.19 was verified during planning; use it for child processes as well.
- Node 24.19 full `test:tools`: 1,492 total, 1,482 passed, zero failed, 10 skipped (seven Bash cases, one unprovisioned API integration, one symlink restriction, one opt-in browser regression), exit 0. Log: `%TEMP%/budaimiao-animation-style-test-tools-20261004.log`.
- Targeted skill/camera/production checks: 46/46 passed. Both skill-creator format validations passed using UTF-8 and temporary PyYAML dependencies; no project dependency changes.
- Original eight-shot example: strict shot_reading zero traps; all 23 applicable craft rows passed. Complete lint intentionally fails only the single-scene/full-episode requirements (missing brief.md and one chapter instead of three); no schema or shot errors. Seven double-action info lines were semantically reviewed as a single action's hold/finish or noun conjunctions.
- Independent forward use produced a fresh three-shot original pilot and full Hailuo/Kling prompts, strict shot_reading zero traps, and correctly refused importing web clips into a profile-bound episode. Artifacts are outside the repo at `%TEMP%/animation-forward-use-bdbac2f8c88a4dfa85d320e91fee8301/`; no media was generated.
- Forward review caught the first shot's half-step/three-metre continuity ambiguity; the example now widens the stance with the torso on the same flagstone. Mirror-aware Markdown links point to the canonical .agents references from both entrypoints.
- Two pre-existing discoveries remain open in their own tasks: offscreen target co-mention false positives in shot_reading and stale anime silent-action advice in drama.md. Neither runtime behavior nor the bound YouTube entrypoints was changed.
- Final review: 10 local Markdown links resolve from their actual files, both animation entrypoint mirrors match byte for byte, and both YouTube entrypoints match origin/main. Independent production/reference review found no remaining issues after the mirror-link correction.
