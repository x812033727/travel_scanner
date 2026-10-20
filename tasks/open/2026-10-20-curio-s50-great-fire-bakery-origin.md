---
id: 2026-10-20-curio-s50-great-fire-bakery-origin
title: Curio S50 Great Fire bakery origin sourced preproduction
status: open
priority: P2
area: docs
owner:
claimed_at:
created_at: 2026-10-20T15:02:41Z
completed_at:
branch:
depends_on: []
scope:
  - docs/videos/curio-s50
---

# Curio S50 Great Fire bakery origin sourced preproduction

## Why

The next Curio history long video needs a distinct, sourced story. S38 already follows Pepys evacuating possessions during the Great Fire; S50 asks the narrower question whether the baker's oven can be blamed for “destroying London.” A preproduction draft must keep the recorded starting house, unknown ignition method, and conditions that spread the fire at different evidence levels.

## Definition of done

- [x] A recommended A/B brief, line cited research and claim map, Traditional Chinese 8+ minute body script, and matching Curio `video.json` exist under `docs/videos/curio-s50`.
- [x] The exact content hashes, author only selfcheck, lint result, and known source access limits are recorded in `docs/videos/curio-s50/author-selfcheck.md`.
- [ ] Independent source review and two different blind readers assess the same pinned script hash; any corrections are applied before site outline/script approval.
- [ ] The site and production gates accept the revised script and completed video, including measured TTS body duration and final 16 second Studio end screen links.

## Steps

- [x] Read series skills, compare S01–S49 topics, and keep S50 separate from S38/P17.
- [x] Read pinned Pepys, 1667 testimony booklet and Vincent text; cite exact lines and raw byte hashes.
- [x] Draft A/B, recommend A, write 116 scene story, 119 spoken lines and matched claim rows.
- [x] Fix Pepys Tower sequence and narrow witness/fireline claims after a read only source audit.
- [x] Run lint and exact text mapping; write author selfcheck and hash manifest.
- [ ] Reopen Gazette and London Museum from a network that allows them; review `fire037` and `fire108` and all other source boundaries independently.
- [ ] Obtain two blind narrative reads on the same final hash, then route site outline/script review.
- [ ] Plan and authorize full media budget before TTS, MiniMax images or music; complete downstream audio, storyboard, final and Studio checks.

## How to verify

From the repo root, run `node tools/video/cli.mjs lint --slug curio-s50 --json`, then `sha256sum docs/videos/curio-s50/{brief,research,claims,video,script}.*` with explicit file names as listed in `author-selfcheck.md`. Compare all 119 JSON spoken lines against the same IDs in `claims.md` and in order against `script.md`. `npm run check:tasks` validates this ticket; preexisting stale claim and scope overlap warnings elsewhere do not fail it. Later, measure the generated TTS body from after the first 8 scenes to the last story scene and inspect the 21 second outro, with Studio links active during its last 16 seconds.

## Notes

- 2026-10-20: Author preproduction is complete. The content hash table and source byte hashes are in `docs/videos/curio-s50/author-selfcheck.md`. No independent source signoff, blind review, website approval, TTS, illustrations, music, upload or Studio work has been done.
- Pepys diary, the 1667 printed testimony and Vincent's account were downloaded at fixed Git commits and read directly. London Gazette issue 85 and London Museum returned HTTP 403 here. Their limited wording relies on repository P17 research from 2026-10-12 and must be checked afresh by the independent source reviewer. `fire037` cites Gazette and `fire108` cites Museum; do not label them verified today.
- A is the recommended local outline. At 250/300/325 CPM, the planned 8 scene cold open estimates 50.1/43.0/40.5 seconds and the later story body 624.9/537.4/506.2 seconds including scene pauses. Actual TTS duration remains a gate.
- Three card scenes are `fire029` (Pepys address), `fire079` (13,200 houses), and `fire095` (Farriner testimony). Other story scenes are illustrative `shot`; do not present them as historical images. Put the original 5 second intro after chapter one, use the shared 21 second v4 end screen, and set Studio elements to the final 16 seconds.
