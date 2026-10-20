---
id: 2026-10-19-curio-s31-r2-source-and-prompt
title: Curio S31 R2 source and prompt corrections
status: in-progress
priority: P2
area: docs
owner: codex-gpt6-s31
claimed_at: 2026-10-19T23:59:43Z
created_at: 2026-10-19T23:59:38Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s31
---

# Curio S31 R2 source and prompt corrections

## Why

Independent source/visual gate [verify-2.md](../../docs/videos/curio-s31/verify-2.md) blocked S31's frozen script SHA `72eb00f5f0f05268dc9125705c3e75eaea98b8b933e2471fb42cf6e28762826c` before audio. The opening linked Du Mu's poetic horse to a later history's relay; the fruit timing could read as additive; Bai Juyi's held fruit and elderly likeness, anachronistic history copyist, written place cards, and a jar for `荔枝煎` asserted details the sources do not give. Make a new source-safe R2 package and review it anew.

## Definition of done

- [ ] Script, claims and still prompts remove the blocked source assertions and visual specificity, while keeping the story body above eight minutes.
- [ ] Fresh context-isolated official 13-question narrative panel and independent source/visual audit pass against the same R2 SHA; lint remains 0 errors/0 warnings.
- [ ] R2 verify/handoff records exact script/video/claims SHA values and states audio and paid media remain unstarted.

## Steps

- [x] Revise the blocked narration and prompts, regenerate `video.json`, `claims.md`, `script.md`; compare all 97 IDs and rerun lint.
- [ ] Obtain new independent panel and source/visual gate, resolve findings, then record R2 verification.
- [ ] Commit and push scoped S31 changes without touching other agents' staged files.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`; `node tools/video/cli.mjs script --slug curio-s31`; `node tools/video/cli.mjs narrative --slug curio-s31 --answers <new-blind-answers> --workdir <new-blind-workdir>`; compare 97 lines in script/claims/video; independently read all still prompts against pinned texts; `npm run test:docs-videos`; `npm run check:tasks`.

## Notes

Working R2 script SHA `d6e2825bb35adbb7bd2b101821b27b4fe32394f7d8e35b166c594a3b9179089e`; video SHA `16cd9d5526c6a563ccc8778ab55b49001e451b0a5c8265cc1d6ef4d160e1f2b5`; claims SHA `398e18988ba11e09dbab2c09a6cdeab728e5567195c02089a5c6c472c387aefe`. Lint 0/0, 97 scenes including outro, 96 still prompts, 18 loops. Chapter title now says Bai commissioned the drawing. Fresh reviews pending. No TTS, image generation, music or assembly.
