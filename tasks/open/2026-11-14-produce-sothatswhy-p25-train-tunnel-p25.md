---
id: 2026-11-14-produce-sothatswhy-p25-train-tunnel-p25
title: Produce sothatswhy-p25-train-tunnel (P25 train tunnel pressure wave) with theatrical gouache keyframes and 8-locale MiniMax dubs
status: in-progress
priority: P2
area: docs
owner: antigravity-gemini
claimed_at: 2026-11-14T07:27:27Z
created_at: 2026-11-14T07:27:17Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/sothatswhy-p25-train-tunnel
  - docs/videos/lessons/sothatswhy.md
---

# Produce sothatswhy-p25-train-tunnel (P25 train tunnel pressure wave)

## Why
Produce episode P25 of 《原來如此事務所》 (`sothatswhy-p25-train-tunnel`), covering why high-speed bullet train noses are elongated for tunnel micro-pressure waves rather than aerodynamic drag, using Gemini TTS for Chinese and MiniMax for 8-language dubs, upgrading visuals to the owner-mandated "theatrical anime lighting x rich gouache editorial illustration" standard without MiniMax image generation.

## Definition of done
- [x] Topic verified with primary sources (RTRI, Saito 2015, Ozawa 1995, Harada 2003, Nakatsu 2018, Crandell 2019, THSRC/JR West).
- [x] Canonical `brief.md`, `claims.md`, `video.json`, `script.md` created with 146 lines, 17 loops, 0 lint errors.
- [x] Independent fact check `verify-1.md` complete (146 OK / 0 FIX).
- [x] Chinese audio synthesized with Gemini (`Sulafat` / `Leda`, pace 5.03 chars/s), pronunciation hints tuned (`仲津`, `截面`), `audio` gate approved.
- [x] 8-language translation sheets translated, verified, and merged into `i18n/*.json`.
- [x] Series visual upgrade formula established: High-craft 2D theatrical anime and rich gouache editorial illustration (16:9 full bleed, warm-sepia tapered ink linework, warm golden directional window sunlight with glowing rim light and dust motes, creamy shallow depth-of-field bokeh, rich multi-layered fabric/wood/metal textures, zero text/letters).
- [x] Upgraded 68-shot prompt manifest generated: `theatrical_prompts.json`.
- [x] New visual standard codified in `docs/videos/lessons/sothatswhy.md`.
- [x] MiniMax foreign dubs:
  - [x] `en`: `dubs/en.m4a` generated and verified.
  - [x] `es`: `dubs/es.m4a` generated and verified.
  - [x] `ja`: `dubs/ja.m4a` generated and verified.
  - [x] `ko`: `dubs/ko.m4a` generated and verified.
  - [ ] `pt`, `id`, `vi`, `th`: pending MiniMax account balance refill (pt synthesized 34/68 lines).
- [x] Audience Review complete: independent blind review scored 36.0/40 (S-tier viral potential), codified into `docs/videos/so-thats-why/dialogue-pilot-20261103/README.md` and `docs/videos/lessons/sothatswhy.md`.
- [x] Audience Review refinements applied: 3 script lines (Shot 31 `paraboloid-winner`, Shot 44 `kingfisher-beak-study`, Shot 61 `new-train-wing`) polished, Chinese TTS re-synthesized via Gemini (08:09, 5.03 chars/s), and `audio` gate re-approved (sha256 `8982aaa7b49c`).
- [ ] Upgraded keyframe generation via `generate_image`: 36/68 shots generated and imported (`--provider external --usd 0`); remaining 32 shots pending `gemini-3.1-flash-image` quota window.
- [ ] 2x zoom independent review and final storyboard approval.
- [ ] Assemble final video, captions, 11/11 QA, review-push, and Google Drive backup.

## How to verify
```bash
node tools/video/cli.mjs lint --slug sothatswhy-p25-train-tunnel
node tools/video/cli.mjs check-audio --slug sothatswhy-p25-train-tunnel
ls -lh /home/antigravity/mokaair-work/videos/sothatswhy-p25-train-tunnel/dubs/*.m4a
```

## Notes
- `gemini-3.1-flash-image` daily quota hit after generating 24 keyframes; per user mandate, strictly do not fall back to MiniMax for image generation. Wait for quota reset to complete remaining 44 keyframes.
- MiniMax voice synthesis API returned balance limit on `pt` scene 34; scenes 1-34 cached locally. Resuming will reuse existing clips without double-billing.
