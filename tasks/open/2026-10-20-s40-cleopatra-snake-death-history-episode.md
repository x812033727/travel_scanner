---
id: 2026-10-20-s40-cleopatra-snake-death-history-episode
title: S40 Cleopatra snake death history episode
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T00:14:38Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s40
---

# S40 Cleopatra snake death history episode

## Why

Make a source-bounded Curio S40 about whether Cleopatra VII definitely died by a snake bite. The prior candidate memo had only Plutarch; this preproduction reopens him and adds Suetonius and Cassius Dio without treating any of the later authors as an eyewitness.

## Definition of done

- [x] Reopen fixed Plutarch full text and at least one separate ancient author; record versions and witness limits.
- [x] Draft two historically sound options, a 8+ minute story body, claims, shots and loop map, with lint at 0 errors and warnings.
- [ ] Pass new independent script-only 13-question blind read and a separate source/prompt audit of exact script hash.
- [ ] Only after gates and whole-episode budget record, progress paid TTS, stills, music and final package.

## Steps

- [x] Pin full Plutarch, Suetonius and Dio translations with SHA-256 and passage scope in `research.md`.
- [x] Write `brief.md`, `video.json`, generated `script.md`, `claims.md`, and `verify-1.md` under `docs/videos/curio-s40`.
- [x] Resolve R1 blind (8/13) and source/prompt reviewer findings in R2, then regenerate and re-run local gates.
- [ ] Pass fresh R2 script-only blind and source/prompt audit on exact R2 hash.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s40 --json` reports 0 errors/0 warnings on R2. Run `node tools/video/cli.mjs narrative --slug curio-s40` for a fresh script-only reviewer, then record its 13 answers formally. `npm run test:docs-videos` and `npm run check:tasks` passed; R2 hashes and known limits are in `docs/videos/curio-s40/verify-2.md`.

## Notes

R1 independent script-only blind 8/13 and source/prompt audit are preserved as `verify-r1-blind.md` and `verify-r1-source-visual.md`; R2 repair in `verify-2.md`. R2 `video.json` SHA-256 `d0b200ac4027daa5c578595d40a79b3c6cf9f0af36feb47db13bd7dfeba7433f`: 86 spoken lines, 85 still shots + outro, estimated story body 8:35 and full length about 9:19, 23 loops, lint 0/0. Exact hash must be refreshed after any later edit. Sources and line-level qualification in `research.md`; do not convert `what really took place is known to no one` to a no-snake claim. No paid media. Fresh independent R2 blind/source audit requested from coordinator.
