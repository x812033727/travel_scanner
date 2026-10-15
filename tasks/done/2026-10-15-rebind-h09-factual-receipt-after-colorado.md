---
id: 2026-10-15-rebind-h09-factual-receipt-after-colorado
title: Rebind H09 factual receipt after Colorado correction
status: done
priority: P2
area: docs
owner: codex-gpt6-h09-new-source-receipt
claimed_at: 2026-10-15T03:44:41Z
created_at: 2026-10-15T03:44:33Z
completed_at: 2026-10-15T03:47:14Z
branch: codex/curio-h09-earhart-20261015
depends_on: []
scope:
  - docs/videos/curio-h09/verify-1.md
---

# Rebind H09 factual receipt after Colorado correction

## Why

Correcting B06 from cruiser to battleship changed the formal H09 script SHA-256 from D63D46A3… to E9404ADD…. The prior source receipt was bound to the old hash; a separate reviewer must verify the correction against primary U.S. Navy sources and confirm the remaining narration before the owner approves the new script.

## Definition of done

- [x] `verify-1.md` binds the E9404ADD… formal script, 011C1AC5… draft and AED33CE8… claims hashes.
- [x] B06 ship class and O3U aircraft are checked against U.S. Navy sources; 99 unchanged formal lines retain their prior source review; Purdue cutoff is refreshed.

## Steps

- [x] Compared all 100 formal narration lines with the previous D63D46A3… script, current `video.json` and the joined 95 editorial lines; only formal line 26/B06 changed.
- [x] Checked U.S. Navy aviation history, BB-45 ship history and photo description for the ship and floatplanes; rechecked the Purdue Oct. 14 article and PRF announcement list.
- [x] Updated only the claimed receipt and this task file; ran task and whitespace checks.

## How to verify

`Get-FileHash -Algorithm SHA256` for `script.md`, `script-draft.md`, `claims.md`; Node comparison of 100 formal lines with `video.json`, 95 joined draft lines and `screenplay(video.json)`; `npm run check:tasks`; `git diff --check`.

## Notes

U.S. Navy Naval Aviation history calls Colorado a battleship (BB-45) and states that three O3U Corsair observation floatplanes began aerial searches July 7, 1937. Navy ship history and photo captions corroborate the BB-45/O3U-3 identities. The formal script delta is exactly `巡洋艦` to `戰艦` at segment 26 plus generated footer hashes; all 99 other narration lines are unchanged. Current PRF expedition list still ends with the Oct. 14 underwater survey; Purdue says conclusions are premature. The Navy full-page fetch returned 502, but primary-site search indexing returned its text, cross-checked against two other Navy pages. This factual receipt does not approve E940 audio, illustration or publication.
