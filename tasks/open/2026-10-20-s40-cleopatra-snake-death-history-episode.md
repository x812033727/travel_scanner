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
- [x] Receive fresh R2 script-only blind (10/13) and source/prompt audit; preserve reports and resolve cited issues in R3.
- [ ] Pass fresh R3 script-only blind and source/prompt audit on exact R3 hash.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s40 --json` reports 0 errors/0 warnings on R3. Run `node tools/video/cli.mjs narrative --slug curio-s40` for a fresh script-only reviewer, then record its 13 answers formally. `npm run test:docs-videos` and `npm run check:tasks` passed; R3 hashes and known limits are in `docs/videos/curio-s40/verify-3.md`.

## Notes

R1 independent script-only blind 8/13 and source/prompt audit are preserved as `verify-r1-blind.md` and `verify-r1-source-visual.md`; R2 repair in `verify-2.md`. Fresh R2 blind 10/13 and source/prompt audit are preserved as `verify-r2-blind.md` and `verify-r2-source-visual.md`. R3 repair in `verify-3.md`. R3 `video.json` SHA-256 `1a12e15009519b03a0a09cda577fe0be12cc58ea0aa51b002cd20208f6f3394e`: 84 spoken lines, 83 still shots + outro, estimated story body 8:33 and full length about 9:16, 25 loops, lint 0/0. Exact hash must be refreshed after any later edit. Sources and line-level qualification in `research.md`; do not convert `what really took place is known to no one` to a no-snake claim. No paid media. Fresh independent R3 blind/source audit needed.
