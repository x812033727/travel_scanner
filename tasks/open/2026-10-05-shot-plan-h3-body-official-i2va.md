---
id: 2026-10-05-shot-plan-h3-body-official-i2va
title: shot_plan.mjs H3 body follows the official I2VA structure
status: open
priority: P3
area: tools
owner:
claimed_at:
created_at: 2026-10-05T16:41:00Z
completed_at:
branch:
depends_on:
  - 2026-10-05-delivery-promise-and-continuity-locks
scope:
  - .agents/skills/animation-preproduction/scripts/shot_plan.mjs
  - tools/animation-preproduction.test.mjs
  - .agents/skills/animation-preproduction/references/route-decisions.md
---

# shot_plan.mjs H3 body follows the official I2VA structure

## Why

`2026-10-05-animation-skill-references-prompt-facts` compared `H3_FIRST_LINE` and the H3 web
body that `shot_plan.mjs --route hailuo --hailuo-model h3` writes against MiniMax's official
prompt guides (the Hugging Face `VIDEO_PROMPT_WRITING_GUIDE_base_en.md`, model card updated
2026-08-13, and the official `MiniMax-AI/MiniMax-H3` skill `h3-prompt-writing`, both read
2026-10-05). The first line and the three fields match verbatim; the body inside `[Shot 1]`
does not. The findings are in `.agents/skills/animation-camera/references/model-misreads.md`
section six. They were out of that ticket's scope (docs only), so they are filed here for the
owner of the script.

## Definition of done

- [ ] `[Shot 1]` opens with an official style word (mapped from the look preset: `anime-2d` →
      `2D-animated`, `cinematic-3d` → `3D CG`, `ink-wash` → `watercolor` or the nearest, …) and an
      anchor sentence that cites `<Picture 1>` and keeps the first frame's composition, identities,
      costumes and props; the motion follows it. Today `WEB_KEEP` sits at the end and never names
      `<Picture 1>`.
- [ ] Camera sentences use only the official speed words: `at slow speed` / `at fast speed`;
      a move that is neither slow nor fast carries no speed (`at a steady speed` is not in the
      official table, and "medium amplitude and normal speed are usually omitted").
- [ ] A shot planned with an end frame writes the FL2VA alignment line (`How the reference
      pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second
      mark …; Picture 2 (from Shot 1) aligns with the S.SS-second mark …`, two decimals, the
      bought seconds) instead of the I2VA line.
- [ ] The three fields are separated by a blank line, as every official example is (or the
      pilot shows it makes no difference, written down).
- [ ] `route-decisions.md` section six shows the new body; `tools/animation-preproduction.test.mjs`
      pins the first line, the style word, the anchor sentence and the speed words.

## Steps

- [ ] Read `model-misreads.md` section six and the official base guide once more; the pilot
      ticket `2026-10-04-paid-verification-hailuo-kling-web` decides the two unverified lines
      (`N/A` sound fields, the `no on-screen text` negation).
- [ ] Change `webPrompt` and `webMove` in `shot_plan.mjs`, update the test and the reference.

## How to verify

```bash
node --test tools/animation-preproduction.test.mjs tools/skills.test.mjs
node .agents/skills/animation-preproduction/scripts/shot_plan.mjs --route hailuo --hailuo-model h3 <episode>
```

## Notes

- Depends on `2026-10-05-delivery-promise-and-continuity-locks`, which holds `shot_plan.mjs`
  in its scope; take this one after it lands.
- Keep `sha256` of the body as the lock's identity: changing the body re-locks every H3 shot,
  so do it before a batch, not between its phases.
