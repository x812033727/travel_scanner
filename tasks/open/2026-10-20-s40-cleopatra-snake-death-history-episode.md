---
id: 2026-10-20-s40-cleopatra-snake-death-history-episode
title: S40 Cleopatra snake death history episode
status: in-progress
priority: P2
area: docs
owner: codex-s40-preprod
claimed_at: 2026-10-20T00:14:40Z
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
- [ ] Resolve fresh blind and source reviewer findings, then re-run all gates for changed hash.

## How to verify

`VIDEO_WORKDIR=/workspace/.video-work node tools/video/cli.mjs lint --slug curio-s40 --json` must report 0 errors/0 warnings. Run `node tools/video/cli.mjs narrative --slug curio-s40` for a fresh script-only reviewer, then record its 13 answers formally. Run `npm run test:docs-videos` and `npm run check:tasks` before push. The script hash and known limits are in `docs/videos/curio-s40/verify-1.md`.

## Notes

Preproduction only. `video.json` SHA-256 `0ba27dd49a63d8f8ed2abc6638bf8f9b772ca60470c460dd87a6aef6d70d9475` at draft: 85 spoken lines, 84 still shots + outro, estimated story body 8:41 and full length about 9:24, 20 loops, lint 0/0. Exact video hash must be refreshed if any later edit. Sources and line-level qualification in `research.md`; do not convert `what really took place is known to no one` to a no-snake claim. No paid media. Fresh independent blind/source audit requested from coordinator.
