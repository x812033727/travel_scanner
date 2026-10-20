---
id: 2026-10-19-curio-s31-r2-source-and-prompt
title: Curio S31 source and prompt corrections through R5
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

# Curio S31 source and prompt corrections through R5

## Why

Independent source/visual gate [verify-2.md](../../docs/videos/curio-s31/verify-2.md) blocked S31's frozen script SHA `72eb00f5f0f05268dc9125705c3e75eaea98b8b933e2471fb42cf6e28762826c` before audio. The opening linked Du Mu's poetic horse to a later history's relay; the fruit timing could read as additive; Bai Juyi's held fruit and elderly likeness, anachronistic history copyist, written place cards, and a jar for `荔枝煎` asserted details the sources do not give. Make a new source-safe R2 package and review it anew.

## Definition of done

- [x] Script, claims and still prompts remove the blocked source assertions and visual specificity, while keeping the story body above eight minutes.
- [ ] Fresh context-isolated official 13-question narrative panel and independent source/visual audit pass against the same final SHA; lint remains 0 errors/0 warnings.
- [x] R2–R5 handoffs record exact script/video/claims SHA values and state audio and paid media remain unstarted.

## Steps

- [x] Revise the blocked narration and prompts, regenerate `video.json`, `claims.md`, `script.md`; compare all 97 IDs and rerun lint.
- [ ] Obtain new independent panel and source/visual gate on R5, resolve findings, then record final verification.
- [x] Commit and push scoped S31 changes without touching other agents' staged files.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s31`; `node tools/video/cli.mjs script --slug curio-s31`; `node tools/video/cli.mjs narrative --slug curio-s31 --answers <new-blind-answers> --workdir <new-blind-workdir>`; compare 97 lines in script/claims/video; independently read all still prompts against pinned texts; `npm run test:docs-videos`; `npm run check:tasks`.

## Notes

R2 script SHA `d6e2825bb35adbb7bd2b101821b27b4fe32394f7d8e35b166c594a3b9179089e` received a fresh official blind panel: 12/13 YES, blocked solely on repeated recap at ly063/066 and ly054–057/090, ly083/091. The sealed receipt is `/tmp/curio_s31_r2_narrative_blind.md`. R3 removes those repetitions by advancing Bai's text at ly066 and making ly090–ly092 an on-page erase action; R3 script SHA `cfc5a32d15d7e5cca20f972aca6dfdb2810a96fe8791d23c70da2188d20dfb5a`, video SHA `a5fdecb15ee4e4eb273db018ec3b6db6a30c4ed27d37d2c315460bf477b527a7`, claims SHA `addcf78f2ded2e3a8778b7c59b176151a15742c09de52ea9803534c53a03f72f`. Lint 0/0, 97 scenes including outro, 96 still prompts, 10 matched loops. No TTS, image generation, music or assembly.

R3 fresh context-isolated official panel again yielded 12/13 YES, with only `no_recap` NO: ly037/038 immediately repeated the unchanged-taste arrival fact, and ly052/053 restated Guangzhou tribute. The sealed receipt is `/tmp/curio_s31_r3_fresh_narrative_blind.md`. R4 makes ly038 flip back to Du Mu's palace scene and ask whether the history joins it; ly053 now puts the two records together and searches for a shared shipment mark. R4 script SHA `899dd8510fbd1a45e0596682df38c6ea18600c356681369ff2ffbde36d56c592`, video SHA `8ebe96c889a8bb20d0d2e341864e7d037232eed0da015df035a924c3c8cd0a86`, claims SHA `eae4a0838b10184975ec50e747934db18659befc67c8eba9a761b73d88fd970b`; the pending review conditions are recorded in [verify-5.md](../../docs/videos/curio-s31/verify-5.md). No media has been made.

R4's independent narrative panel passed 13/13, but the subsequent primary-text and 96-prompt audit blocked on an invented birthday banquet at ly045, a palace-receipt cue at ly037, and a smell/taste mismatch at ly077; it also noted ly016/ly021 precision and missing `NBG` citations at ly076/ly078. R5 applies all corrections and is frozen in [verify-6.md](../../docs/videos/curio-s31/verify-6.md): script SHA `332c875a835f89b428c124f578c380079976b9e35b396d098b086a56ba08cef2`, video SHA `4a0d0bc19c5b2ebbf6982a58a6c1331b6527b6fca4d02a5230e15edeae74c754`, claims SHA `83063009c6fec93840e0e6043118f7ed2df691b3e38651bc1590f12ad0ec2127`. Lint 0/0, 97 aligned lines, 96 still prompts, 10 loops, body above eight minutes; fresh reviews pending. No TTS, image generation, music or assembly.
