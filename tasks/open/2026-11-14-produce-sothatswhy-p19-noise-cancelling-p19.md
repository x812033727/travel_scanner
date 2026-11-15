---
id: 2026-11-14-produce-sothatswhy-p19-noise-cancelling-p19
title: Produce sothatswhy-p19-noise-cancelling (P19 active noise cancellation) with theatrical gouache keyframes
status: in-progress
priority: P2
area: docs
owner: antigravity-gemini
claimed_at: 2026-11-14T14:09:45Z
created_at: 2026-11-14T14:09:32Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/sothatswhy-p19-noise-cancelling
---

# Produce sothatswhy-p19-noise-cancelling (P19 active noise cancellation) with theatrical gouache keyframes

## Why

Episode P19 of 《原來如此事務所》 tackles a universal question everyday headphone wearers face:
"Why does my active noise cancelling (ANC) headphone silence the loud rumble of a subway train or jet engine in an instant, but leaves my coworker's conversation crystal clear right next to me?"
This episode explains the core physical reality: ANC does not absorb sound like a sponge; it plays a *second* inverted-phase sound into the ear canal, causing destructive interference. Low frequencies have long wavelengths (100 Hz = 3.4 m) that form a uniform "zone of quiet" in a 2 cm ear canal with high tolerance, while engine noise is periodic and predictable by DSP algorithms. In contrast, human speech consists of short wavelengths (2000 Hz = 17 cm) where a 0.5 cm shift causes constructive interference (screeching), and non-stationary random plosives that hardware latency cannot predict. Furthermore, bone conduction transmits the speaker's own voice through skull vibration, completely bypassing the ear canal.

## Definition of done

- [x] Pre-production fact-checking and scorecard complete: `brief.md`, `claims.md`, `verify-1.md` (100% OK), `SCORECARD.md` (40/40).
- [x] 8+ minute explainer dialogue script: 76 scenes, 150 lines, 2091 characters (8.6 minutes), 19 causal loops, passing `cli.mjs lint` with 0 errors.
- [x] Gemini Chinese TTS synthesized: Chief (`Sulafat`) and Kid (`Leda`) at 5.18 chars/s (exceeding >= 4.4 chars/s requirement).
- [x] Independent Audience Review conducted and archived: [AUDIENCE_REVIEW.md](docs/videos/sothatswhy-p19-noise-cancelling/AUDIENCE_REVIEW.md) scoring 37.7/40 (S-tier).
- [x] Chinese audio approved (`audio` gate approved: timeline.json sha256 3a9b268fb30d).
- [x] 8-language translations (`en, ja, ko, es, pt, id, vi, th`) completed and merged via `i18n-merge`.
- [x] 8-language dubs synthesized via MiniMax (`en, es, ja, ko, pt, id, vi, th` all complete with exit code 0, 0 window timing violations).
- [ ] 76 keyframes generated in upgraded theatrical anime gouache style via internal `generate_image` and imported via `keyframes import --provider external --usd 0`.
- [ ] Storyboard approved, assembled, captions verified, and backed up.

## Steps

- [x] Research physical acoustic claims and draft `brief.md` and `claims.md`.
- [x] Write `build_scenes.py`, freeze camera paths into `cameras.json`, and generate `video.json` and `script.md`.
- [x] Verify `node tools/video/cli.mjs lint --slug sothatswhy-p19-noise-cancelling` passes with 0 errors.
- [x] Synthesize Chinese TTS with Gemini (`Sulafat` / `Leda`): 150 lines, 5.18 chars/s.
- [x] Dispatch Blind Audience Reviewer subagent and archive report (Score 37.7/40).
- [x] Approve `audio` gate.
- [x] Complete 8-language translations and merge `i18n/*.json`.
- [x] Complete MiniMax 8-language dubs (`en, es, ja, ko, pt, id, vi, th`).
- [ ] Wait for `gemini-3.1-flash-image` quota reset (~17:57 UTC) and generate keyframes for both P25 (shots 25–68) and P19 (shots 1–76).

## How to verify

- `node tools/video/cli.mjs lint --slug sothatswhy-p19-noise-cancelling` (0 errors)
- `node tools/video/cli.mjs check-audio --slug sothatswhy-p19-noise-cancelling`
- `npm run check:tasks`

## Notes

- Visual Upgrade Recipe:
  High-craft 2D theatrical anime and rich gouache editorial illustration, 16:9 full-bleed edge-to-edge with zero borders. Delicate tapered warm-sepia ink linework on foreground subject (no heavy flat black outlines). Warm golden directional window sunlight casting glowing rim light along hair strands, glasses/hood, and object bevels, with subtle dust motes. Tactile multi-layered fabric fold shading, rich wood grain and material reflections. Creamy shallow depth-of-field painterly bokeh background with soft brushy edges and zero black outlines in the background. Clean blank surfaces, zero text/letters/numbers.
- Strictly wait for `gemini-3.1-flash-image` quota reset, strictly NO MiniMax for images.
- MiniMax is used for 8 foreign dubs (`en, ja, ko, es, pt, id, vi, th`).
