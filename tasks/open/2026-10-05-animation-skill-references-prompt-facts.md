---
id: 2026-10-05-animation-skill-references-prompt-facts
title: Animation skill references: prompt length per model, overlays are not depth, H3 format cross-check, error catalogue additions
status: open
priority: P3
area: docs
owner:
claimed_at:
created_at: 2026-10-05T16:08:28Z
completed_at:
branch:
depends_on: []
scope:
  - .agents/skills/animation-camera/references/camera-keywords.md
  - .agents/skills/animation-camera/references/model-misreads.md
  - .agents/skills/animation-camera/SKILL.md
  - .claude/skills/animation-camera/SKILL.md
  - .agents/skills/animation-production/references/error-catalogue.md
  - tools/animation-camera.test.mjs
  - tools/animation-production.test.mjs
---

# Animation skill references: prompt length per model, overlays are not depth, H3 format cross-check, error catalogue additions

## Why

The animation skills read camera words the models parse, but two facts the research found
are missing: each video model has a prompt-length sweet spot (Seedance 200–400 words, Veo
100–250, LTX ≤ 80, Runway ≤ 60, per the vendors' guides) and overlays (titles, HUD, arrows)
must never be asked from the video model as scene depth. The error catalogue also lacks the
failure modes the Seedance / H3 skill packs documented (CJK quotes dropping tasks,
sensitive-word refusals, prompt length caps, style-fingerprint drift).

## Definition of done

- [ ] `camera-keywords.md` has a table of prompt-length sweet spots per model (Hailuo 2.3 / H3,
      Kling, Veo, Omni) with the official page and the read date, and the "overlays, not
      depth" rule; `model-misreads.md` cross-checks `H3_FIRST_LINE` in `shot_plan.mjs` against
      MiniMax's current prompt format and records any discrepancy.
- [ ] `error-catalogue.md` gains: CJK quoting in prompts, a sensitive-word table (MiniMax /
      Kling refusals seen), the prompt length cap, style-fingerprint drift between the look
      sheet and later shots — each with the detection and the fix.
- [ ] `tools/animation-camera.test.mjs` and `tools/animation-production.test.mjs` still pass
      (they pin wording); `SKILL.md` copies stay byte-identical (`npm run test:tools`).

## Steps

- [ ] Read the vendors' prompt guides (Seedance, Veo, Kling, MiniMax H3 official skill), write
      the table, the rule and the catalogue rows.

## How to verify

```bash
node --test tools/animation-camera.test.mjs tools/animation-production.test.mjs tools/skills.test.mjs
```

## Notes

- Docs only; `providers-and-plans.md` / `route-decisions.md` belong to
  `2026-10-04-paid-verification-hailuo-kling-web` and are not touched.
- Sources by name: smixs/visual-skills (CC BY 4.0), MiniMax-AI/MiniMax-H3 (official skill),
  ayase0307/h3-video-prompting, A-cat-with-carrots/OnlyShot (MIT) — facts and wording, no code.
