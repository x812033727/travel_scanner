---
id: 2026-10-20-curio-s39-independent-review
title: Fresh blind and source review for S39 Caesar R1
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T00:20:56Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s39/verify-2.md
  - docs/videos/curio-s39/narrative-1.json
---

# Fresh blind and source review for S39 Caesar R1

## Why

S39 has a source-backed R1 preproduction script, but the author cannot independently pass the 13-question narrative gate or validate their own line and image-prompt choices. No media can start until another reader checks the exact hash.

## Definition of done

- [ ] A new-context reader seals all 13 official narrative answers from the script alone before opening author notes, source, or old results.
- [ ] Independent checker compares all 93 spoken lines and 90 image prompts with the fixed source passages, marking each claim and any misleading visual.
- [ ] Write a pass/hold decision tied to exact SHA-256, with actionable IDs; if passed, official `narrative --answers` record and source result are saved.

## Steps

- [ ] Take this ticket with a fresh context and read `node tools/video/cli.mjs narrative --slug curio-s39` only. Seal a JSON answer for all 13 IDs and evidence in `docs/videos/curio-s39/narrative-1.json`.
- [ ] After sealing, read [research.md](../../docs/videos/curio-s39/research.md), pinned texts, [claims.md](../../docs/videos/curio-s39/claims.md) and `video.json`; specifically check Marcus vs Decimus, Greek vs Latin, `etsi tradiderunt quidam`, later editor footnote, Plutarch English translation, violence-free prompts and manuscript text.
- [ ] Write `docs/videos/curio-s39/verify-2.md` with exact observed hashes and pass/hold. On any failure, leave media held and notify the R1 author/root of line IDs. On pass, run `narrative --slug curio-s39 --answers docs/videos/curio-s39/narrative-1.json` and include result.

## How to verify

`node tools/video/cli.mjs lint --slug curio-s39 --json` must remain 0 error / 0 warning. Compare against R1 `video.json` SHA-256 `cfd7ffda2bdfb98e7cd6d0ad9a909878ee92f3fcbabf4aa18a96c4276797e344` and script SHA-256 `ede55e6eb8a7873c2b962c33176312e8bd4c2efcfb2bfaab6c74374f3d2e4d64`; if changed, stop and request fresh review of the new hash. Avoid reading `verify-1.md` before the blind judgment.

## Notes

Do not start TTS, music, or keyframes in this review task. The independent check must say explicitly whether any statement turns a conditional ancient report into a confirmed last line or projects a modern editor's Latin guess into Suetonius's original.
