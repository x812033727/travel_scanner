---
id: 2026-10-20-curio-s39-caesar-last-words
title: Produce S39 Caesar last words preproduction
status: done
priority: P2
area: docs
owner: codex-s39-caesar
claimed_at: 2026-10-20T00:09:50Z
created_at: 2026-10-20T00:09:48Z
completed_at: 2026-10-20T00:21:12Z
branch:
depends_on: []
scope:
  - docs/videos/curio-s39
---

# Produce S39 Caesar last words preproduction

## Why

The next Curio S-axis history episode asks if Caesar really said `Et tu, Brute?` as his last words. Pinned Suetonius Latin and Shakespeare drama disagree in language and certainty; a reliable episode must keep the ancient author's reported alternative and a later editor's conjecture distinct.

## Definition of done

- [x] Reopen and hash Suetonius Latin and two English translations, Plutarch's *Caesar*/*Brutus*, and Shakespeare's III.i.
- [x] Deliver two historically bounded options, R1 research, per-line claims, 8+ minute script, 90 period-safe prompts, and 8+ concrete loops.
- [x] Run video lint and relevant repository checks; leave an explicit independent-review handoff with no media started.

## Steps

- [x] Write `research.md`, `brief.md`, `video.json`, generated `script.md`, `claims.md`, and author `verify-1.md` under `docs/videos/curio-s39`.
- [x] Separate Marcus and Decimus Brutus; distinguish Suetonius `etsi tradiderunt quidam` + Greek phrase from Shakespeare Latin and later Thomson/Forester footnote.
- [x] Run lint at 0 errors and 0 warnings, dry-run TTS and keyframe quotes, `npm run test:docs-videos`, and `npm run check:tasks`.
- [x] File a separate, unclaimed fresh-reader/source-review task; no TTS, MiniMax, or music order on this preproduction task.

## How to verify

Run `node tools/video/cli.mjs lint --slug curio-s39 --json` and `node tools/video/cli.mjs narrative --slug curio-s39`; inspect [verify-1.md](../../docs/videos/curio-s39/verify-1.md) and SHA-256 there. The current script must still receive a new-context official 13-question blind reader and independent source/prompt review before audio or paid images. `npm run test:docs-videos` passed 236/236 and `npm run check:tasks` exited 0 on 2026-10-20.

## Notes

R1 has 93 spoken lines, 90 illustrations, 19 loops, video SHA-256 `cfd7ffda2bdfb98e7cd6d0ad9a909878ee92f3fcbabf4aa18a96c4276797e344`, script SHA-256 `ede55e6eb8a7873c2b962c33176312e8bd4c2efcfb2bfaab6c74374f3d2e4d64`, and estimated 8:45 story body. This author self-check is not an independent narrative/source sign-off. MiniMax dry-run maximum three tries US$3.65 for all 90 shots; allow roughly US$0.08 music before recording a whole-episode cap of US$3.73. No paid media has been ordered.
