---
id: 2026-10-05-animation-skill-references-prompt-facts
title: Animation skill references: prompt length per model, overlays are not depth, H3 format cross-check, error catalogue additions
status: done
priority: P3
area: docs
owner: claude-fable-5-1-skilldocs
claimed_at: 2026-10-05T16:23:58Z
created_at: 2026-10-05T16:08:28Z
completed_at: 2026-10-05T16:45:07Z
branch: claude/animation-skill-prompt-facts
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

- [x] `camera-keywords.md` has a table of prompt-length sweet spots per model (Hailuo 2.3 / H3,
      Kling, Veo, Omni) with the official page and the read date, and the "overlays, not
      depth" rule; `model-misreads.md` cross-checks `H3_FIRST_LINE` in `shot_plan.mjs` against
      MiniMax's current prompt format and records any discrepancy.
- [x] `error-catalogue.md` gains: CJK quoting in prompts, a sensitive-word table (MiniMax /
      Kling refusals seen), the prompt length cap, style-fingerprint drift between the look
      sheet and later shots — each with the detection and the fix.
- [x] `tools/animation-camera.test.mjs` and `tools/animation-production.test.mjs` still pass
      (they pin wording); `SKILL.md` copies stay byte-identical (`npm run test:tools`).

## Steps

- [x] Read the vendors' prompt guides (Seedance, Veo, Kling, MiniMax H3 official skill), write
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
- What the official pages said (all read 2026-10-05):
  - MiniMax `platform.minimax.io` v2 create (H3 / H3-Max): `text` ≤ 7,000 characters per item,
    first/last frame ≤ 1 each, no negative field; the guides page repeats "Prompt length limit
    ≤ 7000 characters"; i2v (Hailuo 2.3 / 02 / Director): `prompt` ≤ 2,000 characters, 15 bracket
    camera commands, ≤ 3 per bracket recommended, `prompt_optimizer` default true; error codes
    1026 `input new_sensitive`, 1027 `output new_sensitive`, 2013 invalid params. None of the
    pages shows a date.
  - Hugging Face `MiniMaxAI/MiniMax-H3` (model card last modified 2026-08-13): base guide has the
    I2VA first line verbatim as `H3_FIRST_LINE`, the three fields, "one blank line" after the
    instruction, camera = motion type + amplitude + speed with only `at slow speed` / `at fast
    speed`, on-screen text in English double quotes, no word count; the ref guide has the six
    sections and "normally 350-500 English words" for `detailed_description`. The GitHub
    `skills/h3-prompt-writing/SKILL.md` names those two guides as its references and adds only
    "match the total duration to 4–15 seconds".
  - Kling: the VIDEO 3.0 user guide (2026-02-06) has no length rule, only examples (31 / 216 /
    220 / 317 words counted); the API reference pages on kling.ai are an SPA and come back as a
    bare shell, so the 2,500-character cap is cited from the discontinued official doc on
    docs.qingque.cn (changelog 2024-09-19, doc last updated 2025-06-19); the official error-code
    page is the same shell, so 1301 is cited from API users' summaries and marked so.
  - Google: `ai.google.dev/gemini-api/docs/veo` (updated 2026-09-17) lists 1,024 tokens of text
    input for `veo-3.1-generate-preview`, `-fast-` and `-lite-`; the Veo prompt guide now lives at
    `docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/video-gen-prompt-guide`
    (the cloud.google.com URL in the ticket redirects there; updated 2026-10-01), covers Veo and
    Omni, gives structure and vocabulary but no length, and says negative prompts are noun
    lists, not "no"/"don't"; `ai.google.dev/gemini-api/docs/omni` (updated 2026-09-23) has no
    length either, says Omni Flash cuts into several shots by default unless the prompt asks
    for a single continuous shot, and that over-descriptive prompts cause unintended edits.
- Community figures that were verified today: smixs `veo.md` 50–200 words (compress to 50–100
  when the model cherry-picks), smixs `kling.md` 50–80 words for 2.5/2.6, ~30–60 per shot for
  3.0, 20–40 for image-to-video; ayase0307 300–700 English words for text-only H3, shorter with
  references; OnlyShot ≤ 1,500 characters for the Jimeng CLI (`ret=1046 InvalidNode`), with its
  sensitive-word table and the bash-eval / full-width `）` failures.
- Not verified: the Seedance 200–400, LTX-2 ≤ 80, Runway Gen-4 ≤ 60 and Sora 2 100–250 figures the
  2026-10-05 research recorded were not found again in the named sources (smixs's
  `universal-rules.md` carries no numbers), so they are listed as secondary without a page; the
  Hailuo and Kling web input-box limits; whether Hailuo refunds a moderated clip; whether the
  blank line between H3 fields or the `no on-screen text` negation changes H3's output (both
  left to the pilot). GitHub's API and codeload were blocked for foreign repos in this session;
  the source files were read through raw.githubusercontent.com instead.
- Found while reading, filed for the owner of `shot_plan.mjs`:
  `2026-10-05-shot-plan-h3-body-official-i2va` (style word and `<Picture 1>` anchor first in
  `[Shot 1]`, no `at a steady speed`, FL2VA line for end-frame shots).
